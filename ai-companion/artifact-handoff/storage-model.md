# Storage Model

## Anthropic constraints this spec assumes

- Claude Artifacts support persistent storage only when published.
- Storage can be `personal` or `shared`.
- For this project, use `personal` storage only.
- Storage is text-only.
- Current limit is 20 MB per artifact.

## Principle

Persist only what materially improves the user experience.

Do not use persistence to simulate a heavy application backend.

## Persist in personal storage

### 1. Ask threads

Store:

- thread id
- thread title
- created / updated timestamps
- lightweight message history
- citation ids or chunk ids referenced in each assistant turn
- optional scope metadata:
  - section
  - chapter
  - whole book

Reason:

- supports `AskD` style thread list
- lets users return to prior lines of inquiry

### 2. Bookmarks or pinned passages

Store:

- chunk ids
- optional user label
- timestamp

Reason:

- useful across `Read`, `Ask`, and `Sources`

### 3. Reading preferences

Store:

- last mode used
- last opened chapter / section
- whether AI drawer is open or closed
- preferred citation display mode if needed

Reason:

- small but meaningful quality-of-life improvement

## Do not persist in v1

- full reading analytics
- every scroll position in every chapter
- shared notes
- shared threads
- collaborative highlights
- anything that implies moderation or multi-user state management

## Anonymous / logged-out behavior

Assume:

- public visitors can browse the artifact
- basic non-AI interaction can work without sign-in
- advanced AI-powered interactions may require Claude sign-in

So the fallback behavior should be:

- `Read`, `Contents`, `Index`, `Glossary`: available without durable personal state
- `Ask` with persistent thread list: available only when the user is signed in

If the user is not signed in:

- allow a temporary current session
- hide or de-emphasize “past chats”
- present sign-in as the unlock for saved threads

## Thread storage shape

Recommended minimal structure per thread:

```json
{
  "id": "thread_001",
  "title": "Categories and functions",
  "updated_at": "2026-04-18T12:00:00Z",
  "scope": {
    "mode": "book",
    "chapter_title": null,
    "section_title": null
  },
  "messages": [
    {
      "role": "user",
      "text": "What distinction does the book make between categories and functions?"
    },
    {
      "role": "assistant",
      "text": "…",
      "citations": ["language-landscapes-0072", "language-landscapes-0074"]
    }
  ]
}
```

## Practical size guidance

The corpus itself is already small.

Even so, thread storage should stay concise:

- trim very long assistant outputs if needed
- store citation ids instead of copying large source passages into storage
- reconstruct source cards from the embedded corpus at render time

## Shared storage

Do not use shared storage for v1.

There is no real upside here, and it creates confusing expectations about privacy and authorship.
