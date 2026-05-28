# Audiobook Pilot

Assumption: you control the audio rights and can authorize synthetic narration in your own voice.

## Recommendation

Start with a pilot, not the full book.

The current export is about 121k clean words, which is about 13.0 hours at 155 words per minute. That is large enough that mistakes in pronunciation, pacing, and visual adaptation will compound if you start with the whole book.

## Best first pilot

Recommended pilot set:

- `preface.tex`: about 5.6 minutes
- `16 pragmatics.tex`: about 32.0 minutes
- `17 conversation.tex`: about 45.2 minutes

Why these:

- They are prose-heavy.
- They have no figure-heavy dependency.
- They are pedagogically central.
- They give you enough duration to judge fatigue, pacing, and synthetic-voice stability.

This pilot is about 82.8 minutes total.

## Second pilot option

If you want a more book-opening sample rather than a mid-book sample:

- `preface.tex`
- `01 key concepts.tex`

This is about 50.4 minutes total and gives a strong sense of the book's authorial voice, but Chapter 1 has more structure-sensitive material to adapt.

## Chapters to defer

Defer these until the pipeline is stable:

- `06 trees.tex`
- `07 the sound system.tex`
- `09 writing system.tex`

Reason:

- They depend more heavily on symbols, diagrams, phonetic detail, or visual contrasts that need explicit audio adaptation.

## Voice-clone prep

Target recording set:

- 45 to 90 minutes of clean audio
- one speaker only
- consistent microphone and room
- the exact narration register you want for the audiobook

Do not train the voice on casual podcast audio if the target product is textbook narration.

## Production steps

1. Record a clean voice-clone training set.
2. Build a pronunciation sheet for names, technical terms, abbreviations, IPA, and symbols.
3. Adapt the chosen pilot chapters for audio.
4. Generate narration.
5. Review every minute for:
   - wrong emphasis
   - bad sentence boundary decisions
   - broken list rhythm
   - symbol handling
   - references to unseen figures
6. Revise the text, not just the audio settings.

## Text adaptation rules

Before narration, rewrite:

- `see Figure X` into a spoken description or a PDF reference
- symbol-only contrasts into explicit spoken forms
- dense bullet lists into audio-friendly phrasing when needed
- long parenthetical citations if they interrupt listenability

## Success criteria for the pilot

The pilot is good enough to scale only if:

- the cloned voice sounds recognizably like you
- technical terms are handled consistently
- listeners can follow the material without seeing the page
- the edits required per chapter are predictable rather than ad hoc
