#!/usr/bin/env python3
"""Arte AZUL (plano trasero) de v9d «Póster psicodélico»: bandas de ondas fluidas, rayos solares, flores art nouveau en trazo fino,
topografía, nodos/circuitos orgánicos y cortes de sección curvos. Todo azul sólido (#1616FF) sobre transparente (negro de la página);
los detalles internos son negros (#050505). Sin degradados, blur, opacidad ni rojo."""
import math, random, os
B, K = '#1616FF', '#050505'
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
def f(v): return f'{v:.1f}'.rstrip('0').rstrip('.')
def poly_d(pts, close=False): return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ('Z' if close else '')
def band(fn, x0, x1, thick, step=14):
    xs = [x0 + i * step for i in range(int((x1 - x0) / step) + 2)]
    top = [(x, fn(x)) for x in xs]; bot = [(x, fn(x) + thick) for x in reversed(xs)]
    return f'<path d="{poly_d(top + bot, True)}" fill="{B}"/>'
def ondas(x0, x1, y0, n, gap, thick, amp, wl, phase=0, warp=0.0, drift=0.0, step=14):
    out = []
    for k in range(n):
        ph = phase + k * drift
        a = amp * (1 + .35 * math.sin(k * .7))
        fn = lambda x, k=k, ph=ph, a=a: y0 + k * gap + a * math.sin(2 * math.pi * x / wl + ph) + warp * math.sin(2 * math.pi * x / (wl * .43) + ph * 1.7 + k * .3) * a
        out.append(band(fn, x0, x1, thick, step))
    return ''.join(out)
def rayos(cx, cy, r0, r1, n, frac=.5, twist=.25, rot=0, jitter=None):
    out = []; da = 2 * math.pi / n
    for i in range(n):
        a0 = rot + i * da; a1 = a0 + da * frac
        rr = r1 if not jitter else r1 * (1 - jitter * ((i * 37) % 5) / 5)
        P = lambda a, r: (cx + r * math.cos(a), cy + r * math.sin(a))
        p0, p1, p2, p3 = P(a0, r0), P(a0 + twist, rr), P(a1 + twist, rr), P(a1, r0)
        c1 = P(a0 + twist * .2, (r0 + rr) / 2 * 1.04); c2 = P(a1 + twist * .2, (r0 + rr) / 2 * 1.04)
        out.append(f'<path d="M{f(p0[0])} {f(p0[1])} Q{f(c1[0])} {f(c1[1])} {f(p1[0])} {f(p1[1])} L{f(p2[0])} {f(p2[1])} Q{f(c2[0])} {f(c2[1])} {f(p3[0])} {f(p3[1])} Z" fill="{B}"/>')
    return ''.join(out)
def anillos_ondulados(cx, cy, r0, n, gap, thick, amp=10, lobes=7, ph=0):
    out = []
    for k in range(n):
        r = r0 + k * gap; pts_o = []; pts_i = []
        for j in range(181):
            t = 2 * math.pi * j / 180; w = amp * math.sin(lobes * t + ph + k * .5)
            pts_o.append((cx + (r + thick + w) * math.cos(t), cy + (r + thick + w) * math.sin(t))); pts_i.append((cx + (r + w) * math.cos(t), cy + (r + w) * math.sin(t)))
        out.append(f'<path fill-rule="evenodd" d="{poly_d(pts_o, True)}{poly_d(pts_i, True)}" fill="{B}"/>')
    return ''.join(out)
def disco(cx, cy, r, fill=B): return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}"/>'
def aro(cx, cy, r, w=3, col=B): return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{col}" stroke-width="{w}"/>'
def flor(cx, cy, R, capas=4, w=3, rot=0, col=B, relleno_alt=True):
    out = []
    for l in range(capas):
        n = 8 + 2 * l; Rl = R * (1 - l * .2); r0 = Rl * .12; wd = Rl * (.22 - l * .02)
        for i in range(n):
            a = rot + (i + (l % 2) * .5) * 360 / n
            d = f'M0 {-r0:.1f} C{wd:.1f} {-Rl*.35:.1f} {wd*1.1:.1f} {-Rl*.75:.1f} 0 {-Rl:.1f} C{-wd*1.1:.1f} {-Rl*.75:.1f} {-wd:.1f} {-Rl*.35:.1f} 0 {-r0:.1f}Z'
            fill = col if (l == capas - 1 and relleno_alt) else 'none'
            out.append(f'<path d="{d}" transform="translate({f(cx)} {f(cy)}) rotate({a:.1f})" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>')
            if l >= 1: out.append(f'<path d="M0 {-r0-4:.1f} L0 {-Rl*.8:.1f}" transform="translate({f(cx)} {f(cy)}) rotate({a:.1f})" stroke="{col}" stroke-width="{w*.6:.1f}" fill="none"/>')
    out.append(disco(cx, cy, R * .09, col)); out.append(aro(cx, cy, R * .17, w, col))
    for i in range(12):
        a = math.radians(rot + i * 30); out.append(disco(cx + R * .26 * math.cos(a), cy + R * .26 * math.sin(a), R * .015 + 1.5, col))
    return ''.join(out)
