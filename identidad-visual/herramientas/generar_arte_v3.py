#!/usr/bin/env python3
"""Arte v3 de los campos azules: grabado fino vectorial distinto por sección (2 capas: fondo y objetos).
Uso: python3 generar_arte_v3.py ../assets/arte"""
import sys, os, random, math
sys.path.insert(0, os.path.dirname(__file__))
from arte_lib import *

OUT = {}
def save(name, body, defs='', **st): OUT[name] = svg(body, defs=defs, **st)

def topo_bumps(r, n, xr=(0, W), yr=(0, H), sx=(120, 260), sy=(80, 170)):
    return [(r.uniform(*xr), r.uniform(*yr), r.uniform(*sx), r.uniform(*sy), r.uniform(.6, 1.0)) for _ in range(n)]

def mask_fade(idn, x0, y0, x1, y1):
    return f'<linearGradient id="{idn}g" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'

# ============ 1 · HERO (fijo): horizonte, órbitas, estrellas, terreno de nivel ============
def hero():
    r = random.Random(21); hz = 410; b = ''
    for _ in range(70): b += star(r.uniform(30, W - 30), r.uniform(20, hz - 30), r.choice([3, 4, 5, 7, 10]), r.choice(['d', 'd', 'l2']))
    for k, rad in enumerate((150, 230, 320, 420)): b += circ(1130, 250, rad, 'l' if k % 2 else 'd') 
    b += ring_dots(1130, 250, 150, 48, 'fdl', 1.8) + ring_dots(1130, 250, 320, 90, 'fdl', 1.4) + rays(1130, 250, 160, 225, 72, 'l')
    b += circ(1130, 250, 96, 'd2') + circ(1130, 250, 70, 'l') + circ(1130, 250, 44, 'd')
    b += P(f'M0 {hz}H{W}', 'd3')
    for i in range(-16, 17): b += line(W / 2 + i * 40, hz, W / 2 + i * 210, H, 'd')
    y, step = hz, 7
    while y < H:
        y += step; step *= 1.2; b += line(0, y, W, y, 'd' if step < 30 else 'd2')
    xs, ys, Z = field(topo_bumps(r, 5, (0, W), (hz + 40, H - 60), (140, 300), (40, 90)), warp=1)
    b += contours(xs, ys, Z, [0.12 + .1 * i for i in range(9)], 'l2', minlen=6)
    # montañas de nivel en horizonte
    xs, ys, Z = field([(300, hz - 50, 200, 50, 1), (760, hz - 70, 250, 70, 1), (1320, hz - 40, 220, 45, 1)], warp=0.5, win=False)
    b += contours(xs, ys, Z, [.1 + .09 * i for i in range(10)], 'd', minlen=5)
    for x in (420, 980, 1480): b += iso_plate(x, hz + 120, 130, 90, 20, rings=5)
    save('hero-fondo', b, bg='#2f43e0')
    o = ''
    o += obj('console', 980, 700, 360, 6) + obj('cartridge', 1450, 520, 170, 10) + obj('controller', 560, 800, 250, -10)
    o += obj('screen', 1290, 150, 230, 5) + obj('chip', 820, 110, 130, 12) + obj('wifi', 1040, 330, 110)
    o += obj('disc', 1540, 800, 140, 0) 
    o += scatter(r, ['chip','cartridge','play','headset','wifi','disc','clapper','server'], 12, (60, 110), [(980,700,360),(1450,520,170),(560,800,250),(1290,150,230),(820,110,130),(1040,330,110),(1540,800,140),(380,330,560),(300,640,420),(250,150,380)], area=(700, 60, 1560, 860))
    save('hero-objetos', o, bg='#2f43e0')

