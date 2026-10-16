#!/usr/bin/env python3
"""v10d · Capas ROJAS y NEGRAS. Coordenadas = las del plano azul (1440x900); el viewBox se amplía 12 % por lado para que lo rojo rompa el marco.
- heroes/ (masa roja grande, velocidad .30) y piezas/ (piezas pequeñas, .55): íconos de objetos + masas abstractas (cintas, discos, arcos).
- Los PERSONAJES (Pikachu, Kirby, Mario, Zelda, Sonic, Pac-Man, creeper...) NO se dibujan: son «slots» HTML (data-slot) con silueta genérica,
  pensados para sustituirse por imágenes generadas. La lista está en SLOTS.md (la escribe este script).
- medios/ (plano NEGRO medio, .08): bandas y discos negros con aro azul fino, entre el azul de fondo y el rojo."""
import os, re, math, json
from iconos import ICONOS, R, K
B = '#1616FF'
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
E = .12; VBX, VBY, VBW, VBH = -1440 * E, -900 * E, 1440 * (1 + 2 * E), 900 * (1 + 2 * E)
VB = f'{VBX:.1f} {VBY:.1f} {VBW:.1f} {VBH:.1f}'
_n = [0]; HALO = 22
def put(name, cx, cy, size, rot=0):
    _n[0] += 1; body = ICONOS[name]()
    ren = lambda s, k: re.sub(r'url\(#(\w+)\)', lambda m: f'url(#{m.group(1)}{k})', re.sub(r'id="(\w+)"', lambda m: f'id="{m.group(1)}{k}"', s))
    halo = ren(body.replace(R, K).replace('stroke-width="12"', f'stroke-width="{HALO}"'), f'h{_n[0]}')
    halo = re.sub(r'<clipPath.*?</clipPath>', '', halo)
    sc = size / 400
    return f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot}) scale({sc:.3f}) translate(-200 -200)"><g>{halo}</g>{ren(body, _n[0])}</g>'
def pts_d(pts, close=False): return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ('Z' if close else '')
def cinta(x0, x1, y, amp, wl, th, ph=0, rot=0):
    xs = list(range(int(x0), int(x1) + 1, 12))
    top = [(x, y + amp * math.sin(2 * math.pi * x / wl + ph)) for x in xs]; bot = [(x, yy + th) for x, yy in reversed(top)]
    d = pts_d(top + bot, True)
    return f'<g transform="rotate({rot} {(x0+x1)/2:.0f} {y:.0f})"><path d="{d}" fill="none" stroke="{K}" stroke-width="{HALO*2}" stroke-linejoin="round"/><path d="{d}" fill="{R}" stroke="{K}" stroke-width="12" stroke-linejoin="round"/></g>'
def disco_r(cx, cy, r, anillo=0):
    if anillo:
        d = f'M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0Z M{cx-r+anillo} {cy} a{r-anillo} {r-anillo} 0 1 1 {2*(r-anillo)} 0 a{r-anillo} {r-anillo} 0 1 1 {-2*(r-anillo)} 0Z'
        return f'<path fill-rule="evenodd" d="{d}" fill="{R}" stroke="{K}" stroke-width="{HALO*2}"/><path fill-rule="evenodd" d="{d}" fill="{R}" stroke="{K}" stroke-width="12"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="{r+HALO}" fill="{K}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{R}" stroke="{K}" stroke-width="12"/>'
def arco(cx, cy, r, th, a0, a1):
    p = lambda rr, a: (cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a)))
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p(r, a0), p(r, a1), p(r - th, a1), p(r - th, a0)
    d = f'M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f} A{r-th} {r-th} 0 0 0 {x4:.1f} {y4:.1f}Z'
    return f'<path d="{d}" fill="none" stroke="{K}" stroke-width="{HALO*2}" stroke-linejoin="round"/><path d="{d}" fill="{R}" stroke="{K}" stroke-width="12" stroke-linejoin="round"/>'
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" preserveAspectRatio="xMidYMid slice">{body}</svg>'

