'use client';

import { MessageCircle } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { useExperience } from './experience/useExperience';

// Extra room above the bar so it hides before a card edge reaches it.
const AVOID_MARGIN = 24;

export function MobileQuoteBar() {
  const { selectedCount, whatsappUrl } = useExperience();
  const barRef = useRef<HTMLAnchorElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    let frame = 0;
    const update = () => {
      frame = 0;
      const bar = barRef.current;
      if (!bar) return;
      const barTop = bar.getBoundingClientRect().top - AVOID_MARGIN;
      const zones = document.querySelectorAll<HTMLElement>('[data-quote-bar-avoid]');
      const blocked = Array.from(zones).some((zone) => {
        const rect = zone.getBoundingClientRect();
        return rect.bottom > barTop && rect.top < window.innerHeight;
      });
      setVisible(!blocked);
    };
    const schedule = () => {
      if (!frame) frame = window.requestAnimationFrame(update);
    };
    update();
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    return () => {
      window.removeEventListener('scroll', schedule);
      window.removeEventListener('resize', schedule);
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, []);

  return (
    <a
      ref={barRef}
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
