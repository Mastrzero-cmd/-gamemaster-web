# GameMaster · Identidad visual v6 (propuesta)

Página estática aislada (HTML + CSS + JS vanilla, sin build, sin CDN). No toca la web, `main` ni el PR.

**Abrir:** `identidad-visual/index.html` (doble clic) o `python3 -m http.server`. Para probar movimiento reducido: `index.html?reduce`.

## Dirección
Parte de los dos logos de negocio (letras itálicas de pincel, cian/azul eléctrico, contorno magenta desplazado, glitch horizontal, scanlines, pincelada curva) y de las referencias del repo (campo azul eléctrico, grabado negro de líneas finas y trama, rejilla de horizonte, circuitos, placas isométricas, listón rojo al frente).
- **Rojo adelante del azul:** piezas rojas (mando, portátil, audífonos, pantalla, chip, cartucho, listón) sobre campos azules. El negro solo separa (líneas, placas, cortes). Nunca texto rojo sobre azul.
- Áreas grandes en azul suave; efectos marcados solo en logo y piezas; sin parpadeos; `prefers-reduced-motion` respetado.
- Parallax: fondo fijo (capa fija recortada, funciona en iOS) y piezas que se mueven a distinta velocidad.
- 5 cortes distintos: pincelada, escaneo, glitch estático, pixel (el único), cinta de película.
- Filas tipo Netflix: scroll-snap, flechas arriba de la fila (no tapan tarjetas), arrastre con mouse, táctil nativo, teclas ← →.

## Logo (`assets/logo/`)
SVG vectorial (texto convertido a trazos, fuente Bangers OFL) y PNG con fondo transparente (256/512/1024/2048 px).
Variantes: `completo`, `horizontal`, `compacto` (icono GM) × `oscuro`, `claro`, `mono-blanco`, `mono-noche`.
Regenerar: `python3 herramientas/generar_logo.py assets/logo` y `node herramientas/exportar_png.mjs assets/logo` (Playwright).

## Otros
`herramientas/generar_piezas.py` y `generar_arte.py` generan las piezas rojas y los fondos SVG. Fuentes libres autohospedadas: Bangers, Outfit, Space Mono. Portadas, logos de servicios y plataformas copiados del repo. Precios siempre «Consultar precio»; cotización por WhatsApp. Las marcas de terceros pertenecen a sus dueños.

## v3 · grabado fino en los campos azules
- `assets/arte/campo-<sección>-fondo.svg` y `-objetos.svg`: dos capas por sección (hero, paleta, cromo, parallax, filas, catálogo, streaming, IA), todo vectorial (~1 MB en total), con trazo fino de tono azul cercano al fondo (curvas de nivel, placas isométricas con relieve, circuitos y huellas de chip, retículas, guilloche, estrellas, cintas, red neuronal) y objetos gamer/streaming/tech en línea (mando, portátil, cartucho, pantalla, chip, audífonos, claqueta, play, nube, servidor, consola, disco). Las capas se mueven a distinta velocidad (profundidad) y respetan «reducir movimiento».
- Generadores: `herramientas/arte_lib.py` + `generar_arte_v3.py` (`python3 herramientas/generar_arte_v3.py assets/arte`). Piezas rojas con grabado fino y halo magenta: `generar_piezas.py`. Logo: `generar_logo.py` + `exportar_png.mjs` (ajusta el viewBox al contenido + 3 % de margen; PNG con transparencia real).
- Rojo solo sobre azul: en cortes sobre negro se usan cian/hielo. Capturas: `node herramientas/capturar.mjs capturas http://localhost:8000/index.html` (Playwright).

## v4 · negro como refuerzo (como public/art/* y public/art/cromo/* del repo)
Lo que se observó en las referencias: campo azul eléctrico saturado con el negro como segunda tinta (aprox. 25–35 % del área): trazos gruesos de circuito y un bloque-chip negro (panel-chip-rear), contorno negro duro y sombra de capa en cada pieza roja (panel-consoles-front), rejilla de piso negra en perspectiva, estrellas negras de 4 puntas, siluetas de torres/objetos con grabado oscuro, bloques y tramas de puntos (field-gaming, gm-blue-world). El rojo siempre queda sobre azul con borde/sombra negra.
Qué se agregó (`herramientas/generar_negro_v4.py` → `assets/arte/campo-<sección>-negro.svg` y `-sombra.svg`, más CSS):
- Todas las secciones: cuchilla negra arriba y abajo, marco con esquinas, bloques escalonados en esquinas opuestas, placas negras para títulos y entradillas, sombra dura bajo los objetos en línea, contorno negro + sombra dura en piezas rojas, riel negro bajo cada fila, esquinas negras en tarjetas y muestras.
- Hero: rejilla de piso negra, siluetas escalonadas en el horizonte, estrellas negras, tramas de puntos, volumen negro de las placas.
- Paleta: chip negro con pistas gruesas, circuitos pequeños, marcas de registro, trama.
- Cromo: volumen negro de las placas isométricas, pilares escalonados, trazos de rayado, estrellas.
- Parallax: planetas negros con anillo, estrellas negras de varios tamaños, bloques flotantes, trama.
- Filas: chips negros con pistas, bits cuadrados, vías.
- Catálogo: escalera pixel negra gruesa, placas con volumen, cartuchos-silueta, trama.
- Streaming: haz de rayos negros, perforaciones de cinta, estrellas.
- IA: red neuronal negra, chip negro con pistas, matriz binaria en bloques.

