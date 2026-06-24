# Turkish sample chapter plan
## Selection
Use Chapter 18, "Subordination and coordination," as the sample Turkish translation.

Reason: it is the shortest real content chapter with substantial numbered examples. It has about 3,300 source words, 50 numbered example lines, and no `forest` or `tikzpicture` tree source. It does contain four tree figures as already-rendered PDFs; I will keep them if they compile cleanly in the standalone build because they make the sample look like the book without turning the task into a tree-layout exercise.

The standalone PDF should present the chapter as Chapter 18, not as a new Chapter 1. The main book files should remain untouched.
## Turkish title and scope
Working title: `Bağımlılaştırma ve eşgüdüm`

This is a sample translation, not a localized Turkish edition. I will translate the chapter prose into idiomatic academic Turkish while preserving the book's argument, teaching orientation, and example set.
## `\mention{...}` policy
Let inline `\mention{...}` stand on its own when the mentioned English form is a familiar function word, a repeated example fragment, or immediately explained in the surrounding sentence:

- `\mention{that}`
  
- `\mention{whether}`
  
- `\mention{and}`, `\mention{or}`, `\mention{but}`
  
- short repeated fragments such as `\mention{that Kim left}`
  

Add a Turkish gloss in backticks only when a Turkish reader would otherwise lose the local point:

- `\mention{if}` (`whether` anlamındaki `if`, koşul anlamındaki `if` değil)
  
- `\mention{as tall as}` `en az ... kadar uzun`
  
- `\mention{taller than}` `...-den daha uzun`
  
- technical comparisons such as `\mention{did}` as a VP pro-form
  

Do not mechanically gloss every `\mention`. Too many backtick glosses would make the Turkish prose look like an annotated teacher's note rather than a book chapter.
## Numbered examples
Every numbered example should have:

1. the original English example line;
  
2. an interlinear Turkish gloss line for Turkish-style transparency, oriented to Turkish readers: lexical Turkish equivalents plus clear Turkish grammatical labels such as `GEÇMİŞ`, `3TEK`, `BAĞ`, `NEG`, `SIF`, `AD`;
  
3. a natural Turkish translation line introduced with `\glt`;
  
4. the existing bracket labels translated into Turkish where useful, for example `[bağımlı]`, `[eşgüdümlü]`, `[zorunlu]`.
  

For examples whose purpose depends on English word order or the English coordinator/subordinator itself, the English line stays first. The Turkish translation should be natural, not morpheme-for-morpheme Turkish. Ungrammatical examples keep `[*]`, and the Turkish translation can state that the intended sentence is ungrammatical in English.
## Standalone build
Create a separate standalone driver and translated chapter file under `translation-samples/`, using the existing `langscibook` styling, metadata, packages, and commands where possible.

Expected output:

- `translation-samples/main_tr_ch18.pdf`
  

Build target:

- `latexmk -xelatex translation-samples/main_tr_ch18.tex`
  

* * *

comments: {} suggestions: {}
