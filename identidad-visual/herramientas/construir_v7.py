#!/usr/bin/env python3
"""v7 · genera index.html: base negra, azul = plano trasero (planos + placas), rojo = una masa delantera por sección.
Uso: python3 construir_v7.py ../index.html"""
import sys
def sm(n, x, y, w, sp, r=0): return f'<div class="pz sm" data-speed="{sp}" style="--x:{x}%;--y:{y}%;--sw:{w}px;--r:{r}deg"><img src="assets/piezas/pieza-{n}.svg" alt="" draggable="false" loading="lazy"></div>'
def stage(hero, plate, smalls, cap, tag, r=0, bw=74, bx=-2, by=-9, hw=90, hsp=.1):
    return (f'<figure class="stage" aria-hidden="true" style="--bw:{bw}%;--bx:{bx}%;--by:{by}%;--hw:{hw}%"><span class="tag">{tag}</span>'
            f'<div class="bp" data-speed=".03"><img src="assets/placas/placa-{plate}.svg" alt="" draggable="false"></div>'
            f'<div class="pz hero" data-speed="{hsp}" style="--r:{r}deg"><img src="assets/heroes/heroe-{hero}.svg" alt="" draggable="false"></div>{"".join(smalls)}'
            f'<figcaption>{cap}</figcaption></figure>')
