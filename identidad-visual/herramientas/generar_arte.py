#!/usr/bin/env python3
"""Arte de fondo vectorial (SVG, líneas finas casi negras sobre campos azules; rojo para el listón). Uso: python3 generar_arte.py ../assets/arte"""
import sys, os, random, math
K = '#05071f'; RED = '#ff3322'
def wrap(w, h, body, name): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMax slice" role="img" aria-label="{name}"><title>{name}</title>{body}</svg>'
def star(x, y, r, c=K): return f'<path d="M{x} {y-r}C{x+r*.12} {y-r*.3} {x+r*.3} {y-r*.12} {x+r} {y}C{x+r*.3} {y+r*.12} {x+r*.12} {y+r*.3} {x} {y+r}C{x-r*.12} {y+r*.3} {x-r*.3} {y+r*.12} {x-r} {y}C{x-r*.3} {y-r*.12} {x-r*.12} {y-r*.3} {x} {y-r}Z" fill="{c}"/>'
A = {}
# 1 · rejilla de horizonte + estrellas (hero)
def rejilla():
    r = random.Random(3); W, H, hz = 1600, 720, 330; b = ''
    for _ in range(40): b += star(r.uniform(20, W-20), r.uniform(20, hz-40), r.choice([5, 7, 10, 14]))
    b += f'<path d="M0 {hz}H{W}" stroke="{K}" stroke-width="4"/>'
    for i in range(-14, 15):
        b += f'<path d="M{W/2 + i*38} {hz}L{W/2 + i*190} {H}" stroke="{K}" stroke-width="2.4" opacity=".9"/>'
    y = hz; step = 8
    while y < H:
        y += step; step *= 1.22; b += f'<path d="M0 {y:.0f}H{W}" stroke="{K}" stroke-width="{2+ (y-hz)/90:.1f}" opacity=".9"/>'
    return wrap(W, H, b, 'Rejilla de horizonte')
A['rejilla'] = rejilla()
# 2 · circuitos (IA / tecnología)
def circuito():
    r = random.Random(5); W, H = 1600, 700; b = ''
    for k in range(34):
        x, y = r.choice([0, W]) if r.random() < .5 else r.uniform(0, W), r.uniform(20, H-20)
        pts = [(x, y)]
        for s in range(r.randint(3, 6)):
            dx = r.choice([-1, 1]) * r.uniform(40, 170); dy = r.choice([-1, 0, 1]) * r.uniform(30, 90)
            x += dx; pts.append((x, y)); y += dy; pts.append((x, y))
        b += f'<polyline points="{" ".join(f"{px:.0f},{py:.0f}" for px, py in pts)}" fill="none" stroke="{K}" stroke-width="3" stroke-linejoin="round" opacity=".85"/>'
        px, py = pts[-1]; b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="none" stroke="{K}" stroke-width="3"/><circle cx="{px:.0f}" cy="{py:.0f}" r="3" fill="{K}"/>'
    return wrap(W, H, b, 'Circuitos')
A['circuito'] = circuito()
# 3 · isométrico de placas con curvas de nivel (catálogo)
def isometrico():
    r = random.Random(9); W, H = 1600, 760; b = ''
    def plate(cx, cy, w, h, n):
        pts = [(cx, cy-h), (cx+w, cy), (cx, cy+h), (cx-w, cy)]; out = f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{K}" stroke-width="4"/>'
        out += f'<path d="M{cx-w} {cy}V{cy+22}L{cx} {cy+h+22}L{cx+w} {cy+22}V{cy}" fill="none" stroke="{K}" stroke-width="4"/>'
        for i in range(1, n):
            t = i/n; hh = h*(1-t); ww = w*(1-t)
            out += f'<polygon points="{cx},{cy-hh:.0f} {cx+ww:.0f},{cy} {cx},{cy+hh:.0f} {cx-ww:.0f},{cy}" fill="none" stroke="{K}" stroke-width="1.8" opacity=".75"/>'
        return out
    for (cx, cy, w, h, n) in [(1180, 190, 420, 150, 12), (800, 420, 360, 126, 9), (1330, 520, 330, 118, 10), (430, 600, 300, 104, 8), (1000, 660, 240, 84, 6)]:
        b += plate(cx, cy, w, h, n)
    for k in range(10):
        x = r.uniform(100, 1500); y = r.uniform(60, 700); b += f'<path d="M{x:.0f} {y:.0f}V{y+r.uniform(60,160):.0f}" stroke="{K}" stroke-width="2.4" stroke-dasharray="2 6"/>'
    for k in range(18): b += star(r.uniform(20, 1580), r.uniform(20, 740), r.choice([5, 8]))
    return wrap(W, H, b, 'Placas isométricas')
