#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import ipaddress
import json
import os
import re
import shutil
import socket
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)
DEFAULT_WORKSPACE_PROXIES = (
    "http://127.0.0.1:8899",
)
DEFAULT_SHARE_LIMIT = 64 * 1024 * 1024
DEFAULT_FILE_LIMIT = 100 * 1024 * 1024
RSC_MARKER = "window.__reactRouterContext.streamController.enqueue("
URL_RE = re.compile(r"https?://[^\s<>\"'`]+", flags=re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)", flags=re.IGNORECASE)
FILE_LINK_LABEL_RE = re.compile(
    r"(?:download|file|report|research|artifact|скачать|файл|отч[её]т|исследован|"
    r"документ|выгрузк)",
    flags=re.IGNORECASE,
)
SPECIAL_LOCATOR_RE = re.compile(
    r"(?:sandbox:/{1,2}|file-service://|attachment://)[^\s<>\"'`]+",
    flags=re.IGNORECASE,
)
SHARE_PATH_RE = re.compile(r"^/(?:backend-api/)?share/([A-Za-z0-9-]+)")
FILE_EXTENSIONS = {
    ".7z",
    ".avi",
    ".csv",
    ".doc",
    ".docx",
    ".epub",
    ".fb3",
    ".gif",
    ".gz",
    ".jpeg",
    ".jpg",
    ".json",
    ".md",
    ".mov",
    ".mp3",
    ".mp4",
    ".ods",
    ".odt",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".tar",
    ".tgz",
    ".tsv",
    ".txt",
    ".wav",
    ".webm",
    ".webp",
    ".xls",
    ".xlsx",
    ".xml",
    ".yaml",
    ".yml",
    ".zip",
}
REDACTED_TEXTS = {
    "the output of this plugin was redacted.",
    "the output of this tool was redacted.",
}
EXCLUDED_CONTENT_TYPES = {
    "code",
    "computer_initialize_state",
    "execution_output",
    "model_editable_context",
    "reasoning_recap",
    "thoughts",
    "tool_result",
}
HIDDEN_METADATA_KEYS = {
    "is_system_message",
    "is_user_system_message",
    "is_visually_hidden_from_conversation",
}
EXPLICIT_FILE_KEYS = {
    "asset_pointer",
    "attachment_url",
    "download_url",
    "file_url",
    "sandbox_path",
    "source_file_url",
}
FILE_ID_KEYS = {
    "file_id",
    "openai_file_id",
    "openaiFileId",
}
FILENAME_KEYS = ("filename", "file_name", "name", "title")
MIME_KEYS = ("mime_type", "mimeType", "content_type")


class ExtractionError(RuntimeError):
    pass


class ResponseTooLarge(ExtractionError):
    pass


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> urllib.request.Request | None:
        if not _safe_public_download_url(newurl):
            raise urllib.error.HTTPError(
                newurl,
                403,
                "redirect to a non-public target was rejected",
                headers,
                fp,
            )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


@dataclass(frozen=True)
class Route:
    label: str
    proxy: str | None


@dataclass
class HttpResult:
    status: int | None
    content_type: str | None
    headers: dict[str, str]
    body: bytes
    final_url: str
    error: str | None = None


@dataclass
class FetchAttempt:
    route: str
    endpoint: str
    status: int | None
    content_type: str | None
    bytes: int
    error: str | None = None


@dataclass
class FetchedShare:
    share_id: str
    share_url: str
    data: dict[str, Any]
    method: str
    route: Route
    response_body: bytes
    response_sha256: str
    attempts: list[FetchAttempt]
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisibleMessage:
    sequence: int
    message_id: str | None
    role: str
    author_name: str | None
    create_time: str | None
    channel: str | None
    content_type: str | None
    text: str
    raw_message: dict[str, Any] = field(repr=False)

    def as_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "message_id": self.message_id,
            "role": self.role,
            "author_name": self.author_name,
            "create_time": self.create_time,
            "channel": self.channel,
            "content_type": self.content_type,
            "text": self.text,
        }


@dataclass
class ResearchReport:
    index: int
    title: str
    message_id: str | None
    text: str
    sha256: str
    metadata: dict[str, Any]
    source_urls: list[str]


