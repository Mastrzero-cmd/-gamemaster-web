"""Biblioteca de grabado fino vectorial (v3): curvas de nivel, placas isométricas, circuitos, guilloche,
retículas y objetos gamer/streaming/tech en línea fina. Sin dependencias (solo numpy)."""
import math, random
import numpy as np

W, H = 1600, 900
_id = [0]
def uid(p='c'):
    _id[0] += 1; return f'{p}{_id[0]}'
def f(v): return f'{v:.1f}'.rstrip('0').rstrip('.') if abs(v) < 1e5 else str(int(v))

def style(dark='#070d6a', light='#a9bbff', cyan='#3fdcff', bg='#2b3fd6'):
    return (f'<style>path,circle,rect,line,polygon,ellipse,polyline{{fill:none;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round}}'
            f'.d{{stroke:{dark};stroke-opacity:.62;stroke-width:1}}.d2{{stroke:{dark};stroke-opacity:.72;stroke-width:1.6}}.d3{{stroke:{dark};stroke-opacity:.8;stroke-width:2.4}}'
            f'.l{{stroke:{light};stroke-opacity:.34;stroke-width:1}}.l2{{stroke:{light};stroke-opacity:.5;stroke-width:1.5}}'
            f'.c{{stroke:{cyan};stroke-opacity:.42;stroke-width:1.2}}.c2{{stroke:{cyan};stroke-opacity:.6;stroke-width:1.8}}'
            f'.fd{{fill:{dark};fill-opacity:.2;stroke:none}}.fl{{fill:{light};fill-opacity:.1;stroke:none}}.fdd{{fill:{dark};fill-opacity:.55;stroke:none}}'
            f'.fc{{fill:{cyan};fill-opacity:.55;stroke:none}}.fdl{{fill:{dark};fill-opacity:.5;stroke:none}}.oc{{fill:{bg};fill-opacity:.9;stroke:none}}</style>')

def svg(body, w=W, h=H, defs='', **st):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">{style(**st)}<defs>{defs}</defs>{body}</svg>')

def P(d, c='d'): return f'<path class="{c}" d="{d}"/>'
def poly(pts, c='d', close=False):
    d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ('Z' if close else '')
    return P(d, c)
def circ(x, y, r, c='d'): return f'<circle class="{c}" cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>'
def line(x1, y1, x2, y2, c='d'): return f'<path class="{c}" d="M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}"/>'
def rect(x, y, w, h, c='d', rx=0): return f'<rect class="{c}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}"/>'
def G(body, x=0, y=0, s=1, rot=0, ox=0, oy=0, op=None):
    t = f'translate({f(x)} {f(y)}) rotate({f(rot)}) scale({s}) translate({f(-ox)} {f(-oy)})'
    return f'<g transform="{t}"' + (f' opacity="{op}"' if op else '') + f'>{body}</g>'
def star(x, y, r, c='d'):
    return P(f'M{f(x)} {f(y-r)}C{f(x+r*.12)} {f(y-r*.3)} {f(x+r*.3)} {f(y-r*.12)} {f(x+r)} {f(y)}C{f(x+r*.3)} {f(y+r*.12)} {f(x+r*.12)} {f(y+r*.3)} {f(x)} {f(y+r)}C{f(x-r*.12)} {f(y+r*.3)} {f(x-r*.3)} {f(y+r*.12)} {f(x-r)} {f(y)}C{f(x-r*.3)} {f(y-r*.12)} {f(x-r*.12)} {f(y-r*.3)} {f(x)} {f(y-r)}Z', c)

