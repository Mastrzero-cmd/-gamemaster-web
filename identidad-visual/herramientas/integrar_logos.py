#!/usr/bin/env python3
"""Integra los logos monocromos de terceros (simple-icons, CC0 del paquete; marcas de sus dueños) a assets/logos/.
Recolorea al sistema (hielo #f4f4ef, negro #050505, rojo #ff2a1a), ajusta el viewBox a la tinta (centrado exacto)
y escribe medidas ópticas. Uso: python3 integrar_logos.py <carpeta_E_logos>"""
import sys, os, re, json, io
from PIL import Image
SRC = sys.argv[1]; DST = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logos')
os.makedirs(DST, exist_ok=True)
COL = {'hielo': ('#EAF6FF', '#f4f4ef'), 'negro': ('#000000', '#050505'), 'rojo': ('#FF1808', '#ff2a1a')}
marcas = sorted({f.split('_mono_')[0] for f in os.listdir(SRC) if f.endswith('.svg')} - {'max'})  # 'max' de simple-icons es el mensajero Max (otra marca), no el servicio de streaming (ese es hbomax)
med = {}
for m in marcas:
    png = Image.open(os.path.join(SRC, f'{m}_mono_hielo.png')).convert('RGBA')
    bb = png.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox()  # px en 512
    k = 24 / 512; x0, y0, x1, y1 = [round(v * k, 2) for v in bb]; w, h = round(x1 - x0, 2), round(y1 - y0, 2)
    for c, (a, b) in COL.items():
        s = open(os.path.join(SRC, f'{m}_mono_{c}.svg'), encoding='utf-8').read()
        s = s.replace(a, b).replace(a.lower(), b).replace('viewBox="0 0 24 24"', f'viewBox="{x0} {y0} {w} {h}"')
        s = s.replace('role="img"', 'role="img" aria-hidden="true"' if False else 'role="img"')
        open(os.path.join(DST, f'{m}-{c}.svg'), 'w', encoding='utf-8').write(s)
    # PNG hielo 256 px con alfa real (RGB al color del sistema)
    crop = png.crop(bb); sc = 256 / max(crop.size); crop = crop.resize((max(1, round(crop.width * sc)), max(1, round(crop.height * sc))), Image.LANCZOS)
    r = Image.new('RGBA', crop.size, (0xf4, 0xf4, 0xef, 0)); r.putalpha(crop.split()[3]); r.save(os.path.join(DST, f'{m}-hielo-256.png'), optimize=True)
    med[m] = (w, h)
# tamaño óptico: área de tinta constante (A px²), limitada en ancho y alto
A, WMAX, HMAX = 3000, 128, 52
out = {}
for m, (w, h) in med.items():
    a = w / h; ww = (A * a) ** .5; hh = ww / a
    if ww > WMAX: ww = WMAX; hh = ww / a
    if hh > HMAX: hh = HMAX; ww = hh * a
    out[m] = [round(ww), round(hh)]
json.dump(out, open(os.path.join(DST, 'medidas.json'), 'w'), indent=0)
print(json.dumps(out))
