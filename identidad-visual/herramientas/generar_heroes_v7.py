#!/usr/bin/env python3
"""v7 · (parche de v6) 8 piezas HÉROE rojas SOLO rojo/negro: sin halo magenta, sin azul, sin opacidades. 8 piezas HÉROE rojas (SVG): contorno negro duro, sombra de capa, volumen en 3 tonos de rojo y grabado fino.
Uso: python3 generar_heroes_v6.py ../assets/heroes   (sin texto dentro, sin personajes)"""
import sys, os, math
R, RD, RDD, RL, RK, MG, NV = '#ff2a1a', '#c4160c', '#7d0a05', '#ff6552', '#050505', '#050505', '#050505'
BL, BL2, BL3 = '#1a0503', '#4a0a06', '#7d0a05'
_n = [0]
def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def uid(): _n[0] += 1; return 'k%d' % _n[0]
import re as _re
def strip(x): return _re.sub(r' (?:stroke-|fill-)?opacity="[^"]*"','',x)
def svg(name, w, h, body, pad=0):
    defs = ('<defs><pattern id="hc" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-38)"><path d="M0 0H6" stroke="%s" stroke-width="1.5"/></pattern>'
            '<pattern id="hd" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><circle cx="2.5" cy="2.5" r="1" fill="%s"/></pattern></defs>') % (RDD, RDD)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w+2*pad} {h+2*pad}" role="img" aria-label="{name}"><title>{name}</title>{defs}{body}</svg>'.replace('\n',''))
def vol(d, off=9, sw=5, base=R, dark=RD, hatch=True, shadow=0, tr=''):
    """silueta con volumen: tono oscuro abajo/derecha (con grabado), tono base, rim claro arriba/izquierda, contorno negro duro, sombra de capa opcional."""
    i = uid(); o = ''
    if shadow:
        o += f'<path d="{d}" fill="{NV}" opacity=".9" transform="translate({shadow} {shadow*1.1})"/>'
    o += f'<clipPath id="{i}"><path d="{d}"/></clipPath><path d="{d}" fill="{dark}"/>'
    o += f'<g clip-path="url(#{i})">'
    if hatch: o += f'<path d="{d}" fill="url(#hc)" opacity=".75"/>'
    o += f'<path d="{d}" fill="{base}" transform="translate({-off} {-off*1.15})"/>'
    o += '</g>'
    o += f'<path d="{d}" fill="none" stroke="{RK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'
    return f'<g{(" transform=%s" % chr(34)+tr+chr(34)) if tr else ""}>{o}</g>'
def rr(x, y, w, h, r):
    return f'M{f(x+r)} {f(y)}H{f(x+w-r)}Q{f(x+w)} {f(y)} {f(x+w)} {f(y+r)}V{f(y+h-r)}Q{f(x+w)} {f(y+h)} {f(x+w-r)} {f(y+h)}H{f(x+r)}Q{f(x)} {f(y+h)} {f(x)} {f(y+h-r)}V{f(y+r)}Q{f(x)} {f(y)} {f(x+r)} {f(y)}Z'
def ell(cx, cy, rx, ry): return f'M{f(cx-rx)} {f(cy)}a{f(rx)} {f(ry)} 0 1 0 {f(2*rx)} 0a{f(rx)} {f(ry)} 0 1 0 {f(-2*rx)} 0Z'
def ln(d, c=RK, w=4, o=1, extra=''): return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{o}" {extra}/>'
def blk(d, fill=RK, extra=''): return f'<path d="{d}" fill="{fill}" {extra}/>'
def star4(cx, cy, r, k=.25):
    p = []
    for i in range(8):
        a = math.radians(-90 + i * 45); q = r if i % 2 == 0 else r * k; p.append((cx + math.cos(a) * q, cy + math.sin(a) * q))
    return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in p) + 'Z'
def ticks(x, y, n, dx, dy, l, c=RDD, w=2.5, ang=0):
    return ''.join(ln(f'M{f(x+k*dx)} {f(y+k*dy)}l{f(l*math.cos(math.radians(ang)))} {f(l*math.sin(math.radians(ang)))}', c, w, .8) for k in range(n))
H = {}

