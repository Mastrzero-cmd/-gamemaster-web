Las capturas de navegador están pendientes.

En esta sesión, `python3 -m http.server` falló con `PermissionError: [Errno 1] Operation not permitted`. Chrome headless también falló al iniciar con `setsockopt: Operation not permitted`. No se generaron imágenes que puedan confundirse con capturas reales de la página.

En un entorno que permita iniciar el servidor y Chrome, ejecuta desde la raíz del repositorio:

```sh
python3 identidad-v9e/herramientas/capturar.py
```

El script usa Python como servidor local y Chrome/Chromium headless ya instalado. No instala paquetes ni descarga recursos. Produce `v9e-1440.png`, `v9e-390.png` de página completa y un reporte en `herramientas/navegador.json`. También comprueba el ancho de 430 px. Al terminar, cierra el servidor y el navegador.

Revisa ambas capturas visualmente después de generarlas. La comprobación automática no sustituye esa revisión.
