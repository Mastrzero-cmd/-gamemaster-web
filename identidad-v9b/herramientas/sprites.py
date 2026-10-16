"""Sprites de píxel (rojo #FF1A1A, hielo #F4F4EF, negro #050505) para v9b «Arcade-técnico».
Cada sprite: matriz de caracteres  # = rojo · w = hielo · k = negro · . = vacío.  Contorno negro automático de 1 celda."""
import math
RED, ICE, BLK = '#FF1A1A', '#F4F4EF', '#050505'

def mir(rows, odd=False):
    out = []
    for r in rows:
        right = r[::-1][1:] if odd else r[::-1]
        out.append(r + right)
    return out

def grid(w, h): return [['.'] * w for _ in range(h)]
def tog(g): return [''.join(r) for r in g]

S = {}
S['hongo'] = mir(['.....###', '...#####', '..###www', '.####www', '.#ww####', '##www###', '##www###', '.#ww####', '########', '########',
                  '...wwwww', '...wkwww', '...wkwww', '...wwwww', '....wwww'])
S['fantasma'] = mir(['....####', '..######', '.#######', '.##ww###', '.#wwww##', '.#wwkk##', '.#wwkk##', '.##ww###', '########', '########', '########', '########', '###..###', '##....##'])
S['invader'] = mir(['..#.....#..'[:6], '...#...#...'[:6], '..#######..'[:6], '.##.###.##.'[:6], '###########'[:6], '#.#######.#'[:6], '#.#.....#.#'[:6], '...##.##...'[:6]], odd=True)
S['corazon'] = mir(['..###.', '.#####', '######', '######', '######', '.#####', '..####', '...###', '....##', '.....#'])
for i, r in enumerate(S['corazon']): pass
# brillo del corazón
c = [list(r) for r in S['corazon']]; c[1][2] = 'w'; c[2][1] = 'w'; S['corazon'] = tog(c)
S['pacman'] = ['....######....', '..##########..', '.#####k######.', '.############.', '.###########..', '.#########....', '.######.......', '.#########....', '.###########..', '.############.', '.############.', '..##########..', '....######....']
S['pellet'] = ['##', '##']
S['creeper'] = None
g = grid(16, 16)
for y in range(16):
    for x in range(16): g[y][x] = '#'
for y in range(4, 7):
    for x in list(range(3, 6)) + list(range(10, 13)): g[y][x] = 'k'
for x in range(6, 10): g[7][x] = 'k'
for y in (8, 9):
    for x in range(5, 11): g[y][x] = 'k'
for y in (10, 11):
    for x in (5, 6, 9, 10): g[y][x] = 'k'
S['creeper'] = tog(g)
S['amongus'] = ['.....######...', '....########..', '...##########.', '...###wwwwww#.', '##.###wwwwww#.', '##.###wwwwww#.', '##.##########.', '##.##########.', '##.##########.', '...####..####.', '...####..####.']
# estrella
S['estrella'] = mir(['.......#', '.......#', '......##', '......##', '########', '.#######', '..####k#', '...###k#', '...#####', '..######', '..####..', '..###...', '..##....'])
# bloque ?
g = grid(15, 15)
for y in range(15):
    for x in range(15): g[y][x] = '#'
for (y, x) in [(1, 1), (1, 13), (13, 1), (13, 13)]: g[y][x] = 'k'
Q = ['.www.', 'w...w', '....w', '...w.', '..w..', '.....', '..w..']
for j, r in enumerate(Q):
    for i, ch in enumerate(r):
        if ch == 'w': g[4 + j][5 + i] = 'w'
S['bloque'] = tog(g)
# pokébola
n = 17; g = grid(n, n); cx = cy = 8
for y in range(n):
    for x in range(n):
        d = math.hypot(x - cx, y - cy)
        if d <= 8.4:
            g[y][x] = '#' if y < cy else 'w'
            if abs(y - cy) <= 1: g[y][x] = 'k'
        if d <= 3.2: g[y][x] = 'k'
        if d <= 1.9: g[y][x] = 'w'