@dataclass
class FileCandidate:
    locator: str
    source: str
    kind: str
    filename_hint: str | None = None
    mime_type: str | None = None


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def canonical_share_url(value: str) -> tuple[str, str]:
    parsed = urllib.parse.urlsplit(value.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ExtractionError("ChatGPT Share URL must use http or https")
    if parsed.hostname not in {"chatgpt.com", "www.chatgpt.com"}:
        raise ExtractionError("expected a chatgpt.com/share/... URL")
    match = SHARE_PATH_RE.match(parsed.path)
    if not match:
        raise ExtractionError("could not find a share id in the URL")
    share_id = match.group(1)
    return share_id, f"https://chatgpt.com/share/{share_id}"


def redact_proxy(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    host = parsed.hostname or "unknown"
    if parsed.port:
        host = f"{host}:{parsed.port}"
    return urllib.parse.urlunsplit((parsed.scheme, host, "", "", ""))


def _split_proxy_values(value: str | None) -> list[str]:
    if not value:
        return []
    return [item for item in re.split(r"[,;\s]+", value) if item]


def build_routes(explicit: list[str] | None) -> list[Route]:
    values = list(explicit or ["auto"])
    expanded: list[str] = []
    for value in values:
        if value == "auto":
            expanded.extend(_split_proxy_values(os.environ.get("CHATGPT_SHARE_PROXIES")))
            expanded.append("direct")
            expanded.extend(DEFAULT_WORKSPACE_PROXIES)
        else:
            expanded.append(value)

    routes: list[Route] = []
    seen: set[str] = set()
    for value in expanded:
        if value in {"", "none", "direct"}:
            key = "direct"
            route = Route(label="direct", proxy=None)
        else:
            parsed = urllib.parse.urlsplit(value)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname:
                raise ExtractionError(f"unsupported proxy URL: {value}")
            key = value.rstrip("/")
            route = Route(label=f"proxy:{redact_proxy(value)}", proxy=value)
        if key not in seen:
            seen.add(key)
            routes.append(route)
    if not routes:
        raise ExtractionError("no network routes configured")
    return routes


def _read_limited(response: Any, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(1024 * 1024, max_bytes - total + 1))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise ResponseTooLarge(f"response exceeds {max_bytes} bytes")
    return b"".join(chunks)


def _decompress(body: bytes, encoding: str | None, max_bytes: int) -> bytes:
    normalized = (encoding or "").lower().strip()
    if normalized == "gzip":
        body = gzip.decompress(body)
    elif normalized == "deflate":
        try:
            body = zlib.decompress(body)
        except zlib.error:
            body = zlib.decompress(body, -zlib.MAX_WBITS)
    if len(body) > max_bytes:
        raise ResponseTooLarge(f"decompressed response exceeds {max_bytes} bytes")
    return body


def http_get(
    url: str,
    route: Route,
    *,
    accept: str,
    referer: str,
    timeout: float,
    max_bytes: int,
) -> HttpResult:
    proxy_map = {} if route.proxy is None else {"http": route.proxy, "https": route.proxy}
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(proxy_map),
        SafeRedirectHandler(),
    )
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "Accept-Encoding": "gzip, deflate",
            "Referer": referer,
            "User-Agent": USER_AGENT,
        },
    )
    response: Any
    try:
        response = opener.open(request, timeout=timeout)
    except urllib.error.HTTPError as exc:
        response = exc
    except (OSError, urllib.error.URLError, socket.timeout) as exc:
        return HttpResult(
            status=None,
            content_type=None,
            headers={},
            body=b"",
            final_url=url,
            error=f"{type(exc).__name__}: {exc}",
        )

    try:
        headers = {key.lower(): value for key, value in response.headers.items()}
        body = _read_limited(response, max_bytes)
        body = _decompress(body, headers.get("content-encoding"), max_bytes)
    except (OSError, ResponseTooLarge, gzip.BadGzipFile, zlib.error) as exc:
        return HttpResult(
            status=getattr(response, "status", getattr(response, "code", None)),
            content_type=response.headers.get("Content-Type"),
            headers={},
            body=b"",
            final_url=response.geturl(),
            error=f"{type(exc).__name__}: {exc}",
        )
    finally:
        response.close()

    return HttpResult(
        status=getattr(response, "status", getattr(response, "code", None)),
        content_type=headers.get("content-type"),
        headers=headers,
        body=body,
        final_url=response.geturl(),
    )


def _conversation_score(value: dict[str, Any]) -> int:
    score = 0
    if isinstance(value.get("mapping"), dict):
        score += 5
    if isinstance(value.get("linear_conversation"), list):
        score += 4
    if isinstance(value.get("title"), str):
        score += 2
    if isinstance(value.get("conversation_id"), str):
        score += 1
    return score


def find_conversation_data(value: Any) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    best_score = 0
    queue: list[Any] = [value]
    seen: set[int] = set()
    while queue:
        current = queue.pop(0)
        if isinstance(current, (dict, list)):
            identity = id(current)
            if identity in seen:
                continue
            seen.add(identity)
        if isinstance(current, dict):
            score = _conversation_score(current)
            if score > best_score:
                best = current
                best_score = score
            preferred = [current.get("data"), current.get("serverResponse")]
            queue[0:0] = [item for item in preferred if item is not None]
            queue.extend(current.values())
        elif isinstance(current, list):
            queue.extend(current)
        if best_score >= 11:
            break
    return best if best_score >= 5 else None


class RscReferencePool:
    def __init__(self, pool: list[Any]) -> None:
        self.pool = pool
        self.cache: dict[int, Any] = {}
        self.resolving: set[int] = set()

    def resolve_ref(self, value: Any) -> Any:
        if isinstance(value, int):
            if value < 0:
                return None
            return self.resolve_index(value)
        return value

    def resolve_index(self, index: int) -> Any:
        if index in self.cache:
            return self.cache[index]
        if index in self.resolving:
            return {"$cycle": index}
        if index >= len(self.pool):
            raise ExtractionError(f"RSC reference {index} is outside the pool")

        self.resolving.add(index)
        raw = self.pool[index]
        if isinstance(raw, dict):
            result: Any = {}
            self.cache[index] = result
            for encoded_key, value_ref in raw.items():
                if encoded_key.startswith("_") and encoded_key[1:].isdigit():
                    key = self.resolve_index(int(encoded_key[1:]))
                else:
                    key = encoded_key
                result[str(key)] = self.resolve_ref(value_ref)
        elif isinstance(raw, list):
            if raw and isinstance(raw[0], str):
                values = [self.resolve_ref(item) for item in raw[1:] if item != index]
                result = {"$type": raw[0], "$values": values}
            else:
                result = []
                self.cache[index] = result
                result.extend(self.resolve_ref(item) for item in raw)
        else:
            result = raw
        self.cache[index] = result
        self.resolving.remove(index)
        return result


