# Claude Design Handoff

This package is for `claude.ai/design`.

It is meant to produce a polished mock-up for a public-facing AI companion to *Language landscapes* by Brett Reynolds.

The mock-up should be treated as a design exploration for a later Claude Artifacts implementation, not as a generic SaaS chatbot.

## What to give Claude Design

Upload this whole folder.

Also useful, but optional:

- [main.pdf](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/main.pdf)
- [book_chunks.jsonl](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/export/book_chunks.jsonl)

Then paste the prompt from [claude-design-prompt.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/claude-design-prompt.md).

## Included files

- [claude-design-prompt.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/claude-design-prompt.md): paste-ready design prompt
- [product-brief.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/product-brief.md): product, audience, goals, scope
- [ux-spec.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/ux-spec.md): screens, flows, component behavior, sample interactions
- [technical-guardrails.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/technical-guardrails.md): constraints to keep the mock-up implementable in Claude Artifacts
- [copy-deck.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/copy-deck.md): sample product copy and UI text
- [current-surface.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/current-surface.md): what the current local prototype does and what the redesign should improve
- [sample-interactions.md](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/sample-interactions.md): realistic example questions, answer shapes, and source cards
- [reference/book_manifest.json](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/reference/book_manifest.json): current corpus metadata
- [reference/chapter_stats.json](/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes/ai-companion/design-handoff/reference/chapter_stats.json): chapter-level size and duration estimates

## What a good mock-up should solve

- make the product feel like a serious reading companion, not a generic AI wrapper
- help a first-time visitor understand what kinds of questions are worth asking
- surface citations and source passages as first-class UI, not an afterthought
- make chapter browsing and question asking feel complementary
- look strong on desktop and mobile

## What to avoid

- generic productivity-app dashboard patterns
- dark purple AI branding clichés
- fake features that imply a backend we will not have in the first public version
- speculative collaboration or account features
- visually burying the sources rail or chapter browser
