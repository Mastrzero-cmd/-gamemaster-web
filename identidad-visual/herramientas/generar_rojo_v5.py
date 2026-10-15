#!/usr/bin/env python3
"""v5 · piezas rojas NUEVAS (SVG) para ir ADELANTE del azul: contorno negro duro, sombra de capa azul noche, grabado fino rojo.
Sin personajes, sin texto dentro del SVG. Uso: python3 generar_rojo_v5.py ../assets/piezas"""
import sys, os, math
R, RD, RL, RK, NV, CY, MG = '#ff3322', '#d11a10', '#ff8f7d', '#05071f', '#2a3cff', '#3fdcff', '#ff3b7f'
ENG = '#7a0a05'
st = f'stroke="{RK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')

def svg(name, w, h, sil, body):
    defs = (f'<defs><pattern id="hc" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><path d="M0 0H5" stroke="#6e0903" stroke-width="1.2"/></pattern>'
            f'<linearGradient id="fd" x1="0" y1="0" x2="0" y2="1"><stop offset=".4" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>'
            f'<mask id="mk"><rect width="{w}" height="{h}" fill="url(#fd)"/></mask><clipPath id="cp"><path d="{sil}"/></clipPath></defs>')
    shadow = f'<path d="{sil}" fill="#0a1148" opacity=".6" transform="translate(9 10)"/><path d="{sil}" fill="none" stroke="{MG}" stroke-width="3" stroke-linejoin="round" transform="translate(6 6)" opacity=".7"/>'
    eng = (f'<g clip-path="url(#cp)"><rect width="{w}" height="{h}" fill="url(#hc)" mask="url(#mk)" opacity=".5"/>'
           f'<path d="{sil}" fill="none" stroke="#ffd9d2" stroke-width="5" stroke-linejoin="round" opacity=".5" transform="translate(-3 -3)"/>'
           f'<path d="{sil}" fill="none" stroke="{ENG}" stroke-width="3" stroke-linejoin="round" opacity=".45" transform="translate(4 5)"/></g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{name}"><title>{name}</title>{defs}{shadow}{body}{eng}</svg>')

def S(d, fill=R, extra=''):
    a = {'stroke': RK, 'stroke-width': '5', 'stroke-linejoin': 'round', 'stroke-linecap': 'round'}
    import re
    for k, v in re.findall(r'([\w-]+)="([^"]*)"', extra): a[k] = v
    return f'<path d="{d}" fill="{fill}" ' + ' '.join(f'{k}="{v}"' for k, v in a.items()) + '/>'
def C(x, y, r, fill=R, sw=5): return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{RK}" stroke-width="{sw}"/>'
def RR(x, y, w, h, rx, fill=R, sw=5): return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}" stroke="{RK}" stroke-width="{sw}" stroke-linejoin="round"/>'
def LN(d, c=RK, w=4, o=1): return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{o}"/>'
def star4(cx, cy, r, k=.28):
    p = []
    for i in range(8):
        a = math.radians(-90 + i * 45); rr = r if i % 2 == 0 else r * k; p.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in p) + 'Z'

P = {}
# consola de sobremesa
sil = 'M20 100Q20 66 54 66H346Q380 66 380 100V196Q380 230 346 230H54Q20 230 20 196Z'
P['consola'] = svg('Consola de sobremesa', 400, 270, sil, S(sil) + RR(46, 112, 220, 24, 8, RK, 4) + C(318, 124, 22, RD) + LN('M308 124h20M318 114v20', RL, 4)
    + ''.join(LN(f'M{50+k*26} 184h14', RK, 5) for k in range(8)) + C(300, 188, 9, RL, 3) + C(332, 188, 9, RL, 3) + LN('M44 86H340', RL, 6, .8))
# joystick arcade
sil = 'M102 70a48 48 0 1 0 96 0a48 48 0 1 0 -96 0Z M138 110H162V230H138Z M26 316L58 218H242L274 316Z'
P['joystick'] = svg('Joystick arcade', 300, 340, sil, S('M138 110H162V230H138Z', RD) + S('M26 316L58 218H242L274 316Z') + C(90, 276, 17, RL) + C(150, 276, 17, RD) + C(210, 276, 17, RL)
    + C(150, 70, 48) + LN('M122 52C130 38 146 32 160 36', RL, 7, .85) + LN('M40 296H260', RK, 4, .6))
