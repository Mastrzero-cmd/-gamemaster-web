#!/usr/bin/env python3
"""Capas ROJAS de v9d: composiciones de íconos grandes (heroes/) y piezas pequeñas (piezas/). Coordenadas = las del plano azul (1440x900);
el viewBox se amplía 12 % por cada lado para que los íconos rompan el marco."""
import os, re, math
from iconos import ICONOS, R, K
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
E = .12; VB = f'{-1440*E:.1f} {-900*E:.1f} {1440*(1+2*E):.1f} {900*(1+2*E):.1f}'
_n = [0]
def put(name, cx, cy, size, rot=0):
    """Ícono rojo con un borde negro grueso debajo (misma geometría engrosada) para que nunca toque el azul."""
    _n[0] += 1; body = ICONOS[name]()
    ren = lambda s, k: re.sub(r'url\(#(\w+)\)', lambda m: f'url(#{m.group(1)}{k})', re.sub(r'id="(\w+)"', lambda m: f'id="{m.group(1)}{k}"', s))
    halo = ren(body.replace(R, K).replace('stroke-width="12"', 'stroke-width="22"'), f'h{_n[0]}')
    halo = re.sub(r'<clipPath.*?</clipPath>', '', halo)
    sc = size / 400
    return f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot}) scale({sc:.3f}) translate(-200 -200)"><g>{halo}</g>{ren(body, _n[0])}</g>'
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" preserveAspectRatio="xMidYMid slice">{body}</svg>'
HEROES = {
 'inicio': [('hongo', 720, 470, 967, 8)],
 'juegos': [('triforce', 400, 450, 846, -4), ('pikachu', 1040, 570, 652, 6)],
 'marcas': [('anillo', 230, 440, 561, -14)],
 'streaming': [('tv', 400, 450, 700, -5), ('play', 1100, 450, 459, 0)],
 'ia': [('robot', 450, 450, 749, -4), ('destello', 1110, 480, 459, 0)],
 'logo': [('bloque', 400, 250, 356, -10), ('estrella', 1230, 700, 435, 12)],
}
PIEZAS = {
 'inicio': [('estrella', 1170, 320, 181, 15), ('destello', 400, 770, 168, 0), ('anillo', 1130, 760, 246, -10), ('corazon', 330, 330, 144, -8)],
 'juegos': [('espada', 1210, 170, 210, 30), ('corazon', 650, 170, 144, -10), ('pokebola', 890, 140, 246, 10), ('hongo', 200, 750, 205, -10)],
 'marcas': [('destello', 1390, 40, 155, 0), ('destello', 960, 850, 103, 0), ('kirby', 1370, 800, 427, 8), ('estrella', 760, 70, 129, -10)],
 'streaming': [('pacman', 1250, 190, 272, -8), ('fantasma', 1290, 770, 233, 6), ('destello', 700, 130, 116, 0)],
 'ia': [('invasor', 1130, 130, 259, 0), ('bloque', 860, 790, 207, 12), ('destello', 90, 120, 155, 0)],
 'logo': [('creeper', 1290, 180, 272, 8), ('mando', 430, 790, 300, -8), ('destello', 720, 80, 129, 0)],
}
def main():
    for d, M in (('heroes', HEROES), ('piezas', PIEZAS)):
        for n, items in M.items():
            open(os.path.join(OUT, d, n + '.svg'), 'w').write(svg(''.join(put(*it) for it in items)))
    # contacto: sol rojo con rayos negros
    sol = f'<circle cx="500" cy="450" r="400" fill="{R}" stroke="{K}" stroke-width="12"/>' + ''.join(
        f'<path d="M500 450 L{500+410*math.cos(a):.1f} {450+410*math.sin(a):.1f}" stroke="{K}" stroke-width="7" stroke-linecap="round"/>' for a in [i * math.pi / 12 for i in range(24)]) + f'<circle cx="500" cy="450" r="170" fill="{K}"/>'
    sol += put('pikachu', 500, 450, 290, 0)
    open(os.path.join(OUT, 'heroes', 'contacto.svg'), 'w').write(svg(sol))
    open(os.path.join(OUT, 'piezas', 'contacto.svg'), 'w').write(svg(put('pacman', 1060, 150, 180, -8) + put('fantasma', 1270, 180, 150, 6) + put('estrella', 1180, 740, 200, 12) + put('hongo', 140, 780, 180, -10)))
if __name__ == '__main__': main()
