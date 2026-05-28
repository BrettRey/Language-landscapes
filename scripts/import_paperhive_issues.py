#!/usr/bin/env python3
"""Import PaperHive discussions as GitHub issues.

The importer intentionally avoids docLoop's service stack. It uses the public
PaperHive API endpoint that docLoop's PaperHive adapter uses, then creates one
GitHub issue per discussion through the GitHub CLI.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ITEM_ID = "CgFY8Z3opd2h"
DEFAULT_REPO = "langsci/555"
DEFAULT_OUT_DIR = Path("review/paperhive")
DEFAULT_LABELS = ("paperhive", "proofreading")
ITEM_URL = "https://paperhive.org/api/document-items/{item_id}"
DISCUSSIONS_URL = "https://paperhive.org/api/discussions?document={document_id}"
PAPERHIVE_ITEM_URL = "https://paperhive.org/documents/items/{item_id}"
MARKER_RE = re.compile(r"paperhive-discussion:([A-Za-z0-9_-]+)")


@dataclass(frozen=True)
class ImportableDiscussion:
    raw: dict[str, Any]
    discussion_id: str
    title: str
    body: str
    author: str
    created_at: str
    page: int | None
    start: int | None
    selected_text: str
    prefix: str
    suffix: str


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "paperhive-github-importer"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(response.read().decode(charset))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Fetch failed for {url}: HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Fetch failed for {url}: {error}") from error


def run_gh(args: list[str], *, input_text: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["gh", *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        command = " ".join(["gh", *args])
        raise SystemExit(f"Command failed: {command}\n{result.stderr.strip()}")
    return result


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\r\n", "\n").replace("\r", "\n").strip()


def author_name(author: dict[str, Any] | None) -> str:
    if not author:
        return "Unknown author"
    return clean_text(author.get("displayName")) or clean_text(author.get("account", {}).get("username")) or "Unknown author"


def first_selector(discussion: dict[str, Any], key: str) -> dict[str, Any]:
    selectors = discussion.get("target", {}).get("selectors", {})
    values = selectors.get(key) or []
    if isinstance(values, list) and values:
        return values[0] if isinstance(values[0], dict) else {}
    return {}


def page_number(discussion: dict[str, Any]) -> int | None:
    for key in ("pdfTextQuotes", "pdfTextPositions", "pdfRectangles"):
        value = first_selector(discussion, key).get("pageNumber")
        if isinstance(value, int):
            return value
    return None


def start_position(discussion: dict[str, Any]) -> int | None:
    value = first_selector(discussion, "pdfTextPositions").get("start")
    return value if isinstance(value, int) else None


def quote_parts(discussion: dict[str, Any]) -> tuple[str, str, str]:
    selectors = discussion.get("target", {}).get("selectors", {})
    quote = selectors.get("textQuote") or first_selector(discussion, "pdfTextQuotes")
    if not isinstance(quote, dict):
        return "", "", ""
    return (
        clean_text(quote.get("content")),
        clean_text(quote.get("prefix")),
        clean_text(quote.get("suffix")),
    )


def normalize_discussion(discussion: dict[str, Any]) -> ImportableDiscussion:
    selected_text, prefix, suffix = quote_parts(discussion)
    title = clean_text(discussion.get("title")) or "PaperHive comment"
    return ImportableDiscussion(
        raw=discussion,
        discussion_id=clean_text(discussion.get("id")),
        title=title,
        body=clean_text(discussion.get("body")),
        author=author_name(discussion.get("author")),
        created_at=clean_text(discussion.get("createdAt")),
        page=page_number(discussion),
        start=start_position(discussion),
        selected_text=selected_text,
        prefix=prefix,
        suffix=suffix,
    )


def sort_key(discussion: ImportableDiscussion) -> tuple[int, int, str]:
    page = discussion.page if discussion.page is not None else 999999
    start = discussion.start if discussion.start is not None else 999999
    return page, start, discussion.created_at


def truncate_one_line(value: str, limit: int) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "..."


def issue_title(discussion: ImportableDiscussion) -> str:
    page = f"p.{discussion.page}" if discussion.page is not None else "no page"
    title = truncate_one_line(discussion.title, 150)
    return f"PaperHive {page}: {title}"


def fence(text: str, language: str = "text") -> str:
    if not text:
        return "_None provided._"
    fence_len = max((len(match.group(0)) for match in re.finditer(r"`+", text)), default=2) + 1
    ticks = "`" * max(3, fence_len)
    return f"{ticks}{language}\n{text}\n{ticks}"


def clipped(value: str, limit: int = 1400) -> str:
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "\n...[truncated]"


def context_text(discussion: ImportableDiscussion) -> str:
    if not any((discussion.prefix, discussion.selected_text, discussion.suffix)):
        return ""
    return f"{discussion.prefix}[{discussion.selected_text}]{discussion.suffix}".strip()


def discussion_url(item_id: str, discussion_id: str) -> str:
    return f"{PAPERHIVE_ITEM_URL.format(item_id=item_id)}?discussion={discussion_id}"


def issue_body(discussion: ImportableDiscussion, *, item_id: str, source_url: str) -> str:
    page = str(discussion.page) if discussion.page is not None else "Unknown"
    start = str(discussion.start) if discussion.start is not None else "Unknown"
    lines = [
        f"<!-- paperhive-discussion:{discussion.discussion_id} -->",
        "Imported from PaperHive proofreading comments.",
        "",
        f"- PaperHive discussion ID: `{discussion.discussion_id}`",
        f"- PaperHive link: {discussion_url(item_id, discussion.discussion_id)}",
        f"- Feed source: {source_url}",
        f"- PDF page: {page}",
        f"- PDF text position: {start}",
        f"- Author: {discussion.author}",
        f"- Created: {discussion.created_at or 'Unknown'}",
        "",
        "Selected text:",
        "",
        fence(clipped(discussion.selected_text)),
        "",
        "Context:",
        "",
        fence(clipped(context_text(discussion))),
        "",
        "Comment:",
        "",
        f"**{discussion.title}**",
    ]

    if discussion.body:
        lines.extend(["", fence(clipped(discussion.body))])

    replies = discussion.raw.get("replies") or []
    if replies:
        lines.extend(["", "Replies:"])
        for reply in replies:
            reply_author = author_name(reply.get("author"))
            reply_created = clean_text(reply.get("createdAt")) or "Unknown date"
            reply_body = clean_text(reply.get("body"))
            lines.extend(["", f"**{reply_author}**, {reply_created}", "", fence(clipped(reply_body))])

    return "\n".join(lines).strip() + "\n"


def existing_issue_markers(repo: str) -> dict[str, dict[str, Any]]:
    result = run_gh(
        [
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--limit",
            "1000",
            "--json",
            "number,title,body,url",
        ]
    )
    issues = json.loads(result.stdout or "[]")
    markers: dict[str, dict[str, Any]] = {}
    for issue in issues:
        body = issue.get("body") or ""
        match = MARKER_RE.search(body)
        if match:
            markers[match.group(1)] = issue
    return markers


def ensure_labels(repo: str, labels: tuple[str, ...]) -> None:
    label_specs = {
        "paperhive": ("0E8A16", "Imported PaperHive comments"),
        "proofreading": ("FBCA04", "Proofreading and copyediting comments"),
    }
    for label in labels:
        color, description = label_specs.get(label, ("CCCCCC", "Imported issue label"))
        run_gh(
            [
                "label",
                "create",
                label,
                "--repo",
                repo,
                "--color",
                color,
                "--description",
                description,
                "--force",
            ]
        )


def write_outputs(
    out_dir: Path,
    *,
    item: dict[str, Any],
    discussions: list[ImportableDiscussion],
    raw_discussions: dict[str, Any],
    repo: str,
    source_url: str,
    item_id: str,
    existing: dict[str, dict[str, Any]],
    labels: tuple[str, ...],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "paperhive-document-item.json").write_text(
        json.dumps(item, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (out_dir / "paperhive-discussions.json").write_text(
        json.dumps(raw_discussions, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# PaperHive proofreading import preview",
        "",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- Repository: `{repo}`",
        f"- PaperHive item: `{item_id}`",
        f"- Discussion feed: {source_url}",
        f"- Total discussions: {len(discussions)}",
        f"- Existing imported issues: {len(existing)}",
        f"- Labels: {', '.join(labels) if labels else 'none'}",
        "",
    ]

    for discussion in discussions:
        existing_issue = existing.get(discussion.discussion_id)
        status = "already imported" if existing_issue else "pending"
        lines.extend(
            [
                f"## {issue_title(discussion)}",
                "",
                f"- Status: {status}",
                f"- Discussion ID: `{discussion.discussion_id}`",
                f"- GitHub issue: {existing_issue['url']}" if existing_issue else "- GitHub issue: not created",
                f"- Author: {discussion.author}",
                f"- Created: {discussion.created_at or 'Unknown'}",
                f"- Link: {discussion_url(item_id, discussion.discussion_id)}",
                "",
                "Selected text:",
                "",
                fence(clipped(discussion.selected_text, 500)),
                "",
                "Comment:",
                "",
                f"**{discussion.title}**",
                "",
            ]
        )
        if discussion.body:
            lines.extend([fence(clipped(discussion.body, 500)), ""])

    (out_dir / "paperhive-issues-preview.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def create_issue(
    discussion: ImportableDiscussion,
    *,
    repo: str,
    item_id: str,
    source_url: str,
    labels: tuple[str, ...],
) -> str:
    body = issue_body(discussion, item_id=item_id, source_url=source_url)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as body_file:
        body_file.write(body)
        body_path = Path(body_file.name)
    try:
        args = [
            "issue",
            "create",
            "--repo",
            repo,
            "--title",
            issue_title(discussion),
            "--body-file",
            str(body_path),
        ]
        for label in labels:
            args.extend(["--label", label])
        result = run_gh(args)
        return result.stdout.strip()
    finally:
        body_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--item-id", default=DEFAULT_ITEM_ID, help="PaperHive document item id")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repository in OWNER/REPO form")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Directory for raw JSON and preview output")
    parser.add_argument("--label", action="append", dest="labels", help="GitHub label to apply; repeatable")
    parser.add_argument("--no-labels", action="store_true", help="Do not create or apply GitHub labels")
    parser.add_argument("--apply", action="store_true", help="Create GitHub issues. Without this, only writes a preview.")
    parser.add_argument("--limit", type=int, help="Import at most N pending discussions")
    parser.add_argument("--sleep", type=float, default=0.25, help="Seconds to sleep between issue creations")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    labels = () if args.no_labels else (tuple(args.labels) if args.labels else DEFAULT_LABELS)

    item_url = ITEM_URL.format(item_id=args.item_id)
    item = fetch_json(item_url)
    document_id = item.get("document")
    if not document_id:
        raise SystemExit(f"No document id found in {item_url}")

    source_url = DISCUSSIONS_URL.format(document_id=document_id)
    raw_discussions = fetch_json(source_url)
    discussions = [
        normalize_discussion(discussion)
        for discussion in raw_discussions.get("discussions", [])
        if isinstance(discussion, dict)
    ]
    discussions.sort(key=sort_key)

    existing = existing_issue_markers(args.repo)
    write_outputs(
        args.out_dir,
        item=item,
        discussions=discussions,
        raw_discussions=raw_discussions,
        repo=args.repo,
        source_url=source_url,
        item_id=args.item_id,
        existing=existing,
        labels=labels,
    )

    pending = [discussion for discussion in discussions if discussion.discussion_id not in existing]
    if args.limit is not None:
        pending = pending[: args.limit]

    print(f"Fetched {len(discussions)} PaperHive discussions.")
    print(f"Found {len(existing)} previously imported GitHub issues.")
    print(f"Pending imports in this run: {len(pending)}.")
    print(f"Wrote preview to {args.out_dir / 'paperhive-issues-preview.md'}.")

    if not args.apply:
        print("Dry run only. Re-run with --apply to create issues.")
        return

    ensure_labels(args.repo, labels)

    created: list[dict[str, Any]] = []
    for index, discussion in enumerate(pending, start=1):
        url = create_issue(
            discussion,
            repo=args.repo,
            item_id=args.item_id,
            source_url=source_url,
            labels=labels,
        )
        record = {
            "discussionId": discussion.discussion_id,
            "page": discussion.page,
            "title": issue_title(discussion),
            "url": url,
        }
        created.append(record)
        print(f"[{index}/{len(pending)}] {url} {record['title']}", flush=True)
        if args.sleep > 0 and index < len(pending):
            time.sleep(args.sleep)

    import_record = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "repo": args.repo,
        "itemId": args.item_id,
        "documentId": document_id,
        "sourceUrl": source_url,
        "totalDiscussions": len(discussions),
        "existingBeforeRun": len(existing),
        "created": created,
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "github-issue-import.json").write_text(
        json.dumps(import_record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote import record to {args.out_dir / 'github-issue-import.json'}.")


if __name__ == "__main__":
    main()
