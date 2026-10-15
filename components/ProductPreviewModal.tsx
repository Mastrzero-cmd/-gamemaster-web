'use client';

import Image from 'next/image';
import Link from 'next/link';
import { useEffect, useRef } from 'react';
import { ArrowUpRight, Check, MessageCircle, Plus, X } from 'lucide-react';
import { getGameBySlug } from '@/app/data/catalog';
import { gameQuoteMessage, toWhatsApp } from '@/lib/contact';
import { useExperience } from './experience/useExperience';

export function ProductPreviewModal() {
  const modalRef = useRef<HTMLElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);
  const { previewSlug, closePreview, isSelected, toggleGame } = useExperience();
  const game = previewSlug ? getGameBySlug(previewSlug) : undefined;

  useEffect(() => {
    if (!game) return;
    const previousOverflow = document.body.style.overflow;
    previousFocusRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    document.body.style.overflow = 'hidden';

    const focusableSelector = 'button:not([disabled]), a[href], input:not([disabled]), [tabindex]:not([tabindex="-1"])';
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        closePreview();
        return;
      }
      if (event.key !== 'Tab') return;
      const focusable = modalRef.current?.querySelectorAll<HTMLElement>(focusableSelector);
      if (!focusable?.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    requestAnimationFrame(() => modalRef.current?.querySelector<HTMLElement>('[data-modal-close]')?.focus());

    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener('keydown', handleKeyDown);
      previousFocusRef.current?.focus();
    };
  }, [closePreview, game]);

  if (!game) return null;
  const selected = isSelected(game.id);

  return (
    <div className="modalBackdrop" onMouseDown={(event) => {
      if (event.target === event.currentTarget) closePreview();
    }}>
      <section ref={modalRef} className="productModal" role="dialog" aria-modal="true" aria-labelledby="preview-title" aria-describedby="preview-description">
        <button data-modal-close className="modalClose" type="button" onClick={closePreview} aria-label="Cerrar vista rápida"><X aria-hidden="true" /></button>
        <div className="modalArtwork">
          <Image src={game.image} alt={`Portada de ${game.title}`} fill sizes="(max-width: 760px) 100vw, 42vw" />
          <span aria-hidden="true">VISTA / RÁPIDA</span>
        </div>
        <div className="modalCopy">
          <p>{game.platform} · {game.sourceCategory}</p>
          <h2 id="preview-title">{game.title}</h2>
          <div className="modalTags" aria-label="Metadatos del juego">
            {game.genres.slice(0, 3).map((genre) => <span key={genre}>{genre}</span>)}
            {game.worlds.slice(0, 2).map((world) => <span key={world}>{world}</span>)}
          </div>
          <p id="preview-description" className="modalDescription">Título digital registrado para {game.platform}. La modalidad, el precio y la disponibilidad se confirman al momento de cotizar.</p>
          <dl className="modalStatus">
            <div><dt>PRECIO</dt><dd>Consultar precio</dd></div>
            <div><dt>DISPONIBILIDAD</dt><dd>Consultar disponibilidad</dd></div>
          </dl>
          <div className="modalActions">
            <button type="button" onClick={() => toggleGame(game)} aria-pressed={selected}>{selected ? <Check aria-hidden="true" /> : <Plus aria-hidden="true" />} {selected ? 'Agregado a tu solicitud' : 'Agregar a tu solicitud'}</button>
            <a href={toWhatsApp(gameQuoteMessage(game.title, game.platform))} target="_blank" rel="noreferrer"><MessageCircle aria-hidden="true" /> Cotizar por WhatsApp</a>
          </div>
          <Link className="modalDetailLink" href={`/juegos/${game.slug}`} onClick={closePreview}>Ver ficha <ArrowUpRight aria-hidden="true" /></Link>
          <small className="modalNote">GameMaster es un negocio independiente. La portada se muestra como referencia del título.</small>
        </div>
      </section>
    </div>
  );
}
