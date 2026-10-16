"""Íconos-sello rojos (v9a «Grabado»). Cada ícono: viewBox 0 0 200 200, masa roja con borde negro grueso y detalles en negro.
Solo rojo (#FF1A1A) y negro (#050505): nunca azul."""
import math
R, K = '#FF1A1A', '#050505'
def P(d, fill=R, sw=0, stroke=K, extra=''):
    return f'<path d="{d}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if sw else '') + f' {extra}/>'
def mass(d):  # masa roja con contorno negro grueso detrás
    return f'<path d="{d}" fill="{K}" stroke="{K}" stroke-width="16" stroke-linejoin="round"/>' + f'<path d="{d}" fill="{R}"/>'
def circ(cx, cy, r, fill=R): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
def ell(cx, cy, rx, ry, fill=K): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"/>'
def line(d, w=10, c=K): return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def rect(x, y, w, h, fill=R, rx=0): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'

def triforce():
    t = ['M100 14L58 90L142 90Z', 'M16 166L100 166L58 90Z', 'M100 166L184 166L142 90Z']
    return ''.join(mass(d) for d in t)
def seta():  # hongo
    cap = 'M14 112C14 56 52 22 100 22C148 22 186 56 186 112C186 122 178 126 168 126L32 126C22 126 14 122 14 112Z'
    stem = 'M52 126L148 126C148 150 140 176 124 182L76 182C60 176 52 150 52 126Z'
    return (mass(stem) + mass(cap) + circ(100, 62, 22, K) + ell(44, 100, 16, 18) + ell(156, 100, 16, 18)
            + ell(84, 150, 7, 14) + ell(116, 150, 7, 14) + line('M30 126L170 126', 7))
def pokebola():
    return (f'<circle cx="100" cy="100" r="88" fill="{K}"/>'
            + f'<path d="M12 100A88 88 0 0 1 188 100Z" fill="{R}"/>'
            + f'<path d="M12 100A88 88 0 0 0 188 100Z" fill="{K}" stroke="{R}" stroke-width="9" stroke-linejoin="round"/>'
            + f'<circle cx="100" cy="100" r="88" fill="none" stroke="{R}" stroke-width="9"/>'
            + rect(8, 90, 184, 20, K) + circ(100, 100, 30, K) + circ(100, 100, 21, R) + circ(100, 100, 10, K)
            + f'<path d="M44 66A62 62 0 0 1 82 38" fill="none" stroke="{K}" stroke-width="8" stroke-linecap="round"/>')
def pikachu():
    def oreja(sx):  # sx=-1 izquierda, 1 derecha; hoja larga con punta negra
        def X(x): return 100 + sx * (x - 100)
        d = f'M{X(66)} 84C{X(50)} 60 {X(40)} 30 {X(40)} 6C{X(60)} 10 {X(84)} 40 {X(94)} 74Z'
        tip = f'M{X(40)} 6C{X(52)} 8 {X(66)} 20 {X(74)} 36L{X(52)} 38C{X(44)} 28 {X(40)} 18 {X(40)} 6Z'
        return d, tip
    out = ''; tips = ''
    for sx in (-1, 1):
        d, t = oreja(sx); out += mass(d); tips += f'<path d="{t}" fill="{K}"/>'
    tail = 'M168 156L192 128L178 122L204 88L184 84L206 52L160 108L178 114Z'
    head = 'M100 62C150 62 184 90 184 126C184 160 148 184 100 184C52 184 16 160 16 126C16 90 50 62 100 62Z'
    return (mass(tail) + out + mass(head) + tips
            + circ(66, 112, 12, K) + circ(134, 112, 12, K) + circ(70, 107, 4.5, R) + circ(138, 107, 4.5, R)
            + circ(34, 148, 17, K) + circ(166, 148, 17, K) + circ(34, 148, 8, R) + circ(166, 148, 8, R)
            + P('M92 128L108 128L100 138Z', K) + f'<path d="M80 144Q100 168 120 144Z" fill="{K}"/>' + line('M100 138L100 146', 5))

