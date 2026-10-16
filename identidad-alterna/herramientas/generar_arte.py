#!/usr/bin/env python3
"""Genera el arte geométrico de la propuesta ALTERNA (cartel constructivista). Sin degradados, filtros, opacidad ni mezclas.
Cada escena = 3 capas del mismo lienzo 1200x700: azul trasero (assets/planos), una masa roja delantera (assets/heroes) y piezas rojas pequeñas (assets/piezas).
Ningún SVG mezcla rojo y azul. El rojo lleva un borde negro (separa planos). Uso: python3 generar_arte.py"""
import os, math
R, B, K = '#FF1A1A', '#1616FF', '#050505'
ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets')
def save(d, name, body):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    open(os.path.join(ROOT, d, name + '.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" width="1200" height="700" shape-rendering="geometricPrecision">{body}</svg>\n')
def dots(x0, y0, x1, y1, pitch, r):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{B}"/>' for y in range(y0, y1 + 1, pitch) for x in range(x0, x1 + 1, pitch))
def line(x1, y1, x2, y2, w=4): return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{B}" stroke-width="{w}" fill="none"/>'
def rect(x, y, w, h, c=B): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
def star(cx, cy, r, c=R, rot=0):
    pts = []
    for i in range(8):
        a = math.radians(rot + i * 45 - 90); rr = r if i % 2 == 0 else r * .26
        pts.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{c}" stroke="{K}" stroke-width="10" stroke-linejoin="miter"/>'
def bar(x, y, w, h): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{R}" stroke="{K}" stroke-width="10"/>'
def circ(cx, cy, r): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{R}" stroke="{K}" stroke-width="10"/>'

# ---- INICIO: disco rojo con cruz negra (cruceta) / puntos azules atrás
save('planos', 'inicio', dots(150, 70, 1010, 580, 30, 5) + rect(1060, 0, 70, 700) + line(0, 640, 1200, 640, 4) + line(0, 668, 1200, 668, 4))
save('heroes', 'inicio', f'<circle cx="640" cy="360" r="262" fill="{K}"/><circle cx="640" cy="360" r="250" fill="{R}"/>' + rect(605, 235, 70, 250, K) + rect(515, 325, 250, 70, K) + f'<circle cx="640" cy="360" r="26" fill="{R}"/>')
save('piezas', 'inicio', star(1000, 130, 48) + bar(70, 585, 230, 44) + circ(330, 120, 24))
# ---- JUEGOS: retícula de bloques azul / tetromino rojo
g = ''.join(line(x, 40, x, 660, 3) for x in range(80, 1121, 70)) + ''.join(line(80, y, 1120, y, 3) for y in range(40, 661, 70))
g += ''.join(rect(80 + 70 * i + 6, 40 + 70 * j + 6, 58, 58) for i, j in [(2, 1), (3, 1), (3, 2), (11, 6), (12, 6), (12, 7), (1, 6), (14, 2)])
save('planos', 'juegos', g)
sq = ''.join(f'<rect x="{x}" y="{y}" width="160" height="160" fill="{R}" stroke="{K}" stroke-width="12"/>' for x, y in [(560, 90), (560, 250), (560, 410), (720, 410)])
save('heroes', 'juegos', sq)
save('piezas', 'juegos', bar(170, 500, 70, 70) + bar(260, 540, 40, 40) + star(980, 160, 40, R, 22))
# ---- STREAMING: arcos azules / triángulo de reproducción rojo
arcs = ''.join(f'<path d="M{200 - r} 700A{r} {r} 0 0 1 {200 + r} 700" stroke="{B}" stroke-width="9" fill="none"/>' for r in range(120, 1200, 110))
save('planos', 'streaming', arcs + rect(1100, 0, 100, 700))
save('heroes', 'streaming', f'<polygon points="500,110 500,610 960,360" fill="{R}" stroke="{K}" stroke-width="20" stroke-linejoin="miter"/><polygon points="560,230 560,490 790,360" fill="{K}"/>')
save('piezas', 'streaming', circ(1030, 150, 34) + bar(120, 90, 190, 36))
# ---- IA: circuito azul / chip rojo
c = ''
for y in (110, 200, 290, 410, 500, 590): c += line(0, y, 380, y, 6) + line(820, y, 1200, y, 6) + f'<circle cx="{40 + (y % 3) * 90}" cy="{y}" r="11" fill="{B}"/>' + f'<circle cx="{1160 - (y % 4) * 70}" cy="{y}" r="11" fill="{B}"/>'
c += line(160, 110, 160, 290, 6) + line(300, 410, 300, 590, 6) + line(1000, 200, 1000, 410, 6) + line(900, 500, 900, 590, 6) + dots(430, 40, 790, 60, 40, 5)
save('planos', 'ia', c)
pins = ''.join(rect(480 + 60 * i, 85, 26, 30, R) + rect(480 + 60 * i, 585, 26, 30, R) for i in range(6)) + ''.join(rect(385, 190 + 60 * i, 30, 26, R) + rect(785, 190 + 60 * i, 30, 26, R) for i in range(6))
save('heroes', 'ia', f'<rect x="400" y="100" width="400" height="500" fill="{K}"/>' + pins + f'<rect x="410" y="110" width="380" height="480" fill="{R}"/><rect x="470" y="170" width="260" height="360" fill="none" stroke="{K}" stroke-width="14"/><rect x="560" y="290" width="80" height="120" fill="{K}"/>')
save('piezas', 'ia', bar(1010, 90, 60, 60) + bar(1090, 150, 34, 34) + bar(110, 600, 50, 50))
# ---- CONSOLAS: rayado diagonal azul / palanca de arcade roja
h = '<clipPath id="cp"><rect x="120" y="50" width="960" height="600"/></clipPath><g clip-path="url(#cp)">' + ''.join(line(x, 650, x + 600, 50, 7) for x in range(-480, 1100, 48)) + '</g>'
save('planos', 'consolas', h + rect(1110, 50, 40, 600))
save('heroes', 'consolas', f'<polygon points="330,640 870,640 810,520 390,520" fill="{R}" stroke="{K}" stroke-width="14"/><rect x="580" y="250" width="40" height="280" fill="{R}" stroke="{K}" stroke-width="10"/><circle cx="600" cy="205" r="125" fill="{R}" stroke="{K}" stroke-width="14"/>' + rect(520, 580, 160, 26, K))
save('piezas', 'consolas', circ(1000, 590, 44) + circ(910, 640, 30) + bar(130, 120, 150, 36))
# ---- PARALLAX: muro de cuadrados concéntricos azul / anillo rojo
w = ''.join(f'<rect x="{600 - s}" y="{350 - s * .62}" width="{2 * s}" height="{2 * s * .62}" stroke="{B}" stroke-width="5" fill="none"/>' for s in range(80, 900, 80))
save('planos', 'parallax', w)
save('heroes', 'parallax', f'<circle cx="600" cy="350" r="196" fill="none" stroke="{K}" stroke-width="128"/><circle cx="600" cy="350" r="196" fill="none" stroke="{R}" stroke-width="100"/>')
save('piezas', 'parallax', f'<polygon points="1010,520 1090,520 1050,450" fill="{R}" stroke="{K}" stroke-width="10"/>' + bar(100, 90, 160, 34) + star(150, 560, 38))
print('arte ok')
