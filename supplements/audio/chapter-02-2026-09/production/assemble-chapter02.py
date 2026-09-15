#!/usr/bin/env python3
"""Assemble the unfinished Chapter 2 companion from verified takes, locally.

Chapter 2 is not complete. X01 is truncated and the closing run (N01-Q03) was
never generated. This builds an honest partial release: the 40 verified takes in
listening order, a spoken note where X01 belongs, and written material that
carries the missing text in full.

No speech service is called. Run with --allow-missing-note to assemble before
the spoken gap note has been downloaded (silence is substituted and the output
is marked provisional).
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[2]
OUT = ROOT / 'final'
QA = ROOT / 'qa'
RAW = ROOT / 'raw'
RATE = 44100
TARGET = -24.5          # same loudness target as the accepted Chapter 1 master
PEAK_CEILING = -1.6     # true-peak headroom, as Chapter 1
GAP_ID = 'GAP01'
MISSING_MID = 'X01'
MISSING_TAIL = ['N01', 'N02', 'N03', 'N04', 'N05', 'N06', 'C01', 'Q01', 'Q02', 'Q03']


def command(args):
    return subprocess.run(args, capture_output=True, check=True)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_audio(path: Path) -> np.ndarray:
    out = command(['ffmpeg', '-v', 'error', '-i', str(path), '-ac', '1',
                   '-ar', str(RATE), '-f', 'f32le', '-']).stdout
    samples = np.frombuffer(out, dtype='<f4').copy()
    assert len(samples) and np.isfinite(samples).all(), path
    return samples


def write_wav(path: Path, samples: np.ndarray) -> None:
    command(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(RATE),
             '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', str(path)],
            ) if False else None
    proc = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(RATE),
                           '-ac', '1', '-i', 'pipe:0', '-c:a', 'pcm_s16le', str(path)],
                          input=samples.astype('<f4').tobytes(), capture_output=True)
    assert proc.returncode == 0, proc.stderr.decode()[:400]


def measure(path: Path) -> dict:
    out = command(['ffmpeg', '-v', 'info', '-i', str(path), '-af',
                   'loudnorm=print_format=json', '-f', 'null', '-']).stderr.decode()
    blob = out[out.rindex('{'):out.rindex('}') + 1]
    d = json.loads(blob)
    return {'input_i': float(d['input_i']), 'input_tp': float(d['input_tp'])}


def clock(seconds: float) -> str:
    seconds = int(round(seconds))
    return f'{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}'


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--allow-missing-note', action='store_true')
    args = ap.parse_args()

    man = json.loads((ROOT / 'manifest.json').read_text())
    takes = {t['id']: t for t in man['takes']}
    headings = {s['id']: s['subject'] for s in man['segments']}
    order_all = man['budget']['staging']['run_1']['ids']

    complete = [i for i in order_all if takes[i].get('complete')]
    assert MISSING_MID not in complete, 'X01 is supposed to be the known gap'
    assert len(complete) == 40, f'expected 40 verified takes, found {len(complete)}'

    note_path = RAW / f'{GAP_ID}-take-01.mp3'
    have_note = note_path.exists()
    if not have_note and not args.allow_missing_note:
        raise SystemExit(f'Missing {note_path}. Re-export it, or pass --allow-missing-note.')

    for d in (OUT, OUT / 'tracks', OUT / 'wav', QA):
        d.mkdir(parents=True, exist_ok=True)

    # Listening order: the verified takes, with the spoken note standing where X01 belongs.
    sequence = []
    for i in order_all:
        if i == MISSING_MID:
            sequence.append(GAP_ID)
        elif i in complete:
            sequence.append(i)

    entries, master_parts, cursor = [], [], 0
    for number, ident in enumerate(sequence, 1):
        if ident == GAP_ID:
            title = 'A note on what is missing'
            text = (ROOT / 'inputs' / 'GAP01.txt').read_text()
            if have_note:
                samples = read_audio(note_path)
                source = note_path
            else:
                samples = np.zeros(round(1.5 * RATE), dtype=np.float32)
                source = None
        else:
            take = takes[ident]
            source = PROJECT / take['file']
            assert digest(source) == take['sha256'], ident
            title = headings[ident]
            text = (ROOT / 'inputs' / f'{ident}.txt').read_text()
            samples = read_audio(source)

        wav_path = OUT / 'wav' / f'{number:02d}-{ident}.wav'
        mp3_path = OUT / 'tracks' / f'{number:02d}-{ident}.mp3'

        gain = 0.0
        if samples.any():
            ramp = round(.005 * RATE)
            if np.sqrt(np.mean(samples[:ramp] ** 2)) < .0032:
                samples[:ramp] *= np.linspace(0, 1, ramp)
            if np.sqrt(np.mean(samples[-ramp:] ** 2)) < .0032:
                samples[-ramp:] *= np.linspace(1, 0, ramp)
            probe = QA / f'{ident}-pre-gain.wav'
            write_wav(probe, samples)
            before = measure(probe)
            gain = min(TARGET - before['input_i'], PEAK_CEILING - before['input_tp'])
            samples = samples * (10 ** (gain / 20))
            probe.unlink(missing_ok=True)

        write_wav(wav_path, samples)
        levels = measure(wav_path) if samples.any() else {'input_i': -70.0, 'input_tp': -70.0}
        assert levels['input_tp'] <= -1.49, (ident, levels)

        command(['ffmpeg', '-v', 'error', '-y', '-i', str(wav_path), '-c:a', 'libmp3lame',
                 '-b:a', '192k', '-metadata', f'title={title}', '-metadata',
                 'artist=Brett Reynolds', '-metadata',
                 'album=Language Landscapes — Chapter 2 (unfinished)',
                 '-metadata', f'track={number}/{len(sequence)}', str(mp3_path)])

        duration = len(samples) / RATE
        gap = 1.5 if ident in man.get('pause_after', []) else .6
        if number == len(sequence):
            gap = .5
        entries.append({'number': number, 'id': ident, 'title': title,
                        'start_seconds': cursor / RATE, 'duration_seconds': duration,
                        'following_silence_seconds': gap, 'text': text,
                        'is_note': ident == GAP_ID,
                        'mp3': str(mp3_path.relative_to(OUT)),
                        'loudness': levels, 'gain_db': round(gain, 2),
                        'source': str(source.relative_to(PROJECT)) if source else None,
                        'mp3_sha256': digest(mp3_path)})
        master_parts += [samples, np.zeros(round(gap * RATE), dtype=np.float32)]
        cursor += len(samples) + round(gap * RATE)
        print(f'{number:02d}/{len(sequence)} {ident}: {duration:6.2f}s  {levels["input_i"]:.2f} LUFS', flush=True)

    master = np.concatenate(master_parts)
    total = len(master) / RATE
    write_wav(OUT / 'chapter-02.wav', master)
    command(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'chapter-02.wav'),
             '-c:a', 'libmp3lame', '-b:a', '192k',
             '-metadata', 'title=Language Landscapes — Chapter 2 (unfinished)',
             '-metadata', 'artist=Brett Reynolds', str(OUT / 'chapter-02.mp3')])

    # m4b with chapter marks
    meta = [';FFMETADATA1', 'title=Language Landscapes — Chapter 2 (unfinished)',
            'artist=Brett Reynolds']
    for e in entries:
        s = int(e['start_seconds'] * 1000)
        t = int((e['start_seconds'] + e['duration_seconds'] + e['following_silence_seconds']) * 1000)
        meta += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={s}', f'END={t}',
                 'title=' + e['title'].replace('=', ' ')]
    meta_path = QA / 'chapters.txt'
    meta_path.write_text('\n'.join(meta) + '\n')
    command(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'chapter-02.wav'),
             '-i', str(meta_path), '-map_metadata', '1', '-c:a', 'aac', '-b:a', '96k',
             '-f', 'mp4', str(OUT / 'chapter-02.m4b')])

    missing_note = ('This recording is unfinished. The first worked example (section 2.3 of the '
                    'chapter) is not recorded, and neither is the closing material on normativity, '
                    'audience, the conclusion, or the exercises. All of it is present in the written '
                    'transcript below.')

    # plain-text transcript, carrying the unrecorded text in full
    lines = ['Language Landscapes — Chapter 2: Standards, Standard Englishes, and what to teach',
             'Adapted narrated companion. AI narration using the author’s approved voice.', '',
             'UNFINISHED RECORDING. ' + missing_note, '']
    for e in entries:
        lines += [f'[{clock(e["start_seconds"])}] {e["number"]:02d}. {e["title"]}', '', e['text'], '']
        if e['id'] == GAP_ID:
            lines += ['--- not recorded: the first worked example ---', '',
                      (ROOT / 'inputs' / 'X01.txt').read_text(), '']
    lines += ['--- not recorded: normativity, audience, conclusion, and exercises ---', '']
    for i in MISSING_TAIL:
        p = ROOT / 'inputs' / f'{i}.txt'
        if p.exists():
            lines += [f'{i}. {headings.get(i, "")}', '', p.read_text(), '']
    (OUT / 'chapter-02-transcript.txt').write_text('\n'.join(lines) + '\n')

    (OUT / 'chapter-02.m3u').write_text('#EXTM3U\n' + ''.join(
        f'#EXTINF:{round(e["duration_seconds"])},{e["number"]:02d}. {e["title"]}\n{e["mp3"]}\n'
        for e in entries))

    (OUT / 'track-index.json').write_text(json.dumps({
        'chapter': 2, 'status': 'unfinished', 'total_seconds': total,
        'total_hhmmss': clock(total), 'track_count': len(entries),
        'recorded_segments': len(complete), 'planned_segments': 51,
        'not_recorded': [MISSING_MID] + MISSING_TAIL,
        'built_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'spoken_note_included': have_note, 'tracks': entries}, indent=1) + '\n')

    (OUT / 'README.txt').write_text(
        'Language Landscapes — Chapter 2 audio companion (unfinished)\n\n'
        + missing_note + '\n\n'
        f'Recorded: {len(complete)} of 51 planned segments, {clock(total)} of audio.\n'
        'Narration is AI-generated using the author’s approved voice clone.\n'
        'Text is adapted from the chapter for listening; the book remains the source.\n'
        'Language Landscapes is published by Language Science Press under CC BY 4.0.\n')

    print(f'\ntotal {clock(total)}  tracks {len(entries)}  spoken note included: {have_note}')
    print(f'master: {OUT / "chapter-02.mp3"}')


if __name__ == '__main__':
    main()
