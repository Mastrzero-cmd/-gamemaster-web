#!/usr/bin/env python3
"""Auditoría automática de cromoestereopsis (docs/CHROMOSTEREOPSIS.md). Revisa index.html, styles.css, app.js y los SVG de
assets/{heroes,piezas,placas,planos}. Reglas (todas deben dar 0; el logo en assets/logo y los logos de terceros están exentos y se listan aparte):
  R1 filter/blur/drop-shadow/backdrop-filter/feGaussianBlur   R2 box-shadow con blur>0 y cualquier text-shadow
  R3 gradientes (linear/radial/conic, SVG gradient/mask)       R4 opacidad <1 (opacity, rgba/hsla, fill/stroke-opacity)
  R5 magenta/púrpura (matiz 255°-345°) y colores fuera del sistema (cian, verde...) fuera del logo
  R6 rojo y azul mezclados en un mismo objeto (SVG con ambos matices; regla CSS/atributo style con ambos)
  R7 texto en rojo (color: rojo)                               R8 la palabra prohibida (cualquier archivo de texto)
Uso: python3 auditar.py [carpeta_identidad_visual]   → código de salida 1 si hay hallazgos fuera del logo"""
import sys, os, re, glob, colorsys
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
NAMED = {'red': '#ff0000', 'blue': '#0000ff', 'magenta': '#ff00ff', 'fuchsia': '#ff00ff', 'purple': '#800080', 'violet': '#ee82ee', 'cyan': '#00ffff', 'aqua': '#00ffff', 'green': '#008000', 'yellow': '#ffff00', 'orange': '#ffa500', 'pink': '#ffc0cb', 'indigo': '#4b0082', 'black': '#000000', 'white': '#ffffff'}
PROHIBIDA = 'com' + 'part'  # raíz prohibida, construida a trozos para no escribirla completa
def rd(p): return open(p, encoding='utf-8', errors='ignore').read()
def hexrgb(h):
    h = h.lstrip('#')
    if len(h) in (3, 4): h = ''.join(c * 2 for c in h[:3])
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def cls(rgb):
    h, l, s = colorsys.rgb_to_hls(*rgb); h *= 360
    if s < .2 or l < .04 or l > .93: return 'neutro'
    if h >= 345 or h <= 22: return 'rojo'
    if 215 <= h <= 255: return 'azul'
    if 255 < h < 345: return 'magenta/púrpura'
    return 'otro(' + str(int(h)) + '°)'
# variables CSS
css = rd(os.path.join(ROOT, 'styles.css')); VARS = {}
for m in re.finditer(r'(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})', css): VARS[m.group(1)] = m.group(2)
def colors(text):
    out = []
    for m in re.finditer(r'#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b', text): out.append(('#' + m.group(0).lstrip('#')[:6] if len(m.group(0)) == 9 else m.group(0), m.group(0)))
    for m in re.finditer(r'var\((--[\w-]+)\)', text):
        if m.group(1) in VARS: out.append((VARS[m.group(1)], m.group(0)))
    for m in re.finditer(r'rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)', text): out.append(('#%02x%02x%02x' % tuple(int(x) for x in m.groups()), m.group(0)))
    for m in re.finditer(r'(?:[:=]\s*["\']?)(' + '|'.join(NAMED) + r')(?![\w-])', text):
        if m.group(1) not in ('black', 'white'): out.append((NAMED[m.group(1)], m.group(0)))
    return [(hexrgb(h), raw) for h, raw in out]
