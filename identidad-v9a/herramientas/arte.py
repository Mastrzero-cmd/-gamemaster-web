#!/usr/bin/env python3
"""Genera el arte de v9a «Grabado»: planos azules (solo azul, trazo fino tipo billete), capas rojas (íconos + bisel) y cortes.
Uso: python3 arte.py  → escribe assets/{planos,heroes,piezas,cortes,sellos}/*.svg"""
import math, random, os
from iconos import ICONOS, g, svg_icono, R, K
BL = '#1616FF'
W, H, CX, CY, HOLE = 1440, 760, 720, 380, 358
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
def wr(sub, name, s):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True); open(os.path.join(OUT, sub, name), 'w').write(s)

class Lienzo:
    def __init__(self, hole=True, seed=1, cx=CX, cy=CY):
        self.L = []; self.W = []; self.hole = hole; self.rng = random.Random(seed); self.cx, self.cy = cx, cy
    def ok(self, x, y):
        if x < -20 or x > W + 20 or y < -20 or y > H + 20: return False
        return not (self.hole and (x - self.cx) ** 2 + (y - self.cy) ** 2 < HOLE ** 2)
    def poly(self, pts, w=1.1):
        run = []
        for p in pts:
            if self.ok(*p): run.append(p)
            else:
                if len(run) > 1: self.L.append((w, run))
                run = []
        if len(run) > 1: self.L.append((w, run))
    def svg(self):
        by = {}
        for w, r in self.L: by.setdefault(w, []).append('M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in r))
        body = ''.join(f'<path d="{"".join(v)}" stroke-width="{w}"/>' for w, v in sorted(by.items()))
        if self.W: body += '<path fill="%s" stroke="none" d="%s"/>' % (BL, ''.join('M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in p) + 'Z' for p in self.W))
        if self.W: body += '<path fill="%s" stroke="none" d="%s"/>' % (BL, ''.join('M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in p) + 'Z' for p in self.W))
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="none" stroke="{BL}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'

    def guilloche(self, cx, cy, S, k, d, copies, w=.8, rot0=0, n=360, sq=1.0):
        """epitrocoide cerrada: (1-1/k)e^{it}+d e^{-i(k-1)t}; 'copies' giros para formar la roseta de billete"""
        for c in range(copies):
            rot = rot0 + c * (2 * math.pi / k) / copies
            pts = []
            for i in range(n + 1):
                t = 2 * math.pi * i / n
                x = (1 - 1 / k) * math.cos(t) + d * math.cos((k - 1) * t); y = (1 - 1 / k) * math.sin(t) - d * math.sin((k - 1) * t)
                pts.append((cx + S * (x * math.cos(rot) - y * math.sin(rot)), cy + S * sq * (x * math.sin(rot) + y * math.cos(rot))))
            self.poly(pts, w)
    def wedge(self, cx, cy, r0, r1, n, half=.012, skip=0):
        """rayos como cuñas sólidas (grabado a pleno): triángulos delgados rellenos de azul"""
        for i in range(n):
            if skip and i % skip == 0: continue
            a = 2 * math.pi * i / n; ww = half * (1.6 if i % 3 == 0 else 1)
            pts = [(cx + r0 * math.cos(a - ww * .4), cy + r0 * math.sin(a - ww * .4)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a)), (cx + r0 * math.cos(a + ww * .4), cy + r0 * math.sin(a + ww * .4)), (cx + r0 * math.cos(a - ww * .4), cy + r0 * math.sin(a - ww * .4))]
            if all(self.ok(*p) for p in pts): self.W.append(pts)
    def guilloche(self, cx, cy, S, k, d, copies, w=.8, rot0=0, n=360):
        """epitrocoide cerrada (1-1/k)e^{it}+d e^{-i(k-1)t}, repetida con giros: roseta de billete"""
        for c in range(copies):
            rot = rot0 + c * (2 * math.pi / k) / copies; pts = []
            for i in range(n + 1):
                t = 2 * math.pi * i / n
                x = (1 - 1 / k) * math.cos(t) + d * math.cos((k - 1) * t); y = (1 - 1 / k) * math.sin(t) - d * math.sin((k - 1) * t)
                pts.append((cx + S * (x * math.cos(rot) - y * math.sin(rot)), cy + S * (x * math.sin(rot) + y * math.cos(rot))))
            self.poly(pts, w)
    def wedge(self, cx, cy, r0, r1o, n, half=.012):
        """rayos como cuñas sólidas finas (grabado a pleno), recortadas al lienzo"""
        for i in range(n):
            a = 2 * math.pi * i / n + .003; ww = half * (1.6 if i % 3 == 0 else 1); ca, sa = math.cos(a), math.sin(a)
            lim = min((W - cx) / ca if ca > 1e-6 else (-cx / ca if ca < -1e-6 else 1e9), (H - cy) / sa if sa > 1e-6 else (-cy / sa if sa < -1e-6 else 1e9))
            r1 = min(r1o, lim - 2)
            if r1 <= r0 + 5: continue
            self.W.append([(cx + r0 * math.cos(a - ww), cy + r0 * math.sin(a - ww)), (cx + r1 * ca, cy + r1 * sa), (cx + r0 * math.cos(a + ww), cy + r0 * math.sin(a + ww))])
    # ---- primitivas de grabado ----
    def ring(self, cx, cy, r, w=1.1, a0=0, a1=2 * math.pi, n=240):
        self.poly([(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)], w)
    def wavering(self, cx, cy, r, amp, k, ph=0, w=1.0, n=420):
        self.poly([(cx + (r + amp * math.sin(k * t + ph)) * math.cos(t), cy + (r + amp * math.sin(k * t + ph)) * math.sin(t)) for t in [2 * math.pi * i / n for i in range(n + 1)]], w)
    def rosette(self, cx, cy, r0, r1, rings, k, amp, w=0.9, twist=.35):
        for j in range(rings):
            r = r0 + (r1 - r0) * j / max(1, rings - 1)
            self.wavering(cx, cy, r, amp * (0.4 + .6 * j / rings), k, ph=j * twist, w=w)
    def rays(self, cx, cy, r0, r1, n, w=1.0, jit=.5, wide=None, a0=0, a1=2 * math.pi):
        for i in range(n):
            a = a0 + (a1 - a0) * i / n; L = r1 - (r1 - r0) * jit * self.rng.random() * (1 if i % 2 else .3)
            ww = wide if (wide and i % 5 == 0) else w
            self.poly([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + L * math.cos(a), cy + L * math.sin(a))], ww)
    def contour(self, cx, cy, r0, r1, count, harm, w=1.0, n=240):
        for j in range(count):
            r = r0 + (r1 - r0) * j / max(1, count - 1); f = .3 + j / count
            self.poly([(cx + (r + f * sum(a * math.sin(k * t + p) for a, k, p in harm)) * math.cos(t), cy + (r + f * sum(a * math.sin(k * t + p) for a, k, p in harm)) * math.sin(t)) for t in [2 * math.pi * i / n for i in range(n + 1)]], w)
    def waves(self, y0, rows, dy, amp, f, x0=0, x1=W, w=1.0, ph=.4, tilt=0):
        for i in range(rows):
            A = amp * (.35 + .65 * math.sin(math.pi * (i + 1) / (rows + 1)))
            self.poly([(x, y0 + i * dy + A * math.sin(x * f + i * ph) + A * .4 * math.sin(x * f * 2.3 + i) + (x - W / 2) * tilt) for x in range(int(x0), int(x1) + 1, 6)], w + (.5 if i % 4 == 0 else 0))
    def hatch(self, x0, y0, x1, y1, gap, ang, w=.9, cond=None):
        d = math.hypot(x1 - x0, y1 - y0); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; ux, uy = math.cos(ang), math.sin(ang)
        k = -d / 2
        while k < d / 2:
            ox, oy = cx - uy * k, cy + ux * k; pts = [(ox + ux * t, oy + uy * t) for t in range(int(-d / 2), int(d / 2), 8)]
            pts = [p for p in pts if x0 <= p[0] <= x1 and y0 <= p[1] <= y1 and (cond is None or cond(*p))]
            if len(pts) > 1: self.poly(pts, w)
            k += gap
    def stars(self, n, minr=0, w=1.1, zone=None):
        for _ in range(n):
            x, y = self.rng.uniform(10, W - 10), self.rng.uniform(10, H - 10)
            if zone and not zone(x, y): continue
            s = self.rng.choice([5, 8, 12, 17]); self.poly([(x - s, y), (x + s, y)], w); self.poly([(x, y - s), (x, y + s)], w)
            if s > 8: self.poly([(x - s * .5, y - s * .5), (x + s * .5, y + s * .5)], w * .8); self.poly([(x - s * .5, y + s * .5), (x + s * .5, y - s * .5)], w * .8)
    def constel(self, pts, w=1.0, link=170):
        for i, (x, y) in enumerate(pts):
            self.ring(x, y, 5, 1.6, n=18)
            for (u, v) in pts[i + 1:]:
                if math.hypot(u - x, v - y) < link:
                    mx, my = (x + u) / 2 + (v - y) * .12, (y + v) / 2 - (u - x) * .12
                    self.poly([((1 - t) ** 2 * x + 2 * t * (1 - t) * mx + t * t * u, (1 - t) ** 2 * y + 2 * t * (1 - t) * my + t * t * v) for t in [i / 16 for i in range(17)]], w)
    def gear(self, cx, cy, r, teeth, w=1.2, spokes=6):
        pts = []
        for i in range(teeth * 4 + 1):
            a = 2 * math.pi * i / (teeth * 4); rr = r * (1.14 if i % 4 in (1, 2) else 1.0); pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.poly(pts, w + .6)
        for f in (.72, .66, .3, .22): self.ring(cx, cy, r * f, w, n=90)
        for i in range(spokes):
            a = 2 * math.pi * i / spokes; self.poly([(cx + r * .3 * math.cos(a), cy + r * .3 * math.sin(a)), (cx + r * .66 * math.cos(a), cy + r * .66 * math.sin(a))], w)

# ------------------------------------------------------------------ PLANOS (azul)
def plano_inicio():
    c = Lienzo(seed=3)
    c.guilloche(CX, CY, 700, 13, .15, 26, w=.8, n=300)
    c.guilloche(CX, CY, 520, 17, .09, 24, w=.8, rot0=.1, n=260)
    c.wedge(CX, CY, 392, 450, 90, half=.022)
    for r in (366, 374, 382): c.ring(CX, CY, r, 1.2 if r < 382 else .8)
    c.stars(26, w=1.0, zone=lambda x, y: math.hypot(x - CX, y - CY) > 360)
    return c.svg()
def plano_marcas():
    c = Lienzo(seed=5)
    c.contour(CX, CY, 350, 880, 34, [(16, 3, .5), (10, 5, 1.7), (6, 9, .2), (4, 13, 2.2)], w=1.0)
    for (x, y) in [(120, 110), (1320, 110), (120, 650), (1320, 650)]: c.guilloche(x, y, 100, 9, .14, 12, w=.9, n=110); c.ring(x, y, 112, 1.2, n=90)
    for r in (366, 373): c.ring(CX, CY, r, 1.2)
    return c.svg()
def plano_catalogo():
    c = Lienzo(seed=7)
    c.waves(40, 34, 22, 22, .011, w=.9, ph=.5)
    c.wedge(CX, CY, 380, 900, 130, half=.0095)
    for r in (366, 374): c.ring(CX, CY, r, 1.3)
    c.guilloche(150, 130, 90, 11, .15, 14, w=.9, n=150); c.guilloche(1290, 640, 100, 11, .15, 14, w=.9, n=150)
    return c.svg()
def plano_streaming():
    c = Lienzo(seed=11)
    for cx0 in (-120, W + 120):
        for j in range(30): c.ring(cx0, CY, 330 + j * 15, 1.0 + (.5 if j % 5 == 0 else 0), a0=-1.15 if cx0 < 0 else math.pi - 1.15, a1=1.15 if cx0 < 0 else math.pi + 1.15, n=120)
    c.waves(30, 5, 12, 20, .02, x0=380, x1=1060, w=1.0)
    c.waves(H - 90, 6, 12, 26, .017, x0=330, x1=1110, w=1.0, ph=.8)
    c.guilloche(150, CY, 105, 12, .16, 14, w=.9, n=120); c.guilloche(1290, CY, 105, 12, .16, 14, w=.9, n=120)
    c.stars(16, w=1.0, zone=lambda x, y: math.hypot(x - CX, y - CY) > 380)
    for r in (366, 373): c.ring(CX, CY, r, 1.2)
    return c.svg()
def plano_ia():
    c = Lienzo(seed=13)
    rng = random.Random(21); pts = []
    tries = 0
    while len(pts) < 20 and tries < 6000:
        tries += 1
        x, y = rng.uniform(60, W - 60), rng.uniform(60, H - 60)
        if math.hypot(x - CX, y - CY) > 410 and all(math.hypot(x - u, y - v) > 120 for u, v in pts): pts.append((x, y))
    c.constel(pts, link=300, w=1.1)
    for (x, y) in pts[::2]: c.guilloche(x, y, 38, 7, .2, 8, w=.9, n=70)
    c.rosette(CX, CY, 346, 470, 14, 24, 5, w=.8, twist=.5)
    for r in (366, 373): c.ring(CX, CY, r, 1.2)
    c.stars(24, w=.9, zone=lambda x, y: math.hypot(x - CX, y - CY) > 380)
    return c.svg()
def plano_logo():
    c = Lienzo(seed=17)
    for (x, y, r, t) in [(150, 150, 120, 12), (1290, 600, 150, 14), (1230, 140, 70, 9), (210, 640, 80, 10), (720, 24, 60, 8), (720, 740, 70, 9)]: c.gear(x, y, r, t)
    c.guilloche(CX, CY, 520, 15, .12, 22, w=.8, n=240)
    for r in (366, 373): c.ring(CX, CY, r, 1.2)
    return c.svg()
def plano_sistema():
    c = Lienzo(seed=19)
    c.contour(CX, CY, 350, 900, 40, [(20, 2, 1), (12, 4, .3), (8, 7, 2.2), (4, 11, 1)], w=1.0)
    c.guilloche(CX, CY, 440, 11, .18, 20, w=.8, n=240)
    for r in (366, 373): c.ring(CX, CY, r, 1.2)
    return c.svg()
def plano_cierre():
    c = Lienzo(seed=23)
    c.wedge(CX, CY, 380, 1000, 240, half=.008)
    c.guilloche(CX, CY, 470, 19, .08, 22, w=.8, n=300)
    for r in (366, 373): c.ring(CX, CY, r, 1.2)
    return c.svg()
def plano_sellos():
    c = Lienzo(hole=False, seed=29)
    c.guilloche(CX, CY, 480, 15, .14, 18, w=.8, n=180); c.guilloche(CX, CY, 360, 13, .12, 16, w=.8, n=160, rot0=.2); c.guilloche(CX, CY, 250, 11, .1, 14, w=.8, n=140)
    return c.svg()
PLANOS = dict(inicio=plano_inicio, marcas=plano_marcas, catalogo=plano_catalogo, streaming=plano_streaming, ia=plano_ia, logo=plano_logo, sistema=plano_sistema, cierre=plano_cierre)

# ------------------------------------------------------------------ CAPAS ROJAS
def bisel(n=96, r=320, w=30):
    d = ''
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = a0 + 2 * math.pi / n * (.62 if i % 4 else .34)
        d += f'M{CX + r * math.cos(a0):.1f} {CY + r * math.sin(a0):.1f}A{r} {r} 0 0 1 {CX + r * math.cos(a1):.1f} {CY + r * math.sin(a1):.1f}'
    return f'<path d="{d}" fill="none" stroke="{K}" stroke-width="{w + 8}" stroke-linecap="butt"/><path d="{d}" fill="none" stroke="{R}" stroke-width="{w}" stroke-linecap="butt"/>'
def heroe(icon, s=1.9, extra=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{bisel()}<circle cx="{CX}" cy="{CY}" r="300" fill="none" stroke="{K}" stroke-width="7"/><circle cx="{CX}" cy="{CY}" r="300" fill="none" stroke="{R}" stroke-width="2.4"/>{g(icon, CX, CY + 6, s)}{extra}</svg>'
def piezas(lst):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">' + ''.join(g(n, x, y, s, r) for n, x, y, s, r in lst) + '</svg>'
HEROES = dict(inicio=('triforce', 2.7), marcas=('pacman', 2.7), catalogo=('hongo', 2.8), streaming=('pantalla', 2.8), ia=('neuronal', 2.6), logo=('pokebola', 2.6), sistema=('anillo', 2.8), cierre=('espada', 2.3))
PIEZAS = dict(
    inicio=[('corazon', 190, 150, 0.65, -12), ('rupia', 1260, 170, 0.62, 10), ('ocarina', 230, 600, 0.70, 8), ('estrella', 1230, 620, 0.65, -8), ('hongo', 90, 380, 0.46, 0)],
    marcas=[('fantasma', 200, 160, 0.70, -8), ('fantasma', 1250, 600, 0.65, 8), ('invasor', 1230, 150, 0.78, 0), ('pacman', 230, 610, 0.46, 0)],
    catalogo=[('bloque', 200, 150, 0.65, -6), ('estrella', 1240, 160, 0.65, 10), ('tuberia', 220, 610, 0.65, 0), ('pokebola', 1240, 610, 0.62, 12), ('corazon', 100, 390, 0.40, 0)],
    streaming=[('invasor', 190, 170, 0.78, 0), ('onda', 1250, 160, 0.85, 0), ('pantalla', 200, 600, 0.54, -8), ('kirby', 1240, 600, 0.62, 0)],
    ia=[('chip', 190, 160, 0.78, 0), ('onda', 1250, 160, 0.78, 0), ('amongus', 220, 610, 0.65, -8), ('tetris', 1240, 610, 0.62, 8)],
    logo=[('pikachu', 200, 160, 0.70, -6), ('creeper', 1240, 160, 0.62, 0), ('anillo', 220, 610, 0.54, 0), ('kirby', 1240, 600, 0.59, 0)],
    sistema=[('triforce', 200, 150, 0.62, 0), ('hongo', 1240, 160, 0.62, 0), ('pokebola', 220, 610, 0.56, 0), ('espada', 1240, 600, 0.65, 20)],
    cierre=[('estrella', 200, 150, 0.70, -10), ('corazon', 1250, 160, 0.70, 8), ('tetris', 220, 610, 0.59, 0), ('pikachu', 1240, 610, 0.62, 0)])

# ------------------------------------------------------------------ CORTES (azul, teselables en x)
def corte_ondas(w=240, h=96):  # guilloché de olas entrelazadas
    c = Lienzo(hole=False); c.L = []
    L = []
    for j in range(9):
        L.append((1.0 + (.5 if j in (0, 8) else 0), [(x, h / 2 + (14 + j * 1.2) * math.sin(x / w * 2 * math.pi + j * .35) * math.cos(j * .4)) for x in range(0, w + 1, 4)]))
    for j in range(9):
        L.append((.9, [(x, h / 2 + (30 - j * 2.4) * math.sin(x / w * 4 * math.pi + j * .5)) for x in range(0, w + 1, 3)]))
    return tile(L, w, h)
def corte_abanico(w=120, h=96):  # escamas concéntricas
    L = []
    for cx in (0, w / 2, w):
        for j in range(1, 9): L.append((1.0, [(cx + j * 6.5 * math.cos(t), h + 2 - j * 6.5 * math.sin(t) * 1.25) for t in [math.pi * i / 36 for i in range(37)]]))
    for cx in (w / 4, 3 * w / 4):
        for j in range(1, 9): L.append((1.0, [(cx + j * 6.5 * math.cos(t), h - 26 - j * 6.5 * math.sin(t) * 1.25) for t in [math.pi * i / 36 for i in range(37)]]))
    return tile(L, w, h)
def corte_cuerda(w=96, h=96):  # cuerda trenzada
    L = []
    for j in range(7):
        L.append((1.4, [(x, h / 2 + (j - 3) * 4 + 20 * math.sin(x / w * 2 * math.pi + j * .22)) for x in range(0, w + 1, 3)]))
        L.append((1.4, [(x, h / 2 + (j - 3) * 4 - 20 * math.sin(x / w * 2 * math.pi + j * .22)) for x in range(0, w + 1, 3)]))
    return tile(L, w, h)
def corte_estrias(w=160, h=96):  # haces de líneas finas que crecen y se adelgazan
    L = []
    for i in range(0, w, 5):
        a = abs(math.sin(i / w * math.pi)) * 40 + 4
        L.append((1.1, [(i, h / 2 - a), (i, h / 2 + a)]))
    L.append((1.6, [(0, 6), (w, 6)])); L.append((1.6, [(0, h - 6), (w, h - 6)]))
    return tile(L, w, h)
def corte_constela(w=300, h=96):
    L = []; rng = random.Random(4); pts = [(rng.uniform(10, w - 10), rng.uniform(14, h - 14)) for _ in range(7)]; pts.sort()
    for i, (x, y) in enumerate(pts):
        L.append((1.2, [(x + 5 * math.cos(t), y + 5 * math.sin(t)) for t in [2 * math.pi * k / 16 for k in range(17)]]))
        if i: L.append((1.0, [pts[i - 1], (x, y)]))
        L.append((1.0, [(x - 11, y), (x + 11, y)])); L.append((1.0, [(x, y - 11), (x, y + 11)]))
    L.append((1.0, [(0, h / 2), (pts[0][0], pts[0][1])])); L.append((1.0, [(pts[-1][0], pts[-1][1]), (w, h / 2)]))
    return tile(L, w, h)
def tile(L, w, h):
    body = ''.join(f'<path d="M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in p) + f'" stroke-width="{sw}"/>' for sw, p in L)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" stroke="{BL}" stroke-linecap="round">{body}</svg>'
CORTES = dict(ondas=corte_ondas, abanico=corte_abanico, cuerda=corte_cuerda, estrias=corte_estrias, constela=corte_constela)

if __name__ == '__main__':
    for n, f in PLANOS.items(): wr('planos', n + '.svg', f())
    wr('planos', 'sellos.svg', plano_sellos())
    for n, (ic, s) in HEROES.items(): wr('heroes', n + '.svg', heroe(ic, s))
    for n, l in PIEZAS.items(): wr('piezas', n + '.svg', piezas(l))
    for n, f in CORTES.items(): wr('cortes', n + '.svg', f())
    for n in ICONOS: wr('sellos', n + '.svg', svg_icono(n))
    print('arte generado')
