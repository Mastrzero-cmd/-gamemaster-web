#!/usr/bin/env python3
"""Genera el arte de v9b «Arcade-técnico»: planos azules (trazo/grabado, sin rejillas), sprites rojos y cortes. Salida: ../assets/{planos,heroes,piezas}/
Uso: python3 generar_arte.py"""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sprites as SP
BL, BK = '#1616FF', '#050505'
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
W, H = 1200, 640
def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def pl(pts): return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts)
def svg(w, h, body, bg=None): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">' + (f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else '') + body + '</svg>'
def stroke(d, w=2, dash=None, fill='none', extra=''): return f'<path d="{d}" fill="{fill}" stroke="{BL}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + f' stroke-linejoin="round" stroke-linecap="round"{extra}/>'

# ---------- 1. crestas de señal (estilo oscilograma apilado, líneas ocultas) ----------
def crestas(w=W, h=H, y0=120, n=26, gap=19, seed=1, peaks=((.5, .9),), amp=70, x0=0, x1=None):
    r = random.Random(seed); x1 = x1 or w; out = []
    ph = [r.uniform(0, 6.28) for _ in range(4)]
    for i in range(n):
        y = y0 + i * gap; pts = []
        for k in range(0, 121):
            t = k / 120; x = x0 + (x1 - x0) * t
            env = sum(a * math.exp(-((t - c) / .16) ** 2) for c, a in peaks) + .08
            v = (math.sin(t * 38 + ph[0] + i * .35) * .55 + math.sin(t * 17 + ph[1] - i * .2) * .3 + math.sin(t * 71 + ph[2]) * .15) * env * amp
            pts.append((x, y - abs(v) * 1.0 if False else y - v))
        d = pl(pts); out.append(f'<path d="{d}L{f(x1)} {h}L{f(x0)} {h}Z" fill="{BK}" stroke="{BL}" stroke-width="2" stroke-linejoin="round"/>')
    return ''.join(out)

# ---------- 2. constelaciones ----------
def estrella4(cx, cy, r): return f'M{f(cx)} {f(cy - r)}L{f(cx + r * .22)} {f(cy - r * .22)}L{f(cx + r)} {f(cy)}L{f(cx + r * .22)} {f(cy + r * .22)}L{f(cx)} {f(cy + r)}L{f(cx - r * .22)} {f(cy + r * .22)}L{f(cx - r)} {f(cy)}L{f(cx - r * .22)} {f(cy - r * .22)}Z'
def constelacion(w=W, h=H, n=46, seed=2, link=170, big=9, dist=90):
    r = random.Random(seed); pts = []
    tries = 0
    while len(pts) < n and tries < 4000:
        tries += 1; p = (r.uniform(20, w - 20), r.uniform(20, h - 20))
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > dist * .6 for q in pts): pts.append(p)
    segs = set(); out = []
    for i, p in enumerate(pts):
        near = sorted(range(len(pts)), key=lambda j: math.hypot(p[0] - pts[j][0], p[1] - pts[j][1]))[1:3]
        for j in near:
            if math.hypot(p[0] - pts[j][0], p[1] - pts[j][1]) < link and (min(i, j), max(i, j)) not in segs: segs.add((min(i, j), max(i, j)))
    out.append(stroke(''.join(f'M{f(pts[a][0])} {f(pts[a][1])}L{f(pts[b][0])} {f(pts[b][1])}' for a, b in segs), 1.6))
    for k, (x, y) in enumerate(pts):
        if k % 4 == 0: out.append(stroke(estrella4(x, y, big + r.uniform(0, 8)), 2, fill=BL))
        elif k % 4 == 1: out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(3, 6))}" fill="{BL}"/>')
        else: out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(5, 9))}" fill="none" stroke="{BL}" stroke-width="2"/>')
    return ''.join(out)

