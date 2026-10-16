#!/usr/bin/env python3
"""Construye identidad-v9a/index.html (estático). Uso: python3 construir.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from iconos import ICONOS
OUT = os.path.join(os.path.dirname(__file__), '..', 'index.html')
WA = 'https://wa.me/525527699426'
ROM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
def ring_svg(txt, uid):
    # texto grabado en el anillo: hielo sobre negro, dentro del hueco del medallón
    return (f'<svg class="ly fr ringtxt" data-speed=".10" viewBox="0 0 1440 760" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><path id="r{uid}" d="M720 380m-262 0a262 262 0 1 1 524 0a262 262 0 1 1-524 0"/></defs>'
            f'<text class="rt"><textPath href="#r{uid}" startOffset="0" textLength="1636" lengthAdjust="spacing">{txt}</textPath></text></svg>')
def estampa(n, txt, cls=''):
    return (f'<figure class="estampa {cls}" aria-hidden="true"><img class="ly bk" data-speed=".03" src="assets/planos/{n}.svg" alt="" draggable="false">'
            f'<img class="ly fr" data-speed=".10" src="assets/heroes/{n}.svg" alt="" draggable="false">{ring_svg(txt, n)}'
            f'<img class="ly pc" data-speed=".22" src="assets/piezas/{n}.svg" alt="" draggable="false"></figure>')
CINTAS = ['VIDEOJUEGOS|STREAMING|INTELIGENCIA ARTIFICIAL|COTIZA POR WHATSAPP', 'NETFLIX Y MÁS|17 LOGOS|UNA SOLA TINTA|SIN FONDO', 'CONSOLAS|JUEGOS|ACCESORIOS|CUENTAS', 'SERIES|CINE|MÚSICA|ANIME', 'CHATBOTS|ASISTENTES|PRIVACIDAD|NODOS', '23 SELLOS|ROJO AL FRENTE|NEGRO AL MEDIO|AZUL ATRÁS', 'PINCEL|CIAN A AZUL|SOLO EN SU PLACA|SVG Y PNG', 'FRENTE 15 %|MEDIO 60 %|FONDO 25 %|SIN MEZCLA', 'CINCO GRABADOS|ONDAS|ABANICO|CUERDA', 'COTIZA|CONSULTA EL PRECIO|55 2769 9426|WHATSAPP']
def cinta(i):
    a = CINTAS[i].split('|')
    return '<p class="cinta" aria-hidden="true">' + '<i></i>'.join(f'<span>{x}</span>' for x in a) + '</p>'
def banda(i, etiqueta, l1, l2='', hid='', h='h2'):
    return (f'<header class="enc"><p class="num"><span>N.º {ROM[i]}</span><i></i><span>{etiqueta}</span></p>'
            f'<{h} class="banda" id="{hid}"><b>{l1}</b>' + (f'<em>{l2}</em>' if l2 else '') + f'</{h}>' + cinta(i + 1) + '</header>')
def corte(t): return f'<div class="corte c-{t}" role="presentation" aria-hidden="true"></div>'
MARCAS = [('Netflix', 'netflix'), ('HBO Max', 'hbomax'), ('Max', 'max'), ('Spotify', 'spotify'), ('YouTube', 'youtube'), ('YouTube Music', 'youtubemusic'), ('Crunchyroll', 'crunchyroll'), ('Apple TV', 'appletv'), ('PlayStation', 'playstation'), ('Steam', 'steam'), ('Claude', 'claude'), ('Anthropic', 'anthropic'), ('Google Gemini', 'googlegemini'), ('Proton', 'proton'), ('Proton VPN', 'protonvpn'), ('Twitch', 'twitch'), ('Discord', 'discord')]
tiles = ''.join(f'<li><span class="roundel"><img src="assets/logos-mono/{f}_mono_hielo.svg" alt="" width="44" height="44" loading="lazy" draggable="false"></span><span class="nm">{n}</span></li>' for n, f in MARCAS)
NOMBRES = dict(triforce='Trifuerza', hongo='Hongo', pokebola='Pokébola', pikachu='Ratón eléctrico', corazon='Corazón', espada='Espada', bloque='Bloque «?»', estrella='Estrella', tuberia='Tubería', pacman='Comecocos', fantasma='Fantasma', invasor='Invasor', tetris='Bloques que caen', creeper='Rostro cúbico', anillo='Anillo', kirby='Bola rosa', amongus='Tripulante', rupia='Rupia', ocarina='Ocarina', pantalla='Pantalla', neuronal='Red neuronal', chip='Chip', onda='Onda de audio')
sellos = ''.join(f'<li><span class="seal"><img src="assets/sellos/{k}.svg" alt="" width="120" height="120" loading="lazy" draggable="false"></span><span class="nm">{NOMBRES[k]}</span></li>' for k in ICONOS)
T = lambda a: a + ' · '
H = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GameMaster · Identidad v9a «Grabado»</title>
<meta name="description" content="Propuesta v9a «Grabado»: estilo billete antiguo. Fondo azul de grabado fino, sellos rojos al frente, negro en medio (cromoestereopsis).">
<link rel="preload" href="assets/fonts/BodoniModa.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css"></head><body>
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="bar"><nav class="nav l" aria-label="Secciones"><a href="#marcas">Marcas</a><a href="#catalogo">Catálogo</a><a href="#streaming">Streaming</a></nav>
<a class="brand" href="#inicio" aria-label="GameMaster, inicio"><img src="assets/logo/gamemaster-horizontal-mono-blanco.svg" alt="GameMaster" width="132" height="34"></a>
<nav class="nav r" aria-label="Más secciones"><a href="#ia">IA</a><a href="#sellos">Sellos</a><a class="btn red" href="{WA}" rel="noopener">Cotizar</a></nav></header>
<main id="contenido">

<section class="sec hero" id="inicio" aria-labelledby="h1">
 <header class="enc"><p class="num"><span>Serie A · N.º 001</span><i></i><span>Videojuegos · Streaming · IA</span></p>
 <h1 class="banda" id="h1"><b>Todo tu universo</b><em>digital</em></h1>{cinta(0)}</header>
 {estampa('inicio', T('GAMEMASTER · VIDEOJUEGOS · STREAMING · IA'), 'hero-st')}
 <div class="tres">
  <div class="plate logoplate"><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="GameMaster" width="320" height="224"></div>
  <div class="txt"><p class="lead">Elige, consulta el precio y cotiza por WhatsApp. Un solo lugar para tus juegos, tus series y tus herramientas de inteligencia artificial.</p></div>
  <div class="cta"><a class="btn red" href="#catalogo">Ver catálogo →</a><a class="btn line" href="{WA}" rel="noopener">Hablar por WhatsApp</a></div>
 </div>
</section>
{corte('ondas')}

<section class="sec" id="marcas" aria-labelledby="h-marcas">
 {banda(0, 'Marcas', '17 marcas,', 'un solo lugar', 'h-marcas')}
 {estampa('marcas', T('LOGOS EN UNA SOLA TINTA · SIN FONDO · SIN COLOR DE MARCA'), 'st-b')}
 <ul class="roundels">{tiles}</ul>
 <p class="fine">Las marcas pertenecen a sus dueños y se usan solo para identificar el servicio.</p>
</section>
{corte('abanico')}

<section class="sec" id="catalogo" aria-labelledby="h-cat">
 {banda(1, 'Catálogo', 'Consolas', 'y juegos', 'h-cat')}
 {estampa('catalogo', T('CONSOLAS · JUEGOS · ACCESORIOS · CUENTAS'))}
 <p class="lead c">Portadas en una sola tinta (escala de grises), para que el rojo y el azul queden alrededor, nunca mezclados con la imagen. El precio siempre dice «Consultar precio».</p>
 <div data-row="plataformas" data-title="Consolas y PC"></div>
 <div data-row="juegos" data-title="Aventura y plataformas"></div>
</section>
{corte('cuerda')}

<section class="sec" id="streaming" aria-labelledby="h-str">
 {banda(2, 'Suscripciones', 'Series, cine', 'y música', 'h-str')}
 {estampa('streaming', T('SERIES · CINE · MÚSICA · ANIME · EN PANTALLA GRANDE'))}
 <p class="lead c">Plataformas de series, cine y música con su logo en una tarjeta limpia. Consulta el precio y cotiza por WhatsApp.</p>
 <div data-row="streaming" data-title="Streaming"></div>
</section>
{corte('estrias')}

<section class="sec" id="ia" aria-labelledby="h-ia">
 {banda(3, 'IA y tecnología', 'Inteligencia', 'artificial', 'h-ia')}
 {estampa('ia', T('REDES NEURONALES · ASISTENTES · PRIVACIDAD · NODOS'))}
 <p class="lead c">Herramientas de IA y privacidad en la misma fila deslizable.</p>
 <div data-row="ia" data-title="Herramientas de IA"></div>
</section>
{corte('constela')}

<section class="sec sellos" id="sellos" aria-labelledby="h-sel">
 <div class="rosa" aria-hidden="true"><img class="ly bk" data-speed=".03" src="assets/planos/sellos.svg" alt="" draggable="false"></div>
 {banda(4, 'Galería', 'Sellos', 'de colección', 'h-sel')}
 <p class="lead c">Siluetas rojas de mando, de línea y de masa: un trazo grueso y un contorno negro que las separa del azul. Son íconos estilizados, sin personajes ni marcas escritas.</p>
 <ul class="seals">{sellos}</ul>
</section>
{corte('ondas')}

<section class="sec" id="marca" aria-labelledby="h-logo">
 {banda(5, 'Logo', 'El logo,', 'en su placa', 'h-logo')}
 {estampa('logo', T('LETRAS DE PINCEL · CIAN A AZUL · CONTORNO MAGENTA SOLO EN SU PLACA'))}
 <p class="lead c">Letras itálicas de pincel, relleno de cian a azul y contorno magenta. Ese contorno vive solo aquí, dentro de su placa. Fuera de ella no existe. Vectorial (SVG) y PNG sin fondo.</p>
 <div class="plates">
  <div class="plate big-plate dk"><span class="lbl">Sobre oscuro</span><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="Logo GameMaster sobre fondo oscuro" loading="lazy"></div>
  <div class="plate big-plate lt"><span class="lbl">Sobre claro</span><img src="assets/logo/gamemaster-completo-claro.svg" alt="Logo GameMaster sobre fondo claro" loading="lazy"></div>
  <div class="plate sm-plate dk"><img src="assets/logo/gamemaster-horizontal-oscuro.svg" alt="Logo horizontal" loading="lazy"><span class="lbl">Horizontal</span></div>
  <div class="plate sm-plate dk"><img src="assets/logo/gamemaster-compacto-oscuro.svg" alt="Icono GM" loading="lazy"><span class="lbl">Icono GM</span></div>
  <div class="plate sm-plate dk"><img src="assets/logo/gamemaster-completo-mono-blanco.svg" alt="Logo monocromo blanco" loading="lazy"><span class="lbl">Mono blanco</span></div>
  <div class="plate sm-plate lt"><img src="assets/logo/gamemaster-completo-mono-noche.svg" alt="Logo monocromo azul noche" loading="lazy"><span class="lbl">Mono noche</span></div>
 </div>
 <div class="dl"><a href="assets/logo/gamemaster-completo-oscuro.svg">SVG completo oscuro</a><a href="assets/logo/gamemaster-completo-claro.svg">SVG completo claro</a><a href="assets/logo/gamemaster-completo-oscuro-1024.png">PNG 1024 sin fondo</a><a href="assets/logo/gamemaster-horizontal-oscuro-512.png">PNG horizontal 512</a><a href="assets/logo/gamemaster-compacto-oscuro-512.png">PNG icono 512</a></div>
</section>
{corte('abanico')}

<section class="sec" id="cromo" aria-labelledby="h-cromo">
 {banda(6, 'Sistema cromo', 'Rojo al frente,', 'azul atrás', 'h-cromo')}
 {estampa('sistema', T('ROJO AL FRENTE · NEGRO AL MEDIO · AZUL ATRÁS'))}
 <div class="planes">
  <div class="pl pr"><b>Frente</b><p>Rojo. Un sello grande por sección y piezas pequeñas alrededor.</p><small>15 %</small></div>
  <div class="pl pk"><b>Medio</b><p>Negro. El hueco del medallón, el aire y el texto en hielo.</p><small>60 %</small></div>
  <div class="pl pb"><b>Fondo</b><p>Azul. Solo líneas finas de grabado: roseta, curvas de nivel, olas, rayos.</p><small>25 %</small></div>
 </div>
 <div class="rules">
  <div><b>I</b><p>Base negra. El azul nunca rellena secciones: son líneas finas.</p></div>
  <div><b>II</b><p>Un objeto, una geometría: rojo o azul, nunca los dos.</p></div>
  <div><b>III</b><p>Bordes nítidos: sin blur, glow ni sombras.</p></div>
  <div><b>IV</b><p>Texto en hielo o negro; nunca rojo sobre azul.</p></div>
 </div>
 <div class="swatches">
  <div class="sw" style="background:#050505;color:#F4F4EF;outline:1px solid #1616FF;outline-offset:-1px"><span>Negro<br>#050505</span></div>
  <div class="sw" style="background:#0B0B0D;color:#F4F4EF;outline:1px solid #1616FF;outline-offset:-1px"><span>Casi negro<br>#0B0B0D</span></div>
  <div class="sw" style="background:#1616FF;color:#F4F4EF"><span>Azul<br>#1616FF</span></div>
  <div class="sw" style="background:#FF1A1A;color:#050505"><span>Rojo<br>#FF1A1A</span></div>
  <div class="sw" style="background:#F4F4EF;color:#050505"><span>Hielo<br>#F4F4EF</span></div>
 </div>
 <div class="types">
  <div><span class="mono">Display · Bodoni Moda</span><div class="sp s1">Game Master Ñ7</div><p>Serif de alto contraste, estilo billete, en mayúsculas con itálica para la segunda línea. Siempre hielo.</p></div>
  <div><span class="mono">Texto · IBM Plex Sans Condensed</span><div class="sp s2">Aa Ññ 0123</div><p>Grotesca estrecha para párrafos, nombres y botones. 400 y 700.</p></div>
  <div><span class="mono">Etiquetas · IBM Plex Mono</span><div class="sp s3">N.º VII</div><p>Números romanos y pies de pieza, en mayúsculas.</p></div>
 </div>
</section>
{corte('estrias')}

<section class="sec" id="cortes" aria-labelledby="h-cut">
 {banda(7, 'Cortes de sección', 'Cinco', 'grabados', 'h-cut')}
 <p class="lead c">Cada corte es una cinta de grabado fino, de un solo color azul sobre negro. Ninguno se repite: ondas entrelazadas, abanicos, cuerda, estrías y constelación.</p>
 <div class="cutdemo">
  <figure>{corte('ondas')}<figcaption><b>Ondas</b> · guilloché entrelazado</figcaption></figure>
  <figure>{corte('abanico')}<figcaption><b>Abanico</b> · escamas concéntricas</figcaption></figure>
  <figure>{corte('cuerda')}<figcaption><b>Cuerda</b> · trenza fina</figcaption></figure>
  <figure>{corte('estrias')}<figcaption><b>Estrías</b> · haz que crece y se afina</figcaption></figure>
  <figure>{corte('constela')}<figcaption><b>Constelación</b> · estrellas unidas</figcaption></figure>
 </div>
</section>

<section class="sec closing" id="contacto" aria-labelledby="h-wa">
 {banda(8, 'Contacto', 'Cotiza por', 'WhatsApp', 'h-wa')}
 {estampa('cierre', T('GAMEMASTER · COTIZA POR WHATSAPP · 55 2769 9426'))}
 <div class="cta mid"><a class="btn red xl" href="{WA}" rel="noopener">55 2769 9426 →</a><span class="fine">Precios: siempre «Consultar precio».</span></div>
</section>
</main>
<footer class="foot"><p>Propuesta v9a «Grabado» · página estática, sin build ni CDN. Las marcas de terceros pertenecen a sus dueños.</p><a href="#inicio">Volver arriba ↑</a></footer>
<script src="app.js"></script>
</body></html>
'''
open(OUT, 'w').write(H); print('index.html', len(H))
