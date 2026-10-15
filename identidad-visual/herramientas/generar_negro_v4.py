#!/usr/bin/env python3
"""v4 · capas de NEGRO de los campos azules (como public/art/* del repo: grabado/bloques/estrellas/trazos negros, sombras duras).
Por sección: campo-<sec>-negro.svg (sobre el grabado azul, bajo los objetos) y, donde hay placas isométricas,
campo-<sec>-sombra.svg (bajo el grabado: volumen negro de las placas).
Uso: python3 generar_negro_v4.py ../assets/arte"""
import sys, os, random, math
sys.path.insert(0, os.path.dirname(__file__))
from arte_lib import W, H, f, iso, star as _star

K = '#05071f'
CSS = (f'<style>.k{{fill:{K};stroke:none}}.kl{{fill:none;stroke:{K};stroke-width:4;stroke-linecap:square;stroke-linejoin:miter;vector-effect:non-scaling-stroke}}'
       f'.kt{{fill:none;stroke:{K};stroke-width:5;stroke-linecap:square;stroke-linejoin:miter;vector-effect:non-scaling-stroke}}'
       f'.kf{{fill:none;stroke:{K};stroke-width:1.6;vector-effect:non-scaling-stroke}}.kh{{fill:none;stroke:{K};stroke-width:3;vector-effect:non-scaling-stroke}}</style>')
def svg(b): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">{CSS}{b}</svg>'
def P(d, c='k'): return f'<path class="{c}" d="{d}"/>'
def poly(pts, c='k'): return P('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z', c)
def R(x, y, w, h, c='k'): return f'<rect class="{c}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"/>'
def C(x, y, r, c='k'): return f'<circle class="{c}" cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>'
def L(x1, y1, x2, y2, c='kl'): return P(f'M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}', c)
def star(x, y, r): return _star(x, y, r, 'k')
def trace(pts, c='kt'): return P('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts), c)

def stars(r, n, area, sizes=(4, 6, 8, 11, 15)):
    x0, y0, x1, y1 = area; return ''.join(star(r.uniform(x0, x1), r.uniform(y0, y1), r.choice(sizes)) for _ in range(n))

def steps(corner, n=7, u=46, hmul=1.0, base=0):
    """bloques escalonados en una esquina: corner = 'bl','br','tl','tr'"""
    pts = []
    for k in range(n): pts.append((k * u, (n - k) * u * hmul))
    o = ''
    for k in range(n):
        w = (k + 1) * u; h = (n - k) * u * hmul
        pass
    # escalera sólida: columnas con alturas decrecientes
    cols = ''.join(R(k * u, 0, u + .5, (n - k) * u * .62 * hmul) for k in range(n))
    sx = -1 if corner[1] == 'r' else 1; sy = -1 if corner[0] == 'b' else 1
    tx = W if corner[1] == 'r' else 0; ty = H if corner[0] == 'b' else 0
    return f'<g transform="translate({tx} {ty}) scale({sx} {sy})">{cols}</g>'

def chip_block(x, y, w, h, pins=9, r=None, spread=(220, 420), nb=None):
    """chip negro con pistas gruesas que salen en abanico (como panel-chip-rear)"""
    r = r or random.Random(1); o = R(x, y, w, h)
    g = (w - 20) / pins
    for k in range(pins):
        px = x + 10 + k * g + g / 2
        o += R(px - 5, y - 16, 10, 16) + R(px - 5, y + h, 10, 16)
        o += R(x - 16, y + 10 + k * (h - 20) / pins + 2, 16, 8) if k < pins else ''
        o += R(x + w, y + 10 + k * (h - 20) / pins + 2, 16, 8)
        # pistas arriba/abajo con quiebre a 45°
        for (sgn, y0) in ((-1, y - 16), (1, y + h + 16)):
            dx = (k - pins / 2) * r.uniform(10, 22); l1 = r.uniform(18, 60); l2 = r.uniform(*spread) * r.uniform(.3, 1)
            o += trace([(px, y0), (px, y0 + sgn * l1), (px + dx, y0 + sgn * (l1 + abs(dx))), (px + dx, y0 + sgn * (l1 + abs(dx) + l2))])
            if r.random() < .6: o += C(px + dx, y0 + sgn * (l1 + abs(dx) + l2), 7, 'kt')
    return o

def small_ic(x, y, w, h, pins=5):
    o = R(x, y, w, h, 'kt') + ''.join(R(x + 8 + k * (w - 16) / pins + 3, y + h, 5, 14) for k in range(pins))
    return R(x, y, w, h, 'kt') + o

def halftone_k(x0, y0, w, h, step=12, rmax=4.2, d='r'):
    o = ''
    for j in range(int(h / step)):
        for i in range(int(w / step)):
            t = i / max(1, int(w / step)); t = t if d == 'r' else 1 - t
            rad = rmax * (1 - t) ** 1.2
            if rad > .8: o += C(x0 + i * step + (step / 2 if j % 2 else 0), y0 + j * step, rad)
    return o

def hatch_k(x, y, w, h, step=9, c='kh'):
    return ''.join(L(x + k * step, y + h, x + k * step + h * .6, y, c) for k in range(int(w / step)))

def vias(r, n, area):
    x0, y0, x1, y1 = area; o = ''
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1); o += C(x, y, 7, 'kt') + C(x, y, 2.5)
    return o

