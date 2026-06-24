# Language Landscapes -- STATUS

**Status:** **Forthcoming.** [Catalogue page live Apr 16, 2026](https://langsci-press.org/catalog/book/555). CC BY 4.0. Not yet published (PDF not available).
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

### 2026-04-13 Session Notes (evening)
- Full Stefan formatting pass against his complete comment letter (~55 items). All addressed.
- Bold removal: run-in labels folded into prose with \term{} (Chs 7, 8, 15, 18, 20), pseudo-headings → \subsubsection{} (Ch 20), table headers de-bolded (all chapters), list labels de-bolded (Chs 8, 13, 15, 16, 20), learning objectives de-bolded (Ch 13).
- Trees in Ch 6: 15 \ea...\z examples → \begin{figure} environments, all cross-references updated, Ch 11 labels renamed.
- Wrapfigure → figure (Ch 6, 3 instances).
- \& → "and" in cross-references (Chs 1, 5, 10, 11, 12, 19). Citation formatting normalized.
- Ch 1: itemize → \ea, tabulars → \ea, "Learning Objectives" → sentence case.
- Ch 3: uncaptioned table given float + caption.
- Ch 20: Turkish examples glossed with \gll (sourced from Wikipedia + Wiktionary, cross-checked against Göksel & Kerslake 2005). "Meaning Without Grammar" → \subsection*{}.
- Bibliography: ~40 entries corrected. DOIs added for all De Gruyter/Mouton/Foris/Benjamins books (5 new, all resolved against publisher pages). Addresses added to all books/incollections. 24 subtitle capitals brace-protected. 17 proper nouns/acronyms brace-protected. urldate added to 16 entries. Author names standardized (Nation, Gibson, Searle, Boothby, Culicover, Carver, Gough, Tunmer). Duplicate Huddleston entry merged. Malformed Robb DOI fixed.
- Author index: auto-generated from citations via biblatex indexing=cite (was empty, now 223 entries). .latexmkrc added for build workflow.
- Back cover blurb rewritten (naturalist metaphor, no bullet list).
- Li Xiang spacing fixed.
- Build: 536 pages, clean.

### 2026-04-16 Session Notes (morning)
- Ran a multi-pass LangSci sanity cleanup and prose-polish pass across the manuscript, bibliography, figure references, and localcommands; the local XeLaTeX build remained successful throughout.
- Prepared clean Overleaf sync bundles under `snapshots/overleaf-sync-2026-04-16/` (`text-only` and `full`) and added `scripts/compare_overleaf_export.sh` so Overleaf source ZIPs can be compared against the intended sync set instead of the noisy local workspace.
- Compared `/Users/brettreynolds/Downloads/Language_Landscapes(1).zip` against the prepared text-sync bundle. Overleaf matched repo HEAD for 23/25 touched text files. The only Overleaf-side differences were four missing lexical items in `chapters/appendix.tex` and a commented `\orcid` line in `localcommands.tex`. Overleaf was also missing the three new PDF figure files now referenced by the manuscript (`Track_gauge.pdf`, `Places_of_articulation.pdf`, `Great_Vowel_Shift2c.pdf`).
- Pruned 27 unused graphics from `figures/` using the actual build graph in `main.fls` and confirmed the project still builds afterward.
- Sebastian follow-up identified: `tipa` is banned. The manuscript can migrate to `langsci-textipa`, but Chapter 7, Chapter 19, and the glossary still contain residual `tipa` macros that need Unicode/`\textprimstress` replacements before the package switch is clean.
- Current practical next step on Overleaf: replace the `chapters/` folder, `localbibliography.bib`, and `localcommands.tex`, and upload the three required PDF figures. Then resolve the `tipa` conversion if Sebastian insists on immediate removal.

### 2026-04-28 Session Notes (afternoon)
- **Japanese translation review boards run on Ch 1 and Ch 2.** Five-reviewer panel each (academic Japanese translator, Japanese EFL teacher educator, Japanese linguistics scholar, bilingual copy editor, hostile reviewer). All on Opus.
- **Project-scope question is unresolved and recurs across both chapters**: faithful carry-over translation (current state) vs. localised Japanese edition. Hostile reviewer pushes hardest for the latter; copy editor and translator see polish-needed work; EFL educator and linguistics scholar split. Brett to decide before further chapter translations.
- **Cross-chapter recurring issues** (same problems in both chapters):
  - `\enquote{}` systematically replaced with 「」 (Ch 1: 38→0; Ch 2: 47→3). Need book-wide policy decision.
  - "Answer key" → "解答のヒント" (softens to "hints"). Both chapters.
  - Block-quote policy from translation plan §3 (English verbatim + Japanese gloss) is followed inconsistently. Ch 1: Allen 2008 quote replaced. Ch 2: Judges, Cook, Pullum quotes replaced; only Middlemarch compliant.
  - Inconsistent `\term{}` argument language (English vs Japanese vs bilingual).
  - Learning-objective typos at the very top of both chapters (Ch 1 line 86 `含外` → `除外`; Ch 2 line 7 `直言` → `方言`).
- **Ch 1 specific issues**: typo line 303 (`〜かどうかな`); determinative/determiner category-function distinction collapsed into 限定詞; 呼応/一致 doublet inconsistent; Allen 2008 quote not preserved per plan; epigraph (Kazim Ali) feels imported.
- **Ch 2 specific issues**: Samantha Nock epigraph silently deleted (entire `\epigraph{}` block missing); Judges 12:4 citation fabricated (`12:4-6 (新改訳聖書をもとに調整)` claims a Japanese Bible source while admitting modification — source-grounding violation); section title "Standard English(es)" loses the `(es)` plural that signals the chapter's central thesis; mommy-sock gloss meaning shift; `\textit{Middlemarch}` styling lost; `\term{}` over-applied (EN 8 → JA 18); 威信 (prestige) absent where Japanese sociolinguistic convention expects it; 方言 vs 変種 used inconsistently without gloss.
- **Localisation gaps** flagged by R2/R5 across both chapters: no engagement with 学校英文法 / 5文型 / 国語審議会 / 関西弁 stigmatisation / 沖縄語 displacement; no answer to the Japanese EFL teacher's actual classroom question ("which English do I teach?"); soup analogy doesn't transfer (スープ is a narrow loan-category in Japanese, not a fuzzy basic-level one); action/violation wordplay missing the obvious する-verbalisation parallel.
- **What works (consensus)**: です・ます register held cleanly; Nishimura code-switching passage in Ch 2 (added Japanese paraphrase) genuinely strengthens the original; VHS/Betamax analogy lands perfectly for Japanese readers; LaTeX integrity excellent (all 91 `\is{}` index tags exact in Ch 2; same for Ch 1); CGEL-aligned terminology spine (主要部/従属部, 語彙範疇, 法助動詞, 等位接続) defensible.
- **Pending decisions for Brett**: (1) project scope (carry-over vs localised); (2) `\enquote{}` book-wide policy; (3) block-quote treatment policy; (4) determinative/determiner Japanese coinage; (5) epigraph policy across all 20 chapters (translate? facing English+gloss? commission Japanese poems? drop?); (6) 呼応 vs 一致 single term.

### 2026-04-28 Session Notes (afternoon)
- Exported the manuscript into AI-companion assets under `ai-companion/export/`: `book_chunks.jsonl`, `book_manifest.json`, `chapter_stats.json`, and `table_of_contents.json`. The current corpus is 648 retrieval chunks, about 121k clean words, with an estimated 13.02 audiobook hours at 155 wpm.
- Built a first local AI companion server in `scripts/run_ai_companion_chat.py`, then replaced the single chat view with a fuller browser companion: landing page, `Read`, `Ask`, `Contents`, `Glossary`, `Index`, and a source-inspector modal. Web assets now live in `ai-companion/web/`.
- The current local companion is grounded in the exported book data and the manuscript sources. It uses local retrieval over `book_chunks.jsonl`, parses the glossary from `chapters/glossary.tex`, parses the subject index from `index-outline.tex` plus `localseealso.tex`, and supports optional OpenAI synthesis when `OPENAI_API_KEY` is set.
- Core product direction locked: `Read | Ask` is the main split; AI is subordinate to the book; chapter/section/source navigation beats any topographic-map metaphor.
- Added a defensive port fallback: if `8765` is already occupied, `python3 scripts/run_ai_companion_chat.py serve` now falls through to the next open port and reports the bound URL instead of crashing. This is specifically to coexist with Brett's shared-memory MCP server on 8765.
- Prepared both Claude Design and Artifact handoff packages under `ai-companion/design-handoff/` and `ai-companion/artifact-handoff/`, but the practical path forward is now to iterate on the local companion first and only then translate it into an Artifact-ready bundle.
- Verified the current Anthropic constraint from official docs: this repo can prepare an Artifact-ready bundle, but the actual Artifact creation/publish step still has to happen inside Claude rather than via a separate external API workflow.

### 2026-05-27 PM Provenance Audit
- Current tracked manuscript/production edits exactly match `snapshots/overleaf-sync-2026-04-16/text-only/` for all 28 files in that sync set: 23 chapter/front/back files, `localbibliography.bib`, `localcommands.tex`, and the three required PDF figures.
- The previous Overleaf comparison report (`snapshots/overleaf-compare/20260416-095846-text-only/`) shows the April 16 live Overleaf export lagging behind that intended sync set: three required PDF figures missing from Overleaf, 25 changed text/support files, and many extra local-only project files in the export.
- The dirty state is therefore a production-sync state, not casual source drift: commit/sync decisions should happen in a dedicated book-production session after a fresh Overleaf export comparison.
- Added `.gitignore` for generated LaTeX/index scratch files and OS/editor noise. It intentionally does not ignore PDFs, because figure PDFs can be source assets for LangSci.

### 2026-06-01 Session Notes (morning)
- Triaged the remaining PaperHive/GitHub issue tranche with Brett's judgments: ignored the editor's mistaken conjunction analyses (#244, #227, #161, #159), used Oxford spelling for #232, accepted #147 only for asking about `'ll`, and kept #111's capitalization principle while leaving the three flagged instances unchanged.
- Completed the example-typography cleanup: converted remaining `\strong{}` emphasis to `\emph{}`, handled split `\mention{A} B \mention{C}` body-text cases as continuous mentions with internal `\emph{}`, and revised the `sheeps` numbered example so examples are roman with explanations at the end in parentheses.
- Preserved italic `\mention{}` in appendix lexical catalogues of prepositions and determinatives; those are catalogues of forms, not numbered linguistic examples.
- Built successfully with `xelatex && biber && xelatex && xelatex` and standing warnings only; `git diff --check` passed.
- Shipped `be80906 Refine example typography and dialect markers` to `origin/master`.
- Prepared Overleaf upload bundle: `/Users/brettreynolds/Documents/LLM-CLI-projects/papers/Language_Landscapes-overleaf-be80906.zip` (20 MB, 132 files, curated source inputs only).

### 2026-06-06 Session Notes (morning)
- Brett uploaded the post-proofread source set to Overleaf: `chapters/`, `localbibliography.bib`, `localseealso.tex`, `backmatter.tex`, and `localpackages.tex`.
- Confirmed from git history that those files cover the Overleaf-relevant changes from the May 28--June 1 proofreading and typography pass.
- No Overleaf upload is needed for `.gitignore`, `DECISIONS.md`, or `STATUS.md`; those are local repository/tracking files.
- Next practical state: await Sebastian/Overleaf feedback, or download a fresh Overleaf source export and run `scripts/compare_overleaf_export.sh` if a verification pass is needed.

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
- [x] Build first local AI companion over the manuscript export
- [ ] Browser-test the richer local companion and tighten interaction flow based on live use
- [ ] Decide whether to convert the current local companion into a single-file Artifact-ready bundle for Claude

### 2026-06-21 Session Notes (PM)

- **Localization effort has a roster.** People pages created for all five new edition recruits: Niel Sord (Tagalog), Murat Sabuncu (Turkish), Sounak Das (Bengali/Hindi), Afandi Setiawan (Indonesian), Pairoj Kunanupatham (Thai). Koike (Japanese) page already existed. All in `Project-Management/people/`. Languages floated to Pullum but not yet pursued: Chinese ("Larry"), Korean.
- **`/cross-pollinate` run** → `notes/cross-pollinate-20260621.md`. Anchored on the localization frontier. Top hits: Fricker (localization as metalinguistic enfranchisement), Agha (enregisterment; metapragmatic scaffolding per term), truth pluralism (one-concept/many-realizers frame for the translator guide), Powell convergence, Wolters Zipfian (Ch 8 bridge).
- **Five terminology-framing notes drafted** in `correspondence/` (one per new recruit), tailored to each open thread, pending Brett's send. Shared message: preserve the distinction/test, not the word; bilingual glossary defining by test.
- **Open:** Murat's three questions are answered in his draft but he's waiting on a reply; his note half-promises the master term list, attach it. Koike still needs a separately tailored note. Localizer-guidance materials (translator guide / metapragmatic-scaffolding brief) don't exist yet and are where the Fricker/Agha angles would land.
- Decisions logged in `DECISIONS.md` (terminology policy; correspondence scope).
