#!/usr/bin/env python3
"""Chrome local por tuberías, sin servidor, paquetes ni descargas.

Uso: python3 identidad-v10e/herramientas/capturar.py
Para probar sin imágenes: añade --solo-pruebas. Necesita Chrome instalado.
"""
from pathlib import Path
import argparse
import base64
import json
import os
import select
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / 'index.html').as_uri()


class Chrome:
    """Protocolo de Chrome mediante tuberías, sin puerto de depuración."""
    def __init__(self, executable, profile):
        args = [executable, '--headless=new', '--no-sandbox', '--disable-gpu',
                '--disable-dev-shm-usage', '--allow-file-access-from-files', '--disable-background-networking',
                '--disable-component-update', '--disable-sync', '--no-first-run',
                '--no-default-browser-check', '--disable-extensions',
                '--no-proxy-server', '--disable-breakpad',
                '--host-resolver-rules=MAP * ~NOTFOUND',
                '--remote-debugging-pipe', f'--user-data-dir={profile}', 'about:blank']
        # Chrome espera sus canales de control en los descriptores 3 y 4.
        self.stderr = tempfile.TemporaryFile()
        self.process = subprocess.Popen(
            ['bash', '-c', 'exec 3<&0 4>&1\nexec "$@"', 'v10e-chrome', *args],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr)
        self.buffer, self.serial, self.session = b'', 0, None
        self.errors, self.remote = [], set()

    def startup_error(self):
        self.stderr.seek(0)
        detail = self.stderr.read().decode('utf-8', errors='replace').strip()
        return 'Chrome no pudo iniciar. ' + (detail[-1200:] or 'Revisa los permisos del entorno.')

    def packet(self):
        deadline = time.monotonic() + 25
        while b'\0' not in self.buffer:
            if self.process.poll() is not None:
                raise RuntimeError(self.startup_error())
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError('Chrome no respondió en el tiempo previsto.')
            if select.select([self.process.stdout], [], [], remaining)[0]:
                data = os.read(self.process.stdout.fileno(), 1024 * 1024)
                if not data:
                    raise RuntimeError(self.startup_error())
                self.buffer += data
        raw, self.buffer = self.buffer.split(b'\0', 1)
        return json.loads(raw)

    def call(self, method, params=None, scoped=True):
        self.serial += 1
        ident = self.serial
        command = {'id': ident, 'method': method, 'params': params or {}}
        if scoped and self.session:
            command['sessionId'] = self.session
        self.process.stdin.write(json.dumps(command).encode() + b'\0')
        self.process.stdin.flush()
        while True:
            item = self.packet()
            if item.get('method') == 'Runtime.consoleAPICalled' and item['params']['type'] == 'error':
                self.errors.append(item['params'])
            if item.get('method') == 'Log.entryAdded' and item['params']['entry']['level'] == 'error':
                self.errors.append(item['params']['entry'])
            if item.get('method') == 'Network.loadingFailed' and not item['params'].get('canceled'):
                self.errors.append(item['params'])
            if item.get('method') == 'Runtime.exceptionThrown':
                self.errors.append(item['params']['exceptionDetails'])
            if item.get('method') == 'Network.responseReceived':
                response = item['params']['response']
                if response['status'] >= 400:
                    self.errors.append({'recurso': response['url'], 'estado': response['status']})
            if item.get('method') == 'Network.requestWillBeSent':
                url = item['params']['request']['url']
                if url.startswith(('http://', 'https://')) and not url.startswith(URL):
                    self.remote.add(url)
            if item.get('id') == ident:
                if 'error' in item:
                    raise RuntimeError(f"{method}: {item['error']}")
                return item.get('result', {})

    def evaluate(self, expression):
        response = self.call('Runtime.evaluate', {'expression': expression,
                            'awaitPromise': True, 'returnByValue': True})
        if 'exceptionDetails' in response:
            raise RuntimeError(str(response['exceptionDetails']))
        return response.get('result', {}).get('value')

    def settle(self):
        self.evaluate('new Promise(r => setTimeout(r, 1100))')

    def navigate(self, width, height, query=''):
        self.call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height,
                  'deviceScaleFactor': 1, 'mobile': width < 700})
        self.call('Emulation.setTouchEmulationEnabled', {'enabled': width < 700})
        self.evaluate('window.__navigationPending = true')
        result = self.call('Page.navigate', {'url': URL + query})
        if result.get('errorText'):
            raise RuntimeError(result['errorText'])
        for _ in range(100):
            try:
                if self.evaluate("!window.__navigationPending && document.readyState === 'complete' && !!document.getElementById('gaming')"):
                    break
            except RuntimeError:
                pass
            time.sleep(.05)
        else:
            raise RuntimeError('La página local no terminó de cargar.')
        self.evaluate("""(async () => {
          document.querySelectorAll('img').forEach(img => img.loading = 'eager');
          await document.fonts.ready;
          await Promise.all([...document.images].map(img => img.complete ? true :
            new Promise(resolve => { img.onload = img.onerror = resolve; setTimeout(resolve, 10000); })));
          scrollTo({top: 0, behavior: 'instant'});
        })()""")
        self.settle()

    def screenshot(self, width):
        height = self.evaluate('Math.ceil(document.documentElement.scrollHeight)')
        result = self.call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': True,
                           'clip': {'x': 0, 'y': 0, 'width': width, 'height': height, 'scale': 1}})
        path = ROOT / 'capturas' / f'v10e-{width}.png'
        path.write_bytes(base64.b64decode(result['data']))
        return str(path.relative_to(ROOT))

    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        self.process.stdin.close()
        self.process.stdout.close()
        self.stderr.close()


