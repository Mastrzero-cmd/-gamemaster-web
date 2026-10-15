#!/usr/bin/env python3
"""v6 · genera index.html (maquetación editorial: láminas, héroe rojo + 2-3 piezas de apoyo por sección). Uso: python3 construir_v6.py ../index.html"""
import sys
def pz(n, l, t, w, sp, r=0, hero=False, mw=None, folder='piezas', pre='pieza', cls=''):
    mw = mw or (w * 5 if not hero else 100)
    c = 'pz' + (' hero' if hero else ' sm') + (' ' + cls if cls else '')
    return (f'<div class="{c}" data-speed="{sp}" style="--l:{l}%;--t:{t}%;--w:{w}%;--r:{r}deg"><img src="assets/{folder}/{pre}-{n}.svg" alt="" draggable="false" loading="lazy"></div>')
def hero(n, sp=.08, r=0): return pz(n, 0, 0, 100, sp, r, True, folder='heroes', pre='heroe', cls='h')
WIDE = {'chip': 0, 'pantalla': 0, 'portatil': 1, 'audifonos': 1}
def stage(heroname, smalls, cap, r=0, hsp=.08, tag=''):
    h = f'<div class="pz hero" data-speed="{hsp}" style="--r:{r}deg"><img src="assets/heroes/heroe-{heroname}.svg" alt="" draggable="false"></div>'
    return f'<figure class="stage{" wide" if heroname in WIDE else ""}" aria-hidden="true"><i class="frame"></i><span class="tag">{tag}</span>{h}{"".join(smalls)}<figcaption>{cap.split(' · ')[0]}<span class="hh"> · héroe</span></figcaption></figure>'