# ---------------- curvas de nivel (marching squares) ----------------
def field(bumps, nx=200, ny=112, warp=0.0, seed=1, win=True):
    xs = np.linspace(0, W, nx); ys = np.linspace(0, H, ny); X, Y = np.meshgrid(xs, ys)
    r = random.Random(seed); ph = [r.uniform(0, 6.28) for _ in range(4)]
    Xw = X + warp * np.sin(Y / 90 + ph[0]) * 30; Yw = Y + warp * np.sin(X / 110 + ph[1]) * 26
    Z = np.zeros_like(X)
    for (cx, cy, sx, sy, a) in bumps:
        Z += a * np.exp(-(((Xw - cx) / sx) ** 2 + ((Yw - cy) / sy) ** 2))
    Z += 0.05 * np.sin(X / 60 + ph[2]) * np.sin(Y / 70 + ph[3])
    if win:
        wx = np.clip(np.minimum(X, W - X) / 70, 0, 1); wy = np.clip(np.minimum(Y, H - Y) / 70, 0, 1)
        Z = Z * (wx * wy) ** 0.7
    return xs, ys, Z

def contours(xs, ys, Z, levels, c='d', minlen=4, dec=1):
    out = ''
    ny, nx = Z.shape
    for lv in levels:
        segs = []
        B = Z >= lv
        for j in range(ny - 1):
            row = B[j]; row2 = B[j + 1]
            for i in range(nx - 1):
                a, b, cc, d = row[i], row[i + 1], row2[i + 1], row2[i]
                code = a * 8 + b * 4 + cc * 2 + d * 1
                if code in (0, 15): continue
                def pt(e):
                    if e == 0:  # top
                        t = (lv - Z[j, i]) / (Z[j, i + 1] - Z[j, i]); return ('h', i, j, xs[i] + t * (xs[i + 1] - xs[i]), ys[j])
                    if e == 1:  # right
                        t = (lv - Z[j, i + 1]) / (Z[j + 1, i + 1] - Z[j, i + 1]); return ('v', i + 1, j, xs[i + 1], ys[j] + t * (ys[j + 1] - ys[j]))
                    if e == 2:  # bottom
                        t = (lv - Z[j + 1, i]) / (Z[j + 1, i + 1] - Z[j + 1, i]); return ('h', i, j + 1, xs[i] + t * (xs[i + 1] - xs[i]), ys[j + 1])
                    t = (lv - Z[j, i]) / (Z[j + 1, i] - Z[j, i]); return ('v', i, j, xs[i], ys[j] + t * (ys[j + 1] - ys[j]))
                tbl = {1: [(3, 2)], 2: [(2, 1)], 3: [(3, 1)], 4: [(0, 1)], 5: [(0, 3), (2, 1)], 6: [(0, 2)], 7: [(0, 3)], 8: [(0, 3)], 9: [(0, 2)], 10: [(0, 1), (2, 3)], 11: [(0, 1)], 12: [(3, 1)], 13: [(2, 1)], 14: [(3, 2)]}
                for e1, e2 in tbl[code]: segs.append((pt(e1), pt(e2)))
        adj = {}
        for k, (p, q) in enumerate(segs):
            adj.setdefault(p[:3], []).append(k); adj.setdefault(q[:3], []).append(k)
        seen = set(); d = ''
        for k0 in range(len(segs)):
            if k0 in seen: continue
            seen.add(k0); p, q = segs[k0]; chain = [(p[3], p[4]), (q[3], q[4])]
            for direction in (1, 0):
                cur = q if direction else p
                while True:
                    nxt = [k for k in adj[cur[:3]] if k not in seen]
                    if not nxt: break
                    k = nxt[0]; seen.add(k); a, b = segs[k]; other = b if a[:3] == cur[:3] else a
                    if direction: chain.append((other[3], other[4]))
                    else: chain.insert(0, (other[3], other[4]))
                    cur = other
            if len(chain) < minlen: continue
            d += 'M' + 'L'.join(f'{x:.{dec}f} {y:.{dec}f}' for x, y in chain)
        if d: out += P(d, c)
    return out

# ---------------- isométrico ----------------
COS, SIN = math.cos(math.radians(30)), 0.5
def iso(cx, cy, x, y, z=0, s=1): return (cx + (x - y) * COS * s, cy + (x + y) * SIN * s - z * s)

