# v10d · Póster en profundidad (mejora de v9d)

Mismo cartel psicodélico de v9d, ahora con **cinco planos reales** y un parallax cinemático. Rojo delante, negro en medio, azul detrás; una geometría por objeto; bordes nítidos; sin brillos, degradados, desenfoques, copias desplazadas ni mezcla rojo+azul dentro de un objeto.

## Capas (de atrás hacia delante) y velocidad
Cada sección de pantalla completa es un `.stage` con capas `div.ly` movidas con `translate3d` (variable `--py`), interpolación con `requestAnimationFrame` (lerp .14), amplitud acotada con `tanh` y factor .55 en móvil. `prefers-reduced-motion`: todo `transform:none`, nada se mueve.

| Capa | Clase | Contenido | Factor | Límite |
|---|---|---|---|---|
| 1 azul fondo | `.ly.bk` | ondas, rayos, ornamento en trazo fino azul (dentro de la ventana) | .02 | 10 px |
| 2 negro medio | `.ly.md` | bandas negras y discos negros con aro azul fino, entre azul y rojo | .08 | 34 px |
| 3 texto | – | titular, texto, tarjetas (en reposo) | 0 | – |
| 4 rojo frente | `.ly.fr` | masas rojas grandes (cintas, arcos, objetos, slots grandes) con halo negro; rompen el marco (12 % de sangrado) | .30 | 150 px |
| 5 piezas rojas | `.ly.pc` | piezas pequeñas (corazón, espada, destello, slots pequeños) | .55 | 230 px |

El desplazamiento extra va en el sentido del scroll: lo cercano avanza más rápido que la página (como en cine), lo lejano casi se queda con ella.

### Medición a +600 px de scroll (`herramientas/parallax.mjs`, Chromium headless, sección centrada → +600 px)
| Capa | 1440 px | % del scroll | 390 px | % del scroll |
|---|---|---|---|---|
| azul fondo | 8.3 px | 1.4 % | 5.8 px | 1.0 % |
| negro medio | 30.2 px | 5.0 % | 22.1 px | 3.7 % |
| rojo frente | 125.1 px | 20.9 % | 86.8 px | 14.5 % |
| piezas rojas | 205.5 px | 34.3 % | 151.4 px | 25.2 % |

(Idéntico en las cuatro secciones medidas: inicio, catálogo, streaming, IA. En reposo, con la sección centrada, todas valen 0.)

## Cromoestereopsis más marcada
- Masas rojas mucho mayores (×1.4 sobre v9d) sobre las ventanas azules, con halo negro grueso (22 px) que separa rojo de azul.
- Cintas, arcos y discos rojos abstractos que cruzan y rompen el marco de la ventana.
- Plano negro intermedio (bandas y discos con aro azul fino) que añade una capa más entre azul y rojo.
- Escalas muy contrastadas (slots de 150 a 700 u frente a ornamento de trazo fino) y velocidades escalonadas por capa.

## Sistema tipográfico unificado
Shrikhand (display) + Josefin Sans (texto). Todas las secciones usan: etiqueta (número rojo + `kicker` en Josefin versalitas con subrayado azul) → titular apilado en 3 líneas (`.pila`: línea 1 itálica pequeña, línea 2 grande hielo, línea 3 contorno grueso) → lead → contenido. Subtítulos `h3` con un único estilo; mismas medidas, pesos y espaciados vía variables CSS. Sin texto rojo ni rojo sobre azul.

## Personajes = slots
Los personajes ya no se dibujan: son 19 `span.slot[data-slot="personaje-…"]` con silueta genérica roja de borde negro y tamaño fijo, para sustituir por imágenes generadas. Lista completa en `SLOTS.md`. Se conservan los íconos de objeto: corazón, espada, bola de captura, mando, tele, play, robot y destello.

## Se mantiene de v9d
Palabra prohibida construida partida en `auditar.py`, portadas de una sola tinta, borde negro separador, contornos gruesos, filas con flechas, `index.html` estático sin CDN.

## Proporción de color medida (capturas con logos y portadas ocultos)
Ver README.md (se actualiza con cada ronda).
