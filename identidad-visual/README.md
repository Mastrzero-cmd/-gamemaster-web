# GameMaster · Identidad visual v3 (propuesta)

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
