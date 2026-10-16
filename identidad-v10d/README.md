# GAME MASTER · v10d «Póster en profundidad»

Mejora de v9d: parallax por 5 capas, rojo mucho más grande sobre ventanas azules con plano negro intermedio, tipografía unificada y personajes como **slots** (ver `SLOTS.md`). Detalle en `CONCEPTO.md`.

- Abrir `index.html` (estático, sin CDN ni build). Fuentes Shrikhand + Josefin Sans (OFL) locales.
- Regenerar: `python3 herramientas/rojo.py && python3 herramientas/construir.py && python3 herramientas/slots_md.py`.
- Verificar: `herramientas/auditar.py`, `herramientas/medir_mezcla.py <png>`, `herramientas/capturar.mjs`, `herramientas/verificar.mjs`, `herramientas/parallax.mjs <url> [ancho]`.

## Medido (1440 / 390 px)
| | 1440 | 390 |
|---|---|---|
| Rojo | 9.9 % | 7.3 % |
| Azul | 13.4 % | 13.6 % |
| Negro | 72.7 % | 72.6 % |
| Mezcla rojo+azul | ≤0.006 % | 0 % |
| Peso | 512 KB | 512 KB |

Parallax a +600 px (1440): azul 8.3 px (1.4 %), negro 30.2 px (5 %), rojo frente 125 px (21 %), piezas 205 px (34 %). A 390: 5.8 / 22.1 / 86.8 / 151.4 px. Con movimiento reducido todo queda quieto.
