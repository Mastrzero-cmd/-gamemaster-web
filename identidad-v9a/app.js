/* GameMaster · v9a «Grabado» · JS estático, sin dependencias */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) document.documentElement.classList.add('reduce');
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
    streaming: () => streaming.map(svc).join(''), plataformas: () => plataformas.map(svc).join(''), ia: () => ia.map(svc).join('')
  };
  document.querySelectorAll('[data-row]').forEach(row => {
    const id = 'row-' + row.dataset.row, title = row.dataset.title;
    row.classList.add('row');
    row.innerHTML = `<div class="row-head"><h3 id="${id}">${title}</h3><span class="cnt" aria-live="polite"></span><div class="row-ctl"><button type="button" class="prev" aria-label="Anterior: ${title}">←</button><button type="button" class="next" aria-label="Siguiente: ${title}">→</button></div></div><div class="row-wrap"><div class="track" tabindex="0" role="group" aria-labelledby="${id}">${builders[row.dataset.row]()}</div></div>`;
    const tr = row.querySelector('.track'), pv = row.querySelector('.prev'), nx = row.querySelector('.next'), cnt = row.querySelector('.cnt'), cards = [...tr.children];
    const stepPx = () => cards[0].offsetWidth + 18;
    const upd = () => {
      pv.disabled = tr.scrollLeft < 4; nx.disabled = tr.scrollLeft + tr.clientWidth >= tr.scrollWidth - 4;
      const cur = Math.min(cards.length, Math.round(tr.scrollLeft / stepPx()) + 1);
      cnt.textContent = String(cur).padStart(2, '0') + ' / ' + String(cards.length).padStart(2, '0');
    };
    const go = d => tr.scrollBy({ left: d * Math.max(stepPx(), Math.floor(tr.clientWidth * .8 / stepPx()) * stepPx()), behavior: reduced ? 'auto' : 'smooth' });
    pv.addEventListener('click', () => go(-1)); nx.addEventListener('click', () => go(1));
    tr.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); addEventListener('resize', upd); upd();
    tr.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { go(1); e.preventDefault(); } if (e.key === 'ArrowLeft') { go(-1); e.preventDefault(); } });
    let down = false, sx = 0, sl = 0, moved = 0;
    tr.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse' || e.button !== 0) return; down = true; sx = e.clientX; sl = tr.scrollLeft; moved = 0; });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); if (moved > 5) tr.classList.add('drag'); tr.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; if (moved > 5) { tr.classList.remove('drag'); const s = stepPx(); tr.scrollTo({ left: Math.round(tr.scrollLeft / s) * s, behavior: 'smooth' }); } });
  });
  /* PARALLAX: azul lento (.03), rojo medio (.10), piezas rápidas (.22), con tope en píxeles */
  if (!reduced) {
    const items = [...document.querySelectorAll('.ly[data-speed]')]; let tick = false;
    const lim = el => el.classList.contains('bk') ? 26 : el.classList.contains('fr') ? 52 : 70;
    const run = () => {
      tick = false; const vh = innerHeight, k = innerWidth < 700 ? .5 : 1;
      items.forEach(el => {
        const b = el.parentElement.getBoundingClientRect(); if (b.bottom < -200 || b.top > vh + 200) return;
        const raw = (b.top + b.height / 2 - vh / 2) * -parseFloat(el.dataset.speed) * k, M = lim(el);
        el.style.setProperty('--py', (M * Math.tanh(raw / M)).toFixed(1) + 'px');
      });
    };
    addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(run); } }, { passive: true }); addEventListener('resize', run); run();
  }
})();
