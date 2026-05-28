# UX Spec

## Primary screens

### 1. Landing / arrival

Purpose:

- explain what the companion is
- show how to use it
- offer strong example prompts
- let users browse chapters immediately

Content blocks:

- title and one-sentence value proposition
- short explanation that answers come from the book and cite the source
- 4 to 6 example prompts
- chapter index or thematic browse grid
- preview of what a cited answer looks like

### 2. Main companion screen

Purpose:

- ask questions
- read the answer
- inspect citations and source snippets

Suggested layout:

- central conversation pane
- right-side source rail on desktop
- collapsible sources drawer on mobile
- compact chapter/browse rail or top-level browse drawer

### 3. Chapter browsing

Purpose:

- help users who do not yet know what to ask
- make the book’s architecture legible

Suggested elements:

- chapter list
- chapter duration / size hint
- short chapter description
- jump from chapter to suggested questions

### 4. No-match or weak-match state

Purpose:

- preserve trust when retrieval is weak

Behavior:

- say the companion could not find a strong answer in the book
- offer related chapters
- offer narrower follow-up suggestions

## Key interface behaviors

### Asking a question

The experience should support prompt styles like:

- explain X
- compare X and Y
- where does the book discuss X
- quiz me on X

### Answer presentation

Each answer should visibly include:

- answer text
- citation line by chapter/section
- optional chunk id or “source passage” affordance

### Source inspection

Source cards should show:

- chapter and section path
- short excerpt
- confidence or relevance hint if helpful
- affordance to expand full passage

### Suggested prompts

Suggested prompts should be visible in at least two places:

- landing screen
- after an answer, as next-step questions

## Sample questions

- What distinction does the book make between categories and functions?
- Where does it discuss Standard English?
- Explain grammaticality in plain language.
- Compare pragmatics and conversation.
- Quiz me on negation.

## Sample content hierarchy

### Navigation labels

- Ask
- Browse chapters
- Explore topics
- Sources

### Example chapter groupings

- Foundations
- Sound and writing
- Structure
- Meaning and use
- Discourse and interaction

## Mobile guidance

- keep the ask box prominent
- move the sources rail into a bottom sheet or drawer
- make chapter browsing reachable in one tap
- ensure citations remain visible without needing to open a second screen

## Visual direction suggestions

Direction to explore:

- paper, marginalia, map, and notebook cues
- subtle cartographic or annotation motifs
- a palette that feels warm, grounded, and bookish
- typography with more character than standard SaaS sans-serifs

Avoid:

- harsh neon accents
- glassmorphism-heavy dashboards
- all-dark presentation
- decorative “AI magic” iconography
