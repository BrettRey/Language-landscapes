#!/usr/bin/env python3
"""Local AI companion surface for the Language Landscapes manuscript.

Features:
- zero third-party Python dependencies
- retrieval over ai-companion/export/book_chunks.jsonl
- richer local web interface with Read, Ask, Contents, Glossary, and Index
- source inspector backed by structured book metadata
- optional OpenAI generation when OPENAI_API_KEY is set
- CLI ask mode for quick verification
"""

from __future__ import annotations

import argparse
import errno
import json
import math
import os
import re
import textwrap
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from collections import Counter, defaultdict
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
EXPORT_DIR = ROOT / "ai-companion" / "export"
WEB_DIR = ROOT / "ai-companion" / "web"
DEFAULT_CHUNKS = EXPORT_DIR / "book_chunks.jsonl"
DEFAULT_MANIFEST = EXPORT_DIR / "book_manifest.json"
DEFAULT_TOC = EXPORT_DIR / "table_of_contents.json"
DEFAULT_SYSTEM_PROMPT = ROOT / "ai-companion" / "system-prompt.md"
DEFAULT_INDEX_OUTLINE = ROOT / "index-outline.tex"
DEFAULT_INDEX_CROSSREFS = ROOT / "localseealso.tex"
DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5")
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_TOP_K = 5

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
    "you",
    "your",
}

BLOCK_LEVELS = {
    "chapter": 1,
    "section": 2,
    "subsection": 3,
    "subsubsection": 4,
    "box": 5,
}

EXAMPLE_PROMPTS = [
    "What distinction does the book make between categories and functions?",
    "How does the book treat Standard English and what to teach?",
    "What is pragmatic negation?",
    "How does the book define grammaticality?",
    "Where does the book discuss conversation and turn-taking?",
]


@dataclass
class Chunk:
    chunk_id: str
    anchor: str
    source_path: str
    chapter_title: str | None
    section_title: str | None
    subsection_title: str | None
    subsubsection_title: str | None
    box_title: str | None
    block_type: str
    labels: list[str]
    text: str
    word_count: int
    char_count: int
    part_index: int
    part_count: int


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def snippet(text: str, limit: int = 240) -> str:
    clean = normalize_spaces(text)
    if len(clean) <= limit:
        return clean
    return clean[: limit - 1].rstrip() + "…"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "item"


