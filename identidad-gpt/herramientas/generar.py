#!/usr/bin/env python3
"""Arte original Punto de entrada. Sólo biblioteca estándar; salida determinista."""
from pathlib import Path
from math import sin, cos, pi
import re
from xml.etree import ElementTree as ET

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'arte'
BLACK, BLUE, RED, DARK = '#080808', '#243cff', '#ff392b', '#a51e18'


def svg(name, body, width=1440, height=240):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (name + '.svg')).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'fill="none">{body}</svg>\n', encoding='utf-8')


def generate():
    # Eventail ouvert : rayons et cordes sans fenêtre rectangulaire.
    rays = []
    for n in range(64):
        a = pi * (0.04 + n / 70)
        x, y = 730 + cos(a) * 850, 430 - sin(a) * 540
        rays.append(f'<path d="M730 430L{x:.2f} {y:.2f}"/>')
    for n in range(1, 16):
        r = n * 61
        rays.append(f'<path d="M{730-r} 430 Q730 {430-r*1.3} {730+r} 430"/>')
    svg('fuga-radial', f'<g stroke="{BLUE}" stroke-width="1.5">'+''.join(rays)+'</g>', 1440, 500)
    # Un cartucho: carcasa roja, canto oscuro y detalles negros. Sin azul.
    contacts = ''.join(f'<rect x="{188+n*24}" y="370" width="12" height="46" fill="{RED}"/>' for n in range(9))
    ribs = ''.join(f'<path d="M{130+n*23} 128v36"/>' for n in range(14))
    svg('cartucho', f'''<g transform="translate(70 10) rotate(-13 300 250)">
      <path d="M92 80H454L506 126V420L464 460H92Z" fill="{DARK}"/>
      <path d="M64 56H426L478 102V396L438 436H64Z" fill="{RED}"/>
      <path d="M426 56V102H478M64 116H478" stroke="{BLACK}" stroke-width="8"/>
      <path d="M120 128V164M120 180H420V334H120Z" fill="{BLACK}"/>
      <g stroke="{BLACK}" stroke-width="8">{ribs}</g>
      <path d="M145 205H225V227H167V248H214V270H167V310H145ZM256 205H281L310 264L339 205H364V310H342V248L310 293L278 248V310H256Z" fill="{RED}"/>
      <path d="M164 354H426V436H164Z" fill="{BLACK}"/>{contacts}
      <path d="M85 370H128M106 349V391" stroke="{BLACK}" stroke-width="9"/>
    </g>''', 640, 520)
    # Altavoz circular: centro rojo, caja asimétrica. Otra silueta, no auriculares.
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{BLACK}"/>'
                   for y in range(180, 371, 13) for x in range(100, 291, 13)
                   if (x-195)**2+(y-275)**2 < 91**2)
    svg('bocina', f'''<path d="M80 35H290L328 75V432H80Z" fill="{DARK}"/>
      <path d="M48 20H278V414H48Z" fill="{RED}"/>
      <circle cx="163" cy="96" r="39" fill="{BLACK}"/>
      <circle cx="163" cy="96" r="15" fill="{DARK}"/>
      <circle cx="163" cy="275" r="99" fill="{BLACK}"/>
      <circle cx="163" cy="275" r="86" fill="{DARK}"/>
      <circle cx="163" cy="275" r="47" fill="{RED}"/>
      <path d="M65 386H260" stroke="{BLACK}" stroke-width="7"/>''', 380, 460)
    # Servidor: tres bahías, perforación negra, una carcasa sin duplicados cromáticos.
    slots = ''.join(f'<path d="M76 {70+n*85}H294V{130+n*85}H76Z" fill="{BLACK}"/>'
                    f'<path d="M96 {88+n*85}H220V{112+n*85}H96Z" fill="{DARK}"/>'
                    f'<circle cx="268" cy="{100+n*85}" r="8" fill="{RED}"/>' for n in range(3))
    svg('servidor', f'''<path d="M56 28H310L350 66V370H56Z" fill="{DARK}"/>
      <path d="M30 8H288L324 44V348H30Z" fill="{RED}"/>{slots}
      <path d="M48 322H306" stroke="{BLACK}" stroke-width="8"/>''', 380, 400)
    # Gramáticas traseras, nunca rellenos detrás del texto.
    rings = ''.join(f'<path d="M{700-r} 160a{r} {r*.65} 0 0 1 {r*2} 0"/>' for r in range(55, 720, 24))
    svg('acustica', f'<g stroke="{BLUE}" stroke-width="1.5">{rings}</g>', 1440, 320)
    branches = []
    for n in range(12):
        y = 20+n*22
        branches.append(f'<path d="M40 160H{160+n*24}L{340+n*24} {y}H1380"/>')
        branches.append(f'<circle cx="{1000+n*28}" cy="{y}" r="5"/>')
    svg('bifurcaciones', f'<g stroke="{BLUE}" stroke-width="1.5">'+''.join(branches)+'</g>', 1440, 300)
    lattice = ''.join(f'<path d="M{x} 0l-120 120 120 120 120-120Z"/>' for x in range(-80, 1561, 80))
    svg('rombos', f'<g stroke="{BLUE}" stroke-width="1.5">{lattice}</g>', 1440, 240)
    # Cinco cortes distintos. Cada archivo tiene sólo una familia cromática.
    comb = ''.join(f'<path d="M{x} 0h12v{45+(n%5)*17}l-12 20Z" fill="{BLUE}"/>' for n,x in enumerate(range(0,1440,32)))
    svg('corte-peine', comb, 1440, 140)
    holes = ''.join(f'<circle cx="{x}" cy="62" r="14" fill="{BLACK}"/>' for x in range(40,1440,56))
    svg('corte-perforado', f'<path d="M0 28H1440V96H0Z" fill="{RED}"/>'+holes, 1440, 124)
    iris = ''.join(f'<path d="M{180+n*180} 8L{270+n*180} 116H{130+n*180}Z" stroke="{BLUE}" stroke-width="2"/>' for n in range(7))
    svg('corte-prismas', iris, 1440, 130)
    teeth = ''.join(f'<path d="M{x} 14l38 54-38 54-38-54Z" fill="{RED}"/>' for x in range(80,1440,160))
    svg('corte-diamantes', teeth, 1440, 136)
    braid = ''.join(f'<path d="M-80 {25+n*12}C200 {145+n*12} 420 {-90+n*12} 700 {40+n*12}S1180 {145+n*12} 1520 {20+n*12}"/>' for n in range(7))
    svg('corte-trenza', f'<g stroke="{BLUE}" stroke-width="2">{braid}</g>', 1440, 180)
    # Variantes locales monocolor de marcas sin versión hielo en E_logos.
    # Se preservan los originales copiados; sólo se cambia la tinta, no los trazos.
    brands = OUT.parent / 'marcas'
    for name in ('chatgpt', 'xbox-game-pass', 'disney-plus', 'nintendo-switch'):
        content = (brands / (name + '.svg')).read_text()
        if name == 'nintendo-switch':
            content = re.sub(r'<path[^>]*fill="#e60012"[^>]*/>', '', content, count=1)
        content = re.sub(r'#[\da-fA-F]{3,8}\b', '#f2f5f4', content)
        content = re.sub(r'(<svg\b)', r'\1 fill="#f2f5f4"', content, count=1)
        ET.fromstring(content)
        (brands / (name + '-hielo.svg')).write_text(content)
    print(f'Arte original: {len(list(OUT.glob("*.svg")))} SVG reproducibles.')


if __name__ == '__main__':
    generate()
