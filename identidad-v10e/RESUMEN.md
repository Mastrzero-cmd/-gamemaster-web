# v10e — Órbita

- Frente rojo puro más grande, separado del azul plano con negro. Tres capas rojas a velocidades 0.10, 0.18 y 0.28; fondo a 0.015. Movimiento suave, con topes; en celular usa la mitad de amplitud.
- Para verlo, abre `index.html`, baja despacio y mueve el puntero en computadora. Se nota en la portada, Streaming, IA y contacto. El catálogo se queda estable.
- `?reduce` o `?reduce=1` quita las transformaciones y el scroll animado. También funciona la opción de movimiento reducido del sistema. Se añade la clase `reduce-motion` a `<html>`.
- Títulos con Unbounded 700/800 y texto con Space Grotesk 400/500/700. Fuentes locales, dos precargas y licencias OFL en `assets/fuentes/`.
- Cuatro espacios para futuras imágenes, marcados con `data-reservado` y comentario HTML. Por ahora son formas rojas neutras. Se quitaron los símbolos de franquicias y sus SVG. Portadas, logos, precios de consulta y WhatsApp se conservan.

Verificación estática y sintaxis de JavaScript aprobadas. También pasó la prueba de la lógica de movimiento con Node; no sustituye al navegador.

Límites: la profundidad varía según la persona y pantalla. Chrome no arrancó por una restricción del entorno; falta confirmar anchos y consola en navegador. El modo `capturar.py --solo-pruebas` queda listo para hacerlo sin imágenes. No se hicieron capturas nuevas, commit ni push.