# ---------- 1 · MANDO (inicio) ----------
body = 'M196 168C196 112 250 92 318 94H582C650 92 704 112 704 168C762 268 820 420 790 508C770 566 700 574 662 524C634 486 622 450 590 436H310C278 450 266 486 238 524C200 574 130 566 110 508C80 420 138 268 196 168Z'
o = vol(rr(168, 62, 150, 52, 22), 5, 5, shadow=0) + vol(rr(582, 62, 150, 52, 22), 5, 5)
o += vol(body, 14, 6, shadow=26)
o += ln('M250 128C300 118 600 118 650 128', RL, 5, .8) + ln('M214 190C330 150 570 150 686 190', RDD, 3, .7)
o += ln('M150 450C128 480 118 508 126 530', RK, 4, .7) + ln('M750 450C772 480 782 508 774 530', RK, 4, .7)
o += ''.join(ln(f'M{x} {y}l16 -22', RDD, 3, .85) for x, y in [(146, 470), (160, 488), (174, 506), (738, 470), (752, 488), (766, 506)])
# cruceta
dp = 'M246 196H282V232H318V268H282V304H246V268H210V232H246Z'
o += blk(dp, RK, 'transform="translate(6 7)"') + vol(dp, 5, 4, base=RD, dark=RDD, hatch=False)
o += ln('M264 214L264 224M264 286L264 276M228 250L238 250M300 250L290 250', RK, 4)
# botones
for cx, cy in [(636, 188), (690, 244), (636, 300), (582, 244)]:
    o += f'<circle cx="{cx+4}" cy="{cy+6}" r="30" fill="{RK}"/>' + vol(ell(cx, cy, 28, 28), 5, 4, base=RD, dark=RDD, hatch=False)
