#!/usr/bin/env python3
"""v5 · inserta (idempotente) las piezas rojas nuevas en index.html entre marcas <!--v5:id--> ... <!--/v5-->.
Cada pieza: (archivo|texto, izq%, arriba%, ancho_vw, velocidad_parallax, giro_deg, capa 'f' frente|'a' atrás-de-texto, móvil 0/1)
Velocidades (4 capas): .05 lejos · .12 · .22 · .36 cerca. Uso: python3 colocar_v5.py ../index.html"""
import re, sys, json
def img(n, l, t, w, sp, r, z='a', m=1, d=0, esc=1.4):
    if sp != 0: w = round(w * esc, 1)  # v5: piezas ~40 % más grandes (los mosaicos con velocidad 0 no escalan)
    cls = 'pz v5' + (' bk' if z == 'a' else '') + ('' if m else ' dm')
    mw = int(min(max(w * 5.2, 44), 72))
    return (f'<div class="{cls}" data-speed="{sp}" style="--l:{l}%;--t:{t}%;--w:{w}vw;--wx:{int(w*14.4)}px;--mw:{mw}px;--r:{r}deg;--d:{d}s"><img src="assets/piezas/pieza-{n}.svg" alt="" draggable="false" loading="lazy"></div>')
def rt(txt, l, t, sp, r, m=1, k=''):
    cls = 'pz v5 rt' + (' dm' if not m else '') + (' ' + k if k else '')
    return f'<div class="{cls}" data-speed="{sp}" style="--l:{l}%;--t:{t}%;--r:{r}deg"><span>{txt}</span></div>'
TOPL = [64, 79, 90, 50]; BOTL = [3, 22, 41, 60, 78, 90]
def mobile(items, sid):
    """asigna posición móvil: bandas de arriba (≤46px) y de abajo (pegadas al borde), sin tapar texto"""
    out = []; ti = bi = 0
    for k, h in enumerate(items):
        if ' dm' in h.split('data-speed')[0]: out.append(h); continue
        top = (k % 2 == 0) and sid != 'inicio'
        if top: pos = f'--ml:{TOPL[ti % len(TOPL)]}%;--mt:6px;'; ti += 1
        else: pos = f'--ml:{BOTL[bi % len(BOTL)]}%;--mb:6px;'; bi += 1
        out.append(h.replace('style="', 'style="' + pos, 1))
    return out
