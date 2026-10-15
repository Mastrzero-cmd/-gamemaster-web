/**
 * Fondo fijo de toda la página (plano trasero azul suave sobre negro).
 * Es vectorial y se mueve muy poco con el scroll (ver `.backdropFar/.backdropNear`);
 * las piezas rojas de cada sección se desplazan más rápido por encima.
 */
export function Backdrop() {
  return (
    <div className="backdrop" aria-hidden="true">
      <svg className="backdropFar" viewBox="0 0 1600 1200" preserveAspectRatio="xMidYMid slice" focusable="false">
        <defs>
          <pattern id="bdHex" width="96" height="84" patternUnits="userSpaceOnUse">
            <path d="M24 0h48l24 42-24 42H24L0 42z" fill="none" stroke="#6f84ff" strokeWidth="2" />
          </pattern>
          <pattern id="bdDots" width="40" height="40" patternUnits="userSpaceOnUse">
            <circle cx="4" cy="4" r="2.2" fill="#8fa0ff" />
          </pattern>
        </defs>
        <rect width="1600" height="1200" fill="url(#bdHex)" opacity=".5" />
        <rect x="0" y="640" width="1600" height="560" fill="url(#bdDots)" opacity=".5" />
      </svg>
      <svg className="backdropNear" viewBox="0 0 1600 1200" preserveAspectRatio="xMidYMid slice" focusable="false">
        <g fill="none" stroke="#5a70f0" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" opacity=".55">
          <path d="M-20 220H260l60 60h280l40-40h360" />
          <path d="M1620 520H1300l-60 60H980l-40-40H700" />
          <path d="M-20 900H180l70-70h340" />
          <path d="M1620 940H1380l-70 70h-300" />
        </g>
        <g fill="#5a70f0" opacity=".5">
          <circle cx="600" cy="240" r="9" /><circle cx="960" cy="540" r="9" /><circle cx="590" cy="830" r="9" /><circle cx="1010" cy="1010" r="9" />
        </g>
        <circle cx="1280" cy="220" r="260" fill="#2a3a8a" opacity=".35" />
        <circle cx="260" cy="760" r="320" fill="#1f2c78" opacity=".45" />
        <path d="M1000 1200L1600 640v560z" fill="#2a3a8a" opacity=".3" />
      </svg>
    </div>
  );
}