def extract_rsc_chunks(page: str) -> list[str]:
    decoder = json.JSONDecoder()
    chunks: list[str] = []
    position = 0
    while True:
        marker_at = page.find(RSC_MARKER, position)
        if marker_at < 0:
            break
        argument_at = marker_at + len(RSC_MARKER)
        while argument_at < len(page) and page[argument_at].isspace():
            argument_at += 1
        try:
            value, consumed = decoder.raw_decode(page[argument_at:])
        except json.JSONDecodeError as exc:
            raise ExtractionError(f"invalid streamController.enqueue argument: {exc}") from exc
        if not isinstance(value, str):
            raise ExtractionError("streamController.enqueue argument is not a string")
        chunks.append(value)
        position = argument_at + consumed
    return chunks


def decode_rsc_html(body: bytes) -> tuple[dict[str, Any], dict[str, Any]]:
    page = body.decode("utf-8", errors="replace")
    chunks = extract_rsc_chunks(page)
    if not chunks:
        raise ExtractionError("HTML contains no React Router streamController payload")
    payload = "".join(chunks)
    try:
        pool, consumed = json.JSONDecoder().raw_decode(payload)
    except json.JSONDecodeError as exc:
        raise ExtractionError(f"could not decode the RSC reference pool: {exc}") from exc
    if not isinstance(pool, list):
        raise ExtractionError("RSC payload root is not a reference pool")

    string_indexes: dict[str, list[int]] = {}
    for index, value in enumerate(pool):
        if isinstance(value, str):
            string_indexes.setdefault(value, []).append(index)
    required_names = ("title", "mapping", "linear_conversation")
    if not all(name in string_indexes for name in required_names):
        raise ExtractionError("RSC pool has no recognizable shared-conversation schema")

    decoder = RscReferencePool(pool)
    candidates: list[dict[str, Any]] = []
    required_key_sets = [
        {f"_{indexes[0]}" for indexes in (string_indexes[name] for name in required_names)}
    ]
    for required_keys in required_key_sets:
        for index, raw in enumerate(pool):
            if isinstance(raw, dict) and required_keys.issubset(raw):
                resolved = decoder.resolve_index(index)
                if isinstance(resolved, dict):
                    candidates.append(resolved)
    if not candidates:
        root = decoder.resolve_index(0)
        candidate = find_conversation_data(root)
        if candidate:
            candidates.append(candidate)
    if not candidates:
        raise ExtractionError("could not locate conversation data in the RSC pool")
    data = max(candidates, key=_conversation_score)
    return data, {
        "html_bytes": len(body),
        "enqueue_chunks": len(chunks),
        "rsc_payload_chars": len(payload),
        "rsc_json_chars": consumed,
        "rsc_pool_items": len(pool),
        "rsc_trailing_chars": len(payload[consumed:]),
    }


def parse_backend_json(body: bytes) -> dict[str, Any]:
    try:
        parsed = json.loads(body.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExtractionError(f"backend response is not valid JSON: {exc}") from exc
    data = find_conversation_data(parsed)
    if data is None:
        raise ExtractionError("backend JSON has no shared-conversation data")
    return data


def fetch_shared_conversation(
    source_url: str,
    routes: list[Route],
    *,
    timeout: float = 45.0,
    max_bytes: int = DEFAULT_SHARE_LIMIT,
) -> FetchedShare:
    share_id, share_url = canonical_share_url(source_url)
    backend_url = f"https://chatgpt.com/backend-api/share/{share_id}"
    attempts: list[FetchAttempt] = []

    for route in routes:
        backend = http_get(
            backend_url,
            route,
            accept="application/json, text/plain, */*",
            referer=share_url,
            timeout=timeout,
            max_bytes=max_bytes,
        )
        backend_attempt = FetchAttempt(
            route=route.label,
            endpoint="backend-api",
            status=backend.status,
            content_type=backend.content_type,
            bytes=len(backend.body),
            error=backend.error,
        )
        attempts.append(backend_attempt)
        if backend.status == 200 and backend.body:
            try:
                data = parse_backend_json(backend.body)
            except ExtractionError as exc:
                backend_attempt.error = str(exc)
            else:
                return FetchedShare(
                    share_id=share_id,
                    share_url=share_url,
                    data=data,
                    method="backend-json",
                    route=route,
                    response_body=backend.body,
                    response_sha256=sha256_bytes(backend.body),
                    attempts=attempts,
                    diagnostics={"backend_bytes": len(backend.body)},
                )

        page = http_get(
            share_url,
            route,
            accept="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            referer=share_url,
            timeout=timeout,
            max_bytes=max_bytes,
        )
        page_attempt = FetchAttempt(
            route=route.label,
            endpoint="share-html",
            status=page.status,
            content_type=page.content_type,
            bytes=len(page.body),
            error=page.error,
        )
        attempts.append(page_attempt)
        if page.status == 200 and page.body:
            try:
                data, diagnostics = decode_rsc_html(page.body)
            except ExtractionError as exc:
                page_attempt.error = str(exc)
            else:
                return FetchedShare(
                    share_id=share_id,
                    share_url=share_url,
                    data=data,
                    method="html-rsc",
                    route=route,
                    response_body=page.body,
                    response_sha256=sha256_bytes(page.body),
                    attempts=attempts,
                    diagnostics=diagnostics,
                )

    summary = "; ".join(
        f"{item.route}/{item.endpoint}: {item.status or 'network-error'}"
        + (f" ({item.error})" if item.error else "")
        for item in attempts
    )
    raise ExtractionError(f"all ChatGPT Share routes failed: {summary}")


def conversation_nodes(data: dict[str, Any]) -> list[dict[str, Any]]:
    linear = data.get("linear_conversation")
    if isinstance(linear, list) and all(isinstance(item, dict) for item in linear):
        return linear
    mapping = data.get("mapping")
    current = data.get("current_node")
    if not isinstance(mapping, dict) or not isinstance(current, str):
        return []
    branch: list[dict[str, Any]] = []
    seen: set[str] = set()
    while current and current not in seen:
        seen.add(current)
        node = mapping.get(current)
        if not isinstance(node, dict):
            break
        branch.append(node)
        parent = node.get("parent")
        current = parent if isinstance(parent, str) else ""
    branch.reverse()
    return branch


def _text_from_part(part: Any) -> str | None:
    if isinstance(part, str):
        return part
    if not isinstance(part, dict):
        return None
    for key in ("text", "content", "caption", "transcript"):
        value = part.get(key)
        if isinstance(value, str):
            return value
    nested = part.get("parts")
    if isinstance(nested, list):
        values = [_text_from_part(item) for item in nested]
        return "\n\n".join(value for value in values if value)
    return None


def extract_content_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, dict):
        return ""
    parts = content.get("parts")
    values: list[str] = []
    if isinstance(parts, list):
        for part in parts:
            value = _text_from_part(part)
            if value and value.strip():
                values.append(value.strip())
    else:
        value = _text_from_part(content)
        if value and value.strip():
            values.append(value.strip())
    return "\n\n".join(values).strip()


