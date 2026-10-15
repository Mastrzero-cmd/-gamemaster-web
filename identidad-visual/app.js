/* GameMaster · Identidad visual v2 · JS vanilla (cortes, filas, parallax) */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]reduce/.test(location.search);
  if (reduced) document.documentElement.classList.add('reduce');
  const C = { azul: '#2d41dc', prof: '#1e2eb6', noche: '#05071f', azul2: '#4a62ff' };
  const K = '#05071f', RED = '#ff3322', ICE = '#eaf6ff', CY = '#3fdcff', MG = '#ff3b7f';
  let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const W = 1440, H = 170;
  const R = (x, y, w, h, f, ex = '') => `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" fill="${f}" ${ex}/>`;

  /* ---------- CORTES: cada uno con arte distinto ---------- */
  const cuts = {
    // pincelada curva con extremo seco + trazo rojo adelante (como la pincelada del logo)
    pincel: to => {
      let s = `<path d="M0 118C220 62 430 150 710 96S1190 44 1440 104V${H}H0Z" fill="${to}"/>`;
      for (let i = 0; i < 9; i++) { const y = 70 + i * 6 + rnd() * 3, l = 60 + rnd() * 260; s += R(0, y, l, 2 + rnd() * 3, to); }
      s += `<path d="M0 118C220 62 430 150 710 96S1190 44 1440 104" fill="none" stroke="${K}" stroke-width="4"/>`;
      s += `<path d="M-10 92C260 24 560 118 880 56S1300 20 1450 40L1450 62C1300 44 1000 100 880 86C560 148 260 56 -10 112Z" fill="${RED}" stroke="${K}" stroke-width="3"/>`;
      s += `<path d="M-10 124C260 70 560 160 880 100S1300 64 1450 82" fill="none" stroke="${CY}" stroke-width="3" opacity=".8"/>`;
      return s;
    },
    // scanlines que engruesan (TV / señal)
    scan: to => {
      let s = '';
      for (let i = 0; i < 12; i++) s += R(0, 10 + i * 13.4, W, 1.5 + i * 1.15, to);
      s += R(0, 164, W, 6, to);
      for (let i = 0; i < 7; i++) { const y = 18 + rnd() * 120; s += R(rnd() * (W - 300), y, 80 + rnd() * 220, 4, i % 2 ? RED : ICE); }
      return s;
    },
    // glitch horizontal controlado (rebanadas desplazadas, estático)
    glitch: to => {
      let s = R(0, 112, W, 60, to);
      for (let i = 0; i < 8; i++) { const y = 76 + i * 5, off = (rnd() - .5) * 260; s += R(off + 100, y, 320 + rnd() * 600, 5, to); }
      s += R(0, 106, W, 5, K);
      [[120, 40, 230, RED], [520, 56, 340, ICE], [980, 36, 280, RED], [300, 82, 150, CY], [1180, 70, 180, ICE], [760, 94, 200, RED]].forEach(([x, y, w, c]) => { s += R(x, y, w, 5, c); });
      s += R(40, 118, 180, 5, MG) + R(1060, 124, 220, 5, CY);
      return s;
    },
    // escalera pixel (la única pieza pixel) con bloques rojos al frente
    pixel: to => {
      const u = 30; let y = 5, s = '', ys = [];
      for (let x = 0; x < W + u; x += u) { y = Math.max(2, Math.min(7, y + [-1, 0, 1][Math.floor(rnd() * 3)])); ys.push(y); s += R(x, 40 + y * 12 - 4, u + .5, 5, K) + R(x, 40 + y * 12, u + .5, H, to); }
      ys.forEach((v, i) => { if (i % 6 === 2) s += R(i * u + 3, 40 + v * 12 - u + 3, u - 6, u - 6, RED, `stroke="${K}" stroke-width="3"`); });
      s += R(0, 40 + ys[0] * 12 - 3, W, 0, K);
      return s;
    },
    // cinta de película en diagonal
    cinta: to => {
      let s = R(0, 122, W, 60, to) + `<g transform="rotate(-2.2 720 80)">${R(-60, 40, W + 120, 92, K)}`;
      for (let x = -40; x < W + 60; x += 34) s += R(x, 48, 16, 11, ICE, 'rx="2"') + R(x, 113, 16, 11, ICE, 'rx="2"');
      for (let x = -30, i = 0; x < W + 60; x += 118, i++) {
        const c = i % 3 === 1 ? RED : i % 3 === 2 ? C.azul2 : '#1a2a9a';
        s += R(x, 66, 96, 42, c) + `<path d="M${x + 40} ${76}l20 11l-20 11z" fill="${K}" opacity=".8"/>`;
      }
      return s + '</g>';
    }
  };
  document.querySelectorAll('[data-cut]').forEach(el => {
    const t = el.dataset.cut, from = el.dataset.from || 'azul', to = el.dataset.to || 'noche';
    el.classList.add('cut'); el.style.background = C[from]; el.setAttribute('aria-hidden', 'true');
    el.insertAdjacentHTML('afterbegin', `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">${cuts[t](C[to])}</svg>`);
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

  /* ---------- PARALLAX: fondo fijo, piezas al frente se mueven ---------- */
  if (!reduced) {
    const items = [...document.querySelectorAll('.pz[data-speed]')]; let tick = false;
    const run = () => {
      tick = false; const vh = innerHeight;
      items.forEach(el => {
        const host = el.closest('section,.cut,.planes') || el.parentElement, b = host.getBoundingClientRect();
        if (b.bottom < -200 || b.top > vh + 200) return;
        el.style.setProperty('--py', ((b.top + b.height / 2 - vh / 2) * -parseFloat(el.dataset.speed)).toFixed(1) + 'px');
      });
    };
    addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(run); } }, { passive: true }); addEventListener('resize', run); run();
  }
})();
