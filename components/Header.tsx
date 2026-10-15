'use client';

import { useEffect, useRef, useState } from 'react';
import { ArrowUpRight, Menu, X } from 'lucide-react';
import { BrandMark } from './BrandMark';
import { useExperience } from './experience/useExperience';

const navigation = [
  ['Catálogo', '#catalogo'],
  ['Streaming', '#streaming'],
  ['IA', '#ia'],
  ['Privacidad', '#privacidad'],
  ['Cómo funciona', '#modalidades'],
  ['FAQ', '#preguntas'],
];

export function Header({ homePath = '' }: { homePath?: string }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const menuButtonRef = useRef<HTMLButtonElement>(null);
  const navRef = useRef<HTMLElement>(null);
  const { selectedCount } = useExperience();

  useEffect(() => {
    const sync = () => setScrolled(window.scrollY > 24);
    sync();
    window.addEventListener('scroll', sync, { passive: true });
    return () => window.removeEventListener('scroll', sync);
  }, []);

  useEffect(() => {
    if (!menuOpen) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setMenuOpen(false);
        menuButtonRef.current?.focus();
      }
    };
    window.addEventListener('keydown', closeOnEscape);
    window.requestAnimationFrame(() => navRef.current?.querySelector<HTMLAnchorElement>('a')?.focus());
    return () => window.removeEventListener('keydown', closeOnEscape);
  }, [menuOpen]);

  const resolveHref = (hash: string) => `${homePath}${hash}`;

  return (
    <header className={`siteHeader ${scrolled || menuOpen ? 'isSolid' : ''}`}>
      <a className="brandLink" href={resolveHref('#inicio')} aria-label="GameMaster, ir al inicio">
        <BrandMark />
      </a>
      <nav ref={navRef} id="primary-navigation" className={menuOpen ? 'isOpen' : ''} aria-label="Navegación principal">
        {navigation.map(([label, href], index) => (
          <a href={resolveHref(href)} onClick={() => setMenuOpen(false)} key={href}>
            <small aria-hidden="true">{String(index + 1).padStart(2, '0')}</small>{label}
          </a>
        ))}
        <a className="navContact" href={resolveHref('#cotizar')} onClick={() => setMenuOpen(false)}>
          <small aria-hidden="true">07</small>Contacto
        </a>
      </nav>
      <a className="headerCta" href={resolveHref('#cotizar')}>
        <span>{selectedCount ? `Cotización · ${selectedCount}` : 'Cotizar'}</span> <ArrowUpRight aria-hidden="true" />
      </a>
      <button
        ref={menuButtonRef}
        className="menuButton"
        aria-label={menuOpen ? 'Cerrar menú' : 'Abrir menú'}
        aria-expanded={menuOpen}
        aria-controls="primary-navigation"
        onClick={() => setMenuOpen((current) => !current)}
      >
        {menuOpen ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
      </button>
    </header>
  );
}
