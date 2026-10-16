#!/usr/bin/env python3
"""Convierte las portadas a arte plano de UN solo color (rojo sobre negro).
Cada portada queda con 3 tintas planas: negro, rojo oscuro y rojo. Sin azul, sin degradados."""
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps
D = Path(__file__).resolve().parents[1] / 'assets' / 'portadas'
INK = [(8, 8, 8), (150, 22, 18), (255, 48, 40)]
for f in sorted(D.glob('*.webp')):
    im = Image.open(f).convert('L').filter(ImageFilter.MedianFilter(5))
    im = ImageOps.autocontrast(im, cutoff=2)
    lo, hi = 85, 170
    out = Image.new('RGB', im.size)
    px = im.load(); o = out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            v = px[x, y]
            o[x, y] = INK[0] if v < lo else INK[1] if v < hi else INK[2]
    out.save(f, 'WEBP', lossless=True, method=6)
    print(f.name, f.stat().st_size // 1024, 'KB')
