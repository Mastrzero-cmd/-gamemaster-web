#!/usr/bin/env python3
"""Construye ../index.html (HTML estático) de v9b «Arcade-técnico». Uso: python3 construir.py"""
import os
ROOT = os.path.join(os.path.dirname(__file__), '..')
WA = 'https://wa.me/525527699426'
NAV = [('marcas', 'Marcas'), ('catalogo', 'Catálogo'), ('streaming', 'Streaming'), ('ia', 'IA'), ('marca', 'Logo'), ('sistema', 'Sistema'), ('cortes', 'Cortes')]
H = []
def stage(k, cls=''):
    return f'<figure class="stage {cls}" aria-hidden="true"><img class="ly bk" data-speed=".03" src="assets/planos/{k}.svg" alt="" draggable="false"><img class="ly fr" data-speed=".10" src="assets/heroes/{k}.svg" alt="" draggable="false"><img class="ly pc" data-speed=".22" src="assets/piezas/{k}.svg" alt="" draggable="false"></figure>'
def cut(k, pellets=False):
    p = '<img class="ly pc" data-speed=".22" src="assets/piezas/corte-pellets.svg" alt="" draggable="false">' if pellets else ''
    return f'<div class="cut" aria-hidden="true"><img class="ly bk" data-speed=".03" src="assets/planos/corte-{k}.svg" alt="" draggable="false">{p}</div>'
def lvl(n, name, total=9):
    return f'<header class="lvl"><span class="lv">NIVEL 1-{n}</span><span class="nm">{name}</span><i class="dash"></i><span class="st">PANTALLA {n:02d}/{total:02d}</span></header>'
def sec(id_, n, name, k, title, lead, extra='', body='', dlgx='', cls=''):
    return f'''<section class="sec {cls}" id="{id_}" data-nivel="1-{n}" data-name="{name}" aria-labelledby="h-{id_}">
{lvl(n, name)}
<div class="cab"><span class="tag">JUGADOR 1</span>{stage(k)}
<div class="dlg"><div class="dtext"><h2 id="h-{id_}" class="disp">{title}</h2><p class="lead">{lead}</p>{extra}</div>{dlgx}<img class="dsp" src="assets/piezas/dlg-{id_}.svg" alt="" aria-hidden="true" draggable="false"></div></div>
{body}
</section>'''
LOGOS = [('Netflix', 'netflix', 'Series y cine'), ('HBO Max', 'hbomax', 'Series y cine'), ('Max', 'max', 'Streaming (histórico)'), ('Spotify', 'spotify', 'Música'), ('YouTube', 'youtube', 'Video'), ('YouTube Music', 'youtubemusic', 'Música'), ('Crunchyroll', 'crunchyroll', 'Anime'), ('Apple TV', 'appletv', 'Streaming'), ('PlayStation', 'playstation', 'Videojuegos'), ('Steam', 'steam', 'Videojuegos'), ('Twitch', 'twitch', 'En vivo'), ('Discord', 'discord', 'Comunidad'), ('Claude', 'claude', 'Inteligencia artificial'), ('Anthropic', 'anthropic', 'Inteligencia artificial'), ('Google Gemini', 'googlegemini', 'Inteligencia artificial'), ('Proton', 'proton', 'Privacidad'), ('Proton VPN', 'protonvpn', 'Privacidad')]
score = ''.join(f'<li><span class="rk">{i + 1:02d}</span><img src="assets/logos-mono/{k}_mono_hielo.svg" alt="" width="30" height="30" loading="lazy" draggable="false"><span class="nmx">{n}</span><i class="lead-dots"></i><span class="cat">{c}</span></li>' for i, (n, k, c) in enumerate(LOGOS))

head = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GameMaster · Identidad v9b «Arcade-técnico»</title>
<meta name="description" content="Propuesta de identidad visual v9b para GameMaster: cabina arcade con HUD, sprites rojos al frente y arte azul de ondas, constelaciones y circuitos.">
<link rel="preload" href="assets/fonts/silkscreen-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css"></head><body>
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="hud" id="hud"><a class="brand" href="#inicio" aria-label="GameMaster, inicio"><img src="assets/logo/gamemaster-horizontal-mono-blanco.svg" alt="GameMaster" width="116" height="30"></a>
<div class="stats" aria-hidden="true"><span class="hl">PUNTOS <b id="score">000000</b></span><span class="hl">NIVEL <b id="nivel">1-0</b></span><span class="lives"><img src="assets/piezas/sprite-corazon.svg" alt="" width="22" height="22"><img src="assets/piezas/sprite-corazon.svg" alt="" width="22" height="22"><img src="assets/piezas/sprite-corazon.svg" alt="" width="22" height="22"></span></div>
<nav class="nav" aria-label="Secciones">{''.join(f'<a href="#{i}">{t}</a>' for i, t in NAV)}</nav>
<a class="btn red" href="{WA}" rel="noopener">Cotizar</a></header>
<main id="contenido">
'''
H.append(head)
# 0 inicio
H.append(f'''<section class="sec hero" id="inicio" data-nivel="1-0" data-name="Inicio" aria-labelledby="h1">
<p class="insert"><span class="blink">▶ INSERTA MONEDA</span><span>1 JUGADOR</span><span>CRÉDITOS 01</span></p>
<div class="cab big"><span class="tag">JUGADOR 1</span>{stage('inicio', 'tall')}
<div class="dlg hero-dlg"><div class="dtext"><h1 id="h1" class="disp mega">GAME<br>MASTER</h1><p class="sub">Todo tu universo digital</p><p class="lead">Videojuegos, streaming e inteligencia artificial en un solo lugar. Elige, consulta el precio y cotiza por WhatsApp.</p>
<div class="cta"><a class="btn red" href="#catalogo">Ver catálogo ▶</a><a class="btn line" href="{WA}" rel="noopener">Hablar por WhatsApp</a></div></div>
<div class="logoplate"><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="Logo de GameMaster" width="300" height="210"></div></div></div>
</section>
''')
H.append(cut('onda'))
# 1 marcas
H.append(sec('marcas', 1, 'Marcas', 'marcas', '17 marcas<br>un solo lugar', 'Tabla de puntuaciones de los servicios que consigues aquí. Logos de una sola tinta, sin fondo y sin color de marca, para que la página se siga leyendo negra.', body=f'''<div class="board"><p class="cap">★ TABLA DE SERVICIOS ★</p><ol class="score">{score}</ol><p class="fine">Las marcas pertenecen a sus dueños y se usan solo para identificar el servicio.</p></div>'''))
H.append(cut('constelacion', pellets=True))
# 2 catalogo
H.append(sec('catalogo', 2, 'Catálogo', 'catalogo', 'Elige tu<br>juego', 'Portadas en fila, una tarjeta por juego. El precio siempre dice «Consultar precio» y la cotización va por WhatsApp.', body='<div class="rowzone"><div data-row="juegos" data-title="SELECCIONA JUEGO"></div><div data-row="plataformas" data-title="CONSOLAS Y PC"></div></div>'))
H.append(cut('ecualizador'))
H.append(sec('streaming', 3, 'Streaming', 'streaming', 'Series, cine<br>y música', 'Plataformas de series, cine y música con su logo de una sola tinta. Consulta el precio y cotiza por WhatsApp.', body='<div class="rowzone"><div data-row="streaming" data-title="CANALES EN SEÑAL"></div></div>'))
H.append(cut('latido'))
H.append(sec('ia', 4, 'Inteligencia artificial', 'ia', 'IA y<br>tecnología', 'Herramientas de inteligencia artificial y privacidad en la misma fila deslizable, con nodos, circuitos y señal de fondo.', body='<div class="rowzone"><div data-row="ia" data-title="MÓDULOS DE IA"></div></div>'))
H.append(cut('circuito'))
# 5 logo
H.append(f'''<section class="sec" id="marca" data-nivel="1-5" data-name="Logo" aria-labelledby="h-marca">
{lvl(5, 'Logo')}
<div class="cab"><span class="tag">JUGADOR 1</span>{stage('logo')}
<div class="dlg"><img class="dsp" src="assets/piezas/dlg-logo.svg" alt="" aria-hidden="true" draggable="false"><div class="dtext"><h2 id="h-marca" class="disp">El logo<br>en su placa</h2><p class="lead">El logo de Fernando (pincel cian-azul con contorno magenta) vive solo dentro de su placa, sobre fondo neutro. Se usa tal cual: sin recolorear, sin copias desplazadas.</p></div></div></div>
<div class="plates"><div class="plate dk"><span class="lbl">SOBRE OSCURO</span><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="Logo GameMaster sobre fondo oscuro" width="320" height="224" loading="lazy"></div><div class="plate lt"><span class="lbl">SOBRE CLARO</span><img src="assets/logo/gamemaster-completo-claro.svg" alt="Logo GameMaster sobre fondo claro" width="320" height="224" loading="lazy"></div>
<div class="plate sm dk"><img src="assets/logo/gamemaster-horizontal-oscuro.svg" alt="Logo horizontal" width="220" height="60" loading="lazy"><span class="lbl">HORIZONTAL</span></div><div class="plate sm dk"><img src="assets/logo/gamemaster-compacto-oscuro.svg" alt="Icono GM" width="96" height="96" loading="lazy"><span class="lbl">ICONO GM</span></div><div class="plate sm dk"><img src="assets/logo/gamemaster-completo-mono-blanco.svg" alt="Logo monocromo blanco" width="120" height="84" loading="lazy"><span class="lbl">MONO BLANCO</span></div></div>
</section>
''')
H.append(cut('cuadrada'))
# 6 sistema
def meter(cls, n, label, pct):
    on = round(20 * pct / 100); return f'<div class="meter {cls}"><span class="ml">{label}</span><span class="bar">{"".join("<i class=on></i>" if i < on else "<i></i>" for i in range(20))}</span><span class="mp">{pct}%</span></div>'
H.append(f'''<section class="sec" id="sistema" data-nivel="1-6" data-name="Sistema" aria-labelledby="h-sistema">
{lvl(6, 'Sistema cromo')}
<div class="cab"><span class="tag">JUGADOR 1</span>{stage('sistema')}
<div class="dlg"><div class="dtext"><h2 id="h-sistema" class="disp">Rojo al frente<br>azul atrás</h2><p class="lead">Tres planos en regiones separadas por negro. Una forma, un solo color: ningún objeto mezcla rojo y azul, y no hay brillos, degradados ni copias desplazadas.</p></div>
<div class="meters" role="img" aria-label="Proporción objetivo: 15 % rojo, 60 % negro, 25 % azul">{meter('mr', 0, 'FRENTE · ROJO', 15)}{meter('mk', 0, 'MEDIO · NEGRO', 60)}{meter('mb', 0, 'FONDO · AZUL', 25)}</div><img class="dsp" src="assets/piezas/dlg-sistema.svg" alt="" aria-hidden="true" draggable="false"></div></div>
<div class="rules"><div><b>01</b><p>Base negra. El azul no rellena secciones.</p></div><div><b>02</b><p>Una imagen, una geometría: rojo o azul, nunca ambos.</p></div><div><b>03</b><p>Bordes nítidos: sin blur, glow ni sombras.</p></div><div><b>04</b><p>Texto en hielo o negro; nunca rojo sobre azul.</p></div></div>
<div class="swatches"><div class="sw" style="background:#050505;color:#F4F4EF;border:3px solid #1616FF"><span>NEGRO<br>#050505</span></div><div class="sw" style="background:#0B0B0D;color:#F4F4EF;border:3px solid #1616FF"><span>CASI NEGRO<br>#0B0B0D</span></div><div class="sw" style="background:#1616FF;color:#F4F4EF"><span>AZUL<br>#1616FF</span></div><div class="sw" style="background:#FF1A1A;color:#050505"><span>ROJO<br>#FF1A1A</span></div><div class="sw" style="background:#F4F4EF;color:#050505"><span>HIELO<br>#F4F4EF</span></div></div>
<div class="types"><div><span class="mono">DISPLAY · SILKSCREEN</span><p class="sp s1">GAME MASTER Ñ7</p><p>Pixel de pantalla para titulares y marcadores. Siempre en hielo.</p></div><div><span class="mono">TEXTO · PIXELIFY SANS</span><p class="sp s2">Aa Ññ 0123 ¿?¡!</p><p>Párrafos, nombres y botones. 400 y 700.</p></div><div><span class="mono">HUD · VT323</span><p class="sp s3">PUNTOS 004200 · NIVEL 1-6</p><p>Contadores y etiquetas de cabina.</p></div></div>
<div class="speeds-wrap"><p class="cap">PARALLAX · 3 CAPAS</p><ol class="speeds"><li><i class="r"></i>Sprites sueltos · 0.22</li><li><i class="r"></i>Masa roja · 0.10</li><li><i class="b"></i>Plano azul · 0.03</li></ol><p class="fine">El azul, al fondo, casi no se mueve; el rojo, más cerca, se mueve más. Con «reducir movimiento» todo se queda quieto.</p></div>
</section>
''')
H.append(cut('constelacion'))
# 7 cortes
CUTN = [('onda', 'ONDA', 'Senoidal, oscilador'), ('cuadrada', 'CUADRADA', 'Pulsos de reloj'), ('ecualizador', 'ECUALIZADOR', 'Barras de nivel'), ('constelacion', 'CONSTELACIÓN', 'Estrellas y enlaces'), ('latido', 'LATIDO', 'Pulso de vida'), ('circuito', 'CIRCUITO', 'Trazas y nodos')]
H.append(f'''<section class="sec" id="cortes" data-nivel="1-7" data-name="Cortes" aria-labelledby="h-cortes">
{lvl(7, 'Cortes de pantalla')}
<h2 id="h-cortes" class="disp sm">Siete cortes,<br>siete señales</h2><p class="lead wide">Cada salto de pantalla tiene su propio trazo azul: ondas, pulsos, barras, estrellas, latidos y circuitos. En el primero corre una fila de puntos rojos con su comecocos.</p>
<div class="cutdemo">{''.join(f'<figure><div class="cutbox"><img src="assets/planos/corte-{k}.svg" alt="" width="1440" height="120" loading="lazy" draggable="false"></div><figcaption><b>{n}</b> · {d}</figcaption></figure>' for k, n, d in CUTN)}<figure><div class="cutbox"><img src="assets/piezas/corte-pellets.svg" alt="" width="1440" height="120" loading="lazy" draggable="false"></div><figcaption><b>PUNTOS</b> · Comecocos y fila de puntos</figcaption></figure></div>
</section>
''')
H.append(cut('onda', pellets=True))
H.append(f'''<section class="sec closing" id="contacto" data-nivel="1-9" data-name="Contacto" aria-labelledby="h-wa">
{lvl(9, 'Contacto')}
<div class="cab"><span class="tag">JUGADOR 1</span>{stage('contacto')}
<div class="dlg"><div class="dtext"><h2 id="h-wa" class="disp">¿Continuar?<br><span class="count" id="count" aria-hidden="true">9</span></h2><p class="lead">Cotiza por WhatsApp y te respondemos con el precio. Precios: siempre «Consultar precio».</p><div class="cta"><a class="btn red" href="{WA}" rel="noopener">WhatsApp 55 2769 9426 ▶</a></div></div><img class="dsp" src="assets/piezas/dlg-contacto.svg" alt="" aria-hidden="true" draggable="false"></div></div>
</section>
</main>
<footer class="foot"><p>Propuesta v9b «Arcade-técnico» · página estática, sin build ni CDN. Las marcas de terceros pertenecen a sus dueños; los íconos de videojuegos son siluetas de píxel estilizadas, sin texto de marca.</p><a href="#inicio">Volver arriba ↑</a></footer>
<script src="app.js"></script>
</body></html>
''')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(''.join(H))
print('index.html', sum(len(x) for x in H))