# ---- composiciones: ('ico', nombre, x, y, tam, rot) | ('cinta', ...) | ('disco', ...) | ('arco', ...) | ('slot', nombre, x, y, tam, rot, forma)
FR = {
 'inicio': [('cinta', 120, 1100, 740, 36, 330, 90, 0, -3), ('slot', 'personaje-mario-hongo', 720, 440, 560, 8, 'blob')],
 'juegos': [('cinta', 60, 700, 120, 30, 400, 70, 1, 3), ('slot', 'personaje-zelda-trifuerza', 300, 470, 620, -4, 'triangulo'), ('slot', 'personaje-pikachu', 900, 600, 430, 6, 'blob')],
 'marcas': [('arco', 230, 470, 330, 110, 150, 330), ('slot', 'personaje-sonic-anillo', 190, 450, 400, -14, 'anillo')],
 'streaming': [('cinta', 760, 1610, 740, 30, 380, 70, 2, 0), ('ico', 'tv', 560, 450, 560, -5), ('ico', 'play', 1150, 450, 380, 0)],
 'ia': [('arco', 1000, 480, 300, 80, 200, 20), ('ico', 'robot', 520, 450, 540, -4), ('ico', 'destello', 1030, 470, 300, 0)],
 'logo': [('cinta', 560, 1500, 770, 30, 300, 70, 3, 2), ('ico', 'mando', 700, 640, 380, -8), ('slot', 'personaje-creeper', 1180, 640, 360, 8, 'cuadro')],
}
PC = {
 'inicio': [('slot', 'personaje-mario-estrella', 1170, 320, 170, 15, 'estrella'), ('ico', 'destello', 420, 770, 140, 0), ('slot', 'personaje-sonic-anillo-mini', 1130, 760, 210, -10, 'anillo'), ('ico', 'corazon', 330, 330, 130, -8)],
 'juegos': [('ico', 'espada', 1210, 170, 220, 30), ('ico', 'corazon', 650, 170, 150, -10), ('ico', 'pokebola', 890, 140, 230, 10), ('slot', 'personaje-mario-hongo-mini', 200, 690, 170, -10, 'blob')],
 'marcas': [('ico', 'destello', 60, 60, 110, 0), ('ico', 'destello', 1410, 770, 90, 0), ('slot', 'personaje-kirby', 420, 780, 200, 8, 'blob'), ('slot', 'personaje-mario-estrella-b', 330, 60, 110, -10, 'estrella')],
 'streaming': [('slot', 'personaje-pacman', 1250, 190, 230, -8, 'blob'), ('slot', 'personaje-fantasma', 1290, 690, 160, 6, 'fantasma'), ('slot', 'personaje-amongus', 740, 700, 150, -6, 'fantasma'), ('ico', 'destello', 700, 130, 100, 0)],
 'ia': [('slot', 'personaje-invasor', 1110, 120, 150, 0, 'cuadro'), ('slot', 'personaje-mario-bloque', 1080, 790, 150, 12, 'cuadro'), ('ico', 'destello', 90, 120, 130, 0)],
 'logo': [('ico', 'destello', 720, 80, 110, 0), ('ico', 'corazon', 1290, 150, 150, 10), ('slot', 'personaje-mario-estrella-c', 1350, 880, 170, -10, 'estrella')],
}
GROW = 1.5  # escala global del rojo (afinada para ~10 % de rojo medido)
SLOTS = []  # (nombre, seccion, capa, x, y, tam, rot, forma)
def layer(sec, capa, items):
    svgb, slots = '', []
    for it in items:
        it = list(it); k = it[0]
        if k in ('ico', 'slot'): it[4] = round(it[4] * GROW)
        elif k == 'cinta': it[6] = round(it[6] * 1.3)
        if k == 'ico': svgb += put(*it[1:])
        elif k == 'cinta': svgb += cinta(*it[1:])
        elif k == 'disco': svgb += disco_r(*it[1:])
        elif k == 'arco': svgb += arco(*it[1:])
        elif k == 'slot':
            _, name, x, y, size, rot, forma = it
            slots.append(dict(name=name, x=x, y=y, size=size, rot=rot, forma=forma)); SLOTS.append((name, sec, capa, x, y, size, rot, forma))
    return svg(svgb), slots

