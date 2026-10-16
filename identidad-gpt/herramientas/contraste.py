#!/usr/bin/env python3
"""WCAG 2: cálculo sin dependencias, paleta CSS + pares reales del navegador."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def luminance(rgb):
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in (c / 255 for c in rgb)]
    return sum(v * w for v, w in zip(linear, (.2126, .7152, .0722)))


def ratio(fg, bg):
    a, b = sorted([luminance(fg), luminance(bg)])
    return (b + .05) / (a + .05)


def rgb(hexvalue):
    value = hexvalue.lstrip('#')
    return [int(value[n:n+2], 16) for n in (0, 2, 4)]


def main():
    css = (ROOT / 'styles.css').read_text()
    palette = dict(re.findall(r'--([\w-]+):\s*(#[\da-fA-F]{6})', css))
    # Todos los pares de texto permitidos, incluso estados hover, selección y foco.
    pairs = [(fg, bg) for fg in ('ice', 'muted') for bg in ('black', 'surface')]
    pairs += [('black', 'ice')]  # Selección del navegador.
    failures = 0
    for fg, bg in pairs:
        value = ratio(rgb(palette[fg]), rgb(palette[bg]))
        ok = value >= 4.5
        failures += not ok
        print(f'{palette[fg]} / {palette[bg]} : {value:.2f}:1 · texto normal · {"OK" if ok else "FALLA"}')
    # Evita que nuevas declaraciones de texto queden fuera de la matriz.
    text_values = re.findall(r'(?<![\w-])color:\s*([^;}]+)', css)
    allowed = {'var(--ice)', 'var(--muted)', 'var(--black)', 'inherit'}
    for value in text_values:
        if value.strip() not in allowed:
            failures += 1
            print('FALLA: color de texto sin par registrado:', value)
    report = ROOT / 'herramientas' / 'informe-navegador.json'
    if report.exists():
        data = json.loads(report.read_text())
        actual = {}
        for viewport in data['vistas']:
            for pair in viewport['contrastes']:
                key = (tuple(pair['frente']), tuple(pair['fondo']), pair['minimo'])
                actual[key] = pair.get('ejemplo', '')
        print(f'Pares reales del navegador: {len(actual)} (incluye 1440, 390 y 430 px).')
        for (fg, bg, minimum), example in actual.items():
            value = ratio(fg, bg)
            ok = value >= minimum
            failures += not ok
            print(f'{fg} / {bg} : {value:.2f}:1 · mínimo {minimum} · {"OK" if ok else "FALLA"} · {example}')
    else:
        print('Pares del navegador pendientes: ejecutar verificar.py para incluirlos.')
    print(f'Contraste: {failures} fallas. Objetivos: 4.5:1 normal, 3:1 grande.')
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
