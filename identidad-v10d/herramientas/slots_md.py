#!/usr/bin/env python3
"""Genera SLOTS.md a partir de slots.json (lo escribe rojo.py)."""
import json, os
d = json.load(open(os.path.join(os.path.dirname(__file__), 'slots.json')))
SEC = dict(inicio='Inicio (hero)', marcas='01 Marcas', juegos='02 Catálogo', streaming='03 Streaming', ia='04 IA', logo='05 Logo', contacto='07 Contacto')
CAPA = dict(fr='rojo grande · velocidad .30', pc='piezas · velocidad .55')
rows = []
for sec, v in d.items():
    for capa in ('fr', 'pc'):
        for s in v[capa]: rows.append((s['name'], SEC[sec], CAPA[capa], s['size'], s['rot'], s['forma']))
md = ['# SLOTS · espacios reservados para personajes (v10d)', '',
 'Los personajes (Pikachu, Kirby, Mario, Zelda, Sonic, Pac-Man, Among Us, creeper…) **no están dibujados**: cada uno es un `<span class="slot" data-slot="personaje-…" data-forma="…">` con una silueta genérica roja de borde negro y tamaño fijo, listo para sustituirse por una imagen generada.', '',
 '**Cómo sustituir:** dentro del `<span>` poner `<img src="assets/personajes/NOMBRE.png" alt="">` con `width:100%;height:100%;object-fit:contain` y quitar el fondo/borde del slot (`background:none;border:0;outline:0`). Imagen sugerida: PNG sin fondo, **rojo plano (#FF1A1A) con contorno negro (#050505)**, sin degradados, sin glow, sin azul; el contorno negro grueso es el que separa el rojo del azul. Se coloca en la capa roja correspondiente (el slot hereda su parallax).', '',
 'Tamaño: se da en **unidades del lienzo de diseño 1440×900** (el mismo de los SVG); a 1440 px de ancho de pantalla 1 unidad ≈ 0.67 px (el slot escala con la ventana, siempre cuadrado). Para PNG usar al menos el doble del tamaño en unidades.', '',
 '| Slot (`data-slot`) | Sección | Capa | Tamaño (u) | PNG sugerido | Rotación | Forma genérica |', '|---|---|---|---|---|---|---|']
for n, sec, capa, sz, rot, f in rows:
    md.append(f'| `{n}` | {sec} | {capa} | {sz}×{sz} | {sz*2}×{sz*2} | {rot}° | {f} |')
md += ['', f'Total: **{len(rows)} slots** en las secciones, más 6 chapas de ejemplo fijas (86×86 px, `data-slot="personaje-ejemplo-…"`) en la sección Sistema que muestran cada forma genérica (blob, cuadro, triángulo, anillo, estrella, fantasma).', '',
 'Los íconos de objeto que sí se conservan (dibujados en SVG): corazón, espada, bola de captura, mando, tele retro, play, robot y destello IA.']
open(os.path.join(os.path.dirname(__file__), '..', 'SLOTS.md'), 'w').write('\n'.join(md) + '\n')
print(len(rows))
