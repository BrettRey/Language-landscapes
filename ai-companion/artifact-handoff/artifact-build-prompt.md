Build a Claude Artifact for *Language Landscapes AI Companion* using the attached corpus export and the Artifact handoff docs.

Use these files as the source of truth:

- `book_chunks.jsonl`
- `book_manifest.json`
- `chapter_stats.json`
- the docs in this handoff folder

Product goal:

Create a public-facing reading companion for Brett Reynolds’s *Language landscapes* that lets readers read the book, ask grounded questions, inspect cited passages, and browse the contents, glossary, and index.

Non-negotiable product structure:

- Primary modes:
  - `Read`
  - `Ask`
- Supporting surfaces:
  - `Contents`
  - `Index`
  - `Glossary`
  - `Sources`

Important product rules:

1. AI is the conversational layer over the book, not the spectacle.
2. The UI must foreground the book’s structure and citations.
3. Do not use a literal topographic or cartographic map as primary navigation.
4. `Read` is book-first and quiet.
5. `Ask` is thread-based and source-rich.
6. Source inspection must be easy.
7. Glossary and index should behave like real reference surfaces, not like chat gimmicks.

Implementation assumptions:

- No traditional backend.
- Corpus is embedded locally in the artifact.
- Retrieval happens locally against `book_chunks.jsonl`.
- Claude is used for answer synthesis and follow-up help.
- Personal persistent storage may be used for saved ask threads, bookmarks, and lightweight preferences.
- Shared storage should not be used in v1.

Required screens for v1:

1. Landing with `Start reading` and `Ask the book`
2. `Read` mode with a collapsible AI drawer
3. `Ask` mode with:
   - thread list
   - conversation pane
   - source cards or source inspector
4. `Contents`
5. `Index`
6. `Glossary`
7. Source inspector

Desktop behavior:

- In `Ask`, use a thread list on the left and sources on the right when space allows.
- In `Read`, prefer a bottom drawer for AI over a permanently dominant side panel.

Mobile behavior:

- Make `Read | Ask` easy to switch.
- Move threads and sources into drawers or sheets.
- Keep citations visible and easy to open.

Use the strongest ideas from the Design wireframes:

- Ask D for thread-based asking with inline citations
- Ask B for answer + source relationship
- Read B for reading with AI drawer
- Source A for source inspection
- Source D for index
- Source E for glossary

Do not carry over fake or invented metadata from the wireframes.

Use real book-grounded copy wherever possible.