def timestamp_to_iso(value: Any) -> str | None:
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value, timezone.utc).isoformat().replace("+00:00", "Z")
        except (OverflowError, OSError, ValueError):
            return str(value)
    if isinstance(value, str) and value:
        return value
    return None


def extract_visible_messages(
    data: dict[str, Any],
) -> tuple[list[VisibleMessage], dict[str, int]]:
    messages: list[VisibleMessage] = []
    stats: dict[str, int] = {
        "nodes": 0,
        "without_message": 0,
        "excluded_role": 0,
        "excluded_hidden": 0,
        "excluded_content_type": 0,
        "excluded_recipient": 0,
        "excluded_empty_or_redacted": 0,
    }
    for node in conversation_nodes(data):
        stats["nodes"] += 1
        message = node.get("message") if isinstance(node, dict) else None
        if not isinstance(message, dict):
            stats["without_message"] += 1
            continue
        author = message.get("author") if isinstance(message.get("author"), dict) else {}
        role = author.get("role")
        if role not in {"user", "assistant"}:
            stats["excluded_role"] += 1
            continue
        metadata = message.get("metadata") if isinstance(message.get("metadata"), dict) else {}
        if any(bool(metadata.get(key)) for key in HIDDEN_METADATA_KEYS):
            stats["excluded_hidden"] += 1
            continue
        content = message.get("content")
        content_type = content.get("content_type") if isinstance(content, dict) else None
        if content_type in EXCLUDED_CONTENT_TYPES:
            stats["excluded_content_type"] += 1
            continue
        channel = message.get("channel")
        if channel in {"analysis", "reasoning"}:
            stats["excluded_content_type"] += 1
            continue
        recipient = message.get("recipient")
        if recipient not in {None, "", "all"}:
            stats["excluded_recipient"] += 1
            continue
        text = extract_content_text(content)
        if not text or text.strip().lower() in REDACTED_TEXTS:
            stats["excluded_empty_or_redacted"] += 1
            continue
        message_id = message.get("id") or node.get("id")
        messages.append(
            VisibleMessage(
                sequence=len(messages) + 1,
                message_id=message_id if isinstance(message_id, str) else None,
                role=role,
                author_name=author.get("name") if isinstance(author.get("name"), str) else None,
                create_time=timestamp_to_iso(message.get("create_time")),
                channel=channel if isinstance(channel, str) else None,
                content_type=content_type if isinstance(content_type, str) else None,
                text=text,
                raw_message=message,
            )
        )
    stats["visible"] = len(messages)
    return messages, stats