def espiral(cx, cy, r0, r1, turns, a0, dirn=1, n=70):
    pts = []
    for i in range(n + 1):
        t = i / n; r = r0 + (r1 - r0) * (1 - t); a = a0 + dirn * turns * 2 * math.pi * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts
def hoja(x, y, ang, L, w, col=B):
    return f'<path d="M0 0 C{w:.1f} {-L*.3:.1f} {w:.1f} {-L*.7:.1f} 0 {-L:.1f} C{-w:.1f} {-L*.7:.1f} {-w:.1f} {-L*.3:.1f} 0 0Z" transform="translate({f(x)} {f(y)}) rotate({ang:.1f})" fill="{col}"/><path d="M0 -4 L0 {-L*.8:.1f}" transform="translate({f(x)} {f(y)}) rotate({ang:.1f})" stroke="{K}" stroke-width="2" fill="none"/>'
def lianas(x, y, ang, L, curl=1, w=4, hojas=True, seed=1):
    """curva látigo art nouveau que termina en espiral, con hojas."""
    rnd = random.Random(seed); out = []; pts = []; a = math.radians(ang); px, py = x, y
    n = 60
    for i in range(n):
        t = i / n; a += curl * (math.sin(t * 5 + seed) * .035 + .012); px += math.cos(a) * L / n; py += math.sin(a) * L / n; pts.append((px, py))
        if hojas and i % 9 == 4:
            side = 1 if (i // 9) % 2 == 0 else -1
            out.append(hoja(px, py, math.degrees(a) + 90 + side * 60, L * .09 * (1 - t * .5), L * .02))
    sp = espiral(px + math.cos(a) * 1, py + math.sin(a) * 1, 0, L * .06, 1.6, a - math.pi / 2 * curl, curl)
    sp = [(px + (sx - sp[-1][0]) , py + (sy - sp[-1][1])) for sx, sy in sp][::-1] if False else sp
    pts2 = pts + [(px + (sx - sp[0][0]), py + (sy - sp[0][1])) for sx, sy in sp[::-1]]
    out.append(f'<path d="{poly_d([(x, y)] + pts)}" fill="none" stroke="{B}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    cx, cy = px, py
    spir = espiral(cx, cy + 0, 0, L * .07, 1.8, a + math.pi / 2 * curl * -1, curl)
    spir = [(cx + (sx - spir[-1][0]), cy + (sy - spir[-1][1])) for sx, sy in spir]
    out.append(f'<path d="{poly_d(spir)}" fill="none" stroke="{B}" stroke-width="{w}" stroke-linecap="round"/>')
    return ''.join(out)
def pavo(cx, cy, r, rot=0):
    """ojo de pluma: elipses concéntricas en capas azul/negro."""
    out = [f'<g transform="translate({f(cx)} {f(cy)}) rotate({rot})">']
    pal = [(r, B), (r * .78, K), (r * .62, B), (r * .42, K), (r * .26, B)]
    for k, (rr, c) in enumerate(pal):
        out.append(f'<path d="M0 {-rr*1.6:.1f} C{rr*.9:.1f} {-rr*.9:.1f} {rr:.1f} {rr*.6:.1f} 0 {rr*.9:.1f} C{-rr:.1f} {rr*.6:.1f} {-rr*.9:.1f} {-rr*.9:.1f} 0 {-rr*1.6:.1f}Z" fill="{c}"/>')
    for i in range(-3, 4): out.append(f'<path d="M0 {r*.9:.1f} L{i*r*.55:.1f} {r*2.6:.1f}" stroke="{B}" stroke-width="3" fill="none"/>')
    out.append('</g>'); return ''.join(out)
def topo(cx, cy, r0, n, gap, w=3, seed=3, sq=1.0):
    rnd = random.Random(seed); ph = [rnd.random() * 6.28 for _ in range(4)]; out = []
    for k in range(n):
        r = r0 + k * gap; pts = []
        for j in range(121):
            t = 2 * math.pi * j / 120; rr = r * (1 + .12 * math.sin(2 * t + ph[0] + k * .08) + .07 * math.sin(3 * t + ph[1]) + .04 * math.sin(5 * t + ph[2] - k * .1))
            pts.append((cx + rr * math.cos(t), cy + sq * rr * math.sin(t)))
        out.append(f'<path d="{poly_d(pts, True)}" fill="none" stroke="{B}" stroke-width="{w}" stroke-linejoin="round"/>')
    return ''.join(out)
def nodos(pts, edges, r=14, w=3):
    out = []
    for a, b, bend in edges:
        (x1, y1), (x2, y2) = pts[a], pts[b]; mx, my = (x1 + x2) / 2, (y1 + y2) / 2; dx, dy = x2 - x1, y2 - y1
        cx, cy = mx - dy * bend, my + dx * bend
        out.append(f'<path d="M{f(x1)} {f(y1)} Q{f(cx)} {f(cy)} {f(x2)} {f(y2)}" fill="none" stroke="{B}" stroke-width="{w}" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(pts):
        rr = r * (1 + (i % 3) * .35)
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rr)}" fill="{K}" stroke="{B}" stroke-width="{w+1}"/><circle cx="{f(x)}" cy="{f(y)}" r="{f(rr*.42)}" fill="{B}"/>')
    return ''.join(out)
def arcos_senal(cx, cy, r0, n, gap, w, a0, a1):
    out = []
    for k in range(n):
        r = r0 + k * gap
        p = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        (x1, y1), (x2, y2) = p(a0), p(a1)
        out.append(f'<path d="M{f(x1)} {f(y1)} A{f(r)} {f(r)} 0 0 1 {f(x2)} {f(y2)}" fill="none" stroke="{B}" stroke-width="{w}" stroke-linecap="round"/>')
    return ''.join(out)
def grabado(x, y, w, h, n, ang=-30, wd=2.2, fn=None):
    """rayado de grabado dentro de un rectángulo con curva suave."""
    out = []
    for i in range(n):
        yy = y + i * h / n
        pts = [(x + j * 10, yy + 8 * math.sin(j * .12 + i * .3)) for j in range(int(w / 10) + 1)]
        out.append(f'<path d="{poly_d(pts)}" fill="none" stroke="{B}" stroke-width="{wd}"/>')
    return ''.join(out)
def svg(w, h, body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">{body}</svg>'
def estrellas(rnd, n, x0, y0, x1, y1):
    out = []
    for _ in range(n):
        x, y, r = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(5, 13)
        out.append(f'<path d="M{f(x)} {f(y-r)} Q{f(x)} {f(y)} {f(x+r)} {f(y)} Q{f(x)} {f(y)} {f(x)} {f(y+r)} Q{f(x)} {f(y)} {f(x-r)} {f(y)} Q{f(x)} {f(y)} {f(x)} {f(y-r)}Z" fill="{B}"/>')
    return ''.join(out)

W, H = 1440, 900
def plano_inicio():
    cx, cy = 720, 450; rnd = random.Random(5)
    b = rayos(cx, cy, 415, 1100, 24, .45, .22, 0.05)
    b += anillos_ondulados(cx, cy, 262, 3, 26, 11, 9, 9, 0)
    b += disco(cx, cy, 245, B) + disco(cx, cy, 218, K)  # ojo central: negro, ahí vive el rojo
    b += ondas(260, 640, 720, 4, 36, 12, 18, 300, 0, .0, .6)
    b += flor(330, 230, 150, 4, 3, 10) + lianas(300, 880, -80, 240, 1, 4, True, 2) + lianas(1130, 880, -100, 220, -1, 4, True, 7)
    b += estrellas(rnd, 18, 280, 30, 1160, 880)
    return svg(W, H, b)
def plano_marcas():
    rnd = random.Random(8); b = ondas(-20, W + 20, 70, 11, 78, 24, 46, 700, 0, .25, .55, 12)
    b += estrellas(rnd, 22, 40, 30, 1400, 870)
    return svg(W, H, b)
def plano_juegos():
    b = flor(300, 430, 380, 5, 3, 0) + pavo(1010, 350, 70, 20) + pavo(1170, 650, 52, -16) + pavo(900, 690, 42, 30)
    b += lianas(760, 860, -95, 420, 1, 4, True, 3) + lianas(1360, 880, -110, 380, -1, 4, True, 9) + lianas(700, 80, 80, 300, -1, 4, True, 5)
    b += estrellas(random.Random(2), 14, 600, 30, 1400, 500)
    return svg(W, H, b)
def plano_streaming():
    cx, cy = 360, 450
    b = arcos_senal(cx, cy, 160, 5, 62, 20, -62, 62) + arcos_senal(cx, cy, 190, 4, 62, 8, 118, 242)
    b += ondas(800, W + 20, 120, 8, 92, 26, 40, 520, 1, .0, .6, 12)
    b += disco(cx, cy, 120, B) + disco(cx, cy, 92, K)
    b += estrellas(random.Random(4), 16, 560, 30, 1400, 870)
    return svg(W, H, b)
def plano_ia():
    rnd = random.Random(11)
    b = topo(430, 450, 60, 12, 36, 3, 4, .82)
    pts = [(900, 160), (1100, 260), (1290, 150), (1000, 430), (1220, 470), (1380, 380), (880, 640), (1110, 700), (1300, 640), (1020, 840)]
    ed = [(0, 1, .12), (1, 2, -.1), (0, 3, .15), (1, 3, -.12), (1, 4, .1), (2, 5, .2), (4, 5, -.1), (3, 4, .15), (3, 6, -.12), (4, 7, .1), (6, 7, .12), (7, 8, -.1), (4, 8, .12), (6, 9, .1), (7, 9, -.14), (5, 8, .1)]
    b += nodos(pts, ed, 13, 3) + lianas(40, 880, -70, 380, 1, 4, True, 12) + lianas(1400, 40, 100, 300, 1, 4, True, 6)
    b += estrellas(rnd, 22, 40, 30, 1400, 870)
    return svg(W, H, b)
def plano_logo():
    b = flor(720, 450, 430, 6, 3, 0) + anillos_ondulados(720, 450, 450, 2, 30, 10, 10, 12) + estrellas(random.Random(9), 14, 40, 30, 1400, 870)
    return svg(W, H, b)
def plano_sistema():
    b = ondas(-20, W + 20, 40, 10, 92, 12, 60, 900, 0, .2, .5, 12) + pavo(120, 760, 60, 10) + pavo(1330, 130, 56, -20)
    return svg(W, H, b)
def plano_contacto():
    b = ondas(-20, W + 20, 640, 5, 48, 18, 30, 560, 0, .0, .6, 12) + flor(1180, 330, 210, 5, 3, 5) + lianas(980, 880, -90, 300, 1, 4, True, 4) + estrellas(random.Random(3), 16, 40, 30, 1400, 600)
    return svg(W, H, b)

# ----- cortes de sección (tira 1440x200, azul sobre transparente) -----
def corte_cupula():  # arcos grandes tipo cebolla / ogiva con banda doble
    p = ''
    for k, (y, t) in enumerate([(70, 22), (120, 12), (160, 6)]):
        pts = [(x, 200 - (130 - k * 28) * abs(math.sin(math.pi * x / 360)) ** .75 * 1) for x in range(0, 1461, 12)]
        pts_b = [(x, yy + t) for x, yy in reversed(pts)]
        p += f'<path d="{poly_d(pts + pts_b, True)}" fill="{B}"/>'
    return svg(W, 200, p).replace('slice', 'none')
def corte_ola():
    return svg(W, 200, ondas(-20, W + 20, 40, 3, 52, 26, 26, 720, 0, .5, 1.2, 10).replace('', '')).replace('slice', 'none')
def corte_festones():
    p = ''; r = 60
    for row, (yy, t) in enumerate([(110, 24), (150, 10)]):
        for i in range(0, 14):
            cx = i * 2 * r + r + (row * r * .0)
            p += f'<path d="M{cx-r} {yy+60} A{r} {r} 0 0 1 {cx+r} {yy+60}" fill="none" stroke="{B}" stroke-width="{t}"/>'
    return svg(W, 200, p).replace('slice', 'none')
def corte_gota():  # pétalos/gotas apuntadas
    p = ''
    for i in range(0, 11):
        x = i * 150 + 20
        p += f'<path d="M{x} 200 C{x} 120 {x+60} 90 {x+75} 20 C{x+90} 90 {x+150} 120 {x+150} 200Z" fill="{B}"/><path d="M{x+45} 200 C{x+45} 150 {x+75} 120 {x+75} 80 C{x+75} 120 {x+105} 150 {x+105} 200Z" fill="{K}"/>'
    return svg(W, 200, p).replace('slice', 'none')
def corte_sol():  # semicírculo de sol naciente + rayos
    p = disco(720, 220, 120) + disco(720, 220, 96, K) + rayos(720, 220, 140, 300, 40, .45, .0, math.pi)
    return svg(W, 200, p).replace('slice', 'none')

def main():
    for n, fn in [('inicio', plano_inicio), ('marcas', plano_marcas), ('juegos', plano_juegos), ('streaming', plano_streaming), ('ia', plano_ia), ('logo', plano_logo), ('sistema', plano_sistema), ('contacto', plano_contacto)]:
        open(os.path.join(OUT, 'planos', n + '.svg'), 'w').write(fn())
    for n, fn in [('cupula', corte_cupula), ('ola', corte_ola), ('festones', corte_festones), ('gota', corte_gota), ('sol', corte_sol)]:
        open(os.path.join(OUT, 'cortes', n + '.svg'), 'w').write(fn())
if __name__ == '__main__': main()