S = {
 'inicio': [  # (el héroe ya trae mando, portátil, audífonos, play y 2 destellos de v4)
  img('sello', 86, 4, 7, .22, 8, 'f', 1), img('joystick', 41, 7, 5.6, .12, -8, 'f', 0), img('cursor', 54, 77, 4.6, .36, -10, 'f', 0, 1),
  img('bocina', 92, 56, 4.4, .12, 6, 'f', 0, 2), img('estrella', 53, 55, 3.2, .36, 0, 'f', 1), img('estrella', 93, 20, 2.8, .22, 0, 'f', 0), img('estrella', 3, 90, 3, .36, 0, 'f', 1),
  img('teclado', 56, 90, 9, .05, -4, 'f', 0), img('boton', 1, 4, 5, .22, 0, 'f', 0), rt('PS5 · Switch · PC', 30, 90, .22, -4, 0, 'on'), img('flecha', 40, 80, 6.4, .12, 180, 'f', 0)],
 'paleta': [
  img('consola', 68, 4, 15, .12, -5, 'f', 1), img('teclado', 84, 23, 9, .22, 7, 'f', 0), img('raton', 76, 24, 3.6, .36, -12, 'f', 0), img('estrella', 61, 6, 3.4, .36, 0, 'f', 1),
  img('estrella', 94, 8, 3, .22, 0, 'f', 0), img('sello', 0, 52, 6.6, .12, -8, 'a', 0), img('gpu', 62, 90, 13, .05, 3, 'a', 1), img('cinta', 2, 92, 13, .22, -4, 'f', 0), img('disco', 90, 54, 5.5, .36, 0, 'a', 0),
  rt('Cotiza por WhatsApp', 38, 4, .22, 3, 0)],
 'cromo': [
  img('servidor', 76, 4, 10, .12, 6, 'f', 0), img('cursor', 60, 8, 4.2, .36, 12, 'f', 1), img('sello', 89, 41, 6.4, .22, 10, 'a', 0), img('control', 1, 56, 4.2, .12, -8, 'a', 1),
  img('flecha', 62, 37, 6.6, .22, 0, 'a', 0), img('estrella', 53, 14, 3, .36, 0, 'f', 1), img('estrella', 3, 90, 3.2, .22, 0, 'f', 1), rt('Rojo al frente', 74, 30, .22, -3, 0)],
 'parallax': [
  img('microfono', 29, 80, 6, .22, -6, 'f', 1), img('gpu', 47, 93, 11, .12, 4, 'f', 1), img('sello', 51, 30, 7.2, .36, 8, 'f', 1), img('disco', 76, 46, 6.5, .22, 0, 'f', 0), img('teclado', 50, 60, 8, .05, -6, 'f', 0),
  img('estrella', 52, 16, 3.4, .36, 0, 'f', 1), img('estrella', 30, 62, 3.2, .22, 0, 'f', 0), img('estrella', 94, 30, 3.4, .12, 0, 'f', 1), img('cursor', 46, 38, 4.6, .36, -10, 'f', 0),
  img('boton', 4, 40, 5.4, .12, 0, 'f', 0), rt('Fondo fijo', 66, 26, .36, 4, 1)],
 'filas': [
  img('consola', 68, 3, 11, .12, -6, 'f', 1), img('control', 90, 12, 3.8, .22, 8, 'f', 1), img('flecha', 56, 7, 7, .36, 0, 'f', 0), img('estrella', 62, 24, 3.2, .36, 0, 'f', 1),
  img('estrella', 3, 94, 3, .22, 0, 'f', 0), img('cartucho', 2, 88, 4.4, .12, -10, 'a', 1), img('boton', 91, 91, 4.8, .22, 0, 'a', 0), rt('Desliza →', 78, 5, .22, 3, 1)],
 'ej-catalogo': [
  img('joystick', 58, 3, 5.6, .22, 8, 'f', 1), img('cartucho', 90, 40, 5.4, .12, 10, 'a', 0), img('sello', 1, 84, 6, .36, -8, 'a', 0), img('estrella', 52, 9, 3.2, .36, 0, 'f', 1),
  img('estrella', 94, 90, 3, .22, 0, 'f', 0), img('mando', 40, 88, 9, .05, -8, 'a', 0), rt('Populares', 66, 7, .12, -3, 1), img('flecha', 92, 8, 5.6, .36, 0, 'f', 0)],
 'ej-streaming': [
  img('play', 62, 3, 5, .36, 0, 'f', 1), img('control', 54, 4, 3.4, .12, -8, 'f', 0), img('microfono', 91, 54, 4.2, .22, 8, 'a', 0), img('pantalla', 0, 84, 8, .12, -6, 'a', 0), img('estrella', 77, 10, 3.2, .22, 0, 'f', 1),
  img('estrella', 45, 8, 2.8, .36, 0, 'f', 0), img('bocina', 94, 4, 4, .05, 6, 'f', 0), rt('Series y cine', 60, 90, .22, 4, 1), img('cinta', 40, 90, 12, .12, -3, 'a', 0), img('disco', 36, 3, 5, .22, 0, 'f', 0)],
 'ej-ia': [
  img('servidor', 40, 3, 9, .12, -4, 'f', 0), img('gpu', 55, 91, 12, .12, 3, 'f', 1), img('cursor', 30, 90, 4.6, .36, -10, 'f', 1), img('sello', 1, 84, 6, .22, 8, 'a', 0), img('raton', 94, 28, 3, .22, 8, 'a', 0),
  img('estrella', 52, 14, 2.6, .36, 0, 'f', 1), img('estrella', 3, 6, 2.6, .22, 0, 'f', 0), rt('IA y tecnología', 22, 91, .22, -3, 1), img('teclado', 2, 55, 8, .05, 6, 'a', 0)],
}
# piezas que asoman por los bordes, detrás de tarjetas y placas (profundidad), solo escritorio
S['paleta'] += [img('control', -1.5, 40, 5, .12, -8, 'a', 0), img('portatil', 92, 47, 8.5, .22, 8, 'a', 0)]
S['filas'] += [img('portatil', 95, 52, 8, .22, 8, 'a', 0), img('mando', -3.5, 48, 8, .12, 10, 'a', 0), img('microfono', 47, 91, 3.8, .36, 6, 'f', 0)]
S['ej-catalogo'] += [img('audifonos', 95, 58, 7, .22, 6, 'a', 0), img('boton', -1, 52, 5, .36, 0, 'a', 0), img('play', 46, 90, 4.6, .12, 0, 'f', 0)]
S['ej-streaming'] += [img('consola', 94, 60, 9, .12, -6, 'a', 0), img('estrella', 97, 40, 2.8, .22, 0, 'f', 0), img('claqueta', -2, 50, 8, .22, -6, 'a', 0)]
S['ej-ia'] += [img('claqueta', 94, 56, 8, .12, 6, 'a', 0), img('boton', -1, 46, 5, .22, 0, 'a', 0), img('pantalla', 46, 88, 8, .36, 4, 'a', 0)]
S['cromo'] += [img('boton', 94, 8, 5, .36, 0, 'f', 0), img('microfono', 47, 90, 4, .22, -6, 'f', 0)]
# mosaicos del grabado: una pieza roja en cada mosaico (sobre azul)
T = ['consola', 'servidor', 'cartucho', 'sello', 'gpu', 'claqueta', 'teclado', 'portatil']