# teclado
sil = 'M44 64H396L430 194H10Z'
keys = ''.join(RR(40 + r * 14 + c * 38 - (r * 0), 78 + r * 34, 30, 24, 5, RD if (r + c) % 3 else RL, 3) for r in range(3) for c in range(9))
P['teclado'] = svg('Teclado', 440, 220, sil, S(sil) + keys + RR(120, 172, 190, 20, 6, RL, 3) + LN('M56 76H386', RL, 5, .7))
# ratón
sil = 'M100 20C40 20 24 80 24 150C24 230 50 284 100 284C150 284 176 230 176 150C176 80 160 20 100 20Z'
P['raton'] = svg('Ratón', 200, 304, sil, S(sil) + LN('M100 22V132M26 132H174', RK, 5) + RR(89, 56, 22, 46, 10, RK, 3) + LN('M52 60C64 42 80 34 92 32', RL, 7, .85) + S('M30 150C40 250 70 280 100 284C60 262 40 220 30 150Z', RD, 'opacity=".5"'))
# tarjeta gráfica
sil = 'M10 40H430V190H10Z M0 28H28V206H0Z'
fan = lambda cx: C(cx, 115, 54, RD) + ''.join(LN(f'M{cx} 115L{f(cx+46*math.cos(math.radians(a)))} {f(115+46*math.sin(math.radians(a)))}', RK, 5) for a in range(0, 360, 60)) + C(cx, 115, 12, RL, 4)
P['gpu'] = svg('Tarjeta gráfica', 440, 232, sil, S('M10 40H430V190H10Z') + fan(122) + fan(300) + RR(0, 28, 26, 178, 4, RL) + ''.join(f'<rect x="{50+k*18}" y="196" width="10" height="20" fill="{RL}" stroke="{RK}" stroke-width="3"/>' for k in range(16)) + LN('M44 54H410', RL, 5, .7) + RR(378, 70, 40, 34, 4, RK, 3))
# disco
sil = 'M20 140a120 120 0 1 0 240 0a120 120 0 1 0 -240 0Z'
P['disco'] = svg('Disco', 280, 280, sil, C(140, 140, 120) + C(140, 140, 96, RD, 3) + C(140, 140, 68, R, 3) + C(140, 140, 44, RL) + C(140, 140, 14, NV, 4) + LN('M50 90A104 104 0 0 1 120 38', RL, 8, .9) + LN('M232 190A104 104 0 0 1 170 242', ENG, 6, .6))
# bocina
sil = 'M44 24H176Q196 24 196 44V296Q196 316 176 316H44Q24 316 24 296V44Q24 24 44 24Z'
P['bocina'] = svg('Bocina', 220, 340, sil, S(sil) + C(110, 84, 30, RD) + C(110, 84, 10, RL, 4) + C(110, 220, 66, RD) + C(110, 220, 44, R, 4) + C(110, 220, 16, RK, 3) + LN('M52 44H90', RL, 6, .85)
    + ''.join(C(60 + k * 25, 300, 4, RK, 2) for k in range(6)))
# servidor / nube
sil = 'M26 24H354V96H26Z M26 112H354V184H26Z M26 200H354V272H26Z'
unit = lambda y: RR(26, y, 328, 72, 12) + RR(46, y + 20, 180, 14, 6, RK, 3) + RR(46, y + 42, 120, 10, 5, RD, 3) + C(290, y + 36, 9, RL, 3) + C(322, y + 36, 9, NV, 3)
P['servidor'] = svg('Servidor', 380, 296, sil, unit(24) + unit(112) + unit(200))
# cursor
sil = 'M26 14L26 206L72 164L106 240L142 224L108 150L168 150Z'
P['cursor'] = svg('Cursor', 200, 262, sil, S(sil, R, 'stroke-width="8"') + LN('M40 50V170', RL, 6, .8) + LN('M150 40A40 40 0 0 1 188 78', NV, 6, .9) + LN('M146 14A66 66 0 0 1 198 70', NV, 5, .6))
# flecha
sil = 'M12 72H222V22L352 100L222 178V128H12Z'
P['flecha'] = svg('Flecha', 364, 200, sil, S(sil) + LN('M38 100H196M232 52L312 100L232 148', RD, 8, .85) + LN('M26 84H210', RL, 6, .8))
# etiqueta (tag) con ojal
sil = 'M18 22H214L284 80L214 138H18Z'
P['etiqueta'] = svg('Etiqueta', 300, 160, sil, S(sil) + C(62, 80, 12, NV, 4) + LN('M96 56H196M96 80H226M96 104H190', RD, 6, .8) + LN('M30 36H204', RL, 5, .7))
# sello / insignia
n = 16; pts = []
for i in range(n * 2):
    a = math.radians(-90 + i * 180 / n); rr = 112 if i % 2 == 0 else 96; pts.append((120 + math.cos(a) * rr, 120 + math.sin(a) * rr))
