"""Arte vectorial local de Órbita. Sin dependencias ni recursos remotos."""
from pathlib import Path
from math import sin, cos, pi

ROOT = Path(__file__).resolve().parents[1] / 'assets'
BLUE = '#1919E8'
BLACK = '#080808'
RED = '#FF3028'


def svg(name, width, height, content, folder='arte'):
    (ROOT / folder / f'{name}.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
        f'{content}</svg>\n', encoding='utf-8')


def smooth(points, close=True):
    """Spline cúbica: curvas continuas, sin segmentos en ángulo."""
    n = len(points)
    d = f'M{points[0][0]:.2f},{points[0][1]:.2f}'
    for i in range(n if close else n - 1):
        a = points[(i - 1) % n] if close or i else points[0]
        b = points[i]
        c = points[(i + 1) % n]
        e = points[(i + 2) % n] if close or i + 2 < n else c
        d += (f'C{b[0]+(c[0]-a[0])/6:.2f},{b[1]+(c[1]-a[1])/6:.2f} '
              f'{c[0]-(e[0]-b[0])/6:.2f},{c[1]-(e[1]-b[1])/6:.2f} '
              f'{c[0]:.2f},{c[1]:.2f}')
    return d + ('Z' if close else '')


def contours(cx, cy, rx, ry, count, color, phase=0):
    paths = []
    for j in range(count):
        scale = 0.17 + j * 0.036
        pts = []
        for k in range(96):
            a = k * 2 * pi / 96
            r = 1 + .16*sin(3*a+phase) + .065*cos(5*a-phase) + .06*sin(a*2+j*.028)
            pts.append((cx + cos(a)*rx*scale*r + 20*sin(j*.1),
                        cy + sin(a)*ry*scale*r))
        paths.append(f'<path d="{smooth(pts)}"/>')
    return f'<g fill="none" stroke="{color}" stroke-width="1.15">' + ''.join(paths) + '</g>'


# Isla negra, curvas azules independientes y trayectorias libres.
hero = f'<path fill="{BLACK}" d="M1075 65C1290 21 1486 220 1458 416C1436 597 1324 710 1127 709C926 708 829 584 848 427C867 277 877 105 1075 65Z"/>'
hero += contours(1110, 382, 422, 305, 35, BLUE, .4)
hero += contours(144, 828, 344, 230, 24, BLACK, 1.9)
hero += f'<g fill="none" stroke="{BLACK}" stroke-width="1.1">'
for i in range(14):
    y = 42 + i*9
    hero += f'<path d="M685 {y}C780 {y+140} 750 {y+350} 876 {y+455}S1200 {y+485} 1470 {y+340}"/>'
hero += '</g>'
svg('atlas-hero', 1440, 860, hero)

# Móvil: composición abierta para una escena vertical.
mobile = f'<path fill="{BLACK}" d="M276 45C388 13 467 102 435 236C405 365 288 403 190 349C114 308 93 215 137 135C170 75 204 64 276 45Z"/>'
mobile += contours(279, 211, 194, 157, 27, BLUE, .5)
mobile += f'<g stroke="{BLACK}" stroke-width="1" fill="none">'
for i in range(11):
    mobile += f'<path d="M{-80+i*7} 82C{50+i*7} 130 {-50+i*10} 284 {65+i*12} 378S{340+i*8} 386 470 338"/>'
mobile += '</g>'
svg('atlas-mobile', 430, 440, mobile)

# Tres fronteras orgánicas diferentes, con superficies negras opacas.
svg('rive-jeux', 1440, 180,
    f'<path fill="{BLACK}" d="M0 74C230 205 414 133 642 68S1120 16 1440 88V180H0Z"/>' +
    ''.join(f'<path fill="none" stroke="{BLUE}" stroke-width="1" d="M-50 {100+i*6}C230 {230+i*5} 414 {157+i*5} 642 {91+i*5}S1120 {39+i*5} 1490 {111+i*5}"/>' for i in range(9)))
svg('rive-signal', 1440, 240,
    f'<path fill="{BLACK}" d="M0 0H1440V44C1130 245 892 52 620 106S211 283 0 120Z"/>' +
    ''.join(f'<path fill="none" stroke="{BLACK}" stroke-width="1.2" d="M-40 {150+i*6}C211 {313+i*6} 348 {194+i*5} 620 {135+i*5}S1130 {274+i*5} 1480 {67+i*7}"/>' for i in range(13)))
svg('rive-ia', 1440, 180,
    f'<path fill="{BLACK}" d="M0 146C280 34 359 126 613 120S1163 -60 1440 72V180H0Z"/>' +
    ''.join(f'<path fill="none" stroke="{BLUE}" stroke-width="1" d="M-30 {167+i*5}C280 {55+i*5} 359 {147+i*5} 613 {141+i*5}S1163 {-39+i*5} 1470 {93+i*5}"/>' for i in range(8)))

# Ondas largas: paisaje de señal, sin rejilla ni marco.
signal = ''
for i in range(34):
    pts = []
    for k in range(66):
        x = -60 + k*25
        y = 280 + 105*sin(x/205+i*.018) + i*5.7 + 27*sin(x/94+i*.09)
        pts.append((x, y))
    signal += f'<path d="{smooth(pts, False)}"/>'
svg('paysage-signal', 1500, 680,
    f'<g fill="none" stroke="{BLACK}" stroke-width="1">{signal}</g>')