# ---- móvil: tiras en el flujo (no tapan nada) con piezas rojas pequeñas, sin parallax ----
STRIPS = ['consola mando gpu', 'cursor sello estrella boton control', 'servidor microfono flecha disco teclado', 'cartucho play raton bocina estrella', 'portatil estrella cinta cursor boton']
def strip(i):
    names = STRIPS[i % len(STRIPS)].split(); o = ''
    for k, n in enumerate(names):
        w = [64, 54, 70, 50, 60][(k + i) % 5]; r = [-8, 6, -4, 10, 0][(k + 2 * i) % 5]
        o += f'<img class="sp" src="assets/piezas/pieza-{n}.svg" alt="" draggable="false" loading="lazy" style="width:{w}px;--r:{r}deg;--d:{(k*.7)%3:.1f}s">'
    return f'<!--v5s--><div class="rstrip" aria-hidden="true">{o}</div><!--/v5s-->'
def strips(h):
    h = re.sub(r'<!--v5s-->.*?<!--/v5s-->', '', h, flags=re.S); n = [0]
    def add(pat, count=None):
        nonlocal h
        def rep(m): n[0] += 1; return strip(n[0]) + m.group(0)
        h = re.sub(pat, rep, h)
    add(r'<div class="grid g4">(?=\s*<div class="sw")')
    add(r'<div class="grid g3" style="margin-top:26px">')
    add(r'<div class="grid g2" style="align-items:center">')
    add(r'<div data-row="(?:plataformas|juegos|streaming|ia)"')
    return h
def main(path):
    h = open(path).read(); h = re.sub(r'<!--v5:[^>]*-->.*?<!--/v5-->', '', h, flags=re.S)
    for sid, items in S.items():
        m = re.search(r'<section[^>]*id="%s"[^>]*>' % sid, h); assert m, sid
        h = h[:m.end()] + f'\n<!--v5:{sid}-->' + ''.join(mobile(items, sid)) + '<!--/v5-->' + h[m.end():]
    k = [0]
    def tile(m):
        n = T[k[0] % len(T)]; k[0] += 1
        return m.group(0) + f'<!--v5:t-->{img(n, 68 if k[0]%2 else 4, 14, 11, 0, 6 if k[0]%2 else -6, "f", 1)}<!--/v5-->'
    h = re.sub(r'<figure class="tile[^>]*>', tile, h)
    h = strips(h)
    open(path, 'w').write(h); print('colocadas', sum(len(v) for v in S.values()), '+', k[0], 'mosaicos')
main(sys.argv[1])
