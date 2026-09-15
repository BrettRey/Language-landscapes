#!/usr/bin/env python3
"""Build the Chapter 2 companion page and reference page from track-index.json.

Mirrors the Chapter 1 page, with the unfinished state stated plainly at the top
and the unrecorded text carried in full so the page is complete even though the
recording is not.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'final'
TAG = 'language-landscapes-chapter-02-audio-2026-09'
BASE = f'https://github.com/BrettRey/brettreynolds.github.io/releases/download/{TAG}'
CSS = ("body{max-width:70ch;margin:3rem auto;padding:0 1.2rem;font:18px/1.65 Georgia,serif;"
       "color:#17252a;background:#fffdf8}h1,h2,h3,nav,audio{font-family:system-ui,sans-serif}"
       "h1{font-size:2rem;line-height:1.2}h2{margin-top:3rem;font-size:1.3rem}a{color:#176164}"
       "nav{font-size:.9rem}audio{width:100%}.tools{font:14px/1.5 system-ui,sans-serif}"
       "table{border-collapse:collapse;width:100%;font-size:.88rem}th,td{border:1px solid #bbb;"
       "padding:.4rem;text-align:left}blockquote{border-left:3px solid #b0c2bd;margin-left:0;"
       "padding-left:1rem}.unfinished{background:#fdf3e3;border-left:3px solid #c99a3d;"
       "padding:.8rem 1rem;font:15px/1.6 system-ui,sans-serif}.missing{background:#f4f4f2;"
       "border-left:3px solid #999;padding:.8rem 1rem;font-size:.95rem}")


def clock(seconds: float) -> str:
    s = int(round(seconds))
    return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def paras(text: str) -> str:
    return '\n'.join(f'<p>{html.escape(p.strip())}</p>'
                     for p in text.split('\n\n') if p.strip())


def main() -> None:
    idx = json.loads((OUT / 'track-index.json').read_text())
    man = json.loads((ROOT / 'manifest.json').read_text())
    headings = {s['id']: s['subject'] for s in man['segments']}
    tracks = idx['tracks']

    banner = (
        '<div class="unfinished"><strong>This recording is unfinished.</strong> It runs from the '
        'start of the chapter to the end of the model of grammaticality, '
        f'{clock(idx["total_seconds"])} in all. The chapter’s first worked example is not '
        'recorded, and neither is the closing material on normativity, audience, the conclusion, '
        'or the exercises. Everything missing from the audio is printed in full on this page, '
        'marked where it belongs. The rest will be recorded and added.</div>')

    head = [f'<!doctype html><html lang="en"><meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width,initial-scale=1">',
            '<title>Language Landscapes – Chapter 2 audio and transcript</title>',
            f'<link rel="canonical" href="https://brettreynolds.ca/language-landscapes/audio/chapter-02/">',
            f'<style>{CSS}</style><body>',
            '<p class="tools"><a href="../../">Language Landscapes</a> · '
            '<a href="https://brettrey.github.io/TESL5002/">TESL 5002</a></p>',
            '<h1>Chapter 2</h1>',
            '<p>Standards, Standard Englishes, and what to teach</p>',
            '<p class="tools">Brett Reynolds · Adapted narrated companion · '
            'AI narration using the author’s approved voice</p>',
            banner,
            f'<audio id="chapter-audio" controls preload="none" src="{BASE}/chapter-02.mp3"></audio>',
            f'<p class="tools"><a href="{BASE}/chapter-02.m4b">Audiobook with {len(tracks)} chapters</a> '
            f'· <a href="{BASE}/chapter-02.mp3">Complete MP3</a> '
            '· <a href="chapter-02.m3u">Track playlist</a> '
            '· <a href="chapter-02-transcript.txt">Text transcript</a> '
            '· <a href="chapter-02-reference.html">Written references and examples</a></p>',
            '<h2>Sections</h2><nav><ol>']
    for t in tracks:
        head.append(f'<li><a href="#section-{t["number"]}">{html.escape(t["title"])}</a> '
                    f'<span class="tools">{clock(t["start_seconds"])}</span></li>')
    head.append('</ol></nav>')

    body = []
    for t in tracks:
        body.append(f'<section id="section-{t["number"]}">'
                    f'<h2>{t["number"]:02d}. {html.escape(t["title"])}</h2>')
        body.append(f'<p class="tools"><button type="button" data-seek="{t["start_seconds"]:.5f}">'
                    f'Play from {clock(t["start_seconds"])}</button> · '
                    f'<a href="{BASE}/{t["mp3"].replace("tracks/", "")}">Section MP3</a></p>')
        body.append(paras(t['text']))
        if t['is_note']:
            body.append('<div class="missing"><p><strong>Not recorded yet.</strong> '
                        'The chapter’s first worked example and its discussion follow here '
                        'in the book. The text is printed below so you can read what the '
                        'recording skips.</p>'
                        + paras((ROOT / 'inputs' / 'X01.txt').read_text()) + '</div>')
    tail_ids = idx['not_recorded'][1:]
    body.append('<h2>Not recorded yet: normativity, audience, the conclusion, and the exercises</h2>')
    body.append('<div class="missing"><p>The closing third of the chapter has not been narrated. '
                'Its text follows in full.</p>')
    for i in tail_ids:
        p = ROOT / 'inputs' / f'{i}.txt'
        if p.exists():
            body.append(f'<h3>{html.escape(headings.get(i, i))}</h3>')
            body.append(paras(p.read_text()))
    body.append('</div>')

    script = ('<script>const a=document.getElementById("chapter-audio");'
              'document.querySelectorAll("[data-seek]").forEach(b=>b.addEventListener("click",()=>{'
              'a.currentTime=parseFloat(b.dataset.seek);a.play();}));</script>')
    (OUT / 'chapter-02-transcript.html').write_text('\n'.join(head + body) + script + '\n')

    # written references page
    scripts_md = (ROOT / 'chapter-02-scripts.md').read_text()
    start = scripts_md.index('## Written references and production notes')
    ref = scripts_md[start:]
    ref_html = ['<!doctype html><html lang="en"><meta charset="utf-8">',
                '<meta name="viewport" content="width=device-width,initial-scale=1">',
                '<title>Language Landscapes – Chapter 2 written references</title>',
                f'<style>{CSS}</style><body>',
                '<p class="tools"><a href="./">Chapter 2 audio</a> · '
                '<a href="../../">Language Landscapes</a></p>',
                '<h1>Chapter 2: written references</h1>',
                '<p class="tools">What the narration leaves to the page: the epigraph, the figures, '
                'the sources, and the pronunciation decisions.</p>']
    for line in ref.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith('### '):
            ref_html.append(f'<h2>{html.escape(s[4:])}</h2>')
        elif s.startswith('## '):
            continue
        elif s.startswith('| '):
            cells = [c.strip() for c in s.strip('|').split('|')]
            if set(''.join(cells)) <= set('-: '):
                continue
            ref_html.append('<p class="tools">' + ' — '.join(html.escape(c) for c in cells) + '</p>')
        elif s.startswith('- '):
            ref_html.append(f'<p>• {html.escape(s[2:])}</p>')
        else:
            ref_html.append(f'<p>{html.escape(s)}</p>')
    (OUT / 'chapter-02-reference.html').write_text('\n'.join(ref_html) + '\n')

    print(f'page   : {OUT / "chapter-02-transcript.html"}')
    print(f'refs   : {OUT / "chapter-02-reference.html"}')
    print(f'tracks : {len(tracks)}   total {clock(idx["total_seconds"])}   '
          f'spoken note included: {idx["spoken_note_included"]}')


if __name__ == '__main__':
    main()
