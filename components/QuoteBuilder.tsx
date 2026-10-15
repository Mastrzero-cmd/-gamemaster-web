'use client';

import { useState } from 'react';
import { ArrowUpRight, Check, Copy, MessageCircle, X } from 'lucide-react';
import { useExperience } from './experience/useExperience';
import { Sprite } from './art/Sprite';

const interests = ['Nintendo Switch digital', 'Streaming', 'IA / ChatGPT + Claude', 'Privacidad / Proton VPN'];

export function QuoteBuilder() {
  const [copied, setCopied] = useState(false);
  const { selectedGames, selectedCount, interest, quoteMessage, whatsappUrl, setInterest, removeGame } = useExperience();

  const copyRequest = async () => {
    try {
      await navigator.clipboard.writeText(quoteMessage);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  };

  const chooseInterest = (value: string) => {
    setInterest(value);
    setCopied(false);
  };

  return (
    <section className="quoteSection" id="cotizar" aria-labelledby="quote-title" data-quote-bar-avoid>
      <div className="quoteSlab depthPlane" aria-hidden="true" />
      <Sprite name="cartridge" className="quoteSpriteCartridge" />
      <Sprite name="memory-card" className="quoteSpriteCard" />
      <Sprite name="heart" className="quoteSpriteHeart" />
      <div className="sectionShell quoteLayout">
        <div className="quoteCopy">
          <p className="pixelLabel">✢ Capítulo 04 · Cotización</p>
          <h2 id="quote-title">Arma tu <em>solicitud.</em></h2>
          <p>Elige un interés, agrega uno o varios juegos y envía un solo mensaje por WhatsApp. Una persona te responde con precio y disponibilidad vigentes.</p>
        </div>

        <div className="quoteBuilder">
          <div className="quoteBuilderHeader">
            <span className="pixelLabel">Solicitud / GM</span>
            <strong aria-live="polite">{String(selectedCount).padStart(2, '0')}</strong>
          </div>
          <fieldset className="quoteInterests">
            <legend>¿Qué te interesa?</legend>
            <p>{interest || 'Elige una categoría para orientar tu solicitud.'}</p>
            <div>
              {interests.map((option) => {
                const active = interest === option
                  || (option === 'IA / ChatGPT + Claude' && ['ChatGPT', 'Claude'].includes(interest))
                  || (option === 'Privacidad / Proton VPN' && interest === 'Proton VPN');
                return (
                  <button type="button" className={active ? 'isActive' : ''} aria-pressed={active} onClick={() => chooseInterest(option)} key={option}>
                    {active && <Check aria-hidden="true" />} {option}
                  </button>
                );
              })}
            </div>
          </fieldset>
          <div className="quoteSelection" aria-live="polite">
            <div className="quoteSelectionHeading"><span className="pixelLabel">Juegos seleccionados</span><strong>{selectedCount}</strong></div>
            {selectedGames.length ? (
              <ul>
                {selectedGames.map((game) => (
                  <li key={game.id}><span>{game.title}</span><button type="button" onClick={() => removeGame(game.id)} aria-label={`Quitar ${game.title}`}><X aria-hidden="true" /></button></li>
                ))}
              </ul>
            ) : (
              <p>Agrega juegos desde cualquier portada con el botón <strong>+</strong>. Puedes seleccionar más de uno.</p>
            )}
          </div>
          <div className="quoteActions">
            <a className="buttonRed" href={whatsappUrl} target="_blank" rel="noreferrer"><MessageCircle aria-hidden="true" /> Cotizar por WhatsApp <ArrowUpRight aria-hidden="true" /></a>
            <button className="buttonGhost" type="button" onClick={copyRequest}>
              {copied ? <><Check aria-hidden="true" /> Solicitud copiada</> : <><Copy aria-hidden="true" /> Copiar solicitud</>}
            </button>
          </div>
          <small>No se publica un precio fijo: se confirma antes de cada compra.</small>
        </div>
      </div>
    </section>
  );
}