def corazon():
    d = 'M100 178C40 134 14 100 14 66C14 38 34 22 58 22C78 22 92 34 100 50C108 34 122 22 142 22C166 22 186 38 186 66C186 100 160 134 100 178Z'
    return mass(d) + line('M40 62Q44 46 60 44', 9)
def espada():
    blade = 'M100 6L120 36L120 124L80 124L80 36Z'
    guard = 'M42 124C42 108 62 104 80 112L120 112C138 104 158 108 158 124C158 134 148 138 138 136L62 136C52 138 42 134 42 124Z'
    grip = 'M88 136L112 136L112 176L88 176Z'
    return (mass(blade) + mass(grip) + mass(guard) + line('M100 20L100 112', 7) + circ(100, 124, 9, K) + circ(100, 188, 12, R)
            + f'<circle cx="100" cy="188" r="12" fill="none" stroke="{K}" stroke-width="5"/>')
def bloque():
    q = 'M74 76C74 54 88 44 102 44C120 44 132 54 132 70C132 84 122 90 112 98C106 104 104 108 104 118'
    return (mass('M16 16L184 16L184 184L16 184Z').replace('stroke-width="16"', 'stroke-width="12"') + line(q, 18) + circ(104, 146, 11, K)
            + circ(34, 34, 6, K) + circ(166, 34, 6, K) + circ(34, 166, 6, K) + circ(166, 166, 6, K))
def estrella():
    pts = []
    for i in range(10):
        r = 90 if i % 2 == 0 else 40; a = -math.pi / 2 + i * math.pi / 5
        pts.append(f'{100 + r * math.cos(a):.1f} {108 + r * math.sin(a):.1f}')
    return mass('M' + 'L'.join(pts) + 'Z') + ell(84, 98, 8, 17) + ell(116, 98, 8, 17)
def tuberia():
    return (mass('M26 14L174 14L174 66L26 66Z') + mass('M40 66L160 66L160 186L40 186Z')
            + rect(48, 26, 12, 28, K) + rect(60, 80, 12, 92, K) + line('M26 40L174 40', 5) + circ(100, 128, 5, K))
def pacman():
    d = 'M100 100L176 58A88 88 0 1 0 176 142Z'
    return mass(d) + circ(104, 52, 11, K) + circ(186, 100, 8) + f'<circle cx="186" cy="100" r="8" fill="{R}"/>'
def fantasma():
    d = 'M20 186L20 90C20 46 56 16 100 16C144 16 180 46 180 90L180 186L152 160L126 186L100 160L74 186L48 160Z'
    return mass(d) + ell(72, 86, 20, 26) + ell(128, 86, 20, 26) + circ(78, 92, 10, R) + circ(134, 92, 10, R)
def invasor():
    rows = ['00100000100', '00010001000', '00111111100', '01101110110', '11111111111', '10111111101', '10100000101', '00011011000']
    s = 16; ox = (200 - 11 * s) // 2; oy = (200 - 8 * s) // 2
    cells = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == '1']
    out = ''.join(rect(ox + x * s - 3, oy + y * s - 3, s + 6, s + 6, K) for x, y in cells) + ''.join(rect(ox + x * s, oy + y * s, s, s, R) for x, y in cells)
    return out + rect(ox + 2 * s, oy + 3 * s, s, s, K) + rect(ox + 8 * s, oy + 3 * s, s, s, K)
def tetris():
    cells = [(0, 0), (1, 0), (2, 0), (1, 1), (3, 0), (3, 1), (3, 2), (2, 2)]; s = 44
    ox, oy = 100 - 88, 100 - 66
    out = ''.join(rect(ox + x * s - 5, oy + y * s - 5, s + 10, s + 10, K) for x, y in cells)
    for x, y in cells: out += rect(ox + x * s + 1, oy + y * s + 1, s - 2, s - 2, R) + rect(ox + x * s + 11, oy + y * s + 11, s - 22, s - 22, K)
    return out
