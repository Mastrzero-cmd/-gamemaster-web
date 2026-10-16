# v9b · «ARCADE-TÉCNICO»

**Idea en una frase:** la web es una **cabina arcade con HUD**. Cada sección es una «pantalla» de un nivel: marco de pantalla, marcador de puntos, vidas, cuadro de diálogo de juego y sprites rojos de píxel al frente sobre un fondo azul de trazo (ondas, constelaciones, topografía, radar, red neuronal).

## Qué la hace distinta
| Aspecto | v9b |
|---|---|
| Composición | Cabina: HUD fijo arriba (logo, `PUNTOS`, `NIVEL 1-n`, 3 corazones, Cotizar). Cada sección = encabezado de nivel + **pantalla** con marco doble + **cuadro de diálogo** pixel debajo. Sin riel lateral ni titulares gigantes condensados. |
| Tipografía | **Silkscreen** (display pixel), **Pixelify Sans** (texto), **VT323** (HUD/contadores). Autohospedadas en WOFF2, licencia SIL OFL. |
| Arte rojo | Sprites de píxel estilizados, con 1 celda de contorno negro que separa el rojo del azul. Una masa por pantalla (Pac‑Man, hongo, TV con play, robot, mando, Among Us, moneda…) más piezas sueltas. |
| Arte azul | Solo trazo/grabado, **sin cuadrículas**: crestas de señal apiladas (oscilograma con líneas ocultas), constelaciones, topografía de anillos, luna rayada con órbitas, arcos de transmisión + ondas, red neuronal + trazas de circuito, radar con engranes, abanico de rayos + lissajous. |
| Cortes de sección | 7 cortes distintos, uno por salto: onda senoidal, onda cuadrada, ecualizador, constelación, latido, circuito y «comecocos con fila de puntos» (rojo). |
| Marcas | «Tabla de puntuaciones»: 17 logos monocromos (Gpt, `E_logos`, sin tocar) en lista con puntos guía y categoría; sin tarjetas ni cuadrículas. |
| Filas Netflix | Cabecera de fila con contador `01/14` y botones ◀ ▶ pixel; scroll‑snap, flechas, arrastre con mouse, teclado (← →) y táctil. |
| Cierre | «¿Continuar?» con cuenta atrás 9→0 (quieta con reducir movimiento), moneda gigante y botón de WhatsApp. |
| Medidores | El sistema cromo se explica con **barras de energía** de 20 segmentos: rojo 15 %, negro 60 %, azul 25 %. |

## Íconos incluidos (siluetas de píxel, sin texto de marca)
Pac‑Man + fantasma + fila de puntos · Space Invaders · Tetris (T, L, S, I, O, J, Z) · hongo de Mario · estrella de Mario · bloque «?» · Zelda: corazones y Trifuerza (también espada en el kit de sprites) · Pokébola · silueta tipo Pikachu · anillo de Sonic · creeper de Minecraft · Among Us · Kirby · mando retro · TV con play (streaming) · robot (IA) · moneda de arcade.

## Reglas de cromoestereopsis
- Rojo al frente (sprites), negro de plano medio (pantalla, texto, contornos), azul atrás (trazo fino y marcos). Ningún SVG mezcla rojo y azul; el rojo lleva contorno negro.
- Sin blur, glow, sombras difusas, degradados, opacidades, morado ni copias desplazadas (`herramientas/auditar.py`: 0 hallazgos fuera del logo).
- Texto en hielo (#F4F4EF) o negro sobre rojo; nunca texto rojo ni rojo sobre azul.
- Parallax: azul 0.03 < rojo 0.10 < sprites 0.22, con tope en píxeles; `prefers-reduced-motion` lo apaga junto con parpadeos y cuenta atrás.
- El logo de Fernando aparece solo dentro de su placa (hero y sección Logo); en el HUD va la versión monocroma blanca.

## Archivos
`index.html` (generado por `herramientas/construir.py`), `styles.css`, `app.js`; `assets/` (`fonts`, `planos` azules, `heroes` rojos, `piezas` rojas, `logo`, `logos-mono`, `portadas`); `herramientas/` (`sprites.py`, `generar_arte.py`, `construir.py`, `auditar.py`, `medir_mezcla.py`, `solape.mjs`, `contraste.mjs`, `capturar.mjs`, `capturar_auditoria.mjs`); `capturas/` (1440 y 390).

## Cómo verlo
Abrir `identidad-v9b/index.html` o `python3 -m http.server` dentro de la carpeta. Capturas: `node herramientas/capturar.mjs capturas http://localhost:8779/index.html` (Playwright).
