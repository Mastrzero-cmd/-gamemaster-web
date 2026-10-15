/* GameMaster · Identidad visual v6 · JS vanilla (cortes, filas, parallax) */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]reduce/.test(location.search);
  if (reduced) document.documentElement.classList.add('reduce');
  const C = { azul: '#2d41dc', prof: '#1e2eb6', noche: '#05071f' };
  const W = 1440, H = 90;
  const hair = (a, b) => (a === 'noche' || b === 'noche') ? 'rgba(234,246,255,.38)' : '#05071f';
  /* 3 cortes limpios y precisos: diagonal fina, escalón, línea con muescas */
  const cuts = {
    diag: (to, hl) => `<path d="M0 ${H}L${W} 26V${H}Z" fill="${to}"/><path d="M0 ${H}L${W} 26" stroke="${hl}" stroke-width="3" fill="none"/>`,
    step: (to, hl) => `<path d="M0 66H520V46H980V26H${W}V${H}H0Z" fill="${to}"/><path d="M0 66H520V46H980V26H${W}" stroke="${hl}" stroke-width="3" fill="none"/>`,
    notch: (to, hl) => { let d = `M0 46`; for (let x = 0; x < W; x += 120) d += `H${x + 48}L${x + 60} 60L${x + 72} 46`; d += `H${W}`; return `<path d="${d}V${H}H0Z" fill="${to}"/><path d="${d}" stroke="${hl}" stroke-width="3" fill="none"/><path d="M0 36H${W}" stroke="${hl}" stroke-width="1.5" fill="none" opacity=".6"/>`; }
  };
  document.querySelectorAll('[data-cut]').forEach(el => {
    const t = el.dataset.cut, from = el.dataset.from || 'azul', to = el.dataset.to || 'noche';
    el.classList.add('cut'); el.style.background = C[from]; el.setAttribute('aria-hidden', 'true');
    el.insertAdjacentHTML('afterbegin', `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">${cuts[t](C[to], hair(from, to))}</svg>`);
  });

  /* ---------- FILAS TIPO NETFLIX ---------- */
  const WA = 'https://wa.me/525527699426';
  const juegos = [['Zelda · Breath of the Wild','zelda-botw'],['Mario Kart World','mario-kart-world'],['Hollow Knight','hollow-knight'],['Metroid Dread','metroid-dread'],['Pokémon Escarlata','pokemon-scarlet'],['Super Mario Odyssey','mario-odyssey'],['Hades','hades'],['Cuphead','cuphead'],['Celeste','celeste'],['Kirby y la tierra olvidada','kirby-and-the-forgotten-land'],['Animal Crossing','animal-crossing-new-horizons'],['Mario Wonder','mario-wonder'],['Donkey Kong Bananza','donkey-kong-bananza'],['Zelda · Tears of the Kingdom','zelda-totk']];
  const streaming = [['Netflix','netflix','Series y películas en pantalla grande.'],['Spotify','spotify','Tu música y podcasts sin anuncios.'],['HBO Max','hbo-max','Estrenos, series y cine.'],['Disney+','disney-plus','Animación, Marvel y Star Wars.'],['Crunchyroll','crunchyroll','Anime en simulcast.'],['Prime Video','amazon-prime','Series, cine y envíos.'],['Apple TV+','apple-tv-plus','Producciones originales.'],['YouTube Music','youtube-music','Música y videos oficiales.']];
  const plataformas = [['Nintendo Switch','assets/logos/nintendo-switch.png','dk','Juegos, accesorios y cuentas para tu consola.'],['PlayStation','assets/logos/playstation.png','dk','Catálogo para PS4 y PS5.'],['Steam','assets/logos/steam.png','dk','Juegos para PC con entrega rápida.'],['Xbox Game Pass','assets/servicios/xbox-game-pass.svg','','Cientos de juegos por suscripción.']];
  const ia = [['ChatGPT','chatgpt','Escribe, resume y resuelve dudas.'],['Claude','claude','Redacta, analiza documentos y programa.'],['Proton VPN','proton-vpn','Navega con más privacidad.']];
  const svc = (n, img, desc, cls = '') => `<article class="card-s"><div class="plate ${cls}"><img src="${img}" alt="Logo de ${n}" loading="lazy" draggable="false"></div><div class="in"><h4>${n}</h4><p>${desc}</p><span class="chip">Consultar precio</span> <a class="btn" href="${WA}" rel="noopener" style="margin-top:10px">Cotizar →</a></div></article>`;
  const builders = {
    juegos: () => juegos.map(([n, f]) => `<article class="card-g"><div class="cover"><img src="assets/portadas/${f}.webp" alt="Portada de ${n}" loading="lazy" draggable="false"></div><h4>${n}</h4><span class="chip">Consultar precio</span></article>`).join(''),
    streaming: () => streaming.map(([n, f, d]) => svc(n, `assets/servicios/${f}.svg`, d)).join(''),
    plataformas: () => plataformas.map(([n, src, c, d]) => svc(n, src, d, c)).join(''),
    ia: () => ia.map(([n, f, d]) => svc(n, `assets/servicios/${f}.svg`, d)).join('')
  };
  document.querySelectorAll('[data-row]').forEach(row => {
    const id = 'row-' + Math.random().toString(36).slice(2, 7), title = row.dataset.title;
    row.classList.add('row');
    row.innerHTML = `<div class="row-head"><h3 id="${id}">${title}</h3><div class="row-ctl"><button type="button" class="prev" aria-label="Anterior: ${title}">←</button><button type="button" class="next" aria-label="Siguiente: ${title}">→</button></div></div><div class="row-wrap"><div class="track" tabindex="0" role="group" aria-labelledby="${id}">${builders[row.dataset.row]()}</div></div>`;
    const tr = row.querySelector('.track'), pv = row.querySelector('.prev'), nx = row.querySelector('.next');
    const ctl = row.querySelector('.row-ctl'); const upd = () => { ctl.style.visibility = tr.scrollWidth <= tr.clientWidth + 4 ? 'hidden' : 'visible'; pv.disabled = tr.scrollLeft < 4; nx.disabled = tr.scrollLeft + tr.clientWidth >= tr.scrollWidth - 4; };
    const step = d => tr.scrollBy({ left: d * Math.max(240, tr.clientWidth * .82), behavior: reduced ? 'auto' : 'smooth' });
    pv.onclick = () => step(-1); nx.onclick = () => step(1);
    tr.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); addEventListener('resize', upd); upd();
    tr.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { step(1); e.preventDefault(); } if (e.key === 'ArrowLeft') { step(-1); e.preventDefault(); } });
    // arrastre con mouse (táctil usa el scroll nativo)
    let down = false, sx = 0, sl = 0, moved = 0;
    tr.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = tr.scrollLeft; moved = 0; });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); if (moved > 5) tr.classList.add('drag'); tr.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; tr.classList.remove('drag'); if (moved > 5) { const near = Math.round(tr.scrollLeft / (tr.firstElementChild.offsetWidth + 18)) * (tr.firstElementChild.offsetWidth + 18); tr.scrollTo({ left: near, behavior: 'smooth' }); } });
  });

  /* ---------- PARALLAX: fondo fijo, piezas al frente se mueven (suave, con tope) ---------- */
  if (!reduced) {
    const items = [...document.querySelectorAll('.pz[data-speed],.ly[data-speed]')]; let tick = false;
    const lim = el => el.classList.contains('ly') ? 70 : (el.classList.contains('hero') ? 44 : 60);
    const run = () => {
      tick = false; const vh = innerHeight, k = innerWidth < 700 ? .5 : 1;
      items.forEach(el => {
        const host = el.closest('section,.cut') || el.parentElement, b = host.getBoundingClientRect();
        if (b.bottom < -200 || b.top > vh + 200) return;
        const raw = (b.top + b.height / 2 - vh / 2) * -parseFloat(el.dataset.speed) * k, L = lim(el);
        el.style.setProperty('--py', (L * Math.tanh(raw / L)).toFixed(1) + 'px');
      });
    };
    addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(run); } }, { passive: true }); addEventListener('resize', run); run();
  }
})();