def head(no, label, total='10'): return f'<header class="plate-head"><span class="no">{no}</span><span class="lab">{label}</span><span class="rule"></span><span class="of">{no} / {total}</span></header>'
def fix(k): return f'<div class="fixbg" aria-hidden="true"><div class="fixin"><div class="art a-{k}"></div></div></div>'
CUT = lambda t, a, b: f'<div data-cut="{t}" data-from="{a}" data-to="{b}"></div>\n'
H = []
H.append('''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GameMaster · Identidad visual v7 (propuesta)</title>
<meta name="description" content="Propuesta v7 de identidad visual de GameMaster: cromoestereopsis con base negra, azul como plano trasero estructural y una masa roja delantera por sección.">
<link rel="stylesheet" href="styles.css"></head><body>
<header class="hdr"><div class="wrap"><a class="brand" href="#inicio" aria-label="GameMaster, inicio"><img src="assets/logo/gamemaster-horizontal-oscuro.svg" alt="GameMaster" width="130" height="34"></a>
<nav class="nav" aria-label="Secciones"><a href="#logo">Logo</a><a href="#paleta">Paleta</a><a href="#cromo">Cromo</a><a href="#grabado">Planos</a><a href="#parallax">Parallax</a><a href="#cortes">Cortes</a><a href="#filas">Filas</a><a href="#ej-catalogo">Ejemplo</a></nav>
<a class="btn" href="https://wa.me/525527699426" rel="noopener">Cotizar</a></div></header>
<main>
''')
H.append('''<section class="field hero-sec bg-k0" id="inicio" aria-labelledby="h1">
 ''' + fix('hero') + '''
 <div class="wrap g12">
  <div class="copy">
   <div class="logo-plate"><img class="logo-hero" src="assets/logo/gamemaster-completo-oscuro.svg" alt="GameMaster" width="560" height="392"></div>
   <h1 id="h1" class="disp">Todo tu universo <em>digital</em></h1>
   <p class="lead">Videojuegos, streaming e inteligencia artificial en un solo lugar. Elige, consulta el precio y cotiza por WhatsApp.</p>
   <div class="cta"><a class="btn" href="#ej-catalogo">Explorar catálogo →</a><a class="btn ghost" href="https://wa.me/525527699426" rel="noopener">Hablar por WhatsApp</a></div>
  </div>
  ''' + stage('mando', 'hero', [sm('estrella', 90, 4, 64, .2, 8)], 'Lámina 00', 'PS5 · Switch · PC', -5, bw=82, bx=-4, by=-12, hw=80) + '''
 </div>
</section>
''')
H.append(CUT('diag', 'k0', 'k1'))
H.append('''<section class="field bg-k1" id="logo">
 <div class="wrap">
  ''' + head('01', 'Logo') + '''
  <div class="g12 intro"><h2 class="disp">El logo, <em>solo</em></h2>
  <p class="lead">Letras itálicas de pincel, relleno cian a azul eléctrico, contorno magenta desplazado y la pincelada curva debajo. El contorno magenta vive solo aquí, dentro de su placa: en el resto de la web no existe. Vectorial (SVG) y PNG sin fondo.</p></div>
  <div class="logo-stage">
   <div class="osc"><span class="lbl">Sobre oscuro</span><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="Logo GameMaster sobre fondo oscuro"></div>
   <div class="cla"><span class="lbl">Sobre claro</span><img src="assets/logo/gamemaster-completo-claro.svg" alt="Logo GameMaster sobre fondo claro"></div>
  </div>
  <div class="variants">
   <div class="var osc"><img src="assets/logo/gamemaster-horizontal-oscuro.svg" alt="Logo horizontal"><small>Horizontal · oscuro</small></div>
   <div class="var cla"><img src="assets/logo/gamemaster-horizontal-claro.svg" alt="Logo horizontal sobre claro"><small>Horizontal · claro</small></div>
   <div class="var osc"><img src="assets/logo/gamemaster-compacto-oscuro.svg" alt="Icono GM"><small>Icono GM · oscuro</small></div>
   <div class="var cla"><img src="assets/logo/gamemaster-compacto-claro.svg" alt="Icono GM sobre claro"><small>Icono GM · claro</small></div>
   <div class="var osc"><img src="assets/logo/gamemaster-completo-mono-blanco.svg" alt="Logo monocromo blanco"><small>Mono blanco</small></div>
   <div class="var cla"><img src="assets/logo/gamemaster-completo-mono-noche.svg" alt="Logo monocromo azul noche"><small>Mono azul noche</small></div>
   <div class="var osc"><img src="assets/logo/gamemaster-compacto-mono-blanco.svg" alt="Icono monocromo blanco"><small>Icono mono · blanco</small></div>
   <div class="var cla"><img src="assets/logo/gamemaster-compacto-mono-noche.svg" alt="Icono monocromo azul noche"><small>Icono mono · noche</small></div>
  </div>
  <div class="dl"><a href="assets/logo/gamemaster-completo-oscuro.svg">SVG completo oscuro</a><a href="assets/logo/gamemaster-completo-claro.svg">SVG completo claro</a><a href="assets/logo/gamemaster-completo-oscuro-1024.png">PNG 1024 sin fondo</a><a href="assets/logo/gamemaster-horizontal-oscuro-512.png">PNG horizontal 512</a><a href="assets/logo/gamemaster-compacto-oscuro-512.png">PNG icono 512</a></div>
 </div>
</section>
''')
H.append(CUT('step', 'k1', 'k0'))
H.append('''<section class="field bg-k0" id="paleta">
 ''' + fix('paleta') + '''
 <div class="wrap">
  ''' + head('02', 'Paleta y tipos') + '''
  <div class="g12">
   <div class="copy"><h2 class="disp">Negro, azul <em>y un rojo</em></h2>
   <p class="lead">El negro manda: es el aire y la base. El azul queda atrás, hecho de líneas finas y placas. El rojo es una sola masa al frente. Nunca se mezclan en una misma forma.</p></div>
   ''' + stage('portatil', 'paleta', [sm('boton', 91, 80, 62, .2)], 'Lámina 02', 'Switch · portátil', 3, bw=60, bx=2, by=-6, hw=96) + '''
  </div>
  <div class="swatches">
   <div class="sw" style="background:#050505;color:var(--hielo);box-shadow:inset 0 0 0 1px #1a26a8"><span>Negro base<br>#050505</span></div>
   <div class="sw" style="background:#0a0a0d;color:var(--hielo);box-shadow:inset 0 0 0 1px #1a26a8"><span>Casi negro<br>#0A0A0D</span></div>
   <div class="sw" style="background:#1a26a8;color:var(--hielo)"><span>Azul línea<br>#1A26A8</span></div>
   <div class="sw" style="background:#2a3cff;color:var(--hielo)"><span>Azul placa<br>#2A3CFF</span></div>
   <div class="sw" style="background:#ff2a1a;color:#050505"><span>Rojo · frente<br>#FF2A1A</span></div>
   <div class="sw" style="background:#f4f4ef;color:#050505"><span>Hielo · texto<br>#F4F4EF</span></div>
  </div>
  <div class="types">
   <div class="ty"><span class="mono">Display · Instrument Serif</span><div class="specimen s1">Aa <em>Ñ7</em></div><p>Títulos grandes en hielo, con cursiva para el énfasis. Nunca en rojo ni en azul.</p></div>
   <div class="ty"><span class="mono">Texto · Outfit</span><div class="specimen s2">Aa Ñ7</div><p>Párrafos, nombres de juegos y botones. 400 y 600.</p></div>
   <div class="ty"><span class="mono">Etiquetas · Space Mono</span><div class="specimen s3">Aa 07</div><p>Números de lámina y pies de pieza. 11–12 px, mayúsculas.</p></div>
  </div>
 </div>
</section>
''')
H.append(CUT('notch', 'k0', 'k1'))
H.append('''<section class="field bg-k1 rev" id="cromo">
 ''' + fix('cromo') + '''
 <div class="wrap">
  ''' + head('03', 'Sistema cromo') + '''
  <div class="g12">
   <div class="copy"><h2 class="disp">Rojo al frente, <em>azul atrás</em></h2>
   <p class="lead">Tres planos con papeles distintos, como en las referencias del proyecto: negro de base y espacio, azul como estructura trasera, rojo como masa delantera. Cada color es una forma aparte, con bordes nítidos.</p>
   <ol class="planes-key"><li><i style="background:var(--rojo)"></i><b>Delante</b> Rojo · una masa focal</li><li><i style="background:var(--k0);box-shadow:inset 0 0 0 1px var(--hielo)"></i><b>Medio</b> Negro · aire y lectura</li><li><i style="background:var(--azul)"></i><b>Atrás</b> Azul · líneas y placas</li></ol></div>
   ''' + stage('chip', 'cromo', [sm('flecha', 2, 78, 96, .2)], 'Lámina 03', 'Chip · placas', 0, bw=70, bx=-4, by=-10, hw=84) + '''
  </div>
  <div class="rules">
   <div class="rl"><b>01</b><p>Base negra y mucho espacio vacío. El azul no rellena secciones.</p></div>
   <div class="rl"><b>02</b><p>Un objeto, una geometría: rojo o azul, nunca los dos en la misma forma ni en el mismo contorno.</p></div>
   <div class="rl"><b>03</b><p>Sin halos, brillos, difuminados ni degradados rojo–azul. Bordes nítidos.</p></div>
   <div class="rl"><b>04</b><p>Una masa roja por sección y, a lo mucho, una pequeña. Texto en hielo; nunca rojo sobre azul.</p></div>
  </div>
 </div>
</section>
''')
H.append(CUT('diag', 'k1', 'k0'))
names = [('hero', 'placa-hero', 'Horizonte y circuitos', 'Inicio'), ('paleta', 'placa-paleta', 'Retícula y guilloche', 'Paleta'), ('cromo', 'placa-cromo', 'Curvas de nivel', 'Cromo'), ('parallax', 'placa-parallax', 'Órbitas', 'Parallax'), ('filas', 'placa-filas', 'Circuitos', 'Filas'), ('catalogo', 'placa-catalogo', 'Cordilleras píxel', 'Catálogo'), ('streaming', 'placa-streaming', 'Rayos y ondas', 'Streaming'), ('ia', 'placa-ia', 'Red neuronal', 'IA y tecnología')]
tiles = ''.join(f'<figure class="tile"><div class="art a-{k}"></div><img class="tp" src="assets/placas/{p}.svg" alt="" loading="lazy"><figcaption><span class="mono">Lámina {i+1:02d}</span><b>{t}</b><small>{s}</small></figcaption></figure>' for i, (k, p, t, s) in enumerate(names))
H.append('''<section class="field bg-k0" id="grabado">
 <div class="wrap">
  ''' + head('04', 'Planos azules') + '''
  <div class="g12 intro"><h2 class="disp">Un plano trasero por <em>apartado</em></h2>
  <p class="lead">Cada apartado tiene su propia estructura azul: línea fina de fondo y una placa sólida con detalle negro. Todo en azul y negro, sin transparencias. El rojo nunca entra aquí.</p></div>
  <div class="tiles">''' + tiles + '''</div>
 </div>
</section>
''')
H.append(CUT('step', 'k0', 'k1'))
H.append('''<section class="field pxs bg-k1" id="parallax" aria-labelledby="hpx">
 ''' + fix('parallax') + '''
 <div class="wrap">
  ''' + head('05', 'Parallax') + '''
  <div class="g12 pxgrid">
   <div class="copy"><h2 id="hpx" class="disp">Fondo fijo, <em>masa en movimiento</em></h2>
   <p class="lead">Las líneas azules se quedan casi quietas. La placa y, sobre todo, la masa roja se mueven a distinta velocidad: lo más cercano, más rápido. Con «reducir movimiento» todo queda quieto.</p>
   <p class="note">Tres capas: plano fijo · placa lenta · rojo rápido.</p></div>
   ''' + stage('audifonos', 'parallax', [sm('play', 90, 80, 64, .26)], 'Lámina 05', 'Audio · streaming', 0, bw=66, bx=-2, by=-12, hw=82) + '''
  </div>
 </div>
</section>
''')
H.append(CUT('notch', 'k1', 'k0'))
H.append('''<section class="field bg-k0" id="cortes" style="padding-bottom:30px">
 <div class="wrap">
  ''' + head('06', 'Cortes de sección') + '''
  <div class="g12 intro"><h2 class="disp">Tres <em>cortes</em></h2>
  <p class="lead">Diagonal fina, escalón y línea con muescas. Se dibujan con un solo trazo azul sobre negro: ni rojo, ni mezclas.</p></div>
 </div>
</section>
<div class="cutdemo" aria-hidden="true">
 <div data-cut="diag" data-from="k0" data-to="k1"><span class="cut-tag">Diagonal</span></div>
 <div class="mini bg-k1"></div>
 <div data-cut="step" data-from="k1" data-to="k0"><span class="cut-tag">Escalón</span></div>
 <div class="mini bg-k0"></div>
 <div data-cut="notch" data-from="k0" data-to="k1"><span class="cut-tag">Muescas</span></div>
 <div class="mini bg-k1"></div>
</div>
''')
H.append('''<section class="field bg-k1" id="filas">
 ''' + fix('filas') + '''
 <div class="wrap">
  ''' + head('07', 'Filas deslizables') + '''
  <div class="g12">
   <div class="copy"><h2 class="disp">Estilo <em>Netflix</em></h2>
   <p class="lead">Deslizan con el dedo, con arrastre del mouse, con flechas o con las teclas ← →. Se detienen tarjeta por tarjeta; las flechas van arriba de la fila para no tapar nada.</p></div>
   ''' + stage('pantalla', 'filas', [sm('cursor', 91, 78, 54, .22)], 'Lámina 07', 'Catálogo · pantalla', -2, bw=64, bx=-2, by=-8, hw=84) + '''
  </div>
  <div class="rowzone"><div data-row="plataformas" data-title="Consolas y PC"></div>
  <p class="hint">Precios: siempre «Consultar precio» · cotización por WhatsApp</p></div>
 </div>
</section>
''')
H.append(CUT('diag', 'k1', 'k0'))
LEADS = {'ej-catalogo': 'Portadas en fila, una tarjeta por juego. El precio siempre dice «Consultar precio» y la cotización va por WhatsApp.', 'ej-streaming': 'Plataformas de series, cine y música con su logo sobre una placa limpia. Consulta el precio y cotiza por WhatsApp.', 'ej-ia': 'Herramientas de IA y tecnología en la misma fila deslizable, con visuales de cómputo y chips.'}
def ex(id_, no, kicker, title, row, rtitle, st, bg, k):
    return f'''<section class="field bg-{bg}" id="{id_}">
 {fix(k)}
 <div class="wrap">
  {head(no, kicker, '10')}
  <div class="g12"><div class="copy"><h2 class="disp">{title}</h2><p class="lead">{LEADS[id_]}</p></div>{st}</div>
  <div class="rowzone"><div data-row="{row}" data-title="{rtitle}"></div></div>
 </div>
</section>
'''
H.append(ex('ej-catalogo', '08', 'Ejemplo · Catálogo', 'Nintendo <em>Switch</em>', 'juegos', 'Aventura y plataformas', stage('joystick', 'catalogo', [sm('boton', 2, 74, 62, .22)], 'Lámina 08', 'Juegos', 2, bw=66, bx=-4, by=-8, hw=70), 'k0', 'catalogo'))
H.append(CUT('step', 'k0', 'k1'))
H.append(ex('ej-streaming', '09', 'Ejemplo · Suscripciones', '<em>Streaming</em>', 'streaming', 'Series, cine y música', stage('claqueta', 'streaming', [sm('etiqueta', 2, 80, 96, .2)], 'Lámina 09', 'Series · cine', -2, bw=72, bx=-4, by=-8, hw=82), 'k1', 'streaming'))
H.append(CUT('notch', 'k1', 'k0'))
H.append(ex('ej-ia', '10', 'Ejemplo · IA y tecnología', 'Inteligencia <em>artificial</em>', 'ia', 'Herramientas de IA', stage('gpu', 'ia', [sm('sello', 90, 82, 70, .18)], 'Lámina 10', 'IA · cómputo', 2, bw=58, bx=0, by=-14, hw=92), 'k0', 'ia'))
H.append(CUT('diag', 'k0', 'k1'))
H.append('''</main>
<footer><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="GameMaster"><p>Propuesta de identidad visual v7 · página estática, sin build ni CDN. Las marcas de terceros pertenecen a sus dueños. Precios siempre «Consultar precio».</p></footer>
<script src="app.js"></script>
</body></html>
''')
open(sys.argv[1], 'w').write(''.join(H)); print('ok')
