'use client';

import { useEffect, useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import type { Game } from '@/app/data/catalog';
import { GameCard } from './GameCard';

const shelfVariants = ['band', 'open', 'tab'] as const;

export function CatalogShelf({ id, title, description, games, position }: {
  id: string;
  title: string;
  description: string;
  games: Game[];
  position: number;
}) {
  const shelfRef = useRef<HTMLElement>(null);
  const railRef = useRef<HTMLDivElement>(null);
  const frameRef = useRef(0);
  const variant = shelfVariants[position % shelfVariants.length];

  const syncRailDepth = () => {
    const rail = railRef.current;
    const shelf = shelfRef.current;
    if (!rail || !shelf) return;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const maxScroll = Math.max(1, rail.scrollWidth - rail.clientWidth);
    const progress = Math.min(1, Math.max(0, rail.scrollLeft / maxScroll));
    const amplitude = reducedMotion ? 0 : Number.parseFloat(getComputedStyle(shelf).getPropertyValue('--gm-rail-amplitude')) || 0;
    shelf.style.setProperty('--gm-rail-shift', `${((progress - 0.5) * amplitude).toFixed(2)}px`);
  };

  const requestRailDepth = () => {
    if (frameRef.current) return;
    frameRef.current = window.requestAnimationFrame(() => {
      frameRef.current = 0;
      syncRailDepth();
    });
  };

  useEffect(() => {
    syncRailDepth();
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    reducedMotion.addEventListener('change', syncRailDepth);
    return () => {
      if (frameRef.current) window.cancelAnimationFrame(frameRef.current);
      reducedMotion.removeEventListener('change', syncRailDepth);
    };
  }, []);

  const moveRail = (direction: -1 | 1) => {
    const rail = railRef.current;
    if (!rail) return;
    rail.scrollBy({
      left: direction * Math.max(280, rail.clientWidth * 0.78),
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
    });
  };

  return (
    <section ref={shelfRef} className={`catalogShelf shelf-${variant}`} data-shelf-id={id} aria-labelledby={`${id}-title`}>
      {variant === 'band' && <span className="shelfRearBand" aria-hidden="true" />}
      <div className="shelfHeading">
        <span className="shelfNumber pixelLabel" aria-hidden="true">{String(position + 1).padStart(2, '0')}</span>
        <div className="shelfTitle">
          <h3 id={`${id}-title`}>{title}</h3>
          <p>{description}</p>
        </div>
        <div className="shelfMeta">
          <span className="pixelLabel">{games.length} títulos</span>
          <div className="shelfControls" role="group" aria-label={`Mover carrusel ${title}`}>
            <button type="button" onClick={() => moveRail(-1)} aria-label={`Ver títulos anteriores en ${title}`}><ChevronLeft aria-hidden="true" /></button>
            <button type="button" onClick={() => moveRail(1)} aria-label={`Ver más títulos en ${title}`}><ChevronRight aria-hidden="true" /></button>
          </div>
        </div>
      </div>
      <div
        ref={railRef}
        className="catalogRail"
        tabIndex={0}
        role="region"
        aria-label={`Carrusel ${title}. Usa las flechas izquierda y derecha para desplazarte.`}
        onScroll={requestRailDepth}
        onKeyDown={(event) => {
          if (event.key === 'ArrowLeft') {
            event.preventDefault();
            moveRail(-1);
          }
          if (event.key === 'ArrowRight') {
            event.preventDefault();
            moveRail(1);
          }
        }}
      >
        {games.map((game, index) => <GameCard game={game} index={index} key={game.id} />)}
      </div>
    </section>
  );
}