def iso_plate(cx, cy, a, b, t, rings=8, grid=0, hatch=True, fillc='oc', top_c='d', seed=0):
    """caja isométrica: cara superior con anillos concéntricos / retícula, laterales con capas y rayado."""
    A = iso(cx, cy, 0, 0, t); B = iso(cx, cy, a, 0, t); C = iso(cx, cy, a, b, t); D = iso(cx, cy, 0, b, t)
    A0 = iso(cx, cy, 0, 0, 0); B0 = iso(cx, cy, a, 0, 0); C0 = iso(cx, cy, a, b, 0); D0 = iso(cx, cy, 0, b, 0)
    o = poly([A, B, C, D], 'oc', True) + poly([A, B, C, D], 'fl', True)
    o += poly([D, C, C0, D0], 'fd', True) + poly([B, C, C0, B0], 'fd', True)
    o += poly([D, C, C0, D0], 'd2', True) + poly([B, C, C0, B0], 'd2', True) + poly([A, B, C, D], 'd2', True)
    for k in range(1, 4 if t > 10 else 2):  # capas laterales
        z = t * k / (4 if t > 10 else 2); o += line(*iso(cx, cy, 0, b, z), *iso(cx, cy, a, b, z), 'd') + line(*iso(cx, cy, a, 0, z), *iso(cx, cy, a, b, z), 'd')
    if hatch:  # rayado vertical fino en las caras laterales
        n = int(a / 7)
        for k in range(1, n): o += line(*iso(cx, cy, a * k / n, b, t), *iso(cx, cy, a * k / n, b, t * .35 if k % 2 else 0), 'd')
        n = int(b / 7)
        for k in range(1, n): o += line(*iso(cx, cy, a, b * k / n, t), *iso(cx, cy, a, b * k / n, t * .35 if k % 2 else 0), 'd')
    for k in range(1, rings):  # anillos concéntricos (rombos)
        u = k / rings; o += poly([iso(cx, cy, a * (.5 - .5 * (1 - u)) + 0, b * (.5 - .5 * (1 - u)), t), iso(cx, cy, a - a * (.5 * u * 0) - a * (.5 * (1 - u)) * 0 + 0, b * (.5 - .5 * (1 - u)), t)], 'd') if False else ''
        m = (1 - u) * .5
        o += poly([iso(cx, cy, a * m, b * m, t), iso(cx, cy, a * (1 - m), b * m, t), iso(cx, cy, a * (1 - m), b * (1 - m), t), iso(cx, cy, a * m, b * (1 - m), t)], top_c if k % 3 else 'l', True)
    if grid:
        for k in range(1, grid):
            u = k / grid; o += line(*iso(cx, cy, a * u, 0, t), *iso(cx, cy, a * u, b, t), 'l') + line(*iso(cx, cy, 0, b * u, t), *iso(cx, cy, a, b * u, t), 'l')
    return o

def iso_terrain(cx, cy, a, b, t, seed=1, lv=9, nodes=3):
    """placa isométrica con curvas de nivel proyectadas sobre su cara superior"""
    r = random.Random(seed); bumps = [(r.uniform(.2, .8), r.uniform(.2, .8), r.uniform(.12, .3), r.uniform(.12, .3), r.uniform(.6, 1)) for _ in range(nodes)]
    n = 56; us = np.linspace(0, 1, n)
    Xg, Yg = np.meshgrid(us, us); Z = np.zeros_like(Xg)
    for (px, py, sx, sy, am) in bumps: Z += am * np.exp(-(((Xg - px) / sx) ** 2 + ((Yg - py) / sy) ** 2))
    Z *= np.clip(np.minimum(np.minimum(Xg, 1 - Xg), np.minimum(Yg, 1 - Yg)) / .06, 0, 1)
    out = iso_plate(cx, cy, a, b, t, rings=0, hatch=True)
    # contornos en espacio plano -> proyectados
    xs = us * a; ys = us * b
    segs = contours(xs, ys, Z, [Z.max() * (i + 1) / (lv + 1) for i in range(lv)], 'd', minlen=3)
    # reproyectar: parsear path 'M x y L x y ...' y transformar
    import re
    def proj(m):
        d = m.group(1); res = ''
        for sub in d.split('M')[1:]:
            pts = [tuple(map(float, p.split())) for p in sub.split('L')]
            res += 'M' + 'L'.join(f'{iso(cx, cy, px, py, t)[0]:.1f} {iso(cx, cy, px, py, t)[1]:.1f}' for px, py in pts)
        return f'<path class="d" d="{res}"/>'
    out += re.sub(r'<path class="d" d="([^"]*)"/>', proj, segs)
    return out

