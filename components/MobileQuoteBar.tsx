'use client';

import { MessageCircle } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useExperience } from './experience/useExperience';

export function MobileQuoteBar() {
  const { selectedCount, whatsappUrl } = useExperience();
  const [pastHero, setPastHero] = useState(false);

  useEffect(() => {
    const update = () => setPastHero(window.scrollY > window.innerHeight * 0.9);
    update();
    window.addEventListener('scroll', update, { passive: true });
    return () => window.removeEventListener('scroll', update);
  }, []);

  const visible = pastHero || selectedCount > 0;

  return (
    <a
      className={`mobileQuoteBar${visible ? ' isVisible' : ''}`}
      href={whatsappUrl}
      target="_blank"
      rel="noreferrer"
      aria-hidden={visible ? undefined : true}
      tabIndex={visible ? undefined : -1}
      aria-label={`Cotizar por WhatsApp${selectedCount ? ` con ${selectedCount} juegos seleccionados` : ''}`}
    >
      <MessageCircle aria-hidden="true" /><span>Cotizar{selectedCount ? ` · ${selectedCount}` : ''}</span>
    </a>
  );
}
