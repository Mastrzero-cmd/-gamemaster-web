/* GameMaster · identidad ALTERNA «Cartel» · JS estático, sin dependencias */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) document.documentElement.classList.add('reduce');
  const AZUL = '#1616FF', C = { k0: '#050505', k1: '#0B0B0D' };

  /* ---------- CORTES: cintas azules sólidas (diagonales, bloques, arcos) ---------- */
  const bg = el => el ? getComputedStyle(el).backgroundColor : C.k0;
  const hex = c => { const m = c.match(/\d+/g).map(Number); return '#' + m.slice(0, 3).map(v => v.toString(16).padStart(2, '0')).join(''); };
  const build = el => {
    const W = Math.round(el.clientWidth || innerWidth), H = Math.round(el.clientHeight || 96), T = Math.round(H * .2), kind = el.dataset.cut;
    const prev = el.previousElementSibling, next = el.nextElementSibling;
    const from = prev && prev.classList.contains('sec') ? hex(bg(prev)) : C.k0, to = next && next.classList.contains('sec') ? hex(bg(next)) : C.k1;
    let d = '', n;
    if (kind === 'diag') { const s = Math.max(70, H * 1.4); n = Math.ceil(W / s); d = `M0 ${H}`; for (let i = 0; i < n; i++) d += `L${i * s} ${T}L${(i + 1) * s} ${H}`; d += `L${W + s} ${H}`; }
    if (kind === 'bloques') { const s = Math.max(44, H * .75), steps = 4; n = Math.ceil(W / s); d = `M0 ${H}`; for (let i = 0; i < n; i++) { const lvl = (i % (steps + 1)); const y = H - Math.round((H - T) * lvl / steps); d += `L${i * s} ${y}L${(i + 1) * s} ${y}`; } d += `L${n * s} ${H}`; }
    if (kind === 'arcos') { const r = Math.max(26, H * .42); n = Math.ceil(W / (2 * r)); d = `M0 ${H}`; for (let i = 0; i < n; i++) d += `A${r} ${r} 0 0 1 ${(i + 1) * 2 * r} ${H}`; d = d.replace(/^M0 \d+/, `M0 ${H}`); }
    const fill = `${d}L${W + 200} ${H + 4}L0 ${H + 4}Z`;
    el.classList.add('cut'); el.setAttribute('aria-hidden', 'true'); el.style.background = from;
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none"><rect width="${W}" height="${H}" fill="${from}"/><path d="${fill}" fill="${to}" stroke="${AZUL}" stroke-width="${T}" stroke-linejoin="miter" stroke-miterlimit="8"/></svg>`;
  };
  const cuts = [...document.querySelectorAll('[data-cut]')];
  const buildAll = () => cuts.forEach(build);
  buildAll(); let rz; addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(buildAll, 120); });
  document.fonts && document.fonts.ready.then(buildAll);

  /* ---------- FILAS TIPO NETFLIX ---------- */
  const WA = 'https://wa.me/525527699426';
  const L = f => `assets/logos-mono/${f}_mono_hielo.svg`;
  const juegos = [['Zelda · Breath of the Wild','zelda-botw'],['Mario Kart World','mario-kart-world'],['Hollow Knight','hollow-knight'],['Metroid Dread','metroid-dread'],['Pokémon Escarlata','pokemon-scarlet'],['Super Mario Odyssey','mario-odyssey'],['Hades','hades'],['Cuphead','cuphead'],['Celeste','celeste'],['Kirby y la tierra olvidada','kirby-and-the-forgotten-land'],['Animal Crossing','animal-crossing-new-horizons'],['Mario Wonder','mario-wonder'],['Donkey Kong Bananza','donkey-kong-bananza'],['Zelda · Tears of the Kingdom','zelda-totk']];
  const streaming = [['Netflix',L('netflix'),'Series y películas en pantalla grande.'],['Spotify',L('spotify'),'Tu música y podcasts sin anuncios.'],['HBO Max',L('hbomax'),'Estrenos, series y cine.'],['Disney+',null,'Animación, Marvel y Star Wars.'],['Crunchyroll',L('crunchyroll'),'Anime en simulcast.'],['Prime Video',null,'Series, cine y envíos.'],['Apple TV+',L('appletv'),'Producciones originales.'],['YouTube Music',L('youtubemusic'),'Música y videos oficiales.']];
  const plataformas = [['Nintendo Switch',null,'Juegos, accesorios y cuentas para tu consola.'],['PlayStation',L('playstation'),'Catálogo para PS4 y PS5.'],['Steam',L('steam'),'Juegos para PC con entrega rápida.'],['Xbox Game Pass',null,'Cientos de juegos por suscripción.']];
  const ia = [['ChatGPT',null,'Escribe, resume y resuelve dudas.'],['Claude',L('claude'),'Redacta, analiza documentos y programa.'],['Google Gemini',L('googlegemini'),'Asistente de Google para texto e ideas.'],['Proton VPN',L('protonvpn'),'Navega con más privacidad.']];
  const pad = i => String(i + 1).padStart(2, '0');
  const svc = ([n, img, d], i) => `<article class="card s"><div class="mk">${img ? `<img src="${img}" alt="Logo de ${n}" loading="lazy" draggable="false">` : `<span class="wm">${n}</span>`}</div><div class="in"><span class="n">N.º ${pad(i)}</span><h4>${n}</h4><p>${d}</p><span class="chip">Consultar precio</span><a class="btn red sm" href="${WA}" rel="noopener">Cotizar →</a></div></article>`;
  const builders = {
    juegos: () => juegos.map(([n, f], i) => `<article class="card g"><div class="cv"><img src="assets/portadas/${f}.webp" alt="Portada de ${n}" loading="lazy" draggable="false"></div><div class="in"><span class="n">N.º ${pad(i)}</span><h4>${n}</h4><span class="chip">Consultar precio</span></div></article>`).join(''),
    streaming: () => streaming.map(svc).join(''),
    plataformas: () => plataformas.map(svc).join(''),
    ia: () => ia.map(svc).join('')
  };
  document.querySelectorAll('[data-row]').forEach(row => {
    const id = 'row-' + row.dataset.row, title = row.dataset.title;
    row.classList.add('row');
    row.innerHTML = `<div class="row-head"><h3 id="${id}">${title}</h3><span class="cnt" aria-live="polite"></span><div class="row-ctl"><button type="button" class="prev" aria-label="Anterior: ${title}">←</button><button type="button" class="next" aria-label="Siguiente: ${title}">→</button></div></div><div class="row-wrap"><div class="track" tabindex="0" role="group" aria-labelledby="${id}">${builders[row.dataset.row]()}</div></div>`;
    const tr = row.querySelector('.track'), pv = row.querySelector('.prev'), nx = row.querySelector('.next'), cnt = row.querySelector('.cnt'), cards = [...tr.children];
    const stepPx = () => cards[0].offsetWidth + 16;
    const upd = () => {
      pv.disabled = tr.scrollLeft < 4; nx.disabled = tr.scrollLeft + tr.clientWidth >= tr.scrollWidth - 4;
      const cur = Math.min(cards.length, Math.round(tr.scrollLeft / stepPx()) + 1);
      cnt.textContent = String(cur).padStart(2, '0') + ' / ' + String(cards.length).padStart(2, '0');
    };
    const go = d => tr.scrollBy({ left: d * Math.max(stepPx(), Math.floor(tr.clientWidth * .8 / stepPx()) * stepPx()), behavior: reduced ? 'auto' : 'smooth' });
    pv.addEventListener('click', () => go(-1)); nx.addEventListener('click', () => go(1));
    tr.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); addEventListener('resize', upd); upd();
    tr.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { go(1); e.preventDefault(); } if (e.key === 'ArrowLeft') { go(-1); e.preventDefault(); } });
    // arrastre con mouse (en táctil se usa el scroll nativo)
    let down = false, sx = 0, sl = 0, moved = 0;
    tr.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse' || e.button !== 0) return; down = true; sx = e.clientX; sl = tr.scrollLeft; moved = 0; });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); if (moved > 5) tr.classList.add('drag'); tr.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; if (moved > 5) { tr.classList.remove('drag'); const s = stepPx(); tr.scrollTo({ left: Math.round(tr.scrollLeft / s) * s, behavior: 'smooth' }); } });
  });

  /* ---------- PARALLAX: azul lento, rojo medio, piezas rápidas (con tope) ---------- */
  if (!reduced) {
    const items = [...document.querySelectorAll('.ly[data-speed]')]; let tick = false;
    const lim = el => el.classList.contains('bk') ? 26 : el.classList.contains('fr') ? 52 : 70;
    const run = () => {
      tick = false; const vh = innerHeight, k = innerWidth < 700 ? .5 : 1;
      items.forEach(el => {
        const b = el.parentElement.getBoundingClientRect(); if (b.bottom < -200 || b.top > vh + 200) return;
        const raw = (b.top + b.height / 2 - vh / 2) * -parseFloat(el.dataset.speed) * k, L = lim(el);
        el.style.setProperty('--py', (L * Math.tanh(raw / L)).toFixed(1) + 'px');
      });
    };
    addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(run); } }, { passive: true }); addEventListener('resize', run); run();
  }

  /* ---------- RIEL LATERAL: sección actual y avance ---------- */
  const secs = [...document.querySelectorAll('[data-rail]')], rn = document.getElementById('railn'), rl = document.getElementById('raill'), rb = document.getElementById('railbar');
  const rail = () => {
    let cur = 0; secs.forEach((s, i) => { if (s.getBoundingClientRect().top < innerHeight * .4) cur = i; });
    rn.textContent = String(cur).padStart(2, '0'); rl.textContent = secs[cur].dataset.rail;
    rb.style.setProperty('--p', Math.min(100, 100 * scrollY / (document.documentElement.scrollHeight - innerHeight)).toFixed(1) + '%');
  };
  addEventListener('scroll', () => requestAnimationFrame(rail), { passive: true }); rail();
})();