# ---------------- circuitos ----------------
def bundle(x0, y0, dx1, dy, dx2, n=4, g=7, vertical=False, c='d', pads=True, sgn=1):
    """haz de n pistas paralelas: tramo recto, quiebre a 45° y tramo recto. sgn=-1 va hacia la izquierda."""
    s = 1 if dy > 0 else -1; o = ''
    for k in range(n):
        yk = y0 + k * g * 1; xa = x0 + sgn * dx1 - s * k * g * sgn * -1 * 0
        xa = x0 + sgn * (dx1 - s * k * g * sgn * -1) if False else x0 + sgn * dx1 + sgn * (-s) * k * g * sgn
        pts = [(x0, yk), (xa, yk), (xa + sgn * abs(dy), yk + dy), (xa + sgn * (abs(dy) + dx2), yk + dy)]
        if vertical: pts = [(y, x) for x, y in pts]
        o += poly(pts, c)
        if pads:
            ex, ey = pts[-1]; o += circ(ex, ey, 3.6, c)
            if k % 2 == 0: o += circ(ex, ey, 1.2, 'fdd')
            sx, sy = pts[0]; o += circ(sx, sy, 2.4, c)
    return o

def chip_fp(x, y, w, h, pins=8, c='d', die=True, label=None):
    o = rect(x, y, w, h, 'oc', 4) + rect(x, y, w, h, c + '2' if c == 'd' else c, 4)
    px = w / (pins + 1)
    for k in range(1, pins + 1):
        o += line(x + px * k, y - 11, x + px * k, y, c) + line(x + px * k, y + h, x + px * k, y + h + 11, c)
    py = h / (pins + 1)
    for k in range(1, int(pins * h / w) + 1):
        yy = y + h / (int(pins * h / w) + 1) * k; o += line(x - 11, yy, x, yy, c) + line(x + w, yy, x + w + 11, yy, c)
    if die:
        o += rect(x + w * .22, y + h * .22, w * .56, h * .56, c, 3) + rect(x + w * .32, y + h * .32, w * .36, h * .36, 'l') + circ(x + w * .12, y + h * .14, 3, c)
        o += poly([(x + w * .32, y + h * .5), (x + w * .5, y + h * .5), (x + w * .5, y + h * .68)], 'c')
    return o

def guilloche(cx, cy, R, r, d, turns=None, n=720, c='d', rot=0):
    k = (R - r) / r
    if turns is None:
        from math import gcd
        turns = r // gcd(int(R), int(r)) if float(R).is_integer() and float(r).is_integer() else 6
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * turns * i / n
        x = (R - r) * math.cos(t) + d * math.cos(k * t); y = (R - r) * math.sin(t) - d * math.sin(k * t)
        pts.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
    d_ = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'
    return P(d_, c)

def reticle(x0, y0, x1, y1, step=40, major=5, c='l'):
    o = ''
    xs = np.arange(x0, x1 + 1, step); ys = np.arange(y0, y1 + 1, step)
    for i, x in enumerate(xs): o += line(x, y0, x, y1, 'l2' if i % major == 0 else c)
    for j, y in enumerate(ys): o += line(x0, y, x1, y, 'l2' if j % major == 0 else c)
    for i in range(0, len(xs), major):
        for j in range(0, len(ys), major): o += line(xs[i] - 6, ys[j], xs[i] + 6, ys[j], 'd2') + line(xs[i], ys[j] - 6, xs[i], ys[j] + 6, 'd2')
    return o

