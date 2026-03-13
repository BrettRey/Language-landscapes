# TBLS Box Conversion Mapping

## TBLS environments (from langsci-tbls package)

| Environment | Description | Arguments |
|---|---|---|
| `tblsframedsymbol` | Framed + icon | `{title}[frame color][frame width]{icon}` |
| `tblsfilledsymbol` | Shaded + icon | `{title}[bg color]{icon}` |
| `tblslineshorizontal` | Lines above/below | `{title}[line width][line color]` |
| `tblsframed` | Framed, no icon | `{title}[frame width][frame color]` |
| `tblsfilled` | Shaded, no icon | `{title}[shading color]` |

Icons: alarm, book, bulb, bulbon, code, explore, filter, glass, glass2, law, more, pencil, people, plus, r, receipt, refresh, report, test, tree

## Conversion rules

| Current pattern | → TBLS | Icon |
|---|---|---|
| Learning Objectives (blue bg, blue frame) | `tblsframedsymbol{title}{bulb}` | bulb |
| Check Your Understanding / Quick Self-Check / Pattern Recognition (yellow/orange) | `tblsframedsymbol{title}{test}` | test |
| Pause and Reflect (yellow/orange) | `tblsframedsymbol{title}{test}` | test |
| Practice / Try This / Apply Your Knowledge (green) | `tblsframedsymbol{title}{pencil}` | pencil |
| Exercise (white bg, breakable, colored frame) | `tblsframedsymbol{title}{pencil}` | pencil |
| Practice Consolidation (green) | `tblsframedsymbol{title}{pencil}` | pencil |
| Teaching Tip / Learning Strategy (blue tint) | `tblsfilledsymbol{title}{bulbon}` | bulbon |
| Cross-Linguistic Awareness (blue tint) | `tblsfilledsymbol{title}{explore}` | explore |
| Strategic Insight / Practical Application (blue tint) | `tblsfilledsymbol{title}{bulbon}` | bulbon |
| Named content boxes (white, breakable) | `tblsframed{title}` | — |
| Answer Key / Answer (gray/white) | `tblsfilled{title}` | — |
| Tests used in this chapter (gray) | `tblsfilled{title}` | — |
| Essay Questions / Short Answer (white) | `tblslineshorizontal{title}` | — |
| Self-Assessment Checklist (yellow) | `tblsframedsymbol{title}{test}` | test |
| Observation Exercise (yellow/orange) | `tblsframedsymbol{title}{glass}` | glass |
| Diagnostic Awareness (yellow) | `tblsframedsymbol{title}{test}` | test |
| Reflection (blue tint) | `tblsfilledsymbol{title}{bulbon}` | bulbon |

## Notes

- All current boxes use `breakable` -- langsci-tbls handles this natively
- Drop `colback`, `colframe`, `fonttitle`, `coltitle`, `colbacktitle`, `parbox` options
- Keep `\label{}` and `\is{}` index entries attached to the environment
- Title text stays the same (just remove tcolorbox option syntax)
- Subtitles available via `\tcbsubtitle{text}` if needed
