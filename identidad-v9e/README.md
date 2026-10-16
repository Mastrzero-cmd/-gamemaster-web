# GameMaster — Órbita / v9e

Una propuesta nueva de identidad para la web: azul plano, paisajes de curvas y símbolos rojos independientes. Título grande y sobrio; el catálogo queda en una zona negra de descanso. Todo vive en esta carpeta.

## La propuesta

- Arte propio: curvas de nivel, ondas de señal y ramas neuronales. Tres transiciones orgánicas distintas. Sin placas, rejillas ni figuras prismáticas.
- 14 símbolos SVG dibujados en código, con un único relleno rojo y sin personajes. El hongo es un objeto sin rostro.
- Portadas en su color original, búsqueda, cinco filtros, carruseles de juegos, streaming e IA, preguntas frecuentes y acceso a WhatsApp.
- Movimiento por desplazamiento y puntero: fondo lento y símbolos delanteros más rápidos. En móvil se reduce la amplitud y se recompone el arte. Con movimiento reducido los planos quedan quietos.
- Precios consultables y disponibilidad por confirmar. ChatGPT y Claude en IA; Proton VPN en privacidad.

La base azul es una decisión específica de esta propuesta, solicitada por el dueño. Sustituye aquí la proporción negra dominante de los documentos anteriores. La profundidad percibida puede variar entre personas; la página no depende de ella para funcionar.

## Abrir

Abre `index.html` directamente. También funciona con un servidor estático, sin compilación:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory identidad-v9e
```

Después abre `http://127.0.0.1:8765/` en tu navegador.

## Verificación

```sh
python3 identidad-v9e/herramientas/verificar.py
node --check identidad-v9e/app.js
```

El verificador usa Pillow, disponible en esta sesión. No instala nada. Revisa rellenos, efectos prohibidos, término restringido, archivos y destinos internos, enlaces, alfa útil de los PNG de assets, movimiento reducido declarado y contraste de todos los pares de texto definidos en `herramientas/contrastes.json`, usando los colores reales del CSS. Guarda `herramientas/verificacion.json` y termina con error si alguna regla falla. No demuestra por sí solo que todos los pares estén correctamente aplicados en cada estado del navegador.

Contrastes obtenidos: hielo/azul **8.15:1**, hielo/negro **18.24:1**, texto secundario/negro **9.70:1**, rojo/negro **5.44:1**. Los seis pares declarados superan 4.5:1. Los símbolos decorativos no son texto ni comunican estados por sí solos.

**Pendiente: capturas y revisión visual de la página en navegador.** El entorno de esta sesión impidió abrir el servidor local y arrancar Chrome. Se inspeccionó una muestra rasterizada del arte SVG; no se presenta como captura de la web. No se han comprobado todavía el parallax, foco, desborde, carruseles ni movimiento reducido en un navegador real.

```sh
python3 identidad-v9e/herramientas/capturar.py
```

Ese script deja preparado el servidor Python, Chrome/Chromium headless y las capturas completas `capturas/v9e-1440.png` y `capturas/v9e-390.png`. Además incluye comprobaciones a 430 px, búsqueda sin resultados, filtros, títulos largos, foco, carrusel, parallax y movimiento reducido. Requiere un entorno con permiso para iniciar el servidor y Chrome; el propio script todavía no se pudo ejecutar aquí de principio a fin. Revisa visualmente sus resultados antes de dar la propuesta por validada.

## Procedencia y edición

- Logos de servicios: copias mono hielo de `/workspace/bots/Gpt/arte_gm/E_logos`. Se usan sobre aperturas negras o junto a texto neutro.
- Logo de Fernando: copia PNG mono blanca de `identidad-visual/assets/logo/`. El SVG conserva su geometría; solo cambia el relleno blanco a hielo.
- Portadas: copias locales de `identidad-visual/assets/portadas/`, sin alteración.
- Paisajes y símbolos: SVG propios. `herramientas/dibujar.py` reproduce los archivos de `assets/arte/` y `assets/iconos/`.
- Colores y tamaños principales: variables al inicio de `styles.css`. Contenido comercial: HTML. Interacciones: `app.js`.

La página no solicita recursos externos; solo los enlaces de contacto abren WhatsApp al pulsarlos. No usa CDN, servicios de pago, datos remotos ni herramientas de generación por red. El pie incluye el aviso de marcas de terceros.

Sin cambios en otras carpetas. Sin commit ni push.
