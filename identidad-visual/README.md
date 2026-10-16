# GameMaster · Identidad visual v7 (propuesta)

Página estática aislada (HTML + CSS + JS vanilla, sin build, sin CDN). No toca la web, `main` ni el PR #1.
**Abrir:** `identidad-visual/index.html` (doble clic) o `python3 -m http.server`. Movimiento reducido: `index.html?reduce`.

## Qué dicen los docs del repo (y cómo lo cumple v7)
Fuentes: `docs/CHROMOSTEREOPSIS.md`, `docs/VISUAL_SYSTEM.md`, `AGENTS.md`, `docs/REFERENCE_IMAGES.md` y las imágenes `public/art/cromo/*` (abiertas y comparadas en `capturas/comparativa-referencias.jpg`).
1. **Un objeto, una geometría** (CHROMOSTEREOPSIS «First principle»): nada de copias desplazadas rojo/azul, contornos fantasma ni halos.
2. **Tres planos** (CHROMOSTEREOPSIS «Three-plane grammar»): rojo = delante/focal, negro = neutro/aire, azul = atrás/estructural (retículas, curvas de nivel, circuitos, patrones). Formas y regiones **distintas**, bordes nítidos.
3. **Base negra** («read primarily as black», 55–65 % negro; VISUAL_SYSTEM) y mucho espacio negativo; el azul no rellena secciones.
4. **Sin difuminados ni brillo** en las estructuras principales; sin degradados rojo→azul ni púrpura.
5. **Texto:** nunca rojo sobre azul; el texto rojo solo sobre negro; texto pequeño en hielo/blanco.
6. **Movimiento:** el azul de fondo se mueve menos que el rojo; sin parpadeo; `prefers-reduced-motion`.
7. Referencias `public/art/cromo`: `panel-consoles-rear` (regiones azules sólidas con detalle negro), `panel-chip-front` (una masa roja con rejilla negra sobre negro), `sprite-*` (rojo sólido + rojo oscuro + negro, borde duro), `field-gaming/floor` (rejilla de piso y circuitos de línea fina, estrellas de 4 puntas).

## v7 en una línea
Base negra · azul = plano trasero (línea fina fija + una placa sólida con detalle negro) · rojo = una masa delantera por sección (+ 1 pequeña) · cortes de un trazo azul · logo aislado en su placa (el magenta existe solo ahí).

## Estructura
- `assets/planos/plano-*.svg`: 8 ventanas fijas de línea fina azul (horizonte y circuitos, retícula y guilloche, curvas de nivel, órbitas, circuitos, cordilleras píxel, rayos y ondas, red neuronal). Colores sólidos, sin opacidad.
- `assets/placas/placa-*.svg`: 8 regiones azules sólidas con detalle negro (arco y panel perforado, panel, losas isométricas, disco con trama, racks, cordillera y escalera, cinta de película, chip).
- `assets/heroes/heroe-*.svg`: 8 masas rojas (mando, portátil, chip, audífonos, pantalla, joystick, claqueta, tarjeta gráfica) solo rojo/rojo oscuro/negro, contorno negro duro.
- `assets/piezas/pieza-*.svg`: 7 piezas rojas pequeñas (estrella, sello, flecha, botón, play, etiqueta, cursor).
- Parallax: plano fijo (capa `fixed` recortada por la sección) · placa lenta (.03) · masa roja (.10) · pieza pequeña (.16–.26). Tope con `tanh`; móvil a la mitad; `?reduce` lo apaga.
- Tipografía: Instrument Serif (títulos, hielo), Outfit (texto), Space Mono (etiquetas). Filas Netflix: flechas, arrastre, táctil y teclas ← →. Precios siempre «Consultar precio»; cotización por WhatsApp.

## Herramientas (`herramientas/`)
- `generar_v7.py` (planos, placas, piezas) · `generar_heroes_v7.py` (heroes) · `construir_v7.py` (index.html).
- **`auditar.py`**: audita CSS/HTML/JS y todos los SVG: filtros/blur, text-shadow, box-shadow con blur, gradientes/máscaras, opacidad < 1 (incluye rgba/hex8), colores magenta/púrpura u otros fuera del sistema, rojo+azul en un mismo SVG o regla, texto rojo, palabra prohibida. Exenta el logo y los logos de terceros. Salida 1 si hay hallazgos. Resultado v7: **0**.
- **`capturar_auditoria.mjs` + `medir_mezcla.py`**: PNG sin pérdida con logo, portadas y logos de terceros ocultos y % de píxeles de mezcla (matiz 255°–345°). Resultado v7: máx. 0.001 %.
- `solape.mjs 1440|390` (masas/placas vs texto y controles: 0), `contraste.mjs`, `capturar.mjs`.
- Legado de v3–v6 (`generar_arte*.py`, `generar_negro_v4.py`, `generar_rojo_v5.py`, `colocar_v5.py`, `construir_v6.py`, `generar_heroes_v6.py`, `generar_piezas.py`): ya no se usan; sus assets (`assets/arte/`, piezas viejas) se eliminaron.

## Logo (`assets/logo/`)
SVG vectorial (texto convertido a trazos, fuente Bangers OFL) y PNG con fondo transparente (256/512/1024/2048 px).
Variantes: `completo`, `horizontal`, `compacto` (icono GM) × `oscuro`, `claro`, `mono-blanco`, `mono-noche`.
Regenerar: `python3 herramientas/generar_logo.py assets/logo` y `node herramientas/exportar_png.mjs assets/logo` (Playwright).

## Otros
Fuentes libres autohospedadas (Instrument Serif, Outfit, Space Mono, Bangers para el logo). Portadas, logos de servicios y plataformas copiados del repo. Las marcas de terceros pertenecen a sus dueños.

## v8 (incremental sobre v7)
- **Logos de servicios** (`assets/logos/`): 16 marcas en una sola tinta (hielo / negro / rojo del sistema, SVG con viewBox ajustado a la tinta + PNG hielo 256 con alfa). Fuente: simple-icons 16.35.0 (CC0 del paquete); marcas de sus dueños, solo para identificar el servicio. Generados con `herramientas/integrar_logos.py`. Sin logo mono disponible (Disney+, Prime Video, ChatGPT, Nintendo Switch, Xbox) → rótulo tipográfico. Se excluyó `max` (en simple-icons es el mensajero Max, no el streaming; HBO Max = `hbomax`).
- Placas uniformes (hielo sobre negro); al pasar/enfocar la placa pasa a masa roja con logo negro (sin glow). Sección nueva 07B «Logos de servicios».
- Peso: SVG del logo reducido (124 KB → 43 KB, coordenadas a 1 decimal, mismo dibujo); fuentes TTF → WOFF2 subconjunto latino/español (448 KB → 96 KB); se retiraron TTF sin uso (Bangers queda solo en `herramientas/fuentes-origen/` para regenerar el logo).
- Móvil: menos curvas y sin las brillantes detrás de «Rojo al frente, azul atrás» (`plano-cromo-movil.svg`).
- Flecha deshabilitada de las filas: `#6b6f8a` → `#9aa0c0`.
- Herramientas: `peso.mjs` (peso de la página).
