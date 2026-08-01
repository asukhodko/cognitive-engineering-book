from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))

import chatgpt_share_extractor as extractor  # noqa: E402


def message_node(
    message_id: str,
    role: str,
    text: str,
    *,
    content_type: str = "text",
    channel: str | None = None,
    recipient: str = "all",
    metadata: dict | None = None,
) -> dict:
    return {
        "id": message_id,
        "message": {
            "id": message_id,
            "author": {"role": role, "name": None, "metadata": {}},
            "create_time": 1_700_000_000.0,
            "content": {"content_type": content_type, "parts": [text]},
            "metadata": metadata or {},
            "recipient": recipient,
            "channel": channel,
        },
        "parent": None,
        "children": [],
    }


def sample_conversation() -> dict:
    widget_state = {
        "plan": {"title": "Synthetic research"},
        "status": "completed",
        "report_message": {
            "id": "report-1",
            "author": {"role": "assistant"},
            "content": {"content_type": "text", "parts": ["Research body"]},
            "metadata": {
                "safe_urls": ["https://example.org/source"],
                "content_references": [
                    {"safe_urls": ["https://example.org/paper.pdf"]}
                ],
            },
        },
    }
    visible_user = message_node("user-1", "user", "Question")
    hidden_user = message_node(
        "user-hidden",
        "user",
        "Hidden instructions",
        metadata={"is_user_system_message": True},
    )
    thoughts = message_node(
        "assistant-thoughts",
        "assistant",
        "Private reasoning",
        content_type="thoughts",
    )
    final = message_node(
        "assistant-final",
        "assistant",
        (
            "Answer with https://files.oaiusercontent.com/result.csv and "
            "[скачать отчёт](https://example.org/artifacts/opaque-id)"
        ),
        channel="final",
        metadata={
            "attachments": [{"file_id": "file-test", "filename": "result.csv"}],
            "chatgpt_sdk": {"widget_state": json.dumps(widget_state)},
        },
    )
    tool_call = message_node(
        "assistant-tool-call",
        "assistant",
        "Call tool",
        channel="commentary",
        recipient="api_tool.call_tool",
    )
    linear = [
        {"id": "root", "children": []},
        hidden_user,
        visible_user,
        thoughts,
        final,
        tool_call,
    ]
    return {
        "title": "Synthetic share",
        "conversation_id": "share-test",
        "mapping": {node["id"]: node for node in linear},
        "linear_conversation": linear,
        "safe_urls": ["https://example.org/top"],
    }


def synthetic_rsc_page(title: str = "Synthetic RSC") -> bytes:
    pool = [
        "title",
        "mapping",
        "linear_conversation",
        "conversation_id",
        {"_0": 5, "_1": 6, "_2": 7, "_3": 8},
        title,
        {},
        [],
        "rsc-id",
    ]
    payload = json.dumps(pool, ensure_ascii=False, separators=(",", ":"))
    midpoint = len(payload) // 2
    first = json.dumps(payload[:midpoint], ensure_ascii=False)
    second = json.dumps(payload[midpoint:], ensure_ascii=False)
    return (
        f"<script>{extractor.RSC_MARKER}{first})</script>"
        f"<script>{extractor.RSC_MARKER}{second})</script>"
    ).encode()


class ShareUrlTests(unittest.TestCase):
    def test_canonical_share_url_accepts_share_and_backend_urls(self) -> None:
        expected = ("abc-123", "https://chatgpt.com/share/abc-123")
        self.assertEqual(
            extractor.canonical_share_url("https://chatgpt.com/share/abc-123?x=1"),
            expected,
        )
        self.assertEqual(
            extractor.canonical_share_url("https://chatgpt.com/backend-api/share/abc-123"),
            expected,
        )

    def test_explicit_routes_keep_order_and_redact_credentials(self) -> None:
        routes = extractor.build_routes(
            ["direct", "http://user:secret@192.0.2.10:8080", "direct"]
        )
        self.assertEqual([route.label for route in routes], ["direct", "proxy:http://192.0.2.10:8080"])


class RscTests(unittest.TestCase):
    def test_decode_split_rsc_reference_pool(self) -> None:
        page = synthetic_rsc_page()
        data, diagnostics = extractor.decode_rsc_html(page)
        self.assertEqual(data["title"], "Synthetic RSC")
        self.assertEqual(data["conversation_id"], "rsc-id")
        self.assertEqual(diagnostics["enqueue_chunks"], 2)
        self.assertEqual(diagnostics["rsc_pool_items"], 9)

    def test_parse_backend_json_finds_nested_data(self) -> None:
        source = sample_conversation()
        parsed = extractor.parse_backend_json(json.dumps({"serverResponse": {"data": source}}).encode())
        self.assertEqual(parsed["title"], "Synthetic share")