def sm(n, x, y, w, sp, r=0): return f'<div class="pz sm" data-speed="{sp}" style="--x:{x}%;--y:{y}%;--sw:{w}px;--r:{r}deg"><img src="assets/piezas/pieza-{n}.svg" alt="" draggable="false" loading="lazy"></div>'
def head(no, label, total='10'): return f'<header class="plate-head"><span class="no">{no}</span><span class="lab">{label}</span><span class="rule"></span><span class="of">{no} / {total}</span></header>'
def art(k, extra=''): return f'<div class="art ly a-{k}-f" data-speed=".04"></div>' + extra
CUT = lambda t, a, b: f'<div data-cut="{t}" data-from="{a}" data-to="{b}"></div>\n'
H = []
H.append('''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GameMaster · Identidad visual v6 (propuesta)</title>
<meta name="description" content="Propuesta v6 de identidad visual de GameMaster: edición limpia tipo galería, una pieza héroe roja por sección sobre campos azules, arte fino y sutil, parallax y filas deslizables.">
<link rel="stylesheet" href="styles.css"></head><body>
<header class="hdr"><div class="wrap"><a class="brand" href="#inicio" aria-label="GameMaster, inicio"><img src="assets/logo/gamemaster-horizontal-oscuro.svg" alt="GameMaster" width="130" height="34"></a>
<nav class="nav" aria-label="Secciones"><a href="#logo">Logo</a><a href="#paleta">Paleta</a><a href="#cromo">Cromo</a><a href="#grabado">Arte</a><a href="#parallax">Parallax</a><a href="#cortes">Cortes</a><a href="#filas">Filas</a><a href="#ej-catalogo">Ejemplo</a></nav>
<a class="btn" href="https://wa.me/525527699426" rel="noopener">Cotizar</a></div></header>
<main>
''')
# ---- INICIO
H.append('''<section class="field hero-sec bg-azul" id="inicio" aria-labelledby="h1">
 <div class="fixbg" aria-hidden="true"><div class="fixin"><div class="art a-hero-f"></div></div></div>
 <i class="slab" aria-hidden="true"></i>
 <div class="wrap g12">
  <div class="copy">
   <img class="logo-hero" src="assets/logo/gamemaster-completo-oscuro.svg" alt="GameMaster" width="560" height="392">
   <h1 id="h1" class="disp">Todo tu universo <em>digital</em></h1>
   <p class="lead">Videojuegos, streaming e inteligencia artificial en un solo lugar. Elige, consulta el precio y cotiza por WhatsApp.</p>
   <div class="cta"><a class="btn" href="#ej-catalogo">Explorar catálogo →</a><a class="btn ghost" href="https://wa.me/525527699426" rel="noopener">Hablar por WhatsApp</a></div>
  </div>
  ''' + stage('mando', [sm('sello', 90, 16, 96, .2, 8), sm('estrella', 2, 78, 54, .16), sm('boton', 84, 82, 70, .24)], 'Lámina 00 · Mando · pieza héroe', -6, .08, 'PS5 · Switch · PC') + '''
 </div>
</section>
''')
H.append(CUT('diag', 'azul', 'noche'))
# ---- LOGO
H.append('''<section class="field bg-noche" id="logo">
 <div class="wrap">
  ''' + head('01', 'Logo') + '''
  <div class="g12 intro"><h2 class="disp">El logo, <em>solo</em></h2>
  <p class="lead">Letras itálicas de pincel, relleno cian a azul eléctrico, contorno magenta desplazado y la pincelada curva debajo. Vectorial (SVG) y PNG sin fondo.</p></div>
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
   <div class="var azu"><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="Logo sobre campo azul"><small>Sobre campo azul</small></div>
   <div class="var azu"><img src="assets/logo/gamemaster-compacto-mono-blanco.svg" alt="Icono monocromo sobre azul"><small>Icono mono · azul</small></div>
  </div>
  <div class="dl"><a href="assets/logo/gamemaster-completo-oscuro.svg">SVG completo oscuro</a><a href="assets/logo/gamemaster-completo-claro.svg">SVG completo claro</a><a href="assets/logo/gamemaster-completo-oscuro-1024.png">PNG 1024 sin fondo</a><a href="assets/logo/gamemaster-horizontal-oscuro-512.png">PNG horizontal 512</a><a href="assets/logo/gamemaster-compacto-oscuro-512.png">PNG icono 512</a></div>
 </div>
</section>
''')
H.append(CUT('step', 'noche', 'azul'))
# ---- PALETA
H.append('''<section class="field bg-azul" id="paleta">
 ''' + art('paleta') + '''<i class="slab r" aria-hidden="true"></i>
 <div class="wrap">
  ''' + head('02', 'Paleta y tipos') + '''
  <div class="g12">
   <div class="copy"><h2 class="disp">Neón sobre <em>azul</em></h2>
   <p class="lead">Campos grandes en azul eléctrico suavizado. El cian y el magenta viven en el logo y en detalles mínimos. El rojo es solo para la pieza al frente.</p></div>
   ''' + stage('portatil', [sm('cursor', 1, 70, 70, .22, -6), sm('estrella', 90, 88, 54, .16)], 'Lámina 02 · Consola portátil · pieza héroe', 4, .08, 'Switch · portátil') + '''
  </div>
  <div class="swatches">
   <div class="sw" style="background:var(--noche);color:var(--hielo)"><span>Noche<br>#05071F</span></div>
   <div class="sw" style="background:var(--prof);color:var(--hielo)"><span>Azul profundo<br>#1C2BB0</span></div>
   <div class="sw" style="background:var(--azul2);color:#fff"><span>Azul eléctrico<br>#4A62FF</span></div>
   <div class="sw" style="background:var(--cian);color:var(--noche)"><span>Cian neón<br>#3FDCFF</span></div>
   <div class="sw" style="background:var(--rojo);color:var(--noche)"><span>Rojo · al frente<br>#FF3322</span></div>
   <div class="sw" style="background:var(--magenta);color:var(--noche)"><span>Magenta<br>#FF3B7F</span></div>
   <div class="sw" style="background:var(--hielo);color:var(--noche)"><span>Hielo · texto<br>#EAF6FF</span></div>
  </div>
  <div class="types">
   <div class="ty"><span class="mono">Display · Instrument Serif</span><div class="specimen s1">Aa <em>Ñ7</em></div><p>Títulos grandes en hielo, con cursiva para el énfasis. Nunca en rojo.</p></div>
   <div class="ty"><span class="mono">Texto · Outfit</span><div class="specimen s2">Aa Ñ7</div><p>Párrafos, nombres de juegos y botones. 400 y 600.</p></div>
   <div class="ty"><span class="mono">Etiquetas · Space Mono</span><div class="specimen s3">Aa 07</div><p>Números de lámina y pies de pieza. 11–12 px, mayúsculas.</p></div>
  </div>
 </div>
</section>
''')
H.append(CUT('notch', 'azul', 'prof'))
# ---- CROMO
H.append('''<section class="field bg-prof rev" id="cromo">
 ''' + art('cromo') + '''<i class="slab" aria-hidden="true"></i>
 <div class="wrap">
  ''' + head('03', 'Sistema cromo') + '''
  <div class="g12">
   <div class="copy"><h2 class="disp">Rojo al frente, <em>azul atrás</em></h2>
   <p class="lead">Tres planos: el azul profundo queda atrás, el azul eléctrico en medio y la pieza roja adelante. El negro solo separa: una línea, una sombra dura, un bloque.</p>
   <ol class="planes-key"><li><i style="background:var(--prof);outline:1px solid rgba(234,246,255,.5)"></i><b>Plano 3</b> Atrás · azul profundo</li><li><i style="background:var(--azul2)"></i><b>Plano 2</b> Medio · azul eléctrico</li><li><i style="background:var(--rojo)"></i><b>Plano 1</b> Adelante · rojo</li></ol></div>
   ''' + stage('chip', [sm('cartucho', 1, 70, 82, .22, -8), sm('estrella', 92, 84, 54, .16)], 'Lámina 03 · Chip sobre placas · pieza héroe', 0, .08, 'Chip · placas') + '''
  </div>
  <div class="rules">
   <div class="rl"><b>01</b><p>Rojo solo sobre azul. Sobre negro no es pieza principal.</p></div>
   <div class="rl"><b>02</b><p>Contorno negro duro y una sombra de capa en cada pieza.</p></div>
   <div class="rl"><b>03</b><p>Un héroe por sección y dos o tres piezas de apoyo, no más.</p></div>
   <div class="rl"><b>04</b><p>Texto siempre en hielo o noche. Nunca rojo sobre azul.</p></div>
  </div>
 </div>
</section>
''')
H.append(CUT('diag', 'prof', 'noche'))
# ---- GRABADO
names = [('hero','Curvas de nivel y horizonte','Inicio','azul'),('paleta','Plano técnico','Paleta','azul'),('cromo','Placas isométricas','Cromo','prof'),('parallax','Rosetas finas','Parallax','azul'),('filas','Circuitos','Filas','azul'),('catalogo','Montañas y cartuchos','Catálogo','prof'),('streaming','Cintas y rayos','Streaming','azul'),('ia','Red neuronal','IA y tecnología','prof')]
tiles = ''.join(f'<figure class="tile bg-{bg}"><div class="art a-{k}-f"></div><figcaption><span class="mono">Lámina {i+1:02d}</span><b>{t}</b><small>{s}</small></figcaption></figure>' for i, (k, t, s, bg) in enumerate(names))
H.append('''<section class="field bg-noche" id="grabado">
 <div class="wrap">
  ''' + head('04', 'Arte azul') + '''
  <div class="g12 intro"><h2 class="disp">Un arte por <em>apartado</em></h2>
  <p class="lead">Cada campo azul lleva una sola capa de grabado fino, de tono cercano al fondo: curvas de nivel, placas, circuitos, rosetas. Detalle sin ruido, para que la pieza roja respire.</p></div>
  <div class="tiles">''' + tiles + '''</div>
 </div>
</section>
''')
H.append(CUT('step', 'noche', 'azul'))
# ---- PARALLAX
H.append('''<section class="field pxs bg-azul" id="parallax" aria-labelledby="hpx">
 <div class="fixbg" aria-hidden="true"><div class="fixin"><div class="art a-parallax-f"></div></div></div>
 <i class="slab r" aria-hidden="true"></i>
 <div class="wrap">
  ''' + head('05', 'Parallax') + '''
  <div class="g12 pxgrid">
   <div class="copy"><h2 id="hpx" class="disp">Fondo fijo, <em>piezas en movimiento</em></h2>
   <p class="lead">El azul grabado se queda quieto. La pieza roja y sus acompañantes se mueven a distinta velocidad: las más cercanas, más rápido. Con «reducir movimiento» todo queda quieto.</p>
   <p class="note">Tres capas: fondo fijo · héroe lento · apoyo rápido.</p></div>
   ''' + stage('audifonos', [sm('play', 1, 72, 84, .26, 0), sm('estrella', 88, 16, 56, .2), sm('disco', 90, 80, 78, .14)], 'Lámina 05 · Audífonos · pieza héroe', 0, .08, 'Audio · streaming') + '''
  </div>
 </div>
</section>
''')
H.append(CUT('notch', 'azul', 'noche'))
# ---- CORTES
H.append('''<section class="field bg-noche" id="cortes" style="padding-bottom:30px">
 <div class="wrap">
  ''' + head('06', 'Cortes de sección') + '''
  <div class="g12 intro"><h2 class="disp">Tres <em>cortes</em></h2>
  <p class="lead">Diagonal fina, escalón y línea con muescas. Siempre con el color de arriba y el de abajo, una línea de precisión y nada más.</p></div>
 </div>
</section>
<div class="cutdemo" aria-hidden="true">
 <div data-cut="diag" data-from="noche" data-to="azul"><span class="cut-tag">Diagonal</span></div>
 <div class="mini bg-azul"></div>
 <div data-cut="step" data-from="azul" data-to="noche"><span class="cut-tag">Escalón</span></div>
 <div class="mini bg-noche"></div>
 <div data-cut="notch" data-from="noche" data-to="azul"><span class="cut-tag">Muescas</span></div>
 <div class="mini bg-azul"></div>
</div>
''')
# ---- FILAS
H.append('''<section class="field bg-azul" id="filas">
 ''' + art('filas') + '''<i class="slab" aria-hidden="true"></i>
 <div class="wrap">
  ''' + head('07', 'Filas deslizables') + '''
  <div class="g12">
   <div class="copy"><h2 class="disp">Estilo <em>Netflix</em></h2>
   <p class="lead">Deslizan con el dedo, con arrastre del mouse, con flechas o con las teclas ← →. Se detienen tarjeta por tarjeta; las flechas van arriba de la fila para no tapar nada.</p></div>
   ''' + stage('pantalla', [sm('flecha', 1, 74, 100, .22), sm('estrella', 92, 82, 54, .16)], 'Lámina 07 · Pantalla con catálogo · pieza héroe', -3, .08, 'Catálogo · pantalla') + '''
  </div>
  <div class="rowzone"><div data-row="plataformas" data-title="Consolas y PC"></div>
  <p class="hint">Precios: siempre «Consultar precio» · cotización por WhatsApp</p></div>
 </div>
</section>
''')
H.append(CUT('diag', 'azul', 'prof'))
LEADS = {'ej-catalogo': 'Portadas en fila, una tarjeta por juego. El precio siempre dice «Consultar precio» y la cotización va por WhatsApp.', 'ej-streaming': 'Plataformas de series, cine y música con su logo sobre una placa limpia. Consulta el precio y cotiza por WhatsApp.', 'ej-ia': 'Herramientas de IA y tecnología en la misma fila deslizable, con visuales de cómputo y chips.'}
def ex(id_, no, kicker, title, row, rtitle, st, bg, art_k, slab=''):
    return f'''<section class="field bg-{bg}" id="{id_}">
 {art(art_k)}<i class="slab{slab}" aria-hidden="true"></i>
 <div class="wrap">
  {head(no, kicker, '10')}
  <div class="g12"><div class="copy"><h2 class="disp">{title}</h2><p class="lead">{LEADS[id_]}</p></div>{st}</div>
  <div class="rowzone"><div data-row="{row}" data-title="{rtitle}"></div></div>
 </div>
</section>
'''
H.append(ex('ej-catalogo', '08', 'Ejemplo · Catálogo', 'Nintendo <em>Switch</em>', 'juegos', 'Aventura y plataformas', stage('joystick', [sm('cartucho', 1, 70, 78, .22, -8), sm('estrella', 90, 16, 54, .16), sm('boton', 86, 84, 66, .24)], 'Lámina 08 · Joystick arcade · pieza héroe', 3, .08, 'Juegos'), 'prof', 'catalogo', ' r'))
H.append(CUT('step', 'prof', 'azul'))
H.append(ex('ej-streaming', '09', 'Ejemplo · Suscripciones', '<em>Streaming</em>', 'streaming', 'Series, cine y música', stage('claqueta', [sm('estrella', 2, 74, 54, .2), sm('microfono', 90, 78, 56, .24, 8)], 'Lámina 09 · Claqueta · pieza héroe', -2, .08, 'Series · cine'), 'azul', 'streaming'))
H.append(CUT('notch', 'azul', 'prof'))
H.append(ex('ej-ia', '10', 'Ejemplo · IA y tecnología', 'Inteligencia <em>artificial</em>', 'ia', 'Herramientas de IA', stage('gpu', [sm('cursor', 1, 72, 66, .24, -8), sm('chip', 88, 84, 78, .16, 6), sm('estrella', 92, 16, 52, .2)], 'Lámina 10 · Tarjeta gráfica · pieza héroe', 2, .08, 'IA · cómputo'), 'prof', 'ia', ' r'))
H.append(CUT('diag', 'prof', 'noche'))
H.append('''</main>
<footer><img src="assets/logo/gamemaster-completo-oscuro.svg" alt="GameMaster"><p>Propuesta de identidad visual v6 · página estática, sin build ni CDN. Las marcas de terceros pertenecen a sus dueños. Precios siempre «Consultar precio».</p></footer>
<script src="app.js"></script>
</body></html>
''')
open(sys.argv[1], 'w').write(''.join(H)); print('ok')
