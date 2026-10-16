#!/usr/bin/env python3
"""Servidor Python + Chrome headless, sin paquetes, descargas ni sitios externos.

Uso: python3 identidad-v9e/herramientas/capturar.py
Necesita un entorno que permita iniciar procesos de Chrome y un servidor local.
"""
from pathlib import Path
import base64
import json
import os
import select
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
URL = 'http://127.0.0.1:8765/'


class Chrome:
    """Protocolo de Chrome mediante tuberías, sin puerto de depuración."""
    def __init__(self, executable, profile):
        args = [executable, '--headless=new', '--no-sandbox', '--disable-gpu',
                '--disable-dev-shm-usage', '--disable-background-networking',
                '--disable-component-update', '--disable-sync', '--no-first-run',
                '--no-default-browser-check', '--disable-extensions',
                '--no-proxy-server', '--disable-breakpad',
                '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1, EXCLUDE localhost',
                '--remote-debugging-pipe', f'--user-data-dir={profile}', 'about:blank']
        # Chrome espera sus canales de control en los descriptores 3 y 4.
        self.process = subprocess.Popen(
            ['bash', '-c', 'exec 3<&0 4>&1\nexec "$@"', 'v9e-chrome', *args],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.buffer, self.serial, self.session = b'', 0, None
        self.errors, self.remote = [], set()

    def packet(self):
        deadline = time.monotonic() + 25
        while b'\0' not in self.buffer:
            if self.process.poll() is not None:
                raise RuntimeError('Chrome no pudo iniciar. Revisa los permisos del entorno.')
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError('Chrome no respondió en el tiempo previsto.')
            if select.select([self.process.stdout], [], [], remaining)[0]:
                data = os.read(self.process.stdout.fileno(), 1024 * 1024)
                if not data:
                    raise RuntimeError('Chrome cerró su canal de control.')
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
        self.evaluate('new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))')

    def navigate(self, width, height):
        self.call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height,
                  'deviceScaleFactor': 1, 'mobile': width < 700})
        self.call('Emulation.setTouchEmulationEnabled', {'enabled': width < 700})
        self.call('Page.navigate', {'url': URL})
        for _ in range(100):
            try:
                if self.evaluate("document.readyState === 'complete' && !!document.getElementById('gaming')"):
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
        path = ROOT / 'capturas' / f'v9e-{width}.png'
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


def run():
    executable = next((shutil.which(n) for n in ['google-chrome', 'chromium', 'chromium-browser']
                       if shutil.which(n)), None)
    if not executable:
        raise RuntimeError('No hay Chrome o Chromium instalado. No se descargó nada.')
    report = {'pruebas': [], 'capturas': []}

    def check(value, name):
        report['pruebas'].append({'prueba': name, 'ok': bool(value)})
        if not value:
            raise RuntimeError(f'Falló: {name}')

    server = subprocess.Popen([sys.executable, '-m', 'http.server', '8765', '--bind',
                               '127.0.0.1', '--directory', str(ROOT)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    chrome = None
    try:
        for _ in range(40):
            if server.poll() is not None:
                raise RuntimeError('No se pudo iniciar python3 -m http.server en 127.0.0.1:8765.')
            try:
                with urlopen(URL, timeout=.2) as response:
                    if response.status == 200:
                        break
            except OSError:
                time.sleep(.05)
        else:
            raise RuntimeError('El entorno no permite abrir el servidor local.')

        with tempfile.TemporaryDirectory(prefix='.chromium-', dir=ROOT / 'herramientas') as profile:
            chrome = Chrome(executable, profile)
            try:
                target = chrome.call('Target.createTarget', {'url': 'about:blank'}, scoped=False)['targetId']
                chrome.session = chrome.call('Target.attachToTarget', {'targetId': target, 'flatten': True}, scoped=False)['sessionId']
                for method in ('Page.enable', 'Runtime.enable', 'Network.enable'):
                    chrome.call(method)
                chrome.call('Network.setBlockedURLs', {'urls': ['https://*']})

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
                    if width in (1440, 390):
                        report['capturas'].append(chrome.screenshot(width))

                chrome.navigate(1440, 1000)
                chrome.evaluate("document.querySelector('[data-controls=\"games-rail\"] [data-step=\"1\"]').click()")
                chrome.evaluate('new Promise(r => setTimeout(r, 700))')
                check(chrome.evaluate("document.getElementById('games-rail').scrollLeft > 0"), 'Carrusel con botones')
                chrome.evaluate("scrollTo({top:0,behavior:'instant'})")
                chrome.settle()
                before = chrome.evaluate("[...document.querySelectorAll('.hero [data-plane]')].slice(0,2).map(e => new DOMMatrix(getComputedStyle(e).transform).m42)")
                chrome.evaluate("scrollTo({top:300,behavior:'instant'})")
                chrome.settle()
                after = chrome.evaluate("[...document.querySelectorAll('.hero [data-plane]')].slice(0,2).map(e => new DOMMatrix(getComputedStyle(e).transform).m42)")
                check(abs(after[1] - before[1]) > 2*abs(after[0] - before[0]), 'Rojo más rápido que plano trasero al desplazar')
                chrome.call('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': 1200, 'y': 250})
                chrome.settle()
                check(chrome.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('.hero [data-plane=front]')).transform).m41 !== 0"), 'Parallax de puntero')
                chrome.call('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'reduce'}]})
                chrome.settle()
                check(chrome.evaluate("[...document.querySelectorAll('[data-plane]')].every(e => getComputedStyle(e).transform === 'none')"), 'Movimiento reducido: planos quietos')
                check(not chrome.errors, 'Sin errores de JavaScript ni recursos')
                check(not chrome.remote, 'Ninguna solicitud a sitios externos')
                report['ok'] = True
            finally:
                chrome.close()
    except Exception as error:
        report['ok'] = False
        report['error'] = str(error)
        raise
    finally:
        if server.poll() is None:
            server.terminate()
            server.wait(timeout=5)
        (ROOT / 'herramientas/navegador.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Capturas y pruebas listas. Revisa visualmente ambos PNG en capturas/.')


if __name__ == '__main__':
    try:
        run()
    except Exception as error:
        sys.exit(f'No se completó la captura: {error}')