class FetchFlowTests(unittest.TestCase):
    def test_backend_json_wins_when_available(self) -> None:
        body = json.dumps(sample_conversation()).encode()
        response = extractor.HttpResult(
            status=200,
            content_type="application/json",
            headers={},
            body=body,
            final_url="https://chatgpt.com/backend-api/share/test-id",
        )
        with mock.patch.object(extractor, "http_get", return_value=response) as get:
            fetched = extractor.fetch_shared_conversation(
                "https://chatgpt.com/share/test-id",
                [extractor.Route(label="direct", proxy=None)],
            )
        self.assertEqual(fetched.method, "backend-json")
        self.assertEqual(fetched.data["title"], "Synthetic share")
        self.assertEqual(get.call_count, 1)

    def test_html_rsc_is_used_after_backend_403(self) -> None:
        forbidden = extractor.HttpResult(
            status=403,
            content_type="text/html",
            headers={},
            body=b"forbidden",
            final_url="https://chatgpt.com/backend-api/share/test-id",
        )
        page = synthetic_rsc_page("Fallback RSC")
        success = extractor.HttpResult(
            status=200,
            content_type="text/html",
            headers={},
            body=page,
            final_url="https://chatgpt.com/share/test-id",
        )
        with mock.patch.object(extractor, "http_get", side_effect=[forbidden, success]) as get:
            fetched = extractor.fetch_shared_conversation(
                "https://chatgpt.com/share/test-id",
                [extractor.Route(label="direct", proxy=None)],
            )
        self.assertEqual(fetched.method, "html-rsc")
        self.assertEqual(fetched.data["title"], "Fallback RSC")
        self.assertEqual(get.call_count, 2)


class ContentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = sample_conversation()

    def test_visible_filter_excludes_hidden_reasoning_and_tool_calls(self) -> None:
        messages, stats = extractor.extract_visible_messages(self.data)
        self.assertEqual([message.message_id for message in messages], ["user-1", "assistant-final"])
        self.assertEqual(stats["visible"], 2)
        self.assertEqual(stats["excluded_hidden"], 1)
        self.assertEqual(stats["excluded_content_type"], 1)
        self.assertEqual(stats["excluded_recipient"], 1)

    def test_research_report_and_sources_are_extracted(self) -> None:
        reports = extractor.extract_research_reports(self.data)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].title, "Synthetic research")
        self.assertEqual(reports[0].text, "Research body")
        self.assertEqual(
            reports[0].source_urls,
            ["https://example.org/paper.pdf", "https://example.org/source"],
        )

    def test_file_candidates_ignore_research_papers(self) -> None:
        messages, _ = extractor.extract_visible_messages(self.data)
        reports = extractor.extract_research_reports(self.data)
        candidates = extractor.discover_file_candidates(messages, reports)
        locators = {candidate.locator for candidate in candidates}
        self.assertIn("file-service://file-test", locators)
        self.assertIn("https://files.oaiusercontent.com/result.csv", locators)
        self.assertIn("https://example.org/artifacts/opaque-id", locators)
        self.assertNotIn("https://example.org/paper.pdf", locators)

    def test_private_literal_download_targets_are_rejected(self) -> None:
        self.assertFalse(extractor._safe_public_download_url("http://127.0.0.1/file.pdf"))
        self.assertFalse(extractor._safe_public_download_url("http://192.168.1.5/file.pdf"))
        self.assertTrue(extractor._safe_public_download_url("https://example.org/file.pdf"))

    def test_export_writes_manifest_without_raw_hidden_messages(self) -> None:
        fetched = extractor.FetchedShare(
            share_id="share-test",
            share_url="https://chatgpt.com/share/share-test",
            data=self.data,
            method="backend-json",
            route=extractor.Route(label="direct", proxy=None),
            response_body=b"{}",
            response_sha256=extractor.sha256_bytes(b"{}"),
            attempts=[],
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "export"
            manifest = extractor.write_export(
                fetched,
                [fetched.route],
                output,
                timeout=1,
                max_file_bytes=1024,
                download_files=False,
                save_raw=False,
                force=False,
            )
            self.assertEqual(manifest["counts"]["visible_messages"], 2)
            self.assertEqual(manifest["counts"]["research_reports"], 1)
            conversation = (output / "conversation.md").read_text(encoding="utf-8")
            self.assertIn("Question", conversation)
            self.assertNotIn("Private reasoning", conversation)
            self.assertNotIn("Hidden instructions", conversation)
            self.assertEqual(
                (output / "research" / "001-report.md").read_text(encoding="utf-8"),
                "Research body\n",
            )

    def test_force_does_not_replace_an_unrelated_directory(self) -> None:
        fetched = extractor.FetchedShare(
            share_id="share-test",
            share_url="https://chatgpt.com/share/share-test",
            data=self.data,
            method="backend-json",
            route=extractor.Route(label="direct", proxy=None),
            response_body=b"{}",
            response_sha256=extractor.sha256_bytes(b"{}"),
            attempts=[],
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "unrelated"
            output.mkdir()
            marker = output / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            with self.assertRaises(extractor.ExtractionError):
                extractor.write_export(
                    fetched,
                    [fetched.route],
                    output,
                    timeout=1,
                    max_file_bytes=1024,
                    download_files=False,
                    save_raw=False,
                    force=True,
                )
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