# ---- plano NEGRO medio (dentro de la ventana): bandas negras + discos negros con aro azul fino
def medio(sec, seed):
    import random
    rnd = random.Random(seed); b = ''
    for k in range(1):
        y = rnd.uniform(160, 700); amp = rnd.uniform(40, 90); wl = rnd.uniform(500, 900); ph = rnd.uniform(0, 6); th = rnd.uniform(40, 70)
        xs = range(-200, 1700, 14); top = [(x, y + amp * math.sin(2 * math.pi * x / wl + ph)) for x in xs]; bot = [(x, yy + th) for x, yy in reversed(top)]
        b += f'<path d="{pts_d(top + bot, True)}" fill="{K}"/>'
    for k in range(2):
        cx, cy, r = rnd.uniform(150, 1300), rnd.uniform(120, 780), rnd.uniform(40, 80)
        b += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r+16:.0f}" fill="none" stroke="{B}" stroke-width="7"/><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{K}"/>'
    return svg(b)

def main():
    secs = {}; os.makedirs(os.path.join(OUT, 'medios'), exist_ok=True)
    for sec in ['inicio', 'juegos', 'marcas', 'streaming', 'ia', 'logo', 'contacto']:
        if sec == 'contacto':
            open(os.path.join(OUT, 'medios', 'contacto.svg'), 'w').write(medio(sec, 7)); continue
        fr, s1 = layer(sec, 'fr', FR[sec]); pc, s2 = layer(sec, 'pc', PC[sec])
        open(os.path.join(OUT, 'heroes', sec + '.svg'), 'w').write(fr); open(os.path.join(OUT, 'piezas', sec + '.svg'), 'w').write(pc)
        os.makedirs(os.path.join(OUT, 'medios'), exist_ok=True)
        open(os.path.join(OUT, 'medios', sec + '.svg'), 'w').write(medio(sec, hash(sec) % 97 + 5 if False else sum(map(ord, sec))))
        secs[sec] = dict(fr=s1, pc=s2)
    # contacto
    sol = disco_r(500, 450, 410) + ''.join(f'<path d="M500 450 L{500+410*math.cos(a):.1f} {450+410*math.sin(a):.1f}" stroke="{K}" stroke-width="7" stroke-linecap="round"/>' for a in [i * math.pi / 12 for i in range(24)]) + f'<circle cx="500" cy="450" r="170" fill="{K}"/>'
    open(os.path.join(OUT, 'heroes', 'contacto.svg'), 'w').write(svg(sol))
    SLOTS.append(('personaje-pikachu-contacto', 'contacto', 'fr', 500, 450, 300, 0, 'blob'))
    _, s = None, [dict(name='personaje-pikachu-contacto', x=500, y=450, size=300, rot=0, forma='blob')]
    pcs = [('ico', 'destello', 1250, 130, 130, 0), ('ico', 'corazon', 1070, 240, 150, 10)]
    p, _ = layer('contacto', 'pc', pcs)
    pcs2 = [('slot', 'personaje-pacman-contacto', 1070, 740, 200, -8, 'blob'), ('slot', 'personaje-mario-estrella-d', 1240, 540, 140, 12, 'estrella')]
    p2, s2 = layer('contacto', 'pc', pcs2); p = svg(re.search(r'<svg[^>]*>(.*)</svg>', p).group(1) + re.search(r'<svg[^>]*>(.*)</svg>', p2).group(1))
    open(os.path.join(OUT, 'piezas', 'contacto.svg'), 'w').write(p)
    secs['contacto'] = dict(fr=s, pc=s2)
    json.dump(secs, open(os.path.join(os.path.dirname(__file__), 'slots.json'), 'w'), ensure_ascii=False, indent=1)
if __name__ == '__main__': main()
