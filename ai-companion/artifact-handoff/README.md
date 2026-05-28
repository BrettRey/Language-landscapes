# Artifact Handoff

This package translates the Claude Design wireframes into an implementable Claude Artifact plan.

It assumes:

- a published Claude Artifact
- local embedded corpus from `book_chunks.jsonl`
- no traditional backend
- AI synthesis through Claude's artifact capabilities
- optional persistent personal storage for signed-in users

## Included files

- [ia-spec.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/artifact-handoff/ia-spec.md): navigation, modes, information architecture
- [screen-spec.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/artifact-handoff/screen-spec.md): screen-by-screen behavior for desktop and mobile
- [storage-model.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/artifact-handoff/storage-model.md): what to persist, for whom, and under what conditions
- [wireframe-reconciliation.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/artifact-handoff/wireframe-reconciliation.md): which Design concepts to keep, change, or drop
- [artifact-build-prompt.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/artifact-handoff/artifact-build-prompt.md): prompt starter for the future Claude Artifact build
- [reference/book_manifest.json](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/artifact-handoff/reference/book_manifest.json): corpus metadata
- [reference/chapter_stats.json](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/artifact-handoff/reference/chapter_stats.json): chapter sizes and duration estimates

## Core decision

The product should have a primary switch between:

- `Read`
- `Ask`

This is the main structural correction to the wireframes.

`Read` is the default book-first mode.

`Ask` is the conversational, thread-based mode.

Everything else should behave as supporting infrastructure:

- `Contents`
- `Index`
- `Glossary`
- `Sources`

## Why this structure

- It fits the book better than a map-led home screen.
- It fits Claude Artifacts better than a full app-shell with many parallel product modes.
- It keeps the quiet reading experience distinct from active questioning.
- It makes thread persistence a feature of `Ask`, not a burden on the whole app.

## Recommended v1 center of gravity

The most important flows are:

1. Open the companion and start reading.
2. Ask a question while reading and inspect the cited passages.
3. Start in `Ask`, get a grounded answer, and open the source or chapter.
4. Browse through contents, index, and glossary when the user does not know what to ask.

## Not recommended for v1

- topographic map navigation
- graph visualization as primary discovery
- large workspace or note-taking systems
- collaborative or shared conversation features
- export-heavy scholar tooling

## Immediate next use

When the mock-up stabilizes, use [artifact-build-prompt.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/artifact-handoff/artifact-build-prompt.md) plus the current export files to start the first Artifact implementation.