# ============ 2 · PALETA: plano técnico / retícula ============
def paleta():
    r = random.Random(5); b = reticle(0, 0, W, H, 40, 5)
    b += circ(1250, 300, 200, 'd') + circ(1250, 300, 200, 'd') + rays(1250, 300, 200, 214, 120, 'd') + circ(1250, 300, 150, 'l2') + circ(1250, 300, 100, 'd') + circ(1250, 300, 50, 'l')
    b += guilloche(1250, 300, 96, 25, 60, 25, 900, 'l2') 
    b += guilloche(200, 700, 120, 31, 70, 31, 900, 'l')
    b += bundle(0, 560, 420, 90, 300, 6, 8, c='d') + bundle(W, 120, 380, -70, 250, 5, 8, c='d', sgn=-1)
    b += bundle(0, 80, 300, 60, 200, 4, 8, c='l2') + bundle(W, 820, 500, -40, 300, 4, 8, c='l2', sgn=-1)
    for (x, y, a, bb) in ((60, 60, 220, 120), (1100, 700, 300, 120)): b += line(x, y + bb + 20, x + a, y + bb + 20, 'd') + line(x, y + bb + 12, x, y + bb + 28, 'd') + line(x + a, y + bb + 12, x + a, y + bb + 28, 'd')
    save('paleta-fondo', b, bg='#2b3fd6')
    o = obj('chip', 1250, 300, 220, 0) + obj('headset', 180, 160, 180, -6) + obj('cartridge', 130, 740, 170, 8) + obj('controller', 1400, 780, 250, -8) + obj('play', 760, 90, 110)
    o += scatter(r, ['cartridge','play','wifi','disc','headset','controller','server'], 16, (60, 120), [(1250,300,300),(180,160,180),(130,740,170),(1400,780,250),(760,90,110)])
    save('paleta-objetos', o, bg='#2b3fd6')

# ============ 3 · CROMO: placas isométricas con curvas de nivel ============
def cromo():
    r = random.Random(9); b = ''
    plates = [(1130, 190, 300, 210, 30, 3), (760, 420, 260, 190, 22, 4), (1240, 520, 280, 200, 26, 5), (400, 640, 240, 170, 18, 6), (900, 700, 200, 150, 14, 7)]
    for (cx, cy, a, bb, t, sd) in plates:
        b += iso_terrain(cx, cy, a, bb, t, sd, 9)
    for k in range(14):
        x = r.uniform(120, 1480); y = r.uniform(60, 760); b += line(x, y, x, y + r.uniform(60, 190), 'd') if k % 3 else line(x, y, x, y + r.uniform(60, 190), 'l2')
    b += bundle(0, 300, 260, -60, 180, 5, 8, c='d') + bundle(W, 760, 300, -70, 200, 4, 8, c='d', sgn=-1)
    for k in range(40): b += star(r.uniform(20, W - 20), r.uniform(20, H - 20), r.choice([3, 4, 6]), 'l2')
    xs, ys, Z = field(topo_bumps(r, 3, (0, 500), (500, 880), (150, 280), (60, 120)), warp=1.3, seed=4)
    b += contours(xs, ys, Z, [.1 + .1 * i for i in range(8)], 'l', minlen=6)
    save('cromo-fondo', b, bg='#2434c4', dark='#050a5a')
    o = obj('cartridge', 1480, 120, 160, 12) + obj('console', 160, 300, 260, -6) + obj('server', 600, 790, 170, 0) + obj('clapper', 1500, 700, 180, -8)
    o += scatter(r, ['chip','play','headset','disc','wifi','cartridge','screen'], 14, (60, 110), [(1480,120,160),(160,300,260),(600,790,170),(1500,700,180)])
    save('cromo-objetos', o, bg='#2434c4', dark='#050a5a')

# ============ 4 · PARALLAX (fijo): rosetas guilloche + estrellas + órbitas ============
def parallax():
    r = random.Random(14); b = ''
    spots = [(300, 230, 130, 33, 80, 33), (1050, 180, 160, 37, 90, 37), (1400, 640, 150, 41, 80, 41), (650, 640, 120, 29, 70, 29), (140, 760, 100, 23, 55, 23)]
    for (cx, cy, R, rr, d, t) in spots:
        b += guilloche(cx, cy, R, rr, d, t, 900, 'd') + guilloche(cx, cy, R * .62, rr * .6, d * .6, t, 700, 'l') + circ(cx, cy, R + 24, 'd') + rays(cx, cy, R + 24, R + 38, 90, 'd') + circ(cx, cy, 8, 'c')
    for k in range(120): b += star(r.uniform(10, W - 10), r.uniform(10, H - 10), r.choice([2.5, 3, 4, 6]), r.choice(['d', 'l2', 'd']))
    b += bundle(0, 450, 380, 70, 220, 5, 8, c='d') + bundle(W, 420, 330, -50, 260, 5, 8, c='d', sgn=-1)
    xs, ys, Z = field(topo_bumps(r, 4, (300, 1300), (350, 600), (160, 260), (50, 90)), warp=1.5, seed=8)
    b += contours(xs, ys, Z, [.1 + .09 * i for i in range(9)], 'l', minlen=6)
    save('parallax-fondo', b, bg='#2b3fd6')
    o = obj('headset', 640, 190, 170, -8) + obj('controller', 330, 640, 230, 12) + obj('cartridge', 1130, 640, 130, -10) + obj('play', 1440, 180, 120) + obj('disc', 940, 830, 130) + obj('chip', 120, 130, 100, 10)
    o += scatter(r, ['controller','clapper','wifi','server','screen','cartridge'], 12, (70, 130), [(640,190,170),(330,640,230),(1130,640,130),(1440,180,120),(940,830,130),(120,130,100)])
    save('parallax-objetos', o, bg='#2b3fd6')