# ---------- 3. contornos tipo topografía / grabado (anillos deformados) ----------
def anillos(cx, cy, r0, r1, n, seed=3, wob=.12, w=2, rot=0):
    r = random.Random(seed); hs = [(r.uniform(.4, 1), k, r.uniform(0, 6.28)) for k in (2, 3, 5, 7)]; out = []
    for i in range(n):
        R = r0 + (r1 - r0) * i / max(n - 1, 1); pts = []
        for s in range(0, 181):
            a = s / 180 * 2 * math.pi
            d = sum(m * math.sin(k * a + p + i * .22) for m, k, p in hs) * wob * R / 3.2
            pts.append((cx + (R + d) * math.cos(a + rot), cy + (R + d) * math.sin(a + rot) * .78))
        out.append(stroke(pl(pts) + 'Z', w))
    return ''.join(out)

# ---------- 4. radar / medidor con marcas ----------
def radar(cx, cy, R, rings=7, ticks=72, seed=4, sweep=None):
    out = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R * i / rings)}" fill="none" stroke="{BL}" stroke-width="{3 if i == rings else 1.6}"' + (' stroke-dasharray="3 9"' if i % 2 == 0 and i != rings else '') + '/>' for i in range(1, rings + 1)]
    d = ''
    for k in range(ticks):
        a = k / ticks * 2 * math.pi; l = 18 if k % 6 == 0 else 8
        d += f'M{f(cx + (R + 6) * math.cos(a))} {f(cy + (R + 6) * math.sin(a))}L{f(cx + (R + 6 + l) * math.cos(a))} {f(cy + (R + 6 + l) * math.sin(a))}'
    out.append(stroke(d, 2))
    if sweep is not None:  # abanico de líneas
        d = ''
        for k in range(16):
            a = sweep - k * .045; d += f'M{f(cx)} {f(cy)}L{f(cx + R * math.cos(a))} {f(cy + R * math.sin(a))}'
        out.append(stroke(d, 1.4))
        out.append(stroke(f'M{f(cx)} {f(cy)}L{f(cx + R * math.cos(sweep))} {f(cy + R * math.sin(sweep))}', 3.5))
    return ''.join(out)

# ---------- 5. señal: arcos de transmisión + ondas senoidales ----------
def arcos_senal(cx, cy, n=11, step=62, a0=-1.05, a1=1.05, rot=0, seed=5):
    out = []
    for i in range(1, n + 1):
        R = i * step; pts = [(cx + R * math.cos(rot + a0 + (a1 - a0) * k / 40), cy + R * math.sin(rot + a0 + (a1 - a0) * k / 40)) for k in range(41)]
        out.append(stroke(pl(pts), 3 if i % 3 == 0 else 1.8, dash=None if i % 2 else '10 8'))
    return ''.join(out)
def onda(x0, x1, y, amp, periods, w=2, ph=0, dash=None, kind='sin'):
    pts = []
    for k in range(0, 241):
        t = k / 240; s = math.sin(t * periods * 2 * math.pi + ph)
        if kind == 'sq': s = 1 if s >= 0 else -1
        if kind == 'tri': s = 2 / math.pi * math.asin(s)
        pts.append((x0 + (x1 - x0) * t, y + amp * s))
    return stroke(pl(pts), w, dash)

# ---------- 6. red neuronal y trazas de circuito ----------
def red_neuronal(w=W, h=H, seed=6, layers=(4, 7, 8, 7, 4), x0=120, x1=1080, y0=90, y1=H - 90):
    r = random.Random(seed); cols = []
    for i, n in enumerate(layers):
        x = x0 + (x1 - x0) * i / (len(layers) - 1); ys = [y0 + (y1 - y0) * (j + .5) / n + r.uniform(-12, 12) for j in range(n)]; cols.append([(x + r.uniform(-14, 14), y) for y in ys])
    out = []; d = ''
    for a, b in zip(cols, cols[1:]):
        for (xa, ya) in a:
            for (xb, yb) in b:
                if r.random() < .55: d += f'M{f(xa)} {f(ya)}C{f(xa + 90)} {f(ya)} {f(xb - 90)} {f(yb)} {f(xb)} {f(yb)}'
    out.append(stroke(d, 1.3))
    for c in cols:
        for (x, y) in c:
            rr = r.choice([7, 9, 11]); out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{rr + 5}" fill="{BK}" stroke="{BL}" stroke-width="2.5"/><circle cx="{f(x)}" cy="{f(y)}" r="{rr - 3}" fill="{BL}"/>')
    return ''.join(out)