def halftone(x0, y0, w, h, step=11, rmax=3.6, dirn='r', c='fdl', seed=2):
    o = ''
    nx, ny = int(w / step), int(h / step)
    for j in range(ny):
        for i in range(nx):
            t = {'r': i / nx, 'l': 1 - i / nx, 'd': j / ny, 'u': 1 - j / ny}[dirn]
            rr = rmax * t
            if rr < .6: continue
            xx = x0 + i * step + (step / 2 if j % 2 else 0); o += f'<circle class="{c}" cx="{f(xx)}" cy="{f(y0 + j * step)}" r="{rr:.1f}"/>'
    return o

def rays(cx, cy, r0, r1, n, c='l', a0=0, a1=360):
    o = ''
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * k / n); o += line(cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a), c)
    return o

def ring_dots(cx, cy, r, n, c='fdl', rr=2):
    return ''.join(circ(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n), rr, c) for k in range(n))

# ---------------- objetos en línea fina (cada uno en caja ~ 400 px) ----------------
CTRL = 'M52 128C52 70 96 46 146 52H254C304 46 348 70 348 128C348 198 336 262 306 262C280 262 270 226 246 202H154C130 226 120 262 94 262C64 262 52 198 52 128Z'
def hatch_clip(body_d, x0, y0, x1, y1, step=7, ang=1, c='d'):
    i = uid('h'); lines = ''
    k = x0 - (y1 - y0)
    while k < x1:
        lines += f'M{k} {y1}L{k + (y1 - y0) * ang} {y0}'; k += step
    return f'<clipPath id="{i}"><path d="{body_d}"/></clipPath><g clip-path="url(#{i})">{P(lines, c)}</g>'

def o_controller():
    o = f'<path class="oc" d="{CTRL}"/>'
    for s, c in ((1, 'd3'), (.94, 'd'), (.88, 'l')): o += f'<g transform="translate(200 150) scale({s}) translate(-200 -150)"><path class="{c}" d="{CTRL}"/></g>'
    o += hatch_clip(CTRL, 52, 150, 140, 265, 6) + hatch_clip(CTRL, 262, 150, 348, 265, 6)
    o += P('M92 66C120 52 170 62 200 62C230 62 280 52 308 66', 'd2') + P('M120 54L128 40H272L280 54', 'd')
    o += poly([(110, 100), (126, 100), (126, 84), (142, 84), (142, 100), (158, 100), (158, 116), (142, 116), (142, 132), (126, 132), (126, 116), (110, 116)], 'd2', True)
    for (x, y) in ((290, 92), (318, 118), (262, 118), (290, 144)): o += circ(x, y, 11, 'd2') + circ(x, y, 15, 'l') + circ(x, y, 5, 'd')
    for (x, y) in ((158, 172), (242, 172)):
        for r, c in ((22, 'd2'), (16, 'd'), (10, 'd'), (4, 'fdd')): o += circ(x, y, r, c)
        o += line(x - 22, y, x + 22, y, 'l') + line(x, y - 22, x, y + 22, 'l')
    o += rect(176, 90, 48, 24, 'd', 8) + line(188, 102, 212, 102, 'd') + circ(200, 140, 4, 'c')
    return o, (400, 290)

def o_handheld():
    o = ''
    for x in (8, 346): o += rect(x, 30, 86, 190, 'oc', 34) + rect(x, 30, 86, 190, 'd2', 34) + rect(x + 8, 38, 70, 174, 'l', 28)
    o += rect(82, 22, 276, 206, 'oc', 16) + rect(82, 22, 276, 206, 'd3', 16) + rect(92, 32, 256, 186, 'd', 11)
    o += rect(104, 42, 232, 166, 'd2', 8)
    for y in range(52, 206, 9): o += line(108, y, 332, y, 'l')
    o += poly([(194, 84), (254, 120), (194, 156)], 'c2', True) + poly([(204, 98), (238, 120), (204, 142)], 'c', True)
    o += circ(50, 92, 20, 'd2') + circ(50, 92, 12, 'd') + circ(390, 152, 20, 'd2') + circ(390, 152, 12, 'd') + circ(50, 92, 4, 'fdd') + circ(390, 152, 4, 'fdd')
    o += line(40, 160, 60, 160, 'd2') + line(50, 150, 50, 170, 'd2')
    for (x, y) in ((378, 76), (402, 76), (378, 100), (402, 100)): o += circ(x, y, 6, 'd2')
    o += hatch_clip('M8 64A34 34 0 0 1 42 30H94V220H42A34 34 0 0 1 8 186Z', 8, 30, 94, 220, 6)
    return o, (440, 250)

