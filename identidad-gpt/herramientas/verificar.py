#!/usr/bin/env python3
"""Pruebas DOM en Chrome local mediante CDP; nunca toma capturas.

Usa websockets ya disponible en el entorno; no descarga ni instala nada.
Servidor, perfil temporal e informe están aislados en identidad-gpt.
"""
import asyncio
import argparse
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from threading import Thread
import time
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


class CDP:
    def __init__(self, socket):
        self.socket = socket
        self.sequence = 0

    async def call(self, method, params=None):
        self.sequence += 1
        number = self.sequence
        await self.socket.send(json.dumps({'id': number, 'method': method, 'params': params or {}}))
        while True:
            message = json.loads(await self.socket.recv())
            if message.get('method') == 'Runtime.exceptionThrown':
                ERRORS.append(message['params']['exceptionDetails'])
            if message.get('id') == number:
                if 'error' in message:
                    raise RuntimeError(message['error'])
                return message.get('result', {})

    async def evaluate(self, expression):
        result = await self.call('Runtime.evaluate', {'expression': expression, 'returnByValue': True, 'awaitPromise': True})
        if 'exceptionDetails' in result:
            raise RuntimeError(result['exceptionDetails'])
        return result.get('result', {}).get('value')


INSPECT = r'''(() => {
 const colors = s => (s.match(/[\d.]+/g) || []).map(Number).slice(0, 3);
 const bg = element => {
   let current = element;
   while (current) {
     const color = getComputedStyle(current).backgroundColor;
     const components = color.match(/[\d.]+/g)?.map(Number) || [];
     if (components.length === 3 || components[3] === 1) return colors(color);
     current = current.parentElement;
   }
   return [8, 8, 8];
 };
 const pairs = new Map();
 for (const element of document.querySelectorAll('body *')) {
   if (!element.checkVisibility() || !element.getBoundingClientRect().width) continue;
   const text = [...element.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
   if (!text && !element.matches('input')) continue;
   const style = getComputedStyle(element);
   const large = parseFloat(style.fontSize) >= 24 || (parseFloat(style.fontSize) >= 18.66 && +style.fontWeight >= 700);
   const pair = {frente: colors(style.color), fondo: bg(element), minimo: large ? 3 : 4.5, ejemplo: element.textContent.trim().slice(0, 36)};
   pairs.set(JSON.stringify([pair.frente,pair.fondo,pair.minimo]),pair);
 }
 const outside = [...document.querySelectorAll('main h1, main h2, main p, .section-heading, header, footer')].filter(e=>{
   const r = e.getBoundingClientRect(); return r.width && (r.right > innerWidth + 1 || r.left < -1);
 }).map(e => e.tagName + ':' + e.textContent.trim().slice(0, 35));
 const missing = [...document.images].filter(image => !image.complete || !image.naturalWidth).map(i=>i.getAttribute('src'));
 const external = [...document.querySelectorAll('[src],link[href]')].map(e=>e.getAttribute('src')||e.getAttribute('href')).filter(v=>/^https?:/.test(v));
 return {ancho:innerWidth, anchoPagina:document.documentElement.scrollWidth, desbordes:outside, imagenesRotas:missing, recursosExternos:external, contrastes:[...pairs.values()], filas:document.querySelectorAll('.rail').length, cortes:new Set([...document.querySelectorAll('.section-cut')].map(i=>i.src)).size};
})()'''