def ext(cx, cy, a, b, t, depth=30):
    A = iso(cx, cy, 0, 0, t); B = iso(cx, cy, a, 0, t); D = iso(cx, cy, 0, b, t)
    Bl = iso(cx, cy, a, 0, -depth); Cl = iso(cx, cy, a, b, -depth); Dl = iso(cx, cy, 0, b, -depth)
    return poly([A, B, Bl, Cl, Dl, D])

OUT = {}
# ================= HERO: horizonte con suelo de rejilla negra, montañas en bloque, estrellas, columnas =================
def hero():
    r = random.Random(101); hz = 410; b = stars(r, 26, (30, 20, W - 30, hz - 40))
    # suelo: rejilla negra gruesa en perspectiva (como field-gaming)
    b += P(f'M0 {hz}H{W}', 'kt')
    for i in range(-14, 15): b += L(W / 2 + i * 54, hz, W / 2 + i * 300, H, 'kl')
    y, step = hz, 8
    while y < H:
        y += step; step *= 1.3; b += L(0, y, W, y, 'kl')
    # siluetas escalonadas (pixel) a la izquierda del horizonte
    for (x, w, hh) in ((0, 70, 92), (70, 60, 140), (130, 70, 70), (200, 56, 112), (256, 70, 54)): b += R(x, hz - hh, w, hh)
    for k in range(5): b += R(1100 + k * 66, hz - 40 - (k % 3) * 38, 66, 40 + (k % 3) * 38)
    b += halftone_k(0, 120, 520, 160, 14, 5, 'r')
    b += steps('bl', 5, 44) + steps('br', 4, 44)
    OUT['hero-negro'] = svg(b)
    s = ''.join(ext(x, hz + 120, 130, 90, 20, 30) for x in (420, 980, 1480))
    OUT['hero-sombra'] = svg(s)

# ================= PALETA: plano técnico: chip negro con pistas, marcas de registro, cruces =================
def paleta():
    r = random.Random(102); b = chip_block(1070, 220, 360, 330, 12, r, (160, 300))
    b += small_ic(120, 640, 150, 100) + small_ic(1330, 700, 140, 90, 4)
    # marcas de registro
    for (x, y) in ((70, 70), (1530, 830)): b += C(x, y, 22, 'kt') + L(x - 36, y, x + 36, y) + L(x, y - 36, x, y + 36)
    b += steps('tl', 4, 42) + steps('br', 5, 46)
    b += stars(r, 22, (40, 40, W - 40, H - 40), (4, 6, 9))
    b += halftone_k(60, 760, 560, 100, 12, 4, 'l')
    b += vias(r, 14, (60, 60, 1540, 840))
    OUT['paleta-negro'] = svg(b)

# ================= CROMO: placas con volumen negro, columnas de bloques, bandas =================
def cromo():
    r = random.Random(103); plates = [(1130, 190, 300, 210, 30), (760, 420, 260, 190, 22), (1240, 520, 280, 200, 26), (400, 640, 240, 170, 18), (900, 700, 200, 150, 14)]
    OUT['cromo-sombra'] = svg(''.join(ext(cx, cy, a, bb, t, 42) for (cx, cy, a, bb, t) in plates))
    b = ''
    # columnas negras escalonadas (pilares) a los lados
    for k, hh in enumerate((260, 180, 330, 120, 220)): b += R(0 + k * 34, H - hh, 34, hh)
    for k, hh in enumerate((140, 250, 90, 300)): b += R(W - 4 * 36 + k * 36, 0, 36, hh)
    b += stars(r, 26, (150, 30, W - 150, H - 40), (4, 6, 9, 13))
    b += hatch_k(520, 60, 260, 70) + hatch_k(1280, 780, 240, 70)
    b += P('M0 60H300L380 0H0Z') + P(f'M{W} {H-70}H{W-360}L{W-440} {H}H{W}Z')
    b += vias(r, 12, (200, 60, 1400, 840))
    OUT['cromo-negro'] = svg(b)

# ================= PARALLAX: planetas negros con anillo, estrellas negras grandes, bloques flotantes =================
def parallax():
    r = random.Random(104); b = stars(r, 60, (20, 20, W - 20, H - 20), (4, 6, 9, 14, 20))
    for (cx, cy, rad) in ((1556, 800, 44), (46, 200, 34)):  # v5: planetas solo en los bordes, lejos de las piezas rojas
        b += C(cx, cy, rad) + P(f'M{cx - rad * 1.9} {cy + 10}A{rad * 1.9} {rad * .42} -14 0 0 {cx + rad * 1.9} {cy - 10}', 'kt') + P(f'M{cx - rad * 2.2} {cy + 18}A{rad * 2.2} {rad * .5} -14 0 0 {cx + rad * 2.2} {cy - 18}', 'kl')
    for (x, y, w, h) in ((0, 220, 90, 90), (1500, 520, 100, 60), (1450, 580, 150, 50), (0, 700, 70, 70)): b += R(x, y, w, h)
    b += steps('bl', 4, 40) + steps('tr', 5, 44)
    b += halftone_k(900, 40, 640, 120, 13, 4.6, 'l')
    OUT['parallax-negro'] = svg(b)

