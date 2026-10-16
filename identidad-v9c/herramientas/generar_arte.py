#!/usr/bin/env python3
"""v9c «Mapa / Expedición»: genera todo el arte SVG (planos azules de grabado cartográfico, sellos rojos con emblemas y piezas).
Colores planos: azul #1616FF, rojo #FF1A1A, negro #050505, hielo #F4F4EF. Sin degradados, opacidades, filtros ni mezcla rojo+azul en un mismo SVG.
Uso: python3 generar_arte.py   (escribe en ../assets/{planos,heroes,piezas})"""
import os, math, random
import numpy as np
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
B, R, K, I = '#1616FF', '#FF1A1A', '#050505', '#F4F4EF'
def w(rel, s):
    p = os.path.join(OUT, rel); open(p, 'w').write(s); return len(s)
f1 = lambda v: ('%.1f' % v).rstrip('0').rstrip('.')
# ---------- campo y contornos (marching squares propio) ----------
def field(W, H, seed, step, blobs=40, smin=70, smax=280):
    rng = np.random.default_rng(seed)
    xs = np.arange(0, W + step, step); ys = np.arange(0, H + step, step); X, Y = np.meshgrid(xs, ys)
    F = np.zeros_like(X, dtype=float)
    for _ in range(blobs):
        cx, cy, s, a = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(smin, smax), rng.choice([-1, 1]) * rng.uniform(.5, 1)
        F += a * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * s * s))
    F += .12 * np.sin(X / 90 + rng.uniform(0, 6)) * np.cos(Y / 130 + rng.uniform(0, 6))
    F = (F - F.min()) / (F.max() - F.min()); return F
TAB = {1: [('l', 'b')], 2: [('b', 'r')], 3: [('l', 'r')], 4: [('t', 'r')], 5: [('t', 'l'), ('b', 'r')], 6: [('t', 'b')], 7: [('t', 'l')], 8: [('t', 'l')],
       9: [('t', 'b')], 10: [('t', 'r'), ('l', 'b')], 11: [('t', 'r')], 12: [('l', 'r')], 13: [('b', 'r')], 14: [('l', 'b')]}
def contours(F, lv, step):
    ny, nx = F.shape; segs = []
    def pt(e, i, j):
        if e == 't': a, b, pa, pb = F[j, i], F[j, i + 1], (i, j), (i + 1, j); k = ('h', i, j)
        if e == 'b': a, b, pa, pb = F[j + 1, i], F[j + 1, i + 1], (i, j + 1), (i + 1, j + 1); k = ('h', i, j + 1)
        if e == 'l': a, b, pa, pb = F[j, i], F[j + 1, i], (i, j), (i, j + 1); k = ('v', i, j)
        if e == 'r': a, b, pa, pb = F[j, i + 1], F[j + 1, i + 1], (i + 1, j), (i + 1, j + 1); k = ('v', i + 1, j)
        t = (lv - a) / (b - a + 1e-12); return k, ((pa[0] + (pb[0] - pa[0]) * t) * step, (pa[1] + (pb[1] - pa[1]) * t) * step)
    for j in range(ny - 1):
        for i in range(nx - 1):
            c = (F[j, i] > lv) * 8 + (F[j, i + 1] > lv) * 4 + (F[j + 1, i + 1] > lv) * 2 + (F[j + 1, i] > lv)
            for e1, e2 in TAB.get(c, []): segs.append((pt(e1, i, j), pt(e2, i, j)))
    adj = {}
    for n, (a, b) in enumerate(segs): adj.setdefault(a[0], []).append(n); adj.setdefault(b[0], []).append(n)
    used = set(); out = []
    for n0 in range(len(segs)):
        if n0 in used: continue
        used.add(n0); a, b = segs[n0]; chain = [a[1], b[1]]; ke, ks = b[0], a[0]
        for direction in (0, 1):
            while True:
                key = ke if direction == 0 else ks; nxt = [m for m in adj[key] if m not in used]
                if not nxt: break
                m = nxt[0]; used.add(m); p, q = segs[m]; nq = q if p[0] == key else p
                if direction == 0: chain.append(nq[1]); ke = nq[0]
                else: chain.insert(0, nq[1]); ks = nq[0]
        out.append(chain)
    return out
