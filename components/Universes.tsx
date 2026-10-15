'use client';

import Image from 'next/image';
import { ArrowUpRight, Check, Play, SendHorizontal } from 'lucide-react';
import { aiServices, privacyServices, streamingServices, type Service } from '@/app/data/services';
import { ServiceMark } from './ServiceMark';
import { GiantType, Sprite } from './art/Sprite';
import { useExperience } from './experience/useExperience';

function ServiceButton({ service, selected, onSelect, className = 'serviceLogo' }: {
  service: Service;
  selected: boolean;
  onSelect: () => void;
  className?: string;
}) {
  return (
    <button type="button" className={`${className} ${selected ? 'isSelected' : ''}`} onClick={onSelect} aria-pressed={selected}>
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
    <section className="universes" id="servicios" aria-labelledby="universes-title" data-quote-bar-avoid>
      <GiantType className="universesType">Stream</GiantType>
      <Sprite name="headphones" className="universesSpriteHeadphones" />
      <div className="universesHeading sectionShell">
        <p className="pixelLabel">✢ Capítulo 02 · Más allá del juego</p>
        <h2 id="universes-title">Streaming, IA y privacidad. <em>Bajo consulta.</em></h2>
        <dl className="universesLedger">
          <div><dt>Universos</dt><dd>03</dd></div>
          <div><dt>Servicios</dt><dd>Streaming · IA · Privacidad</dd></div>
          <div><dt>Precio</dt><dd>Vigente, por WhatsApp</dd></div>
        </dl>
      </div>

      <article className="universe universeStreaming" id="streaming" aria-labelledby="streaming-title" data-quote-bar-avoid>
        <div className="universeArt streamStage">
          <span className="streamSignal depthPlane" aria-hidden="true" />
          <Sprite name="clapperboard" className="streamSpriteClapper" />
          <Sprite name="remote" className="streamSpriteRemote" />
          <div className="streamScreen">
            <div className="streamBar" aria-hidden="true">
              <span className="streamBrand">GM</span>
              <span>Inicio</span>
              <span>Series</span>
              <span>Películas</span>
              <span>Anime</span>
              <span>Música</span>
            </div>
            <div className="streamFeature" aria-hidden="true">
              <span className="pixelLabel">En pantalla</span>
              <strong>Series, películas, anime y música</strong>
              <span className="streamPlay"><Play /></span>
              <span className="streamProgress"><i /></span>
            </div>
            <p className="streamRowLabel pixelLabel" id="streaming-row">Plataformas · elige una</p>
            <div className="streamTiles" role="group" aria-labelledby="streaming-row">
              {streamingServices.map((service) => (
                <ServiceButton
                  className="streamTile"
                  service={service}
                  selected={interest === service.name}
                  onSelect={() => setInterest(service.name)}
                  key={service.name}
                />
              ))}
            </div>
          </div>
          <span className="streamStand" aria-hidden="true" />
        </div>
        <div className="universeCopy">
          <p className="pixelLabel">Lámina 02 · Streaming y música</p>
          <h3 id="streaming-title">Series, música y anime</h3>
          <p>Explora familias de entretenimiento y pide una cotización vigente por el servicio que te interesa. No publicamos planes ni precios sin confirmarlos.</p>
          <a className="buttonBlack" href="#cotizar" onClick={() => setInterest(streamingInterest)}>Consultar precio <ArrowUpRight aria-hidden="true" /></a>
        </div>
      </article>

      <article className="universe universeAi" id="ia" aria-labelledby="ia-title" data-quote-bar-avoid>
        <div className="universeArt aiStage">
          <span className="aiChipRear depthPlane" aria-hidden="true">
            <Image src="/art/cromo/panel-chip-rear.webp" alt="" width={864} height={1152} unoptimized />
          </span>
          <span className="aiChipFront depthPlane" aria-hidden="true">
            <Image src="/art/cromo/panel-chip-front.webp" alt="" width={864} height={1152} unoptimized />
          </span>
          <Sprite name="keycap" className="aiSpriteKeycap" />
          <Sprite name="mouse" className="aiSpriteMouse" />
          <div className="aiChat">
            <div className="aiTabs" role="group" aria-label="Herramientas de IA consultables">
              {aiServices.map((service) => (
                <ServiceButton
                  className="aiTab"
                  service={service}
                  selected={interest === service.name}
                  onSelect={() => setInterest(service.name)}
                  key={service.name}
                />
              ))}
            </div>
            <div className="aiThread" aria-hidden="true">
              <p className="aiPrompt">Resume este documento en cinco puntos.</p>
              <div className="aiReply">
                <i style={{ width: '92%' }} />
                <i style={{ width: '78%' }} />
                <i style={{ width: '86%' }} />
                <i style={{ width: '54%' }} />
                <b />
              </div>
            </div>
            <div className="aiInput" aria-hidden="true">
              <span>Escribe tu mensaje…</span>
              <SendHorizontal />
            </div>
          </div>
        </div>
        <div className="universeCopy">
          <p className="pixelLabel">Lámina 03 · Inteligencia artificial</p>
          <h3 id="ia-title">IA para crear y trabajar</h3>
          <p>ChatGPT y Claude forman la oferta actual de IA. Precio, modalidad y disponibilidad se consultan al momento.</p>
          <a className="buttonBlack" href="#cotizar" onClick={() => setInterest(aiInterest)}>Consultar precio <ArrowUpRight aria-hidden="true" /></a>
        </div>
      </article>

      <article className="universePrivacy sectionShell" id="privacidad" aria-labelledby="privacy-title">
        <Sprite name="phone" className="privacySpritePhone" />
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
