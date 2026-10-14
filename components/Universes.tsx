'use client';

import Image from 'next/image';
import { ArrowUpRight, Check } from 'lucide-react';
import { aiServices, privacyServices, streamingServices, type Service } from '@/app/data/services';
import { ServiceMark } from './ServiceMark';
import { useExperience } from './experience/useExperience';

function ServiceButton({ service, selected, onSelect }: {
  service: Service;
  selected: boolean;
  onSelect: () => void;
}) {
  return (
    <button type="button" className={`serviceLogo ${selected ? 'isSelected' : ''}`} onClick={onSelect} aria-pressed={selected}>
      <ServiceMark src={service.logo} />
      <span className="serviceName">{service.name}</span>
      {selected && <Check className="serviceCheck" aria-hidden="true" />}
    </button>
  );
}

export function Universes() {
  const { interest, setInterest } = useExperience();
  const streamingInterest = streamingServices.some((service) => service.name === interest) ? interest : 'Streaming';
  const aiInterest = aiServices.some((service) => service.name === interest) ? interest : 'ChatGPT';

  return (
    <section className="universes" id="servicios" aria-labelledby="universes-title">
      <div className="universesHeading sectionShell">
        <p className="pixelLabel">✢ Capítulo 02 · Más allá del juego</p>
        <h2 id="universes-title">Streaming, IA y privacidad. <em>Bajo consulta.</em></h2>
        <dl className="universesLedger">
          <div><dt>Universos</dt><dd>03</dd></div>
          <div><dt>Servicios</dt><dd>Streaming · IA · Privacidad</dd></div>
          <div><dt>Precio</dt><dd>Vigente, por WhatsApp</dd></div>
        </dl>
      </div>

      <article className="universe universeStreaming" id="streaming" aria-labelledby="streaming-title">
        <figure className="universeArt depthPlane" aria-hidden="true">
          <Image src="/art/cromo/panel-streaming.webp" alt="" width={864} height={1152} unoptimized />
        </figure>
        <div className="universeCopy">
          <p className="pixelLabel">Lámina 02 · Streaming y música</p>
          <h3 id="streaming-title">Series, música y anime</h3>
          <p>Explora familias de entretenimiento y pide una cotización vigente por el servicio que te interesa. No publicamos planes ni precios sin confirmarlos.</p>
          <div className="serviceLogoGrid" role="group" aria-label="Servicios de streaming y música consultables">
            {streamingServices.map((service) => (
              <ServiceButton service={service} selected={interest === service.name} onSelect={() => setInterest(service.name)} key={service.name} />
            ))}
          </div>
          <a className="buttonBlack" href="#cotizar" onClick={() => setInterest(streamingInterest)}>Consultar precio <ArrowUpRight aria-hidden="true" /></a>
        </div>
      </article>

      <article className="universe universeAi" id="ia" aria-labelledby="ia-title">
        <figure className="universeArt depthPlane" aria-hidden="true">
          <Image src="/art/cromo/panel-ia.webp" alt="" width={864} height={1152} unoptimized />
        </figure>
        <div className="universeCopy">
          <p className="pixelLabel">Lámina 03 · Inteligencia artificial</p>
          <h3 id="ia-title">IA para crear y trabajar</h3>
          <p>ChatGPT y Claude forman la oferta actual de IA. Precio, modalidad y disponibilidad se consultan al momento.</p>
          <div className="serviceLogoGrid serviceLogoGridPair" role="group" aria-label="Herramientas de IA consultables">
            {aiServices.map((service) => (
              <ServiceButton service={service} selected={interest === service.name} onSelect={() => setInterest(service.name)} key={service.name} />
            ))}
          </div>
          <a className="buttonBlack" href="#cotizar" onClick={() => setInterest(aiInterest)}>Consultar precio <ArrowUpRight aria-hidden="true" /></a>
        </div>
      </article>

      <article className="universePrivacy sectionShell" id="privacidad" aria-labelledby="privacy-title">
        <p className="pixelLabel">Universo 04 · Servicios digitales</p>
        <h3 id="privacy-title">Privacidad digital</h3>
        <p>Proton VPN pertenece a una familia propia. Precio, duración y disponibilidad se consultan al momento.</p>
        <div className="serviceLogoGrid serviceLogoGridSingle" role="group" aria-label="Servicios de privacidad consultables">
          {privacyServices.map((service) => (
            <ServiceButton service={service} selected={interest === service.name} onSelect={() => setInterest(service.name)} key={service.name} />
          ))}
        </div>
        <a className="buttonBlack" href="#cotizar" onClick={() => setInterest('Proton VPN')}>Consultar precio <ArrowUpRight aria-hidden="true" /></a>
      </article>

      <p className="universesDisclaimer sectionShell">Las marcas pertenecen a sus respectivos titulares. Su presencia no implica afiliación, patrocinio ni disponibilidad garantizada.</p>
    </section>
  );
}