S['pokebola'] = tog(g)
# anillo (Sonic)
n = 15; g = grid(n, n)
for y in range(n):
    for x in range(n):
        d = math.hypot(x - 7, y - 7)
        if 4.6 <= d <= 7.5: g[y][x] = '#'
g[2][4] = g[3][3] = 'w'
S['anillo'] = tog(g)
# espada
n = 17; g = grid(n, n)
for i in range(4, 16):
    g[16 - i][i] = 'w'; g[16 - i][i - 1] = 'w'
g[0][16] = 'w'; g[1][16] = 'w'
for t_ in range(-3, 4):  # guarda, perpendicular a la hoja
    yy, xx = 11 + t_, 5 + t_ * -1 - 0
    yy, xx = 12 - t_, 4 + t_
    if 0 <= xx < n and 0 <= yy < n: g[yy][xx] = '#'; g[yy][min(xx + 1, n - 1)] = '#'
for i in range(0, 4):  # empuñadura
    g[16 - i][i] = '#'; g[15 - i][i] = '#' if i else '#'
S['espada'] = tog(g)
# triforce
rows = 13; W = 28; g = grid(W, rows)
def tri(cx, r0, h):
    for r in range(h):
        w = 2 * (r + 1)
        for x in range(cx - w // 2, cx + w // 2): g[r0 + r][x] = '#'
tri(14, 0, 6); tri(7, 7, 6); tri(21, 7, 6)
S['trifuerza'] = tog(g)
# Pikachu
S['pikachu'] = mir(['.kk.....', '.kk.....', '.##.....', '.##.....', '..##....', '..###...', '..######', '.#######', '.#######', '##kk####', '##kw####', '########', '#ww#####', '#ww####k', '.#######', '..######', '...#####'])
# Kirby
n = 17; g = grid(n, 14)
for y in range(14):
    for x in range(n):
        if ((x - 8) / 7.6) ** 2 + ((y - 6) / 6.2) ** 2 <= 1: g[y][x] = '#'
for y in (4, 5, 6, 7):
    g[y][6] = 'k'; g[y][10] = 'k'
g[4][6] = g[4][10] = 'w'
for y in range(9, 12):  # brazos
    pass
g[8][1] = g[8][15] = '#'; g[9][0] = g[9][16] = '#'
for y in (11, 12, 13):
    for x in list(range(2, 7)) + list(range(10, 15)):
        if (y == 13 and x in (2, 6, 10, 14)) : continue
        g[y][x] = '#'
for x in (8,): g[9][x] = 'k'
S['kirby'] = tog(g)
# mando retro
S['mando'] = mir(['########', '########', '###kk###'.replace('kk', 'k#'), '##kkkk##', '###kk###', '########', '########'][:0] or ['.#######', '########', '########', '###k####', '##kkk###', '###k####', '########', '########', '.#######'], odd=False)
m = [list(r) for r in S['mando']]
for y in range(9):
    pass
# botones a la derecha
for (y, x) in [(3, 12), (4, 13), (5, 12), (4, 11)]: m[y][x] = 'k'
S['mando'] = tog(m)
# TV con play
g = grid(16, 16)
for y in range(3, 16):
    for x in range(16): g[y][x] = '#'
for y in range(5, 14):
    for x in range(2, 12): g[y][x] = 'k'
for i, wd in enumerate([1, 3, 5, 7, 5, 3, 1]):
    for x in range(4, 4 + wd): g[6 + i][x] = '#'
for y in (6, 9, 12): g[y][13] = 'k'; g[y][14] = 'k'
for (y, x) in [(0, 3), (1, 4), (2, 5), (0, 12), (1, 11), (2, 10)]: g[y][x] = '#'
S['tv'] = tog(g)
# robot IA
S['robot'] = mir(['...##...'[:8], '...##...', '...##...', '########', '########', '##ww#www'.replace('#www', 'wwww'), '##wwkwww'.replace('kwww', 'kwww'), '########', '########', '###kkkkk', '###k#k#k', '########', '.#######', '.#######'])
r = [list(x) for x in S['robot']]
for y in (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13): pass
S['robot'] = tog(r)
n = 15; g = grid(n, n)
for y in range(n):
    for x in range(n):
        d = math.hypot(x - 7, y - 7)
        if d <= 7.4: g[y][x] = '#'
        if 4.4 <= d <= 5.4: g[y][x] = 'k'
for y in range(4, 11):
    for x in (6, 7, 8): g[y][x] = 'w'
S['moneda'] = tog(g)

def tetro(kind, sub=5):
    sh = {'T': [(0, 0), (1, 0), (2, 0), (1, 1)], 'L': [(0, 0), (0, 1), (0, 2), (1, 2)], 'S': [(1, 0), (2, 0), (0, 1), (1, 1)], 'I': [(0, 0), (1, 0), (2, 0), (3, 0)], 'O': [(0, 0), (1, 0), (0, 1), (1, 1)], 'J': [(1, 0), (1, 1), (1, 2), (0, 2)], 'Z': [(0, 0), (1, 0), (1, 1), (2, 1)]}[kind]
    W = max(x for x, y in sh) + 1; H = max(y for x, y in sh) + 1
    g = grid(W * sub, H * sub)
    for (x, y) in sh:
        for j in range(sub):
            for i in range(sub):
                ch = '#'
                if i == sub - 1 or j == sub - 1: ch = 'k'
                if (i, j) in ((1, 1), (2, 1), (1, 2)): ch = 'w'
                g[y * sub + j][x * sub + i] = ch
    return tog(g)
for k in 'TLSIOJZ': S['tetris_' + k] = tetro(k)

def render(name, cell=1, outline=True, extra=0):
    rows = S[name]; h = len(rows); w = max(len(r) for r in rows); rows = [r.ljust(w, '.') for r in rows]
    solid = [[rows[y][x] != '.' for x in range(w)] for y in range(h)]
    ox = oy = 1 if outline else 0
    W, H = w + 2 * ox, h + 2 * oy
    rects = {'k': [], 'k2': [], '#': [], 'w': []}
    def runs(mask, y, key):
        x = 0
        while x < len(mask[y]):
            if mask[y][x]:
                x0 = x
                while x < len(mask[y]) and mask[y][x]: x += 1
                rects[key].append((x0, y, x - x0))
            else: x += 1
    if outline:
        dil = [[False] * W for _ in range(H)]
        for y in range(h):
            for x in range(w):
                if solid[y][x]:
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1): dil[y + oy + dy][x + ox + dx] = True
        for y in range(H): runs(dil, y, 'k')
    for key in ('k', 'w', '#'):
        mask = [[False] * W for _ in range(H)]
        for y in range(h):
            for x in range(w):
                ch = rows[y][x]
                if ch == key and key != 'k': mask[y + oy][x + ox] = True
                if ch == 'k' and key == 'k': mask[y + oy][x + ox] = True
        for y in range(H): runs(mask, y, key if key != 'k' else 'k2')
    def path(rs): return ''.join(f'M{x} {y}h{n}v1h-{n}z' for x, y, n in rs)
    k2 = rects['k2']
    return W, H, [(BLK, path(rects['k'] + k2)), (ICE, path(rects['w'])), (RED, path(rects['#']))]

def sprite_svg(name, cell=8, outline=True):
    W, H, layers = render(name, outline=outline)
    body = ''.join(f'<path fill="{c}" d="{d}"/>' for c, d in layers if d)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*cell}" height="{H*cell}" shape-rendering="crispEdges">{body}</svg>', W, H

def group(name, x, y, cell, outline=True, rot=0):
    """Grupo <g> para componer escenas; (x,y) esquina superior izquierda en px."""
    W, H, layers = render(name, outline=outline)
    body = ''.join(f'<path fill="{c}" d="{d}"/>' for c, d in layers if d)
    return f'<g transform="translate({x} {y}) scale({cell})">{body}</g>', W * cell, H * cell
