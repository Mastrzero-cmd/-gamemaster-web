#!/usr/bin/env python3
"""Genera el logo GameMaster v2 (SVG vectorial, texto convertido a trazos) a partir de Bangers (OFL).
Uso: python3 generar_logo.py ../assets/logo"""
import sys, os, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
BB=[1e9,1e9,-1e9,-1e9]
BB_ON=[False]
FONT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'Bangers-Regular.ttf')
font = TTFont(FONT); gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
SKEW = 0.20  # ~ -11.3 grados

def text_path(txt, size, x, y, track=0.0):
    """devuelve (d, ancho). Itálica por sesgo; y = línea base."""
    s = size / upm; pen_x = 0; ds = []
    for ch in txt:
        g = cmap[ord(ch)]; gl = gs[g]
        sp = SVGPathPen(gs)
        # x' = x + SKEW*(y) con y hacia arriba; en SVG y se invierte
        tp = TransformPen(sp, (s, 0, SKEW * s, -s, x + pen_x * s, y))
        gl.draw(tp); ds.append(sp.getCommands())
        bp = BoundsPen(gs); gl.draw(TransformPen(bp, (s, 0, SKEW * s, -s, x + pen_x * s, y)))
        if bp.bounds and BB_ON[0]:
            b = bp.bounds; BB[0]=min(BB[0],b[0]);BB[1]=min(BB[1],b[1]);BB[2]=max(BB[2],b[2]);BB[3]=max(BB[3],b[3])
        pen_x += gl.width + track * upm
    return ' '.join(ds), pen_x * s

def fit_line(txt, width, x0, y, track=0.02):
    _, w = text_path(txt, 100, 0, 0, track)
    size = 100 * width / w
    BB[:] = [1e9, 1e9, -1e9, -1e9]; BB_ON[0] = True
    d, w2 = text_path(txt, size, x0, y, track)
    BB_ON[0] = False
    return d, list(BB)

THEMES = {
  'oscuro': dict(top='#d6fbff', mid='#3fdcff', bot='#2a6bff', outline='#0a1148', off='#ff3b7f', glitch1='#ff4a5e', glitch2='#5fe6ff', mono=None),
  'claro':  dict(top='#3aa8ff', mid='#1f55f0', bot='#1b2fc0', outline='#070b2a', off='#ff2e78', glitch1='#ff3b57', glitch2='#2f6bff', mono=None),
  'mono-blanco': dict(mono='#ffffff'),
  'mono-noche':  dict(mono='#0a1148'),
}

def bars(rnd, bb, side, n, colors, lmin, lmax, hmin, hmax, gap=0):
    """barras horizontales sesgadas a un lado de la línea (pincel seco / glitch)"""
    out = []; y0, y1 = bb[1], bb[3]
    for i in range(n):
        L = rnd.uniform(lmin, lmax); h = rnd.uniform(hmin, hmax)
        y = rnd.uniform(y0 + 4, y1 - h - 4); sk = h * SKEW
        edge = (bb[2] - (y - y0) * SKEW * 0 + gap) if side == 'r' else bb[0] - gap
        x = edge - 6 if side == 'r' else edge - L + 6
        out.append(f'<path d="M{x+sk:.1f} {y:.1f}h{L:.1f}l{-sk:.1f} {h:.1f}h{-L:.1f}z" fill="{rnd.choice(colors)}"/>')
    return ''.join(out)

def swoosh(x0, x1, y, th):
    """pincelada curva cónica con extremo seco a la izquierda"""
    d = x1 - x0
    return (f'M{x0} {y+th*1.3:.1f} C{x0+d*.28:.1f} {y+th*.2:.1f} {x0+d*.62:.1f} {y-th*1.2:.1f} {x1} {y-th*1.6:.1f} '
            f'C{x0+d*.75:.1f} {y-th*.5:.1f} {x0+d*.42:.1f} {y+th*.9:.1f} {x0+th*2.4:.1f} {y+th*1.55:.1f} '
            f'L{x0+th*1.6:.1f} {y+th*1.2:.1f} L{x0+th*1.0:.1f} {y+th*1.6:.1f} L{x0+th*.6:.1f} {y+th*1.15:.1f} L{x0+th*.2:.1f} {y+th*1.45:.1f}Z')