async def run(url, socket_url):
    import websockets
    report = {'vistas': [], 'pruebas': {}, 'erroresJS': ERRORS}
    async with websockets.connect(socket_url, max_size=8 * 1024 * 1024) as socket:
        cdp = CDP(socket)
        await cdp.call('Page.enable')
        await cdp.call('Runtime.enable')
        for width in (1440, 390, 430):
            await cdp.call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 950, 'deviceScaleFactor': 1, 'mobile': width < 621})
            await cdp.call('Page.navigate', {'url': url})
            await asyncio.sleep(.5)
            await cdp.evaluate("Promise.all([...document.images].map(i => { i.loading='eager'; return i.decode().catch(()=>{}); }))")
            await asyncio.sleep(.1)
            view = await cdp.evaluate(INSPECT)
            report['vistas'].append(view)
            assert view['anchoPagina'] == width, view
            assert not view['desbordes'], view['desbordes']
            assert not view['imagenesRotas'], view['imagenesRotas']
            assert not view['recursosExternos'], view['recursosExternos']
            assert view['filas'] == 4 and view['cortes'] == 5

        # Búsqueda sin resultados y restauración.
        result = await cdp.evaluate('''(() => {
          const input=document.querySelector('#game-search'); input.value='zzzzzzzz'; input.dispatchEvent(new Event('input'));
          const empty=!document.querySelector('#empty-state').hidden && document.querySelector('#rail-juegos').hidden;
          document.querySelector('#reset-search').click();
          const all=[...document.querySelectorAll('.game-card')].filter(e=>!e.hidden).length===14;
          document.querySelector('[data-collection="switch2"]').click();
          const filtered=[...document.querySelectorAll('.game-card')].filter(e=>!e.hidden).length===2;
          document.querySelector('[data-collection="todo"]').click();
          input.value='pokemon'; input.dispatchEvent(new Event('input'));
          const accents=[...document.querySelectorAll('.game-card')].filter(e=>!e.hidden).length===1;
          document.querySelector('#reset-search').click();
          return {empty,all,filtered,accents};
        })()''')
        assert all(result.values()), result
        report['pruebas']['busqueda'] = result

        # Cada fila: flechas y teclado reales, con desplazamiento visible.
        await cdp.call('Page.navigate', {'url': url + '?reduce'})
        await asyncio.sleep(.3)
        navigation = {}
        for name in ('juegos', 'streaming', 'ia', 'plataformas'):
            await cdp.evaluate(f"document.querySelector('#rail-{name}').scrollIntoView({{block:'center'}})")
            before = await cdp.evaluate(f"document.querySelector('#rail-{name}').scrollLeft")
            await cdp.evaluate(f"document.querySelector('[data-controls=\"rail-{name}\"] [data-direction=\"1\"]').click()")
            after = await cdp.evaluate(f"document.querySelector('#rail-{name}').scrollLeft")
            assert after > before, (name, before, after)
            await cdp.evaluate(f"document.querySelector('#rail-{name}').focus()")
            await cdp.call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'ArrowLeft', 'code': 'ArrowLeft', 'windowsVirtualKeyCode': 37})
            await cdp.call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'ArrowLeft', 'code': 'ArrowLeft', 'windowsVirtualKeyCode': 37})
            end = await cdp.evaluate(f"document.querySelector('#rail-{name}').scrollLeft")
            assert end < after, (name, after, end)
            navigation[name] = {'flecha': after > before, 'teclado': end < after}
        report['pruebas']['filas'] = navigation

        # Arrastre de ratón real en Chrome, sin abrir enlaces.
        await cdp.evaluate("document.querySelector('#rail-juegos').scrollIntoView({block:'center'})")
        rect = await cdp.evaluate("(()=>{const r=document.querySelector('#rail-juegos').getBoundingClientRect();return {x:r.x+250,y:r.y+100}})()")
        await cdp.call('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': rect['x'], 'y': rect['y'], 'button': 'left', 'clickCount': 1})
        for delta in (20, 60, 100, 150):
            await cdp.call('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': rect['x'] - delta, 'y': rect['y'], 'button': 'left', 'buttons': 1})
        await cdp.call('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': rect['x'] - 150, 'y': rect['y'], 'button': 'left', 'clickCount': 1})
        await asyncio.sleep(.2)
        drag = await cdp.evaluate("document.querySelector('#rail-juegos').scrollLeft > 10")
        assert drag
        report['pruebas']['arrastreMouse'] = drag

        # Un gesto táctil nativo no queda capturado por el código de arrastre.
        await cdp.call('Emulation.setTouchEmulationEnabled', {'enabled': True, 'maxTouchPoints': 1})
        await cdp.evaluate("document.querySelector('#rail-juegos').scrollLeft=0")
        for event, delta in [('touchStart', 0), ('touchMove', 40), ('touchMove', 90), ('touchMove', 160), ('touchEnd', 160)]:
            points = [] if event == 'touchEnd' else [{'x': rect['x'] - delta, 'y': rect['y']}]
            await cdp.call('Input.dispatchTouchEvent', {'type': event, 'touchPoints': points})
            await asyncio.sleep(.04)
        await asyncio.sleep(.3)
        touch = await cdp.evaluate("document.querySelector('#rail-juegos').scrollLeft > 10")
        assert touch
        report['pruebas']['tactil'] = touch

        # Parallax: la misma distancia produce la mitad en teléfono.
        motion = {}
        for width in (1440, 390):
            await cdp.call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 950, 'deviceScaleFactor': 1, 'mobile': width < 621})
            await cdp.call('Page.navigate', {'url': url})
            await asyncio.sleep(.2)
            await cdp.evaluate("(()=>{const e=document.querySelector('.hero-stage');window.scrollTo(0,e.getBoundingClientRect().top+scrollY+e.offsetHeight/2-innerHeight/2+200)})()")
            await asyncio.sleep(.1)
            values = await cdp.evaluate("[...document.querySelectorAll('.hero-stage [data-plane]')].map(e=>parseFloat(e.style.getPropertyValue('--shift')))")
            assert 0 < abs(values[0]) < abs(values[1])
            assert abs(values[0]) <= (6 if width == 390 else 12)
            assert abs(values[1]) <= (21 if width == 390 else 42)
            motion[str(width)] = values
        assert all(abs(motion['390'][n] * 2 - motion['1440'][n]) < .2 for n in (0, 1)), motion
        report['pruebas']['parallax'] = motion

        for mode in ('query', 'sistema'):
            await cdp.call('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'reduce' if mode == 'sistema' else 'no-preference'}]})
            await cdp.call('Page.navigate', {'url': url + ('?reduce' if mode == 'query' else '')})
            await asyncio.sleep(.2)
            await cdp.evaluate('window.scrollTo(0,400)')
            await asyncio.sleep(.1)
            disabled = await cdp.evaluate("[...document.querySelectorAll('[data-plane]')].every(e=>getComputedStyle(e).transform==='none')")
            assert disabled
            report['pruebas']['movimientoReducido-' + mode] = disabled

        # Foco visible y enlaces de consulta exactos.
        await cdp.evaluate("document.querySelector('#game-search').focus()")
        focus = await cdp.evaluate("getComputedStyle(document.activeElement).outlineStyle !== 'none'")
        links = await cdp.evaluate("[...document.querySelectorAll('[data-quote]')].every(e=>e.getAttribute('href')==='https://wa.me/525527699426')")
        assert focus and links
        report['pruebas']['focoVisible'] = focus
        report['pruebas']['whatsappExacto'] = links
        assert not ERRORS, ERRORS
    output = ROOT / 'herramientas' / 'informe-navegador.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Chrome: 1440 / 390 / 430 px; cuatro filas, cinco cortes, búsqueda, teclado, mouse, táctil, parallax y movimiento reducido: OK. Sin capturas.')


