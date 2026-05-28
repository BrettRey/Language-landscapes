# IA Spec

## Product framing

This is a book companion with two primary modes:

- `Read`
- `Ask`

AI is subordinate to the book.

The interface should privilege:

- orientation
- source trust
- chapter and section structure
- movement between answer and source

It should not privilege:

- generic chat theater
- autonomous AI behavior
- metaphorical terrain as literal navigation

## Primary navigation

Top-level navigation:

- `Read`
- `Ask`
- `Contents`
- `Index`
- `Glossary`

Contextual utility:

- `Sources`
- `Bookmarks`
- `Recent`

`Sources` should usually be a panel or drawer, not a top-level product mode.

## Mode definitions

### Read

Purpose:

- read the book in a calm, book-first interface
- optionally invoke AI to explain, define, summarize, or locate related passages
- preserve immersion

Characteristics:

- chapter and section navigation
- reading progress or chapter context
- AI sidecar kept collapsed or secondary by default
- source links available but not dominant

### Ask

Purpose:

- ask natural-language questions about the book
- inspect grounded answers and passages
- revisit previous threads when signed in

Characteristics:

- question box is primary
- thread list appears here, not globally
- answers must cite the book
- source cards and source inspector are always near at hand

## Navigation logic

### Entry point

Default landing should offer two clear moves:

- `Start reading`
- `Ask the book`

The user should not be forced to choose immediately, but the choice should structure the experience.

### Read to Ask transition

From `Read`, the user can:

- ask about the current section
- ask about the whole chapter
- ask about the whole book

This should open an ask surface already scoped to the relevant context.

### Ask to Read transition

From `Ask`, the user can:

- open cited source passage
- open section in reading view
- open chapter

This should feel like moving from answer back into the book.

## Recommended object model

Main content objects:

- chapter
- section
- glossary term
- source passage
- ask thread
- citation

The artifact should treat these as first-class surfaces rather than flattening everything into chat messages.

## Desktop IA

### Read

- top bar with `Read | Ask | Contents | Index | Glossary`
- central reading pane
- optional chapter rail or chapter drawer
- collapsible bottom or right AI sidecar

### Ask

- left rail for threads
- central thread pane
- right rail for sources on wide screens

### Index / Glossary

- full-page browse surfaces
- allow jump into reading or ask flow

## Mobile IA

### Read

- bottom or top segmented control for `Read` and `Ask`
- content-first view
- sources and AI in bottom sheet or slide-up drawer

### Ask

- thread list as drawer or separate list screen
- conversation on main screen
- sources in bottom sheet

## IA principle

The main relationship is:

`Read` for immersion.

`Ask` for intervention.

The product should make switching between those two states feel effortless and reversible.