def trazas(w=W, h=H, seed=7, n=14, x0=0, x1=None):
    r = random.Random(seed); x1 = x1 or w; out = []
    for i in range(n):
        x, y = r.choice([x0, x1]), r.uniform(30, h - 30); pts = [(x, y)]; dx = -1 if x > w / 2 else 1
        for s in range(r.randint(3, 6)):
            x += dx * r.uniform(40, 130); pts.append((x, y)); y += r.choice([-1, 1]) * r.uniform(30, 90); y = min(max(y, 20), h - 20); pts.append((x, y))
            if r.random() < .3: dx = -dx if False else dx
        out.append(stroke(pl(pts), 2.2)); ex, ey = pts[-1]; out.append(f'<circle cx="{f(ex)}" cy="{f(ey)}" r="7" fill="{BK}" stroke="{BL}" stroke-width="2.5"/>')
    return ''.join(out)

# ---------- 7. sol de rayos, engranes, lissajous, luna rayada ----------
def rayos(cx, cy, r0, r1, n=60, seed=8, w=2):
    r = random.Random(seed); d = ''
    for k in range(n):
        a = k / n * 2 * math.pi; rr = r1 * (1 if k % 3 else .8) * r.uniform(.9, 1.0); d += f'M{f(cx + r0 * math.cos(a))} {f(cy + r0 * math.sin(a))}L{f(cx + rr * math.cos(a))} {f(cy + rr * math.sin(a))}'
    return stroke(d, w)
def engrane(cx, cy, R, dientes=14, hole=.35, w=2.5):
    pts = []
    for k in range(dientes * 4):
        a = k / (dientes * 4) * 2 * math.pi; rr = R if (k % 4) in (1, 2) else R * .84; pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return stroke(pl(pts) + 'Z', w) + f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R * hole)}" fill="none" stroke="{BL}" stroke-width="{w}"/>' + f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R * .12)}" fill="{BL}"/>'
def lissajous(cx, cy, A, B, a, b, d=math.pi / 2, n=400, w=1.8, turns=1):
    pts = [(cx + A * math.sin(a * t + d), cy + B * math.sin(b * t)) for t in [k / n * 2 * math.pi * turns for k in range(n + 1)]]
    return stroke(pl(pts), w)
def luna_rayada(cx, cy, R, gap=9, ang=.8, w=2, cid='c'):
    d = ''; ca, sa = math.cos(ang), math.sin(ang)
    k = -R
    while k <= R:
        half = math.sqrt(max(R * R - k * k, 0)); x1, y1 = cx + k * (-sa) - half * ca, cy + k * ca - half * sa; x2, y2 = cx + k * (-sa) + half * ca, cy + k * ca + half * sa
        d += f'M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}'; k += gap
    return stroke(d, w) + f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{R}" fill="none" stroke="{BL}" stroke-width="3.5"/>'
def orbitas(cx, cy, rs, tilt=-.35, w=1.8):
    out = ''
    for i, R in enumerate(rs):
        out += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{R}" ry="{f(R * .32)}" transform="rotate({f(tilt * 57.3)} {f(cx)} {f(cy)})" fill="none" stroke="{BL}" stroke-width="{w}"' + (' stroke-dasharray="4 8"' if i % 2 else '') + '/>'
    return out
