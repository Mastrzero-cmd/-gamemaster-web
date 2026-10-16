#!/usr/bin/env python3
"""Capas ROJAS de v9d: composiciones de íconos grandes (heroes/) y piezas pequeñas (piezas/). Coordenadas = las del plano azul (1440x900);
el viewBox se amplía 12 % por cada lado para que los íconos rompan el marco."""
import os, re, math
from iconos import ICONOS, R, K
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
E = .12; VB = f'{-1440*E:.1f} {-900*E:.1f} {1440*(1+2*E):.1f} {900*(1+2*E):.1f}'
_n = [0]
def put(name, cx, cy, size, rot=0):
    _n[0] += 1; body = ICONOS[name]()
    body = re.sub(r'id="(\w+)"', lambda m: f'id="{m.group(1)}{_n[0]}"', body); body = re.sub(r'url\(#(\w+)\)', lambda m: f'url(#{m.group(1)}{_n[0]})', body)
    sc = size / 400
    return f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot}) scale({sc:.3f}) translate(-200 -200)">{body}</g>'
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" preserveAspectRatio="xMidYMid slice">{body}</svg>'
HEROES = {
 'inicio': [('hongo', 720, 460, 520, 8)],
 'juegos': [('triforce', 420, 440, 540, -4), ('pikachu', 1010, 570, 430, 6)],
 'marcas': [('anillo', 230, 380, 380, -14)],
 'streaming': [('tv', 380, 450, 400, -5), ('play', 1090, 450, 250, 0)],
 'ia': [('robot', 430, 440, 420, -4), ('destello', 1100, 470, 250, 0)],
 'logo': [('bloque', 190, 220, 220, -10), ('estrella', 1270, 700, 230, 12)],
}
PIEZAS = {
 'inicio': [('estrella', 1090, 170, 110, 15), ('destello', 420, 760, 90, 0), ('anillo', 1100, 760, 140, -10), ('corazon', 430, 190, 100, -8)],
 'juegos': [('espada', 1270, 250, 250, 28), ('corazon', 780, 130, 110, -10), ('pokebola', 1230, 790, 190, 10), ('hongo', 150, 780, 120, -10)],
 'marcas': [('destello', 1390, 40, 100, 0), ('destello', 960, 840, 70, 0), ('kirby', 1380, 820, 240, 8), ('estrella', 760, 70, 80, -10)],
 'streaming': [('pacman', 1260, 190, 150, -8), ('fantasma', 1320, 770, 130, 6), ('destello', 700, 140, 70, 0)],
 'ia': [('invasor', 1250, 140, 150, 0), ('bloque', 880, 790, 120, 12), ('destello', 80, 140, 90, 0)],
 'logo': [('creeper', 1280, 170, 160, 8), ('mando', 220, 740, 260, -8), ('destello', 720, 90, 80, 0)],
}
def main():
    for d, M in (('heroes', HEROES), ('piezas', PIEZAS)):
        for n, items in M.items():
            open(os.path.join(OUT, d, n + '.svg'), 'w').write(svg(''.join(put(*it) for it in items)))
    # contacto: sol rojo con rayos negros
    sol = f'<circle cx="500" cy="450" r="370" fill="{R}" stroke="{K}" stroke-width="12"/>' + ''.join(
        f'<path d="M500 450 L{500+370*math.cos(a):.1f} {450+370*math.sin(a):.1f}" stroke="{K}" stroke-width="7" stroke-linecap="round"/>' for a in [i * math.pi / 12 for i in range(24)]) + f'<circle cx="500" cy="450" r="140" fill="{K}"/>'
    sol += put('pikachu', 500, 450, 230, 0)
    open(os.path.join(OUT, 'heroes', 'contacto.svg'), 'w').write(svg(sol))
    open(os.path.join(OUT, 'piezas', 'contacto.svg'), 'w').write(svg(put('pacman', 1060, 150, 130, -8) + put('fantasma', 1250, 170, 110, 6) + put('estrella', 1180, 740, 150, 12) + put('hongo', 130, 780, 130, -10)))
if __name__ == '__main__': main()