# ================= FILAS: pistas gruesas, chips negros, bits =================
def filas():
    r = random.Random(105); b = chip_block(60, 330, 220, 160, 8, r, (120, 240)) + chip_block(1290, 90, 240, 150, 8, r, (120, 240))
    b += small_ic(760, 760, 160, 90, 6) + small_ic(520, 60, 150, 80, 5)
    for k in range(70): 
        x, y = r.uniform(30, W - 30), r.uniform(30, H - 30); s = r.choice([8, 10, 14]); b += R(x, y, s, s)
    b += steps('br', 5, 44) + steps('tl', 4, 40)
    b += vias(r, 14, (60, 60, W - 60, H - 60))
    OUT['filas-negro'] = svg(b)

# ================= CATÁLOGO: escalera pixel negra gruesa, placas con volumen, cartuchos-silueta =================
def catalogo():
    r = random.Random(106); plates = [(1270, 160, 240, 170, 18), (620, 400, 300, 200, 24), (1200, 600, 280, 190, 22), (230, 640, 230, 160, 16)]
    OUT['catalogo-sombra'] = svg(''.join(ext(cx, cy, a, bb, t, 36) for (cx, cy, a, bb, t) in plates))
    b = ''; x, y = 0, 800
    for k in range(40):
        y = max(760, min(860, y + r.choice([-20, 0, 20]))); b += R(x, y, 40, H - y + 10); x += 40
    b += stars(r, 26, (30, 30, W - 30, 700), (4, 6, 9, 12))
    # cartucho-silueta pixel (blanco y negro de bloque) al fondo
    for (x0, y0) in ((60, 120), (1420, 420)):
        b += R(x0, y0, 70, 96) + R(x0 + 8, y0 - 12, 54, 14)
    b += hatch_k(700, 780, 320, 70) + halftone_k(40, 400, 460, 130, 13, 4.6, 'r')
    b += steps('tr', 5, 42)
    OUT['catalogo-negro'] = svg(b)

# ================= STREAMING: haz de rayos negros, cintas con perforaciones, estrellas =================
def streaming():
    r = random.Random(107); b = ''
    cx, cy = 1250, 260
    b += '<g opacity=".55">'  # v5: rayos más suaves
    for k in range(18):
        a0 = k * 20 + 4; a1 = a0 + 3.6
        p = lambda a, rr: (cx + math.cos(math.radians(a)) * rr, cy + math.sin(math.radians(a)) * rr)
        b += poly([p(a0, 230), p(a0, 1500), p(a1, 1500), p(a1, 230)])
    b += '</g>'
    for y in (60, 410, 690):
        b += R(0, y, W, 16) + R(0, y + 134, W, 16) if False else ''
    for k in range(16): b += R(-10 + k * 108, 40 if k % 2 else 820, 72, 22)
    b += stars(r, 30, (20, 20, W - 20, H - 20), (4, 6, 9, 13))
    b += steps('bl', 5, 44) + steps('tl', 3, 40)
    b += halftone_k(0, 250, 560, 130, 13, 4.6, 'r')
    OUT['streaming-negro'] = svg(b)

# ================= IA: red neuronal negra, matriz binaria en bloques, chip =================
def ia():
    r = random.Random(108); layers = (3, 5, 6, 5, 3); xs = [1010 + k * 120 for k in range(len(layers))]; nodes = []
    for k, n in enumerate(layers): nodes.append([(xs[k], 735 + (j - (n - 1) / 2) * 52) for j in range(n)])
    b = ''
    for a, c2 in zip(nodes, nodes[1:]):
        for (x1, y1) in a:
            for (x2, y2) in c2: b += L(x1, y1, x2, y2, 'kf')
    for col in nodes:
        for (x, y) in col: b += C(x, y, 15)
    b += chip_block(1130, 380, 240, 150, 8, r, (90, 160))
    for j in range(9):
        for i in range(16):
            if r.random() < .55: b += R(560 + i * 18, 600 + j * 30, r.choice([8, 12, 20]), 12)
    b += stars(r, 16, (30, 30, W - 30, 450), (4, 6, 9))
    b += steps('br', 5, 44) + steps('tl', 4, 40)
    OUT['ia-negro'] = svg(b)

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for fn in (hero, paleta, cromo, parallax, filas, catalogo, streaming, ia): fn()
    for k, v in OUT.items():
        open(os.path.join(out, f'campo-{k}.svg'), 'w').write(v); print(k, len(v) // 1024, 'KB')