def build(kind, theme, uid):
    T = THEMES[theme]; mono = T.get('mono'); rnd = random.Random(11)
    if kind == 'completo':
        d1, b1 = fit_line('GAME', 700, 180, 300, 0.03)
        d2, b2 = fit_line('MASTER', 840, 110, 560, 0.02)
        lines = [(d1, b1), (d2, b2)]; sw = (130, 930, 680, 50)
    elif kind == 'horizontal':
        d1, b1 = fit_line('GAME MASTER', 1360, 110, 240, 0.02)
        lines = [(d1, b1)]; sw = (170, 1400, 312, 21)
    else:
        d1, b1 = fit_line('GM', 520, 130, 400, 0.04)
        lines = [(d1, b1)]; sw = (110, 640, 510, 38)
    texts = [d for d, _ in lines]; swd = swoosh(*sw)
    x0 = min(b[0] for _, b in lines); x1 = max(b[2] for _, b in lines)
    y0 = min(b[1] for _, b in lines); y1 = sw[2] + sw[3] * 1.8
    pad = 70; vb = (x0 - pad - 40, y0 - pad * .7, (x1 - x0) + 2 * pad + 110, (y1 - y0) + pad * 1.5)
    defs = ''; body = ''
    if mono:
        body += ''.join(f'<path d="{d}" fill="{mono}"/>' for d in texts) + f'<path d="{swd}" fill="{mono}"/>'
    else:
        for i, (_, b) in enumerate(lines):
            defs += (f'<linearGradient id="g{uid}{i}" gradientUnits="userSpaceOnUse" x1="0" y1="{b[1]:.0f}" x2="0" y2="{b[3]:.0f}">'
                     f'<stop offset="0" stop-color="{T["top"]}"/><stop offset=".5" stop-color="{T["mid"]}"/><stop offset="1" stop-color="{T["bot"]}"/></linearGradient>')
        defs += f'<linearGradient id="gs{uid}" x1="0" x2="1"><stop offset="0" stop-color="{T["mid"]}"/><stop offset="1" stop-color="{T["top"]}"/></linearGradient>'
        defs += f'<clipPath id="c{uid}">' + ''.join(f'<path d="{d}"/>' for d in texts) + '</clipPath>'
        # glitch y pincel seco (detrás)
        for d, b in lines:
            body += bars(rnd, b, 'r', 5, [T['glitch1'], T['glitch2'], T['glitch1']], 50, 190, 4, 8, gap=10)
            body += bars(rnd, b, 'l', 4, [T['glitch1'], T['glitch2']], 40, 150, 4, 7, gap=14)
            body += bars(rnd, b, 'r', 4, [T['mid'], T['top']], 18, 70, 5, 10, gap=-6)
        # 0) placa noche exterior (v3): separa el logo de campos azules y evita que se funda
        if theme == 'oscuro':
            body += f'<g fill="#05071f" stroke="#05071f" stroke-width="30" stroke-linejoin="round" transform="translate(6 5)">' + ''.join(f'<path d="{d}"/>' for d in texts) + f'<path d="{swd}"/></g>'
        # 1) contorno desplazado magenta-rojo
        body += f'<g fill="{T["off"]}" stroke="{T["off"]}" stroke-width="13" stroke-linejoin="round" transform="translate(11 9)">'
        body += ''.join(f'<path d="{d}"/>' for d in texts) + f'<path d="{swd}"/></g>'
        # 2) contorno azul noche
        body += f'<g fill="{T["outline"]}" stroke="{T["outline"]}" stroke-width="9" stroke-linejoin="round">'
        body += ''.join(f'<path d="{d}"/>' for d in texts) + f'<path d="{swd}"/></g>'
        # 3) relleno degradado
        for i, d in enumerate(texts): body += f'<path d="{d}" fill="url(#g{uid}{i})"/>'
        body += f'<path d="{swd}" fill="url(#gs{uid})"/>'
        # 4) scanlines suaves sobre las letras
        body += f'<g clip-path="url(#c{uid})" opacity=".16" stroke="{T["outline"]}" stroke-width="2">'
        body += ''.join(f'<path d="M0 {y}H2000"/>' for y in range(0, 1000, 11)) + '</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]:.0f} {vb[1]:.0f} {vb[2]:.0f} {vb[3]:.0f}" role="img" aria-label="GameMaster">'
            f'<title>GameMaster</title><defs>{defs}</defs>{body}</svg>'), vb[2], vb[3]

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for kind in ('completo', 'horizontal', 'compacto'):
        for theme in THEMES:
            svg, W, H = build(kind, theme, f'{kind[0]}{theme[:2]}')
            open(os.path.join(out, f'gamemaster-{kind}-{theme}.svg'), 'w').write(svg)
    print('ok')
