# Wireframe Reconciliation

This document maps the Claude Design output to the planned Claude Artifact build.

## Keep

### Ask D · Threaded with inline cites

Why:

- best expression of `Ask` as a persistent inquiry mode
- inline citations make grounding feel native to the thread
- left thread rail is compatible with personal storage

Keep conceptually:

- thread list
- pinned passages
- inline citation chips
- follow-up flow

Change:

- replace invented content with real book-grounded examples
- change “the authors” to the singular author voice
- keep thread list only in `Ask`

### Ask B · Answer + live source

Why:

- strongest trust pattern
- clear answer-to-source relationship
- ideal for desktop

Keep conceptually:

- split answer/source view
- click citation to inspect passage

Change:

- avoid pretending to show exact page facsimiles unless the artifact really has them
- source pane can use clean passage cards instead of faux scanned pages

### Read B · Docked AI drawer

Why:

- best model for `Read`
- preserves a book-first reading surface
- clear way to bridge reading and asking

Keep conceptually:

- reading is primary
- AI lives in collapsible bottom drawer
- question scope control for section / chapter / book

### Source A · Source inspector

Why:

- necessary trust layer
- works on desktop and mobile

Keep conceptually:

- focused source modal
- provenance path
- open in reading mode

### Source D · Index

Why:

- matches actual book behavior
- helps non-chat users

Keep conceptually:

- classical alphabetical browse
- direct path into reading or asking

### Source E · Glossary entry

Why:

- strong fit for the actual manuscript
- ideal for grounded definitions plus plain-language paraphrase

Keep conceptually:

- verbatim book definition
- secondary “in other words” layer
- related terms and chapter appearances

## Keep with major change

### Home A

Keep:

- bookish, restrained landing
- contents-aware structure
- ask bar visible but not dominant

Change:

- remove fake metadata
- replace “region” framing with chapter and topic framing

### Home C

Keep:

- clear ask-first entry point
- concise trust statement

Change:

- add equal-weight `Start reading` action
- make `Read | Ask` explicit

## Drop or defer

### Home B · Topographic map

Drop as primary navigation.

Reason:

- literalizes the metaphor badly
- is weaker than book-native structures
- will add complexity without real navigational gain

### Source B · Cross-reference graph

Defer.

Reason:

- visually interesting
- not necessary for v1
- adds inference burden and UI complexity

### Read C / large workspace patterns

Defer.

Reason:

- drifts toward note-taking app behavior
- not necessary for first public artifact

### Export-heavy scholar surfaces

Defer.

Reason:

- low priority compared with reading, asking, and source inspection

## Structural correction

The wireframes imply multiple parallel product centers.

The Artifact should instead have one simple structure:

- `Read`
- `Ask`

with supporting reference surfaces:

- `Contents`
- `Index`
- `Glossary`
- `Sources`

That is the main reconciliation move.
