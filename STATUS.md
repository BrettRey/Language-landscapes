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

## Next Actions

- [x] Import Overleaf source to local folder
- [ ] Read annotated manuscript PDF for inline comments
- [ ] Download TBLS-Packages from HU Box link
- [x] Stage 1: bold/underline cleanup (March 12--13)
  - [x] \uline → \emph, \uuline → \textbf, gaps → \gap (793→0)
  - [x] Strip outer \textit{} from numbered examples
  - [x] Bold cleanup (6 emphasis→\emph, 390 structural kept)
  - [x] \href → footnote URLs (32→0)
  - [x] Package cleanup (contour/soul removed)
  - [ ] Color palette: PENDING -- raise Tol vs LangSci palette with Stefan
- [ ] Stage 2: LangSci formatting (blocked on TBLS package)
- [ ] Substantive revisions (TLA framing, learning goals, bridging paragraphs)