F = []  # (regla, archivo, detalle)
def add(r, f, d): F.append((r, os.path.relpath(f, ROOT), d))
EXENTOS = ('assets/logo/', 'assets/servicios/', 'assets/logos/', 'assets/portadas/', 'assets/fonts/')
files = [os.path.join(ROOT, n) for n in ('index.html', 'styles.css', 'app.js')]
files += sorted(glob.glob(os.path.join(ROOT, 'assets/heroes/*.svg')) + glob.glob(os.path.join(ROOT, 'assets/piezas/*.svg')) + glob.glob(os.path.join(ROOT, 'assets/placas/*.svg')) + glob.glob(os.path.join(ROOT, 'assets/planos/*.svg')))
for p in files:
    t = rd(p); isvg = p.endswith('.svg')
    if p.endswith('.css'): t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    # R1
    for m in re.finditer(r'(backdrop-filter|filter)\s*:\s*[^;}]+|<filter\b|feGaussianBlur|filter="[^"]+"|blur\(', t): add('R1 blur/filter', p, m.group(0)[:60])
    # R2
    for m in re.finditer(r'text-shadow\s*:[^;}]+', t): add('R2 text-shadow', p, m.group(0)[:60])
    for m in re.finditer(r'box-shadow\s*:\s*([^;}]+)', t):
        for part in re.split(r',(?![^(]*\))', m.group(1)):
            if 'inset' in part and False: continue
            nums = re.findall(r'(?<![\w#.-])-?\d+(?:\.\d+)?(?:px)?(?![\w%])', re.sub(r'(rgba?|hsla?)\([^)]*\)|var\([^)]*\)|#[0-9a-fA-F]+', '', part))
            if len(nums) >= 3 and float(nums[2].replace('px', '')) > 0: add('R2 box-shadow con blur', p, part.strip()[:60])
    # R3
    for m in re.finditer(r'(linear|radial|conic|repeating-linear|repeating-radial)-gradient\(|<(linear|radial)Gradient|<mask\b|mask-image|<pattern\b[^>]*opacity', t): add('R3 gradiente/máscara', p, m.group(0)[:50])
    # R4
    for m in re.finditer(r'(?<![\w-])(opacity|fill-opacity|stroke-opacity)\s*[:=]\s*["\']?([0-9.]+)', t):
        if float(m.group(2)) < 1: add('R4 opacidad<1', p, m.group(0))
    for m in re.finditer(r'(rgba|hsla)\(([^)]*)\)', t):
        a = re.split(r'[ ,/]+', m.group(2).strip())[-1]
        try:
            if float(a) < 1: add('R4 alfa<1', p, m.group(0)[:50])
        except ValueError: pass
    for m in re.finditer(r'#[0-9a-fA-F]{8}\b', t): add('R4 alfa<1 (hex8)', p, m.group(0))
    # R5 (CSS/HTML/JS/SVG): colores fuera del sistema
    for rgb, raw in colors(t):
        c = cls(rgb)
        if c not in ('neutro', 'rojo', 'azul'): add('R5 color fuera del sistema (' + c + ')', p, raw)
    # R6: SVG con rojo y azul
    if isvg:
        cs = {cls(rgb) for rgb, _ in colors(t)}
        if 'rojo' in cs and 'azul' in cs: add('R6 rojo+azul en el mismo SVG', p, 'tiene ambos matices')
    else:
        for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', t if p.endswith('.css') else ''):
            if ':root' in m.group(1): continue
            cs = {cls(rgb) for rgb, _ in colors(m.group(2))}
            if 'rojo' in cs and 'azul' in cs: add('R6 rojo+azul en una regla CSS', p, m.group(1).strip()[:60])
        for m in re.finditer(r'style="([^"]*)"', t):
            cs = {cls(rgb) for rgb, _ in colors(m.group(1))}
            if 'rojo' in cs and 'azul' in cs: add('R6 rojo+azul en un style=""', p, m.group(1)[:60])
    # R7: texto rojo
    if p.endswith('.css'):
        for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', t):
            for d in re.finditer(r'(?<![\w-])color\s*:\s*([^;}]+)', m.group(2)):
                if 'rojo' in {cls(rgb) for rgb, _ in colors(d.group(1))}: add('R7 texto rojo', p, m.group(1).strip()[:60])
    # R8
    if re.search(PROHIBIDA, t, re.I): add('R8 palabra prohibida', p, 'aparece')
# R8 en el resto de archivos de texto (README, herramientas excepto este script)
for p in glob.glob(os.path.join(ROOT, '**/*'), recursive=True):
    if os.path.isfile(p) and p.endswith(('.md', '.mjs', '.py', '.txt', '.html')) and os.path.abspath(p) != os.path.abspath(__file__) and p not in files:
        if re.search(PROHIBIDA, rd(p), re.I): add('R8 palabra prohibida', p, 'aparece')
# logo (exento): solo informativo
logo = {}
for p in sorted(glob.glob(os.path.join(ROOT, 'assets/logo/*.svg'))):
    t = rd(p); logo[os.path.basename(p)] = sorted({cls(rgb) for rgb, _ in colors(t)} - {'neutro'})
print('AUDITORÍA v7 · archivos revisados:', len(files), '(index.html, styles.css, app.js + SVG de heroes/piezas/placas/planos)')
by = {}
for r, f, d in F: by.setdefault(r, []).append((f, d))
for r in ['R1 blur/filter', 'R2 text-shadow', 'R2 box-shadow con blur', 'R3 gradiente/máscara', 'R4 opacidad<1', 'R4 alfa<1', 'R4 alfa<1 (hex8)', 'R6 rojo+azul en el mismo SVG', 'R6 rojo+azul en una regla CSS', 'R6 rojo+azul en un style=""', 'R7 texto rojo', 'R8 palabra prohibida']:
    print(f'  {r:34s} {len(by.get(r, []))}')
for r in sorted(k for k in by if k.startswith('R5')): print(f'  {r:34s} {len(by[r])}')
if not any(k.startswith('R5') for k in by): print(f'  {"R5 magenta/púrpura/otros":34s} 0')
for r, v in by.items():
    for f, d in v[:12]: print('   !', r, '|', f, '|', d)
print('Exentos (logo propio, solo informativo): ' + ', '.join(f'{k}:{"/".join(v) or "neutro"}' for k, v in list(logo.items())[:4]) + ' …')
print('TOTAL HALLAZGOS FUERA DEL LOGO:', len(F)); sys.exit(1 if F else 0)