def creeper():
    cells = {(1, 1), (2, 1), (5, 1), (6, 1), (1, 2), (2, 2), (5, 2), (6, 2), (3, 3), (4, 3), (2, 4), (3, 4), (4, 4), (5, 4), (2, 5), (3, 5), (4, 5), (5, 5), (2, 6), (5, 6)}
    s = 23; ox = oy = 8
    out = mass('M12 12L188 12L188 188L12 188Z').replace('stroke-width="16"', 'stroke-width="12"')
    return out + ''.join(rect(ox + x * s, oy + y * s, s, s, K) for x, y in cells)
def anillo():
    def ep(cx, cy, rx, ry, rot, fill, extra=''):
        return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" fill="{fill}" {extra}/>'
    out = ep(100, 104, 84, 72, -28, K, f'stroke="{K}" stroke-width="16"') + ep(100, 104, 84, 72, -28, R)
    out += ep(108, 98, 48, 36, -28, K)                       # agujero
    out += ep(100, 112, 70, 56, -28, 'none', f'stroke="{K}" stroke-width="6"')  # borde interior que da grosor
    out += line('M44 80A66 56 -28 0 1 82 46', 9) + line('M92 38L114 34', 7)  # brillo
    for (x, y, s) in [(176, 36, 18), (24, 168, 13)]:  # destellos de cuatro puntas
        out += f'<path d="M{x} {y-s}L{x+s*.28} {y-s*.28}L{x+s} {y}L{x+s*.28} {y+s*.28}L{x} {y+s}L{x-s*.28} {y+s*.28}L{x-s} {y}L{x-s*.28} {y-s*.28}Z" fill="{R}" stroke="{K}" stroke-width="5" stroke-linejoin="round"/>'
    return out

def kirby():
    return (mass('M10 150C10 128 34 120 48 134L48 168L10 168Z').replace('', '') if False else
            f'<ellipse cx="42" cy="176" rx="38" ry="18" fill="{K}" stroke="{K}" stroke-width="12"/><ellipse cx="158" cy="176" rx="38" ry="18" fill="{K}" stroke="{K}" stroke-width="12"/>'
            + ell(42, 176, 38, 18, R) + ell(158, 176, 38, 18, R)
            + mass('M100 18C146 18 182 52 182 98C182 144 146 176 100 176C54 176 18 144 18 98C18 52 54 18 100 18Z')
            + ell(76, 84, 10, 22) + ell(124, 84, 10, 22) + ell(76, 70, 10, 8, R) + ell(124, 70, 10, 8, R)
            + ell(52, 116, 14, 8) + ell(148, 116, 14, 8) + P('M90 126Q100 140 110 126Z', K))
def amongus():
    body = 'M54 28C54 14 70 8 100 8C132 8 148 22 148 46L148 150C148 166 140 176 128 176L116 176L116 150L84 150L84 176L72 176C60 176 54 166 54 150Z'
    pack = 'M54 70L30 70C20 70 16 78 16 86L16 126C16 134 20 142 30 142L54 142Z'
    return mass(pack) + mass(body) + f'<path d="M92 52L136 52C146 52 150 58 150 66C150 76 146 82 136 82L92 82C80 82 76 76 76 67C76 58 82 52 92 52Z" fill="{K}"/>' + line('M92 62L120 62', 7, R)
def rupia():
    d = 'M100 8L162 70L162 130L100 192L38 130L38 70Z'
    return mass(d) + line('M100 8L100 192M38 70L162 70M38 130L162 130', 6)