def dedupe_preserve(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def paragraph_blocks(text: str) -> list[str]:
    return [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]


def load_chunks(path: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            chunks.append(
                Chunk(
                    chunk_id=row["chunk_id"],
                    anchor=row["anchor"],
                    source_path=row["source_path"],
                    chapter_title=row["chapter_title"],
                    section_title=row["section_title"],
                    subsection_title=row["subsection_title"],
                    subsubsection_title=row["subsubsection_title"],
                    box_title=row["box_title"],
                    block_type=row["block_type"],
                    labels=row["labels"],
                    text=row["text"],
                    word_count=row["word_count"],
                    char_count=row["char_count"],
                    part_index=int(row.get("part_index", 1)),
                    part_count=int(row.get("part_count", 1)),
                )
            )
    return chunks


class Retriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.doc_term_counts: list[Counter[str]] = []
        self.doc_title_counts: list[Counter[str]] = []
        self.doc_norms: list[float] = []
        self.idf: dict[str, float] = {}
        self._build_index()

    def _build_index(self) -> None:
        doc_freq: Counter[str] = Counter()
        for chunk in self.chunks:
            terms = [tok for tok in tokenize(chunk.text) if tok not in STOPWORDS]
            counts = Counter(terms)
            self.doc_term_counts.append(counts)

            title_text = " ".join(
                part
                for part in [
                    chunk.chapter_title,
                    chunk.section_title,
                    chunk.subsection_title,
                    chunk.subsubsection_title,
                    chunk.box_title,
                    chunk.anchor,
                ]
                if part
            )
            title_counts = Counter(tok for tok in tokenize(title_text) if tok not in STOPWORDS)
            self.doc_title_counts.append(title_counts)

            for token in counts:
                doc_freq[token] += 1

        total_docs = max(1, len(self.chunks))
        self.idf = {
            token: math.log((1 + total_docs) / (1 + freq)) + 1.0
            for token, freq in doc_freq.items()
        }

        for counts in self.doc_term_counts:
            norm_sq = 0.0
            for token, tf in counts.items():
                weight = (1.0 + math.log(tf)) * self.idf.get(token, 0.0)
                norm_sq += weight * weight
            self.doc_norms.append(math.sqrt(norm_sq) or 1.0)

    def search(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        allowed_indices: set[int] | None = None,
    ) -> list[dict[str, Any]]:
        if allowed_indices is not None and not allowed_indices:
            return []

        query_tokens = [tok for tok in tokenize(query) if tok not in STOPWORDS]
        if not query_tokens:
            query_tokens = tokenize(query)

        query_counts = Counter(query_tokens)
        query_weights: dict[str, float] = {}
        query_norm_sq = 0.0
        for token, tf in query_counts.items():
            weight = (1.0 + math.log(tf)) * self.idf.get(token, math.log(1 + len(self.chunks)))
            query_weights[token] = weight
            query_norm_sq += weight * weight
        query_norm = math.sqrt(query_norm_sq) or 1.0

        phrase = normalize_spaces(query.lower())
        results: list[dict[str, Any]] = []
        for idx, chunk in enumerate(self.chunks):
            if allowed_indices is not None and idx not in allowed_indices:
                continue

            dot = 0.0
            doc_counts = self.doc_term_counts[idx]
            for token, q_weight in query_weights.items():
                tf = doc_counts.get(token)
                if not tf:
                    continue
                d_weight = (1.0 + math.log(tf)) * self.idf.get(token, 0.0)
                dot += q_weight * d_weight
            cosine = dot / (self.doc_norms[idx] * query_norm)

            title_counts = self.doc_title_counts[idx]
            title_overlap = sum(title_counts.get(token, 0) for token in query_counts)
            title_boost = 0.07 * title_overlap
            exact_phrase_boost = 0.15 if phrase and phrase in chunk.text.lower() else 0.0

            score = cosine + title_boost + exact_phrase_boost
            if score <= 0:
                continue
            results.append(
                {
                    "score": round(score, 4),
                    "chunk": chunk,
                    "chunk_index": idx,
                }
            )

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:top_k]


def build_context_block(results: list[dict[str, Any]]) -> str:
    blocks = []
    for idx, item in enumerate(results, start=1):
        chunk: Chunk = item["chunk"]
        blocks.append(
            "\n".join(
                [
                    f"[{idx}] {chunk.anchor}",
                    f"chunk_id: {chunk.chunk_id}",
                    f"source_path: {chunk.source_path}",
                    f"score: {item['score']}",
                    "text:",
                    chunk.text,
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


def build_openai_prompt(
    system_prompt: str,
    question: str,
    results: list[dict[str, Any]],
    history: list[dict[str, str]],
    scope_label: str,
) -> tuple[str, str]:
    context_block = build_context_block(results)
    history_lines = []
    for turn in history[-8:]:
        role = turn.get("role", "user").upper()
        content = turn.get("content", "").strip()
        if content:
            history_lines.append(f"{role}: {content}")
    history_block = "\n".join(history_lines) if history_lines else "None"

    instructions = textwrap.dedent(
        f"""\
        {system_prompt}

        Additional runtime rules:
        - The current answer is scoped to {scope_label}.
        - Answer strictly from the retrieved book chunks unless you explicitly mark something as outside the book.
        - If the retrieved chunks are weak or partial, say so.
        - Cite the book by anchor in every answer.
        - Prefer short, direct answers.
        """
    ).strip()

    user_input = textwrap.dedent(
        f"""\
        Conversation history:
        {history_block}

        Retrieved book chunks:
        {context_block}

        User question:
        {question}
        """
    ).strip()
    return instructions, user_input


def extract_output_text(response_json: dict[str, Any]) -> str:
    output_items = response_json.get("output", [])
    texts: list[str] = []
    for item in output_items:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            ctype = content.get("type")
            if ctype in {"output_text", "text"}:
                texts.append(content.get("text", ""))
    return "\n".join(part for part in texts if part).strip()


def call_openai(
    *,
    model: str,
    instructions: str,
    user_input: str,
    api_key: str,
) -> str:
    payload = {
        "model": model,
        "instructions": instructions,
        "input": user_input,
        "max_output_tokens": 900,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        body = json.loads(response.read().decode("utf-8"))
    text = extract_output_text(body)
    if not text:
        raise RuntimeError("OpenAI response did not contain output text.")
    return text


def build_fallback_answer(
    question: str,
    results: list[dict[str, Any]],
    scope_label: str,
    reason: str | None = None,
) -> str:
    if not results:
        base = f"I could not find a strong match inside {scope_label}."
        if reason:
            return f"{reason}\n\n{base}"
        return base

    lines = []
    if reason:
        lines.extend([reason, ""])
    lines.append(f"I do not have model generation available, so here are the best matching passages in {scope_label} for {question!r}:")
    lines.append("")
    for idx, item in enumerate(results[:3], start=1):
        chunk: Chunk = item["chunk"]
        lines.append(f"{idx}. {chunk.anchor}: {snippet(chunk.text, limit=280)}")
    return "\n".join(lines)


def chapter_groups_from_toc(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for row in rows:
        if row.get("block_type") == "chapter":
            if (
                current
                and current["chapter_title"] == row["title"]
                and current["include_path"] == row["include_path"]
                and all(item.get("block_type") == "box" for item in current["items"][1:])
            ):
                continue
            if current:
                groups.append(current)
            current = {
                "chapter_title": row["title"],
                "include_path": row["include_path"],
                "items": [row],
            }
            continue
        if current is not None:
            current["items"].append(row)
    if current:
        groups.append(current)
    return groups


def heading_from_chunk(chunk: Chunk) -> str | None:
    if chunk.block_type == "box":
        return chunk.box_title or "Box"
    if chunk.block_type == "subsubsection":
        return chunk.subsubsection_title
    if chunk.block_type == "subsection":
        return chunk.subsection_title
    if chunk.block_type == "section":
        return chunk.section_title
    if chunk.block_type == "chapter":
        return chunk.chapter_title
    return chunk.anchor


def path_from_chunk(chunk: Chunk) -> list[str]:
    parts = [chunk.chapter_title]
    for value in [chunk.section_title, chunk.subsection_title, chunk.subsubsection_title]:
        if value:
            parts.append(value)
    if chunk.block_type == "box" and chunk.box_title:
        parts.append(f"Box: {chunk.box_title}")
    return [part for part in parts if part]


def parse_glossary_entries(chunks: list[Chunk]) -> list[dict[str, Any]]:
    glossary_text = "\n\n".join(chunk.text for chunk in chunks if chunk.chapter_title == "Glossary")
    pattern = re.compile(r"- \[([^\]]+)\]\s+(.*?)(?=\n\s*-\s+\[|\Z)", re.S)
    entries: list[dict[str, Any]] = []
    for match in pattern.finditer(glossary_text):
        term = normalize_spaces(match.group(1))
        definition = normalize_spaces(match.group(2))
        entries.append(
            {
                "term": term,
                "slug": slugify(term),
                "definition": definition,
                "excerpt": snippet(definition, 180),
            }
        )
    entries.sort(key=lambda entry: entry["term"].lower())
    return entries


def clean_index_text(text: str) -> str:
    text = text.strip()
    if "@" in text:
        _, text = text.split("@", 1)
    replacements = {
        r"\textit{": "",
        r"\emph{": "",
        r"\mention{": "",
        r"\ae": "ae",
        r"\textupsilon": "u",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = re.sub(r"\\[a-zA-Z]+\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("``", '"').replace("''", '"')
    return normalize_spaces(text)


def split_index_refs(raw: str) -> list[str]:
    pieces = raw.split(";") if ";" in raw else [raw]
    cleaned = [clean_index_text(piece.strip(" ,;")) for piece in pieces if piece.strip(" ,;")]
    return [piece for piece in cleaned if piece]


def parse_index_crossrefs(path: Path) -> dict[str, dict[str, list[str]]]:
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    mapping: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"see": [], "seealso": []})
    pattern = re.compile(r"\\is\{(.+?)\|see(also)?\s*\{(.+?)\}\}")
    for raw_term, also_flag, raw_target in pattern.findall(text):
        term = clean_index_text(raw_term)
        if not term:
            continue
        kind = "seealso" if also_flag else "see"
        mapping[term.lower()][kind].extend(split_index_refs(raw_target))
    return {key: {"see": dedupe_preserve(value["see"]), "seealso": dedupe_preserve(value["seealso"])} for key, value in mapping.items()}


def parse_index_entries(outline_path: Path, crossref_path: Path) -> list[dict[str, Any]]:
    if not outline_path.exists():
        return []

    crossrefs = parse_index_crossrefs(crossref_path)
    lines = outline_path.read_text(encoding="utf-8").splitlines()
    entries: list[dict[str, Any]] = []
    stack: list[str] = []
    last_by_depth: dict[int, dict[str, Any]] = {}

    for raw_line in lines:
        if not raw_line.strip():
            continue
        line = raw_line.rstrip()
        depth = len(line) - len(line.lstrip("!"))
        content = line[depth:].strip()
        if not content:
            continue

        if content.startswith("→"):
            parent = last_by_depth.get(depth - 1)
            if parent:
                parent["seealso"] = dedupe_preserve(parent["seealso"] + split_index_refs(content[1:]))
            continue

        see: list[str] = []
        seealso: list[str] = []

        inline_match = re.search(r"\((see|seealso):\s*([^)]+)\)\s*$", content)
        if inline_match:
            if inline_match.group(1) == "see":
                see.extend(split_index_refs(inline_match.group(2)))
            else:
                seealso.extend(split_index_refs(inline_match.group(2)))
            content = content[: inline_match.start()].strip()

        if "→" in content:
            left, right = content.split("→", 1)
            if left.strip():
                content = left.strip()
                seealso.extend(split_index_refs(right))
            else:
                parent = last_by_depth.get(depth - 1)
                if parent:
                    parent["seealso"] = dedupe_preserve(parent["seealso"] + split_index_refs(right))
                continue

        term = clean_index_text(content)
        if not term:
            continue

        stack = stack[:depth]
        stack.append(term)
        path_terms = list(stack)

        inherited = crossrefs.get(term.lower(), {"see": [], "seealso": []})
        entry = {
            "id": f"idx-{len(entries) + 1}",
            "term": term,
            "slug": slugify("-".join(path_terms)),
            "level": depth,
            "path": path_terms,
            "path_display": " > ".join(path_terms),
            "see": dedupe_preserve(see + inherited["see"]),
            "seealso": dedupe_preserve(seealso + inherited["seealso"]),
        }
        entries.append(entry)
        last_by_depth[depth] = entry
    return entries


def first_sentence(text: str) -> str:
    parts = re.split(r"(?<=[.!?])\s+", normalize_spaces(text))
    return parts[0] if parts else normalize_spaces(text)


class ChatApp:
    def __init__(
        self,
        *,
        chunks_path: Path,
        manifest_path: Path,
        toc_path: Path,
        system_prompt_path: Path,
        index_outline_path: Path,
        index_crossrefs_path: Path,
        default_model: str,
        web_dir: Path,
    ) -> None:
        self.chunks_path = chunks_path
        self.manifest_path = manifest_path
        self.toc_path = toc_path
        self.system_prompt_path = system_prompt_path
        self.index_outline_path = index_outline_path
        self.index_crossrefs_path = index_crossrefs_path
        self.default_model = default_model
        self.web_dir = web_dir

        self.system_prompt = system_prompt_path.read_text(encoding="utf-8").strip()
        self.manifest = load_json(manifest_path)
        self.toc_rows = load_json(toc_path)
        self.chunks = load_chunks(chunks_path)
        self.retriever = Retriever(self.chunks)
        self.openai_key = os.environ.get("OPENAI_API_KEY")

        self.chunk_index_by_id = {chunk.chunk_id: idx for idx, chunk in enumerate(self.chunks)}
        self.chunks_by_id = {chunk.chunk_id: chunk for chunk in self.chunks}

        self.chapter_order: list[str] = []
        self.chapter_by_id: dict[str, dict[str, Any]] = {}
        self.chapter_id_by_title: dict[str, str] = {}
        self.passage_by_id: dict[str, dict[str, Any]] = {}
        self.passage_id_by_chunk_id: dict[str, str] = {}
        self.allowed_indices_by_chapter_id: dict[str, set[int]] = {}
        self.allowed_indices_by_passage_id: dict[str, set[int]] = {}

        self._build_book_structure()
        self.glossary_entries = self._build_glossary_entries()
        self.index_entries = parse_index_entries(self.index_outline_path, self.index_crossrefs_path)
        self.landing_source = self._build_landing_source()

    def _build_book_structure(self) -> None:
        chunks_by_chapter: dict[str, list[Chunk]] = defaultdict(list)
        for chunk in self.chunks:
            if chunk.chapter_title:
                chunks_by_chapter[chunk.chapter_title].append(chunk)

        toc_groups = chapter_groups_from_toc(self.toc_rows)
        used_ids: set[str] = set()

        for position, group in enumerate(toc_groups, start=1):
            title = group["chapter_title"]
            chapter_id = slugify(title)
            suffix = 2
            while chapter_id in used_ids:
                chapter_id = f"{slugify(title)}-{suffix}"
                suffix += 1
            used_ids.add(chapter_id)

            chapter_chunks = chunks_by_chapter.get(title, [])
            passages = self._build_passages(chapter_id, chapter_chunks)
            toc_items = [self._toc_item_payload(item) for item in group["items"][1:]]
            source_path = chapter_chunks[0].source_path if chapter_chunks else group["include_path"]
            word_count = sum(chunk.word_count for chunk in chapter_chunks)
            char_count = sum(chunk.char_count for chunk in chapter_chunks)
            minutes = round(word_count / 155.0, 1) if word_count else 0.0

            chapter_record = {
                "id": chapter_id,
                "position": position,
                "title": title,
                "source_path": source_path,
                "word_count": word_count,
                "char_count": char_count,
                "minutes": minutes,
                "section_count": sum(1 for item in toc_items if item["level"] in {2, 3, 4}),
                "toc_items": toc_items,
                "passage_ids": [passage["passage_id"] for passage in passages],
                "teaser": self._chapter_teaser(passages),
            }
            self.chapter_order.append(chapter_id)
            self.chapter_by_id[chapter_id] = chapter_record
            self.chapter_id_by_title[title] = chapter_id
            self.allowed_indices_by_chapter_id[chapter_id] = {
                self.chunk_index_by_id[chunk.chunk_id]
                for chunk in chapter_chunks
            }

    def _toc_item_payload(self, item: dict[str, Any]) -> dict[str, Any]:
        level = BLOCK_LEVELS.get(str(item.get("block_type")), 6)
        return {
            "anchor": item["anchor"],
            "title": item["title"],
            "block_type": item["block_type"],
            "level": level,
        }

    def _build_passages(self, chapter_id: str, chapter_chunks: list[Chunk]) -> list[dict[str, Any]]:
        passages: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None

        def flush() -> None:
            nonlocal current
            if current is None:
                return
            passage = {
                "passage_id": current["chunk_ids"][0],
                "chapter_id": chapter_id,
                "chapter_title": current["chapter_title"],
                "anchor": current["anchor"],
                "heading": current["heading"],
                "path": current["path"],
                "source_path": current["source_path"],
                "block_type": current["block_type"],
                "level": current["level"],
                "text": "\n\n".join(part.strip() for part in current["text_parts"] if part.strip()),
                "chunk_ids": list(current["chunk_ids"]),
            }
            passages.append(passage)
            self.passage_by_id[passage["passage_id"]] = passage
            self.allowed_indices_by_passage_id[passage["passage_id"]] = {
                self.chunk_index_by_id[chunk_id]
                for chunk_id in passage["chunk_ids"]
            }
            for chunk_id in passage["chunk_ids"]:
                self.passage_id_by_chunk_id[chunk_id] = passage["passage_id"]
            current = None

        for chunk in chapter_chunks:
            if current and current["anchor"] == chunk.anchor and current["block_type"] == chunk.block_type:
                current["text_parts"].append(chunk.text)
                current["chunk_ids"].append(chunk.chunk_id)
                continue

            flush()
            current = {
                "chapter_title": chunk.chapter_title,
                "anchor": chunk.anchor,
                "heading": heading_from_chunk(chunk),
                "path": path_from_chunk(chunk),
                "source_path": chunk.source_path,
                "block_type": chunk.block_type,
                "level": BLOCK_LEVELS.get(chunk.block_type, 6),
                "text_parts": [chunk.text],
                "chunk_ids": [chunk.chunk_id],
            }

        flush()
        return passages

    def _chapter_teaser(self, passages: list[dict[str, Any]]) -> str:
        for passage in passages:
            if passage["chapter_title"] == "Glossary":
                continue
            if passage["block_type"] == "box":
                continue
            clean = normalize_spaces(passage["text"])
            if len(clean) >= 120:
                return snippet(clean, 220)
        for passage in passages:
            clean = normalize_spaces(passage["text"])
            if clean:
                return snippet(clean, 220)
        return ""

    def _build_glossary_entries(self) -> list[dict[str, Any]]:
        entries = parse_glossary_entries(self.chunks)
        for entry in entries:
            term_results = self.retriever.search(entry["term"], top_k=6)
            related: list[dict[str, str]] = []
            for item in term_results:
                chapter_title = item["chunk"].chapter_title
                if not chapter_title or chapter_title == "Glossary":
                    continue
                chapter_id = self.chapter_id_by_title.get(chapter_title)
                if not chapter_id:
                    continue
                related.append({"id": chapter_id, "title": chapter_title})
            entry["related_chapters"] = dedupe_preserve_json(related, key_field="id")[:4]
            entry["plain_hint"] = first_sentence(entry["definition"])
        return entries

    def _build_landing_source(self) -> dict[str, Any]:
        for chunk in self.chunks:
            if chunk.chapter_title == "Preface":
                return self._source_payload_from_chunk(chunk, score=None)
        return self._source_payload_from_chunk(self.chunks[0], score=None)

    def _source_payload_from_chunk(self, chunk: Chunk, score: float | None) -> dict[str, Any]:
        passage = self.passage_by_id[self.passage_id_by_chunk_id[chunk.chunk_id]]
        return {
            "chunk_id": chunk.chunk_id,
            "passage_id": passage["passage_id"],
            "chapter_id": passage["chapter_id"],
            "chapter_title": passage["chapter_title"],
            "anchor": passage["anchor"],
            "title": passage["heading"] or passage["anchor"],
            "path": passage["path"],
            "source_path": passage["source_path"],
            "block_type": passage["block_type"],
            "score": score,
            "preview": snippet(passage["text"], 320),
        }

    def _sources_payload(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen_passages: set[str] = set()
        payload: list[dict[str, Any]] = []
        for item in results:
            chunk: Chunk = item["chunk"]
            passage_id = self.passage_id_by_chunk_id[chunk.chunk_id]
            if passage_id in seen_passages:
                continue
            seen_passages.add(passage_id)
            payload.append(self._source_payload_from_chunk(chunk, score=item["score"]))
        return payload

    def _scope_details(self, scope: dict[str, Any] | None) -> tuple[set[int] | None, dict[str, Any]]:
        mode = str((scope or {}).get("mode") or "book").strip().lower()
        value = str((scope or {}).get("value") or "").strip()

        if mode == "chapter" and value in self.chapter_by_id:
            chapter = self.chapter_by_id[value]
            return self.allowed_indices_by_chapter_id[value], {
                "mode": "chapter",
                "value": value,
                "display_label": f"Chapter: {chapter['title']}",
                "prompt_label": f"chapter {chapter['title']}",
            }

        if mode == "passage" and value in self.passage_by_id:
            passage = self.passage_by_id[value]
            return self.allowed_indices_by_passage_id[value], {
                "mode": "passage",
                "value": value,
                "display_label": f"Section: {passage['anchor']}",
                "prompt_label": f"section {passage['anchor']}",
                "chapter_id": passage["chapter_id"],
            }

        return None, {
            "mode": "book",
            "value": None,
            "display_label": "Whole book",
            "prompt_label": "the whole book",
        }

    def _related_chapters_for_query(self, query: str) -> list[dict[str, Any]]:
        chapter_scores: dict[str, float] = defaultdict(float)
        for item in self.retriever.search(query, top_k=12):
            chunk: Chunk = item["chunk"]
            if not chunk.chapter_title or chunk.chapter_title == "Glossary":
                continue
            chapter_id = self.chapter_id_by_title.get(chunk.chapter_title)
            if not chapter_id:
                continue
            chapter_scores[chapter_id] += float(item["score"])

        ranked = sorted(chapter_scores.items(), key=lambda pair: pair[1], reverse=True)
        return [self._chapter_summary(chapter_id) for chapter_id, _score in ranked[:4]]

    def _chapter_summary(self, chapter_id: str) -> dict[str, Any]:
        chapter = self.chapter_by_id[chapter_id]
        return {
            "id": chapter["id"],
            "position": chapter["position"],
            "title": chapter["title"],
            "source_path": chapter["source_path"],
            "word_count": chapter["word_count"],
            "minutes": chapter["minutes"],
            "section_count": chapter["section_count"],
            "teaser": chapter["teaser"],
        }

    def config(self) -> dict[str, Any]:
        return {
            "book_title": self.manifest["book_title"],
            "book_author": self.manifest["book_author"],
            "chunk_count": len(self.chunks),
            "chapter_count": len(self.chapter_order),
            "total_clean_word_count": self.manifest.get("total_clean_word_count"),
            "estimated_audio_hours_at_155_wpm": self.manifest.get("estimated_audio_hours_at_155_wpm"),
            "chunks_path": str(self.chunks_path.relative_to(ROOT)),
            "default_model": self.default_model,
            "openai_available": bool(self.openai_key),
            "example_prompts": EXAMPLE_PROMPTS,
            "chapters": [self._chapter_summary(chapter_id) for chapter_id in self.chapter_order],
            "glossary_count": len(self.glossary_entries),
            "index_count": len(self.index_entries),
            "landing_source": self.landing_source,
        }

    def chapter_payload(self, chapter_id: str) -> dict[str, Any]:
        chapter = self.chapter_by_id[chapter_id]
        passages = [self.passage_by_id[passage_id] for passage_id in chapter["passage_ids"]]
        return {
            "chapter": {
                **self._chapter_summary(chapter_id),
                "toc_items": chapter["toc_items"],
            },
            "passages": passages,
        }

    def glossary_payload(self) -> dict[str, Any]:
        return {"entries": self.glossary_entries}

    def index_payload(self) -> dict[str, Any]:
        return {"entries": self.index_entries}

    def source_payload(self, chunk_id: str) -> dict[str, Any]:
        chunk = self.chunks_by_id[chunk_id]
        passage_id = self.passage_id_by_chunk_id[chunk_id]
        passage = self.passage_by_id[passage_id]
        chapter = self.chapter_by_id[passage["chapter_id"]]
        passage_ids = chapter["passage_ids"]
        idx = passage_ids.index(passage_id)
        previous_passage = self.passage_by_id[passage_ids[idx - 1]] if idx > 0 else None
        next_passage = self.passage_by_id[passage_ids[idx + 1]] if idx + 1 < len(passage_ids) else None

        return {
            "source": {
                "chunk_id": chunk.chunk_id,
                "passage_id": passage_id,
                "chapter_id": passage["chapter_id"],
                "chapter_title": passage["chapter_title"],
                "anchor": passage["anchor"],
                "title": passage["heading"] or passage["anchor"],
                "path": passage["path"],
                "source_path": passage["source_path"],
                "block_type": passage["block_type"],
                "selected_text": chunk.text,
                "passage_text": passage["text"],
                "chunk_position": chunk.part_index,
                "chunk_total": chunk.part_count,
            },
            "context": {
                "previous": (
                    {
                        "passage_id": previous_passage["passage_id"],
                        "anchor": previous_passage["anchor"],
                        "title": previous_passage["heading"] or previous_passage["anchor"],
                        "preview": snippet(previous_passage["text"], 180),
                    }
                    if previous_passage
                    else None
                ),
                "next": (
                    {
                        "passage_id": next_passage["passage_id"],
                        "anchor": next_passage["anchor"],
                        "title": next_passage["heading"] or next_passage["anchor"],
                        "preview": snippet(next_passage["text"], 180),
                    }
                    if next_passage
                    else None
                ),
            },
        }

    def answer(
        self,
        *,
        question: str,
        history: list[dict[str, str]],
        top_k: int,
        use_openai: bool,
        model: str | None,
        scope: dict[str, Any] | None,
    ) -> dict[str, Any]:
        allowed_indices, scope_details = self._scope_details(scope)
        results = self.retriever.search(question, top_k=top_k, allowed_indices=allowed_indices)
        selected_model = model or self.default_model
        sources = self._sources_payload(results)

        weak_match = not results or results[0]["score"] < 0.11
        related_chapters = self._related_chapters_for_query(question) if weak_match else []

        if use_openai and self.openai_key and results:
            try:
                instructions, user_input = build_openai_prompt(
                    self.system_prompt,
                    question,
                    results,
                    history,
                    scope_details["prompt_label"],
                )
                answer = call_openai(
                    model=selected_model,
                    instructions=instructions,
                    user_input=user_input,
                    api_key=self.openai_key,
                )
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                answer = build_fallback_answer(
                    question,
                    results,
                    scope_details["prompt_label"],
                    reason=f"OpenAI request failed with HTTP {exc.code}. Falling back to retrieval-only mode.\n{body}",
                )
            except Exception as exc:  # noqa: BLE001
                answer = build_fallback_answer(
                    question,
                    results,
                    scope_details["prompt_label"],
                    reason=f"OpenAI generation failed. Falling back to retrieval-only mode.\n{exc}",
                )
        else:
            reason = None
            if use_openai and not self.openai_key:
                reason = "OPENAI_API_KEY is not set. Falling back to retrieval-only mode."
            elif use_openai and not results:
                reason = "No strong retrieved context was available for model generation."
            answer = build_fallback_answer(
                question,
                results,
                scope_details["prompt_label"],
                reason=reason,
            )

        return {
            "answer": answer,
            "sources": sources,
            "used_openai": bool(use_openai and self.openai_key and results),
            "model": selected_model,
            "weak_match": weak_match,
            "related_chapters": related_chapters,
            "scope": {
                "mode": scope_details["mode"],
                "value": scope_details["value"],
                "label": scope_details["display_label"],
            },
        }

    def static_asset(self, path: str) -> tuple[bytes, str] | None:
        asset_path = (self.web_dir / path.lstrip("/")).resolve()
        if not asset_path.is_file() or self.web_dir.resolve() not in asset_path.parents:
            return None

        if asset_path.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        elif asset_path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif asset_path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        else:
            content_type = "application/octet-stream"
        return asset_path.read_bytes(), content_type


def dedupe_preserve_json(items: list[dict[str, Any]], key_field: str) -> list[dict[str, Any]]:
    seen: set[Any] = set()
    out: list[dict[str, Any]] = []
    for item in items:
        key = item.get(key_field)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def make_handler(app: ChatApp) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def _send_json(self, payload: dict[str, Any], status: int = HTTPStatus.OK) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_bytes(self, body: bytes, content_type: str, status: int = HTTPStatus.OK) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            if parsed.path in {"/", "/index.html"}:
                asset = app.static_asset("/index.html")
                if asset:
                    body, content_type = asset
                    self._send_bytes(body, content_type)
                    return
                self.send_error(HTTPStatus.NOT_FOUND)
                return

            if parsed.path in {"/styles.css", "/app.js"}:
                asset = app.static_asset(parsed.path)
                if asset:
                    body, content_type = asset
                    self._send_bytes(body, content_type)
                    return
                self.send_error(HTTPStatus.NOT_FOUND)
                return

            if parsed.path == "/api/config":
                self._send_json(app.config())
                return

            if parsed.path == "/api/read":
                chapter_id = (params.get("chapter_id") or [""])[0]
                if not chapter_id or chapter_id not in app.chapter_by_id:
                    self._send_json({"error": "Valid chapter_id is required."}, status=HTTPStatus.BAD_REQUEST)
                    return
                self._send_json(app.chapter_payload(chapter_id))
                return

            if parsed.path == "/api/glossary":
                self._send_json(app.glossary_payload())
                return

            if parsed.path == "/api/index":
                self._send_json(app.index_payload())
                return

            if parsed.path == "/api/source":
                chunk_id = (params.get("chunk_id") or [""])[0]
                if not chunk_id or chunk_id not in app.chunks_by_id:
                    self._send_json({"error": "Valid chunk_id is required."}, status=HTTPStatus.BAD_REQUEST)
                    return
                self._send_json(app.source_payload(chunk_id))
                return

            self.send_error(HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/api/chat":
                self.send_error(HTTPStatus.NOT_FOUND)
                return

            content_length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON body."}, status=HTTPStatus.BAD_REQUEST)
                return

            question = str(payload.get("question", "")).strip()
            history = payload.get("history", [])
            top_k = int(payload.get("top_k", DEFAULT_TOP_K))
            top_k = max(1, min(12, top_k))
            use_openai = bool(payload.get("use_openai", False))
            model = str(payload.get("model") or "").strip() or None
            scope = payload.get("scope")

            if not question:
                self._send_json({"error": "Question is required."}, status=HTTPStatus.BAD_REQUEST)
                return

            response = app.answer(
                question=question,
                history=history if isinstance(history, list) else [],
                top_k=top_k,
                use_openai=use_openai,
                model=model,
                scope=scope if isinstance(scope, dict) else None,
            )
            self._send_json(response)

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            return

    return Handler


def run_server(host: str, port: int, app: ChatApp, open_browser: bool) -> None:
    server = None
    bound_port = port
    handler = make_handler(app)
    for candidate_port in range(port, port + 20):
        try:
            server = ThreadingHTTPServer((host, candidate_port), handler)
            bound_port = candidate_port
            break
        except OSError as exc:
            if exc.errno != errno.EADDRINUSE:
                raise
    if server is None:
        raise OSError(
            errno.EADDRINUSE,
            f"Could not bind to any port in the range {port}-{port + 19}.",
        )

    url = f"http://{host}:{bound_port}"
    if bound_port != port:
        print(f"Port {port} is already in use. Falling back to {bound_port}.")
    print(f"Serving Language Landscapes AI Companion at {url}")
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()


def run_ask(app: ChatApp, question: str, top_k: int, use_openai: bool, model: str | None) -> int:
    response = app.answer(
        question=question,
        history=[],
        top_k=top_k,
        use_openai=use_openai,
        model=model,
        scope={"mode": "book"},
    )
    print(response["answer"])
    print("\nSources:")
    for source in response["sources"]:
        score = source.get("score")
        if score is None:
            print(f"- {source['anchor']} ({source['chunk_id']})")
        else:
            print(f"- {source['anchor']} ({source['chunk_id']}, score {score})")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS, help="Path to book_chunks.jsonl.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="Path to book_manifest.json.")
    parser.add_argument("--toc", type=Path, default=DEFAULT_TOC, help="Path to table_of_contents.json.")
    parser.add_argument(
        "--system-prompt",
        type=Path,
        default=DEFAULT_SYSTEM_PROMPT,
        help="Path to the system prompt markdown file.",
    )
    parser.add_argument(
        "--index-outline",
        type=Path,
        default=DEFAULT_INDEX_OUTLINE,
        help="Path to the subject index outline source.",
    )
    parser.add_argument(
        "--index-crossrefs",
        type=Path,
        default=DEFAULT_INDEX_CROSSREFS,
        help="Path to subject index cross-reference macros.",
    )
    parser.add_argument("--web-dir", type=Path, default=WEB_DIR, help="Directory containing the local web assets.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Default OpenAI model for UI or ask mode.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    serve = subparsers.add_parser("serve", help="Run the local web companion.")
    serve.add_argument("--host", default=DEFAULT_HOST, help="Host interface to bind.")
    serve.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to bind.")
    serve.add_argument("--no-browser", action="store_true", help="Do not auto-open a browser tab.")

    ask = subparsers.add_parser("ask", help="Ask a single question on the command line.")
    ask.add_argument("question", help="Question to ask about the book.")
    ask.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="Number of chunks to retrieve.")
    ask.add_argument(
        "--use-openai",
        action="store_true",
        help="Use OpenAI generation if OPENAI_API_KEY is set.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    app = ChatApp(
        chunks_path=args.chunks.resolve(),
        manifest_path=args.manifest.resolve(),
        toc_path=args.toc.resolve(),
        system_prompt_path=args.system_prompt.resolve(),
        index_outline_path=args.index_outline.resolve(),
        index_crossrefs_path=args.index_crossrefs.resolve(),
        default_model=args.model,
        web_dir=args.web_dir.resolve(),
    )

    if args.command == "serve":
        run_server(args.host, args.port, app, open_browser=not args.no_browser)
        return 0
    if args.command == "ask":
        return run_ask(app, args.question, args.top_k, args.use_openai, args.model)
    raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
