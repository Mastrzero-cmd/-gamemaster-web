# v9a «Grabado» · identidad visual de GameMaster

**Idea en una frase:** un billete antiguo del mundo de los videojuegos. El fondo azul es un grabado fino de líneas (roseta guilloché, curvas de nivel, olas, rayos, engranes, constelaciones) y el rojo son grandes sellos con trazo grueso: Trifuerza, hongo, Pokébola, comecocos y más.

## Qué lo hace distinto (de v1–v8, de «Cartel» y de las otras propuestas v9)
| Aspecto | v9a «Grabado» |
|---|---|
| Composición | Titular en **banda horizontal** centrada entre dobles filetes azules (como el encabezado de un billete) y, debajo, un **medallón** central: anillo rojo de rayitas, texto grabado en hielo alrededor y un sello rojo grande en el hueco negro. Cada sección repite la fórmula pero con otro sello y otro grabado. |
| Tipografía | **Bodoni Moda** (serif de alto contraste, mayúsculas + itálica), **IBM Plex Sans Condensed** (texto, grotesca estrecha) e **IBM Plex Mono** (etiquetas, numeración romana). Todas OFL, autohospedadas en WOFF2. |
| Arte azul | Solo **líneas finas de grabado** generadas por script (epitrocoides guilloché, curvas de nivel, olas, cuñas de rayos, engranes, constelaciones). Sin cuadrículas ni rejillas. Cada sección usa un idioma de grabado distinto. |
| Arte rojo | Íconos-sello de masa roja con borde negro grueso y detalles negros (ver lista). Un sello principal por sección + 4 piezas pequeñas alrededor. |
| Cortes de sección | **Cinco cintas de grabado de un solo color**, ninguna repetida: ondas entrelazadas, abanico de escamas, cuerda trenzada, estrías que crecen y se afinan, constelación. |
| Filas tipo Netflix | Tarjetas tipo billete (doble filete azul), título entre filetes, flechas redondas, contador romano-numérico «01 / 14», scroll-snap, arrastre, teclado. |
| Marcas | 17 logos monocromos (Gpt, `E_logos`, sin modificar) dentro de **roeles** (círculos con doble filete). |
| Navegación | Barra con el logo al centro y el menú repartido a ambos lados. |

## Íconos incluidos (todos en rojo, sin personajes con texto de marca)
Zelda: Trifuerza, espada, corazón, rupia, ocarina. Mario: hongo, bloque «?», estrella, tubería. Pokémon: Pokébola, cabeza tipo Pikachu. Otros: comecocos y fantasma, invasor espacial, piezas tipo Tetris, rostro cúbico (creeper), anillo (Sonic), bola rosa (Kirby), tripulante (Among Us). Tecnología (streaming e IA): pantalla con play, red neuronal, chip, onda de audio.

## Reglas de cromoestereopsis que cumple
- Rojo al frente, negro en medio (el hueco del medallón y el aire), azul atrás (solo líneas).
- Una imagen, una geometría: ningún SVG tiene rojo y azul a la vez (planos = solo azul; héroes, piezas y sellos = solo rojo y negro).
- Sin blur, glow, sombras, degradados, opacidades, morado ni copias desplazadas (`herramientas/auditar.py`: 0 hallazgos fuera del logo).
- Texto en hielo; nunca rojo sobre azul.
- Parallax: azul 0.03 (más lento), rojo 0.10, piezas 0.22, con tope en píxeles; `prefers-reduced-motion` lo deja todo quieto.
- La página se lee negra (ronda 2, medido en capturas: ≈ 79 % negro, 10 % rojo, 5–8 % azul).
- Logo de Fernando solo dentro de su placa (hero, sección Logo); en la barra se usa la versión monocroma blanca.

## Archivos
`index.html` (lo genera `herramientas/construir.py`), `styles.css`, `app.js`; `assets/` (`fonts`, `planos` azules, `heroes` y `piezas` rojos, `sellos` íconos sueltos, `cortes`, `logo`, `logos-mono`, `portadas`); `herramientas/` (`iconos.py`, `arte.py`, `construir.py`, `auditar.py`, `medir_mezcla.py`, `capturar.mjs`, `capturar_auditoria.mjs`, `solape.mjs`, `contraste.mjs`); `capturas/`.

## Cómo verlo
Abrir `identidad-v9a/index.html` con un servidor estático (por ejemplo `python3 -m http.server` en la carpeta). Regenerar arte: `python3 herramientas/arte.py && python3 herramientas/construir.py`.

## Ronda 2
- Rojo ≈ 10 %: sellos y piezas más grandes, bisel rojo más grueso, cinta roja de serie (texto negro) bajo cada titular y filete rojo sobre cada fila.
- Íconos rediseñados: ocarina (boquilla + 6 agujeros + Trifuerza), anillo (aro en perspectiva con brillo y destellos), cabeza tipo Pikachu (orejas largas con punta negra, mejillas, cola de rayo).
- Portadas de juegos en una sola tinta (grises); logo SVG ligero de v8 (≈ 43 KB); separación negra entre los picos azules y el anillo rojo del medallón; sin box-shadow (se usa outline nítido).
