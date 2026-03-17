# Language Landscapes -- STATUS

**Status:** Accepted with revisions (review received March 5, 2026)
**Source:** Overleaf + local copy (extracted March 12, 2026)
**Series:** TBLS (Textbooks in Language Sciences), LangSci Press
**Editor:** Stefan Muller (St.Mueller@hu-berlin.de)
**Reviewer verdict:** Positive. Publish after revisions.

### Contacts

- **Stefan Muller** -- series editor (HU Berlin)
- **Antonio Machicao Y Priemer** (mapriema@hu-berlin.de) -- series co-editor
- **Kelsey Neely** (kelsey.neely@bbaw.de) -- series co-editor
- **Felix Kopecky** (felix.kopecky@langsci-press-gug.org) -- junior publication manager (handles indexes, technical LaTeX)
- **Sebastian Nordhoff** (sebastian.nordhoff@langsci-press-gug.org) -- technical (colors, style)

### Overleaf

Project link: https://www.overleaf.com/5333979836npdxspvphgdd#275821

---

## Review Summary

### What the reviewer liked
- Clear and engaging style; complex topics made transparent for non-technical audience
- Accessible for pre- and in-service teachers
- Welcome breadth: covers fluency and conversation (unusual for the genre)

### Substantive points

**Stefan pre-empted (no action needed):**
- Reviewer questions pedagogical value of syntax trees (Ch 6) and Jespersen Cycle (Ch 11). Stefan says keep both.

**Address in revision:**

1. **Teacher Language Awareness framing (Ch 1).** Add a paragraph spelling out the TLA rationale. Cite Andrews (2007) *Teacher Language Awareness* (CUP) and Bartels (2009) "Knowledge About Language" in *Cambridge Guide to SLTE* (pp. 125--134). This gives the whole book a principled answer to "why should teachers know linguistics?"

2. **Target audience.** Specify ESL vs EFL vs both in the introduction. Reviewer notes these pose different challenges.

3. **Learning goals.** Review across chapters. Flagged:
   - Ch 1: where does pedagogical grammar fall (everyday vs technical)?
   - Ch 8: "apply frequency-based principles" -- mechanics of application thin
   - Ch 14: "apply information packaging principles" -- HOW to improve clarity pedagogically is missing

4. **Pedagogical bridge.** Recurring note: linguistic description doesn't always connect to teaching practice. Flagged in Chs 3, 4, 5, 8, 9. Not a rewrite -- add bridging paragraphs or sharpen existing ones.

5. **"Traditional sources."** Define more precisely. Reviewer notes CGEL could itself be viewed as traditional.

6. **Competitor acknowledgement.** Reviewer lists: Berry (2021), Celce-Murcia & Larsen-Freeman (1999), Cowan (2008), Park-Johnson & Shin (2020), Parrott (2000), Valenzuela (2020). Consider positioning relative to these in the intro.

### Formatting requirements (Stefan)

**Series rules (non-negotiable, settled in June 2024 exchange):**
- No italics in numbered examples (series-wide rule). Normal text; italics only to highlight a specific word/constituent.
- No underlining anywhere.
- emph for emphasis; bold only where emph is impossible (and in headings).
- Use `langid` (not `language`) in bib entries for non-English works.

**Stage 1 (first):** Bold and underlining cleanup
- emph for emphasis, bold only where emph is impossible, no underlining
- Simplify multi-color / double-underline examples (Ch 15 especially)
- Ch 5: colored sentences probably unnecessary

**Stage 2:**
- Examples into langsci-gb4e environments
- Use TBLS predefined boxes with icons (see TBLS-Packages on HU Box link)
- Tables in LangSci style (see LangSci guidelines)
- Section cross-references instead of hyperlinked words (e.g., "see Section 2.3" not hyperlinked "interrogatives")
- URLs shown explicitly, e.g., as footnotes (for print version)
- Verify figure rights (e.g. p. 37)
- Check whether color in figures is necessary; use LangSci color scheme (Sebastian may help)
- Footnotes: fix any inverted footnote markers

### Files

- `review/general-review.pdf` -- 4-page review
- `review/annotated-manuscript.pdf` -- marked-up book PDF (large)
- Stefan's HU Box link: https://box.hu-berlin.de/d/7fe14e6fb70e4697bf18/ (TBLS packages, style guides)

