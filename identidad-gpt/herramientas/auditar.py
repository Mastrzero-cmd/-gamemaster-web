#!/usr/bin/env python3
"""Auditoría estática sin dependencias. Uso: python3 herramientas/auditar.py [carpeta]."""
import colorsys
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {'.css', '.html', '.js', '.mjs', '.svg'}
EXEMPT = {'assets/logo', 'assets/marcas'}
NAMES = {'black': '#000000', 'white': '#ffffff', 'red': '#ff0000',
         'blue': '#0000ff', 'purple': '#800080', 'magenta': '#ff00ff',
         'fuchsia': '#ff00ff', 'violet': '#ee82ee', 'rebeccapurple': '#663399',
         'darkmagenta': '#8b008b', 'darkviolet': '#9400d3', 'blueviolet': '#8a2be2',
         'indigo': '#4b0082', 'orchid': '#da70d6', 'mediumorchid': '#ba55d3',
         'darkorchid': '#9932cc', 'mediumpurple': '#9370db', 'plum': '#dda0dd'}
COLOR = re.compile(r'#[\da-f]{3,8}\b|(?:rgba?|hsla?)\([^)]*\)|\b(?:' + '|'.join(NAMES) + r')\b', re.I)


def rgba(value):
    value = NAMES.get(value.lower(), value.lower())
    if value.startswith('#'):
        value = value[1:]
        if len(value) in (3, 4):
            value = ''.join(x * 2 for x in value)
        if len(value) not in (6, 8):
            return None
        rgb = [int(value[n:n+2], 16) / 255 for n in (0, 2, 4)]
        return (*rgb, int(value[6:8], 16) / 255 if len(value) == 8 else 1)
    parts = re.findall(r'[-+]?(?:\d*\.)?\d+%?', value)
    if len(parts) < 3:
        return None
    alpha = float(parts[3].rstrip('%')) / (100 if parts[3].endswith('%') else 1) if len(parts) > 3 else 1
    if value.startswith('hsl'):
        h = float(parts[0]) / 360
        s, light = [float(p.rstrip('%')) / 100 for p in parts[1:3]]
        return (*colorsys.hls_to_rgb(h, light, s), alpha)
    return (*[float(p.rstrip('%')) / (100 if p.endswith('%') else 255) for p in parts[:3]], alpha)


def family(value):
    parsed = rgba(value)
    if not parsed:
        return 'unknown'
    h, s, _ = colorsys.rgb_to_hsv(*parsed[:3])
    if s < .25:
        return 'neutral'
    hue = h * 360
    if 255 < hue < 345:
        return 'prohibited'
    if hue < 40 or hue >= 345:
        return 'red'
    if 200 <= hue <= 255:
        return 'blue'
    return 'other'


def audit(root):
    findings = []
    count = 0
    global_variables = {}
    for sheet in root.rglob('*.css'):
        global_variables.update(re.findall(r'(--[\w-]+)\s*:\s*([^;}]+)', sheet.read_text()))
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        relative = path.relative_to(root).as_posix()
        if any(relative.startswith(folder + '/') for folder in EXEMPT):
            continue
        count += 1
        source = path.read_text(encoding='utf-8')

        def report(message, at=0):
            findings.append(f'{relative}:{source.count(chr(10), 0, at)+1}: {message}')

        rules = [
            (r'(?:linear|radial|conic|repeating-linear|repeating-radial)-gradient\s*\(|<\s*(?:linearGradient|radialGradient)\b', 'Degradado'),
            (r'(?<![\w-])(?:backdrop-filter|filter)\s*:\s*(?!none)[^;}\n]+|<\s*(?:filter|feGaussianBlur)\b|\bblur\s*\(', 'Filtro o desenfoque'),
            (r'\btext-shadow\s*:\s*(?!none)[^;}\n]+', 'Sombra de texto'),
            (r'(?<![\w-])(?:mask(?:-image)?|clip-path)\s*:|<\s*(?:mask|clipPath)\b', 'Máscara o recorte'),
            (r'\bmix-blend-mode\s*:\s*(?!normal)', 'Mezcla de planos'),
            (r'\b(?:purple|magenta|fuchsia|violet|rebeccapurple)\b', 'Color fuera de la paleta'),
            ('com' + 'part', 'Palabra restringida'),
        ]
        for pattern, label in rules:
            for match in re.finditer(pattern, source, re.I):
                report(label, match.start())
        for match in re.finditer(r'\b(?:opacity|fill-opacity|stroke-opacity)\s*(?:=\s*[\"\']|:\s*)([\d.]+)(%)?', source, re.I):
            if float(match[1]) / (100 if match[2] else 1) < 1:
                report('Opacidad menor que 1', match.start())
        for match in re.finditer(r'box-shadow\s*:\s*([^;}]+)', source, re.I):
            # Longitudes: desplazamiento x, y, radio de difusión, expansión.
            value = COLOR.sub('', match[1])
            for shadow in value.split(','):
                lengths = re.findall(r'(?<![\w-])-?(?:\d*\.)?\d+(?:px|rem|em)?', shadow)
                if len(lengths) >= 3 and float(re.sub('[a-z]+', '', lengths[2])) != 0:
                    report('Sombra con difusión', match.start())
        color_families = set()
        for match in COLOR.finditer(source):
            parsed = rgba(match[0])
            if parsed is None:
                report('Color no interpretable: ' + match[0], match.start())
                continue
            if parsed[3] < 1:
                report('Alfa menor que 1: ' + match[0], match.start())
            kind = family(match[0])
            color_families.add(kind)
            if kind in ('prohibited', 'other'):
                report('Color fuera de la paleta: ' + match[0], match.start())
        if path.suffix == '.svg':
            if {'red', 'blue'} <= color_families:
                report('Rojo y azul dentro del mismo SVG')
            try:
                document = ET.fromstring(source)
                def inspect_text(node, inherited='black'):
                    ink = node.attrib.get('fill', inherited)
                    ink_style = re.search(r'(?:^|;)\s*fill\s*:\s*([^;]+)', node.attrib.get('style', ''))
                    if ink_style:
                        ink = ink_style[1]
                    if node.tag.rsplit('}', 1)[-1] in ('text', 'tspan'):
                        if any(family(c[0]) == 'red' for c in COLOR.finditer(ink)):
                            report('Texto SVG rojo')
                    for child in node:
                        inspect_text(child, ink)
                inspect_text(document)
            except ET.ParseError as error:
                report('SVG no válido: ' + str(error))
        variables = global_variables | dict(re.findall(r'(--[\w-]+)\s*:\s*([^;}]+)', source))
        for match in re.finditer(r'(?:^|[;{\"\'])\s*color\s*:\s*([^;}\"\']+)', source):
            value = match[1].strip()
            for _ in range(8):
                value = re.sub(r'var\((--[\w-]+)\)', lambda m: variables.get(m[1], m[0]), value)
            if any(family(c[0]) == 'red' for c in COLOR.finditer(value)):
                report('Texto rojo (requiere revisión; esta propuesta sólo usa texto neutro)', match.start())
        for match in re.finditer(r'(?:\.style\.color\s*=|[\"\']color[\"\']\s*,)\s*[\"\']([^\"\']+)', source):
            if any(family(c[0]) == 'red' for c in COLOR.finditer(match[1])):
                report('Texto rojo asignado desde JS', match.start())
    return count, findings


if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    count, findings = audit(root)
    for finding in findings:
        print(finding)
    print(f'{count} archivos revisados · {len(findings)} hallazgos · logos exentos: assets/logo y assets/marcas')
    sys.exit(bool(findings))
