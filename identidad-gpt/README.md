# GameMaster — Punto de entrada

Tercera propuesta visual, aislada en `identidad-gpt/`. Abre **index.html** directamente: HTML, CSS y JavaScript local; sin build, CDN, fuentes descargadas ni peticiones de datos.

Concepto: una entrada editorial al entretenimiento digital. Tipografía grotesca de sistema, titulares gigantes, un cartucho rojo sobre una fuga radial azul y navegación comercial directa. Nada de serif, numeración de piezas ni ventanas fijas. Bocina y servidor tienen otras siluetas; las filas cambian de escala y alineación. Las portadas conservan sus colores.

Negro dominante; estructuras azules de línea fina atrás; objetos rojos independientes delante. Los textos son neutros y descansan sobre superficies negras. El reparto 55–65 % negro es una referencia de composición; no se presenta como una medición de píxeles. No hay promesas sobre la percepción de profundidad de cada persona.

## Archivos

- `index.html`: página completa, cuatro filas, 14 juegos, 7 servicios de streaming, ChatGPT y Claude, cinco entradas de plataformas, contacto y preguntas frecuentes. Proton VPN tiene una entrada separada de privacidad.
- `styles.css`: composición, paleta, tipografía de sistema y versión móvil.
- `script.js`: búsqueda, colecciones, flechas, arrastre con mouse, desplazamiento táctil nativo, teclas ← → y parallax limitado.
- `assets/arte/`: 12 SVG originales: tres objetos, cuatro estructuras y cinco cortes distintos: peine, perforado, prismas, diamantes y trenza. Cada SVG artístico utiliza una sola familia cromática.
- `herramientas/generar.py`: regenera exactamente los SVG y las variantes hielo locales de las marcas que no tenían esa versión.
- `herramientas/auditar.py`: restricciones de efectos, paleta, alfa, texto rojo, separación cromática por SVG y vocabulario. Exenta exclusivamente `assets/logo/` y `assets/marcas/`.
- `herramientas/contraste.py`: contraste WCAG de todos los pares de texto de la paleta; también puede leer los pares reales del verificador de navegador.
- `herramientas/verificar.py`: referencias locales, enlaces, dimensiones, SVG y sintaxis; modo adicional de Chrome sin capturas.

## Uso

Las filas funcionan por desplazamiento nativo incluso sin JavaScript. La búsqueda y los botones requieren JavaScript. Todos los precios dicen «Consultar precio» y los enlaces de consulta usan exactamente `https://wa.me/525527699426`.

El parallax usa posiciones reales de scroll, velocidades diferentes y límites de 12 px atrás / 42 px delante; en móvil, velocidades y límites se reducen a la mitad. Se desactiva con la preferencia del sistema o abriendo `index.html?reduce`.

Desde la raíz del repositorio:

```sh
python3 identidad-gpt/herramientas/generar.py
python3 identidad-gpt/herramientas/auditar.py
python3 identidad-gpt/herramientas/contraste.py
python3 identidad-gpt/herramientas/verificar.py --local
```

La auditoría visual estática termina con **0 hallazgos**. Los cinco pares de texto de la paleta pasan 4.5:1; mínimo **9.67:1**. La sintaxis y las referencias locales pasan. Los informes quedan en `herramientas/`.

La revisión en Chrome de 1440, 390 y 430 px está preparada con `python3 identidad-gpt/herramientas/verificar.py` y utiliza el Chrome y la biblioteca Python `websockets` existentes. **No pudo ejecutarse en este entorno:** se bloquean la apertura de sockets y el arranque de Chrome. No se atribuyen resultados de navegador a las comprobaciones estáticas. No se tomaron capturas ni se hicieron commits.

## Recursos y procedencia

- Logo de Fernando: SVG oscuro horizontal y compacto, más PNG horizontal transparente, copiados de `identidad-visual/assets/logo/`. Su tinta original se conserva.
- Marcas hielo: copias de `/workspace/bots/Gpt/arte_gm/E_logos/`. Para ChatGPT, Nintendo Switch, Disney+ y Xbox Game Pass se copió el original desde `identidad-visual/assets/servicios/`; el generador crea variantes monocolor sin alterar sus trazos y preserva los originales. La placa roja de fondo del logo Nintendo se elimina sólo en su variante hielo.
- Portadas: copias de `identidad-visual/assets/portadas/`, sin retoques ni efectos.
- `assets/recursos/rojo_joystick.png` y `azul_joystick.png`: copias del directorio solicitado. Ambos tienen canal alfa real con píxeles transparentes; cifras en `transparencia.json`. Se conservan como biblioteca y no aparecen en la composición para mantener una identidad diferente.
- El arte propio se dibuja con Python estándar y SVG; no usa gráficos de v7. Los logotipos de terceros son de sus respectivos titulares y no implican afiliación.
