/* Interacción local. Sin dependencias, seguimiento ni peticiones externas. */
(() => {
  'use strict';
  const WA = 'https://wa.me/525527699426';
  document.querySelectorAll('[data-quote]').forEach(link => {
    link.href = WA;
    link.rel = 'noopener';
  });

  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = matchMedia('(max-width: 620px)');
  const forcedReduce = new URLSearchParams(location.search).has('reduce');
  let reduced = forcedReduce || preference.matches;
  const behavior = () => reduced ? 'instant' : 'smooth';
  const planes = [...document.querySelectorAll('[data-plane]')];
  let scheduled = false;

  function updatePlanes() {
    scheduled = false;
    const tokens = getComputedStyle(document.documentElement);
    for (const plane of planes) {
      if (reduced) { plane.style.removeProperty('--shift'); continue; }
      const bounds = plane.parentElement.getBoundingClientRect();
      const distance = innerHeight / 2 - (bounds.top + bounds.height / 2);
      const front = plane.dataset.plane === 'front';
      const limit = parseFloat(tokens.getPropertyValue(front ? '--motion-front' : '--motion-back'));
      const speed = parseFloat(tokens.getPropertyValue(front ? '--speed-front' : '--speed-back'));
      const shift = Math.max(-limit, Math.min(limit, distance * speed));
      plane.style.setProperty('--shift', `${shift.toFixed(2)}px`);
    }
  }
  function schedule() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(updatePlanes); }
  }
  function setMotion() {
    reduced = forcedReduce || preference.matches;
    document.documentElement.classList.toggle('reduced', reduced);
    schedule();
  }
  preference.addEventListener('change', setMotion);
  mobile.addEventListener('change', schedule);
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule, { passive: true });
  setMotion();

  document.querySelectorAll('.rail').forEach(rail => {
    const controls = document.querySelector(`[data-controls="${rail.id}"]`);
    const previous = controls.querySelector('[data-direction="-1"]');
    const next = controls.querySelector('[data-direction="1"]');
    function updateButtons() {
      previous.disabled = rail.scrollLeft <= 2;
      next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 2;
    }
    function move(direction) {
      const card = [...rail.children].find(child => !child.hidden);
      const gap = parseFloat(getComputedStyle(rail).columnGap) || 0;
      const distance = card ? card.getBoundingClientRect().width + gap : rail.clientWidth;
      rail.scrollBy({ left: direction * distance, behavior: behavior() });
    }
    previous.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    rail.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault();
        move(event.key === 'ArrowRight' ? 1 : -1);
      }
    });

    let origin = 0, start = 0, dragging = false, moved = false, pointer;
    rail.addEventListener('pointerdown', event => {
      // El táctil conserva el desplazamiento nativo, incluido el scroll vertical.
      if (event.pointerType !== 'mouse' || event.button !== 0) return;
      origin = event.clientX;
      start = rail.scrollLeft;
      dragging = true;
      moved = false;
      pointer = event.pointerId;
    });
    rail.addEventListener('pointermove', event => {
      if (!dragging) return;
      const delta = event.clientX - origin;
      if (Math.abs(delta) > 6 && !moved) {
        moved = true;
        rail.setPointerCapture(pointer);
        rail.classList.add('is-dragging');
      }
      if (moved) { event.preventDefault(); rail.scrollLeft = start - delta; }
    });
    function finish() {
      dragging = false;
      rail.classList.remove('is-dragging');
      if (pointer !== undefined && rail.hasPointerCapture(pointer)) rail.releasePointerCapture(pointer);
    }
    rail.addEventListener('pointerup', finish);
    rail.addEventListener('pointercancel', finish);
    rail.addEventListener('pointerleave', () => { if (!moved) dragging = false; });
    rail.addEventListener('lostpointercapture', () => { dragging = false; });
    // Los enlaces siguen operativos con un clic; un arrastre nunca abre WhatsApp.
    rail.addEventListener('click', event => {
      if (moved) { event.preventDefault(); event.stopPropagation(); moved = false; }
    }, true);
    rail.addEventListener('dragstart', event => event.preventDefault());
    rail.addEventListener('scroll', updateButtons, { passive: true });
    addEventListener('resize', updateButtons, { passive: true });
    rail.addEventListener('catalogchange', updateButtons);
    updateButtons();
  });

  const search = document.querySelector('#game-search');
  const gameRail = document.querySelector('#rail-juegos');
  const cards = [...gameRail.querySelectorAll('article')];
  const filters = [...document.querySelectorAll('[data-collection]')];
  const empty = document.querySelector('#empty-state');
  const counter = document.querySelector('#result-count');
  let collection = 'todo';
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  function filterGames() {
    const query = normalize(search.value.trim());
    let count = 0;
    for (const card of cards) {
      card.hidden = !normalize(card.dataset.title).includes(query) || (collection !== 'todo' && card.dataset.collection !== collection);
      if (!card.hidden) count++;
    }
    empty.hidden = count !== 0;
    gameRail.hidden = count === 0;
    counter.textContent = `${count} ${count === 1 ? 'juego' : 'juegos'} · Precio y disponibilidad por confirmar`;
    gameRail.scrollLeft = 0;
    gameRail.dispatchEvent(new Event('catalogchange'));
  }
  filters.forEach(button => button.addEventListener('click', () => {
    collection = button.dataset.collection;
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    filterGames();
  }));
  search.addEventListener('input', filterGames);
  document.querySelector('#reset-search').addEventListener('click', () => {
    search.value = '';
    filters[0].click();
    search.focus();
  });
  filterGames();
})();