def walk_values(value: Any, path: str = "$") -> Iterator[tuple[str, str | None, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield child_path, str(key), child
            yield from walk_values(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]"
            yield child_path, None, child
            yield from walk_values(child, child_path)


def normalize_url(value: str) -> str | None:
    cleaned = html.unescape(value.strip()).rstrip(".,;:!?)]}>")
    parsed = urllib.parse.urlsplit(cleaned)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        return None
    return cleaned


def urls_from_text(value: str) -> list[str]:
    urls: list[str] = []
    for match in URL_RE.finditer(value):
        normalized = normalize_url(match.group(0))
        if normalized:
            urls.append(normalized)
    return urls


def urls_from_object(value: Any, *, skip_widget_state: bool = True) -> list[str]:
    urls: list[str] = []
    if isinstance(value, str):
        return urls_from_text(value)
    if isinstance(value, dict):
        for key, child in value.items():
            if skip_widget_state and key in {"widget_state", "websocket_url"}:
                continue
            urls.extend(urls_from_object(child, skip_widget_state=skip_widget_state))
    elif isinstance(value, list):
        for child in value:
            urls.extend(urls_from_object(child, skip_widget_state=skip_widget_state))
    return urls


def _widget_states(data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    seen: set[str] = set()
    for node in conversation_nodes(data):
        message = node.get("message") if isinstance(node, dict) else None
        if not isinstance(message, dict):
            continue
        metadata = message.get("metadata")
        if not isinstance(metadata, dict):
            continue
        for _, key, value in walk_values(metadata):
            if key != "widget_state":
                continue
            if isinstance(value, dict):
                parsed = value
                fingerprint = sha256_text(json.dumps(value, ensure_ascii=False, sort_keys=True))
            elif isinstance(value, str):
                try:
                    parsed = json.loads(value)
                except json.JSONDecodeError:
                    continue
                if not isinstance(parsed, dict):
                    continue
                fingerprint = sha256_text(value)
            else:
                continue
            if fingerprint not in seen:
                seen.add(fingerprint)
                yield parsed


def _find_report_messages(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"report_message", "final_report_message", "research_report_message"}:
                if isinstance(child, dict):
                    yield child
            yield from _find_report_messages(child)
    elif isinstance(value, list):
        for child in value:
            yield from _find_report_messages(child)


def extract_research_reports(data: dict[str, Any]) -> list[ResearchReport]:
    reports: list[ResearchReport] = []
    seen: set[str] = set()
    fallback_title = str(data.get("title") or "Research report")
    for widget in _widget_states(data):
        plan = widget.get("plan") if isinstance(widget.get("plan"), dict) else {}
        title = str(plan.get("title") or fallback_title)
        for message in _find_report_messages(widget):
            text = extract_content_text(message.get("content"))
            if not text:
                continue
            digest = sha256_text(text)
            if digest in seen:
                continue
            seen.add(digest)
            metadata = message.get("metadata") if isinstance(message.get("metadata"), dict) else {}
            safe_metadata = {
                key: metadata[key]
                for key in ("content_references", "citations", "safe_urls")
                if key in metadata
            }
            source_urls = sorted(set(urls_from_object(safe_metadata)))
            reports.append(
                ResearchReport(
                    index=len(reports) + 1,
                    title=title,
                    message_id=message.get("id") if isinstance(message.get("id"), str) else None,
                    text=text,
                    sha256=digest,
                    metadata=safe_metadata,
                    source_urls=source_urls,
                )
            )
    return reports


def collect_links(
    data: dict[str, Any],
    messages: list[VisibleMessage],
    reports: list[ResearchReport],
) -> list[dict[str, Any]]:
    sources: dict[str, set[str]] = {}

    def add(values: Iterable[str], source: str) -> None:
        for value in values:
            normalized = normalize_url(value)
            if normalized:
                sources.setdefault(normalized, set()).add(source)

    top_safe_urls = data.get("safe_urls")
    if isinstance(top_safe_urls, list):
        add((value for value in top_safe_urls if isinstance(value, str)), "conversation.safe_urls")
    for message in messages:
        add(urls_from_text(message.text), f"message:{message.sequence}")
        metadata = message.raw_message.get("metadata")
        if isinstance(metadata, dict):
            selected = {
                key: metadata[key]
                for key in ("content_references", "citations", "safe_urls")
                if key in metadata
            }
            add(urls_from_object(selected), f"message:{message.sequence}:metadata")
    for report in reports:
        add(report.source_urls, f"research:{report.index}")
        add(urls_from_text(report.text), f"research:{report.index}:text")

    return [
        {
            "url": url,
            "sources": sorted(url_sources),
            "looks_like_file": looks_like_file_url(url),
        }
        for url, url_sources in sorted(sources.items())
    ]


def looks_like_file_url(value: str) -> bool:
    parsed = urllib.parse.urlsplit(value)
    path = urllib.parse.unquote(parsed.path).lower()
    suffix = Path(path).suffix
    host = (parsed.hostname or "").lower()
    return (
        suffix in FILE_EXTENSIONS
        or "/download" in path
        or "/backend-api/files/" in path
        or (host.endswith("oaiusercontent.com") and "file" in path)
    )


def labeled_file_urls_from_text(value: str) -> list[str]:
    urls: list[str] = []
    for label, url in MARKDOWN_LINK_RE.findall(value):
        normalized = normalize_url(url)
        if normalized and FILE_LINK_LABEL_RE.search(label):
            urls.append(normalized)
    return urls


def _filename_hint(value: dict[str, Any]) -> str | None:
    for key in FILENAME_KEYS:
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return None


def _mime_hint(value: dict[str, Any]) -> str | None:
    for key in MIME_KEYS:
        candidate = value.get(key)
        if isinstance(candidate, str) and "/" in candidate:
            return candidate
    return None


def discover_file_candidates(
    messages: list[VisibleMessage], reports: list[ResearchReport]
) -> list[FileCandidate]:
    found: dict[str, FileCandidate] = {}

    def add(
        locator: str,
        source: str,
        kind: str,
        filename_hint: str | None = None,
        mime_type: str | None = None,
    ) -> None:
        locator = html.unescape(locator.strip()).rstrip(".,;:!?)]}>")
        if not locator:
            return
        found.setdefault(
            locator,
            FileCandidate(
                locator=locator,
                source=source,
                kind=kind,
                filename_hint=filename_hint,
                mime_type=mime_type,
            ),
        )

    def scan(value: Any, source: str, *, allow_linked_urls: bool) -> None:
        if isinstance(value, dict):
            filename = _filename_hint(value)
            mime_type = _mime_hint(value)
            for key, child in value.items():
                if key == "widget_state":
                    continue
                normalized_key = key.lower()
                if isinstance(child, str):
                    if key in EXPLICIT_FILE_KEYS or "download_url" in normalized_key:
                        add(child, source, "explicit-file-field", filename, mime_type)
                    elif key in FILE_ID_KEYS and child:
                        locator = child if "://" in child else f"file-service://{child}"
                        add(locator, source, "file-id", filename, mime_type)
                    for match in SPECIAL_LOCATOR_RE.finditer(child):
                        add(match.group(0), source, "embedded-file-locator", filename, mime_type)
                    for url in urls_from_text(child):
                        if allow_linked_urls and looks_like_file_url(url):
                            add(url, source, "linked-file", filename, mime_type)
                scan(child, source, allow_linked_urls=allow_linked_urls)
        elif isinstance(value, list):
            for child in value:
                scan(child, source, allow_linked_urls=allow_linked_urls)
        elif isinstance(value, str):
            for match in SPECIAL_LOCATOR_RE.finditer(value):
                add(match.group(0), source, "embedded-file-locator")
            if allow_linked_urls:
                for url in urls_from_text(value):
                    if looks_like_file_url(url):
                        add(url, source, "linked-file")
                for url in labeled_file_urls_from_text(value):
                    add(url, source, "labeled-file-link")

    for message in messages:
        scan(
            message.raw_message.get("content"),
            f"message:{message.sequence}:content",
            allow_linked_urls=True,
        )
        metadata = message.raw_message.get("metadata")
        if isinstance(metadata, dict):
            scan(
                metadata,
                f"message:{message.sequence}:metadata",
                allow_linked_urls=False,
            )
    for report in reports:
        scan(report.text, f"research:{report.index}:text", allow_linked_urls=False)
        scan(report.metadata, f"research:{report.index}:metadata", allow_linked_urls=False)
    return list(found.values())


def _safe_public_download_url(value: str) -> bool:
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    hostname = parsed.hostname.lower()
    if hostname in {"localhost", "localhost.localdomain"} or hostname.endswith(".local"):
        return False
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return True
    return not (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
    )


def _candidate_urls(candidate: FileCandidate) -> list[str]:
    locator = candidate.locator
    if locator.startswith("file-service://"):
        file_id = locator.removeprefix("file-service://").strip("/")
        encoded = urllib.parse.quote(file_id, safe="")
        return [
            f"https://chatgpt.com/backend-api/files/{encoded}/download",
            f"https://chatgpt.com/backend-api/files/{encoded}",
        ]
    if locator.startswith(("sandbox:/", "sandbox://", "attachment://")):
        return []
    normalized = normalize_url(locator)
    return [normalized] if normalized else []


def _filename_from_headers(headers: dict[str, str]) -> str | None:
    disposition = headers.get("content-disposition", "")
    encoded = re.search(r"filename\*=UTF-8''([^;]+)", disposition, flags=re.IGNORECASE)
    if encoded:
        return urllib.parse.unquote(encoded.group(1))
    quoted = re.search(r'filename="([^"]+)"', disposition, flags=re.IGNORECASE)
    if quoted:
        return quoted.group(1)
    plain = re.search(r"filename=([^;]+)", disposition, flags=re.IGNORECASE)
    return plain.group(1).strip() if plain else None


def safe_filename(value: str, fallback: str) -> str:
    value = value.replace("\\", "/").rsplit("/", 1)[-1]
    value = re.sub(r"[\x00-\x1f\x7f]", "", value)
    value = re.sub(r"[/:*?\"<>|]", "_", value).strip(" .")
    if not value or value in {".", ".."}:
        value = fallback
    if len(value) > 180:
        suffix = Path(value).suffix[:20]
        value = value[: 180 - len(suffix)] + suffix
    return value


def _unique_destination(directory: Path, name: str) -> Path:
    candidate = directory / name
    counter = 2
    while candidate.exists():
        suffix = candidate.suffix
        stem = candidate.name[: -len(suffix)] if suffix else candidate.name
        candidate = directory / f"{stem}-{counter}{suffix}"
        counter += 1
    return candidate


def download_file_candidates(
    candidates: list[FileCandidate],
    output_dir: Path,
    routes: list[Route],
    active_route: Route,
    *,
    referer: str,
    timeout: float,
    max_bytes: int,
) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ordered_routes = [active_route] + [route for route in routes if route != active_route]
    results: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates, start=1):
        result: dict[str, Any] = {
            "locator": candidate.locator,
            "source": candidate.source,
            "kind": candidate.kind,
            "status": "not-downloaded",
            "attempts": [],
        }
        urls = _candidate_urls(candidate)
        if not urls:
            result["error"] = "locator has no public HTTP download URL"
            results.append(result)
            continue
        downloaded = False
        for url in urls:
            if not _safe_public_download_url(url):
                result["attempts"].append({"url": url, "error": "unsafe download target"})
                continue
            for route in ordered_routes:
                response = http_get(
                    url,
                    route,
                    accept="*/*",
                    referer=referer,
                    timeout=timeout,
                    max_bytes=max_bytes,
                )
                attempt = {
                    "url": url,
                    "route": route.label,
                    "status": response.status,
                    "content_type": response.content_type,
                    "bytes": len(response.body),
                    "error": response.error,
                }
                result["attempts"].append(attempt)
                if response.status != 200 or not response.body:
                    continue
                if response.content_type and response.content_type.lower().startswith("text/html"):
                    attempt["error"] = "received HTML instead of a file"
                    continue
                header_name = _filename_from_headers(response.headers)
                path_name = Path(urllib.parse.unquote(urllib.parse.urlsplit(url).path)).name
                name = safe_filename(
                    header_name or candidate.filename_hint or path_name,
                    f"artifact-{index:03d}.bin",
                )
                destination = _unique_destination(output_dir, name)
                destination.write_bytes(response.body)
                result.update(
                    {
                        "status": "downloaded",
                        "path": destination.name,
                        "bytes": len(response.body),
                        "sha256": sha256_bytes(response.body),
                        "content_type": response.content_type,
                        "download_url": url,
                        "route": route.label,
                    }
                )
                downloaded = True
                break
            if downloaded:
                break
        if not downloaded:
            result["status"] = "failed"
            result["error"] = "all public download attempts failed"
        results.append(result)
    return results


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _role_label(role: str) -> str:
    return {"user": "Пользователь", "assistant": "Ассистент"}.get(role, role)


def render_conversation_markdown(
    fetched: FetchedShare, messages: list[VisibleMessage], stats: dict[str, int]
) -> str:
    title = str(fetched.data.get("title") or "ChatGPT Share")
    lines = [
        f"# {title}",
        "",
        "## Метаданные",
        "",
        f"- Shared-ссылка: <{fetched.share_url}>",
        f"- Способ извлечения: `{fetched.method}`",
        f"- Сетевой маршрут: `{fetched.route.label}`",
        f"- Узлов в цепочке: {stats['nodes']}",
        f"- Видимых ходов user/assistant: {stats['visible']}",
        "- Скрытые system/tool/reasoning/code-узлы в текст не включены.",
        "",
        "## Видимые сообщения",
        "",
    ]
    for message in messages:
        lines.append(f"### {message.sequence}. {_role_label(message.role)}")
        lines.append("")
        details = []
        if message.message_id:
            details.append(f"узел `{message.message_id}`")
        if message.create_time:
            details.append(f"время `{message.create_time}`")
        if message.channel:
            details.append(f"канал `{message.channel}`")
        if details:
            lines.append("_" + "; ".join(details) + "_")
            lines.append("")
        lines.append(message.text)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_links_markdown(links: list[dict[str, Any]]) -> str:
    lines = [
        "# Ссылки из ChatGPT Share",
        "",
        "Список является технической выгрузкой и не считается проверенной библиографией.",
        "",
    ]
    for item in links:
        sources = ", ".join(f"`{source}`" for source in item["sources"])
        lines.append(f"- <{item['url']}> — {sources}")
    return "\n".join(lines).rstrip() + "\n"


def render_report_sources_markdown(report: ResearchReport) -> str:
    lines = [
        f"# Источники research-отчета {report.index}",
        "",
        "Ссылки извлечены из metadata отчета и требуют библиографической проверки.",
        "",
    ]
    lines.extend(f"- <{url}>" for url in report.source_urls)
    return "\n".join(lines).rstrip() + "\n"


def _artifact_manifest(root: Path) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            body = path.read_bytes()
            artifacts.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "bytes": len(body),
                    "sha256": sha256_bytes(body),
                }
            )
    return artifacts


