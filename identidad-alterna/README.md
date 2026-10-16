# Identidad visual ALTERNA · «Cartel»

Propuesta alterna para la web de GameMaster, hecha en paralelo a `identidad-visual/` (v1–v7) y pensada para no parecerse. Misma base obligatoria (docs/CHROMOSTEREOPSIS.md y docs/VISUAL_SYSTEM.md): rojo al frente, negro en medio, azul atrás, como regiones distintas con bordes nítidos.

**Idea en una frase:** un cartel constructivista de titulares enormes y figuras geométricas planas, no una galería de láminas con ilustraciones.

## En qué difiere de v7

| Aspecto | v7 (identidad-visual) | Alterna «Cartel» |
|---|---|---|
| Composición | Texto a la izquierda, ilustración a la derecha, láminas numeradas | Titular de cartel a todo el ancho; riel lateral fijo con sección actual y avance; cada sección cambia de maqueta (arte a la izquierda, a la derecha, en franja, sin arte) |
| Tipografía | Instrument Serif · Outfit · Space Mono | **Big Shoulders Display** (grotesca condensada, mayúsculas) · **Archivo** · **JetBrains Mono**. Autohospedadas, licencia SIL OFL |
| Arte | Objetos ilustrados rojos (mando, chip, audífonos…) sobre placas azules con circuitos y retícula en perspectiva | Geometría pura en SVG: disco con cruceta, tetromino, triángulo de reproducción, chip, palanca, anillo. Atrás: puntos de media tinta, retículas de bloques, arcos, circuitos, rayado, cuadrados concéntricos |
| Azul | Líneas finas y placas sólidas | Líneas, puntos, bloques, barras verticales y cintas de corte; bordes de 2 px |
| Cortes de sección | Un trazo azul fino: diagonal, escalón, muescas | **Cintas azules sólidas y gruesas**, generadas por JS: dientes de sierra, escalones de píxel y arcos |
| Sistema de color | Paleta en fichas | Tres franjas verticales 15 % rojo / 60 % negro / 25 % azul, con negro siempre entre rojo y azul |
| Logos de servicios | Tarjetas sobre placas de color | 17 logos monocromos en hielo (Gpt, `E_logos`, sin tocar) en cuadrícula; las marcas sin logo monocromo disponible (Disney+, Prime Video, Nintendo Switch, Xbox Game Pass, ChatGPT) van como texto condensado |
| Filas tipo Netflix | Título arriba, flechas arriba | Columna de control a la izquierda (título, contador «03 / 14», flechas) y la fila se desborda hasta el borde derecho |
| Cierre | Pie discreto | Bloque rojo completo: «Cotiza por WhatsApp» en negro sobre rojo |
| Paleta | #050505 / #0A0A0D / #1A26A8 / #2A3CFF / #FF2A1A | #050505 / #0B0B0D / #1616FF / #FF1A1A / #F4F4EF (valores de docs/CHROMOSTEREOPSIS.md) |

## Reglas que se cumplen

- **Una imagen, una geometría.** Cada escena son tres capas del mismo lienzo (1200×700): azul trasero (`assets/planos`), una masa roja (`assets/heroes`) y piezas rojas pequeñas (`assets/piezas`). Ningún SVG mezcla rojo y azul. El rojo lleva un borde negro que lo separa del azul.
- **Sin blur, glow, sombras difuminadas, degradados, opacidades, morado ni copias desplazadas.** Lo comprueba `herramientas/auditar.py` (0 hallazgos fuera del logo).
- **Texto:** hielo sobre negro/azul, negro sobre rojo. Nunca rojo sobre azul, nunca texto rojo. Los contornos de titular son hielo; los números fantasma, azul sobre negro (decorativos).
- **Parallax:** el azul se mueve más lento (0.03) que el rojo (0.10) y que las piezas (0.22), con tope en píxeles. `prefers-reduced-motion` deja todo quieto.
- **Logo de Fernando:** solo dentro de su placa (portada y sección Logo). En la barra superior se usa la versión monocroma blanca.
- **Se lee negro:** en las mediciones sobre capturas, ~79 % negro, ~10 % rojo, ~5 % azul (cuando aparece el bloque rojo final sube el rojo).
- **Contenido real:** catálogo, precios («Consultar precio») y WhatsApp (55 2769 9426) tomados de v7 y del repo. No hay personajes.

## Archivos

- `index.html` (generado por `herramientas/construir.py`), `styles.css`, `app.js`: HTML/CSS/JS estáticos, sin build ni CDN.
- `assets/`: `fonts/`, `planos/`, `heroes/`, `piezas/`, `logo/` (logo de Fernando), `logos-mono/` (copia sin cambios de `/workspace/bots/Gpt/arte_gm/E_logos/`, con INDICE.md), `portadas/`.
- `herramientas/`: `generar_arte.py`, `construir.py`, `auditar.py`, `medir_mezcla.py`, `capturar.mjs`, `capturar_auditoria.mjs`, `solape.mjs`, `contraste.mjs`.
- `capturas/`: 1440 y 390, completas y por sección.

## Cómo verlo

Abrir `identidad-alterna/index.html` en el navegador, o `python3 -m http.server` dentro de la carpeta. Las capturas se generan con Playwright (`node capturar.mjs capturas http://localhost:8777/index.html`).