sil = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z'
P['sello'] = svg('Sello', 240, 240, sil, S(sil) + C(120, 120, 74, RD, 4) + C(120, 120, 62, R, 3) + S(star4(120, 120, 46, .42), RL, 'stroke-width="4"') + LN('M62 70A70 70 0 0 1 112 44', RL, 6, .8))
# estrella de 4 puntas
sil = star4(60, 60, 54, .26)
P['estrella'] = svg('Estrella', 120, 120, sil, S(sil, R, 'stroke-width="5"'))
# botón arcade
sil = 'M14 140a108 100 0 1 0 216 0a108 100 0 1 0 -216 0Z'
P['boton'] = svg('Botón', 240, 250, sil, S('M16 140C16 200 62 244 122 244C182 244 228 200 228 140Z', RD) + C(122, 128, 106, R) + C(122, 120, 78, RL, 3) + LN('M46 96A86 86 0 0 1 112 40', '#fff', 8, .55) + LN('M178 170A70 70 0 0 1 120 198', ENG, 6, .6))
# play triangular (cinta streaming) y cartucho doble ya existen; control remoto
sil = 'M70 20H150Q172 20 172 42V318Q172 340 150 340H70Q48 340 48 318V42Q48 20 70 20Z'
P['control'] = svg('Control remoto', 220, 360, sil, S(sil) + C(110, 90, 30, RD) + LN('M110 70V110M90 90H130', RK, 4) + C(110, 170, 22, RL) + ''.join(C(84 + (k % 2) * 52, 224 + (k // 2) * 40, 11, RD, 3) for k in range(4)) + RR(78, 306, 64, 14, 6, RK, 3) + LN('M62 42H92', RL, 6, .85))
# micrófono
sil = 'M120 14a52 52 0 0 0 -52 52V150a52 52 0 0 0 104 0V66a52 52 0 0 0 -52 -52Z M118 190H122V254H118Z M64 270H176V292H64Z'
P['microfono'] = svg('Micrófono', 240, 310, sil, S('M118 190H122V254H118Z', RD) + S('M64 270H176V292H64Z', RD) + LN('M40 130V150A80 80 0 0 0 200 150V130', RK, 12) + LN('M40 130V150A80 80 0 0 0 200 150V130', R, 5)
    + S('M120 14a52 52 0 0 0 -52 52V150a52 52 0 0 0 104 0V66a52 52 0 0 0 -52 -52Z') + ''.join(LN(f'M72 {60+k*24}H168', RK, 3, .55) for k in range(4)) + LN('M84 46C88 32 100 26 112 26', RL, 7, .85))
# cinta/listón en chevrones (sin texto)
sil = 'M10 30H330L310 70L330 110H10L30 70Z'
P['cinta'] = svg('Cinta', 340, 140, sil, S(sil) + ''.join(S(f'M{60+k*58} 38L{92+k*58} 70L{60+k*58} 102', 'none', 'stroke-width="9" stroke="#8e0e07"') for k in range(4)) + LN('M40 42H300', RL, 5, .75))

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    tot = 0
    for k, v in P.items():
        open(os.path.join(out, f'pieza-{k}.svg'), 'w').write(v); tot += len(v)
    print(len(P), 'piezas', tot // 1024, 'KB')