def chaikin(pts, closed):
    if len(pts) < 3: return pts
    o = [] if closed else [pts[0]]
    for a, b in zip(pts, pts[1:]): o += [(.75 * a[0] + .25 * b[0], .75 * a[1] + .25 * b[1]), (.25 * a[0] + .75 * b[0], .25 * a[1] + .75 * b[1])]
    if not closed: o.append(pts[-1])
    return o
def d_of(pts):
    closed = math.dist(pts[0], pts[-1]) < .5; pts = chaikin(pts, closed)
    return 'M' + ' '.join(str(round(x)) + ' ' + str(round(y)) for x, y in pts[:1]) + 'L' + ' '.join(str(round(x)) + ' ' + str(round(y)) for x, y in pts[1:]) + ('Z' if closed else '')
def path(d, stroke, sw, fill='none', extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{extra}/>'
def levels(F, lvs, step, stroke, sw, minlen=6):
    s = ''
    for lv in lvs:
        ds = [d_of(c) for c in contours(F, lv, step) if len(c) >= minlen]
        if ds: s += path(''.join(ds), stroke, sw)
    return s
def coast_ticks(F, lv, step, stroke, sw, every=15, ln=9):
    d = ''
    for c in contours(F, lv, step):
        if len(c) < 12: continue
        acc = 0
        for a, b in zip(c, c[1:]):
            seg = math.dist(a, b); acc += seg
            if acc < every or seg < .01: continue
            acc = 0; tx, ty = (b[0] - a[0]) / seg, (b[1] - a[1]) / seg; nx_, ny_ = -ty, tx
            def val(px, py):
                i = min(F.shape[1] - 1, max(0, int(px / step))); j = min(F.shape[0] - 1, max(0, int(py / step))); return F[j, i]
            sgn = 1 if val(b[0] + nx_ * step * 1.5, b[1] + ny_ * step * 1.5) < val(b[0] - nx_ * step * 1.5, b[1] - ny_ * step * 1.5) else -1
            d += f'M{f1(b[0])} {f1(b[1])}l{f1(sgn * nx_ * ln)} {f1(sgn * ny_ * ln)}'
    return path(d, stroke, sw) if d else ''
def scatter(F, step, W, H, cond, n, mind, seed, margin=40):
    rng = random.Random(seed); pts = []
    for _ in range(n * 40):
        x, y = rng.uniform(margin, W - margin), rng.uniform(margin, H - margin)
        i, j = int(x / step), int(y / step)
        if cond(F[j, i]) and all(math.dist((x, y), p) > mind for p in pts): pts.append((x, y))
        if len(pts) >= n: break
    return pts
def mountains(pts, stroke, sw, s=1.0):
    d = ''
    for x, y in pts:
        a, h = 15 * s, 24 * s; d += f'M{f1(x - a)} {f1(y)}L{f1(x)} {f1(y - h)}L{f1(x + a)} {f1(y)}'
        for k in range(1, 5): d += f'M{f1(x + k * a / 5 * 1)} {f1(y - h * (1 - k / 5) )}l{f1(a * .1)} {f1(h * .22)}'
        d += f'M{f1(x - a * .4)} {f1(y - h * .35)}L{f1(x + a * .1)} {f1(y)}'
    return path(d, stroke, sw)
def waves(pts, stroke, sw, s=1.0):
    d = ''
    for x, y in pts: d += f'M{f1(x - 11 * s)} {f1(y)}q{f1(5.5 * s)} {f1(-8 * s)} {f1(11 * s)} 0q{f1(5.5 * s)} {f1(8 * s)} {f1(11 * s)} 0'
    return path(d, stroke, sw)
def trees(pts, stroke, sw):
    d = ''
    for x, y in pts: d += f'M{f1(x)} {f1(y + 6)}v-12M{f1(x - 6)} {f1(y - 2)}l6 -12l6 12z'
    return path(d, stroke, sw)
def rose(cx, cy, Rr, fg, bg, ticks=True, rays=0, sw=2):
    s = f'<circle cx="{cx}" cy="{cy}" r="{f1(Rr * 1.08)}" fill="{bg}"/>'
    if rays:
        d = ''.join(f'M{cx} {cy}L{f1(cx + math.sin(math.radians(k * 22.5)) * rays)} {f1(cy - math.cos(math.radians(k * 22.5)) * rays)}' for k in range(16))
        s = path(d, fg, 1.3) + s
    s += f'<circle cx="{cx}" cy="{cy}" r="{f1(Rr)}" fill="none" stroke="{fg}" stroke-width="{sw * 1.5}"/><circle cx="{cx}" cy="{cy}" r="{f1(Rr * .9)}" fill="none" stroke="{fg}" stroke-width="{sw}"/>'
    if ticks:
        d = ''
        for k in range(72):
            a = math.radians(k * 5); l0 = Rr * (.8 if k % 6 == 0 else .85 if k % 2 == 0 else .88)
            d += f'M{f1(cx + math.sin(a) * l0)} {f1(cy - math.cos(a) * l0)}L{f1(cx + math.sin(a) * Rr * .9)} {f1(cy - math.cos(a) * Rr * .9)}'
        s += path(d, fg, sw * .7)
    rb = .2 * Rr; pa, ps = '', ''
    for k in range(16):
        L = Rr * (.76 if k % 4 == 0 else .58 if k % 2 == 0 else .4) * (1.0 if k % 4 else 1.0)
        th = math.radians(k * 22.5); tip = (cx + math.sin(th) * L, cy - math.cos(th) * L)
        bl = (cx + math.sin(th - math.radians(11.25)) * rb, cy - math.cos(th - math.radians(11.25)) * rb); br = (cx + math.sin(th + math.radians(11.25)) * rb, cy - math.cos(th + math.radians(11.25)) * rb)
        pa += f'M{cx} {cy}L{f1(tip[0])} {f1(tip[1])}L{f1(bl[0])} {f1(bl[1])}Z'; ps += f'M{cx} {cy}L{f1(tip[0])} {f1(tip[1])}L{f1(br[0])} {f1(br[1])}Z'
    s += f'<path d="{pa}" fill="{fg}" stroke="{fg}" stroke-width="{sw * .6}" stroke-linejoin="round"/><path d="{ps}" fill="{bg}" stroke="{fg}" stroke-width="{sw * .8}" stroke-linejoin="round"/>'
    # flor de lis / norte
    s += f'<path d="M{cx} {f1(cy - Rr * .8)}l{f1(-Rr * .07)} {f1(-Rr * .1)}q{f1(Rr * .07)} {f1(-Rr * .12)} {f1(Rr * .07)} {f1(-Rr * .3)}q{f1(0)} {f1(Rr * .18)} {f1(Rr * .07)} {f1(Rr * .3)}z" fill="{fg}" stroke="{fg}" stroke-width="{sw * .6}"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{f1(rb * .5)}" fill="{bg}" stroke="{fg}" stroke-width="{sw}"/>'
    return s
def star4(x, y, r, fg):
    return f'M{f1(x)} {f1(y - r)}Q{f1(x)} {f1(y)} {f1(x + r)} {f1(y)}Q{f1(x)} {f1(y)} {f1(x)} {f1(y + r)}Q{f1(x)} {f1(y)} {f1(x - r)} {f1(y)}Q{f1(x)} {f1(y)} {f1(x)} {f1(y - r)}Z'
def svg(W, H, body, bg=None):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">' + (f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else '') + body + '</svg>'
W, H, ST = 1600, 1000, 10
# ---------- PLANOS ----------
def plano_isla(seed, fg, bg, n_m=26, n_w=60, n_t=0, rosas=((1260, 270, 150),), dens=1.0, solid=True, sea=.46, rays=True):
    F = field(W, H, seed, ST); s = ''
    s += levels(F, [x for x in np.linspace(.1, sea - .03, 7)], ST, fg, 1.6)           # ondas del mar (eco de la costa)
    s += levels(F, [sea], ST, fg, 5)                                                # costa
    s += coast_ticks(F, sea, ST, fg, 1.6)
    s += levels(F, [x for x in np.linspace(sea + .04, .98, int(14 * dens))], ST, fg, 2)  # relieve
    s += mountains(scatter(F, ST, W, H, lambda v: v > .74, n_m, 58, seed + 1), fg, 2, 1.0)
    s += trees(scatter(F, ST, W, H, lambda v: sea + .02 < v < .66, n_t, 34, seed + 2), fg, 1.8) if n_t else ''
    s += waves(scatter(F, ST, W, H, lambda v: v < sea - .08, n_w, 70, seed + 3), fg, 1.8)
    for (cx, cy, rr) in rosas: s += rose(cx, cy, rr, fg, bg, rays=(rr * 5 if rays else 0))
    return svg(W, H, s, bg if solid else None)
def plano_ondas(seed, fg, bg, cx=900, rows=52):
    rng = random.Random(seed); s = ''
    cs = [(rng.uniform(300, 1300), rng.uniform(60, 130), rng.uniform(.5, 1)) for _ in range(5)]
    for r in range(rows):
        y0 = 120 + r * (H - 160) / rows; pts = []
        for x in range(-20, W + 21, 8):
            amp = sum(a * math.exp(-((x - c) ** 2) / (2 * sg * sg)) for c, sg, a in cs) * 62
            ph = x / (30 + (r % 5) * 3) + r * .9
            pts.append((x, y0 - amp * abs(math.sin(ph * .7) * .6 + math.sin(ph * 1.9) * .4) - 3 * math.sin(x / 40 + r)))
        d = 'M' + f1(pts[0][0]) + ' ' + f1(H + 20) + 'L' + ' '.join(f1(x) + ' ' + f1(y) for x, y in pts) + 'L' + f1(pts[-1][0]) + ' ' + f1(H + 20) + 'Z'
        s += f'<path d="{d}" fill="{bg}" stroke="{fg}" stroke-width="2.4" stroke-linejoin="round"/>'
    # señal: arcos rotos concentricos
    for k, rr in enumerate([180, 270, 360, 450, 540]):
        a0 = -150 + k * 7; d = ''
        for seg in range(5):
            s0 = math.radians(a0 + seg * 62); s1 = s0 + math.radians(40)
            d += f'M{f1(1180 + rr * math.cos(s0))} {f1(300 + rr * math.sin(s0))}A{rr} {rr} 0 0 1 {f1(1180 + rr * math.cos(s1))} {f1(300 + rr * math.sin(s1))}'
        s += path(d, fg, 4 + (k % 2) * 2)
    s += rose(250, 840, 120, fg, bg, rays=0)
    return svg(W, H, s)
def plano_const(seed, fg, bg):
    rng = random.Random(seed); s = ''
    # anillos ecliptica con marcas
    for (cx, cy, rr, dash) in [(800, 500, 470, '3 11'), (800, 500, 380, ''), (800, 500, 560, '14 9')]:
        s += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{fg}" stroke-width="{2.2 if not dash else 3}" stroke-dasharray="{dash}"/>' if dash else f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{fg}" stroke-width="2"/>'
    d = ''
    for k in range(120):
        a = math.radians(k * 3); l = 24 if k % 10 == 0 else 12 if k % 5 == 0 else 6
        d += f'M{f1(800 + 380 * math.cos(a))} {f1(500 + 380 * math.sin(a))}L{f1(800 + (380 - l) * math.cos(a))} {f1(500 + (380 - l) * math.sin(a))}'
    s += path(d, fg, 1.6)
    # red neuronal en capas (curvas)
    layers = [(300, [250, 400, 550, 700, 820]), (560, [200, 340, 480, 620, 760, 880]), (820, [270, 430, 590, 750]), (1080, [200, 350, 500, 650, 800]), (1340, [340, 520, 700])]
    nodes = [[(x, y + rng.uniform(-14, 14)) for y in ys] for x, ys in layers]; d = ''
    for a, b in zip(nodes, nodes[1:]):
        for p in a:
            for q in b:
                if rng.random() < .75: d += f'M{f1(p[0])} {f1(p[1])}C{f1((p[0] + q[0]) / 2)} {f1(p[1])} {f1((p[0] + q[0]) / 2)} {f1(q[1])} {f1(q[0])} {f1(q[1])}'
    s += path(d, fg, 1.1)
    for L in nodes:
        for x, y in L: s += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="11" fill="{bg}" stroke="{fg}" stroke-width="3.2"/><circle cx="{f1(x)}" cy="{f1(y)}" r="3.5" fill="{fg}"/>'
    # constelaciones sueltas
    for _ in range(9):
        cx, cy = rng.choice([rng.uniform(40, 360), rng.uniform(1240, 1560)]), rng.uniform(60, 940); pts = [(cx + rng.uniform(-120, 120), cy + rng.uniform(-90, 90)) for _ in range(rng.randint(4, 6))]
        d = 'M' + 'L'.join(f1(x) + ' ' + f1(y) for x, y in pts); s += path(d, fg, 1.6)
        for x, y in pts: s += f'<path d="{star4(x, y, rng.choice([9, 13, 17]), fg)}" fill="{fg}"/>'
    # estrellas de relleno
    d = ''.join(star4(rng.uniform(10, 1590), rng.uniform(10, 990), rng.choice([3, 4, 5, 7]), fg) for _ in range(150)); s += f'<path d="{d}" fill="{fg}"/>'
    # circuitos-rio: trazos con codos a 45 grados
    for _ in range(10):
        x, y = rng.choice([rng.uniform(20, 260), rng.uniform(1340, 1580)]), rng.uniform(60, 940); d = f'M{f1(x)} {f1(y)}'; sx = 1 if x < 800 else -1
        for _k in range(3): d += f'l{f1(sx * rng.uniform(30, 80))} 0l{f1(sx * 40)} {f1(rng.choice([-1, 1]) * 40)}'
        s += path(d, fg, 2.4) + f'<circle cx="{f1(x)}" cy="{f1(y)}" r="6" fill="{bg}" stroke="{fg}" stroke-width="2.6"/>'
    s += rose(1420, 830, 120, fg, bg)
    return svg(W, H, s, bg)
def plano_ripples(seed, fg, bg):
    rng = random.Random(seed); s = ''
    for (cx, cy, n) in [(420, 480, 24), (1250, 620, 18)]:
        for k in range(1, n):
            d = ''; rr = 28 * k + (k * k) * .55; gap = rng.random() * 360
            for seg in range(rng.randint(2, 4)):
                a0 = math.radians(gap + seg * 360 / 3 + rng.uniform(0, 40)); a1 = a0 + math.radians(rng.uniform(60, 100))
                d += f'M{f1(cx + rr * math.cos(a0))} {f1(cy + rr * math.sin(a0))}A{f1(rr)} {f1(rr)} 0 0 1 {f1(cx + rr * math.cos(a1))} {f1(cy + rr * math.sin(a1))}'
            s += path(d, fg, 1.8 + (k % 3) * .8)
    s += rose(1260, 250, 120, fg, bg)
    d = ''.join(f'M{f1(x)} {f1(y)}q6 -9 12 0q6 9 12 0' for x, y in [(rng.uniform(40, 1560), rng.uniform(40, 960)) for _ in range(70)]); s += path(d, fg, 1.8)
    return svg(W, H, s, bg)
def plano_topo_linea(seed, fg, rosas, rays=True):
    F = field(W, H, seed, ST); s = levels(F, list(np.linspace(.06, .96, 26)), ST, fg, 2)
    s += levels(F, [.5], ST, fg, 5) + coast_ticks(F, .5, ST, fg, 1.5, 17, 8)
    for (cx, cy, rr) in rosas: s += rose(cx, cy, rr, fg, K, rays=(rr * 6 if rays else 0))
    return svg(W, H, s)
def plano_tesoro(seed, fg, bg):
    F = field(W, H, seed, ST); sea = .5; s = levels(F, list(np.linspace(.12, sea - .03, 6)), ST, fg, 1.6) + levels(F, [sea], ST, fg, 5) + coast_ticks(F, sea, ST, fg, 1.6) + levels(F, list(np.linspace(sea + .05, .98, 12)), ST, fg, 2)
    s += mountains(scatter(F, ST, W, H, lambda v: v > .75, 20, 62, seed + 1), fg, 2) + waves(scatter(F, ST, W, H, lambda v: v < sea - .1, 50, 80, seed + 2), fg, 1.8)
    s += rose(300, 760, 170, fg, bg, rays=900)
    return svg(W, H, s, bg)
def plano_hojas(seed, fg, bg):  # logo: sello de mar con ondas
    return plano_ripples(seed, fg, bg)
PL = {
 'inicio': plano_isla(11, K, B, n_m=30, n_w=70, n_t=22, rosas=((1250, 260, 165), (230, 790, 105))),
 'marcas': plano_topo_linea(23, B, ((1380, 780, 150), (200, 220, 90))),
 'catalogo': plano_isla(37, K, B, n_m=40, n_w=40, n_t=26, rosas=((250, 780, 120),), dens=1.2, sea=.42),
 'streaming': plano_ondas(41, B, K),
 'ia': plano_const(53, K, B),
 'logo': plano_ripples(61, K, B),
 'sistema': plano_topo_linea(71, B, ((300, 740, 110),), rays=False),
 'contacto': plano_tesoro(83, K, B),
}
# el plano de ripples en azul sobre negro (logo y sistema usan fondo azul) -> se cambia de colores aqui:
for k, v in PL.items(): print('plano', k, w(f'planos/{k}.svg', v) // 1024, 'KB')
# ---------- EMBLEMAS (rojo con detalle negro/hielo), caja 400x400 ----------
def poly(pts, fill, stroke=K, sw=10, extra=''):
    return f'<polygon points="{" ".join(f1(x) + "," + f1(y) for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{extra}/>'
def emb_triforce():
    return poly([(200, 40), (115, 185), (285, 185)], R) + poly([(30, 335), (115, 185), (200, 335)], R) + poly([(200, 335), (285, 185), (370, 335)], R)
def emb_espada():
    s = poly([(200, 14), (222, 78), (222, 238), (178, 238), (178, 78)], R)
    s += f'<path d="M200 70V222" stroke="{K}" stroke-width="7" stroke-linecap="round"/>'
    s += poly([(96, 205), (150, 232), (250, 232), (304, 205), (292, 268), (240, 256), (160, 256), (108, 268)], R)
    s += f'<polygon points="200,236 188,252 212,252" fill="{K}"/>'
    s += poly([(188, 256), (212, 256), (212, 322), (188, 322)], R, sw=9) + f'<path d="M188 276H212M188 296H212" stroke="{K}" stroke-width="6"/>'
    s += f'<circle cx="200" cy="342" r="22" fill="{R}" stroke="{K}" stroke-width="10"/>'
    return s
def emb_hongo():
    s = f'<path d="M92 236C84 262 118 284 156 284H244C282 284 316 262 308 236Z" fill="{I}" stroke="{K}" stroke-width="10" stroke-linejoin="round"/>'
    s = f'<path d="M126 282C120 330 134 352 160 352H240C266 352 280 330 274 282Z" fill="{I}" stroke="{K}" stroke-width="10" stroke-linejoin="round"/>' + f'<ellipse cx="172" cy="312" rx="9" ry="20" fill="{K}"/><ellipse cx="228" cy="312" rx="9" ry="20" fill="{K}"/>'
    s += f'<path d="M30 250C22 120 110 40 200 40S378 120 370 250C370 270 352 280 336 280H64C48 280 30 270 30 250Z" fill="{R}" stroke="{K}" stroke-width="10" stroke-linejoin="round"/>'
    s += f'<ellipse cx="200" cy="108" rx="46" ry="38" fill="{I}" stroke="{K}" stroke-width="8"/><ellipse cx="96" cy="206" rx="36" ry="44" fill="{I}" stroke="{K}" stroke-width="8"/><ellipse cx="304" cy="206" rx="36" ry="44" fill="{I}" stroke="{K}" stroke-width="8"/>'
    return s
def emb_pokebola():
    s = f'<circle cx="200" cy="200" r="172" fill="{I}"/><path d="M28 200A172 172 0 0 1 372 200Z" fill="{R}"/>'
    s += f'<rect x="28" y="178" width="344" height="44" fill="{K}"/><circle cx="200" cy="200" r="172" fill="none" stroke="{K}" stroke-width="14"/>'
    s += f'<circle cx="200" cy="200" r="58" fill="{I}" stroke="{K}" stroke-width="16"/><circle cx="200" cy="200" r="22" fill="none" stroke="{K}" stroke-width="8"/>'
    return s
def emb_anillo():
    s = f'<path fill-rule="evenodd" d="M200 34a166 166 0 1 0 0.1 0ZM214 112a96 96 0 1 1 -0.1 0Z" fill="{R}" stroke="{K}" stroke-width="10"/>'
    s += f'<path d="M92 120A140 140 0 0 1 180 62" fill="none" stroke="{I}" stroke-width="14" stroke-linecap="round"/><path d="M262 330A140 140 0 0 0 330 250" fill="none" stroke="{K}" stroke-width="14" stroke-linecap="round"/>'
    return s
def emb_estrella():
    pts = []
    for k in range(10):
        r = 178 if k % 2 == 0 else 86; a = math.radians(-90 + k * 36); pts.append((200 + r * math.cos(a), 210 + r * math.sin(a)))
    s = poly(pts, R, sw=22, extra='')
    s += poly(pts, R, stroke=R, sw=4)
    s += f'<ellipse cx="170" cy="206" rx="12" ry="30" fill="{K}"/><ellipse cx="230" cy="206" rx="12" ry="30" fill="{K}"/>'
    return s
def emb_corazon():
    return f'<path d="M200 352C60 252 40 170 40 128C40 70 84 44 128 44C164 44 190 64 200 92C210 64 236 44 272 44C316 44 360 70 360 128C360 170 340 252 200 352Z" fill="{R}" stroke="{K}" stroke-width="12" stroke-linejoin="round"/><path d="M96 120Q100 90 130 84" fill="none" stroke="{I}" stroke-width="16" stroke-linecap="round"/>'
def emb_fantasma():
    s = f'<path d="M60 360V190C60 100 120 40 200 40S340 100 340 190V360L296 322L248 360L200 322L152 360L104 322Z" fill="{R}" stroke="{K}" stroke-width="12" stroke-linejoin="round"/>'
    s += f'<ellipse cx="150" cy="170" rx="38" ry="48" fill="{I}"/><ellipse cx="250" cy="170" rx="38" ry="48" fill="{I}"/><circle cx="162" cy="178" r="20" fill="{K}"/><circle cx="262" cy="178" r="20" fill="{K}"/>'
    return s
def emb_pacman():
    return f'<path d="M200 200L350 120A175 175 0 1 0 350 280Z" fill="{R}" stroke="{K}" stroke-width="12" stroke-linejoin="round"/><circle cx="215" cy="110" r="20" fill="{K}"/>'
def emb_invader():
    rows = ['00100000100', '00010001000', '00111111100', '01101110110', '11111111111', '10111111101', '10100000101', '00011011000']; u = 32; ox, oy = 24, 72; s = ''
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c == '1': s += f'<rect x="{ox + i * u}" y="{oy + j * u}" width="{u}" height="{u}"/>'
    return f'<g fill="{R}" stroke="{K}" stroke-width="6" shape-rendering="crispEdges">{s}</g>'
def emb_creeper():
    rows = ['11111111', '11111111', '10011001', '10011001', '11100111', '11000011', '11000011', '11011011']; u = 42; ox, oy = 32, 32; s = ''
    for j, r in enumerate(rows):
        for i, c in enumerate(r): s += f'<rect x="{ox + i * u}" y="{oy + j * u}" width="{u}" height="{u}" fill="{R if c == "1" else K}"/>'
    return f'<g shape-rendering="crispEdges">{s}</g><rect x="{ox}" y="{oy}" width="{8 * u}" height="{8 * u}" fill="none" stroke="{K}" stroke-width="12"/>'
def emb_tv():
    s = f'<rect x="40" y="90" width="320" height="230" rx="34" fill="{R}" stroke="{K}" stroke-width="12"/><rect x="72" y="120" width="256" height="170" rx="18" fill="{K}"/>'
    s += f'<polygon points="165,160 165,250 245,205" fill="{R}"/><path d="M130 90L84 36M270 90L316 36" stroke="{R}" stroke-width="16" stroke-linecap="round"/><path d="M120 340H280" stroke="{R}" stroke-width="16" stroke-linecap="round"/>'
    s += f'<path d="M130 90L84 36M270 90L316 36" stroke="{K}" stroke-width="4" stroke-linecap="round"/>'
    return s
def emb_chip():
    s = ''
    for k in range(5):
        p = 98 + k * 51; s += f'<rect x="{p - 9}" y="30" width="18" height="52" fill="{R}" stroke="{K}" stroke-width="5"/><rect x="{p - 9}" y="318" width="18" height="52" fill="{R}" stroke="{K}" stroke-width="5"/><rect x="30" y="{p - 9}" width="52" height="18" fill="{R}" stroke="{K}" stroke-width="5"/><rect x="318" y="{p - 9}" width="52" height="18" fill="{R}" stroke="{K}" stroke-width="5"/>'
    s += f'<rect x="64" y="64" width="272" height="272" rx="28" fill="{R}" stroke="{K}" stroke-width="12"/><rect x="104" y="104" width="192" height="192" rx="14" fill="{K}"/>'
    s += f'<path d="{star4(200, 200, 72, R)}" fill="{R}"/><path d="{star4(262, 138, 24, R)}" fill="{R}"/><path d="{star4(140, 262, 20, R)}" fill="{R}"/>'
    return s
def emb_x():
    return poly([(60, 110), (110, 60), (200, 150), (290, 60), (340, 110), (250, 200), (340, 290), (290, 340), (200, 250), (110, 340), (60, 290), (150, 200)], R, sw=12)
def emb_aguja():
    return poly([(200, 20), (250, 200), (200, 380), (150, 200)], R, sw=10) + f'<polygon points="200,20 250,200 200,200" fill="{K}"/><circle cx="200" cy="200" r="18" fill="{I}" stroke="{K}" stroke-width="8"/>'
EMB = {'triforce': emb_triforce, 'espada': emb_espada, 'hongo': emb_hongo, 'pokebola': emb_pokebola, 'anillo': emb_anillo, 'estrella': emb_estrella, 'corazon': emb_corazon, 'fantasma': emb_fantasma, 'pacman': emb_pacman, 'invader': emb_invader, 'creeper': emb_creeper, 'tv': emb_tv, 'chip': emb_chip, 'x': emb_x, 'aguja': emb_aguja}
def sello(name):
    s = f'<circle cx="300" cy="300" r="292" fill="{K}"/><circle cx="300" cy="300" r="268" fill="none" stroke="{R}" stroke-width="16"/>'
    d = ''
    for k in range(60):
        a = math.radians(k * 6); l0, l1 = (232, 250) if k % 5 == 0 else (240, 250)
        d += f'M{f1(300 + l0 * math.cos(a))} {f1(300 + l0 * math.sin(a))}L{f1(300 + l1 * math.cos(a))} {f1(300 + l1 * math.sin(a))}'
    s += path(d, R, 5) + f'<circle cx="300" cy="300" r="222" fill="none" stroke="{R}" stroke-width="3"/>'
    s += f'<g transform="translate(300 300) scale(.9) translate(-200 -200)">{EMB[name]()}</g>'
    return svg(600, 600, s)
for k in EMB:
    w(f'heroes/{k}.svg', sello(k)); w(f'piezas/{k}.svg', svg(400, 400, EMB[k]()))
print('emblemas', len(EMB))