# Red de ramas curvas, sin cuadrículas ni mosaicos.
neural = f'<g fill="none" stroke="{BLUE}" stroke-width="1.15">'
for i in range(23):
    y = 30+i*23
    neural += f'<path d="M-100 {y}C90 {y-80} 130 {500-y*.35} 340 {270+i*4}S680 {y-160} 920 {y+50}"/>'
neural += '</g>'
neural += contours(680, 240, 160, 190, 13, BLUE, 1.2)
for x, y, r in [(244,231,5),(457,317,8),(620,186,4),(738,364,7),(114,129,5),(530,421,4)]:
    neural += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BLUE}"/>'
svg('jardin-neural', 900, 650, neural)
svg('courant-final', 1440, 440, contours(1194, 266, 510, 290, 28, BLACK, 1.3))

# Siluetas originales: un solo color pleno y huecos transparentes.
icons = {
    'hongo': ('0 0 200 200', 'M100 14C49 14 8 53 8 100C8 118 24 126 59 127L54 160C51 180 67 188 100 188C133 188 149 180 146 160L141 127C176 126 192 118 192 100C192 53 151 14 100 14ZM84 42C84 28 116 28 116 42V70C116 87 84 87 84 70ZM33 78C40 67 54 70 56 83C59 98 44 108 34 99C29 93 29 85 33 78ZM144 83C146 70 160 67 167 78C171 85 171 93 166 99C156 108 141 98 144 83Z'),
    'estrella': ('0 0 200 200', 'M100 8L125 66L190 73L141 116L155 180L100 146L45 180L59 116L10 73L75 66Z'),
    'triforce': ('0 0 200 180', 'M100 8L145 86H55ZM51 93L96 171H6ZM149 93L194 171H104Z'),
    'espada': ('0 0 120 240', 'M60 4L81 37L74 145L110 133L116 149L73 166L69 202L79 217L60 234L41 217L51 202L47 166L4 149L10 133L46 145L39 37Z'),
    'moneda': ('0 0 160 200', 'M80 7C31 7 11 46 11 100S31 193 80 193S149 154 149 100S129 7 80 7ZM80 28C112 28 128 58 128 100S112 172 80 172S32 142 32 100S48 28 80 28ZM70 54H90V145H70Z'),
    'pokeball': ('0 0 200 200', 'M100 8C52 8 14 43 9 89H61C66 72 80 61 100 61S134 72 139 89H191C186 43 148 8 100 8ZM9 111C14 157 52 192 100 192S186 157 191 111H139C134 128 120 139 100 139S66 128 61 111ZM100 77A23 23 0 1 0 100 123A23 23 0 1 0 100 77Z'),
    'rayo': ('0 0 160 220', 'M86 5L12 127H65L45 215L149 83H96L117 5Z'),
    'mando': ('0 0 280 180', 'M68 28C41 28 30 47 21 75L7 122C-2 155 19 173 41 161L83 134H197L239 161C261 173 282 155 273 122L259 75C250 47 239 28 212 28H68ZM65 63H81V82H100V98H81V117H65V98H46V82H65ZM211 61A12 12 0 1 0 211 85A12 12 0 1 0 211 61ZM238 91A12 12 0 1 0 238 115A12 12 0 1 0 238 91ZM124 89H156V100H124Z'),
    'play': ('0 0 200 200', 'M48 17C41 12 32 18 32 26V174C32 182 41 188 48 183L175 109C182 105 182 95 175 91Z'),
    'audio': ('0 0 200 220', 'M100 10C49 10 17 47 17 101V167C17 189 31 201 55 201H72V113H42V101C42 61 65 35 100 35S158 61 158 101V113H128V201H145C169 201 183 189 183 167V101C183 47 151 10 100 10Z'),
    'antena': ('0 0 200 200', 'M100 18C54 18 18 54 18 100H33C33 63 63 33 100 33S167 63 167 100H182C182 54 146 18 100 18ZM100 53C74 53 53 74 53 100H68C68 82 82 68 100 68S132 82 132 100H147C147 74 126 53 100 53ZM100 85A18 18 0 1 0 100 121A18 18 0 1 0 100 85ZM94 129L67 186H133L106 129Z'),
    'destello': ('0 0 200 200', 'M100 0C108 65 135 92 200 100C135 108 108 135 100 200C92 135 65 108 0 100C65 92 92 65 100 0Z'),
    'disco': ('0 0 200 200', 'M100 8A92 92 0 1 0 100 192A92 92 0 1 0 100 8ZM100 76A24 24 0 1 1 100 124A24 24 0 1 1 100 76Z'),
    'botones': ('0 0 240 100', 'M24 16A24 24 0 1 0 24 64A24 24 0 1 0 24 16ZM24 24A16 16 0 1 1 24 56A16 16 0 1 1 24 24ZM66 18L80 32L94 18L101 25L87 39L101 53L94 60L80 46L66 60L59 53L73 39L59 25ZM138 13L166 65H110ZM138 31L123 57H153ZM182 16H230V64H182ZM190 24V56H222V24Z'),
}
for name, (viewbox, d) in icons.items():
    (ROOT / 'iconos' / f'{name}.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">'
        f'<path fill="{RED}" fill-rule="evenodd" d="{d}"/></svg>\n', encoding='utf-8')
print(f'Arte listo: 9 paisajes y {len(icons)} símbolos originales.')
