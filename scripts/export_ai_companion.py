#!/usr/bin/env python3
"""Export the LaTeX manuscript into structured assets for an AI companion.

The output is designed for retrieval-based systems rather than raw full-text
upload. Each chunk carries chapter/section metadata so an assistant can cite
the book by location instead of free-associating across the whole manuscript.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


BOOK_TITLE = "Language landscapes"
BOOK_AUTHOR = "Brett Reynolds"
BOOK_SLUG = "language-landscapes"

HEADING_COMMANDS = ("chapter", "section", "subsection", "subsubsection")
TEXT_MACRO_REPLACEMENTS = {
    "LaTeX": "LaTeX",
    "TeX": "TeX",
    "lsAcknowledgementTitle": "Acknowledgments",
    "lsPrefaceTitle": "Preface",
}
UNWRAP_ONE_ARG = {
    "emph",
    "enquote",
    "foreignlanguage",
    "mention",
    "term",
    "textbf",
    "textit",
    "textsc",
    "textsf",
    "texttt",
    "uline",
    "uuline",
}
STRIP_ONE_ARG = {
    "Cref",
    "autoref",
    "cref",
    "eqref",
    "il",
    "index",
    "is",
    "ix",
    "label",
    "pageref",
    "ref",
    "refp",
    "vref",
    "Vref",
}
TEXT_CITE_COMMANDS = {"textcite", "citet"}
PAREN_CITE_COMMANDS = {"autocite", "cite", "citealt", "citep", "parencite"}


@dataclass
class Event:
    kind: str
    level: str | None
    title: str
    start: int
    end: int
    body: str | None = None


@dataclass
class Block:
    include_path: str
    block_type: str
    chapter_title: str | None
    section_title: str | None
    subsection_title: str | None
    subsubsection_title: str | None
    box_title: str | None
    raw_tex: str


def strip_line_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        escaped = False
        cut = None
        for idx, char in enumerate(line):
            if char == "%" and not escaped:
                cut = idx
                break
            escaped = char == "\\" and not escaped
            if char != "\\":
                escaped = False
        if cut is not None:
            line = line[:cut]
        lines.append(line)
    return "\n".join(lines)


def skip_whitespace(text: str, idx: int) -> int:
    while idx < len(text) and text[idx].isspace():
        idx += 1
    return idx


def read_group(text: str, idx: int, open_char: str = "{", close_char: str = "}") -> tuple[str, int]:
    if idx >= len(text) or text[idx] != open_char:
        raise ValueError(f"Expected {open_char!r} at position {idx}")

    depth = 0
    chars: list[str] = []
    i = idx
    while i < len(text):
        char = text[i]
        if char == "\\":
            if depth >= 1 and i + 1 < len(text):
                chars.append(char)
                i += 1
                chars.append(text[i])
                i += 1
                continue
        if char == open_char:
            depth += 1
            if depth > 1:
                chars.append(char)
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return "".join(chars), i + 1
            chars.append(char)
        else:
            chars.append(char)
        i += 1
    raise ValueError(f"Unclosed group starting at {idx}")


def read_command_name(text: str, idx: int) -> tuple[str, int]:
    if idx >= len(text) or text[idx] != "\\":
        raise ValueError(f"Expected command at position {idx}")
    i = idx + 1
    if i < len(text) and not text[i].isalpha():
        return text[i], i + 1
    while i < len(text) and text[i].isalpha():
        i += 1
    return text[idx + 1 : i], i


def slugify(value: str) -> str:
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "chunk"


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def sentence_splits(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def load_bib_lookup(bib_path: Path) -> dict[str, dict[str, str]]:
    if not bib_path.exists():
        return {}

    raw = bib_path.read_text(encoding="utf-8")
    lookup: dict[str, dict[str, str]] = {}

    entry_pattern = re.compile(r"@[\w]+\s*\{\s*([^,]+),(.*?)\n\}", re.S)
    for match in entry_pattern.finditer(raw):
        key = match.group(1).strip()
        body = match.group(2)
        author_match = re.search(r"author\s*=\s*\{(.*?)\}", body, re.S | re.I)
        year_match = re.search(r"year\s*=\s*\{(.*?)\}", body, re.S | re.I)
        date_match = re.search(r"date\s*=\s*\{(.*?)\}", body, re.S | re.I)
        author = author_match.group(1).strip() if author_match else key
        year_source = year_match.group(1).strip() if year_match else (date_match.group(1).strip() if date_match else "n.d.")
        year_match_text = re.search(r"\d{4}", year_source)
        year = year_match_text.group(0) if year_match_text else year_source
        lookup[key] = {
            "author": short_author(author),
            "year": year,
        }
    return lookup


def short_author(author_field: str) -> str:
    author_field = re.sub(r"[{}]", "", author_field).strip()
    authors = [chunk.strip() for chunk in author_field.split(" and ") if chunk.strip()]
    if not authors:
        return "Unknown"
    first = authors[0]
    family_match = re.search(r"family\s*=\s*([^,]+)", first)
    if family_match:
        surname = family_match.group(1).strip()
    elif "," in first:
        surname = first.split(",", 1)[0].strip()
    else:
        surname = first.split()[-1].strip()
    return f"{surname} et al." if len(authors) > 1 else surname


def format_citation(keys: str, style: str, lookup: dict[str, dict[str, str]]) -> str:
    parts = []
    for key in [piece.strip() for piece in keys.split(",") if piece.strip()]:
        meta = lookup.get(key, {"author": key, "year": ""})
        author = meta["author"]
        year = meta["year"]
        if style == "year":
            parts.append(year or key)
        elif style == "text":
            parts.append(f"{author} ({year})" if year else author)
        else:
            parts.append(f"{author}, {year}" if year else author)
    if style == "paren":
        return f"({'; '.join(parts)})" if parts else ""
    return "; ".join(parts)


def replace_figure_like_environment(text: str, env_name: str, prefix: str) -> str:
    begin_token = f"\\begin{{{env_name}}}"
    end_token = f"\\end{{{env_name}}}"
    out: list[str] = []
    cursor = 0
    while True:
        start = text.find(begin_token, cursor)
        if start == -1:
            out.append(text[cursor:])
            break
        out.append(text[cursor:start])
        end = text.find(end_token, start)
        if end == -1:
            out.append(text[start:])
            break
        fragment = text[start + len(begin_token) : end]
        caption = extract_caption(fragment)
        if caption:
            out.append(f"\n{prefix}: {caption}\n")
        else:
            out.append("\n")
        cursor = end + len(end_token)
    return "".join(out)


def strip_environment(text: str, env_name: str) -> str:
    begin_token = f"\\begin{{{env_name}}}"
    end_token = f"\\end{{{env_name}}}"
    out: list[str] = []
    cursor = 0
    while True:
        start = text.find(begin_token, cursor)
        if start == -1:
            out.append(text[cursor:])
            break
        out.append(text[cursor:start])
        end = text.find(end_token, start)
        if end == -1:
            break
        out.append("\n")
        cursor = end + len(end_token)
    return "".join(out)


def extract_caption(fragment: str) -> str | None:
    for command in ("caption", "captionof"):
        marker = f"\\{command}"
        start = fragment.find(marker)
        if start == -1:
            continue
        idx = start + len(marker)
        idx = skip_whitespace(fragment, idx)
        try:
            if command == "captionof":
                _, idx = read_group(fragment, idx)
                idx = skip_whitespace(fragment, idx)
            caption_tex, _ = read_group(fragment, idx)
        except ValueError:
            continue
        return cleanup_tex_fragment(caption_tex, {})
    return None


def rewrite_tex(text: str, bib_lookup: dict[str, dict[str, str]]) -> str:
    out: list[str] = []
    i = 0

    while i < len(text):
        if text.startswith("\\\\", i):
            out.append("\n")
            i += 2
            continue

        char = text[i]
        if char != "\\":
            if char == "~":
                out.append(" ")
            else:
                out.append(char)
            i += 1
            continue

        name, cursor = read_command_name(text, i)
        if not name:
            out.append("\\")
            i += 1
            continue
        if cursor < len(text) and text[cursor] == "*":
            cursor += 1

        if name in {"ea", "ex", "z", "smallskip", "medskip", "bigskip", "noindent"}:
            out.append("\n")
            i = cursor
            continue

        if name == "item":
            out.append("\n- ")
            i = cursor
            continue

        if name in {"begin", "end"}:
            cursor = skip_whitespace(text, cursor)
            if cursor < len(text) and text[cursor] == "{":
                env_name, cursor = read_group(text, cursor)
                if env_name in {"itemize", "enumerate", "description", "quote", "quotation", "center"}:
                    if name == "begin":
                        cursor = skip_optional_arguments(text, cursor)
                    out.append("\n")
                    i = cursor
                    continue
            out.append(f"\\{name}")
            i = cursor
            continue

        if name in STRIP_ONE_ARG:
            cursor = skip_whitespace(text, cursor)
            if cursor < len(text) and text[cursor] == "{":
                _, cursor = read_group(text, cursor)
                i = cursor
                continue
            out.append(f"\\{name}")
            i = cursor
            continue

        if name in TEXT_CITE_COMMANDS | PAREN_CITE_COMMANDS | {"citeyear"}:
            cursor = skip_optional_arguments(text, cursor)
            cursor = skip_whitespace(text, cursor)
            if cursor < len(text) and text[cursor] == "{":
                keys, cursor = read_group(text, cursor)
                if name == "citeyear":
                    out.append(format_citation(keys, "year", bib_lookup))
                elif name in TEXT_CITE_COMMANDS:
                    out.append(format_citation(keys, "text", bib_lookup))
                else:
                    out.append(format_citation(keys, "paren", bib_lookup))
                i = cursor
                continue
            out.append(f"\\{name}")
            i = cursor
            continue

        if name in UNWRAP_ONE_ARG:
            cursor = skip_whitespace(text, cursor)
            if cursor < len(text) and text[cursor] == "{":
                arg, cursor = read_group(text, cursor)
                out.append(rewrite_tex(arg, bib_lookup))
                i = cursor
                continue
            out.append(f"\\{name}")
            i = cursor
            continue

        if name == "footnote":
            cursor = skip_whitespace(text, cursor)
            if cursor < len(text) and text[cursor] == "{":
                arg, cursor = read_group(text, cursor)
                cleaned = rewrite_tex(arg, bib_lookup).strip()
                if cleaned:
                    out.append(f" ({cleaned})")
                i = cursor
                continue
            out.append("\\footnote")
            i = cursor
            continue

        if name == "href":
            cursor = skip_whitespace(text, cursor)
            if cursor < len(text) and text[cursor] == "{":
                _, cursor = read_group(text, cursor)
                cursor = skip_whitespace(text, cursor)
                if cursor < len(text) and text[cursor] == "{":
                    arg, cursor = read_group(text, cursor)
                    out.append(rewrite_tex(arg, bib_lookup))
                    i = cursor
                    continue
            out.append("\\href")
            i = cursor
            continue

        if name == "url":
            cursor = skip_whitespace(text, cursor)
            if cursor < len(text) and text[cursor] == "{":
                arg, cursor = read_group(text, cursor)
                out.append(arg)
                i = cursor
                continue
            out.append("\\url")
            i = cursor
            continue

        if name == "gap":
            out.append("[gap]")
            i = cursor
            continue

        if name in TEXT_MACRO_REPLACEMENTS:
            out.append(TEXT_MACRO_REPLACEMENTS[name])
            i = cursor
            continue

        out.append(f"\\{name}")
        i = cursor

    return "".join(out)


def skip_optional_arguments(text: str, idx: int) -> int:
    cursor = skip_whitespace(text, idx)
    while cursor < len(text) and text[cursor] == "[":
        _, cursor = read_group(text, cursor, "[", "]")
        cursor = skip_whitespace(text, cursor)
    return cursor


def run_detex(fragment: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".tex", encoding="utf-8") as handle:
        handle.write(fragment)
        handle.flush()
        result = subprocess.run(
            ["detex", handle.name],
            check=True,
            capture_output=True,
            text=True,
        )
    return result.stdout


def cleanup_tex_fragment(text: str, bib_lookup: dict[str, dict[str, str]]) -> str:
    text = strip_line_comments(text)
    text = replace_figure_like_environment(text, "figure", "Figure")
    text = replace_figure_like_environment(text, "table", "Table")
    for env_name in ("tikzpicture", "forest", "tabular", "longtable"):
        text = strip_environment(text, env_name)
    text = rewrite_tex(text, bib_lookup)
    text = run_detex(text)
    text = text.replace("``", '"').replace("''", '"')
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" ?([,.;:?!])", r"\1", text)
    return text.strip()


def clean_heading_title(title_tex: str, bib_lookup: dict[str, dict[str, str]]) -> str:
    cleaned = cleanup_tex_fragment(title_tex, bib_lookup)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def find_next_event(text: str, start: int, bib_lookup: dict[str, dict[str, str]]) -> Event | None:
    idx = start
    while True:
        idx = text.find("\\", idx)
        if idx == -1:
            return None

        if text.startswith("\\begin{tblsframedsymbol}", idx):
            cursor = idx + len("\\begin")
            _, cursor = read_group(text, cursor)
            cursor = skip_whitespace(text, cursor)
            title_tex, cursor = read_group(text, cursor)
            cursor = skip_whitespace(text, cursor)
            _, cursor = read_group(text, cursor)
            end_token = "\\end{tblsframedsymbol}"
            body_end = text.find(end_token, cursor)
            if body_end == -1:
                idx += 1
                continue
            title = clean_heading_title(title_tex, bib_lookup)
            body = text[cursor:body_end]
            return Event(
                kind="box",
                level=None,
                title=title,
                start=idx,
                end=body_end + len(end_token),
                body=body,
            )

        for command in ("subsubsection", "subsection", "section", "chapter", "addchap"):
            marker = f"\\{command}"
            if not text.startswith(marker, idx):
                continue
            cursor = idx + len(marker)
            if cursor < len(text) and text[cursor] == "*":
                cursor += 1
            cursor = skip_whitespace(text, cursor)
            if cursor >= len(text) or text[cursor] != "{":
                continue
            title_tex, cursor = read_group(text, cursor)
            title = clean_heading_title(title_tex, bib_lookup)
            return Event(
                kind="heading",
                level="chapter" if command == "addchap" else command,
                title=title,
                start=idx,
                end=cursor,
            )
        idx += 1


def split_into_blocks(path: Path, bib_lookup: dict[str, dict[str, str]]) -> list[Block]:
    text = strip_line_comments(path.read_text(encoding="utf-8"))
    blocks: list[Block] = []
    context = {
        "chapter": None,
        "section": None,
        "subsection": None,
        "subsubsection": None,
    }
    current_type = "frontmatter"
    current_start = 0
    cursor = 0

    while True:
        event = find_next_event(text, cursor, bib_lookup)
        if event is None:
            remainder = text[current_start:]
            block = build_block(path, current_type, context, None, remainder)
            if block:
                blocks.append(block)
            break

        before = text[current_start:event.start]
        block = build_block(path, current_type, context, None, before)
        if block:
            blocks.append(block)

        if event.kind == "box":
            box_block = build_block(path, "box", context, event.title, event.body or "")
            if box_block:
                blocks.append(box_block)
            current_start = event.end
            cursor = event.end
            continue

        assert event.level is not None
        if event.level == "chapter":
            context["chapter"] = event.title
            context["section"] = None
            context["subsection"] = None
            context["subsubsection"] = None
        elif event.level == "section":
            context["section"] = event.title
            context["subsection"] = None
            context["subsubsection"] = None
        elif event.level == "subsection":
            context["subsection"] = event.title
            context["subsubsection"] = None
        elif event.level == "subsubsection":
            context["subsubsection"] = event.title

        current_type = event.level
        current_start = event.end
        cursor = event.end

    return blocks


def build_block(
    path: Path,
    block_type: str,
    context: dict[str, str | None],
    box_title: str | None,
    raw_tex: str,
) -> Block | None:
    if not raw_tex or not raw_tex.strip():
        return None
    return Block(
        include_path=str(path.relative_to(path.parent.parent)),
        block_type=block_type,
        chapter_title=context["chapter"],
        section_title=context["section"],
        subsection_title=context["subsection"],
        subsubsection_title=context["subsubsection"],
        box_title=box_title,
        raw_tex=raw_tex,
    )


def labels_in_tex(raw_tex: str) -> list[str]:
    return re.findall(r"\\label\{([^}]+)\}", raw_tex)


def block_anchor(block: Block) -> str:
    parts = [
        block.chapter_title,
        block.section_title,
        block.subsection_title,
        block.subsubsection_title,
    ]
    parts = [part for part in parts if part]
    if block.block_type == "box" and block.box_title:
        parts.append(f"Box: {block.box_title}")
    return " > ".join(parts) if parts else block.include_path


def split_clean_text(text: str, target_words: int = 340, max_words: int = 520) -> list[str]:
    paragraphs = [para.strip() for para in re.split(r"\n\s*\n", text) if para.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    current: list[str] = []
    current_words = 0

    def flush_current() -> None:
        nonlocal current, current_words
        if current:
            chunks.append("\n\n".join(current).strip())
            current = []
            current_words = 0

    for para in paragraphs:
        para_words = word_count(para)
        if para_words > max_words:
            flush_current()
            sentences = sentence_splits(para)
            sentence_bucket: list[str] = []
            sentence_words = 0
            for sentence in sentences:
                sent_words = word_count(sentence)
                if sentence_bucket and sentence_words + sent_words > max_words:
                    chunks.append(" ".join(sentence_bucket).strip())
                    sentence_bucket = [sentence]
                    sentence_words = sent_words
                else:
                    sentence_bucket.append(sentence)
                    sentence_words += sent_words
            if sentence_bucket:
                chunks.append(" ".join(sentence_bucket).strip())
            continue

        if current and current_words >= target_words and current_words + para_words > max_words:
            flush_current()

        current.append(para)
        current_words += para_words

    flush_current()
    return chunks


def read_main_includes(main_tex: Path) -> list[Path]:
    text = strip_line_comments(main_tex.read_text(encoding="utf-8"))
    includes = []
    for match in re.finditer(r"\\include\{([^}]+)\}", text):
        include = match.group(1).strip()
        candidate = (main_tex.parent / include).with_suffix(".tex")
        includes.append(candidate)
    return includes


def export(main_tex: Path, output_dir: Path) -> dict[str, object]:
    bib_lookup = load_bib_lookup(main_tex.parent / "localbibliography.bib")
    include_paths = read_main_includes(main_tex)
    output_dir.mkdir(parents=True, exist_ok=True)

    chunks: list[dict[str, object]] = []
    chapter_stats: list[dict[str, object]] = []
    toc: list[dict[str, object]] = []
    chunk_counter = 0

    for include_path in include_paths:
        if not include_path.exists():
            continue
        blocks = split_into_blocks(include_path, bib_lookup)
        chapter_clean_words = 0
        chapter_clean_chars = 0
        chapter_title = None

        for block in blocks:
            clean_text = cleanup_tex_fragment(block.raw_tex, bib_lookup)
            if not clean_text:
                continue

            if block.chapter_title and chapter_title is None:
                chapter_title = block.chapter_title

            labels = labels_in_tex(block.raw_tex)
            anchor = block_anchor(block)
            packed_chunks = split_clean_text(clean_text)
            if not packed_chunks:
                continue

            chapter_clean_words += sum(word_count(piece) for piece in packed_chunks)
            chapter_clean_chars += sum(len(piece) for piece in packed_chunks)

            if block.block_type in {"chapter", "section", "subsection", "subsubsection", "box"}:
                toc.append(
                    {
                        "include_path": block.include_path,
                        "block_type": block.block_type,
                        "title": block.box_title if block.block_type == "box" else anchor.split(" > ")[-1],
                        "anchor": anchor,
                        "labels": labels,
                    }
                )

            for part_index, piece in enumerate(packed_chunks, start=1):
                chunk_counter += 1
                chunks.append(
                    {
                        "chunk_id": f"{BOOK_SLUG}-{chunk_counter:04d}",
                        "source_path": block.include_path,
                        "block_type": block.block_type,
                        "chapter_title": block.chapter_title,
                        "section_title": block.section_title,
                        "subsection_title": block.subsection_title,
                        "subsubsection_title": block.subsubsection_title,
                        "box_title": block.box_title,
                        "anchor": anchor,
                        "labels": labels,
                        "part_index": part_index,
                        "part_count": len(packed_chunks),
                        "word_count": word_count(piece),
                        "char_count": len(piece),
                        "text": piece,
                    }
                )

        if chapter_title:
            chapter_stats.append(
                {
                    "chapter_title": chapter_title,
                    "source_path": str(include_path.relative_to(main_tex.parent)),
                    "clean_word_count": chapter_clean_words,
                    "clean_char_count": chapter_clean_chars,
                    "minutes_at_155_wpm": round(chapter_clean_words / 155, 1),
                }
            )

    manifest = {
        "book_title": BOOK_TITLE,
        "book_author": BOOK_AUTHOR,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "main_tex": str(main_tex.relative_to(main_tex.parent)),
        "source_files": [str(path.relative_to(main_tex.parent)) for path in include_paths if path.exists()],
        "chunk_count": len(chunks),
        "chapter_count": len(chapter_stats),
        "total_clean_word_count": sum(item["clean_word_count"] for item in chapter_stats),
        "total_clean_char_count": sum(item["clean_char_count"] for item in chapter_stats),
        "estimated_audio_hours_at_155_wpm": round(
            sum(item["clean_word_count"] for item in chapter_stats) / 155 / 60,
            2,
        ),
    }

    (output_dir / "book_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "table_of_contents.json").write_text(
        json.dumps(toc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "chapter_stats.json").write_text(
        json.dumps(chapter_stats, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with (output_dir / "book_chunks.jsonl").open("w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--main-tex",
        default="main.tex",
        help="Path to the book's main TeX file.",
    )
    parser.add_argument(
        "--output-dir",
        default="ai-companion/export",
        help="Directory for the generated export files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    main_tex = Path(args.main_tex).resolve()
    output_dir = Path(args.output_dir).resolve()
    manifest = export(main_tex, output_dir)
    print(
        f"Exported {manifest['chunk_count']} chunks from {manifest['chapter_count']} chapters "
        f"to {output_dir}"
    )


if __name__ == "__main__":
    main()
