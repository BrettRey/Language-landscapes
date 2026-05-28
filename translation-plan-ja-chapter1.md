# Translation Plan: Chapter 1 (English to Japanese)

## 1. Project Overview & Tone
- **Target Audience:** Aspiring and current English-language teachers in Japan.
- **Tone & Style:** The original text is conversational, encouraging, yet academically rigorous ("If the idea of teaching English grammar makes you nervous, you're not alone.").
- **Recommendation:** Use the polite **"Desu/Masu" (です・ます) form** to maintain the approachable, pedagogical voice of the author, rather than the stiff academic "Da/Dearu" (だ・である) form.

## 2. Handling Technical Terminology (Glossary)
Linguistic terms must be translated consistently. A preliminary glossary for Chapter 1:
- **Noun / Noun Phrase (NP):** 名詞 (Meishi) / 名詞句 (Meishiku)
- **Verb / Verb Phrase (VP):** 動詞 (Doushi) / 動詞句 (Doushiku)
- **Adjective / Adjective Phrase (AdjP):** 形容詞 (Keiyoushi) / 形容詞句 (Keiyoushiku)
- **Adverb / Adverb Phrase:** 副詞 (Fukushi) / 副詞句 (Fukushiku)
- **Determinative (Category):** 決定詞 (Ketteishi)
- **Determiner (Function):** 限定詞 (Genteishi)
- **Auxiliary Verb / Modal:** 助動詞 (Jodoushi) / 法助動詞 (Houjodoushi)
- **Head / Dependent:** 主要部 (Shuyoubu) / 従属部 (Juuzokubu)
- **Subject / Object:** 主語 (Shugo) / 目的語 (Mokutekigo)
- **Countability (Count / Non-count):** 可算性 (Kasansei) / 可算名詞 (Kasan-meishi) / 不可算名詞 (Fukasan-meishi)
- **Clause:** 節 (Setsu)
- **Agreement:** 一致 (Itchi)

## 3. Formatting and Style Guidelines
- **Technical Terms (`\term{}`):** Format technical terms introduced using the `\term{}` macro as bilingual parentheticals. Example: `\term{助動詞（auxiliary verbs）}`.
- **Emphasis:** Avoid using `\emph{}` or `\textit{}` on Japanese text, as slanting Japanese characters reduces legibility. Only use these macros on English text.
- **Prose Style:** Avoid "translation-ese". Break up long English clause-stacks into natural Japanese sentences. Cut calque connectives (like translating "Therefore" strictly as したがって instead of a more natural つまり or だから where appropriate).
- **Scope:** This is a "carry-over" translation intended for English-medium programs, so analogies and examples should remain close to the original text without over-localizing the structural progression.

## 3. Handling English Grammar Examples
Since this is a book *about* English grammar:
- **Preserve English Examples:** Words in `\mention{...}`, `\emph{...}`, and formatted examples (e.g., `\ea ... \ex ... \z`) MUST remain in English.
- **Inline Translations:** When an English example is given in the text, provide a parenthetical Japanese translation only if it aids the explanation.
- **Dictionary Definitions:** For the Longman Dictionary quotes, keep the English quote intact and provide the Japanese translation immediately following it.
- **Cross-linguistic references & Glossing:** The text mentions French (`cheveux`); this should be preserved. Crucially, for non-English numbered examples (using `\gll` for interlinear glosses), the word-by-word glosses (the second line) should be translated into Japanese (e.g. `私 持つ 切る 私の-\textsc{pl} 髪-\textsc{pl}.` instead of `I have cut my-\textsc{pl} hairs-\textsc{pl}.`). The free translation line (`\glt`) should also be translated entirely into Japanese (e.g. `\glt 「私は髪を切った」`) since the reader's primary language is now Japanese.

## 4. LaTeX & Formatting Guidelines
- **Macros:** Do NOT translate the names of LaTeX commands (`\chapter`, `\section`, `\enquote`, `\term`, `\mention`).
- **Custom Environments:** For environments like `\begin{tblsframedsymbol}{Learning objectives}{bulb}`, translate the title argument: `\begin{tblsframedsymbol}{学習目標}{bulb}`.
- **Indexing (`\is{...}`):** Retain the exact English index tags so the compilation process and index generation (`makeindex`) do not break. If a localized index is required later, we will append Japanese terms (e.g., `\is{noun@名詞 (noun)}`). For now, leave as `\is{noun}`.
- **Citations:** Leave `\textcite{...}` and `\autocite{...}` unchanged.

## 5. Specific Chapter 1 Challenges & Localization Notes
- **The "Soup" Analogy:** Translates well. Can use スープ (suupu) and perhaps mention 味噌汁 (misoshiru) conceptually if localizing, though sticking to the text's "tea, sauce, porridge, stew, juice" is safest.
- **Wason Selection Task:** The 4-card logic puzzle (3, 8, blue, red) translates directly without issue.
- **Countability Concepts:** Japanese does not grammatically mark plural nouns or countability in the same way English does. Explanations about "two furnitures" vs. "two pencils" need clear, explicit translations emphasizing that this is an *English-specific* structural rule, as a Japanese speaker would just use counters (e.g., 家具を2つ).

## 6. Proposed Workflow
1. **Drafting:** Translate section by section, starting with the Introduction up to "The trouble with (linguistic) definitions".
2. **Reviewing Terminology:** Ensure consistency in the translation of terms like "necessary and sufficient conditions" (必要十分条件).
3. **Translating Exercises:** Carefully translate the quizzes and answer keys, ensuring the "trick" in the English questions is preserved and explained correctly in the Japanese answer keys.
4. **Compilation Check:** Run the translated `.tex` file through `latexmk` to ensure no syntax errors were introduced.