def o_cartridge():
    body = 'M40 24H260V270L240 316H60L40 270Z'
    o = f'<path class="oc" d="{body}"/><path class="d3" d="{body}"/>'
    o += f'<g transform="translate(150 170) scale(.93) translate(-150 -170)"><path class="d" d="{body}"/></g>'
    o += rect(66, 48, 168, 128, 'd2', 8) + rect(76, 58, 148, 108, 'l', 4)
    for y in range(70, 166, 9): o += line(80, y, 220, y, 'l')
    o += poly([(112, 142), (150, 82), (188, 142)], 'c2', True) + circ(196, 100, 10, 'c')
    o += rect(66, 196, 168, 20, 'd', 6)
    for x in range(70, 232, 8): o += line(x, 196, x, 216, 'd')
    for x in range(80, 222, 7): o += line(x, 276, x, 306, 'd')
    o += line(40, 270, 260, 270, 'd2') + line(60, 316, 60, 270, 'd') + line(240, 316, 240, 270, 'd')
    return o, (300, 340)

def o_screen():
    o = rect(20, 20, 400, 260, 'oc', 26) + rect(20, 20, 400, 260, 'd3', 26) + rect(30, 30, 380, 240, 'd', 20) + rect(46, 44, 348, 212, 'd2', 12)
    for y in range(52, 250, 8): o += line(50, y, 390, y, 'l')
    o += circ(220, 150, 56, 'c') + circ(220, 150, 44, 'c2') + poly([(204, 122), (254, 150), (204, 178)], 'c2', True)
    for r in (70, 84): o += P(f'M{220 - r} 150A{r} {r} 0 0 1 {220 - r * .5} {150 - r * .87}', 'l')
    o += P('M150 296H290L306 326H134Z', 'oc') + P('M150 296H290L306 326H134Z', 'd2') + line(150, 280, 150, 296, 'd2') + line(290, 280, 290, 296, 'd2')
    for x in range(160, 290, 10): o += line(x, 304, x - 3, 322, 'd')
    o += circ(380, 270, 3.5, 'c')
    return o, (440, 340)

def o_chip(n=7):
    o = ''; sz = 240; x0 = 50
    for k in range(n):
        p = x0 + 28 + k * (sz - 56) / (n - 1)
        for (a, b) in ((p, 4), (p, 276)): o += rect(a - 6, b - 0, 12, 48 if b < 100 else 48, 'd', 2) if False else ''
        o += rect(p - 6, 6, 12, 44, 'd', 2) + rect(p - 6, 286, 12, 44, 'd', 2) + rect(6, p - 6 + 0 if True else 0, 44, 12, 'd', 2) + rect(286, p - 6, 44, 12, 'd', 2)
    o = o.replace('', '')
    o += rect(40, 40, 256, 256, 'oc', 26) + rect(40, 40, 256, 256, 'd3', 26) + rect(52, 52, 232, 232, 'd', 18)
    o += rect(84, 84, 168, 168, 'd2', 12) + rect(98, 98, 140, 140, 'l', 8)
    o += P('M110 140H170V108M226 140H190M110 168H146V206H190M226 168V210M110 196H130M200 108V130', 'c2') + circ(170, 106, 6, 'c') + circ(226, 212, 6, 'c') + circ(130, 196, 5, 'c')
    o += poly([(52, 76), (76, 52)], 'd2')
    for k in range(5): o += rect(118 + k * 22, 220, 14, 8, 'd')
    return o, (336, 336)

