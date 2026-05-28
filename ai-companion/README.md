# AI Companion

This directory holds the first-pass assets for an interactive AI version of *Language landscapes*.

The goal is not to fine-tune a model on the book. The goal is to give a retrieval-based assistant clean, citeable chunks with enough structure to answer questions by chapter and section.

## What gets generated

Run:

```bash
python3 scripts/export_ai_companion.py
```

This writes to `ai-companion/export/`:

- `book_manifest.json`: corpus-level metadata and rough size estimates
- `table_of_contents.json`: heading-level navigation metadata
- `chapter_stats.json`: clean word counts and rough audiobook durations
- `book_chunks.jsonl`: retrieval-ready chunk export

Each JSONL row includes:

- `chunk_id`
- `source_path`
- `block_type`
- `chapter_title`
- `section_title`
- `subsection_title`
- `subsubsection_title`
- `box_title`
- `anchor`
- `labels`
- `part_index`
- `part_count`
- `word_count`
- `char_count`
- `text`

## Intended use

Use the chunks in a standard RAG stack:

1. Index `book_chunks.jsonl`.
2. Retrieve by semantic similarity plus chapter/section filters.
3. Feed the retrieved chunks to the assistant with the prompt in [system-prompt.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/system-prompt.md).
4. Require answers to cite the book by `anchor` and, when helpful, `chunk_id`.

## Local companion surface

There is now a built-in local companion:

```bash
python3 scripts/run_ai_companion_chat.py serve
```

This serves a browser UI on `http://127.0.0.1:8765`.

The local app now includes:

- a landing page with example prompts
- `Read` mode with chapter browsing and a scoped guide drawer
- `Ask` mode with local thread history in the browser
- `Contents`, `Glossary`, and `Index` browse surfaces
- a source inspector modal for retrieved passages

The app always retrieves locally from `ai-companion/export/book_chunks.jsonl`.

If you want model-generated answers, set `OPENAI_API_KEY` before starting the server. If no key is set, the UI still works in retrieval-only mode and returns the most relevant passages with citations.

Quick CLI check:

```bash
python3 scripts/run_ai_companion_chat.py ask "What distinction does the book make between categories and functions?"
```

The web assets live in `ai-companion/web/`, and the server exposes structured endpoints for the UI:

- `/api/config`
- `/api/read?chapter_id=...`
- `/api/glossary`
- `/api/index`
- `/api/source?chunk_id=...`
- `/api/chat`

## Design choices

- Chunking is based on the book's own structure first, then split into retrieval-sized parts.
- Figure and table bodies are stripped, but captions are preserved where possible.
- Bibliographic citations are converted to short author-year text when the local `.bib` file can supply it.
- Indexing commands and cross-reference labels are removed from the answerable text, but raw labels remain in metadata.

## Known limitations

- Visual material is only partially represented. A user asking about a tree, chart, or diagram may need the PDF.
- Example numbering is flattened. The linguistic content remains, but not the exact textbook layout.
- Audio-unfriendly sections still export fine for retrieval, but they should be adapted before narration.

## Suggested product surface

For this manuscript, the AI version should behave like a teaching companion:

- answer questions about the book
- explain distinctions in plain language
- compare nearby concepts without inventing external doctrine
- point readers to the right chapter or section
- admit when a visual example or table is necessary
