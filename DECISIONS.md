# Language Landscapes -- Decisions Log

2026-03-12 -- Underline replacement: \uline{} → \emph{}, \uuline{} → \textbf{}, gaps → \gap macro. Rationale: with examples in roman, italics become available for highlighting; bold for second-layer annotation per LangSci Generic Style Rules.

2026-03-12 -- Ch 15 colors: keep color, remap to LangSci palette. The cohesion chains need visual distinction that bold/italic alone can't provide.

2026-03-12 -- Workflow: local git + Overleaf sync via git remote.

2026-03-13 -- Ch 05 fill-in blanks: \uline{~~~~} exercise blanks converted to \gap macro (same visual function as syntactic gaps).

2026-03-13 -- Bold cleanup: only 6 running-text emphasis cases converted to \emph{}; ~390 structural bold instances preserved (table headers, NICE mnemonic, item labels, tcolorbox labels, dialogue speakers, etc.).

2026-03-13 -- Internal \href cross-references (3 instances) converted to \hyperref[label]{text} rather than footnote URLs. External \href all converted to text\footnote{\url{URL}}.

2026-03-13 -- Color palette: LangSci's langscibook.cls palette (20+ CMYK colors) lacks purple and magenta. Current Tol palette (xGreen/xOrange/xPurple/xPink) is deliberately colorblind-friendly. Recommend raising with Stefan/Sebastian rather than silently downgrading. PENDING Brett decision.

2026-03-13 -- Package cleanup: removed contour and soul; retained ulem for \xout{} (ellipsis strikethrough in Ch 15). Also removed duplicate mdframed loading.