A['isometrico'] = isometrico()
# 4 · cinta de película + destellos (streaming)
def cinta():
    W, H = 1600, 600; b = ''
    for row, y in enumerate((70, 250, 430)):
        sk = [-60, 40, -20][row]
        b += f'<g transform="translate({sk} 0) rotate(-3 800 {y+60})"><rect x="-100" y="{y}" width="1800" height="120" fill="none" stroke="{K}" stroke-width="4"/>'
        for x in range(-80, 1700, 40): b += f'<rect x="{x}" y="{y+10}" width="20" height="14" rx="3" fill="{K}"/><rect x="{x}" y="{y+96}" width="20" height="14" rx="3" fill="{K}"/>'
        for x in range(-60, 1700, 190): b += f'<rect x="{x}" y="{y+34}" width="160" height="52" fill="none" stroke="{K}" stroke-width="3"/><path d="M{x+68} {y+46}l26 14l-26 14z" fill="{K}"/>'
        b += '</g>'
    return wrap(W, H, b, 'Cintas de película')
A['cinta'] = cinta()
# 5 · listón rojo ornamental (inspirado en el plano frontal rojo de la referencia)
def liston():
    W, H = 600, 1100
    d = ('M560 20C470 150 380 210 340 330C310 420 410 470 380 560C350 650 230 640 160 760C110 840 90 960 40 1080'
         'C120 990 190 930 260 880C330 830 420 800 430 700C440 600 330 560 380 440C430 320 520 200 560 20Z')
    b = f'<path d="{d}" fill="{RED}"/>'
    # grabado: líneas finas negras siguiendo la forma
    for i in range(1, 9):
        b += f'<path d="{d}" fill="none" stroke="{K}" stroke-width="1.6" opacity=".55" transform="translate({i*-6} {i*3}) scale(1)" />'
    b += f'<path d="M560 20C470 150 380 210 340 330" fill="none" stroke="{K}" stroke-width="3"/>'
    for (x, y, r) in [(350, 330, 16), (395, 470, 11), (300, 690, 13), (210, 770, 9), (130, 880, 7)]: b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{K}"/><circle cx="{x}" cy="{y}" r="{r+9}" fill="none" stroke="{K}" stroke-width="2"/>'
    b += f'<path d="M520 90C610 220 520 330 470 420" fill="none" stroke="{RED}" stroke-width="3"/><circle cx="470" cy="420" r="9" fill="{RED}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Listón rojo"><title>Listón rojo</title>{b}</svg>'
A['liston'] = liston()
# 6 · rosetas (patrón repetible)
def rosetas():
    s = 120; b = f'<g fill="none" stroke="{K}" stroke-width="3"><rect x="20" y="20" width="80" height="80"/><rect x="38" y="38" width="44" height="44" transform="rotate(45 60 60)"/><circle cx="60" cy="60" r="10" fill="{K}"/><path d="M60 0V20M60 100V120M0 60H20M100 60H120"/></g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}">{b}</svg>'
A['rosetas'] = rosetas()
if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for k, v in A.items():
        if k != 'liston': continue  # v3: el resto del arte lo genera generar_arte_v3.py
        open(os.path.join(out, f'arte-{k}.svg'), 'w').write(v)
    print(len(A), 'artes')
