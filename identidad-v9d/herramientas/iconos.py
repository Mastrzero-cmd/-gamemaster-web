#!/usr/bin/env python3
"""Íconos rojos de v9d «Póster psicodélico». Cada ícono: masa roja plana (#FF1A1A) con contorno negro (#050505) y detalles negros.
Nunca azul. Sin degradados, blur ni opacidad. Lienzo 400x400."""
import math
R, K = '#FF1A1A', '#050505'
SW = 12
def S(d, extra=''): return f'<path d="{d}" fill="{R}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'
def Kp(d, extra=''): return f'<path d="{d}" fill="{K}" {extra}/>'
def Kl(d, w=8): return f'<path d="{d}" fill="none" stroke="{K}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def Rl(d, w=6): return f'<path d="{d}" fill="none" stroke="{R}" stroke-width="{w}" stroke-linecap="round"/>'
def circ(x, y, r, fill=K, stroke=''): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {stroke}/>'
def ell(x, y, rx, ry, rot=0, fill=R, stroke=True):
    st = f'stroke="{K}" stroke-width="{SW}"' if stroke else ''
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({rot} {x} {y})" fill="{fill}" {st}/>'
def poly(pts, fill=R, stroke=True):
    st = f'stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"' if stroke else ''
    return f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="{fill}" {st}/>'
def star_pts(cx, cy, ro, ri, n=5, rot=-90):
    return [(round(cx + (ro if i % 2 == 0 else ri) * math.cos(math.radians(rot + i * 180 / n)), 1), round(cy + (ro if i % 2 == 0 else ri) * math.sin(math.radians(rot + i * 180 / n)), 1)) for i in range(2 * n)]

def hongo():
    return ''.join([
        S('M30 250 C20 120 110 30 200 30 C290 30 380 120 370 250 C340 275 60 275 30 250 Z'),
        S('M105 262 L105 318 C105 362 148 382 200 382 C252 382 295 362 295 318 L295 262 Z'),
        '<clipPath id="hc"><path d="M30 250 C20 120 110 30 200 30 C290 30 380 120 370 250 C340 275 60 275 30 250 Z"/></clipPath>',
        f'<g clip-path="url(#hc)">{circ(200,100,48)}{circ(52,196,52)}{circ(348,196,52)}{circ(120,246,26)}{circ(280,246,26)}</g>',
        ell(166, 316, 15, 34, 0, K, False), ell(234, 316, 15, 34, 0, K, False),
        Kl('M130 300 C150 292 175 292 195 300', 0), Kl('M62 120 C90 70 130 50 160 44', 7),
    ])
