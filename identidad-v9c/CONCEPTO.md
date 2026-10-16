# v9c «Mapa / Expedición»

**Idea en una frase:** la web es un mapa de aventura grabado a mano; el azul es el territorio (curvas de nivel, costas, rosas de los vientos, constelaciones) y el rojo son sellos-emblema grandes (Trifuerza, espada, hongo, Pokébola, anillo, estrella…) estampados encima. El scroll es un viaje de nivel en nivel (I a VIII) con una ruta punteada y un alfiler rojo que avanza.

## Lenguaje visual (distinto a v1–v8, Cartel y a las otras propuestas v9)
- **Composición:** cartelas de mapa (cajas negras con marco doble de hielo) sobre planos de mapa a sangre; marco de mapa («neatline») con segmentos alternos en las secciones azules; los sellos rompen el marco.
- **Tipografía:** Cinzel (capitales romanas de inscripción) para titulares, Alegreya Sans (humanista) para texto, IM Fell English cursiva para notas y coordenadas. Autohospedadas WOFF2, licencia SIL OFL (en `assets/fonts/`).
- **Arte azul (grabado, sin rejillas):** curvas de nivel por *marching squares* propio, costas con rayado de oleaje, montañas con trazos, ondas del mar, rosas de los vientos de 16 puntas con rumbos radiales, mares de crestas de señal (streaming), constelaciones con red neuronal de nodos y trazos tipo circuito (IA), ondas concéntricas (logo), mapa del tesoro (cierre).
- **Arte rojo:** sellos de lacre de 600×600 (disco negro + aro rojo + marcas de grado) con emblema: Trifuerza, Espada Maestra, hongo, Pokébola, anillo, estrella, corazón, fantasma (Pac-Man), Pac-Man, invasor, creeper, televisión, chip con destello de IA, equis del tesoro y aguja de brújula.
- **Cortes de sección = bordes de mapa con aristas nítidas:** acordeón (pliegues en Z con dobleces), esquina doblada, costa irregular con eco de oleaje, meridianos (paralelos azules sobre negro).
- **Filas Netflix:** cabecera de cartela con contador «03 / 14» y flechas redondas, tarjetas con marco, medallones para servicios; scroll-snap, flechas, arrastre, teclado y táctil.
- **Logo de Fernando:** solo en su cartela (hero) y en su sección «Cartela del mapa»; en la barra va la versión mono blanca.
- **Brújula fija** abajo a la derecha: aguja roja que gira con el scroll y nivel actual.

## Reglas de cromoestereopsis
Rojo al frente (sellos), negro en medio (disco del sello y cartelas), azul detrás (planos). Cada SVG es de una sola geometría: planos azul/negro, sellos rojo/negro/hielo; nunca rojo y azul en un mismo objeto. Sin blur, glow, degradados, opacidades, morado ni copias desplazadas. Texto en hielo o negro (negro sobre rojo, 5.3:1); nunca texto rojo. Parallax: azul 0.03 (tope 26 px), rojo 0.10–0.22 (tope 70 px); `prefers-reduced-motion` lo detiene todo.

## Archivos
`index.html`, `styles.css`, `app.js` (estáticos, sin build ni CDN) · `assets/{planos,heroes,piezas,fonts,logo,logos-mono,portadas}` · `herramientas/` (`generar_arte.py` genera todo el arte, `auditar.py`, `medir_mezcla.py`, `capturar.mjs`, `solape.mjs`, `contraste.mjs`) · `capturas/`.
Los logos de `logos-mono/` son copia sin cambios de `/workspace/bots/Gpt/arte_gm/E_logos/`.
Ver: `python3 -m http.server` dentro de esta carpeta y abrir `index.html`.
