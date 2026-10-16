/* GameMaster · v9b «Arcade-técnico» · JS vanilla: filas tipo Netflix, parallax, HUD (puntos y nivel), cuenta atrás */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]reduce/.test(location.search);
  if (reduced) document.documentElement.classList.add('reduce');
  const WA = 'https://wa.me/525527699426';
  const juegos = [['Zelda · Breath of the Wild','zelda-botw'],['Mario Kart World','mario-kart-world'],['Hollow Knight','hollow-knight'],['Metroid Dread','metroid-dread'],['Pokémon Escarlata','pokemon-scarlet'],['Super Mario Odyssey','mario-odyssey'],['Hades','hades'],['Cuphead','cuphead'],['Celeste','celeste'],['Kirby y la tierra olvidada','kirby-and-the-forgotten-land'],['Animal Crossing','animal-crossing-new-horizons'],['Mario Wonder','mario-wonder'],['Donkey Kong Bananza','donkey-kong-bananza'],['Zelda · Tears of the Kingdom','zelda-totk']];
  const streaming = [['Netflix','netflix','Series y películas en pantalla grande.'],['Spotify','spotify','Tu música y podcasts sin anuncios.'],['HBO Max','hbomax','Estrenos, series y cine.'],['Disney+',null,'Animación, Marvel y Star Wars.'],['Crunchyroll','crunchyroll','Anime en simulcast.'],['Prime Video',null,'Series, cine y envíos.'],['Apple TV+','appletv','Producciones originales.'],['YouTube Music','youtubemusic','Música y videos oficiales.']];
  const plataformas = [['Nintendo Switch',null,'Juegos, accesorios y cuentas para tu consola.'],['PlayStation','playstation','Catálogo para PS4 y PS5.'],['Steam','steam','Juegos para PC con entrega rápida.'],['Xbox Game Pass',null,'Cientos de juegos por suscripción.']];
  const ia = [['ChatGPT',null,'Escribe, resume y resuelve dudas.'],['Claude','claude','Redacta, analiza documentos y programa.'],['Proton VPN','protonvpn','Navega con más privacidad.']];
  const pad = n => String(n).padStart(2, '0');
  const logo = (n, k) => k ? `<img src="assets/logos-mono/${k}_mono_hielo.svg" alt="Logo de ${n}" loading="lazy" draggable="false">` : `<span class="wm" aria-label="${n}">${n}</span>`;
  const svc = (n, k, d, i) => `<article class="card-s"><div class="plate"><span class="no">P${i + 1}</span>${logo(n, k)}</div><div class="in"><h4>${n}</h4><p>${d}</p><span class="chip">Consultar precio</span><br><a class="btn red" href="${WA}" rel="noopener">Cotizar ▶</a></div></article>`;
  const builders = {
    juegos: () => juegos.map(([n, f], i) => `<article class="card-g"><div class="cover"><span class="no">${pad(i + 1)}</span><img src="assets/portadas/${f}.webp" alt="Portada de ${n}" loading="lazy" draggable="false"></div><h4>${n}</h4><span class="chip">Consultar precio</span></article>`).join(''),
    streaming: () => streaming.map((a, i) => svc(...a, i)).join(''),
    plataformas: () => plataformas.map((a, i) => svc(...a, i)).join(''),
    ia: () => ia.map((a, i) => svc(...a, i)).join('')
  };
  document.querySelectorAll('[data-row]').forEach(row => {
    const id = 'row-' + Math.random().toString(36).slice(2, 7), title = row.dataset.title, total = builders[row.dataset.row] ? (row.dataset.row === 'juegos' ? juegos : row.dataset.row === 'streaming' ? streaming : row.dataset.row === 'ia' ? ia : plataformas).length : 0;
    row.classList.add('row');
    row.innerHTML = `<div class="row-head"><h3 id="${id}">${title}</h3><span class="cnt" aria-hidden="true">01/${pad(total)}</span><i class="bar"></i><div class="row-ctl"><button type="button" class="prev" aria-label="Anterior: ${title}">◀</button><button type="button" class="next" aria-label="Siguiente: ${title}">▶</button></div></div><div class="track" tabindex="0" role="group" aria-labelledby="${id}">${builders[row.dataset.row]()}</div>`;
    const tr = row.querySelector('.track'), pv = row.querySelector('.prev'), nx = row.querySelector('.next'), cnt = row.querySelector('.cnt'), ctl = row.querySelector('.row-ctl');
    const upd = () => {
      const w = tr.firstElementChild.offsetWidth + 18, cur = Math.min(total, Math.round(tr.scrollLeft / w) + 1);
      cnt.textContent = pad(cur) + '/' + pad(total); ctl.style.visibility = tr.scrollWidth <= tr.clientWidth + 4 ? 'hidden' : 'visible';
      pv.disabled = tr.scrollLeft < 4; nx.disabled = tr.scrollLeft + tr.clientWidth >= tr.scrollWidth - 4;
    };
    const step = d => tr.scrollBy({ left: d * Math.max(240, tr.clientWidth * .82), behavior: reduced ? 'auto' : 'smooth' });
    pv.onclick = () => step(-1); nx.onclick = () => step(1);
    tr.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); addEventListener('resize', upd); upd();
    tr.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { step(1); e.preventDefault(); } if (e.key === 'ArrowLeft') { step(-1); e.preventDefault(); } });
    let down = false, sx = 0, sl = 0, moved = 0;
    tr.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = tr.scrollLeft; moved = 0; });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); if (moved > 5) tr.classList.add('drag'); tr.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; tr.classList.remove('drag'); if (moved > 5) { const w = tr.firstElementChild.offsetWidth + 18; tr.scrollTo({ left: Math.round(tr.scrollLeft / w) * w, behavior: 'smooth' }); } });
  });

  /* PARALLAX: azul (.03) más lento que rojo (.10) y sprites (.22), con tope en px; sin movimiento si se pide reducir */
  const lay = [...document.querySelectorAll('.ly[data-speed]')];
  const lim = el => el.classList.contains('pc') ? 40 : el.classList.contains('fr') ? 30 : 12;
  let tick = false;
  const run = () => {
    tick = false; const vh = innerHeight, k = innerWidth < 700 ? .5 : 1;
    lay.forEach(el => {
      const host = el.parentElement, b = host.getBoundingClientRect(); if (b.bottom < -200 || b.top > vh + 200) return;
      const L = lim(el), raw = (b.top + b.height / 2 - vh / 2) * -parseFloat(el.dataset.speed) * k;
      el.style.setProperty('--py', (L * Math.tanh(raw / L)).toFixed(1) + 'px');
    });
  };
  if (!reduced) { addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(run); } }, { passive: true }); addEventListener('resize', run); run(); }

  /* HUD: puntos según el avance y nivel de la pantalla visible */
  const sc = document.getElementById('score'), nv = document.getElementById('nivel'), secs = [...document.querySelectorAll('.sec[data-nivel]')], links = [...document.querySelectorAll('.nav a')];
  const hud = () => {
    const y = scrollY, max = document.documentElement.scrollHeight - innerHeight || 1;
    sc.textContent = String(Math.round(y / max * 9000) * 10).padStart(6, '0');
    let cur = secs[0]; secs.forEach(s => { if (s.getBoundingClientRect().top < innerHeight * .4) cur = s; });
    nv.textContent = cur.dataset.nivel; links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + cur.id));
  };
  addEventListener('scroll', () => requestAnimationFrame(hud), { passive: true }); hud();

  /* cuenta atrás de «¿Continuar?» */
  const c = document.getElementById('count');
  if (c && !reduced) { let n = 9; setInterval(() => { n = (n + 9) % 10; c.textContent = n; }, 1000); }
})();