o += ''.join(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{RK}"/>' for cx, cy in [(636, 188), (690, 244), (636, 300), (582, 244)]) + ''.join(f'<circle cx="{cx}" cy="{cy}" r="15" fill="none" stroke="{RDD}" stroke-width="2.5"/>' for cx, cy in [(636, 188), (690, 244), (636, 300), (582, 244)])
# sticks
for cx in (340, 560):
    o += f'<circle cx="{cx}" cy="368" r="52" fill="{RK}"/>' + f'<circle cx="{cx}" cy="368" r="42" fill="{RDD}" stroke="{RK}" stroke-width="4"/>' + vol(ell(cx, 366, 33, 33), 6, 4, base=R, dark=RD) + f'<circle cx="{cx}" cy="366" r="18" fill="none" stroke="{RDD}" stroke-width="3"/>' + ticks(cx - 12, 360, 4, 8, 0, 0, RDD, 2)
# centro
o += vol(rr(398, 150, 104, 66, 14), 4, 4, base=RD, dark=RDD, hatch=False) + ln('M414 170H486M414 184H470', RK, 3.5, .8)
o += f'<circle cx="450" cy="258" r="22" fill="{RK}"/><circle cx="450" cy="258" r="13" fill="{R}"/>' + ln('M418 120H482', RL, 4, .8)
o += f'<rect x="372" y="236" width="38" height="12" rx="6" fill="{RK}"/><rect x="490" y="236" width="38" height="12" rx="6" fill="{RK}"/>'
H['mando'] = svg('Mando', 900, 620, o, 40)

# ---------- 2 · PORTÁTIL (paleta) ----------
o = ''
L = 'M96 130Q96 74 152 74H268V486H152Q96 486 96 430Z'; Rr = 'M804 130Q804 74 748 74H632V486H748Q804 486 804 430Z'
o += vol(L, 10, 6, shadow=22) + vol(Rr, 10, 6)
o += vol(rr(240, 44, 420, 470, 34), 12, 6, base='#ff4a37', dark=RD, shadow=22)
# pantalla
o += f'<rect x="268" y="74" width="364" height="410" rx="16" fill="{RK}"/><rect x="284" y="90" width="332" height="378" rx="8" fill="{BL}"/>'
o += f'<clipPath id="sc"><rect x="284" y="90" width="332" height="378" rx="8"/></clipPath><g clip-path="url(#sc)"><rect x="284" y="90" width="332" height="190" fill="{BL3}" opacity=".5"/>'
for k in range(18): o += f'<path d="M284 {110+k*20}H616" stroke="{RK}" stroke-width="1.2" opacity=".18"/>'
o += ln('M284 400C360 340 420 420 520 350S600 380 616 360', BL3, 3, .8) + ln('M284 430C380 380 440 450 540 390S600 420 616 400', RK, 3, .35)
o += ''.join(f'<rect x="{304+k*72}" y="{338}" width="60" height="88" rx="4" fill="{BL2}" stroke="{RK}" stroke-width="3"/>' for k in range(4)) + '</g>'
o += f'<circle cx="450" cy="214" r="52" fill="{R}" stroke="{RK}" stroke-width="5"/><path d="M434 188L476 214L434 240Z" fill="{RK}"/>' + ln('M404 196A52 52 0 0 1 430 170', RL, 5, .9)
# palancas y botones
o += f'<circle cx="182" cy="170" r="44" fill="{RK}"/>' + vol(ell(182, 168, 34, 34), 6, 4, dark=RDD) + f'<circle cx="182" cy="168" r="18" fill="none" stroke="{RDD}" stroke-width="3"/>'
o += f'<circle cx="718" cy="330" r="44" fill="{RK}"/>' + vol(ell(718, 328, 34, 34), 6, 4, dark=RDD) + f'<circle cx="718" cy="328" r="18" fill="none" stroke="{RDD}" stroke-width="3"/>'
for cx, cy in [(718, 176), (756, 214), (718, 252), (680, 214)]: o += f'<circle cx="{cx+3}" cy="{cy+4}" r="19" fill="{RK}"/>' + vol(ell(cx, cy, 17, 17), 4, 3, base=RD, dark=RDD, hatch=False)
for cx, cy, d in [(182, 330, 'M182 306V354M158 330H206')]: o += f'<circle cx="{cx}" cy="{cy}" r="34" fill="{RK}"/>' + ln(d, R, 12)
o += ln('M130 110V440', RDD, 3, .6) + ln('M770 110V440', RDD, 3, .6) + ln('M170 450H250M650 450H730', RK, 4, .7)
o += f'<rect x="150" y="406" width="40" height="12" rx="6" fill="{RK}"/><rect x="710" y="406" width="40" height="12" rx="6" fill="{RK}"/>'
H['portatil'] = svg('Consola portátil', 900, 560, o, 40)

# ---------- 3 · CHIP ISOMÉTRICO (cromo) ----------
cx0, cy0, S = 420, 180, 1.0
def P(x, y, z=0): return (cx0 + (x - y) * .866 * S, cy0 + (x + y) * .5 * S - z)
def poly(pts): return 'M' + 'L'.join(f'{f(a)} {f(b)}' for a, b in pts) + 'Z'
def box(x0, y0, z0, w, d, h, top=R, left=RD, right=RDD, sw=5, hatch=True):
    t = poly([P(x0, y0, z0 + h), P(x0 + w, y0, z0 + h), P(x0 + w, y0 + d, z0 + h), P(x0, y0 + d, z0 + h)])
    l = poly([P(x0, y0 + d, z0 + h), P(x0 + w, y0 + d, z0 + h), P(x0 + w, y0 + d, z0), P(x0, y0 + d, z0)])
    r = poly([P(x0 + w, y0, z0 + h), P(x0 + w, y0 + d, z0 + h), P(x0 + w, y0 + d, z0), P(x0 + w, y0, z0)])
    s = f'stroke="{RK}" stroke-width="{sw}" stroke-linejoin="round"'
    o = f'<path d="{l}" fill="{left}" {s}/><path d="{r}" fill="{right}" {s}/>'
    if hatch: o += f'<path d="{l}" fill="url(#hc)" opacity=".7"/>'
    o += f'<path d="{t}" fill="{top}" {s}/>'
    return o
o = ''
# sombra de capa
sh = poly([P(-40, -40, -30), P(380, -40, -30), P(380, 380, -30), P(-40, 380, -30)])
o += f'<path d="{sh}" fill="{NV}" opacity=".85" transform="translate(26 30)"/>'
o += box(-40, -40, 0, 420, 420, 26, R, RD, RDD)           # placa base grande
o += box(30, 30, 26, 280, 280, 22, '#ff5a45', RD, RDD)     # placa media
# pistas sobre la placa media
tr = lambda pts, c=RDD, w=4: ln('M' + 'L'.join(f'{f(P(a, b, 48)[0])} {f(P(a, b, 48)[1])}' for a, b in pts), c, w, .9)
o += tr([(30, 70), (60, 70), (80, 90)]) + tr([(30, 110), (50, 110)]) + tr([(310, 200), (270, 200), (250, 220)]) + tr([(310, 240), (290, 240)]) + tr([(100, 310), (100, 280)]) + tr([(140, 310), (140, 290)]) + tr([(200, 30), (200, 60)])
# pines
for k in range(7):
    t = 56 + k * 30
    o += box(t, 8, 48, 14, 24, 8, RL, RD, RDD, 3, False) + box(t, 308, 48, 14, 24, 8, RL, RD, RDD, 3, False)
for k in range(7):
    t = 56 + k * 30
    o += box(8, t, 48, 24, 14, 8, RL, RD, RDD, 3, False) + box(308, t, 48, 24, 14, 8, RL, RD, RDD, 3, False)
# dado central
o += box(100, 100, 48, 120, 120, 40, R, RD, RDD)
o += box(124, 124, 88, 72, 72, 10, RL, RD, RDD, 4, False)
o += ln('M' + 'L'.join(f'{f(P(a, b, 98)[0])} {f(P(a, b, 98)[1])}' for a, b in [(138, 138), (180, 138), (180, 180), (150, 180), (150, 156)]), RK, 4)
o += f'<path d="{poly([P(124, 124, 98), P(196, 124, 98), P(196, 196, 98), P(124, 196, 98)])}" fill="none" stroke="{RDD}" stroke-width="2" opacity=".6"/>'
H['chip'] = svg('Chip en placas', 860, 600, o, 40)

# ---------- 4 · AUDÍFONOS (parallax) ----------
o = ''
band = 'M150 330C150 150 250 70 400 70S650 150 650 330'
o += ln(band, NV, 62, .9, 'transform="translate(20 24)"')
o += ln(band, RK, 66) + ln(band, RDD, 52) + ln(band, R, 44, 1, 'transform="translate(-3 -4)"') + ln(band, RL, 8, .75, 'transform="translate(-6 -12)"')
o += ln('M174 300C176 190 250 112 400 112', RDD, 3, .8, 'stroke-dasharray="3 9"') + ln('M626 300C624 190 550 112 400 112', RDD, 3, .8, 'stroke-dasharray="3 9"')
o += vol(rr(370, 36, 60, 28, 8), 4, 4, base=RD, dark=RDD, hatch=False)
for sx in (1, -1):
    mx = 400 + sx * 250
    c = rr(mx - 78, 300, 156, 290, 70)
    yk = rr(mx - 20, 270, 40, 60, 12)
    o += vol(yk, 5, 4, base=RD, dark=RDD, hatch=False)
    o += vol(c, 14, 6, shadow=24)
    o += vol(rr(mx - 52 + sx * (-6), 336, 104, 218, 50), 8, 4, base=RD, dark=RDD)
    o += f'<ellipse cx="{mx - sx*6}" cy="445" rx="30" ry="62" fill="{RK}"/><ellipse cx="{mx - sx*6}" cy="445" rx="20" ry="46" fill="{RDD}"/>'
    o += ticks(mx - 56, 330, 0, 0, 0, 0)
    o += ''.join(ln(f'M{mx-58} {548+k*0}h0', RK, 1) for k in range(1))
    o += ln(f'M{mx-40} 590H{mx+40}', RDD, 3, .8)
    o += ''.join(f'<circle cx="{mx - sx*2 + (k-1)*22}" cy="{578}" r="3.5" fill="{RK}"/>' for k in range(3))
H['audifonos'] = svg('Audífonos', 800, 640, o, 40)

# ---------- 5 · PANTALLA (filas) ----------
o = ''
tvb = rr(60, 40, 780, 480, 30)
o += vol(rr(360, 520, 180, 64, 6), 5, 5, base=RD, dark=RDD)
o += vol(rr(250, 576, 400, 40, 18), 8, 5, shadow=20)
o += vol(tvb, 12, 6, shadow=26)
o += f'<rect x="96" y="76" width="708" height="408" rx="14" fill="{RK}"/><rect x="110" y="90" width="680" height="380" rx="8" fill="{BL}"/>'
o += f'<clipPath id="tv"><rect x="110" y="90" width="680" height="380" rx="8"/></clipPath><g clip-path="url(#tv)">'
o += f'<rect x="110" y="90" width="680" height="190" fill="{BL3}" opacity=".45"/>'
for k in range(20): o += f'<path d="M110 {110+k*19}H790" stroke="{RK}" stroke-width="1.2" opacity=".18"/>'
o += ln('M110 250C230 190 330 270 460 210S690 240 790 190', BL3, 3, .8)
o += f'<circle cx="450" cy="190" r="70" fill="{R}" stroke="{RK}" stroke-width="6"/><path d="M428 150L488 190L428 230Z" fill="{RK}"/>' + ln('M392 166A70 70 0 0 1 424 130', RL, 6, .9)
for k in range(5):
    o += f'<rect x="{138+k*130}" y="340" width="112" height="96" rx="5" fill="{BL2}" stroke="{RK}" stroke-width="3"/>' + f'<path d="M{138+k*130} 436l30 -34 20 18 28 -40 34 56z" fill="{BL3}" opacity=".45"/>'
o += f'<rect x="138" y="318" width="120" height="8" fill="{R}"/></g>'
o += ln('M100 100C100 60 140 56 180 56H300', RL, 5, .85) + f'<circle cx="780" cy="500" r="7" fill="{RK}"/><circle cx="756" cy="500" r="7" fill="{RDD}" stroke="{RK}" stroke-width="2"/>'
H['pantalla'] = svg('Pantalla con catálogo', 900, 640, o, 40)

# ---------- 6 · JOYSTICK ARCADE (catálogo) ----------
o = ''
base = 'M60 520L110 360H590L640 520Z'
o += f'<ellipse cx="350" cy="560" rx="310" ry="34" fill="{NV}" opacity=".9" transform="translate(16 12)"/>'
o += vol(rr(60, 500, 580, 70, 14), 8, 5, base=RD, dark=RDD)
o += vol(base, 12, 6, shadow=0)
o += vol(rr(110, 340, 480, 44, 12), 6, 5, base='#ff5a45')
o += ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{RK}"/>' for x, y in [(138, 362), (562, 362), (84, 500), (616, 500)])
o += ln('M120 440H580M100 480H600', RDD, 3, .8)
o += f'<ellipse cx="350" cy="352" rx="82" ry="22" fill="{RK}"/>' + vol(ell(350, 340, 70, 17), 4, 4, base=RD, dark=RDD)
o += vol(rr(332, 120, 36, 230, 10), 6, 5, base=R, dark=RDD)
o += ln('M342 140V330', RL, 4, .8)
o += vol(ell(350, 96, 90, 90), 18, 6, shadow=0)
o += ln('M290 64C304 44 330 34 354 36', RL, 10, .9) + ln('M392 150A86 86 0 0 0 428 108', RDD, 5, .6)
for cx, col in [(180, 0), (260, 1), (440, 1), (520, 0)]:
    o += f'<circle cx="{cx}" cy="440" r="30" fill="{RK}"/>' + vol(ell(cx, 436, 22, 22), 5, 4, base=R if col else RL, dark=RD, hatch=False)
o += ln('M110 400H250M450 400H590', RK, 4, .7)
H['joystick'] = svg('Joystick arcade', 700, 600, o, 40)

# ---------- 7 · CLAQUETA (streaming) ----------
o = ''
o += vol(rr(80, 250, 700, 360, 22), 12, 6, shadow=24)
o += f'<rect x="110" y="320" width="640" height="26" rx="4" fill="{RK}"/><rect x="110" y="368" width="420" height="16" rx="4" fill="{RDD}" stroke="{RK}" stroke-width="3"/>'
for k in range(3): o += f'<rect x="{110+k*214}" y="414" width="196" height="150" rx="6" fill="{RD}" stroke="{RK}" stroke-width="4"/>' + ln(f'M{128+k*214} 450H{286+k*214}M{128+k*214} 480H{250+k*214}', RK, 5, .85)
o += ''.join(f'<path d="M{110+k*214} 398H{306+k*214}" stroke="{RL}" stroke-width="3" opacity=".7"/>' for k in range(3))
# brazo superior (inclinado)
arm = 'M70 230L146 90L786 170L770 252Z'
o += f'<g transform="rotate(-10 90 236)">' + vol('M70 190H790V252H70Z', 8, 6, shadow=18)
for k in range(9):
    x = 100 + k * 76
    o += f'<path d="M{x} 190l44 0l-30 62h-44z" fill="{RK}"/>'
o += f'<path d="M70 190H790V252H70Z" fill="none" stroke="{RK}" stroke-width="6" stroke-linejoin="round"/>' + ln('M80 204H780', RL, 4, .7) + '</g>'
# brazo fijo superior de la tabla
o += f'<path d="M80 252H780V288H80Z" fill="{RD}" stroke="{RK}" stroke-width="6" stroke-linejoin="round"/>'
for k in range(9):
    x = 96 + k * 76
    o += f'<path d="M{x} 252l44 0l-26 36h-44z" fill="{RK}"/>'
o += f'<circle cx="104" cy="240" r="22" fill="{RK}"/><circle cx="104" cy="240" r="12" fill="{RL}"/>'
# sello play
o += f'<circle cx="716" cy="590" r="64" fill="{RK}"/>' + vol(ell(716, 584, 52, 52), 6, 5, base=R) + '<path d="M700 556L742 584L700 612Z" fill="%s"/>' % RK
H['claqueta'] = svg('Claqueta', 880, 700, o, 40)

# ---------- 8 · GPU (IA) ----------
o = ''
card = 'M70 70H930V420H70Z'
o += f'<rect x="40" y="40" width="40" height="410" rx="6" fill="{RK}" transform="translate(18 20)"/>'
o += vol(card, 12, 6, shadow=24)
o += vol(rr(20, 40, 52, 420, 8), 6, 5, base=RL, dark=RD, hatch=False) + ''.join(f'<rect x="32" y="{70+k*38}" width="28" height="18" rx="3" fill="{RK}"/>' for k in range(8))
o += ''.join(f'<rect x="{150+k*26}" y="420" width="14" height="50" fill="{RL}" stroke="{RK}" stroke-width="3"/>' for k in range(26))
for cx in (330, 700):
    o += f'<circle cx="{cx}" cy="245" r="140" fill="{RK}"/><circle cx="{cx}" cy="245" r="124" fill="{RDD}" stroke="{RK}" stroke-width="4"/>'
    for a in range(0, 360, 360 // 9):
        r0, r1 = math.radians(a), math.radians(a + 38)
        x1, y1, x2, y2 = cx + 24 * math.cos(r0), 245 + 24 * math.sin(r0), cx + 116 * math.cos(r1), 245 + 116 * math.sin(r1)
        bd = f'M{f(cx)} 245L{f(cx+112*math.cos(r0-.35))} {f(245+112*math.sin(r0-.35))}A112 112 0 0 1 {f(cx+112*math.cos(r0+.35))} {f(245+112*math.sin(r0+.35))}Z'
        o += vol(bd, 4, 3, base=R, dark=RD, hatch=False)
    o += vol(ell(cx, 245, 34, 34), 5, 4, base=RL, dark=RD, hatch=False) + f'<circle cx="{cx}" cy="245" r="10" fill="{RK}"/>'
    o += f'<circle cx="{cx}" cy="245" r="140" fill="none" stroke="{RL}" stroke-width="3" stroke-dasharray="2 14" opacity=".8"/>'
o += vol(rr(468, 90, 64, 310, 8), 4, 4, base=RD, dark=RDD, hatch=False) + ''.join(ln(f'M476 {110+k*30}H524', RK, 4, .8) for k in range(10))
o += f'<rect x="800" y="86" width="104" height="22" rx="4" fill="{RK}"/><rect x="800" y="130" width="64" height="10" rx="3" fill="{RDD}"/>'
o += ln('M110 96H300M720 96H780', RL, 5, .8)
H['gpu'] = svg('Tarjeta gráfica', 960, 520, o, 40)

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '../assets/heroes'
    os.makedirs(out, exist_ok=True)
    for k, v in H.items():
        open(os.path.join(out, f'heroe-{k}.svg'), 'w').write(strip(v)); print(k, len(v))
