/* Órbita v10e: interfaz estable, fondo y tres velocidades de frente. */
(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const forcedReduce = new URLSearchParams(location.search).has('reduce');
  // Puntero "no táctil": también cuenta cuando el navegador no declara tipo de puntero.
  const coarsePointer = window.matchMedia('(pointer: coarse)');
  const finePointer = { get matches() { return !coarsePointer.matches; }, addEventListener: (type, fn) => coarsePointer.addEventListener(type, fn) };
  const phone = window.matchMedia('(max-width: 700px)');
  // Velocidad relativa al scroll, amplitud del puntero y límite total en px.
  const motion = {
    rear: { speed: 0.015, pointer: 2, limit: 18 },
    'front-1': { speed: 0.10, pointer: 24, limit: 80 },
    'front-2': { speed: 0.18, pointer: 42, limit: 130 },
    'front-3': { speed: 0.28, pointer: 64, limit: 184 },
  };
  const scenes = [...document.querySelectorAll('[data-scene]')].map((node) => ({
    node,
    planes: [...node.querySelectorAll('[data-plane]')].map((node) => ({
      node, config: motion[node.dataset.plane], x: 0, y: 0,
    })),
  }));
  const pointer = { x: 0, y: 0 };
  const clamp = (value, limit) => Math.max(-limit, Math.min(limit, value));
  const lerp = (current, target, amount) => current + (target - current) * amount;
  const isReduced = () => forcedReduce || reduced.matches;
  let frame = 0;
  let previousTime = 0;

  function stopMotion() {
    cancelAnimationFrame(frame);
    frame = previousTime = 0;
    scenes.forEach(({ planes }) => planes.forEach((plane) => {
      plane.x = plane.y = 0;
      plane.node.style.removeProperty('transform');
    }));
  }

  function paintPlanes(time) {
    frame = 0;
    if (isReduced()) return;
    // Lerp ajustado al tiempo: misma suavidad en pantallas de 60 y 120 Hz.
    const elapsed = previousTime ? Math.min(time - previousTime, 64) : 1000 / 60;
    const amount = 1 - Math.pow(0.88, elapsed / (1000 / 60));
    previousTime = time;
    const scale = phone.matches ? 0.5 : 1;
    const usePointer = finePointer.matches;
    let moving = false;
    for (const { node, planes } of scenes) {
      const rect = node.getBoundingClientRect();
      const distance = innerHeight * 0.5 - rect.top - rect.height * 0.5;
      for (const plane of planes) {
        const { speed, pointer: strength, limit } = plane.config;
        const targetX = clamp(usePointer ? pointer.x * strength * scale : 0, limit * scale);
        const targetY = clamp((distance * speed + (usePointer ? pointer.y * strength : 0)) * scale, limit * scale);
        plane.x = lerp(plane.x, targetX, amount);
        plane.y = lerp(plane.y, targetY, amount);
        if (Math.abs(targetX - plane.x) > 0.02 || Math.abs(targetY - plane.y) > 0.02) {
          moving = true;
        } else {
          plane.x = targetX;
          plane.y = targetY;
        }
        plane.node.style.transform = `translate3d(${plane.x.toFixed(2)}px, ${plane.y.toFixed(2)}px, 0)`;
      }
    }
    if (moving) frame = requestAnimationFrame(paintPlanes);
    else previousTime = 0;
  }

  function requestPaint() {
    if (!frame && !isReduced()) frame = requestAnimationFrame(paintPlanes);
  }
  function syncMotion() {
    document.documentElement.classList.toggle('reduce-motion', isReduced());
    if (isReduced()) stopMotion();
    else requestPaint();
  }
  window.addEventListener('scroll', requestPaint, { passive: true });
  window.addEventListener('resize', requestPaint, { passive: true });
  window.addEventListener('pointermove', (event) => {
    if (isReduced() || !finePointer.matches) return;
    pointer.x = clamp(event.clientX / innerWidth * 2 - 1, 1);
    pointer.y = clamp(event.clientY / innerHeight * 2 - 1, 1);
    requestPaint();
  }, { passive: true });
  function resetPointer() {
    pointer.x = pointer.y = 0;
    requestPaint();
  }
  document.documentElement.addEventListener('pointerleave', resetPointer);
  window.addEventListener('blur', resetPointer);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopMotion();
      pointer.x = pointer.y = 0;
    } else requestPaint();
  });
  reduced.addEventListener('change', syncMotion);
  finePointer.addEventListener('change', resetPointer);
  phone.addEventListener('change', requestPaint);
  syncMotion();

  const rails = [...document.querySelectorAll('.rail')];
  function updateRail(rail) {
    const controls = document.querySelector(`[data-controls="${rail.id}"]`);
    if (!controls) return;
    const max = rail.scrollWidth - rail.clientWidth;
    controls.querySelector('[data-step="-1"]').disabled = rail.scrollLeft < 3 || max < 3;
    controls.querySelector('[data-step="1"]').disabled = rail.scrollLeft >= max - 3 || max < 3;
  }
  function moveRail(rail, step) {
    rail.scrollBy({ left: rail.clientWidth * 0.8 * step, behavior: isReduced() ? 'instant' : 'smooth' });
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
