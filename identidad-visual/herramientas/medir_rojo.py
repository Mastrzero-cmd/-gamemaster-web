import sys, numpy as np, glob, os
from PIL import Image
def pct(f):
    a = np.asarray(Image.open(f).convert('RGB')).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r > 150) & (r > 2.2 * g) & (r > 1.9 * b) & (g < 130) & (b < 120)
    return round(m.mean() * 100, 1)
if __name__ == '__main__':
    for f in sorted(glob.glob(sys.argv[1] + '/*.jpg')):
        n = os.path.basename(f)
        if any(k in n for k in ('hero.jpg', 'paleta.jpg', 'cromo.jpg', 'parallax.jpg', 'filas.jpg', 'ejemplo', 'pagina-completa', 'parallax-seccion')): print(n.ljust(36), pct(f))
