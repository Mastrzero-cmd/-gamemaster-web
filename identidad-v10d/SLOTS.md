# SLOTS · espacios reservados para personajes (v10d)

Los personajes (Pikachu, Kirby, Mario, Zelda, Sonic, Pac-Man, Among Us, creeper…) **no están dibujados**: cada uno es un `<span class="slot" data-slot="personaje-…" data-forma="…">` con una silueta genérica roja de borde negro y tamaño fijo, listo para sustituirse por una imagen generada.

**Cómo sustituir:** dentro del `<span>` poner `<img src="assets/personajes/NOMBRE.png" alt="">` con `width:100%;height:100%;object-fit:contain` y quitar el fondo/borde del slot (`background:none;border:0;outline:0`). Imagen sugerida: PNG sin fondo, **rojo plano (#FF1A1A) con contorno negro (#050505)**, sin degradados, sin glow, sin azul; el contorno negro grueso es el que separa el rojo del azul. Se coloca en la capa roja correspondiente (el slot hereda su parallax).

Tamaño: se da en **unidades del lienzo de diseño 1440×900** (el mismo de los SVG); a 1440 px de ancho de pantalla 1 unidad ≈ 0.67 px (el slot escala con la ventana, siempre cuadrado). Para PNG usar al menos el doble del tamaño en unidades.

| Slot (`data-slot`) | Sección | Capa | Tamaño (u) | PNG sugerido | Rotación | Forma genérica |
|---|---|---|---|---|---|---|
| `personaje-mario-hongo` | Inicio (hero) | rojo grande · velocidad .30 | 840×840 | 1680×1680 | 8° | blob |
| `personaje-mario-estrella` | Inicio (hero) | piezas · velocidad .55 | 255×255 | 510×510 | 15° | estrella |
| `personaje-sonic-anillo-mini` | Inicio (hero) | piezas · velocidad .55 | 315×315 | 630×630 | -10° | anillo |
| `personaje-zelda-trifuerza` | 02 Catálogo | rojo grande · velocidad .30 | 930×930 | 1860×1860 | -4° | triangulo |
| `personaje-pikachu` | 02 Catálogo | rojo grande · velocidad .30 | 645×645 | 1290×1290 | 6° | blob |
| `personaje-mario-hongo-mini` | 02 Catálogo | piezas · velocidad .55 | 255×255 | 510×510 | -10° | blob |
| `personaje-sonic-anillo` | 01 Marcas | rojo grande · velocidad .30 | 600×600 | 1200×1200 | -14° | anillo |
| `personaje-kirby` | 01 Marcas | piezas · velocidad .55 | 300×300 | 600×600 | 8° | blob |
| `personaje-mario-estrella-b` | 01 Marcas | piezas · velocidad .55 | 165×165 | 330×330 | -10° | estrella |
| `personaje-pacman` | 03 Streaming | piezas · velocidad .55 | 345×345 | 690×690 | -8° | blob |
| `personaje-fantasma` | 03 Streaming | piezas · velocidad .55 | 240×240 | 480×480 | 6° | fantasma |
| `personaje-amongus` | 03 Streaming | piezas · velocidad .55 | 225×225 | 450×450 | -6° | fantasma |
| `personaje-invasor` | 04 IA | piezas · velocidad .55 | 225×225 | 450×450 | 0° | cuadro |
| `personaje-mario-bloque` | 04 IA | piezas · velocidad .55 | 225×225 | 450×450 | 12° | cuadro |
| `personaje-creeper` | 05 Logo | rojo grande · velocidad .30 | 540×540 | 1080×1080 | 8° | cuadro |
| `personaje-mario-estrella-c` | 05 Logo | piezas · velocidad .55 | 255×255 | 510×510 | -10° | estrella |
| `personaje-pikachu-contacto` | 07 Contacto | rojo grande · velocidad .30 | 300×300 | 600×600 | 0° | blob |
| `personaje-pacman-contacto` | 07 Contacto | piezas · velocidad .55 | 300×300 | 600×600 | -8° | blob |
| `personaje-mario-estrella-d` | 07 Contacto | piezas · velocidad .55 | 210×210 | 420×420 | 12° | estrella |

Total: **19 slots** en las secciones, más 6 chapas de ejemplo fijas (86×86 px, `data-slot="personaje-ejemplo-…"`) en la sección Sistema que muestran cada forma genérica (blob, cuadro, triángulo, anillo, estrella, fantasma).

Los íconos de objeto que sí se conservan (dibujados en SVG): corazón, espada, bola de captura, mando, tele retro, play, robot y destello IA.
