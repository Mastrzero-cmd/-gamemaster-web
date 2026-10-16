#!/usr/bin/env python3
"""Mide en capturas PNG (con logo/portadas/logos de terceros ocultos) el % de píxeles de mezcla rojo+azul:
púrpura/magenta = matiz 255°–345° con saturación y brillo apreciables. Debe ser ~0 (solo bordes antialias).
También reporta % negro / azul / rojo / hielo. Uso: python3 medir_mezcla.py <carpeta_png>"""
import sys, glob, os, numpy as np
from PIL import Image
def stats(f):
    a = np.asarray(Image.open(f).convert('RGB')).astype(np.float32) / 255; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1); d = mx - mn + 1e-9; s = d / (mx + 1e-9)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    col = (s > .35) & (mx > .25)
    mezcla = col & (h > 255) & (h < 345)
    rojo = col & ((h >= 345) | (h <= 22)) & (r > .6)
    azul = col & (h >= 215) & (h <= 255)
    negro = mx < .12; hielo = (s < .2) & (mx > .8)
    n = r.size; p = lambda m: 100 * m.sum() / n
    return p(mezcla), p(rojo), p(azul), p(negro), p(hielo)
rows = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.png'))):
    rows.append((os.path.basename(f),) + stats(f))
print('captura'.ljust(30), 'mezcla%  rojo%  azul%  negro%  hielo%')
for n, m, r, a, k, h in rows: print(n.ljust(30), f'{m:7.3f} {r:6.1f} {a:6.1f} {k:7.1f} {h:6.1f}')
M = np.array([x[1] for x in rows]); print(f'\nMEZCLA rojo/azul → máx {M.max():.3f}%  media {M.mean():.3f}%  (n={len(rows)})')
print('MEDIA  rojo %.1f%%  azul %.1f%%  negro %.1f%%' % tuple(np.mean([x[i] for x in rows]) for i in (2, 3, 4)))
