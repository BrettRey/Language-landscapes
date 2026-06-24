# French, Spanish, and Japanese terminology plan for Chapter 18
Purpose: fix the terminology before producing the French, Spanish, and Japanese standalone versions of Chapter 18, "Subordination and coordination." The goal is not just fluent translation. The translated chapters must preserve the book's core distinctions: category vs function, clause vs phrase, head-dependent structure vs non-headed coordination, and English-specific clause types.
## Global Translation Policy
Use the target-language term as the main term, with the English term in parentheses on first mention when the local term is either non-obvious or only approximately equivalent. After first mention, use the target-language term alone unless the paragraph is explicitly comparing terms.

Leave English example material in English. Translate the surrounding prose, example labels, interlinear lexical glosses, and natural translations. Numbered examples should keep the same analytical purpose as the English original.

For `\mention{...}`, let the English form stand on its own when the form itself is under discussion, especially for `that`, `whether`, `if`, `and`, `or`, `but`, `than`, and `as`. Add a short target-language gloss only when the reader needs it to follow the local point, for example the `whether` meaning of `if`, or the "at least as tall as" interpretation of `as tall as`.

For interlinear examples, use the requested natural-translation convention in every language:

```tex
\glt `natural translation in the target language'
```

Do not use double quotation marks for `\glt` translations.

Phrase-category abbreviations:

| Category | French | Spanish | Japanese |
| --- | --- | --- | --- |
| noun phrase | syntagme nominal (SN) | sintagma nominal (SN) | 名詞句（NP） |
| verb phrase | syntagme verbal (SV) | sintagma verbal (SV) | 動詞句（VP） |
| adjective phrase | syntagme adjectival (SAdj) | sintagma adjetival (SAdj) | 形容詞句（AdjP） |
| adverb phrase | syntagme adverbial (SAdv) | sintagma adverbial (SAdv) | 副詞句（AdvP） |
| preposition phrase | syntagme prépositionnel (SP) | sintagma preposicional (SP) | 前置詞句（PP） |

Keep the compact tree/category labels `Sdr`, `Crd`, and `Mk` for subordinator, coordinator, and marker unless the figure labels are fully remade. These labels are already compact and tied to the book's analysis.
## Confound-Control Policy
Some terms have no perfect local equivalent. For these, the translation should not rely on the term alone. It should pair the term with a small recurring diagnostic, mnemonic, or contrast the first time the term matters. The aim is to keep readers from importing an incompatible school-grammar or everyday meaning.

| Term family | Likely confound | Translation tool |
|---|---|---|
| clause vs phrase | French `proposition` and Spanish `oración` can be heard as sentence-level terms; French `phrase` and Spanish `frase` are false friends for English `phrase`. | Introduce the pair contrastively: a clause/proposition/oración/節 is the VP-headed unit; a phrase/syntagme/sintagma/句 is a headed unit below clause level. Use a "container vs contained unit" analogy only where needed. |
| main vs matrix | Readers may treat both as "the main clause." | Use a parent/container mnemonic: a matrix clause is the clause that contains another clause; a main clause is not contained in a larger matrix. Say explicitly that one clause can be both matrix and main. |
| content clause | French `complétive` and Spanish `completiva/sustantiva` suggest function, not clause type. | Define by contrast: content clauses are the default subordinate clauses, unlike relative and comparative clauses. Use the familiar local term only as a bridge, not as the analytic definition. |
| subordinator/coordinator vs marker | Local "conjunction" terminology can make the words sound like heads or semantic connectors. | Repeat the category/function contrast: a subordinator or coordinator is the small word class; marker is the function it serves in the tree. |
| head/dependent vs coordination | Readers may look for a head in every multiword unit. | Use a simple structural contrast: subordination has a head-dependent architecture; coordination is equal-status and non-headed. |
| complement vs modifier/adjunct | School grammar often treats many dependents as "complements" or "circumstantials" without the selection distinction. | Use the licensing mnemonic: complements are selected or licensed by a head; modifiers/adjuncts add information without being selected in the same way. |
| ellipsis vs gap | Both can look like "something missing." | Use the recoverability/tree contrast: ellipsis is recoverable meaning without a syntactic slot in the tree; a gap is a structural position. |
| subjunctive in the mandative | Japanese `仮定法` can suggest counterfactual meaning; French/Spanish mood terms can invite transfer from those languages. | Tie the term to the English form: in `that he be there`, the relevant fact is the plain verb form in a requirement/necessity construction. |

These supports should be built into the translated prose at the first point of possible confusion. They should be brief; the translated chapters should still read like book chapters, not terminology notes.

Approved production rule: because the sample chapter is Chapter 18, do not re-explain every technical term as though the reader has skipped the preceding chapters. Assume core terms such as clause, phrase, head, dependent, complement, modifier, and subject have already been introduced unless the localized term itself creates a new trap in the immediate passage. In this chapter, the highest-risk area is the coordination terminology, especially where readers might confuse equal-status coordination with head-dependent subordination or with loose discourse connection. Add short analogies, warnings, or diagnostics there when the local term is likely to be misconstrued.
## Load-Bearing Choices
### Clause vs Phrase
The book's `clause` is a grammatical structure headed by a VP, normally with a subject. The book's `phrase` is a headed structure below that level. This distinction is especially fragile in French and Spanish because everyday `phrase`/`frase` can mean a sentence or expression.

Recommendation:

| English | French | Spanish | Japanese | Notes |
| --- | --- | --- | --- | --- |
| clause | proposition | oración | 節   | French `proposition` has some risk, but the alternatives are worse: `phrase` is a false friend here, and `clause` is too Anglicized/specialized for the sample. Spanish `oración` is teacher-facing and standard in `oración subordinada`; `cláusula` is available as a precision gloss if needed, but should not be the default. Japanese continues the existing `節`. At first use, define the term structurally as the VP-headed unit. |
| phrase | syntagme | sintagma | 句   | Do not use French `phrase` or Spanish `frase`. Existing Japanese already uses `句`. |
| phrasal category | catégorie syntagmatique | categoría sintagmática | 句範疇 | Needed where the chapter contrasts lexical categories with larger phrases. |
| lexical category | catégorie lexicale | categoría léxica | 語彙範疇 | Existing Japanese uses `語彙範疇`; keep it. |
| syntactic function | fonction syntaxique | función sintáctica | 統語機能 | Use function terms consistently in the coordination section. |

### Main, Matrix, and Subordinate Clauses

The chapter depends on the relational nature of `matrix` and `subordinate`, and on the non-relational status of `main clause`.

| English | French | Spanish | Japanese | Notes |
| --- | --- | --- | --- | --- |
| main clause | proposition principale | oración principal | 主節  | Standard and clear in all three languages. |
| matrix clause | proposition matrice | oración matriz | 母節  | Do not collapse this into "main clause." A clause can be matrix without being main. |
| subordinate clause | proposition subordonnée | oración subordinada | 従属節 | Standard term. |
| subordination | subordination | subordinación | 従属化 / 従属関係 | Use `従属化` for the process and chapter title, `従属関係` where the prose means dependency relation. |
| dependent | dépendant | dependiente | 従属部 | Existing Japanese uses `従属部`; keep it. |

### Content, Comparative, and Relative Clauses

`Content clause` is the most terminologically risky term. French `complétive` and Spanish `completiva` are familiar, but they can suggest "complement clause," while the chapter explicitly says content clauses can function in several ways, including as subject.

Recommendation: use a CGEL-compatible translated term as primary, with the familiar local term as an explanatory bridge on first mention.

| English | French | Spanish | Japanese | Notes |
| --- | --- | --- | --- | --- |
| content clause | proposition de contenu (proche des complétives) | oración de contenido (tradicionalmente, completiva o sustantiva) | 内容節 | This avoids implying that the clause type is defined by complement function. |
| declarative content clause | proposition de contenu déclarative | oración de contenido declarativa | 平叙内容節 | Use `declarative`, not "affirmative"; polarity is separate. |
| interrogative content clause | proposition de contenu interrogative | oración de contenido interrogativa | 疑問内容節 | Preserve the syntax/meaning distinction between interrogatives and questions. |
| comparative clause | proposition comparative | oración comparativa | 比較節 | Straightforward. |
| relative clause | proposition relative | oración de relativo | 関係節 | `Oración relativa` is possible in Spanish, but `oración de relativo` makes the clause type clearer. |

### Interrogatives

The book intentionally uses `basic interrogative` and `focused interrogative`, while noting elsewhere that CGEL would say `closed` and `open`. Do not silently replace the author's terms with the CGEL alternatives in Chapter 18.

| English | French | Spanish | Japanese | Notes |
| --- | --- | --- | --- | --- |
| interrogative clause | proposition interrogative | oración interrogativa | 疑問節 | Use syntactic term, not "question" term. |
| basic interrogative | interrogative de base | interrogativa básica | 基本疑問節 | Keep the author's label, even though these often ask closed questions. |
| focused interrogative | interrogative focalisée | interrogativa focalizada | 焦点化疑問節 | Preserve the focus analysis. |
| subject-auxiliary inversion | inversion sujet-auxiliaire | inversión sujeto-auxiliar | 主語・助動詞倒置 | Standard enough and transparent. |

### Subordinators, Coordinators, and Markers

The chapter says subordinators and coordinators are lexical categories, but that they function as markers rather than heads. Terms must not erase that category/function distinction.

| English | French | Spanish | Japanese | Notes |
| --- | --- | --- | --- | --- |
| subordinator | subordonnant | subordinador | 従属接続詞 | Prefer the compact category term. In Japanese, use `従属接続詞` as the lexical-category-like term, then state that it functions as a `標識`. |
| coordinator | coordonnant | coordinador | 等位接続詞 | Avoid making this merely a semantic "connector." It is the small category containing `and`, `or`, and `but`. |
| marker | marqueur | marcador | 標識  | Function term. Important: a subordinator/coordinator can function as a marker. |
| head | tête | núcleo | 主要部 | Existing Japanese uses `主要部`; keep it. |
| non-headed | sans tête | sin núcleo | 主要部をもたない | Use this plain phrasing rather than technical endocentric/exocentric labels. |

Rejected default alternatives:

| Avoid as primary | Why |
|---|---|
| French `conjonction de subordination` / Spanish `conjunción subordinante` | Too tied to school grammar and not ideal for the book's small category `Sdr`. Can be mentioned descriptively if needed. |
| Japanese `従属標識` as the main equivalent of `subordinator` | It makes "subordinators function as markers" read tautologically. Better: `従属接続詞` for category, `標識` for function. |
| Japanese `並列` for `coordination` | Too broad and less tied to equal syntactic status. Use `等位接続`; `並列` can appear only as an explanatory paraphrase. |

### Complements, Modifiers, Adjuncts, and Subjects

The coordination section tests whether coordinated elements have the same syntactic function. These terms need to be consistent.

| English | French | Spanish | Japanese | Notes |
| --- | --- | --- | --- | --- |
| complement | complément | complemento | 補部  | Use Japanese `補部`, not `補語`, because the book's complement function is broader than school-grammar predicative complements. |
| modifier | modificateur | modificador | 修飾語 | Existing Japanese uses `修飾語`; keep it in prose and labels. |
| adjunct | adjoint | adjunto | 付加部 | Appears in labels such as "time adjuncts." Avoid French `complément circonstanciel`, which imports a different school-grammar analysis. |
| subject | sujet | sujeto | 主語  | Standard. |
| extraposed subject | sujet extraposé | sujeto extrapuesto | 外置主語 | Use the technical term; explain if needed. |
| object | objet | objeto | 目的語 | Used mainly in comparison labels. |

### Coordination Family

This is the chapter's second core domain. Japanese should use `等位接続` consistently, correcting the existing Chapter 1 placeholder where `coordination` was left in English.

| English | French | Spanish | Japanese | Notes |
| --- | --- | --- | --- | --- |
| coordination | coordination | coordinación | 等位接続 | Chapter title: French `Subordination et coordination`; Spanish `Subordinación y coordinación`; Japanese `従属化と等位接続`. |
| coordinate(s) | coordonné(s) / éléments coordonnés | coordinado(s) / elementos coordinados | 等位要素 | Use plural paraphrases where morphology would get awkward. |
| coordinate structure | structure coordonnée | estructura coordinada | 等位構造 | Good for prose around examples and figures. |
| symmetric coordination | coordination symétrique | coordinación simétrica | 対称的等位接続 | Straightforward. |
| asymmetric coordination | coordination asymétrique | coordinación asimétrica | 非対称的等位接続 | Straightforward. |
| distributive coordination | coordination distributive | coordinación distributiva | 分配的等位接続 | The property applies to each coordinate individually. |
| joint coordination | coordination conjointe | coordinación conjunta | 共同的等位接続 | The property applies to the group together. |
| asyndetic coordination | coordination asyndétique | coordinación asindética | 無接続の等位接続 | Technical term is fine in French/Spanish; Japanese should be transparent. |
| syndetic coordination | coordination syndétique | coordinación sindética | 接続詞付きの等位接続 | Technical term is fine in French/Spanish; Japanese should be transparent. |
| correlative coordination | coordination corrélative | coordinación correlativa | 相関的等位接続 | Use for `both...and`, `either...or`, `neither...nor`. |
| layered coordination | coordination à plusieurs niveaux | coordinación por niveles | 階層的等位接続 | Prefer transparent terms over calques like "stratified" unless the prose needs compactness. |
| discourse connector | connecteur discursif | conector discursivo | 談話接続表現 | Sentence-initial coordinators are not tight coordinations here; they can work as discourse connectors. |

### Comparison, Ellipsis, and Pro-Forms

Comparative clauses rely on ellipsis and on the distinction between gaps and ellipsis. Keep this explicit.

| English | French | Spanish | Japanese | Notes |
| --- | --- | --- | --- | --- |
| equality | égalité | igualdad | 同等  | In the `as tall as` footnote, explicitly say this label is somewhat misleading. |
| inequality | inégalité | desigualdad | 不等  | Used for `taller than`. |
| ellipsis | ellipse | elipsis | 省略  | Distinguish from gaps. |
| gap | lacune | hueco | 空所  | French `trace` would import a movement analysis not needed here; Spanish `hueco` is more reader-friendly than `vacío`. |
| pro-form | proforme | proforma | 代用形式 | Use for `did` replacing a VP. |
| fronting | antéposition | anteposición | 前置  | Use the plain syntactic term, not movement-heavy terminology unless the chapter requires it. |

### Mandative, Subjunctive, and Indicative

This section is English-specific and vulnerable to false friends. Keep English terms visible at first mention.

| English | French | Spanish | Japanese | Notes |
|---|---|---|---|---|
| mandative | mandatif (mandative) | mandativo (mandative) | mandative構文（命令・要求構文） | French/Spanish can naturalize the term; Japanese should keep English `mandative` plus an explanatory gloss. |
| subjunctive | subjonctif | subjuntivo | 仮定法現在 | In Japanese, plain `仮定法` is too broad and often evokes counterfactuals; `仮定法現在` matches examples like `that he be there`. |
| indicative | indicatif | indicativo | 直説法 | Standard. |
| should variant | variante avec `should` | variante con `should` | `should`型 | Leave `should` as an English form under discussion. |

## Example Labels

Translate example labels where they help the target reader:

| English label | French | Spanish | Japanese |
| --- | --- | --- | --- |
| separate | séparées | separadas | 別個  |
| subordinate | subordonnée | subordinada | 従属  |
| coordinate | coordonnée | coordinada | 等位  |
| main | principale | principal | 主節  |
| main/matrix | principale/matrice | principal/matriz | 主節/母節 |
| content | contenu | contenido | 内容  |
| comparative | comparative | comparativa | 比較  |
| relative | relative | de relativo | 関係  |
| obligatory | obligatoire | obligatorio | 必須  |
| optional | facultatif | opcional | 任意  |
| inadmissible | inadmissible | inadmisible | 不可  |
| complements | compléments | complementos | 補部  |
| modifiers | modificateurs | modificadores | 修飾語 |
| mixed functions | fonctions mixtes | funciones mixtas | 機能の混在 |

## Practical Implementation Notes

Create separate drivers and chapter files:

| Language | Driver | Chapter source | Expected PDF |
|---|---|---|---|
| French | `translation-samples/main_fr_ch18.tex` | `translation-samples/ch18_fr.tex` | `translation-samples/main_fr_ch18.pdf` |
| Spanish | `translation-samples/main_es_ch18.tex` | `translation-samples/ch18_es.tex` | `translation-samples/main_es_ch18.pdf` |
| Japanese | `translation-samples/main_ja_ch18.tex` | `translation-samples/ch18_ja.tex` | `translation-samples/main_ja_ch18.pdf` |

Each driver should set `\setcounter{chapter}{17}` so the standalone sample renders as Chapter 18. The main book files should remain untouched.

## Approved Decisions

These decisions are approved for implementation:

1. Spanish `clause`: use `oración`, not `cláusula`, for the main prose.
  
2. French/Spanish `content clause`: use `proposition/oración de contenu/contenido` as the CGEL-compatible primary term, with `complétive/completiva` only as an explanatory bridge.
  
3. Japanese `subordinator`: use `従属接続詞` for the category and `標識` for the marker function.
  
4. Japanese `coordination`: use `等位接続`, not the broader `並列`.
  
5. Japanese `complement`: use `補部`, not `補語`.
  
6. Japanese `subjunctive`: use `仮定法現在` in the mandative examples, not plain `仮定法`.
