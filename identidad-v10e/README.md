# GameMaster — Órbita / v10e

Catálogo estático de Gaming, Streaming e IA. Esta versión refuerza el frente rojo sobre azul plano: formas más grandes, separadores negros y tres velocidades de movimiento. Conserva búsqueda, colecciones, carruseles y contacto por WhatsApp. Los precios siguen como «Consultar precio».

## Abrir y probar el movimiento

Abre `identidad-v10e/index.html` directamente. No requiere instalación, compilación ni conexión. También puedes usar un servidor local desde la raíz del repositorio:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory identidad-v10e
```

Abre `http://127.0.0.1:8765/`. Desplázate lentamente en la primera pantalla y en las zonas de Streaming, IA y contacto; en computadora mueve también el puntero. El catálogo permanece estable.

| Plano | Velocidad de scroll | Puntero máximo | Tope de desplazamiento |
| --- | --- | --- | --- |
| Azul / `rear` | 0.015 | 2 px | 18 px |
| Rojo / `front-1` | 0.10 | 24 px | 80 px |
| Rojo / `front-2` | 0.18 | 42 px | 130 px |
| Rojo / `front-3` | 0.28 | 64 px | 184 px |

El tope se aplica al resultado combinado de scroll y puntero. En móvil se usa la mitad de amplitud; el puntero solo participa en dispositivos con apuntador preciso. El suavizado usa interpolación gradual (lerp) en `requestAnimationFrame`, ajustada al tiempo entre cuadros; se detiene al llegar a su posición. Los fondos tienen margen extra de 32 px para cubrir el movimiento sin mostrar bordes vacíos.

Añade `?reduce` o `?reduce=1` a la dirección para desactivar las transformaciones y el desplazamiento animado. También se respeta la preferencia de movimiento reducido del sistema, incluso si cambia mientras la página está abierta. Ambos mecanismos añaden `reduce-motion` a `<html>` desde el encabezado, antes de pintar la página. Para reactivar, quita el parámetro, recarga y revisa la preferencia del sistema.

## Arte y tipografía

- Rojo de frente `#FF0000`, azul plano `#1919E8` y placas negras `#080808`. Cada geometría usa rojo o azul, con negro como separación; no hay copias desplazadas del mismo objeto. Texto neutro sobre azul; texto rojo únicamente en zonas negras.
- Cuatro lugares para futuras imágenes: `hero-principal`, `hero-rombo`, `hero-bloque` y `stream-circulo`. Cada uno tiene `data-reservado` y el comentario `RESERVADO: imagen generada`. Hoy muestran círculos, rombo o bloque rojos simples. No se generaron imágenes.
- Se retiraron los símbolos decorativos de franquicias y sus SVG; el generador local ya no los reproduce. Quedan símbolos tecnológicos genéricos.
- Unbounded 700/800 en títulos; Space Grotesk 400/500/700 en texto y controles. Cinco WOFF2 locales con carga `swap` y dos precargas críticas. Escala de tamaños en las variables de `styles.css`; respaldo `system-ui`. Licencias OFL y nota en `assets/fuentes/LEEME.md`.
- Logos mono de `assets/logos/`, procedentes de `/workspace/bots/Gpt/arte_gm/E_logos`. Las portadas existentes se conservan en rojo/negro, sin nueva conversión.

La profundidad percibida varía según la persona y pantalla. Estos colores y velocidades son decisiones de diseño, no una garantía perceptual.

## Verificar sin capturas

Desde la raíz del repositorio:

```sh
python3 identidad-v10e/herramientas/verificar.py
node --check identidad-v10e/app.js
python3 identidad-v10e/herramientas/capturar.py --solo-pruebas
```

`verificar.py` usa Python y Pillow ya instalados. Revisa recursos locales, efectos prohibidos, texto restringido, precios, contacto exacto, espacios reservados, tipografías, color de símbolos y contraste. Escribe `herramientas/verificacion.json`.

`capturar.py --solo-pruebas` abre el archivo local con Chrome por tuberías, bloquea HTTP/HTTPS y comprueba 1440, 390 y 430 px, búsqueda, filtros, foco, carruseles, fuentes, velocidades, límites y ambos modos de movimiento reducido. No crea imágenes. Guarda `herramientas/navegador.json`.

Las 270 comprobaciones estáticas y `node --check` pasaron. Se probó además el código real de movimiento con Node y un DOM simulado: velocidades, lerp gradual, topes, detención de cuadros, amplitud móvil y ambos parámetros `?reduce` pasaron; eso no verifica el diseño renderizado.

En esta sesión Chrome no pudo arrancar: `setsockopt: Operation not permitted`. Por eso la comprobación de anchos y consola en navegador queda pendiente; no se presenta como aprobada. Las revisiones estáticas no sustituyen esa prueba ni la revisión visual.

## Capturas manuales del dueño

Cuando quieras generarlas, ejecuta el mismo script **sin** `--solo-pruebas`. Produce `capturas/v10e-1440.png` y `capturas/v10e-390.png`. No se ejecutó ese modo durante este trabajo. Los PNG con `-base` son archivos heredados de la copia inicial; no muestran el resultado actual.

`herramientas/dibujar.py` mantiene los paisajes y símbolos genéricos; `planas.py` es una utilidad para convertir portadas y no se ejecutó. No hay solicitudes externas al abrir la página. El enlace a WhatsApp permanece en `https://wa.me/525527699426`.