---

### 2026-03-13 Session Notes (afternoon)
- Footnote markers: found 10 actual inverted markers (via balanced-brace parser; initial agent analysis overcounted at 28). Fixed across Chs 01, 02, 07, 08, 09. Most were artifacts of `\href` → `\footnote{\url{}}` conversion.
- Wrapfigure: 3 instances in Ch 6 verified compatible. No action needed.
- Color palette resolved: Tol palette stays. Color-coded text is content, not formatting.
- Stefan email re figure permissions: Brett signs copyright declaration, keeps confirmations on file.
- Revision letter fully rewritten with Rapoport framing. All TODOs cleared.
- Remaining: annotated manuscript PDF (inline comments), xkcd permission.

### 2026-03-13 Session Notes (evening)
- Humour audit: multi-model audit complete (Claude Opus 4.6 + Codex gpt-5.4, ~200 suggestions total).
- Codex batches 5-6 (Chs 1-10) successfully dispatched; earlier batches 1-2 had failed on regex escaping.
- Claude retry agents generated fresh suggestions for Chs 6, 7, 18 (original suggestions rejected or insufficient).
- 14 humour insertions implemented across 8 chapter files (Chs 3, 4, 5, 6, 7, 8, 9, 18).
- Brett's "consider" list (~60 items from Claude + Codex) remains for future consideration; only 14 were confirmed and implemented.
- Remaining: xkcd #2942 permission.

### 2026-03-14 Session Notes (morning)
- "Two categories, one label" insight implemented: new tblsframed box in Ch 3 ("When one label names two things") + enhanced definiteness opening + cross-references in Chs 1 and 5.
- Cross-references revised after Brett flagged initial versions as too mechanistic. Principle: grow from the surrounding argument, don't announce abstract frameworks.
- Added item 7 to revision letter for Stefan.

### 2026-03-14 Session Notes (earlier)
- Annotated manuscript PDF fully reviewed: 71 annotations extracted via pymupdf.
- All 17 typo corrections already present in current .tex source (PDF was October 2025 draft).
- 48 substantive comments cross-referenced against DECISIONS.md: all duplicate the general review points already addressed.
- New items addressed in revision letter: CGEL footnotes defended (gateway function), "non-affirmative" vs "NPI" terminology defended, tone concerns in Chs 2/10/16 defended.
- Annotated manuscript item is now complete. Only remaining item: xkcd #2942 permission.

### 2026-03-14 Session Notes (morning, continued)
- Revision letter refined: pulled back superlatives ("single most productive" → "extremely productive"), replaced evaluative framing ("correctly identified" → "helpfully identified," "rightly notes" → "notes"), cut "Fair point." as teacher-grading, passive to active ("An internal rhetoric audit was conducted" → "I conducted"), added "I believe the content was fair, but the ordering was not."
- Added "where" as preposition (Ch 19, p.440 annotation) to CGEL footnotes paragraph in revision letter.
- Three-wave editorial review dispatched via Codex (66 agents total):
  - Wave 1: Wendy Lesser (prose quality, micro)
  - Wave 2: Edward Mendelson (intellectual architecture, meso)
  - Wave 3: John McPhee (structural economy, macro)
  - All 66 reviews written to `editorial-reviews/wave-{1,2,3}-{lesser,mendelson,mcphee}/`
  - Synthesis produced: `editorial-reviews/synthesis.md`
- Key finding: book systematically over-scaffolds (announces, does, re-announces, summarizes). Brett's decision: keep structural scaffolding (audience needs handrails), cut only nervous verbal tics ("as I've pointed out," "to reiterate," "recall that").
- Six broken sentences / copy-paste errors fixed:
  - Ch 6, line 217+225: "helped"/"you" → "had"/"my breakfast" (copy-paste from different tree)
  - Ch 11, line 297: dangling "and" deleted
  - Ch 4, line 528: "we drive our cars run" → "we drive, our cars run"
  - Ch 5, line 683: "has come to," → "has come to express time,"
  - Ch 16, line 346: "should instructor" → "should an instructor"
  - Ch 4, line 430: "is possible speak" → "is possible: speak"

