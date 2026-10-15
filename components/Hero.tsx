import Image from 'next/image';
import { ArrowRight, MessageCircle } from 'lucide-react';
import { catalog } from '@/app/data/catalog';
import { GENERAL_CONTACT_URL } from '@/lib/contact';
import { GameCard } from './catalog/GameCard';
import { GiantType, Sprite } from './art/Sprite';

const switch2Games = catalog.filter((game) => game.platform === 'Nintendo Switch 2');

export function Hero() {
  return (
    <section className="hero" id="inicio" aria-labelledby="hero-title" data-quote-bar-avoid>
      <div className="heroField depthPlane" aria-hidden="true" />
      <GiantType className="heroType">Play</GiantType>
      <div className="heroBlade depthPlane" aria-hidden="true" />
      <Sprite name="cartridge" className="heroSpriteCartridge" />
      <Sprite name="keycap" className="heroSpriteKeycap" />
      <Sprite name="memory-card" className="heroSpriteCard" />

      <div className="heroStage">
        <div className="heroCopy">
          <p className="pixelLabel heroKicker"><span aria-hidden="true">✢</span> Biblioteca digital · México <span aria-hidden="true">✢</span></p>
          <h1 id="hero-title">
            <span>Todo lo que</span>
            <span>quieres</span>
            <span className="heroAccent">jugar.</span>
          </h1>
          <div className="heroPlate">
            <p>
              Juegos digitales para Nintendo Switch y Switch 2, además de streaming e IA con ChatGPT y Claude.
              Eliges, te confirmamos precio y disponibilidad por WhatsApp, y juegas.
            </p>
            <div className="heroActions">
              <a className="buttonRed" href="#catalogo">Explorar catálogo <ArrowRight aria-hidden="true" /></a>
              <a className="buttonBlack" href={GENERAL_CONTACT_URL} target="_blank" rel="noreferrer"><MessageCircle aria-hidden="true" /> Hablar por WhatsApp</a>
            </div>
          </div>
        </div>

        <figure className="heroIcon" aria-hidden="true">
          <span className="heroIconRear depthPlane">
            <Image src="/art/cromo/panel-consoles-rear.webp" alt="" width={864} height={1152} unoptimized priority />
          </span>
          <span className="heroIconFront depthPlane">
            <Image src="/art/cromo/panel-consoles-front.webp" alt="" width={864} height={1152} unoptimized priority />
          </span>
          <figcaption className="pixelLabel">Lámina 01 · Consola, mandos y PC</figcaption>
        </figure>
      </div>

      <dl className="heroSpec" aria-label="GameMaster en breve">
        <div><dt>Catálogo</dt><dd>{catalog.length} títulos</dd></div>
        <div><dt>Plataformas</dt><dd>Switch · Switch 2</dd></div>
        <div><dt>Servicios</dt><dd>Streaming · IA · Privacidad</dd></div>
        <div><dt>Pago</dt><dd>Transferencia o depósito</dd></div>
        <div><dt>Atención</dt><dd>1:1 por WhatsApp</dd></div>
      </dl>

      <div className="heroRail" aria-labelledby="hero-rail-title">
        <div className="heroRailHeading">
          <h2 id="hero-rail-title" className="pixelLabel">Nuevo en Switch 2</h2>
          <a href="#catalogo">Ver todo el catálogo <ArrowRight aria-hidden="true" /></a>
        </div>
        <div className="heroRailTrack" tabIndex={0} role="region" aria-label="Juegos de Nintendo Switch 2. Desplázate horizontalmente para ver más.">
          {switch2Games.map((game, index) => <GameCard game={game} index={index} key={game.id} priority />)}
        </div>
      </div>
    </section>
  );
}
