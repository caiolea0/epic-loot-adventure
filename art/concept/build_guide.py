#!/usr/bin/env python
"""Monta o guia visual em um único arquivo HTML, com as imagens embutidas.

Lê `concepts.json` e as sheets geradas, corta cada sheet nos 4 quadrantes,
comprime em WebP e embute tudo em base64 — o arquivo final abre sozinho e
pode ser mandado por qualquer meio, sem pasta de imagens junto.

Uso: python art/concept/build_guide.py [--out docs/tribos/guia-visual.html] [--width 900]
"""
import argparse
import base64
import io as _io
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def quadrants(img):
    w, h = img.size
    cx, cy = w // 2, h // 2
    return [
        img.crop((0, 0, cx, cy)), img.crop((cx, 0, w, cy)),
        img.crop((0, cy, cx, h)), img.crop((cx, cy, w, h)),
    ]


def embed(img, width, quality=82):
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    buf = _io.BytesIO()
    img.convert('RGB').save(buf, 'WEBP', quality=quality, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()


HEAD = """<!doctype html>
<meta charset="utf-8">
<title>TRIBOS — Guia visual</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  :root{--bg:#14160f;--panel:#1c1f16;--line:#2e3326;--ink:#e8e3d4;--dim:#9a9583;--gold:#d8b24c;--rust:#b4542a}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
       font:16px/1.65 ui-sans-serif,system-ui,'Segoe UI',sans-serif}
  .wrap{max-width:1180px;margin:0 auto;padding:0 24px 96px}
  header{padding:72px 0 28px;border-bottom:1px solid var(--line)}
  h1{font-size:40px;margin:0 0 6px;letter-spacing:-.4px}
  .sub{color:var(--gold);font-size:14px;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:18px}
  .lede{color:var(--dim);max-width:72ch;font-size:17px}
  h2{font-size:13px;letter-spacing:2.5px;text-transform:uppercase;color:var(--gold);
     margin:64px 0 4px;padding-top:24px;border-top:1px solid var(--line)}
  h3{font-size:26px;margin:14px 0 4px}
  .note{color:var(--dim);margin:0 0 22px;max-width:70ch}
  .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
  @media(max-width:760px){.grid{grid-template-columns:1fr}}
  figure{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
  figure img{display:block;width:100%;height:auto;cursor:zoom-in}
  figcaption{padding:12px 14px;font-size:13px;color:var(--dim);border-top:1px solid var(--line)}
  .full{margin-top:18px}
  .full img{width:100%;border:1px solid var(--line);border-radius:10px;cursor:zoom-in}
  details{margin-top:12px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}
  summary{padding:10px 14px;cursor:pointer;font-size:13px;color:var(--dim)}
  details pre{margin:0;padding:0 14px 14px;white-space:pre-wrap;font-size:12px;color:var(--dim);line-height:1.6}
  .world{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--rust);
         border-radius:8px;padding:20px 24px;margin:28px 0}
  .world h4{margin:0 0 8px;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--rust)}
  .ask{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--gold);
       border-radius:8px;padding:20px 24px;margin:30px 0}
  .ask h4{margin:0 0 10px;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--gold)}
  .ask ol{margin:0;padding-left:20px;color:var(--dim)}
  .ask li{margin:7px 0}
  footer{margin-top:72px;padding-top:22px;border-top:1px solid var(--line);color:var(--dim);font-size:13px}
  dialog{border:0;background:transparent;padding:0;max-width:96vw;max-height:96vh}
  dialog::backdrop{background:rgba(0,0,0,.92)}
  dialog img{max-width:96vw;max-height:96vh;display:block}
</style>
<div class="wrap">
<header>
  <div class="sub">TRIBOS &middot; exploração de direção de arte</div>
  <h1>Que cara o jogo vai ter</h1>
  <p class="lede">Amostras geradas para escolher o rumo visual antes de produzir arte de verdade.
  Nada aqui é final — é material para decidir. Clique em qualquer imagem para ampliar.</p>
</header>
"""

FOOT = """
<footer>
  Geradas com GPT Image dirigido por <code>gpt-5.6-luna</code> em esforço médio.
  Pipeline em <code>art/concept/</code> — <code>concepts.json</code> descreve cada quadro,
  <code>generate.py</code> gera, <code>build_guide.py</code> monta esta página.
  Para refazer um painel, apague o PNG em <code>art/concept/sheets/</code> e rode o gerador de novo.
</footer>
</div>
<dialog id="zoom"></dialog>
<script>
  const dlg = document.getElementById('zoom');
  document.addEventListener('click', e => {
    if (e.target.tagName === 'IMG' && e.target.closest('figure,.full')) {
      // A imagem do zoom nasce só no primeiro clique: um <img> sem src na
      // página conta como imagem quebrada.
      let big = dlg.querySelector('img');
      if (!big) { big = document.createElement('img'); big.alt = ''; dlg.appendChild(big); }
      big.src = e.target.src;
      dlg.showModal();
    } else if (e.target === dlg || e.target.closest('dialog')) {
      dlg.close();
    }
  });
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'tribos', 'guia-visual.html'))
    ap.add_argument('--width', type=int, default=900)
    args = ap.parse_args()

    with open(os.path.join(HERE, 'concepts.json'), encoding='utf-8') as f:
        data = json.load(f)

    parts = [HEAD]
    parts.append(f'<div class="world"><h4>O mundo</h4><p>{data["world"]}</p></div>')
    parts.append("""<div class="ask"><h4>O que precisamos decidir</h4><ol>
      <li><b>Direção de arte</b> — qual das quatro (A, B, C, D) o jogo persegue. Decide custo de produção e quanto a arte envelhece.</li>
      <li><b>Leitura da cidade</b> — se a evolução de nível deve aparecer como mais estrutura (chaminés, guindastes, torres) ou como melhor material no mesmo volume.</li>
      <li><b>Personagem</b> — quanto de rosto aparece. Máscara e capuz escondem, facilitam variedade e envelhecem melhor.</li>
      <li><b>Mutação</b> — até onde vai. Hoje está em &quot;crescimento errado&quot;, não em monstro de fantasia.</li>
    </ol></div>""")

    missing = []
    group_atual = None
    for sheet in data['sheets']:
        src = os.path.join(HERE, 'sheets', f'{sheet["id"]}.png')
        if not os.path.exists(src):
            missing.append(sheet['id'])
            continue
        if sheet['group'] != group_atual:
            group_atual = sheet['group']
            parts.append(f'<h2>{group_atual}</h2>')
        img = Image.open(src)
        parts.append(f'<h3>{sheet["label"]}</h3>')
        parts.append(f'<p class="note">{sheet["note"]}</p>')
        parts.append('<div class="grid">')
        for quad, shot in zip(quadrants(img), sheet['shots']):
            legenda = shot[0].upper() + shot[1:]
            parts.append(
                f'<figure><img loading="lazy" src="{embed(quad, args.width)}" alt="">'
                f'<figcaption>{legenda}</figcaption></figure>'
            )
        parts.append('</div>')
        parts.append(
            f'<details><summary>Prompt usado neste painel</summary>'
            f'<pre>{sheet["shared"]}</pre></details>'
        )

    parts.append(FOOT)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))
    kb = os.path.getsize(args.out) / 1024
    print(f'{args.out}  {kb:.0f} KB')
    if missing:
        print('sheets faltando: ' + ', '.join(missing))


if __name__ == '__main__':
    main()
