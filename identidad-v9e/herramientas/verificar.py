#!/usr/bin/env python3
"""Auditoría local de v9e. Ejecutar con Python 3 y Pillow, sin conexión."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

try:
    from PIL import Image
except ImportError:
    sys.exit('Falta Pillow para revisar el canal alfa de los PNG. No se instaló nada.')

ROOT = Path(__file__).resolve().parents[1]
WA = 'https://wa.me/525527699426'
failures = []
report = {'contrastes': [], 'png': [], 'comprobaciones': []}


def check(condition, message):
    report['comprobaciones'].append({'regla': message, 'ok': bool(condition)})
    if not condition:
        failures.append(message)


sources = {p: p.read_text(encoding='utf-8') for p in ROOT.rglob('*')
           if p.is_file() and p.suffix in {'.html', '.css', '.js', '.svg', '.py', '.md', '.json'}
           and not any(part.startswith('.') for part in p.relative_to(ROOT).parts)}
# El término se construye por partes para no escribirlo en ningún archivo.
restricted = re.compile('com' + 'part', re.I)
for path, source in sources.items():
    check(not restricted.search(source), f'Término restringido ausente: {path.relative_to(ROOT)}')

patterns = {
    'Rellenos sólidos': r'(?:linear|radial|conic|repeating-linear|repeating-radial)-gradient\s*\(|(?:linear|radial)Gradient\b|\bgradient\s*\(',
    'Sin efectos de difusión ni sombras': r'(?:\b(?:backdrop-)?filter\s*[:=]|<filter\b|\bblur\s*\(|\bbox-shadow\s*:|\btext-shadow\s*:)',
}
for path, source in sources.items():
    if path.suffix not in {'.html', '.css', '.js', '.svg'}:
        continue
    for name, pattern in patterns.items():
        check(not re.search(pattern, source, re.I), f'{name}: {path.relative_to(ROOT)}')


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.links, self.images = [], set(), [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('src', 'href'):
            if attrs.get(key):
                self.refs.append(attrs[key])
        if attrs.get('srcset'):
            self.refs.extend(v.strip().split()[0] for v in attrs['srcset'].split(','))
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'img':
            self.images.append(attrs)


page = Page()
page.feed((ROOT / 'index.html').read_text())
for ref in page.refs:
    if ref.startswith('#'):
        check(ref[1:] in page.ids, f'Destino interno existente: {ref}')
    elif re.match(r'https?://', ref):
        check(ref == WA, f'Único enlace externo permitido: {ref}')
    else:
        target = (ROOT / ref).resolve()
        check(target.is_relative_to(ROOT) and target.is_file(), f'Recurso local existente: {ref}')
check(any(link == WA for link in page.links), 'WhatsApp presente con número exacto')
check(all('alt' in image for image in page.images), 'Todas las imágenes tienen atributo alternativo')
check(all('width' in image and 'height' in image for image in page.images), 'Todas las imágenes declaran dimensiones')
check('prefers-reduced-motion' in (ROOT / 'styles.css').read_text()
      and 'prefers-reduced-motion' in (ROOT / 'app.js').read_text(), 'Movimiento reducido previsto en CSS y JS')
check(not re.search(r'@import\b|https?://', (ROOT / 'styles.css').read_text()), 'CSS sin recursos remotos')

css = (ROOT / 'styles.css').read_text()
tokens = dict(re.findall(r'(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})', css))


def luminance(hex_color):
    channels = [int(hex_color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055)**2.4 for c in channels]
    return sum(c*w for c, w in zip(linear, (0.2126, 0.7152, 0.0722)))


for pair in json.loads((ROOT / 'herramientas/contrastes.json').read_text()):
    foreground, background = tokens[pair['frente']], tokens[pair['fondo']]
    low, high = sorted((luminance(foreground), luminance(background)))
    ratio = (high + 0.05) / (low + 0.05)
    report['contrastes'].append({'nombre': pair['nombre'], 'texto': foreground,
                                'fondo': background, 'ratio': round(ratio, 2), 'minimo': pair['minimo']})
    check(ratio >= pair['minimo'], f"Contraste WCAG: {pair['nombre']} ({ratio:.2f}:1)")

# Solo los PNG de assets requieren transparencia; una captura debe ser opaca.
for path in sorted((ROOT / 'assets').rglob('*.png')):
    with Image.open(path) as image:
        has_alpha = 'A' in image.getbands() or 'transparency' in image.info
        alpha = image.convert('RGBA').getchannel('A')
        lo, hi = alpha.getextrema()
        report['png'].append({'archivo': str(path.relative_to(ROOT)), 'modo': image.mode,
                              'tamano': list(image.size), 'alfa': has_alpha, 'min': lo, 'max': hi})
        check(has_alpha and lo == 0 and hi == 255, f'PNG con transparencia útil: {path.name}')

for path in sorted((ROOT / 'assets/iconos').glob('*.svg')):
    icon = ET.parse(path).getroot()
    fills = {node.get('fill') for node in icon.iter() if node.get('fill')}
    check(fills == {tokens['--red'].upper()}, f'Símbolo con un solo relleno rojo: {path.name}')
    check(not any(node.get('stroke') or node.get('filter') for node in icon.iter()),
          f'Símbolo sin contornos ni efectos: {path.name}')

report['ok'] = not failures
report['errores'] = failures
report['alcance'] = 'Revisión estática. No sustituye la revisión de la página en navegador.'
(ROOT / 'herramientas/verificacion.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
for pair in report['contrastes']:
    print(f"{pair['nombre']}: {pair['ratio']:.2f}:1")
print(f"PNG revisados: {len(report['png'])}. Reglas revisadas: {len(report['comprobaciones'])}.")
if failures:
    print('\n'.join(f'ERROR: {failure}' for failure in failures))
    sys.exit(1)
print('OK. Verificación estática aprobada.')
