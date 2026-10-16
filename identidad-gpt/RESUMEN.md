# GameMaster · Identidad visual GPT (tercera propuesta)

Diseñada con Codex (gpt-6.1-sol, esfuerzo alto). Es una página aparte: no toca la web, `identidad-visual/` ni `main`.
**Para verla:** abre `identidad-gpt/index.html` (doble clic). Con `?reduce` se apaga el movimiento.

## La idea
Un titular enorme y blanco sobre negro, con un solo objeto rojo al frente (un cartucho de juego) y una rejilla azul de línea fina al fondo. Cada sección cambia de objeto rojo: cartucho, servidor, bocina. Así se ve distinta a las propuestas de Claude: tipografía gruesa en lugar de serif, sin «láminas», objetos y planos nuevos.

## Cómo cumple las reglas
- Base negra, mucho espacio vacío.
- Azul solo atrás y en línea fina; rojo solo adelante, en zonas distintas. Nunca texto rojo sobre azul.
- Un objeto, una forma. Sin brillos, sin degradados, sin morado, sin copias.
- Parallax real: el azul se mueve menos que el rojo; en celular se reduce a la mitad.
- 5 cortes entre secciones, cada uno con dibujo distinto (diamantes, peine, perforado, prismas, trenza).
- Filas tipo Netflix: Juegos, Streaming, IA y Plataformas (flechas, arrastre y teclado).
- Precios siempre «Consultar precio»; cotización por WhatsApp (mismo enlace de siempre).
- Logo de Fernando y logos de plataformas en PNG/SVG sin fondo.

## Lo que se revisó
- Auditoría automática: 0 hallazgos (`herramientas/auditar.py`).
- Contraste de colores: 0 fallas, el mínimo es 9.67 a 1 (`herramientas/contraste.py`).
- Capturas en `capturas/` a 1440 y 390 px, sin errores en consola ni desbordes laterales.

## Pendientes honestos
- Disney+, Prime Video, Nintendo Switch, Xbox y ChatGPT usan marcas de arte previo; conviene confirmar con los kits oficiales.
- Los joysticks de ChatGPT (rojo/azul) no se usaron en esta versión.
- Las marcas de terceros pertenecen a sus dueños.