def barras_eq(w, h, n=70, seed=9, base=None):
    r = random.Random(seed); base = base or h - 10; d = ''; bw = w / n
    for i in range(n):
        env = .5 + .5 * math.sin(i / n * 9 + 1) * math.sin(i / n * 3.1); hh = (h - 24) * max(.12, min(1, env * r.uniform(.6, 1))); d += f'M{f(i * bw + bw / 2)} {f(base)}V{f(base - hh)}'
    return f'<path d="{d}" fill="none" stroke="{BL}" stroke-width="{f(bw * .52)}"/>'

PLANOS = {
 'inicio': lambda: crestas(y0=170, n=24, gap=19, seed=11, peaks=((.22, .9), (.7, 1.0)), amp=82) + stroke(estrella4(110, 70, 22), 2, fill=BL) + stroke(estrella4(1090, 560, 18), 2, fill=BL) + lissajous(1020, 130, 120, 70, 3, 2, w=1.8) + f'<circle cx="190" cy="120" r="9" fill="{BL}"/><circle cx="900" cy="64" r="6" fill="{BL}"/><circle cx="520" cy="90" r="5" fill="{BL}"/>',
 'marcas': lambda: constelacion(n=60, seed=21, link=190) + luna_rayada(980, 470, 120, 9, .9) + orbitas(980, 470, [190, 240, 290], -.35),
 'catalogo': lambda: anillos(330, 330, 20, 330, 22, seed=31, wob=.3) + anillos(1000, 300, 14, 230, 14, seed=32, wob=.28, rot=.5) + rayos(1000, 300, 250, 330, 56, seed=33),
 'streaming': lambda: arcos_senal(40, 560, 14, 70, -1.45, .05) + onda(0, W, 130, 38, 5, 2.5) + onda(0, W, 190, 26, 9, 1.6, ph=1, dash='10 8') + onda(0, W, 250, 20, 3.2, 3, kind='sq') + f''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{BL}"/>' for x, y in [(300, 130), (700, 210), (1040, 90), (1130, 380)]),
 'ia': lambda: trazas(seed=41, n=16) + red_neuronal(seed=42) ,
 'logo': lambda: radar(600, 330, 270, 7, 90, sweep=-.75) + engrane(120, 130, 90, 14) + engrane(235, 70, 52, 9) + engrane(1090, 520, 100, 16) + estrella4and(),
 'sistema': lambda: rayos(600, 320, 90, 620, 120, seed=51) + lissajous(220, 330, 170, 120, 3, 4, w=2) + lissajous(1000, 300, 150, 150, 5, 4, w=2) + orbitas(600, 330, [260, 330, 400], .3),
 'contacto': lambda: crestas(y0=340, n=17, gap=19, seed=61, peaks=((.5, 1.1),), amp=90) + constelacion(w=W, h=300, n=22, seed=62, link=200),
}
def estrella4and(): return stroke(estrella4(1000, 100, 24), 2, fill=BL) + stroke(estrella4(160, 560, 16), 2, fill=BL)

# ---------- escenas rojas ----------
def sp(name, x, y, cell): return SP.group(name, x, y, cell)[0]
def scene(items):
    return svg(W, H, ''.join(sp(*it) for it in items))