## v5 · más rojo al frente (cantidad y variedad), sin saturar
- **17 piezas rojas nuevas** (SVG, 45 KB en total, sin texto dentro): consola de sobremesa, joystick arcade, teclado, ratón, tarjeta gráfica, disco, bocina, servidor, cursor, flecha, etiqueta, sello/insignia, estrella de 4 puntas, botón arcade, control remoto, micrófono y cinta. Todas con contorno negro duro, sombra de capa azul noche, halo magenta fino y grabado fino rojo oscuro (`herramientas/generar_rojo_v5.py`). Más **cintillos** en HTML/CSS (texto blanco sobre rojo oscuro #B3120A, contraste 6.98:1).
- **Colocación** (`herramientas/colocar_v5.py`, idempotente): 91 piezas/cintillos en 8 secciones azules + 1 en cada mosaico del grabado, en 4 capas de parallax (.05 · .12 · .22 · .36). Las del frente van en zonas sin texto; las de «atrás» asoman por detrás de tarjetas y placas. Móvil: bandas arriba y abajo y tiras en el flujo (no tapan nada), parallax a la mitad.
- Rojo siempre sobre azul; sin parpadeo; con «reducir movimiento» todo queda quieto.
- **Pendientes de v4 resueltos:** planetas negros solo en los bordes (ya no rozan piezas rojas), rayos de streaming al 55 % de opacidad y más delgados.
- **Verificación:** `node herramientas/solape.mjs 1440|390` (piezas del frente vs. texto/controles al barrer el scroll → 0 solapes), `node herramientas/contraste.mjs` (contrastes WCAG), `python3 herramientas/medir_rojo.py <v4> <v5>` (% de rojo por captura), `node herramientas/capturar.mjs`.


## v6 · mínima, limpia y artística (edición tipo galería)
Fernando pidió bajar la densidad de v5. `index.html` ahora se genera con `python3 herramientas/construir_v6.py index.html`.
- **Una pieza héroe roja por sección + 2–3 de apoyo** (máx. 4; v5 tenía 11–13). Héroes dibujados a mano en SVG con volumen en 3 tonos de rojo, grabado fino, contorno negro duro y sombra de capa (`herramientas/generar_heroes_v6.py` → `assets/heroes/`): mando (inicio), consola portátil (paleta), chip isométrico sobre placas (cromo), audífonos (parallax), pantalla con catálogo (filas), joystick arcade (catálogo), claqueta (streaming), tarjeta gráfica (IA).
- **Parallax en 3 capas suaves:** fondo fijo/grabado (.04), héroe (.08, tope ±44 px) y apoyo (.14–.26, tope ±60 px) con `tanh` para que el movimiento sea lento y deliberado. Móvil a la mitad. `?reduce` o «reducir movimiento» lo apaga.
- **Retícula editorial:** 12 columnas, guías de 6 columnas casi invisibles, cabecera de lámina (número, nombre, filete, «NN / 10»), etiqueta negra y pie «Lámina NN · héroe» sobre un marco fino con esquinas.
- **Tipografía:** display Instrument Serif (regular + cursiva, OFL, autohospedada; sustituye a Bangers fuera del logo), texto Outfit, etiquetas Space Mono. Títulos en hielo, nunca rojos.
- **Arte azul y negro sutil:** una sola capa de grabado por sección (opacidad .5, con máscara que despeja el lado del texto) y el negro solo como acento: etiqueta, esquinas del marco, un bloque escalonado en la esquina, la sombra dura del héroe y las tarjetas de las filas.
- **Cortes:** 3 (diagonal fina, escalón, línea con muescas), con una línea de precisión.
- **Filas Netflix:** igual (flechas, arrastre, táctil, teclado); tarjetas con sombra negra y «Cotizar →» como enlace para que el rojo se concentre en el héroe.
- **Verificación:** `node herramientas/solape.mjs 1440|390` (0 solapes), `node herramientas/contraste.mjs`, `python3 herramientas/medir_rojo.py capturas`, `node herramientas/capturar.mjs capturas http://localhost:8766/index.html`.
- Los assets de v3–v5 que ya no se usan (`campo-*-negro/sombra/objetos.svg`, piezas pequeñas sobrantes) se dejan en `assets/` sin borrar.
