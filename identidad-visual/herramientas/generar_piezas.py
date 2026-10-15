#!/usr/bin/env python3
"""Piezas rojas vectoriales (SVG) para ir ADELANTE del azul. Sin personajes. Uso: python3 generar_piezas.py ../assets/piezas"""
import sys, os
R, RD, RL, RK, CY, NV = '#ff3322', '#d11a10', '#ff8f7d', '#05071f', '#05071f', '#2a3cff'
SHADE = {
 'Mando': 'M52 128C52 70 96 46 146 52H254C304 46 348 70 348 128C348 198 336 262 306 262C280 262 270 226 246 202H154C130 226 120 262 94 262C64 262 52 198 52 128Z',
 'Consola portátil': 'M82 22H358V228H82Z M8 30H94V220H8Z M346 30H432V220H346Z',
 'Pantalla de streaming': 'M20 20H420V280H20Z',
 'Chip': 'M36 36H304V304H36Z',
 'Cartucho': 'M40 24H260V270L240 316H60L40 270Z',
 'Reproducir': 'M16 120a104 104 0 1 0 208 0a104 104 0 1 0 -208 0Z',
 'Audífonos': 'M22 170H108V320H22Z M252 170H338V320H252Z',
}
def svg(vb, body, name):
    x, y, w, h = [float(v) for v in vb.split()][0:4] if False else (0, 0, *[float(v) for v in vb.split()[2:]])
    defs = ('<defs><pattern id="ht" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="4.5" cy="4.5" r="2" fill="#05071f"/></pattern>'
            f'<linearGradient id="fd" x1="0" y1="0" x2="0" y2="1"><stop offset=".45" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>'
            f'<mask id="mk"><rect width="{w}" height="{h}" fill="url(#fd)"/></mask></defs>')
    over = f'<path d="{SHADE[name]}" fill="url(#ht)" mask="url(#mk)" opacity=".55"/>' if name in SHADE else ''
    body = body + over
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{name}"><title>{name}</title>{defs}{body}</svg>'
st = f'stroke="{RK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
P = {}
# mando genérico
P['mando'] = svg('0 0 400 290', f'''
<path d="M52 128C52 70 96 46 146 52H254C304 46 348 70 348 128C348 198 336 262 306 262C280 262 270 226 246 202H154C130 226 120 262 94 262C64 262 52 198 52 128Z" fill="{R}" {st}/>
<path d="M60 150C80 190 120 200 154 202C130 226 120 262 94 262C64 262 52 198 60 150Z M340 150C320 190 280 200 246 202C270 226 280 262 306 262C336 262 348 198 340 150Z" fill="{RD}" opacity=".55"/>
<path d="M92 66C120 52 170 62 200 62C230 62 280 52 308 66" fill="none" stroke="{RL}" stroke-width="7" stroke-linecap="round" opacity=".8"/>
<path d="M118 100h16v-14h16v14h16v16h-16v14h-16v-14h-16z" fill="{RK}"/>
<circle cx="290" cy="94" r="10" fill="{RK}"/><circle cx="318" cy="118" r="10" fill="{RK}"/><circle cx="262" cy="118" r="10" fill="{RK}"/><circle cx="290" cy="142" r="10" fill="{RK}"/>
<circle cx="158" cy="170" r="19" fill="{RD}" {st}/><circle cx="242" cy="170" r="19" fill="{RD}" {st}/>
<rect x="176" y="88" width="48" height="28" rx="8" fill="{RD}" {st}/>
<path d="M70 84C84 60 108 54 128 58" fill="none" stroke="{CY}" stroke-width="4" stroke-linecap="round" opacity=".9"/>''', 'Mando')
# portátil (tipo consola híbrida)
P['portatil'] = svg('0 0 440 250', f'''
<rect x="8" y="30" width="86" height="190" rx="34" fill="{RD}" {st}/>
<rect x="346" y="30" width="86" height="190" rx="34" fill="{RD}" {st}/>
<rect x="82" y="22" width="276" height="206" rx="16" fill="{R}" {st}/>
<rect x="104" y="42" width="232" height="166" rx="8" fill="{NV}" stroke="{RK}" stroke-width="5"/>
<path d="M104 70h232M104 98h232M104 126h232M104 154h232M104 182h232" stroke="{CY}" stroke-width="2" opacity=".28"/>
<path d="M190 84l62 36-62 36z" fill="{R}" stroke="{RL}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="50" cy="92" r="17" fill="{RL}" {st}/><circle cx="390" cy="152" r="17" fill="{RL}" {st}/>
<path d="M40 150h20M50 140v20" stroke="{RK}" stroke-width="6" stroke-linecap="round"/>
<circle cx="378" cy="82" r="7" fill="{RK}"/><circle cx="402" cy="82" r="7" fill="{RK}"/>
<path d="M92 36h256" stroke="{CY}" stroke-width="4" stroke-linecap="round" opacity=".85"/>''', 'Consola portátil')
# audífonos
P['audifonos'] = svg('0 0 360 340', f'''
<path d="M62 212C46 92 112 30 180 30S314 92 298 212" fill="none" stroke="{RK}" stroke-width="40" stroke-linecap="round"/>
<path d="M62 212C46 92 112 30 180 30S314 92 298 212" fill="none" stroke="{R}" stroke-width="28" stroke-linecap="round"/>
<path d="M78 120C100 62 140 48 180 48" fill="none" stroke="{RL}" stroke-width="7" stroke-linecap="round" opacity=".85"/>
<rect x="22" y="170" width="86" height="150" rx="32" fill="{RD}" {st}/><rect x="252" y="170" width="86" height="150" rx="32" fill="{RD}" {st}/>
<rect x="36" y="186" width="44" height="118" rx="20" fill="{R}"/><rect x="280" y="186" width="44" height="118" rx="20" fill="{R}"/>
<path d="M44 196v96" stroke="{CY}" stroke-width="5" stroke-linecap="round" opacity=".85"/>''', 'Audífonos')
# pantalla / tv
P['pantalla'] = svg('0 0 440 340', f'''
<rect x="20" y="20" width="400" height="260" rx="26" fill="{R}" {st}/>
<rect x="46" y="44" width="348" height="212" rx="14" fill="{NV}" stroke="{RK}" stroke-width="5"/>
<path d="M46 80h348M46 116h348M46 152h348M46 188h348M46 224h348" stroke="{CY}" stroke-width="2" opacity=".25"/>
<circle cx="220" cy="150" r="52" fill="{R}" stroke="{RL}" stroke-width="5"/>
<path d="M204 122l46 28-46 28z" fill="{RL}"/>
<path d="M150 296h140l16 28H134z" fill="{RD}" {st}/>
<path d="M36 34h150" stroke="{CY}" stroke-width="5" stroke-linecap="round" opacity=".9"/>''', 'Pantalla de streaming')
# chip
P['chip'] = svg('0 0 340 340', f'''
<g stroke="{RK}" stroke-width="5" stroke-linecap="round" fill="{RD}">
''' + ''.join(f'<rect x="{x}" y="6" width="16" height="48" rx="3"/><rect x="{x}" y="286" width="16" height="48" rx="3"/><rect x="6" y="{x}" width="48" height="16" rx="3"/><rect x="286" y="{x}" width="48" height="16" rx="3"/>' for x in (66, 106, 146, 186, 226, 258)) + f'''</g>
<rect x="36" y="36" width="268" height="268" rx="30" fill="{R}" {st}/>
<rect x="84" y="84" width="172" height="172" rx="16" fill="{NV}" stroke="{RK}" stroke-width="5"/>
<path d="M104 130h60v-30M236 130h-48M104 170h40v40h52M236 170v50M104 210h20" fill="none" stroke="{CY}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>
<circle cx="164" cy="100" r="7" fill="{R}"/><circle cx="236" cy="220" r="7" fill="{R}"/><circle cx="124" cy="210" r="7" fill="{R}"/>
<path d="M52 52h120" stroke="{CY}" stroke-width="5" stroke-linecap="round" opacity=".9"/>''', 'Chip')
# cartucho
P['cartucho'] = svg('0 0 300 340', f'''
<path d="M40 24H260V270L240 316H60L40 270Z" fill="{R}" {st}/>
<path d="M40 270L60 316H240L260 270Z" fill="{RD}" opacity=".6"/>
<rect x="70" y="50" width="160" height="124" rx="10" fill="{NV}" stroke="{RK}" stroke-width="5"/>
<path d="M70 82h160M70 114h160M70 146h160" stroke="{CY}" stroke-width="2" opacity=".3"/>
<path d="M120 122l30-40 30 40z" fill="{R}"/>
<rect x="70" y="196" width="160" height="22" rx="6" fill="{RD}" {st}/>
<path d="M92 290h116" stroke="{RK}" stroke-width="6" stroke-linecap="round"/>
<path d="M56 42h70" stroke="{CY}" stroke-width="5" stroke-linecap="round"/>''', 'Cartucho')
# play
P['play'] = svg('0 0 240 240', f'''
<circle cx="120" cy="120" r="104" fill="{R}" {st}/>
<path d="M30 140A92 92 0 0 0 210 140A100 100 0 0 1 30 140Z" fill="{RD}" opacity=".6"/>
<path d="M96 68l76 52-76 52z" fill="{RL}" stroke="{RK}" stroke-width="5" stroke-linejoin="round"/>
<path d="M36 90A90 90 0 0 1 100 30" fill="none" stroke="{CY}" stroke-width="6" stroke-linecap="round"/>''', 'Reproducir')
# destello
P['destello'] = svg('0 0 120 120', f'<path d="M60 4C64 40 80 56 116 60C80 64 64 80 60 116C56 80 40 64 4 60C40 56 56 40 60 4Z" fill="{CY}"/>', 'Destello')
# anillo
P['anillo'] = svg('0 0 300 300', f'<circle cx="150" cy="150" r="128" fill="none" stroke="{R}" stroke-width="26"/><circle cx="150" cy="150" r="128" fill="none" stroke="{RK}" stroke-width="5" opacity=".6"/><path d="M60 80A120 120 0 0 1 140 28" fill="none" stroke="{RL}" stroke-width="8" stroke-linecap="round"/>', 'Anillo')
if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for k, v in P.items(): open(os.path.join(out, f'pieza-{k}.svg'), 'w').write(v)
    print(len(P), 'piezas')
