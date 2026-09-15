# Chapters 3 and 2 audio: sizing and budget check
<!-- SUMMARY: Ch2 script drafted, 43,698 credits exact; Brett chose a staged run, 33,896 now through MO8 and 9,802 after 1 Oct · status: ch2 awaiting script review before generation · updated: 2026-09-14 -->

14 September 2026. No credits spent. No ElevenLabs generation requested.

## Live balance, verified 2026-09-14

Read from the ElevenLabs account after reconnecting the Chrome extension.

| Field | Value |
|---|---|
| Remaining | 44,184 credits |
| Used this cycle | 86,816 of 131,000 |
| Plan | Creator, 22 USD/month, 121k credits/month |
| Renews | 1 October 2026 |

Remaining matches the 7 September post-Chapter-1 figure exactly, so nothing
has been charged since. That also resolves the open question in the video
pilot record: the generated test MP4 did not draw credits after that
observation. `actual_video_credits_charged` can be treated as either zero or
already inside the 7 September number.

### Extension blocker, resolved

Chrome had run since 10 September and was holding extension build 1.0.91 in
memory while 1.0.93 sat on disk, with its native-messaging bridge pinned to a
Claude Code binary three versions stale. A full Chrome quit plus `/chrome`
reconnect fixed it. Worth remembering before the next chapter run, since the
same failure blocked production on 7 September.

## Sizing, grounded in Chapter 1 actuals

Metrics from the current TeX, with Chapter 1's measured outcome as the anchor.

| | Ch 1 (done) | Ch 3 | Ch 2 |
|---|---:|---:|---:|
| Clean-export characters | 41,225 | 41,327 | 39,890 |
| `\item` example entries | 116 | 134 | 45 |
| Tabulars | 2 | 3 | 0 |
| Forest trees | 0 | 1 | 0 |
| Footnotes | 18 | 6 | 3 |
| Mention-marked forms | 86 | 192 | 38 |

Chapter 1's approved script came to 38,069 new readable characters on top of
roughly 10,000 characters of reused pilot audio, so its full narration was
about 48,000 characters from a 41,225-character base: an adaptation ratio
near 1.16. Neither Chapter 3 nor Chapter 2 has reusable prior audio.

Chapter 3 is the most adaptation-heavy of the three: more examples than
Chapter 1, three tables, a syntax tree, and more than double Chapter 1's
mention-marked forms, each of which needs "the word X" treatment in speech.
Chapter 2 is the lightest: prose-heavy, no tables, few examples.

| Chapter | First-take estimate | 15% repair reserve | Total |
|---|---:|---:|---:|
| Ch 3 | 50,000–54,000 | ~7,500 | 57,500–61,500 |
| Ch 2 | 42,000–46,000 | ~6,500 | 48,500–52,500 |
| Both | | | 106,000–114,000 |

These are estimates from the ratio above, not counts of an approved script.
Exact counts require the adapted script, which is the next deliverable.

## Chapter 2: exact, no longer an estimate

The Chapter 2 script package is drafted at
`supplements/audio/chapter-02-2026-09/chapter-02-scripts.md`, 51 inputs, and
`scripts/voice/prepare_chapter02.py` writes the exact inputs and manifest. No
credits have been spent and no generation has been requested.

| | Credits |
|---|---:|
| First takes, exact submitted characters | 43,698 |
| 15% repair reserve | 6,555 |
| Total wanted | 50,253 |
| Verified balance | 44,184 |
| Shortfall | 6,069 |

First takes alone fit, with 486 credits left over. That is a 1% repair reserve,
and the pilot needed four repairs on a two-minute calibration, so running the
whole chapter now means any defect waits until 1 October.

Section subtotals, for choosing a stopping point:

| Section | Characters | Cumulative | Cumulative +15% |
|---|---:|---:|---:|
| Opening and standards | 8,774 | 8,774 | 10,090 |
| Standard Englishes | 3,779 | 12,553 | 14,436 |
| Questioning grammaticality | 15,186 | 27,739 | 31,900 |
| A model of grammaticality | 6,157 | 33,896 | 38,980 |
| Normativity and conclusion | 5,455 | 39,351 | 45,254 |
| Exercises and answers | 4,347 | 43,698 | 50,253 |

The largest run that keeps a full 15% reserve is 38,420 characters, which
reaches the Audience segment, 86% of the chapter.

### Staged run, chosen 2026-09-14

Brett chose to stop after the model section.

| | Run 1, now | Run 2, after 1 Oct |
|---|---:|---:|
| Inputs | 41 (H01 through MO8) | 10 (N01 through Q03) |
| First takes | 33,896 | 9,802 |
| 15% reserve | 5,085 | |
| Ceiling | 39,000 | |
| Balance left untouched | 5,203 | |

Run 1 ends on a section boundary, after "A model of grammaticality". Run 2
covers normativity, audience, the conclusion, and the three exercise segments.

**Generation is not yet authorized.** Two things stand before it, below.

### Chapter 3, still estimated

Chapter 3 has not been drafted, so its 57,500 to 61,500 figure remains an
estimate from the Chapter 1 ratio. Chapter 2 came in at 43,698 against a
42,000 to 46,000 estimate, which is inside the predicted band, so the Chapter 3
estimate is worth about as much. It still exceeds the current balance either way.

## Before run 1 can be generated

**The script has not been read.** Chapter 1 went script review, then budget
approval, then generation, and Brett accepted three adaptation changes at the
review stage. Chapter 2's 41 run-1 inputs have had no such pass. Generating
33,896 credits of unreviewed narration would spend 77% of the balance on
wording that may still change, and a wording change after synthesis costs the
credits again.

**Two of the three open questions sit inside run 1.** MO2 and SH01 are both in
scope; only the TESL question falls in run 2 and can wait.

## Open questions in the Chapter 2 script

Three, all flagged in the review copy and the manifest.

- **The Japanese passage (MO2).** Nishimura's code-switching example is read
  aloud with each gloss following. Long vowels are respelled to stop an English
  spelling-pronunciation. Whether to read it at all, or to describe it instead,
  is Brett's call.
- **The Judges passage (SH01).** The book quotes the New International Version,
  which is licensed rather than public domain. Print permission does not
  automatically cover an audio recording. Confirm the audio right before
  publishing that segment, or substitute a public-domain translation.
- **TESL.** Spoken as a word or spelled out.

## Next

Chapter 2 needs a read-through and a budget choice before anything is
generated. Chapter 3's script package can start whenever.