def triforce():
    def sh(p, k=.9):
        cx = sum(x for x, _ in p) / 3; cy = sum(y for _, y in p) / 3
        return [(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in p]
    t = [[(200, 10), (385, 380), (15, 380)]]
    top = [(200, 10), (293, 195), (107, 195)]; bl = [(107, 195), (200, 380), (15, 380)]; br = [(293, 195), (385, 380), (200, 380)]
    return ''.join(poly(sh(p, .93)) for p in (top, bl, br)) + Kl('M200 56 L200 120', 6) + Kl('M107 250 L60 340', 6) + Kl('M293 250 L340 340', 6)
def pikachu():
    return ''.join([
        S('M276 340 L350 336 L322 280 L392 270 L350 190 L398 40 L290 172 L328 176 L262 256 L300 262 Z'),
        S('M110 120 C96 84 84 44 66 6 C118 18 168 56 182 108 Z'), S('M290 120 C306 78 318 38 344 0 C282 14 236 56 222 108 Z'),
        Kp('M66 6 C84 10 100 18 112 28 L90 70 C84 46 76 26 66 6 Z'), Kp('M344 0 C324 4 308 12 296 22 L316 64 C324 44 334 22 344 0 Z'),
        S('M200 372 C120 372 98 322 104 268 C108 224 140 204 200 204 C260 204 292 224 296 268 C302 322 280 372 200 372 Z'),
        S('M200 232 C110 232 66 190 66 148 C66 96 126 66 200 66 C274 66 334 96 334 148 C334 190 290 232 200 232 Z'),
        circ(148, 140, 14), circ(252, 140, 14), circ(144, 135, 5, R), circ(248, 135, 5, R),
        circ(104, 188, 22), circ(296, 188, 22),
        Kp('M192 164 L208 164 L200 174 Z'), Kl('M168 188 C180 206 194 206 200 190 C206 206 220 206 232 188', 6),
        S('M118 372 C104 372 100 352 118 346 C150 342 164 352 164 362 C164 372 140 376 118 372 Z'), S('M282 372 C296 372 300 352 282 346 C250 342 236 352 236 362 C236 372 260 376 282 372 Z'),
        Kl('M104 268 C130 292 160 296 188 286', 6), Kl('M296 268 C270 292 240 296 212 286', 6),
    ])
def kirby():
    return ''.join([
        ell(62, 236, 56, 40, 24), ell(346, 150, 56, 38, -52),
        ell(120, 352, 70, 38, -12), ell(290, 352, 70, 38, 12),
        S('M200 56 C300 56 352 130 352 214 C352 300 290 360 200 360 C110 360 48 300 48 214 C48 130 100 56 200 56 Z'),
        ell(164, 166, 16, 42, 0, K, False), ell(236, 166, 16, 42, 0, K, False),
        ell(164, 148, 7, 14, 0, R, False), ell(236, 148, 7, 14, 0, R, False),
        ell(104, 236, 28, 15, 0, K, False), ell(296, 236, 28, 15, 0, K, False),
        Kp('M176 252 C176 232 224 232 224 252 C224 286 176 286 176 252 Z'),
        Kl('M90 120 C110 90 140 72 170 66', 6),
    ])
def anillo():
    o = 'M200 24 C296 24 350 90 350 190 C350 290 290 372 200 372 C110 372 50 290 50 190 C50 90 104 24 200 24 Z'
    i = 'M200 104 C150 104 112 144 112 196 C112 250 150 296 200 296 C250 296 288 250 288 196 C288 144 250 104 200 104 Z'
    return ''.join([f'<g transform="translate(34 16)"><path d="{o} {i}" fill-rule="evenodd" fill="{K}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/></g>',
        f'<g transform="translate(-14 -2)"><path fill-rule="evenodd" d="{o} {i}" fill="{R}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/></g>',
        Kl('M70 120 C86 80 120 50 160 40', 10), Kl('M250 40 C270 46 284 56 296 70', 6)])
def pokebola():
    return ''.join([
        f'<circle cx="200" cy="200" r="168" fill="{K}"/>',
        '<clipPath id="pb"><circle cx="200" cy="200" r="168"/></clipPath>',
        f'<g clip-path="url(#pb)"><rect x="20" y="20" width="360" height="164" fill="{R}"/>' + ''.join(Rl(f'M{200-r} 214 A{r} {r} 0 0 0 {200+r} 214', 6) for r in (70,106,142,172)) + '</g>',
        f'<circle cx="200" cy="200" r="168" fill="none" stroke="{R}" stroke-width="0"/>',
        Kp('M20 184 L380 184 L380 216 L20 216 Z'),
        S('M200 150 C228 150 250 172 250 200 C250 228 228 250 200 250 C172 250 150 228 150 200 C150 172 172 150 200 150 Z'),
        circ(200, 200, 18), Kl('M64 110 C88 70 126 46 168 38', 9),
    ])
def corazon():
    return ''.join([S('M200 366 C70 270 20 200 20 124 C20 62 66 28 116 28 C154 28 184 48 200 82 C216 48 246 28 284 28 C334 28 380 62 380 124 C380 200 330 270 200 366 Z'),
                    Kl('M62 120 C62 90 82 70 108 68', 12)])
def espada():
    return ''.join([
        S('M200 6 L232 60 L232 250 L168 250 L168 60 Z'), Kl('M200 24 L200 244', 6),
        S('M60 232 C70 210 120 218 168 250 L232 250 C280 218 330 210 340 232 C340 262 300 276 232 276 L168 276 C100 276 60 262 60 232 Z'),
        S('M176 276 L224 276 L224 344 L176 344 Z'), Kl('M176 296 L224 296', 6), Kl('M176 316 L224 316', 6),
        S('M200 344 C224 344 236 358 236 372 C236 388 220 394 200 394 C180 394 164 388 164 372 C164 358 176 344 200 344 Z'), circ(200, 370, 10),
        circ(200, 252, 12),
    ])
def invasor():
    rows = ['00100000100', '00010001000', '00111111100', '01101110110', '11111111111', '10111111101', '10100000101', '00011011000']
    out = []
    u = 34
    ox, oy = 13, 64
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c == '1': out.append(f'<rect x="{ox+i*u}" y="{oy+j*u}" width="{u}" height="{u}" fill="{R}"/>')
    # borde negro fino alrededor: se logra con un trazo del silueta por rect negro debajo
    under = ''.join(f'<rect x="{ox+i*u-5}" y="{oy+j*u-5}" width="{u+10}" height="{u+10}" fill="{K}"/>' for j, r in enumerate(rows) for i, c in enumerate(r) if c == '1')
    eyes = ''.join(f'<rect x="{ox+i*u}" y="{oy+j*u}" width="{u}" height="{u}" fill="{K}"/>' for (i, j) in [(3, 3), (7, 3)])
    return under + ''.join(out) + eyes
def pacman():
    return ''.join([S('M200 200 L370 120 C340 40 280 24 200 24 C100 24 30 100 30 200 C30 300 100 376 200 376 C280 376 340 360 370 280 Z'), circ(222, 100, 18),
                    Kl('M60 150 C70 110 100 80 140 62', 8)])
def fantasma():
    return ''.join([S('M40 372 L40 190 C40 90 110 28 200 28 C290 28 360 90 360 190 L360 372 L310 330 L255 372 L200 330 L145 372 L90 330 Z'),
                    ell(142, 180, 36, 44, 0, K, False), ell(258, 180, 36, 44, 0, K, False), circ(152, 190, 16, R), circ(268, 190, 16, R)])
def bloque():
    return ''.join([S('M50 30 L350 30 C362 30 370 38 370 50 L370 350 C370 362 362 370 350 370 L50 370 C38 370 30 362 30 350 L30 50 C30 38 38 30 50 30 Z'),
                    circ(66, 66, 11), circ(334, 66, 11), circ(66, 334, 11), circ(334, 334, 11),
                    Kl('M146 150 C146 70 256 70 256 142 C256 190 200 190 200 242', 34), circ(200, 308, 22)])
def creeper():
    u = 44; px = [(1,2),(2,2),(1,3),(2,3),(5,2),(6,2),(5,3),(6,3),(3,4),(4,4),(2,5),(3,5),(4,5),(5,5),(2,6),(3,6),(4,6),(5,6),(2,7),(5,7)]
    base = S('M24 24 L376 24 L376 376 L24 376 Z')
    return base + ''.join(f'<rect x="{24+i*u}" y="{24+(j-1)*u}" width="{u}" height="{u}" fill="{K}"/>' for i, j in px)
def estrella():
    return ''.join([poly(star_pts(200, 206, 180, 80)), ell(176, 196, 12, 30, 0, K, False), ell(224, 196, 12, 30, 0, K, False)])
def mando():
    return ''.join([S('M110 110 L290 110 C350 110 392 180 392 262 C392 330 360 352 332 330 C300 304 290 280 270 262 L130 262 C110 280 100 304 68 330 C40 352 8 330 8 262 C8 180 50 110 110 110 Z'),
                    Kp('M92 160 L112 160 L112 182 L134 182 L134 204 L112 204 L112 226 L92 226 L92 204 L70 204 L70 182 L92 182 Z'),
                    circ(290, 170, 17), circ(332, 204, 17), circ(248, 204, 17), circ(290, 238, 17), Kl('M165 190 L235 190', 10)])
def tv():
    return ''.join([Kl('M150 100 L96 24', 12), Kl('M250 100 L304 24', 12), circ(96, 24, 10, R, f'stroke="{K}" stroke-width="6"'), circ(304, 24, 10, R, f'stroke="{K}" stroke-width="6"'),
                    S('M52 100 L348 100 C366 100 378 112 378 130 L378 328 C378 346 366 358 348 358 L52 358 C34 358 22 346 22 328 L22 130 C22 112 34 100 52 100 Z'),
                    f'<path d="M60 134 C60 128 64 124 70 124 L252 124 C258 124 262 128 262 134 L262 324 C262 330 258 334 252 334 L70 334 C64 334 60 330 60 324 Z" fill="{K}"/>',
                    f'<path d="M120 170 L120 288 L214 229 Z" fill="{R}"/>', circ(318, 170, 24), circ(318, 250, 24), Kl('M298 310 L338 310', 6),
                    Kl('M92 372 L92 392', 12), Kl('M308 372 L308 392', 12)])
def play():
    return S('M50 20 L370 200 L50 380 Z') + Kl('M96 100 L96 300', 0)
def robot():
    return ''.join([Kl('M200 76 L200 30', 12), circ(200, 24, 18, R, f'stroke="{K}" stroke-width="8"'),
                    S('M90 76 L310 76 C340 76 360 96 360 126 L360 270 C360 300 340 320 310 320 L90 320 C60 320 40 300 40 270 L40 126 C40 96 60 76 90 76 Z'),
                    S('M40 150 L12 150 L12 250 L40 250 Z'), S('M360 150 L388 150 L388 250 L360 250 Z'),
                    f'<path d="M84 128 L316 128 C328 128 336 136 336 148 L336 192 C336 204 328 212 316 212 L84 212 C72 212 64 204 64 192 L64 148 C64 136 72 128 84 128 Z" fill="{K}"/>',
                    circ(140, 170, 26, R), circ(260, 170, 26, R), circ(133, 163, 7, K), circ(253, 163, 7, K), Kl('M110 262 L290 262', 10), Kl('M140 288 L260 288', 6),
                    S('M140 320 L140 372 L260 372 L260 320')])
def destello():
    return S('M200 12 C214 120 280 186 388 200 C280 214 214 280 200 388 C186 280 120 214 12 200 C120 186 186 120 200 12 Z')

ICONOS = dict(hongo=hongo, triforce=triforce, pikachu=pikachu, kirby=kirby, anillo=anillo, pokebola=pokebola, corazon=corazon, espada=espada,
              invasor=invasor, pacman=pacman, fantasma=fantasma, bloque=bloque, creeper=creeper, estrella=estrella, mando=mando, tv=tv, play=play, robot=robot, destello=destello)
NOMBRES = dict(hongo='Hongo', triforce='Trifuerza', pikachu='Silueta eléctrica', kirby='Bolita rosa', anillo='Anillo dorado', pokebola='Bola de captura', corazon='Corazón de aventura', espada='Espada legendaria',
               invasor='Invasor espacial', pacman='Comecocos', fantasma='Fantasma', bloque='Bloque de pregunta', creeper='Creeper', estrella='Estrella', mando='Mando', tv='Tele retro', play='Play', robot='Robot', destello='Destello IA')
def svg(name, size=400):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="{size}" height="{size}">{ICONOS[name]()}</svg>'
if __name__ == '__main__':
    import os
    d = os.path.join(os.path.dirname(__file__), '..', 'assets', 'iconos'); os.makedirs(d, exist_ok=True)
    for n in ICONOS: open(os.path.join(d, n + '.svg'), 'w').write(svg(n))
    # hoja de prueba sobre azul
    cells = ''
    for i, n in enumerate(ICONOS):
        x, y = (i % 5) * 300, (i // 5) * 300
        cells += f'<g transform="translate({x+20} {y+20}) scale(.65)">{ICONOS[n]()}</g>'
    open('/workspace/scratch/hoja_iconos.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1200" width="1500" height="1200"><rect width="1500" height="1200" fill="#1616FF"/>{cells}</svg>')
