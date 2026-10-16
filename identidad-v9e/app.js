/* Órbita: interfaz estable, arte en dos planos independientes. */
(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(pointer: fine)');
  const phone = window.matchMedia('(max-width: 700px)');
  const scenes = [...document.querySelectorAll('[data-scene]')].map((node) => ({
    node,
    planes: [...node.querySelectorAll('[data-plane]')],
  }));
  const pointer = { x: 0, y: 0 };
  let frame = 0;

  function paintPlanes() {
    frame = 0;
    for (const { node, planes } of scenes) {
      if (reduced.matches) {
        planes.forEach((plane) => plane.style.removeProperty('transform'));
        continue;
      }
      const rect = node.getBoundingClientRect();
      if (rect.bottom < -200 || rect.top > innerHeight + 200) continue;
      const distance = Math.max(-600, Math.min(600, innerHeight * 0.5 - rect.top - rect.height * 0.5));
      for (const plane of planes) {
        const front = plane.dataset.plane === 'front';
        const speed = front ? 0.105 : 0.028;
        const strength = front ? 15 : 4;
        const scale = phone.matches ? 0.52 : 1;
        const x = pointer.x * strength * scale;
        const y = (distance * speed + pointer.y * strength) * scale;
        plane.style.transform = `translate3d(${x.toFixed(2)}px, ${y.toFixed(2)}px, 0)`;
      }
    }
  }

  function requestPaint() {
    if (!frame) frame = requestAnimationFrame(paintPlanes);
  }
  window.addEventListener('scroll', requestPaint, { passive: true });
  window.addEventListener('resize', requestPaint, { passive: true });
  window.addEventListener('pointermove', (event) => {
    if (reduced.matches || !finePointer.matches) return;
    pointer.x = event.clientX / innerWidth * 2 - 1;
    pointer.y = event.clientY / innerHeight * 2 - 1;
    requestPaint();
  }, { passive: true });
  document.documentElement.addEventListener('pointerleave', () => {
    pointer.x = pointer.y = 0;
    requestPaint();
  });
  reduced.addEventListener('change', requestPaint);
  requestPaint();

  const rails = [...document.querySelectorAll('.rail')];
  function updateRail(rail) {
    const controls = document.querySelector(`[data-controls="${rail.id}"]`);
    if (!controls) return;
    const max = rail.scrollWidth - rail.clientWidth;
    controls.querySelector('[data-step="-1"]').disabled = rail.scrollLeft < 3 || max < 3;
    controls.querySelector('[data-step="1"]').disabled = rail.scrollLeft >= max - 3 || max < 3;
  }
  function moveRail(rail, step) {
    rail.scrollBy({ left: rail.clientWidth * 0.8 * step, behavior: reduced.matches ? 'instant' : 'smooth' });
  }
  document.querySelectorAll('[data-controls] button').forEach((button) => {
    button.addEventListener('click', () => {
      moveRail(document.getElementById(button.parentElement.dataset.controls), Number(button.dataset.step));
    });
  });
  rails.forEach((rail) => {
    rail.addEventListener('scroll', () => updateRail(rail), { passive: true });
    rail.addEventListener('keydown', (event) => {
      if (event.target !== rail) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        moveRail(rail, event.key === 'ArrowLeft' ? -1 : 1);
      }
      if (event.key === 'Home' || event.key === 'End') {
        event.preventDefault();
        rail.scrollTo({ left: event.key === 'Home' ? 0 : rail.scrollWidth, behavior: 'instant' });
      }
    });
  });
  const railObserver = new ResizeObserver(() => rails.forEach(updateRail));
  rails.forEach((rail) => railObserver.observe(rail));

  const search = document.getElementById('game-search');
  const gamesRail = document.getElementById('games-rail');
  const games = [...gamesRail.querySelectorAll('.game')];
  const collectionButtons = [...document.querySelectorAll('[data-collection]')];
  const empty = document.querySelector('.empty-state');
  let collection = 'all';
  const normalize = (value) => value.toLocaleLowerCase('es-MX').normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  function applySearch() {
    const term = normalize(search.value.trim());
    let total = 0;
    games.forEach((game) => {
      const matches = normalize(game.dataset.title).includes(term)
        && (collection === 'all' || game.dataset.collections.split(' ').includes(collection));
      game.hidden = !matches;
      if (matches) total += 1;
    });
    gamesRail.hidden = total === 0;
    empty.hidden = total > 0;
    document.getElementById('results').textContent = `${total} ${total === 1 ? 'juego encontrado' : 'juegos encontrados'}.`;
    gamesRail.scrollLeft = 0;
    updateRail(gamesRail);
  }
  search.addEventListener('input', applySearch);
  search.closest('form').addEventListener('submit', (event) => event.preventDefault());
  collectionButtons.forEach((button) => {
    button.addEventListener('click', () => {
      collection = button.dataset.collection;
      collectionButtons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
      applySearch();
    });
  });
  document.getElementById('reset-search').addEventListener('click', () => {
    search.value = '';
    collection = 'all';
    collectionButtons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.collection === 'all')));
    applySearch();
    search.focus({ preventScroll: true });
  });
  rails.forEach(updateRail);
})();