### 2026-03-14 Session Notes (evening)
- Full editorial pass from synthesis: verbal tics (11 cut), chapter endings (20 rewritten), structural trimming
- Ch 1: countability section trimmed ~58%, mid-chapter glossary relocated, glossary definitions improved from HPC book
- Ch 5: complementation bridging paragraph added
- Ch 13: "Fluency across skills" deleted, Tokyo anecdote relocated
- Ch 20: detector framing imported from HPC book, contingency point sharpened, Judgment Severity Range compressed
- All 8 chapter glossaries consolidated into single back-of-book glossary (chapters/glossary.tex)
- Ch 14 closing resolved via multi-model dispatch (Codex won)
- Epigraph research: 6 files generated (international + Canadian poets, oblique poetry). 47 Best Canadian Poetry PDFs downloaded for next-session reading
- Remaining synthesis items: Ch 5 aspect/tense resequencing, Ch 7 pronunciation goals + suprasegmentals, Ch 9 digital-age resequencing, Ch 12 subjects overbuilt, Ch 15 Renaissance passage, Ch 17 repair consolidation, Ch 19 taxonomy order, Ch 20 intro pre-announces
- Draft mode turned off; snapshot saved

### 2026-03-17 Session Notes (morning)
- Proofread pipeline tuned (5 iterations on Ch 1) and deployed across all 20 chapters + preface, acknowledgments, glossary, appendix
- Grammar fixes applied per chapter: comma splices, missing articles, agreement, typos, punctuation
- Semantic macros: \textit → \mention (3493), \textsc → \term (344), `` '' → \enquote{} (Chs 1-2)
- Bibliography audit: 25+ corrections (wrong authors/years/pages/URLs, missing metadata, brace protection)
- Ch 19: 44 stranded braces fixed, 5 \\\hfill line breaks added, example labels → \textsc
- Ch 4 answer key: "arrive selects to" → "at" (factual error)
- Dash audit (Bringhurst standard): 337→106 en-dashes. ~228 converted to commas/parentheses/colons/semicolons. Kept ~110 (dialogue, surprise pivots, self-corrections, structural disambiguation).
- GitHub repo created: https://github.com/BrettRey/Language-landscapes
- Revision letter sent to Stefan (with repo URL added).
- Remaining: AI-phrase revision pass, model names in acknowledgments

## Next Actions

- [x] Import Overleaf source to local folder
- [ ] Read annotated manuscript PDF for inline comments
- [x] Download TBLS-Packages from HU Box link
- [x] Stage 1: bold/underline cleanup (March 12--13)
  - [x] \uline → \emph, \uuline → \textbf, gaps → \gap (793→0)
  - [x] Strip outer \textit{} from numbered examples
  - [x] Bold cleanup (6 emphasis→\emph, 390 structural kept)
  - [x] \href → footnote URLs (32→0)
  - [x] Package cleanup (contour/soul removed)
  - [x] Color palette: Keep Tol palette -- content, not house-style formatting
- [x] Stage 2: LangSci formatting
  - [x] 2a: tcolorbox → langsci-tbls (146 boxes converted, March 12--13)
  - [x] 2b: Tables → booktabs (~16 formal tables)
  - [x] 2d: Figure verification (rights resolved; 4 replaced with originals, 1 permission secured, xkcd obtained)
  - [x] 2e: Footnote markers (10 inverted markers fixed)
  - [x] 2f: Bibliography langid -- all works English, no additions needed
  - [x] Wrapfigure: 3 in Ch 6, compatible with langscibook.cls
- [x] Substantive revisions (all 7 reviewer items addressed)
- [x] Revision letter drafted (Rapoport-compliant)
- [x] Read annotated manuscript PDF for inline comments
  - 71 annotations total (48 substantive, 17 typos, 6 highlight-only)
  - Substantive comments largely duplicate the general review: pedagogy gap, syntax trees, learning goals, audience -- all already addressed via the 7 reviewer items
  - CGEL footnote complaints (4 instances): respond in revision letter; footnotes orient readers who consult CGEL
  - 17 typo corrections (strikeouts/carets): to be applied
- [x] xkcd #2942 permission (obtained)
- [x] Epigraphs: all 20 AI-generated chapter epigraphs replaced with real Canadian poetry (19 BCP 2020/2023 + Ondaatje). Fair use; no permissions needed.