HEROES = {
 'inicio': [('fantasma', 250, 190, 13), ('pacman', 540, 120, 23), ('pellet', 940, 292, 9), ('pellet', 1000, 292, 9), ('pellet', 1060, 292, 9)],
 'marcas': [('tetris_L', 330, 330, 15), ('tetris_T', 530, 405, 15), ('tetris_I', 780, 480, 15), ('tetris_S', 560, 225, 15), ('tetris_O', 800, 150, 15)],
 'catalogo': [('hongo', 560, 130, 22), ('pokebola', 250, 290, 14), ('trifuerza', 770, 10, 10)],
 'streaming': [('tv', 600, 110, 23)],
 'ia': [('robot', 590, 100, 24)],
 'logo': [('mando', 470, 190, 22)],
 'sistema': [('amongus', 520, 110, 26)],
 'contacto': [('moneda', 380, 80, 28)],
}
PIEZAS = {
 'inicio': [('invader', 150, 70, 8), ('corazon', 900, 60, 7), ('estrella', 150, 430, 9), ('corazon', 990, 60, 7), ('invader', 840, 480, 6)],
 'marcas': [('bloque', 160, 90, 8), ('moneda', 950, 70, 6), ('tetris_O', 140, 470, 8)],
 'catalogo': [('bloque', 140, 70, 8), ('estrella', 960, 430, 8), ('corazon', 760, 540, 6), ('corazon', 850, 540, 6), ('pikachu', 330, 40, 9), ('anillo', 1000, 200, 7)],
 'streaming': [('fantasma', 150, 110, 8), ('mando', 930, 460, 6), ('pacman', 150, 440, 7)],
 'ia': [('creeper', 150, 90, 8), ('invader', 960, 90, 8), ('anillo', 150, 460, 8), ('kirby', 950, 430, 7)],
 'logo': [('anillo', 160, 100, 9), ('moneda', 960, 440, 7), ('corazon', 150, 450, 7), ('estrella', 960, 100, 8)],
 'sistema': [('creeper', 150, 110, 8), ('kirby', 940, 90, 8), ('pikachu', 930, 400, 9), ('pokebola', 150, 430, 8)],
 'contacto': [('corazon', 160, 90, 8), ('corazon', 260, 90, 8), ('corazon', 360, 90, 8), ('estrella', 960, 90, 9), ('invader', 150, 420, 8)],
}
# ---------- cortes (1440x120) ----------
CW, CH = 1440, 120
def corte(kind):
    if kind == 'onda': return onda(0, CW, 60, 34, 7, 4) + onda(0, CW, 60, 18, 13, 2, ph=1, dash='8 8')
    if kind == 'cuadrada': return onda(0, CW, 60, 32, 6, 4, kind='sq') + onda(0, CW, 60, 22, 11, 2, kind='tri', dash='6 8')
    if kind == 'ecualizador': return barras_eq(CW, CH, 90, 5)
    if kind == 'constelacion': return constelacion(CW, CH, 38, 71, 220, 6, 80)
    if kind == 'latido':
        pts = [(0, 60)]; x = 0
        while x < CW:
            x += 150; pts += [(x - 70, 60), (x - 50, 60), (x - 40, 30), (x - 30, 100), (x - 18, 10), (x - 8, 70), (x, 60)]
        return stroke(pl(pts), 3.5) + stroke(f'M0 106H{CW}', 1.5, dash='3 9')
    if kind == 'circuito': return trazas(CW, CH, 81, 20)
CUTS = ['onda', 'cuadrada', 'ecualizador', 'constelacion', 'latido', 'circuito']
PELLETS = lambda: svg(CW, CH, ''.join(sp('pellet', 40 + i * 70, 56, 7) for i in range(20)) + sp('pacman', 1340, 22, 5))

def main():
    for d in ('planos', 'heroes', 'piezas'): os.makedirs(os.path.join(OUT, d), exist_ok=True)
    def w(sub, name, s): open(os.path.join(OUT, sub, name + '.svg'), 'w').write(s)
    for k, fn in PLANOS.items(): w('planos', k, svg(W, H, fn()))
    for k, it in HEROES.items(): w('heroes', k, scene(it))
    for k, it in PIEZAS.items(): w('piezas', k, scene(it))
    for k in CUTS: w('planos', 'corte-' + k, svg(CW, CH, corte(k)))
    w('piezas', 'corte-pellets', PELLETS())
    # sprites sueltos para HUD y rellenos
    for n in ('corazon', 'moneda', 'estrella', 'invader', 'pacman', 'fantasma', 'hongo'):
        s, _, _ = SP.sprite_svg(n, 4); w('piezas', 'sprite-' + n, s)
if __name__ == '__main__': main()