def run(capture=True):
    executable = next((shutil.which(n) for n in ['google-chrome', 'chromium', 'chromium-browser']
                       if shutil.which(n)), None)
    if not executable:
        raise RuntimeError('No hay Chrome o Chromium instalado. No se descargó nada.')
    report = {'version': 'v10e', 'modo': 'capturas' if capture else 'solo-pruebas', 'pruebas': [], 'capturas': []}

    def check(value, name):
        report['pruebas'].append({'prueba': name, 'ok': bool(value)})
        if not value:
            raise RuntimeError(f'Falló: {name}')

    try:
        with tempfile.TemporaryDirectory(prefix='.chromium-', dir=ROOT / 'herramientas') as profile:
            chrome = Chrome(executable, profile)
            try:
                target = chrome.call('Target.createTarget', {'url': 'about:blank'}, scoped=False)['targetId']
                chrome.session = chrome.call('Target.attachToTarget', {'targetId': target, 'flatten': True}, scoped=False)['sessionId']
                for method in ('Page.enable', 'Runtime.enable', 'Network.enable', 'Log.enable'):
                    chrome.call(method)
                chrome.call('Network.setBlockedURLs', {'urls': ['http://*', 'https://*']})

                for width, height in [(1440, 1000), (390, 844), (430, 900)]:
                    chrome.navigate(width, height)
                    check(chrome.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), f'Sin desborde a {width}px')
                    check(chrome.evaluate('[...document.images].every(i => i.complete && i.naturalWidth > 0)'), f'Imágenes completas a {width}px')
                    check(chrome.evaluate("[...document.querySelectorAll('.game h3')].every(e => e.scrollWidth <= e.clientWidth + 1)"), f'Títulos largos a {width}px')
                    chrome.evaluate("document.getElementById('game-search').value='zzzzqqq'; document.getElementById('game-search').dispatchEvent(new Event('input'))")
                    check(chrome.evaluate("!document.querySelector('.empty-state').hidden && document.querySelectorAll('.game:not([hidden])').length === 0"), f'Búsqueda vacía a {width}px')
                    chrome.evaluate("document.getElementById('reset-search').click(); document.querySelector('[data-collection=\"switch2\"]').click()")
                    check(chrome.evaluate("document.querySelectorAll('.game:not([hidden])').length === 2"), f'Colección Switch 2 a {width}px')
                    chrome.evaluate("document.querySelector('[data-collection=\"all\"]').click(); document.activeElement.blur(); scrollTo({top:0,behavior:'instant'})")
                    chrome.call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
                    chrome.call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
                    check(chrome.evaluate("document.activeElement.matches(':focus-visible')"), f'Foco de teclado visible a {width}px')
                    chrome.evaluate("document.activeElement.blur(); scrollTo({top:0,behavior:'instant'})")
                    chrome.settle()
                    if capture and width in (1440, 390):
                        report['capturas'].append(chrome.screenshot(width))

                def positions():
                    return chrome.evaluate("""['rear','front-1','front-2','front-3'].map(name => {
                      const matrix = new DOMMatrix(getComputedStyle(document.querySelector(`.hero [data-plane="${name}"]`)).transform);
                      return {x: matrix.m41, y: matrix.m42};
                    })""")

                for width, height in [(1440, 1000), (390, 844)]:
                    chrome.navigate(width, height)
                    before = positions()
                    chrome.evaluate("scrollTo({top:300,behavior:'instant'})")
                    chrome.settle()
                    after = positions()
                    changes = [abs(a['y'] - b['y']) for a, b in zip(after, before)]
                    expected = [300 * speed * (0.5 if width < 700 else 1) for speed in [.015, .10, .18, .28]]
                    check(all(abs(a-b) < 1 for a, b in zip(changes, expected)), f'Cuatro velocidades de scroll a {width}px')
                    check(changes[3] > changes[2] > changes[1] > 5*changes[0], f'Frente claramente separado del fondo a {width}px')
                    report.setdefault('movimiento', []).append({'ancho': width, 'cambio_px': changes})
                    chrome.evaluate("scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
                    chrome.settle()
                    positions_end = positions()
                    check(chrome.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), f'Sin desborde al tope a {width}px')
                    scale = 0.5 if width < 700 else 1
                    check(all(abs(p['y']) <= limit*scale + .1 for p, limit in zip(positions_end, [18,80,130,184])), f'Amplitud limitada a {width}px')
                    chrome.evaluate("scrollTo({top:0,behavior:'instant'})")
                    chrome.settle()
                    check(chrome.evaluate("""(() => {
                      const clip = document.querySelector('.hero-art').getBoundingClientRect();
                      const rear = document.querySelector('.atlas').getBoundingClientRect();
                      return rear.left <= clip.left && rear.right >= clip.right && rear.top <= clip.top && rear.bottom >= clip.bottom;
                    })()"""), f'Plano trasero cubre el área recortada a {width}px')
                    check(chrome.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), f'Sin desborde con capas desplazadas a {width}px')
                    check(chrome.evaluate("""document.fonts.check('800 32px Unbounded') &&
                      document.fonts.check('700 24px Unbounded') && document.fonts.check('400 16px "Space Grotesk"') &&
                      document.fonts.check('500 16px "Space Grotesk"') && document.fonts.check('700 16px "Space Grotesk"')"""), f'Cinco fuentes locales cargadas a {width}px')

                chrome.navigate(1440, 1000)
                chrome.call('Emulation.setEmulatedMedia', {'features': [{'name': 'pointer', 'value': 'fine'}, {'name': 'hover', 'value': 'hover'}]})
                chrome.evaluate("document.querySelector('[data-controls=\"games-rail\"] [data-step=\"1\"]').click()")
                chrome.settle()
                check(chrome.evaluate("document.getElementById('games-rail').scrollLeft > 0"), 'Carrusel con botones')
                chrome.call('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': 1200, 'y': 250})
                chrome.settle()
                pointer = positions()
                check(abs(pointer[3]['x']) > abs(pointer[2]['x']) > abs(pointer[1]['x']) > 5*abs(pointer[0]['x']), 'Puntero más amplio en las tres capas de frente')
                chrome.call('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'reduce'}]})
                chrome.settle()
                stationary = "document.documentElement.classList.contains('reduce-motion') && [...document.querySelectorAll('[data-plane], [data-plane] img')].every(e => getComputedStyle(e).transform === 'none' && !e.style.transform)"
                check(chrome.evaluate(stationary), 'Preferencia del sistema: sin transformaciones')
                chrome.call('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'no-preference'}]})
                chrome.settle()
                check(chrome.evaluate("!document.documentElement.classList.contains('reduce-motion')"), 'Movimiento vuelve al quitar la preferencia del sistema')
                for query in ['?reduce', '?reduce=1']:
                    chrome.navigate(1440, 1000, query)
                    chrome.evaluate("scrollTo({top:300,behavior:'instant'})")
                    chrome.call('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': 1200, 'y': 250})
                    chrome.settle()
                    check(chrome.evaluate(stationary), f'{query}: sin transformaciones con scroll y puntero')
                    check(chrome.evaluate("getComputedStyle(document.documentElement).scrollBehavior === 'auto'"), f'{query}: sin scroll animado')
                check(not chrome.errors, 'Sin errores de JavaScript, consola ni recursos')
                check(not chrome.remote, 'Ninguna solicitud HTTP o HTTPS')
                report['ok'] = True
            finally:
                chrome.close()
    except Exception as error:
        report['ok'] = False
        report['error'] = str(error)
        raise
    finally:
        (ROOT / 'herramientas/navegador.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Pruebas de navegador aprobadas.' + (' Capturas listas.' if capture else ' Sin generar capturas.'))


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--solo-pruebas', action='store_true', help='Revisar sin crear imágenes')
        run(capture=not parser.parse_args().solo_pruebas)
    except Exception as error:
        sys.exit(f'No se completó la revisión: {error}')