def validate_local():
    from xml.etree import ElementTree as ET
    import ast
    import re

    class Page(HTMLParser):
        def __init__(self):
            super().__init__()
            self.nodes = []

        def handle_starttag(self, tag, attrs):
            self.nodes.append((tag, dict(attrs)))

    document = Page()
    document.feed((ROOT / 'index.html').read_text())
    ids = [attrs['id'] for _, attrs in document.nodes if 'id' in attrs]
    assert len(set(ids)) == len(ids), 'IDs duplicados'
    refs, images, quotes = [], 0, 0
    for tag, attrs in document.nodes:
        for name in ('src', 'href'):
            value = attrs.get(name, '')
            if value.startswith('#'):
                assert value[1:] in ids, value
            elif value and not re.match(r'https?://', value):
                assert (ROOT / value).is_file(), value
                refs.append(value)
            elif value:
                assert value == 'https://wa.me/525527699426', value
        if tag == 'img':
            images += 1
            assert {'alt', 'width', 'height'} <= attrs.keys(), attrs
        if 'data-quote' in attrs:
            quotes += 1
            assert attrs['href'] == 'https://wa.me/525527699426'
    for art in (ROOT / 'assets').rglob('*.svg'):
        ET.fromstring(art.read_text())
    for script in (ROOT / 'herramientas').glob('*.py'):
        ast.parse(script.read_text())
    subprocess.run(['node', '--check', str(ROOT / 'script.js')], check=True)
    result = {'referenciasLocales': len(set(refs)), 'imagenesConDimensiones': images,
              'enlacesWhatsAppExactos': quotes, 'idsUnicos': len(ids),
              'svgValidos': len(list((ROOT / 'assets').rglob('*.svg'))),
              'sintaxisJS': 'OK', 'sintaxisPython': 'OK',
              'navegador': 'Pendiente; el entorno actual bloquea sockets y Chrome.',
              'capturas': 0}
    (ROOT / 'herramientas' / 'informe-local.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Verificación local:', json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local', action='store_true', help='Referencias, enlaces, SVG y sintaxis; sin navegador.')
    args = parser.parse_args()
    validate_local()
    if args.local:
        return
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    with tempfile.TemporaryDirectory(prefix='.verificacion-', dir=ROOT) as profile:
        chrome = shutil.which('google-chrome') or shutil.which('chromium')
        if not chrome:
            raise RuntimeError('Se requiere Chrome local; no se instala automáticamente.')
        process = subprocess.Popen([chrome, '--headless=new', '--no-sandbox', '--disable-dev-shm-usage',
                                    '--disable-background-networking', '--no-first-run', '--no-default-browser-check',
                                    '--remote-debugging-port=0', '--user-data-dir=' + profile, 'about:blank'],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            active = Path(profile) / 'DevToolsActivePort'
            for _ in range(100):
                if active.exists():
                    break
                if process.poll() is not None:
                    raise RuntimeError('Chrome no pudo iniciarse.')
                time.sleep(.05)
            port = active.read_text().splitlines()[0]
            endpoint = f'http://127.0.0.1:{port}'
            request = Request(endpoint + '/json/new?about:blank', method='PUT')
            with urlopen(request) as response:
                target = json.load(response)
            asyncio.run(run(f'http://127.0.0.1:{server.server_port}/index.html', target['webSocketDebuggerUrl']))
        finally:
            process.terminate()
            process.wait(timeout=10)
            server.shutdown()


if __name__ == '__main__':
    main()
