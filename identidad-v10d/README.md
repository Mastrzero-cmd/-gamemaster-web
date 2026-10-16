# v9d · «Póster psicodélico»

Propuesta de identidad visual de GameMaster hecha desde cero: un cartel de gira de los años 60-70, hecho de curvas, con el rojo gigante rompiendo el marco. Parte de STYLITES (la página como una sola composición gráfica) y de las referencias de cromoestereopsis de `docs/REFERENCE_IMAGES.md` (figura roja grabada al frente, campo azul de trazo fino atrás, negro en medio). Respeta `docs/CHROMOSTEREOPSIS.md` y `docs/VISUAL_SYSTEM.md`.

**Idea en una frase:** cada sección es una lámina de cartel: una ventana azul con forma (arco, hoja, óvalo, ola) llena de ondas, rayos solares, flores art nouveau y grabado fino, y encima un ícono rojo enorme que se sale de la ventana.

## Qué lo hace distinto
| Aspecto | v9d |
|---|---|
| Composición | Asimétrica. Texto apilado en un lado y una «ventana» con forma curva en el otro; la ventana cambia de forma y de lado en cada sección. Secciones de pantalla completa. |
| Tipografía | **Shrikhand** (display, gruesa y redondeada de cartel; apilada, girada unos grados, con una línea en contorno) y **Josefin Sans** (texto, geométrica de aire art nouveau). WOFF2 autohospedadas, licencia SIL OFL. Un arco de texto sigue el contorno del sol en el hero. |
| Arte azul | Sólo trazo y masa curva: bandas de ondas fluidas, rayos solares con giro, flor de pétalos en capas, látigos art nouveau con espiral y hojas, ojos de pavo real, curvas de nivel, nodos de red neuronal, ondas de señal. **Ninguna cuadrícula ni rejilla.** |
| Arte rojo | 19 íconos propios en SVG de masa roja con contorno y detalles negros: hongo, Trifuerza, silueta eléctrica, bolita rosa, anillo dorado, bola de captura, corazón, espada, invasor espacial, comecocos, fantasma, bloque «?», creeper, estrella, mando, tele retro, play, robot y destello. Son siluetas, no personajes con textura. |
| Cortes de sección | Cinco cortes curvos con arte distinto: cúpulas, ola, festones, gotas/pétalos y sol naciente. Más las propias ventanas curvas. |
| Filas tipo Netflix | Tarjetas en arco de ventana (portada dentro de un arco con marco azul); flechas redondas, contador, arrastre, teclado, scroll-snap. |
| Logos | 17 logos monocromos (Gpt, `E_logos`, sin tocar) en discos negros con aro azul, acomodados en una ola sobre las bandas azules. Las marcas sin logo monocromo (Disney+, Prime Video, Switch, Xbox, ChatGPT) van en texto display. |

## Reglas de cromoestereopsis
- Rojo al frente, negro en medio, azul atrás, siempre como regiones distintas con borde nítido. El rojo lleva contorno negro cuando toca azul.
- Un objeto, una geometría: ningún SVG ni regla CSS mezcla rojo y azul. Sin blur, glow, degradados, opacidades, morado ni copias desplazadas (`herramientas/auditar.py` = 0 hallazgos).
- Nunca texto rojo ni rojo sobre azul. Texto en hielo (#F4F4EF) sobre negro; negro sobre rojo.
- Parallax: azul 0.03 (más lento), rojo 0.10, piezas 0.22. El movimiento tiene tope en píxeles; con `prefers-reduced-motion` todo queda quieto.
- La página se lee negra: en las capturas ~72 % negro, ~9 % rojo y ~14 % azul (ronda 2). Los íconos rojos llevan un borde negro grueso que los separa siempre del azul.
- Las portadas de juegos van en una sola tinta (escala de grises) para que no metan rojo y azul juntos; el color vive solo en el sistema.
- El logo de Fernando (pincel cian-azul con contorno magenta) sólo aparece dentro de su placa (hero y sección Logo); en la barra va la versión monocroma blanca.

## Archivos
`index.html` (lo genera `herramientas/construir.py`), `styles.css`, `app.js`; `assets/` (`fonts`, `planos` azul, `heroes` y `piezas` rojos, `cortes`, `iconos`, `logo`, `logos-mono`, `portadas`); `herramientas/` (`iconos.py`, `arte.py`, `rojo.py`, `construir.py`, `auditar.py`, `medir_mezcla.py`, `capturar.mjs`, `verificar.mjs`); `capturas/`.

Regenerar: `python3 herramientas/arte.py && python3 herramientas/rojo.py && python3 herramientas/construir.py`. Ver: servir la carpeta del repo con `python3 -m http.server` y abrir `identidad-v9d/index.html`.