def ocarina():
    out = line('M70 104L30 50', 54, K) + line('M70 104L30 50', 36, R) + line('M30 50L24 42', 12, K)
    out += f'<ellipse cx="116" cy="124" rx="82" ry="58" transform="rotate(-8 116 124)" fill="{K}" stroke="{K}" stroke-width="16"/>' + f'<ellipse cx="116" cy="124" rx="82" ry="58" transform="rotate(-8 116 124)" fill="{R}"/>'
    out += line('M52 94L64 108', 6, R)
    for (x, y, r) in [(86, 104, 8), (112, 100, 8), (138, 102, 8), (162, 112, 8), (96, 128, 6), (146, 134, 6)]: out += circ(x, y, r, K)
    out += P('M118 134L108 152L128 152Z', K) + P('M108 152L98 170L118 170Z', K) + P('M128 152L118 170L138 170Z', K)
    return out

def tv_play():  # tecnología: pantalla con play
    return (mass('M14 30L186 30L186 150L14 150Z') + f'<path d="M26 42L174 42L174 138L26 138Z" fill="{K}"/>'
            + P('M82 64L82 118L128 91Z', R) + mass('M70 172L130 172L130 164L70 164Z').replace('stroke-width="16"', 'stroke-width="8"'))
def red_neuronal():
    nodes = [(24, 100), (24, 50), (24, 150), (100, 30), (100, 80), (100, 130), (100, 175), (176, 70), (176, 130)]
    L = [(0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (2, 5), (2, 6), (0, 5), (3, 7), (4, 7), (4, 8), (5, 7), (5, 8), (6, 8), (3, 8)]
    out = ''.join(line(f'M{nodes[a][0]} {nodes[a][1]}L{nodes[b][0]} {nodes[b][1]}', 15, K) for a, b in L)
    out += ''.join(line(f'M{nodes[a][0]} {nodes[a][1]}L{nodes[b][0]} {nodes[b][1]}', 6, R) for a, b in L)
    for x, y in nodes: out += circ(x, y, 17, K) + circ(x, y, 12, R)
    return out
def chip():
    out = ''
    for i in range(5):
        for (x1, y1, x2, y2) in [(34 + i * 33, 6, 34 + i * 33, 40), (34 + i * 33, 160, 34 + i * 33, 194), (6, 34 + i * 33, 40, 34 + i * 33), (160, 34 + i * 33, 194, 34 + i * 33)]:
            out += line(f'M{x1} {y1}L{x2} {y2}', 14, K) + line(f'M{x1} {y1}L{x2} {y2}', 6, R)
    return out + mass('M36 36L164 36L164 164L36 164Z') + f'<path d="M56 56L144 56L144 144L56 144Z" fill="{K}"/>' + P('M100 70C84 70 76 82 80 94C70 98 70 114 82 118C84 130 116 130 118 118C130 114 130 98 120 94C124 82 116 70 100 70Z', R)
def onda():
    return ''.join(line(f'M{10 + i * 20} {100 - h}L{10 + i * 20} {100 + h}', 11, K) for i, h in enumerate([20, 40, 66, 36, 84, 50, 28, 70, 40, 18])) + ''.join(line(f'M{10 + i * 20} {100 - h}L{10 + i * 20} {100 + h}', 5, R) for i, h in enumerate([20, 40, 66, 36, 84, 50, 28, 70, 40, 18]))

ICONOS = dict(triforce=triforce, hongo=seta, pokebola=pokebola, pikachu=pikachu, corazon=corazon, espada=espada, bloque=bloque, estrella=estrella,
              tuberia=tuberia, pacman=pacman, fantasma=fantasma, invasor=invasor, tetris=tetris, creeper=creeper, anillo=anillo, kirby=kirby,
              amongus=amongus, rupia=rupia, ocarina=ocarina, pantalla=tv_play, neuronal=red_neuronal, chip=chip, onda=onda)
def svg_icono(n): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -12 224 224">{ICONOS[n]()}</svg>'
def g(n, x, y, s, rot=0):  # grupo para componer escenas (centro del ícono en x,y; escala s sobre 200)
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s}) translate(-100 -100)">{ICONOS[n]()}</g>'
