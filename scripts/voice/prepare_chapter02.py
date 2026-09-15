#!/usr/bin/env python3
"""Prepare exact local Chapter 2 draft inputs and their review manifest.

This does not call a speech service. It extracts the marked speech blocks from
the review document, checks the 5,000-character per-input limit, writes exact
.txt inputs, regenerates the counts and coverage tables in the review copy, and
writes a source/take manifest.

Chapter 2 has no reusable prior audio, so every input is new material.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata

PROJECT = Path(__file__).resolve().parents[2]
ROOT = PROJECT / "supplements/audio/chapter-02-2026-09"
REVIEW = ROOT / "chapter-02-scripts.md"
SOURCE = PROJECT / "chapters/02 standards.tex"
SNAPSHOT = ROOT / "source/chapter-02.tex"
LIMIT = 5000
RESERVE_RATE = .15
# Verified in the account on 2026-09-14; see notes/2026-09-14-ch03-ch02-audio-sizing.md
BALANCE = 44184
BALANCE_DATE = "2026-09-14"

# Brett chose the staged run on 2026-09-14: everything through the model section
# now, the rest after the 1 October renewal. RUN_1 is that scope, in listening order.
RUN_1_LAST = "MO8"

ORDER = [
    "H01", "I01",
    "T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08",
    "E01", "E02", "E03", "E04", "SH01",
    "G01", "G02", "G03", "M01", "G04", "G05",
    "X01", "X02", "X03", "X04", "X05", "X06", "X07", "X08", "X09", "X10", "X11", "X12",
    "MO1", "MO2", "MO3", "MO4", "MO5", "MO6", "MO7", "MO8",
    "N01", "N02", "N03", "N04", "N05", "N06",
    "C01", "Q01", "Q02", "Q03",
]

# Inclusive ranges partition every source line.
COVERAGE = [
    (1, 2, "Chapter title", "adapted", ["H01"]),
    (3, 9, "Samantha Nock epigraph, “pahpowin”", "written reference", []),
    (10, 23, "Learning objectives", "adapted", ["H01"]),
    (24, 32, "Introduction and chapter roadmap", "adapted", ["I01"]),
    (33, 36, "Standard as positive connotation; Standard English as aspiration", "adapted", ["T01"]),
    (37, 40, "VHS and Betamax", "adapted", ["T02"]),
    (41, 42, "Rail gauge and the two measurements", "adapted", ["T03"]),
    (43, 48, "Not superior; sociopolitical marker; codified conventions", "adapted", ["T04"]),
    (49, 54, "Track gauge figure", "figure described in speech", ["T03"]),
    (55, 58, "A4, US Letter, and arbitrariness", "adapted", ["T05"]),
    (59, 60, "Two differences between technology and language standards", "adapted", ["T06"]),
    (61, 62, "Group membership and slang", "adapted", ["T07"]),
    (63, 67, "Clothing analogy and social implications", "adapted", ["T08"]),
    (68, 69, "Section heading; Middlemarch introduced", "adapted", ["E01"]),
    (70, 80, "Middlemarch conversation", "adapted + quotation read", ["E01"]),
    (81, 82, "Correct English is not Standard English; no brief definition", "adapted", ["E01"]),
    (83, 86, "Dialects as local standards; First-Nations English", "adapted", ["E02"]),
    (87, 88, "Standard Englishes in the plural", "adapted", ["E03"]),
    (89, 90, "Not better, formal, or most common; cluster of dialects", "adapted", ["E04"]),
    (91, 102, "Shibboleth box, including the Judges passage", "adapted + quotation read", ["SH01"]),
    (103, 104, "Section heading", "heading", ["G01"]),
    (105, 108, "Hiring in Japan; no explicit grammatical knowledge", "adapted", ["G01"]),
    (109, 110, "Students’ questions; “it sounds right”", "adapted", ["G02"]),
    (111, 114, "What you already know; coffee and toast", "adapted", ["G03"]),
    (115, 118, "Fallacy of monosemy box", "adapted", ["M01"]),
    (119, 122, "What grammatical means; the task set for the reader", "adapted", ["G04"]),
    (123, 131, "Hotdog comic figure", "named; left to written material", ["G04"]),
    (132, 139, "Matthews dictionary definition, both senses", "adapted + quotation read", ["G05"]),
    (140, 144, "Wittgenstein; let’s start with an easy one", "adapted", ["G05"]),
    (145, 151, "Example 2.1 and its analysis", "adapted", ["X01"]),
    (152, 162, "Colorless green ideas, 2.2a and 2.2b", "adapted", ["X02"]),
    (163, 171, "Green ideas figure; Chomsky’s judgment", "adapted; figure left to written material", ["X02"]),
    (172, 173, "Frequency, Pereira, and language models", "adapted", ["X03"]),
    (174, 184, "Jean Paul, very very good (2.3)", "adapted", ["X04"]),
    (185, 193, "Rules in grammar books; beautiful boy (2.4a, 2.4b)", "adapted", ["X05"]),
    (194, 200, "Island constraint (2.5)", "adapted", ["X06"]),
    (201, 206, "Suitcase example (2.6)", "adapted", ["X07"]),
    (207, 213, "Suitcase figure", "figure described in speech", ["X07"]),
    (214, 217, "Which suitcase is unpacked; why people get it wrong", "adapted", ["X07"]),
    (218, 222, "The horse raced past the barn fell (2.7)", "adapted", ["X08"]),
    (223, 233, "I have 30 years (2.8); at the weekend (2.9)", "adapted", ["X09"]),
    (234, 243, "I ain’t no quitter (2.10); Me and Mia (2.11)", "adapted", ["X10"]),
    (244, 249, "Jim and me’s teacher was Geoff (2.12)", "adapted", ["X11"]),
    (250, 253, "Summary of the grammaticality section", "adapted", ["X12"]),
    (254, 259, "Model section; form-and-meaning pairings; mommy sock", "adapted", ["MO1"]),
    (260, 267, "Nishimura code-switching passage", "adapted + quotation read", ["MO2"]),
    (268, 302, "Figure 2.5, speaker groups, drawn in TikZ", "figure described in speech", ["MO3"]),
    (303, 308, "Layers of meaning; going to; Shakespeare", "adapted", ["MO4"]),
    (309, 313, "Four situations for calling something ungrammatical", "adapted", ["MO5"]),
    (314, 317, "It very good; unreliable judgments", "adapted", ["MO6"]),
    (318, 319, "The model restated; language is fluid", "adapted", ["MO7"]),
    (320, 323, "Who learners aim at; standards bend", "adapted", ["MO8"]),
    (324, 327, "Normativity heading and definition", "adapted", ["N01"]),
    (328, 341, "Normative and positive domains table", "adapted; table narrated", ["N02"]),
    (342, 350, "Pullum’s normative examples", "adapted", ["N03"]),
    (351, 363, "Are grammar rules normative; comprehensibility and fluency", "adapted", ["N04"]),
    (364, 369, "Audience", "adapted", ["N05"]),
    (370, 373, "Cook quotation; facilitation goes two ways", "adapted + quotation read", ["N06"]),
    (374, 377, "Conclusion", "adapted", ["C01"]),
    (378, 383, "Cross-reference note", "written reference", []),
    (384, 400, "Ten exercises", "adapted", ["Q01"]),
    (401, 416, "Ten answers", "adapted", ["Q02"]),
    (417, 426, "Five discussion questions", "adapted; no supplied key", ["Q03"]),
]

PAUSE_AFTER = ["G04", "X04", "X11", "Q01", "Q03"]
ANSWERS = {"Q01": "Q02"}


def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode("utf-8")).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def relative(path):
    return str(path.relative_to(PROJECT))


def replace_region(text, name, body):
    pattern = rf"<!-- generated:{name} -->\n.*?\n<!-- /generated:{name} -->"
    updated, n = re.subn(pattern, lambda _: f"<!-- generated:{name} -->\n\n{body}\n\n<!-- /generated:{name} -->",
                         text, flags=re.S)
    assert n == 1, f"Missing or repeated {name} region"
    return updated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Read-only checks; write nothing")
    args = parser.parse_args()

    state_path = ROOT / "review-state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    if state.get("status") == "in_review":
        raise SystemExit("The file is under human review. Wait for Done Reviewing before regenerating it.")

    prior_path = ROOT / "manifest.json"
    prior = json.loads(prior_path.read_text()) if prior_path.exists() else {}
    if not args.check and (prior.get("takes") or prior.get("script_status") == "approved"):
        raise SystemExit("An approved/generated version exists; preserve it before preparing a revision.")

    assert SOURCE.read_bytes() == SNAPSHOT.read_bytes(), "The chapter changed; inspect source differences."
    lines = SNAPSHOT.read_text().splitlines(keepends=True)

    text = REVIEW.read_text()
    assert text.startswith("# "), "Review files must not begin with YAML frontmatter."
    assert "@@" not in text, "Resolve preparation placeholders."

    pairs = re.findall(r"<!-- speech:([A-Z]{1,2}[0-9]{1,2}) -->\n(.*?)\n<!-- /speech -->", text, re.S)
    assert [k for k, _ in pairs] == ORDER, "Inputs missing, repeated, or reordered"
    headings = dict(re.findall(r"^### ([A-Z]{1,2}[0-9]{1,2}) · (.+)$", text, re.M))

    output = {}
    for key, value in pairs:
        assert value == value.strip() and value == unicodedata.normalize("NFC", value), key
        assert not re.search(r"\{(?:>>|==|\+\+|--|~~|#)|<!--|[<>]|\\[A-Za-z]", value), key
        assert 0 < len(value) <= LIMIT, (key, len(value))
        output[key] = value

    split = ORDER.index(RUN_1_LAST) + 1
    run1_ids, run2_ids = ORDER[:split], ORDER[split:]
    run1_chars = sum(len(output[k]) for k in run1_ids)
    run2_chars = sum(len(output[k]) for k in run2_ids)
    run1_reserve = math.ceil(run1_chars * RESERVE_RATE)
    run1_ceiling = math.ceil((run1_chars + run1_reserve) / 1000) * 1000
    run1_headroom = BALANCE - run1_chars - run1_reserve

    characters = sum(len(s) for s in output.values())
    words = sum(len(s.split()) for s in output.values())
    reserve = math.ceil(characters * RESERVE_RATE)
    headroom = BALANCE - characters - reserve
    ceiling = math.ceil((characters + reserve) / 1000) * 1000
    fits = (characters + reserve) <= BALANCE
    allowance_status = "approved" if prior.get("budget", {}).get("generation_authorized") else "proposed"

    # Chapter 1's accepted readings measured 133.4-154.6 spoken words per minute.
    rates = (154.6, 133.4)
    minutes = [words / rates[0], words / rates[1]]

    budget_lines = [
        "| Item | Credits |", "| --- | ---: |",
        f"| First takes: exact submitted-character count ({len(output)} inputs) | **{characters:,}** |",
        f"| Targeted repair reserve (15%, rounded up) | {reserve:,} |",
        f"| **{allowance_status.capitalize()} chapter ceiling** | **{ceiling:,}** |",
        f"| Verified account balance, {BALANCE_DATE} | {BALANCE:,} |",
        f"| Headroom after first takes and reserve | {headroom:,} |",
        "",
        f"The scripts contain **{words:,} words** across **{len(output)} inputs**. At the word rates measured "
        f"in the two accepted pilot readings, they would run approximately "
        f"**{round(minutes[0])}–{round(minutes[1])} minutes**, before learner-controlled pauses. "
        "Lists, the Japanese passage, and final pauses may change that estimate.",
        "",
        f"**Staged run, chosen by Brett on 2026-09-14.** The whole chapter would need "
        f"{characters + reserve:,} credits with a full reserve, against {BALANCE:,} available, so it is split. "
        f"**Run 1 is H01 through {RUN_1_LAST}**, {len(run1_ids)} inputs and **{run1_chars:,} credits** of first takes, "
        f"with a {run1_reserve:,} reserve inside a {run1_ceiling:,} ceiling, leaving {run1_headroom:,} of the "
        f"current balance untouched. **Run 2 is the remaining {len(run2_ids)} inputs**, {run2_chars:,} credits of "
        f"first takes, after the cycle renews on 1 October.",
        "",
        "Counts include punctuation, whitespace, and internal paragraph breaks. Files have no added final "
        "newline. The 15% reserve is a planning allowance, not a measured failure rate or a target to spend.",
        "",
        "| Input | Subject | Submitted characters | Spoken words |", "| --- | --- | ---: | ---: |",
    ]
    budget_lines.extend(
        f"| {k} | {headings[k]} | {len(output[k]):,} | {len(output[k].split()):,} |" for k in ORDER)

    table = ["| Source lines | Material | Treatment | Input |", "| --- | --- | --- | --- |"]
    covered = []
    for lo, hi, label, disposition, ids in COVERAGE:
        table.append(f"| {lo}–{hi} | {label} | {disposition} | {', '.join(ids) or 'Written reference below'} |")
        for line_no in range(lo, hi + 1):
            content = lines[line_no - 1].strip()
            specific = "blank" if not content else "inactive comment" if content.startswith("%") else disposition
            covered.append({"line": line_no, "block": label, "disposition": specific, "inputs": ids})
    assert [x["line"] for x in covered] == list(range(1, len(lines) + 1)), "Coverage must partition every line"

    text = replace_region(text, "counts", "\n".join(budget_lines))
    text = replace_region(text, "coverage", "\n".join(table))

    if args.check:
        print(f"inputs {len(output)}  characters {characters:,}  words {words:,}")
        print(f"run 1 (H01-{RUN_1_LAST}, {len(run1_ids)}): {run1_chars:,} + {run1_reserve:,} "
              f"= {run1_ceiling:,} ceiling; leaves {run1_headroom:,}")
        print(f"run 2 ({len(run2_ids)}, after renewal): {run2_chars:,}")
        return

    for key, value in output.items():
        (ROOT / "inputs" / f"{key}.txt").write_text(value)
    (ROOT / "transcript.txt").write_text("\n\n".join(output.values()) + "\n")
    REVIEW.write_text(text)

    manifest = {
        "schema_version": 1,
        "prepared_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "review_file": relative(REVIEW),
        "review_sha256": digest(text),
        "script_status": "draft_awaiting_review",
        "source": {
            "path": relative(SOURCE), "snapshot": relative(SNAPSHOT),
            "sha256": digest(SNAPSHOT.read_bytes()), "lines": len(lines),
        },
        "voice_name": "Audio textbook Brett",
        "model_name": "Eleven Multilingual v2",
        "settings": {"speed": 1, "stability": 0.5, "similarity": 0.75, "style": 0, "speaker_boost": True},
        "budget": {
            "status": allowance_status,
            "generation_authorized": False,
            "rate_credits_per_character": 1,
            "rate_url": "https://elevenlabs.io/pricing",
            "first_take_credits": characters,
            "repair_fraction": RESERVE_RATE,
            "repair_reserve": reserve,
            "proposed_ceiling": ceiling,
            "verified_account_balance": BALANCE,
            "balance_verified_on": BALANCE_DATE,
            "balance_source": "ElevenLabs account, subscription pane, read in browser",
            "cycle_renews": "2026-10-01",
            "headroom_after_reserve": headroom,
            "fits_current_balance": fits,
            "max_targeted_repairs_per_defective_passage": 2,
            "staging": {
                "chosen_by": "Brett",
                "chosen_on": "2026-09-14",
                "statement": "Stop after the model section.",
                "run_1": {
                    "ids": run1_ids, "last": RUN_1_LAST, "inputs": len(run1_ids),
                    "first_take_credits": run1_chars, "repair_reserve": run1_reserve,
                    "ceiling": run1_ceiling, "headroom_after_reserve": run1_headroom,
                    "status": "scope_chosen; script not yet reviewed; generation NOT authorized",
                },
                "run_2": {
                    "ids": run2_ids, "inputs": len(run2_ids),
                    "first_take_credits": run2_chars,
                    "status": "deferred to the cycle renewing 2026-10-01",
                },
            },
        },
        "spoken_words": words,
        "estimated_minutes": [round(minutes[0], 1), round(minutes[1], 1)],
        "duration_basis": "Word rates measured in accepted pilot Readings A and B",
        "reused_audio": [],
        "listening_order": ORDER,
        "pause_after": PAUSE_AFTER,
        "answer_segments": ANSWERS,
        "segments": [
            {
                "id": k, "subject": headings[k], "characters": len(output[k]),
                "words": len(output[k].split()), "sha256": digest(output[k]),
                "input_file": relative(ROOT / "inputs" / f"{k}.txt"),
            } for k in ORDER
        ],
        "line_dispositions": covered,
        "takes": [],
        "production_status": "not_started",
        "open_questions": [
            "MO2: whether to read the Japanese aloud or describe it (marked in the review copy).",
            "SH01: audio permission for the New International Version passage in Judges.",
            "TESL: confirm whether it is spoken as a word or spelled out.",
        ],
    }
    write_json(prior_path, manifest)
    print(f"Wrote {len(output)} inputs, transcript, and manifest.")
    print(f"whole chapter {characters:,}  balance {BALANCE:,}")
    print(f"run 1 (H01-{RUN_1_LAST}, {len(run1_ids)} inputs): {run1_chars:,} + {run1_reserve:,} reserve "
          f"= ceiling {run1_ceiling:,}; leaves {run1_headroom:,}")
    print(f"run 2 ({len(run2_ids)} inputs, after 2026-10-01): {run2_chars:,}")


if __name__ == "__main__":
    main()