def _validate_output_target(path: Path) -> None:
    resolved = path.resolve()
    script_path = Path(__file__).resolve()
    cwd = Path.cwd().resolve()
    forbidden = {
        Path("/").resolve(),
        Path.home().resolve(),
        cwd,
        *script_path.parents,
        *cwd.parents,
    }
    if resolved in forbidden:
        raise ExtractionError(f"refusing broad output target: {resolved}")
    if (resolved / ".git").exists():
        raise ExtractionError(f"refusing to use a Git repository as output: {resolved}")


def _replaceable_export(path: Path, share_id: str) -> bool:
    try:
        entries = list(path.iterdir())
    except OSError:
        return False
    if not entries:
        return True
    manifest_path = path / "manifest.json"
    if not manifest_path.is_file():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        manifest.get("format_version") == 1
        and (manifest.get("source") or {}).get("share_id") == share_id
    )


def write_export(
    fetched: FetchedShare,
    routes: list[Route],
    output_dir: Path,
    *,
    timeout: float,
    max_file_bytes: int,
    download_files: bool,
    save_raw: bool,
    force: bool,
) -> dict[str, Any]:
    messages, message_stats = extract_visible_messages(fetched.data)
    reports = extract_research_reports(fetched.data)
    links = collect_links(fetched.data, messages, reports)
    file_candidates = discover_file_candidates(messages, reports)

    output_dir = output_dir.resolve()
    _validate_output_target(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    if output_dir.exists():
        if not force:
            raise ExtractionError(f"output directory already exists: {output_dir}; use --force")
        if output_dir.is_symlink() or not output_dir.is_dir():
            raise ExtractionError(f"refusing to replace non-directory output: {output_dir}")
        if not _replaceable_export(output_dir, fetched.share_id):
            raise ExtractionError(
                "refusing to replace a directory that is not an earlier export of this share id: "
                f"{output_dir}"
            )
        shutil.rmtree(output_dir)

    staging = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.tmp-", dir=output_dir.parent))
    try:
        (staging / "conversation.md").write_text(
            render_conversation_markdown(fetched, messages, message_stats), encoding="utf-8"
        )
        _write_json(
            staging / "conversation.json",
            {
                "title": fetched.data.get("title"),
                "share_id": fetched.share_id,
                "share_url": fetched.share_url,
                "conversation_id": fetched.data.get("conversation_id"),
                "messages": [message.as_dict() for message in messages],
            },
        )
        (staging / "links.md").write_text(render_links_markdown(links), encoding="utf-8")
        _write_json(staging / "links.json", links)

        if reports:
            research_dir = staging / "research"
            research_dir.mkdir()
            for report in reports:
                prefix = f"{report.index:03d}"
                body = report.text if report.text.endswith("\n") else report.text + "\n"
                (research_dir / f"{prefix}-report.md").write_text(body, encoding="utf-8")
                _write_json(
                    research_dir / f"{prefix}-report-metadata.json",
                    {
                        "title": report.title,
                        "message_id": report.message_id,
                        "text_chars": len(report.text),
                        "text_sha256": report.sha256,
                        "source_urls": report.source_urls,
                        "metadata": report.metadata,
                    },
                )
                (research_dir / f"{prefix}-sources.md").write_text(
                    render_report_sources_markdown(report), encoding="utf-8"
                )

        if download_files:
            file_results = download_file_candidates(
                file_candidates,
                staging / "files",
                routes,
                fetched.route,
                referer=fetched.share_url,
                timeout=timeout,
                max_bytes=max_file_bytes,
            )
        else:
            file_results = [
                {
                    "locator": item.locator,
                    "source": item.source,
                    "kind": item.kind,
                    "status": "skipped",
                }
                for item in file_candidates
            ]
        _write_json(staging / "files.json", file_results)

        if save_raw:
            raw_dir = staging / "raw"
            raw_dir.mkdir()
            name = "backend-response.json" if fetched.method == "backend-json" else "share-page.html"
            (raw_dir / name).write_bytes(fetched.response_body)

        downloaded_count = sum(item.get("status") == "downloaded" for item in file_results)
        failed_count = sum(item.get("status") == "failed" for item in file_results)
        warnings = []
        if failed_count:
            warnings.append(f"{failed_count} file candidates could not be downloaded")
        if not reports:
            warnings.append("no embedded research report was found")

        manifest = {
            "format_version": 1,
            "extracted_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": {
                "share_id": fetched.share_id,
                "share_url": fetched.share_url,
                "title": fetched.data.get("title"),
                "conversation_id": fetched.data.get("conversation_id"),
                "method": fetched.method,
                "route": fetched.route.label,
                "response_bytes": len(fetched.response_body),
                "response_sha256": fetched.response_sha256,
                "diagnostics": fetched.diagnostics,
                "attempts": [item.__dict__ for item in fetched.attempts],
            },
            "counts": {
                "conversation_nodes": message_stats["nodes"],
                "visible_messages": len(messages),
                "research_reports": len(reports),
                "unique_links": len(links),
                "file_candidates": len(file_candidates),
                "downloaded_files": downloaded_count,
            },
            "message_filter": message_stats,
            "warnings": warnings,
        }
        manifest["artifacts"] = _artifact_manifest(staging)
        _write_json(staging / "manifest.json", manifest)
        staging.replace(output_dir)
        return manifest
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract a public ChatGPT Share conversation without launching a browser."
    )
    parser.add_argument("share_url", help="https://chatgpt.com/share/<id>")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="exact output directory; default: ./chatgpt-share-exports/<share-id>",
    )
    parser.add_argument(
        "--proxy",
        action="append",
        help=(
            "network route; repeat to define fallback order. Use 'direct' for no proxy or "
            "'auto' for environment, direct, and workspace proxy candidates"
        ),
    )
    parser.add_argument("--timeout", type=float, default=45.0, help="per-request timeout")
    parser.add_argument(
        "--max-share-bytes", type=int, default=DEFAULT_SHARE_LIMIT, help="share response limit"
    )
    parser.add_argument(
        "--max-file-bytes", type=int, default=DEFAULT_FILE_LIMIT, help="per-file download limit"
    )
    parser.add_argument(
        "--download-files",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="attempt public generated-file downloads (default: enabled)",
    )
    parser.add_argument(
        "--save-raw",
        action="store_true",
        help="also save raw backend JSON or HTML; may contain ephemeral service metadata",
    )
    parser.add_argument("--force", action="store_true", help="replace an existing output directory")
    return parser


