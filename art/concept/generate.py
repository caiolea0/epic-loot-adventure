#!/usr/bin/env python
"""Gera as amostras de conceito visual do TRIBOS via Codex + GPT Image.

Cada entrada de `concepts.json` vira uma sheet 2x2 com quatro enquadramentos
diferentes do mesmo tema — quatro amostras por chamada, em vez de quatro
chamadas. O modelo que dirige a sessão é `gpt-5.6-luna` em esforço `medium`.

Uso: python art/concept/generate.py [--workers 4] [--only style-a-lowpoly,characters]
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GEN_DIR = os.path.join(os.path.expanduser('~'), '.codex', 'generated_images')
OUT_DIR = os.path.join(HERE, 'sheets')
LOG_DIR = os.path.join(OUT_DIR, '_logs')
CODEX = shutil.which('codex') or 'codex'
MODEL = 'gpt-5.6-luna'
EFFORT = 'medium'
QUADRANTS = ['TOP-LEFT', 'TOP-RIGHT', 'BOTTOM-LEFT', 'BOTTOM-RIGHT']


def sheet_prompt(world, negative, sheet):
    shots = '  '.join(
        f'{QUADRANTS[i]}: {shot}.' for i, shot in enumerate(sheet['shots'])
    )
    return (
        'A single 1024x1024 image laid out as a 2x2 grid of four separate concept frames, '
        'each frame filling its own quadrant with a thin dark gutter between them. '
        'The four frames share one world and one art direction but show different subjects. '
        f'{world} '
        f'{sheet["shared"]} '
        f'The four frames are — {shots} '
        f'{negative} '
        'Generate exactly ONE image.'
    )


def run_sheet(world, negative, sheet, timeout=900):
    out = os.path.join(OUT_DIR, f'{sheet["id"]}.png')
    if os.path.exists(out):
        return 'skip'
    os.makedirs(LOG_DIR, exist_ok=True)
    cmd = [CODEX, 'exec', '--skip-git-repo-check', '-s', 'read-only', '-m', MODEL,
           '-c', f'model_reasoning_effort="{EFFORT}"', '-']
    started = time.time()
    try:
        proc = subprocess.run(cmd, input='$imagegen ' + sheet_prompt(world, negative, sheet),
                              capture_output=True, text=True, encoding='utf-8',
                              errors='replace', timeout=timeout, cwd=HERE)
        log = (proc.stdout or '') + (proc.stderr or '')
    except subprocess.TimeoutExpired as e:
        log = f'TIMEOUT {timeout}s\n{e.stdout or ""}'
    with open(os.path.join(LOG_DIR, sheet['id'] + '.log'), 'w', encoding='utf-8') as f:
        f.write(log)
    m = re.search(r'session id:\s*([0-9a-f-]{36})', log)
    if not m:
        return 'no-session'
    pngs = sorted(glob.glob(os.path.join(GEN_DIR, m.group(1), '*.png')), key=os.path.getmtime)
    if not pngs:
        return 'no-image'
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(pngs[-1], out)
    return f'ok {time.time() - started:.0f}s'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--only', default='')
    args = ap.parse_args()

    with open(os.path.join(HERE, 'concepts.json'), encoding='utf-8') as f:
        data = json.load(f)
    only = {x for x in args.only.split(',') if x}
    sheets = [s for s in data['sheets'] if not only or s['id'] in only]

    def one(sheet):
        status = run_sheet(data['world'], data['negative'], sheet)
        print(f'[{time.strftime("%H:%M:%S")}] {sheet["id"]}: {status}', flush=True)
        return status == 'skip' or status.startswith('ok')

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(one, sheets))
    bad = [s['id'] for s, ok in zip(sheets, results) if not ok]
    print('DONE' + (f' — falharam: {", ".join(bad)}' if bad else ''))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