def o_headset():
    arc = 'M62 212C46 92 112 30 180 30S314 92 298 212'
    o = f'<path class="d3" d="{arc}" style="stroke-width:7"/>' + f'<path class="oc" d="{arc}" style="fill:none;stroke:#2b3fd6;stroke-opacity:.9;stroke-width:5;vector-effect:non-scaling-stroke"/>'
    o += P(arc, 'd2') + f'<g transform="translate(180 124) scale(.88) translate(-180 -124)">' + P(arc, 'l') + '</g>'
    for x in (22, 252):
        o += rect(x, 170, 86, 150, 'oc', 32) + rect(x, 170, 86, 150, 'd3', 32) + rect(x + 10, 182, 66, 126, 'd', 24) + rect(x + 22, 198, 42, 94, 'l', 16)
        for y in range(206, 288, 8): o += line(x + 26, y, x + 60, y, 'd')
        o += circ(x + 43, 245, 7, 'c')
    o += P('M65 300C60 340 90 352 140 346', 'd2') + rect(138, 336, 26, 16, 'd2', 8) + circ(151, 344, 3, 'c')
    return o, (360, 360)

def o_clapper():
    o = rect(24, 100, 340, 200, 'oc', 8) + rect(24, 100, 340, 200, 'd3', 8) + rect(40, 150, 308, 134, 'd', 4)
    for y in (190, 230, 262): o += line(40, y, 348, y, 'l')
    o += circ(190, 220, 28, 'c') + poly([(182, 206), (206, 220), (182, 234)], 'c2', True)
    o += P('M24 100L348 40L364 100', 'oc') + P('M24 100L348 40L364 100Z', 'd3')
    o += rect(24, 100, 340, 36, 'd2', 4)
    for k in range(7):
        x = 24 + k * 50; o += poly([(x, 136), (x + 30, 136), (x + 52, 100), (x + 22, 100)], 'fdl' if k % 2 == 0 else 'd', True)
    for k in range(6):
        x = 40 + k * 52; o += poly([(x, 100), (x + 26, 100), (x + 38, 68), (x + 12, 74)], 'fdl' if k % 2 == 0 else 'd', True)
    o += circ(40, 100, 5, 'd2')
    return o, (390, 310)

def o_play():
    o = ''
    for r, c in ((124, 'l'), (108, 'd'), (96, 'd3')): o += circ(130, 130, r, c)
    o += circ(130, 130, 88, 'oc') + circ(130, 130, 88, 'd2') + circ(130, 130, 76, 'l')
    o += poly([(104, 86), (176, 130), (104, 174)], 'oc', True) + poly([(104, 86), (176, 130), (104, 174)], 'c2', True) + poly([(116, 106), (152, 130), (116, 154)], 'c', True)
    o += ring_dots(130, 130, 116, 36, 'fdl', 1.6)
    return o, (260, 260)

def o_cloud():
    body = 'M80 220C30 220 14 160 62 146C58 94 124 70 158 108C178 56 262 56 280 116C340 106 362 188 308 220Z'
    o = f'<path class="oc" d="{body}"/><path class="d3" d="{body}"/><g transform="translate(190 150) scale(.9) translate(-190 -150)"><path class="d" d="{body}"/></g><g transform="translate(190 150) scale(.8) translate(-190 -150)"><path class="l" d="{body}"/></g>'
    o += hatch_clip(body, 20, 100, 360, 222, 8, 1, 'd')
    for k, x in enumerate((130, 190, 250)):
        o += rect(x - 22, 250, 44, 62, 'oc', 3) + rect(x - 22, 250, 44, 62, 'd2', 3)
        for y in (262, 276, 290): o += line(x - 14, y, x + 6, y, 'd') + circ(x + 14, y, 2.2, 'c')
        o += line(x, 222, x, 250, 'c' if k == 1 else 'd')
    return o, (380, 320)