def run_cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        share_id, _ = canonical_share_url(args.share_url)
        routes = build_routes(args.proxy)
        fetched = fetch_shared_conversation(
            args.share_url,
            routes,
            timeout=args.timeout,
            max_bytes=args.max_share_bytes,
        )
        output_dir = args.output_dir or Path.cwd() / "chatgpt-share-exports" / share_id
        manifest = write_export(
            fetched,
            routes,
            output_dir,
            timeout=args.timeout,
            max_file_bytes=args.max_file_bytes,
            download_files=args.download_files,
            save_raw=args.save_raw,
            force=args.force,
        )
    except (ExtractionError, OSError, ValueError) as exc:
        print(f"chatgpt share extraction failed: {exc}", file=sys.stderr)
        return 1

    counts = manifest["counts"]
    print("chatgpt share extraction passed")
    print(f"title: {manifest['source']['title']}")
    print(f"method: {manifest['source']['method']}")
    print(f"route: {manifest['source']['route']}")
    print(f"visible messages: {counts['visible_messages']}")
    print(f"research reports: {counts['research_reports']}")
    print(f"unique links: {counts['unique_links']}")
    print(f"file candidates: {counts['file_candidates']}")
    print(f"downloaded files: {counts['downloaded_files']}")
    print(f"output: {output_dir.resolve()}")
    for warning in manifest.get("warnings", []):
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
