import { ArrowRight, Check, Gamepad2, UserRound, UsersRound, Wifi, WifiOff } from 'lucide-react';

const steps = [
  ['01', 'Elige tus juegos', 'Busca en el catálogo y agrega los títulos que quieres revisar.'],
  ['02', 'Confirmamos contigo', 'Revisamos precio, modalidad y disponibilidad antes de cualquier pago.'],
  ['03', 'Realiza tu pago', 'Transferencia o depósito después de validar tu solicitud.'],
  ['04', 'Descarga y juega', 'Recibes las indicaciones para descargar el título en tu consola.'],
];

export function PurchaseModes() {
  return (
    <section className="modesSection" id="modalidades" aria-labelledby="modes-title">
      <div className="modesRearBand depthPlane" aria-hidden="true" />
      <div className="sectionShell">
        <div className="sectionHeading">
          <p className="pixelLabel">✢ Capítulo 03 · Cómo funciona</p>
          <h2 id="modes-title">Dos formas de <em>jugar.</em></h2>
          <p>Ambas opciones son el mismo juego digital completo. Cambian la forma de acceso y la verificación por internet.</p>
        </div>

        <div className="modeGrid">
          <article className="modeCard modePrincipal">
            <header>
              <span className="pixelLabel">Opción 01 · Mayor comodidad</span>
              <h3>Cuenta Principal</h3>
            </header>
            <ul>
              <li><UserRound aria-hidden="true" /><span>Juega con cualquier usuario o perfil de la consola.</span></li>
              <li><WifiOff aria-hidden="true" /><span>Puede abrirse y jugarse sin conexión a internet.</span></li>
              <li><Gamepad2 aria-hidden="true" /><span>La opción más cómoda según la información fuente.</span></li>
            </ul>
            <a href="#cotizar">Consultar esta modalidad <ArrowRight aria-hidden="true" /></a>
          </article>
          <article className="modeCard modeSecondary">
            <header>
              <span className="pixelLabel">Opción 02 · Económica</span>
              <h3>Cuenta Secundaria</h3>
            </header>
            <ul>
              <li><Check aria-hidden="true" /><span>Se juega desde el perfil proporcionado para el título.</span></li>
              <li><Wifi aria-hidden="true" /><span>Necesita una conexión breve al abrir para verificar.</span></li>
              <li><UsersRound aria-hidden="true" /><span>El juego en línea depende del título y se confirma antes.</span></li>
            </ul>
            <a href="#cotizar">Consultar esta modalidad <ArrowRight aria-hidden="true" /></a>
          </article>
        </div>

        <ol className="purchaseSteps" aria-label="Pasos para comprar">
          {steps.map(([number, title, description]) => (
            <li key={number}><span className="pixelLabel">{number}</span><h3>{title}</h3><p>{description}</p></li>
          ))}
        </ol>
      </div>
    </section>
  );
}
