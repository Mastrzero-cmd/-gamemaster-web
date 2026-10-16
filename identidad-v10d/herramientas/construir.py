#!/usr/bin/env python3
"""Construye identidad-v9d/index.html (HTML estático). Uso: python3 construir.py"""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'index.html')
WA = 'https://wa.me/525527699426'
import json
SL = json.load(open(os.path.join(os.path.dirname(__file__), 'slots.json')))
VBX, VBY, VBW, VBH = -172.8, -108.0, 1785.6, 1116.0
def slots_html(sec, capa):
    out = ''
    for s in SL.get(sec, {}).get(capa, []):
        out += (f'<span class="slot" data-slot="{s["name"]}" data-forma="{s["forma"]}" style="left:{(s["x"]-VBX)/VBW*100:.2f}%;top:{(s["y"]-VBY)/VBH*100:.2f}%;'
                f'width:{s["size"]/VBW*100:.2f}%;rotate:{s["rot"]}deg"></span>')
    return out
def stage(es, cls='', frame='', extra=''):
    return (f'<figure class="stage {cls}" aria-hidden="true"><div class="box"><div class="frame {frame}"><img class="ly bk" data-speed=".02" src="assets/planos/{es}.svg" alt="" draggable="false">'
            f'<img class="ly md" data-speed=".08" src="assets/medios/{es}.svg" alt="" draggable="false"></div>{extra}'
            f'<div class="ly fr" data-speed=".30"><img src="assets/heroes/{es}.svg" alt="" draggable="false">{slots_html(es, "fr")}</div>'
            f'<div class="ly pc" data-speed=".55"><img src="assets/piezas/{es}.svg" alt="" draggable="false">{slots_html(es, "pc")}</div></div></figure>')
def corte(n): return f'<div class="corte c-{n}" aria-hidden="true"><img src="assets/cortes/{n}.svg" alt="" draggable="false"></div>'
def num(n, lab): return f'<p class="num"><b>{n}</b><span>{lab}</span></p>'
MARCAS = [('Netflix', 'netflix'), ('HBO Max', 'hbomax'), ('Max', 'max'), ('Spotify', 'spotify'), ('YouTube', 'youtube'), ('YouTube Music', 'youtubemusic'), ('Crunchyroll', 'crunchyroll'), ('Apple TV', 'appletv'), ('PlayStation', 'playstation'), ('Steam', 'steam'), ('Claude', 'claude'), ('Anthropic', 'anthropic'), ('Google Gemini', 'googlegemini'), ('Proton', 'proton'), ('Proton VPN', 'protonvpn'), ('Twitch', 'twitch'), ('Discord', 'discord')]
tiles = ''.join(f'<li><span class="disc"><img src="assets/logos-mono/{f}_mono_hielo.svg" alt="" width="44" height="44" loading="lazy" draggable="false"></span><em>{n}</em></li>' for n, f in MARCAS)
ICONOS = [('corazon', 'Corazón'), ('espada', 'Espada legendaria'), ('pokebola', 'Bola de captura'), ('mando', 'Mando'), ('tv', 'Tele retro'), ('play', 'Play'), ('robot', 'Robot IA'), ('destello', 'Destello IA')]
pan = ''.join(f'<li><span class="chapa"><img src="assets/iconos/{f}.svg" alt="" width="120" height="120" loading="lazy" draggable="false"></span><em>{n}</em></li>' for f, n in ICONOS)
pan += ''.join(f'<li><span class="chapa"><span class="slot fijo" data-slot="personaje-ejemplo-{f}" data-forma="{f}"></span></span><em>Espacio · {n}</em></li>' for f, n in [('blob', 'blob'), ('cuadro', 'cuadro'), ('triangulo', 'triángulo'), ('anillo', 'anillo'), ('estrella', 'estrella'), ('fantasma', 'fantasma')])
ARC = '''<svg class="arco-txt" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><path id="arc1" d="M 720 450 m -392 0 a 392 392 0 1 1 784 0"/></defs><text><textPath href="#arc1" startOffset="50%" text-anchor="middle">Juegos ✦ Streaming ✦ IA</textPath></text></svg>'''
H = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GameMaster · Identidad v10d: Póster psicodélico</title>
<meta name="description" content="Propuesta v9d de identidad visual de GameMaster: cartel psicodélico de los 60-70 con cromoestereopsis (rojo al frente, negro al medio, azul atrás).">
<link rel="preload" href="assets/fonts/Shrikhand-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css"></head><body>
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="bar"><a class="brand" href="#inicio" aria-label="GameMaster, inicio"><img src="assets/logo/gamemaster-compacto-mono-blanco.svg" alt="GameMaster" width="40" height="40"></a>
<nav class="nav" aria-label="Secciones"><a href="#marcas">Marcas</a><a href="#catalogo">Catálogo</a><a href="#streaming">Streaming</a><a href="#ia">IA</a><a href="#marca">Logo</a><a href="#sistema">Sistema</a></nav>
<a class="btn red" href="{WA}" rel="noopener">Cotizar</a></header>
<main id="contenido">

