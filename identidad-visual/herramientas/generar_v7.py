#!/usr/bin/env python3
"""v7 · cromoestereopsis según docs/CHROMOSTEREOPSIS.md: base negra; azul = plano trasero estructural; rojo = masa delantera.
Genera (todo SVG, colores sólidos, SIN opacidades, SIN degradados, SIN filtros):
  assets/planos/plano-<sección>.svg  líneas finas azules (retículas, curvas de nivel, circuitos...) sobre transparente
  assets/placas/placa-<sección>.svg  regiones azules sólidas con detalle negro (como panel-consoles-rear de public/art/cromo)
  assets/piezas/pieza-*.svg          piezas rojas pequeñas (rojo sólido + negro + rojo oscuro; sin azul, sin halo)
Uso: python3 generar_v7.py ..   (desde herramientas/; escribe en ../assets/...)"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
import arte_lib as A
from arte_lib import f, P, poly, circ, line, rect, star, G, field, contours, reticle, bundle, guilloche, rays, ring_dots, chip_fp, iso_plate, o_neural, halftone
BLUE, BLUE_D, BLACK = '#2a3cff', '#1a26a8', '#050505'
RED, RED_D, RED_DD = '#ff2a1a', '#c4160c', '#7d0a05'
W, H = 1600, 900

def style():
    return ('<style>path,circle,rect,line,polygon,ellipse,polyline{fill:none;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round}'
            f'.d{{stroke:{BLUE_D};stroke-width:1}}.d2{{stroke:{BLUE_D};stroke-width:1.6}}.d3{{stroke:{BLUE};stroke-width:2.4}}'
            f'.l{{stroke:{BLUE_D};stroke-width:1}}.l2{{stroke:{BLUE};stroke-width:1.4}}.c{{stroke:{BLUE};stroke-width:1.2}}.c2{{stroke:{BLUE};stroke-width:1.8}}'
            f'.fd,.fl,.fdl,.fdd{{fill:{BLUE_D};stroke:none}}.fc{{fill:{BLUE};stroke:none}}.oc{{fill:{BLACK};stroke:none}}</style>')
def svg7(body, w=W, h=H, slice_=True):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="{"xMidYMid slice" if slice_ else "xMidYMid meet"}">{style()}{body}</svg>'
OUT = {}
def topo_bumps(r, n, xr, yr, sx=(120, 260), sy=(80, 170)):
    return [(r.uniform(*xr), r.uniform(*yr), r.uniform(*sx), r.uniform(*sy), r.uniform(.6, 1.0)) for _ in range(n)]

# ================= PLANOS (azul trasero, línea fina, ventana fija) =================
def plano_hero():
    r = random.Random(21); hz = 520; b = ''
    for _ in range(46): b += star(r.uniform(30, W - 30), r.uniform(20, hz - 40), r.choice([3, 4, 5, 8, 11]), r.choice(['d', 'd', 'l2']))
    b += P(f'M0 {hz}H{W}', 'd3')
    for i in range(-18, 19): b += line(W / 2 + i * 38, hz, W / 2 + i * 190, H, 'd')
    y, st = hz, 6
    while y < H: y += st; st *= 1.22; b += line(0, y, W, y, 'd')
    b += bundle(0, 70, 380, 60, 220, 5, 8, c='d2') + bundle(W, 70, 380, 60, 220, 5, 8, c='d2', sgn=-1)
    OUT['hero'] = svg7(b)
def plano_paleta():
    b = reticle(0, 0, W, H, 40, 5, 'd')
    b += circ(1180, 330, 210, 'd2') + rays(1180, 330, 210, 226, 120, 'd') + circ(1180, 330, 150, 'l2') + circ(1180, 330, 90, 'd') + guilloche(1180, 330, 96, 25, 60, 25, 900, 'l2')
    b += guilloche(260, 720, 120, 31, 70, 31, 900, 'd')
    OUT['paleta'] = svg7(b)
def plano_cromo():
    r = random.Random(9)
    xs, ys, Z = field(topo_bumps(r, 7, (0, W), (0, H), (180, 360), (120, 240)), warp=1.2)
    b = contours(xs, ys, Z, [0.1 + .075 * i for i in range(11)], 'd', minlen=6) + contours(xs, ys, Z, [0.2, 0.44, 0.68], 'l2', minlen=6)
    OUT['cromo'] = svg7(b)
def plano_parallax():
    b = ''
    for k, rad in enumerate(range(90, 760, 70)): b += circ(1100, 430, rad, 'l2' if k % 3 == 0 else 'd')
    b += ring_dots(1100, 430, 160, 60, 'fdl', 2) + ring_dots(1100, 430, 370, 110, 'fdl', 1.8) + rays(1100, 430, 170, 360, 90, 'd')
    b += circ(1100 - 370, 430, 14, 'c2') + circ(1100 + 160 * .7, 430 - 160 * .7, 9, 'c2')
    OUT['parallax'] = svg7(b)
def plano_filas():
    b = ''
    for (x, y, d, dy, dx2, sg) in [(0, 120, 360, 70, 260, 1), (0, 420, 520, -70, 300, 1), (W, 200, 420, 80, 250, -1), (W, 640, 480, -60, 280, -1), (0, 760, 300, -50, 500, 1)]:
        b += bundle(x, y, d, dy, dx2, 6, 8, c='d2', sgn=sg)
    b += chip_fp(1300, 740, 150, 112, 7, 'd')
    OUT['filas'] = svg7(b)
def plano_catalogo():
    b = ''
    for k in range(7):  # cordilleras zigzag escalonadas (píxel)
        y0 = 360 + k * 62; pts = []; x = 0
        while x < W + 80:
            pts += [(x, y0), (x + 56, y0 - 40 - (k % 3) * 14), (x + 112, y0)]; x += 112
        b += poly(pts, 'd2' if k % 2 else 'd')
    for (x, y) in ((220, 150), (1010, 120), (1420, 170), (700, 790)): b += star(x, y, 14, 'd2')
    OUT['catalogo'] = svg7(b)
def plano_streaming():
    b = rays(1180, 450, 60, 1100, 80, 'd')
    for k in range(7):
        y = 140 + k * 100; pts = [(x, y + 26 * math.sin(x / 90 + k * .7)) for x in range(0, W + 1, 20)]; b += poly(pts, 'd2' if k % 3 == 0 else 'd')
    for k in range(40): b += rect(20 + k * 40, 22, 16, 22, 'd', 2) + rect(20 + k * 40, H - 44, 16, 22, 'd', 2)
    OUT['streaming'] = svg7(b)
def plano_ia():
    body, (w, h) = o_neural(seed=5, layers=(4, 7, 8, 7, 4), w=900, h=640)
    b = reticle(0, 0, W, H, 80, 4, 'd') + G(body, 1060, 430, 1.1, 0, w / 2, h / 2)
    b += bundle(0, 740, 300, -60, 300, 5, 8, c='d2') + chip_fp(150, 640, 150, 118, 7, 'd')
    OUT['ia'] = svg7(b)

# ================= PLACAS (regiones azules sólidas con detalle negro) =================
PW, PH = 800, 640
def R(x, y, w, h, c=BLUE): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
def Pg(pts, c=BLUE): return f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="{c}"/>'
def zig(x0, x1, y, amp, step, base, c):  # montaña escalonada tipo píxel, recortada abajo en 'base'
    pts = [(x0, base), (x0, y)]; x = x0; up = True
    while x < x1:
        nx = min(x + step, x1); pts += [(x + step * .5, y - amp) if x + step * .5 <= x1 else (x1, y - amp), (nx, y)]; x = nx
    pts += [(x1, base)]
    return Pg(pts, c)
def pix_zig(x0, x1, ytop, step, cell, base, c):
    o = ''
    n = int((x1 - x0) / step); 
    for i in range(n):
        for lvl in range(6):
            h = min(lvl, 5 - lvl) if False else 0
    # peldaños simétricos
    pts = []; x = x0
    while x < x1:
        for k in range(4): pts.append((x + k * cell, ytop - (k + 1) * cell if k < 4 else ytop))
        for k in range(4): pts.append((x + (4 + k) * cell, ytop - (4 - k) * cell))
        x += 8 * cell
    return pts
def dots_grid(x0, y0, cols, rows, gap, r, c=BLACK):
    return ''.join(f'<circle cx="{x0 + i * gap}" cy="{y0 + j * gap}" r="{r}" fill="{c}"/>' for j in range(rows) for i in range(cols))
def star4(cx, cy, r, c=BLACK, k=.22):
    p = []
    for i in range(8):
        a = math.radians(-90 + i * 45); q = r if i % 2 == 0 else r * k; p.append((cx + math.cos(a) * q, cy + math.sin(a) * q))
    return Pg(p, c)
def plate(name, body): OUT['placa-' + name] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" shape-rendering="crispEdges" role="img" aria-label="Placa azul"><title>Placa azul · plano trasero</title>{body}</svg>'
def zz(x0, x1, y, step, amp, base, col):
    """zigzag escalonado: serrucho con base recta"""
    pts = [(x0, base)]; x = x0; k = 0
    while x < x1:
        yy = y - amp if k % 2 == 0 else y; pts += [(x, yy), (min(x + step, x1), yy)]; x += step; k += 1
    pts += [(x1, base)]
    return Pg(pts, col)
def placa_hero():  # arco azul + ventana negra con montañas + panel perforado
    b = f'<path d="M96 640V250A240 240 0 0 1 576 250V640Z" fill="{BLUE}"/>'
    b += R(176, 214, 320, 214, BLACK) + zz(176, 496, 330, 40, 40, 428, BLUE) + zz(176, 496, 372, 32, 28, 428, BLACK) + R(176, 392, 320, 36, BLUE)
    b += ''.join(R(96, 452 + i * 28, 480, 8, BLACK) for i in range(6))
    b += R(560, 330, 184, 310, BLUE) + dots_grid(584, 354, 6, 10, 28, 7) 
    b += star4(660, 120, 22) + star4(120, 120, 14) + star4(740, 250, 10) + R(0, 628, 800, 12, BLUE)
    plate('hero', b)
def placa_paleta():  # panel perforado + columna de rejilla + tarjeta de teclas
    b = R(110, 70, 520, 500) + dots_grid(142, 102, 18, 17, 28, 8) + R(500, 70, 130, 500, BLACK) + ''.join(R(516, 94 + i * 30, 98, 14, BLUE) for i in range(15))
    b += R(110, 586, 520, 14, BLUE) + R(110, 614, 340, 14, BLUE) + R(660, 150, 100, 100, BLUE) + R(676, 166, 68, 68, BLACK) + R(692, 182, 36, 36, BLUE)
    plate('paleta', b)
def placa_cromo():  # tres losas isométricas apiladas, cara frontal negra
    def slab(cx, cy, w, d, t):
        top = [(cx, cy - d), (cx + w, cy), (cx, cy + d), (cx - w, cy)]
        left = [(cx - w, cy), (cx, cy + d), (cx, cy + d + t), (cx - w, cy + t)]
        right = [(cx + w, cy), (cx, cy + d), (cx, cy + d + t), (cx + w, cy + t)]
        return Pg(left, BLACK) + Pg(right, BLUE_D) + Pg(top, BLUE) + Pg([(cx, cy - d * .55), (cx + w * .55, cy), (cx, cy + d * .55), (cx - w * .55, cy)], BLACK) + Pg([(cx, cy - d * .3), (cx + w * .3, cy), (cx, cy + d * .3), (cx - w * .3, cy)], BLUE)
    b = slab(400, 420, 330, 190, 56) + slab(400, 330, 250, 140, 56) + slab(400, 250, 160, 90, 56)
    plate('cromo', b)
def placa_parallax():  # disco azul con trama de puntos negros y órbita
    b = f'<circle cx="420" cy="320" r="260" fill="{BLUE}"/>'
    for j in range(14):
        for i in range(14):
            x, y = 190 + i * 32, 90 + j * 32
            t = (i + j) / 26
            if (x - 420) ** 2 + (y - 320) ** 2 < 240 ** 2 and t > .35: b += f'<circle cx="{x}" cy="{y}" r="{round(3 + 7 * (t - .3), 1)}" fill="{BLACK}"/>'
    b += f'<circle cx="420" cy="320" r="320" fill="none" stroke="{BLUE}" stroke-width="6"/><circle cx="130" cy="520" r="26" fill="{BLUE}"/><circle cx="130" cy="520" r="9" fill="{BLACK}"/>' + R(160, 600, 520, 14)
    plate('parallax', b)
def placa_filas():  # torres tipo rack con ranuras
    b = ''
    for (x, y, w, h) in [(90, 150, 170, 430), (290, 60, 210, 520), (530, 230, 170, 350)]:
        b += R(x, y, w, h) + ''.join(R(x + 18, y + 22 + i * 36, w - 36, 16, BLACK) for i in range((h - 60) // 36)) + ''.join(f'<circle cx="{x + w - 30}" cy="{y + 30 + i * 36}" r="4" fill="{BLUE}"/>' for i in range(0, (h - 60) // 36, 2))
    b += R(60, 592, 680, 14) + R(60, 618, 400, 14)
    plate('filas', b)
def placa_catalogo():  # bloque con cordillera negra y escalera píxel
    b = R(90, 110, 620, 420) + zz(90, 710, 330, 56, 60, 530, BLACK) + zz(90, 710, 410, 56, 40, 530, BLUE) + zz(90, 710, 470, 56, 30, 530, BLACK)
    b += ''.join(R(470 + i * 48, 530 + 0, 48, 0) for i in range(0)) + ''.join(R(404 + i * 56, 574 - i * 36, 56 * (5 - i) + 120, 36) for i in range(0))
    b += ''.join(R(380 + i * 70, 590 - i * 44, 350 - i * 70, 44) for i in range(4)) + star4(180, 190, 26) + star4(300, 240, 12) + star4(600, 170, 16)
    plate('catalogo', b)
def placa_streaming():  # cinta de película con tres fotogramas
    b = R(60, 120, 680, 400)
    b += ''.join(R(80 + i * 48, 134, 22, 28, BLACK) + R(80 + i * 48, 478, 22, 28, BLACK) for i in range(14))
    for k in range(3):
        x = 96 + k * 218; b += R(x, 190, 196, 250, BLACK) + zz(x, x + 196, 360, 28, 36, 440, BLUE) + star4(x + 140, 240, 14, BLUE)
    b += R(40, 560, 720, 14) + R(40, 590, 420, 14)
    plate('streaming', b)
def placa_ia():  # chip con retícula negra, pines y pistas
    b = R(200, 130, 400, 400) + ''.join(R(200 + 40 + i * 40, 130, 10, 400, BLACK) if False else '' for i in range(0))
    b += ''.join(R(228 + i * 48, 158, 12, 344, BLACK) for i in range(8)) + ''.join(R(228, 158 + i * 48, 344, 12, BLACK) for i in range(8))
    for i in range(7):
        b += R(236 + i * 52, 96, 18, 34) + R(236 + i * 52, 530, 18, 34) + R(166, 150 + i * 52 + 10, 34, 18) + R(600, 150 + i * 52 + 10, 34, 18)
    b += R(0, 612, 800, 12) + f'<circle cx="716" cy="150" r="12" fill="{BLUE}"/><circle cx="716" cy="150" r="5" fill="{BLACK}"/>' + R(716, 150, 4, 90) 
    plate('ia', b)

# ================= PIEZAS ROJAS PEQUEÑAS (solo rojo/negro) =================
def piece(name, w, h, body, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 {w+12} {h+12}" role="img" aria-label="{label}"><title>{label}</title>{body}</svg>'
KS = f'stroke="{BLACK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'
def sh(d, fill=RED, sw=6): return f'<path d="{d}" fill="{fill}" stroke="{BLACK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'
def shade(d, dx=-9, dy=-9, base=RED, dark=RED_D):  # volumen: sombra roja oscura abajo-derecha + masa clara; contorno negro
    i = 'p%d' % abs(__import__("zlib").crc32((d+name_ctx[0]).encode()) % 99999)
    return (f'<clipPath id="{i}"><path d="{d}"/></clipPath><path d="{d}" fill="{dark}"/><g clip-path="url(#{i})"><path d="{d}" fill="{base}" transform="translate({dx} {dy})"/></g>'
            f'<path d="{d}" fill="none" stroke="{BLACK}" stroke-width="6" stroke-linejoin="round"/>')
name_ctx = ['']
PZ = {}
def mk(name, w, h, body, label): name_ctx[0] = name; PZ[name] = piece(name, w, h, body, label)
def starp(cx, cy, r, k=.26):
    p = []
    for i in range(8):
        a = math.radians(-90 + i * 45); q = r if i % 2 == 0 else r * k; p.append((cx + math.cos(a) * q, cy + math.sin(a) * q))
    return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in p) + 'Z'
name_ctx[0] = 'estrella'; mk('estrella', 200, 200, shade(starp(100, 100, 98), -8, -8), 'Estrella')
name_ctx[0] = 'sello'
def sello():
    pts = []; n = 16
    for i in range(n * 2):
        a = math.radians(i * 180 / n); q = 98 if i % 2 == 0 else 86; pts.append((100 + q * math.cos(a), 100 + q * math.sin(a)))
    d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z'
    return shade(d, -7, -7) + f'<circle cx="100" cy="100" r="58" fill="none" stroke="{BLACK}" stroke-width="6"/>' + f'<path d="{starp(100, 100, 36, .3)}" fill="{BLACK}"/>'
mk('sello', 200, 200, sello(), 'Sello')
mk('flecha', 220, 150, shade('M8 52H130V10L212 75L130 140V98H8Z', -9, -9), 'Flecha')
def boton():
    c = f'<circle cx="100" cy="100" r="96" fill="{RED_D}" stroke="{BLACK}" stroke-width="6"/><circle cx="92" cy="92" r="88" fill="{RED}"/><circle cx="100" cy="100" r="96" fill="none" stroke="{BLACK}" stroke-width="6"/>'
    return c + f'<path d="M84 44H116V84H156V116H116V156H84V116H44V84H84Z" fill="{BLACK}"/>'
mk('boton', 200, 200, boton(), 'Botón')
mk('play', 200, 200, f'<circle cx="100" cy="100" r="96" fill="{RED_D}" stroke="{BLACK}" stroke-width="6"/><circle cx="92" cy="92" r="88" fill="{RED}"/><circle cx="100" cy="100" r="96" fill="none" stroke="{BLACK}" stroke-width="6"/><path d="M78 56L146 100L78 144Z" fill="{BLACK}"/>', 'Reproducir')
mk('etiqueta', 220, 130, shade('M10 20H150L212 65L150 110H10Z', -8, -8) + f'<circle cx="46" cy="65" r="13" fill="{BLACK}"/><path d="M80 52H138M80 78H118" stroke="{BLACK}" stroke-width="8" stroke-linecap="round"/>', 'Etiqueta')
mk('cursor', 160, 200, shade('M12 8L12 164L56 124L86 190L118 176L88 112L148 108Z', -8, -8), 'Cursor')

if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 else '..'
    for fn in (plano_hero, plano_paleta, plano_cromo, plano_parallax, plano_filas, plano_catalogo, plano_streaming, plano_ia, placa_hero, placa_paleta, placa_cromo, placa_parallax, placa_filas, placa_catalogo, placa_streaming, placa_ia): fn()
    for d in ('planos', 'placas', 'piezas'): os.makedirs(os.path.join(base, 'assets', d), exist_ok=True)
    for k, v in OUT.items():
        d = 'placas' if k.startswith('placa-') else 'planos'; nm = k if k.startswith('placa-') else 'plano-' + k
        open(os.path.join(base, 'assets', d, nm + '.svg'), 'w').write(v); print(d, nm, len(v))
    for k, v in PZ.items(): open(os.path.join(base, 'assets/piezas', f'pieza-{k}.svg'), 'w').write(v); print('pieza', k, len(v))
