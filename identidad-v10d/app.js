/* GameMaster · v9d «Póster psicodélico» · JS estático, sin dependencias */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
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
    const stepPx = () => cards[0].offsetWidth + 22;
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

  /* PARALLAX CINEMÁTICO v10d · capas por velocidad (desplazamiento propio extra, en la dirección del scroll: lo cercano avanza más rápido que la página):
     azul de fondo .02 (casi fijo) · plano negro medio .08 · rojo grande al frente .30 · piezas rojas pequeñas .55.
     Cada capa va con translate3d, suavizada con rAF (lerp) y con tope en píxeles (tanh): sin saltos ni desbordes. Con «reducir movimiento» no se anima nada. */
  if (!reduced) {
    const items = [...document.querySelectorAll('.ly[data-speed]')].map(el => ({ el, sp: parseFloat(el.dataset.speed), box: el.parentElement, cur: 0, tgt: 0,
      lim: el.classList.contains('bk') ? 10 : el.classList.contains('md') ? 34 : el.classList.contains('fr') ? 150 : 230 }));
    let raf = 0, last = 0;
    const target = () => {
      const vh = innerHeight, k = innerWidth < 700 ? .55 : 1;
      items.forEach(o => {
        const b = o.box.getBoundingClientRect();
        if (b.bottom < -300 || b.top > vh + 300) { o.vis = false; return; }
        o.vis = true; const raw = (b.top + b.height / 2 - vh / 2) * o.sp * k; o.tgt = o.lim * Math.tanh(raw / o.lim);
      });
    };
    const tick = t => {
      raf = 0; let moving = false;
      items.forEach(o => {
        if (!o.vis && Math.abs(o.cur - o.tgt) < .05) return;
        const d = o.tgt - o.cur; o.cur += Math.abs(d) < .05 ? d : d * .14; if (Math.abs(d) >= .05) moving = true;
        o.el.style.setProperty('--py', o.cur.toFixed(2) + 'px');
      });
      if (moving) raf = requestAnimationFrame(tick);
    };
    const kick = () => { target(); if (!raf) raf = requestAnimationFrame(tick); };
    addEventListener('scroll', kick, { passive: true }); addEventListener('resize', kick);
    target(); items.forEach(o => { o.cur = o.tgt; o.el.style.setProperty('--py', o.cur.toFixed(2) + 'px'); });
    window.__gmParallax = items;
  }
})();