<section class="lam hero" id="inicio" aria-labelledby="h1">
 <div class="txt">
  <p class="kick">Videojuegos · Streaming · IA</p>
  <h1 id="h1" class="pila"><span class="a">Todo tu</span><span class="b">universo</span><span class="c">digital</span></h1>
  <p class="lead">Elige, consulta el precio y cotiza por WhatsApp. Un solo lugar para tus juegos, tus series y tus herramientas de inteligencia artificial.</p>
  <div class="cta"><a class="btn red" href="#catalogo">Ver catálogo →</a><a class="btn line" href="{WA}" rel="noopener">Hablar por WhatsApp</a></div>
  <div class="plate logoplate"><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="GameMaster" width="200" height="140"></div>
 </div>
 {stage('inicio', 'st-hero', 'f-arco', ARC)}
</section>
{corte('cupula')}

<section class="lam" id="marcas" aria-labelledby="h-marcas">
 <div class="txt wide">{num('01', 'Marcas')}<h2 id="h-marcas" class="pila"><span class="a">Diecisiete</span><span class="b">marcas</span><span class="c">en una ola</span></h2>
 <p class="lead">Logos de un solo tono, sin fondo ni color de marca: así la página sigue leyéndose negra.</p></div>
 {stage('marcas', 'st-marcas', 'f-ola')}
 <ul class="tiles" aria-label="Marcas disponibles">{tiles}</ul>
 <p class="fine">Las marcas pertenecen a sus dueños y se usan solo para identificar el servicio.</p>
</section>
{corte('ola')}

<section class="lam rev" id="catalogo" aria-labelledby="h-cat">
 {stage('juegos', 'st-juegos', 'f-hoja')}
 <div class="txt">{num('02', 'Catálogo')}<h2 id="h-cat" class="pila"><span class="a">Consolas</span><span class="b">y juegos</span><span class="c">a tu medida</span></h2>
 <p class="lead">Portadas originales, tal cual. El rojo y el azul quedan alrededor, nunca encima. El precio siempre dice «Consultar precio».</p></div>
 <div class="rows"><div data-row="plataformas" data-title="Consolas y PC"></div><div data-row="juegos" data-title="Aventura y plataformas"></div></div>
</section>
{corte('festones')}

<section class="lam" id="streaming" aria-labelledby="h-str">
 <div class="txt">{num('03', 'Suscripciones')}<h2 id="h-str" class="pila"><span class="a">Series,</span><span class="b">cine</span><span class="c">y música</span></h2>
 <p class="lead">Plataformas de series, cine y música con su logo en una tarjeta limpia. Consulta el precio y cotiza por WhatsApp.</p></div>
 {stage('streaming', 'st-str', 'f-ojo')}
 <div class="rows"><div data-row="streaming" data-title="Streaming"></div></div>
