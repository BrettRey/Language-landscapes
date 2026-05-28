# Screen Spec

## 1. Landing

Purpose:

- explain what the companion is
- let the user choose `Read` or `Ask`
- show that answers are grounded in the book

Required elements:

- title
- short trust statement
- primary actions:
  - `Start reading`
  - `Ask the book`
- 3 to 5 example prompts
- one compact citation example or source preview

Avoid:

- map-led hero
- fake metadata
- dense dashboard UI

## 2. Read Mode

Primary goal:

- quiet book-first reading

Required elements:

- chapter and section breadcrumb
- readable text column
- chapter navigation affordance
- AI sidecar toggle or `Ask about this section` affordance
- citation-linked source opening when relevant

Recommended interaction:

- default to a collapsed AI drawer
- let user scope a question to:
  - section
  - chapter
  - whole book

Desktop pattern:

- central reading pane
- bottom drawer is preferred over permanent right rail for v1

Mobile pattern:

- reading pane full width
- AI and sources open in bottom sheet

## 3. Ask Mode

Primary goal:

- thread-based questioning with visible grounding

Required elements:

- ask input
- answer area
- visible citation chips or citation line
- source cards or source rail
- thread list

Important rule:

Thread list belongs inside `Ask`.

It should not dominate `Read`.

Desktop pattern:

- left rail for threads
- central conversation pane
- right rail for source cards

Mobile pattern:

- current thread on main view
- thread list in drawer
- sources in bottom sheet

## 4. Source Inspector

Primary goal:

- verify the answer against the book

Required elements:

- chapter / section path
- source passage
- surrounding context when possible
- affordance to open in reading mode

Recommended form:

- modal on desktop
- full-screen sheet or page on mobile

## 5. Contents

Primary goal:

- browse the structure of the book

Required elements:

- chapter list
- section count or chapter size hint
- chapter description or thematic cue
- quick jump into `Read`
- quick jump into `Ask about this chapter`

Recommended behavior:

- contents is authored and structural, not AI-generated

## 6. Index

Primary goal:

- look something up directly

Required elements:

- alphabetical browse
- search box
- entry to chapter/section jump
- optional `Ask about this term`

Recommended behavior:

- treat index as a reference surface, not a chat replacement

## 7. Glossary

Primary goal:

- define terms from the book

Required elements:

- book-grounded definition
- plain-language paraphrase
- related terms
- chapters where the term appears

Recommended behavior:

- the book’s definition should lead
- the AI explanation should be secondary and clearly marked

## 8. Empty and weak-match states

### Empty state

Prompt the user with examples and scope suggestions.

### Weak match

Say the match is weak.

Offer:

- related chapters
- narrower follow-up prompts
- a path into contents or index

## 9. Thread behavior

Thread view should support:

- new thread
- rename thread
- revisit prior thread
- citation inspection within a thread
- follow-up question with scope retained when useful

The system should not pretend every interaction is one endless universal chat.

## 10. Recommended v1 screen set

Build these first:

1. landing
2. read mode with bottom AI drawer
3. ask mode with thread rail and source rail
4. source inspector
5. contents
6. glossary
7. index