# ============ 5 · FILAS: circuitos y huellas de chip ============
def filas():
    r = random.Random(33); b = ''
    for k in range(7):
        y = 70 + k * 120 + r.uniform(-20, 20); b += bundle(0, y, r.uniform(150, 420), r.choice([-60, -40, 40, 60, 80]), r.uniform(80, 260), r.choice([3, 4, 5, 6]), 8, c='d' if k % 2 else 'l2')
        b += bundle(W, y + 55, r.uniform(150, 420), r.choice([-60, -40, 40, 60]), r.uniform(80, 260), r.choice([3, 4, 5]), 8, c='d' if k % 2 == 0 else 'l2', sgn=-1)
    for (x, y, w, h, n) in ((620, 120, 200, 120, 8), (900, 560, 240, 140, 9), (260, 600, 180, 120, 7), (1280, 300, 190, 130, 7)): b += chip_fp(x, y, w, h, n, 'd')
    for k in range(50): b += circ(r.uniform(40, W - 40), r.uniform(30, H - 30), r.choice([2, 3, 4]), 'd' if k % 3 else 'fdl')
    b += halftone(1000, 740, 560, 140, 11, 3.4, 'l', 'fdl') + halftone(20, 20, 420, 100, 11, 3.2, 'r', 'fdl')
    save('filas-fondo', b, bg='#2b3fd6')
    o = obj('server', 1400, 160, 160, 0) + obj('cloud', 330, 120, 250, 0) + obj('console', 1000, 380, 200, 4) + obj('wifi', 60, 800, 130)
    o += scatter(r, ['chip','cartridge','play','headset','disc','controller'], 14, (60, 110), [(1400,160,160),(330,120,250),(1000,380,200),(60,800,130)])
    save('filas-objetos', o, bg='#2b3fd6')

# ============ 6 · CATÁLOGO: placas + cartuchos + montañas ============
def catalogo():
    r = random.Random(41); b = ''
    for (cx, cy, a, bb, t, sd) in [(1270, 160, 240, 170, 18, 11), (620, 400, 300, 200, 24, 12), (1200, 600, 280, 190, 22, 13), (230, 640, 230, 160, 16, 14)]:
        b += iso_terrain(cx, cy, a, bb, t, sd, 10)
    for k in range(9):
        x = r.uniform(80, 1500); y = r.uniform(40, 800); b += line(x, y, x, y + r.uniform(60, 160), 'd') + circ(x, y, 4, 'd') 
    xs, ys, Z = field(topo_bumps(r, 4, (0, W), (0, H), (170, 320), (80, 150)), warp=1.4, seed=12)
    b += contours(xs, ys, Z, [.1 + .09 * i for i in range(9)], 'l', minlen=6)
    pix = ''  # escalera pixel fina (guiño al arte de STYLITES)
    x, y = 0, 820
    for k in range(40):
        y += r.choice([-20, 0, 20]); y = max(760, min(860, y)); pix += rect(x, y, 40, 40, 'd'); pix += rect(x + 6, y + 6, 28, 28, 'l') if k % 4 == 0 else ''; x += 40
    b += pix
    save('catalogo-fondo', b, bg='#2434c4', dark='#050a5a')
    o = obj('handheld', 1300, 150, 330, 6) + obj('cartridge', 120, 160, 150, -8) + obj('controller', 640, 780, 230, 6) + obj('cartridge', 1460, 620, 120, 14)
    o += scatter(r, ['play','wifi','disc','chip','headset','screen','clapper'], 12, (60, 110), [(1300,150,330),(120,160,150),(640,780,230),(1460,620,120)])
    save('catalogo-objetos', o, bg='#2434c4', dark='#050a5a')