</section>
{corte('gota')}

<section class="lam rev" id="ia" aria-labelledby="h-ia">
 {stage('ia', 'st-ia', 'f-arco2')}
 <div class="txt">{num('04', 'IA y tecnología')}<h2 id="h-ia" class="pila"><span class="a">Inteligencia</span><span class="b">artificial</span><span class="c">con alma</span></h2>
 <p class="lead">Herramientas de IA y privacidad en la misma fila deslizable.</p></div>
 <div class="rows"><div data-row="ia" data-title="Herramientas de IA"></div></div>
</section>
{corte('sol')}

<section class="lam" id="marca" aria-labelledby="h-logo">
 <div class="txt">{num('05', 'Logo')}<h2 id="h-logo" class="pila"><span class="a">El logo,</span><span class="b">en su</span><span class="c">placa</span></h2>
 <p class="lead">Letras itálicas de pincel, relleno de cian a azul y contorno magenta. Ese contorno vive solo aquí, dentro de su placa. Fuera de ella no existe. Vectorial (SVG) y PNG sin fondo.</p>
 <div class="dl"><a href="assets/logo/gamemaster-completo-oscuro.svg">SVG completo oscuro</a><a href="assets/logo/gamemaster-completo-claro.svg">SVG completo claro</a><a href="assets/logo/gamemaster-completo-oscuro-1024.png">PNG 1024 sin fondo</a><a href="assets/logo/gamemaster-horizontal-oscuro-512.png">PNG horizontal 512</a><a href="assets/logo/gamemaster-compacto-oscuro-512.png">PNG icono 512</a></div></div>
 {stage('logo', 'st-logo', 'f-ojo')}
 <div class="plates">
  <div class="plate big dk"><span class="lbl">Sobre oscuro</span><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="Logo GameMaster sobre fondo oscuro" loading="lazy"></div>
  <div class="plate big lt"><span class="lbl">Sobre claro</span><img src="assets/logo/gamemaster-completo-claro.svg" alt="Logo GameMaster sobre fondo claro" loading="lazy"></div>
  <div class="plate sm dk"><img src="assets/logo/gamemaster-horizontal-oscuro.svg" alt="Logo horizontal" loading="lazy"><span class="lbl">Horizontal</span></div>
  <div class="plate sm dk"><img src="assets/logo/gamemaster-compacto-oscuro.svg" alt="Icono GM" loading="lazy"><span class="lbl">Icono GM</span></div>
  <div class="plate sm dk"><img src="assets/logo/gamemaster-completo-mono-blanco.svg" alt="Logo monocromo blanco" loading="lazy"><span class="lbl">Mono blanco</span></div>
  <div class="plate sm lt"><img src="assets/logo/gamemaster-completo-mono-noche.svg" alt="Logo monocromo azul noche" loading="lazy"><span class="lbl">Mono noche</span></div>
 </div>
</section>
{corte('cupula')}

