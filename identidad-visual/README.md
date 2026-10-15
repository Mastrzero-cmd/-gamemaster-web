# GameMaster · Identidad visual v4 (propuesta)

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