# ============ 7 · STREAMING: cintas, rayos, claquetas ============
def streaming():
    r = random.Random(55); b = rays(1250, 260, 60, 1700, 90, 'l')
    for row, y in enumerate((80, 430, 700)):
        sk = [-60, 40, -20][row]; g = ''
        g += rect(-100, y, 1800, 110, 'oc', 0) + rect(-100, y, 1800, 110, 'd2') + line(-100, y + 20, 1700, y + 20, 'd') + line(-100, y + 90, 1700, y + 90, 'd')
        for x in range(-80, 1700, 34): g += rect(x, y + 5, 16, 10, 'd', 2) + rect(x, y + 95, 16, 10, 'd', 2)
        for x in range(-60, 1700, 170):
            g += rect(x, y + 26, 146, 58, 'd') + poly([(x + 66, y + 42), (x + 90, y + 55), (x + 66, y + 68)], 'c') if (x // 170) % 2 else rect(x, y + 26, 146, 58, 'd') + line(x + 10, y + 40, x + 136, y + 40, 'l') + line(x + 10, y + 55, x + 100, y + 55, 'l') + line(x + 10, y + 70, x + 120, y + 70, 'l')
        b += G(g, 800, y + 55, 1, -3, 800, y + 55)
    b += halftone(0, 250, 700, 140, 11, 3.6, 'r', 'fdl') + halftone(900, 560, 700, 120, 11, 3.6, 'l', 'fdl')
    for k in range(60): b += star(r.uniform(20, W - 20), r.uniform(20, H - 20), r.choice([3, 4, 6]), 'l2')
    b += circ(1250, 260, 70, 'd2') + circ(1250, 260, 100, 'd') + circ(1250, 260, 130, 'l')
    save('streaming-fondo', b, bg='#2b3fd6')
    o = obj('clapper', 1250, 260, 230, -6) + obj('screen', 250, 330, 250, 4) + obj('play', 760, 600, 140) + obj('headset', 1400, 600, 170, 8) + obj('wifi', 560, 80, 130) + obj('disc', 90, 620, 130)
    o += scatter(r, ['play','disc','wifi','cartridge','chip','controller'], 14, (60, 110), [(1250,260,230),(250,330,250),(760,600,140),(1400,600,170),(560,80,130),(90,620,130)])
    save('streaming-objetos', o, bg='#2b3fd6')

# ============ 8 · IA: red neuronal, circuitos, nube/servidor, matriz de puntos ============
def ia():
    r = random.Random(77); b = ''
    for k in range(9):
        y = 60 + k * 100; b += bundle(0, y, r.uniform(160, 380), r.choice([-50, 50, 70]), r.uniform(60, 200), r.choice([3, 4]), 8, c='d' if k % 2 else 'l2')
    for (x, y, w, h, n) in ((1000, 130, 260, 170, 9), (330, 560, 220, 150, 8)): b += chip_fp(x, y, w, h, n, 'd')
    # matriz binaria de puntos
    for j in range(14):
        for i in range(60): 
            if r.random() < .5: b += circ(780 + i * 12, 40 + j * 12 if False else 740 + j * 9, 1.6 if r.random() < .5 else 2.8, 'fdl')
    b += reticle(1050, 420, 1560, 700, 34, 5, 'l')
    xs, ys, Z = field(topo_bumps(r, 4, (0, W), (0, H), (150, 280), (60, 120)), warp=1.2, seed=3)
    b += contours(xs, ys, Z, [.12 + .1 * i for i in range(8)], 'l', minlen=6)
    b += guilloche(1350, 150, 100, 27, 60, 27, 800, 'l2')
    save('ia-fondo', b, bg='#2434c4', dark='#050a5a')
    o = obj('neural', 1300, 560, 330, 0, layers=(3, 5, 6, 4, 2), w=420, h=280) + obj('cloud', 330, 180, 270, 0) + obj('server', 150, 640, 160, 0) + obj('chip', 1000, 130, 140, 8) + obj('wifi', 700, 120, 120)
    o += scatter(r, ['play','disc','headset','controller','cartridge','screen','clapper'], 12, (60, 110), [(1300,560,330),(330,180,270),(150,640,160),(1000,130,140),(700,120,120)])
    save('ia-objetos', o, bg='#2434c4', dark='#050a5a')

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for fn in (hero, paleta, cromo, parallax, filas, catalogo, streaming, ia): fn()
    for k, v in OUT.items():
        open(os.path.join(out, f'campo-{k}.svg'), 'w').write(v); print(k, len(v) // 1024, 'KB')