<section class="lam sis" id="sistema" aria-labelledby="h-sis">
 <div class="bgondas" aria-hidden="true"><img class="ly bk" data-speed=".02" src="assets/planos/sistema.svg" alt="" draggable="false"></div>
 <div class="txt wide">{num('06', 'Sistema cromo')}<h2 id="h-sis" class="pila"><span class="a">Rojo al frente,</span><span class="b">azul atrás</span></h2>
 <p class="lead">Tres planos con papeles distintos, separados por negro. Nada de copias desplazadas, brillos ni degradados: cada forma es de un solo color y de un solo plano.</p></div>
 <div class="planes">
  <div class="pl pr"><b>Frente</b><p>Rojo. Íconos y trazos gigantes que rompen el marco.</p><small>12 %</small></div>
  <div class="pl pk"><b>Medio</b><p>Negro. Aire, lectura y texto en hielo.</p><small>62 %</small></div>
  <div class="pl pb"><b>Fondo</b><p>Azul. Ondas, rayos, ornamento y grabado.</p><small>26 %</small></div>
 </div>
 <h3 class="sub">Objetos rojos y espacios de personaje</h3>
 <ul class="pan">{pan}</ul>
 <h3 class="sub">Cortes de sección</h3>
 <div class="cutdemo">
  <figure>{corte('cupula')}<figcaption>Cúpula</figcaption></figure><figure>{corte('ola')}<figcaption>Ola</figcaption></figure><figure>{corte('festones')}<figcaption>Festones</figcaption></figure><figure>{corte('gota')}<figcaption>Gotas</figcaption></figure><figure>{corte('sol')}<figcaption>Sol naciente</figcaption></figure>
 </div>
 <h3 class="sub">Paleta y tipografía</h3>
 <div class="swatches">
  <div class="sw" style="background:#050505;color:#F4F4EF;box-shadow:inset 0 0 0 2px #1616FF"><span>Negro<br>#050505</span></div>
  <div class="sw" style="background:#0B0B0D;color:#F4F4EF;box-shadow:inset 0 0 0 2px #1616FF"><span>Casi negro<br>#0B0B0D</span></div>
  <div class="sw" style="background:#1616FF;color:#F4F4EF"><span>Azul<br>#1616FF</span></div>
  <div class="sw" style="background:#FF1A1A;color:#050505"><span>Rojo<br>#FF1A1A</span></div>
  <div class="sw" style="background:#F4F4EF;color:#050505"><span>Hielo<br>#F4F4EF</span></div>
 </div>
 <div class="types">
  <div><span class="mono">Display · Shrikhand</span><div class="sp s1">Game<br>Master Ñ7</div><p>Letra gruesa y redondeada de cartel de gira, apilada y a veces curva. Siempre hielo; el contorno, solo en hielo.</p></div>
  <div><span class="mono">Texto · Josefin Sans</span><div class="sp s2">Aa Ññ 0123</div><p>Geométrica de aire art nouveau para párrafos, nombres y botones. 400 a 700.</p></div>
 </div>
 <div class="rules"><div><b>01</b><p>Base negra. El azul nunca rellena secciones completas.</p></div><div><b>02</b><p>Un objeto, una geometría: rojo o azul, nunca los dos.</p></div><div><b>03</b><p>Bordes nítidos: sin blur, glow ni sombras.</p></div><div><b>04</b><p>Texto en hielo o negro; nunca rojo sobre azul.</p></div></div>
</section>

<section class="lam cierre" id="contacto" aria-labelledby="h-wa">
 {stage('contacto', 'st-con', 'f-ojo')}
 <div class="txt wide">{num('07', 'Contacto')}<h2 id="h-wa" class="pila"><span class="a">Cotiza por</span><span class="b">WhatsApp</span></h2>
 <div class="cta"><a class="btn red big" href="{WA}" rel="noopener">55 2769 9426 →</a></div><p class="fine">Precios: siempre «Consultar precio».</p></div>
</section>
</main>
<script src="app.js"></script></body></html>'''
import re
def _n(m):
    a, b, c = m.group(3), m.group(4), m.group(6) or ''
    n = max(len(b), len(c) * .8, len(a) * .42, 5)
    return f'<{m.group(1)} id="{m.group(2)}" class="pila" style="--n:{n:.1f}"><span class="a">{a}</span><span class="b">{b}</span>' + (f'<span class="c">{c}</span>' if m.group(6) else '') + f'</{m.group(1)}>'
H = re.sub(r'<(h1|h2) id="([\w-]+)" class="pila"><span class="a">(.*?)</span><span class="b">(.*?)</span>(<span class="c">(.*?)</span>)?</h[12]>', _n, H)
open(OUT, 'w', encoding='utf-8').write(H)