def o_server():
    o = ''
    for k in range(4):
        y = 20 + k * 62; o += rect(20, y, 260, 52, 'oc', 5) + rect(20, y, 260, 52, 'd2', 5)
        for x in range(60, 200, 12): o += line(x, y + 12, x, y + 40, 'd')
        o += circ(244, y + 18, 5, 'c') + circ(260, y + 18, 5, 'd') + line(36, y + 26, 48, y + 26, 'd2') + rect(206, y + 32, 56, 8, 'l', 3)
    return o, (300, 280)

def o_console():
    body = 'M40 120C40 60 80 34 130 34H270C320 34 360 60 360 120V150C360 190 330 210 290 210H110C70 210 40 190 40 150Z'
    o = f'<path class="oc" d="{body}"/><path class="d3" d="{body}"/><g transform="translate(200 120) scale(.93) translate(-200 -120)"><path class="d" d="{body}"/></g>'
    o += circ(200, 100, 52, 'd2') + circ(200, 100, 40, 'd') + circ(200, 100, 22, 'l') + circ(200, 100, 5, 'c')
    for k in range(7): o += line(90 + k * 10, 168, 90 + k * 10, 192, 'd') + line(250 + k * 10, 168, 250 + k * 10, 192, 'd')
    o += rect(176, 184, 48, 8, 'd2', 4) + circ(80, 70, 3.5, 'c')
    return o, (400, 240)

def o_neural(seed=3, layers=(3, 5, 5, 3), w=340, h=240):
    r = random.Random(seed); xs = [w * (k + .5) / len(layers) for k in range(len(layers))]; nodes = []
    for k, n in enumerate(layers): nodes.append([(xs[k], h * (j + .5) / n + r.uniform(-6, 6)) for j in range(n)])
    o = ''
    for a, b in zip(nodes, nodes[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b: o += line(x1, y1, x2, y2, 'l')
    for col in nodes:
        for (x, y) in col: o += circ(x, y, 9, 'oc') + circ(x, y, 9, 'd2') + circ(x, y, 3.5, 'c')
    return o, (w, h)

def o_disc():
    o = ''
    for r in range(18, 140, 9): o += circ(150, 150, r, 'd' if r % 18 else 'l')
    o += circ(150, 150, 150, 'd3') + circ(150, 150, 40, 'oc') + circ(150, 150, 40, 'd2') + circ(150, 150, 12, 'oc') + circ(150, 150, 12, 'd2')
    o += P('M60 70A110 110 0 0 1 140 40', 'c2')
    return o, (300, 300)

def o_wifi():
    o = ''
    for r in (30, 60, 90, 120): o += P(f'M{150 - r} {150 - r * .2}A{r} {r} 0 0 1 {150 + r} {150 - r * .2}', 'd2' if r % 60 else 'c2')
    o += circ(150, 150, 8, 'fc')
    return o, (300, 170)

OBJ = dict(controller=o_controller, handheld=o_handheld, cartridge=o_cartridge, screen=o_screen, chip=o_chip, headset=o_headset,
           clapper=o_clapper, play=o_play, cloud=o_cloud, server=o_server, console=o_console, neural=o_neural, disc=o_disc, wifi=o_wifi)
def obj(name, cx, cy, width, rot=0, op=None, **kw):
    body, (w, h) = OBJ[name](**kw) if kw else OBJ[name]()
    s = width / w
    return G(body, cx, cy, s, rot, w / 2, h / 2, op)

def scatter(r, names, n, wr, placed, area=(60, 60, W - 60, H - 60), gap=1.0, rot=14, op=None):
    """coloca n objetos pequeños sin encimarse (rechazo por distancia)"""
    o = ''; tries = 0; k = 0
    while k < n and tries < 600:
        tries += 1; w = r.uniform(*wr); x = r.uniform(area[0], area[2]); y = r.uniform(area[1], area[3])
        if any((x - px) ** 2 + (y - py) ** 2 < ((w + pw) * .5 * gap) ** 2 for px, py, pw in placed): continue
        placed.append((x, y, w)); nm = names[k % len(names)]
        o += obj(nm, x, y, w, r.uniform(-rot, rot), op)
        k += 1
    return o
