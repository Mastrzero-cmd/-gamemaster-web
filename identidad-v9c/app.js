/* GameMaster · v9c «Mapa / Expedición» · JS estático, sin dependencias */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) document.documentElement.classList.add('reduce');
  const COL = { b: '#1616FF', k: '#050505' }, ICE = '#F4F4EF', AZUL = '#1616FF', NEG = '#050505';
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const ns = 'http://www.w3.org/2000/svg';

  /* ---------- LEYENDA (17 marcas) ---------- */
  const marcas = [['netflix','Netflix'],['hbomax','HBO Max'],['max','Max'],['spotify','Spotify'],['youtube','YouTube'],['youtubemusic','YouTube Music'],['crunchyroll','Crunchyroll'],['appletv','Apple TV'],['playstation','PlayStation'],['steam','Steam'],['claude','Claude'],['anthropic','Anthropic'],['googlegemini','Google Gemini'],['proton','Proton'],['protonvpn','Proton VPN'],['twitch','Twitch'],['discord','Discord']];
  const pad = i => String(i + 1).padStart(2, '0');
  $('#legend').innerHTML = marcas.map(([f, n], i) => `<li><img src="assets/logos-mono/${f}_mono_hielo.svg" alt="" width="34" height="34" loading="lazy" draggable="false"><span>${n}</span><small>${pad(i)}</small></li>`).join('');

  /* ---------- CORTES: bordes de mapa (acordeón, esquina doblada, costa, meridianos) ---------- */
  const bgOf = (el, dir) => { const s = dir < 0 ? el.previousElementSibling : el.nextElementSibling; return s && s.dataset.bg ? COL[s.dataset.bg] : NEG; };
  const f = v => v.toFixed(1);
  const poly = pts => pts.map(p => f(p[0]) + ' ' + f(p[1])).join('L');
  const build = el => {
    const W = Math.round(el.clientWidth || innerWidth), H = Math.round(el.clientHeight || 110), kind = el.dataset.cut, seed = +(el.dataset.seed || 1);
    const from = el.dataset.demo ? (kind === 'meridianos' ? COL.k : COL.b) : bgOf(el, -1), to = el.dataset.demo ? COL.k : bgOf(el, 1);
    let body = '';
    const fillTo = pts => `<path d="M0 ${H}L${poly(pts)}L${W} ${H}Z" fill="${to}"/>`;
    const line = (pts, w = 3, c = ICE, dash = '') => `<path d="M${poly(pts)}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linejoin="miter" stroke-miterlimit="6"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
    if (kind === 'acordeon') {
      const n = W < 700 ? 4 : 8, p = W / n, hi = H * .24, lo = H * .76, pts = [];
      for (let i = 0; i <= n; i++) { const y = (i + seed) % 2 ? hi : lo, y2 = (i + seed) % 2 ? lo : hi; pts.push([i * p, y]); if (i < n) pts.push([i * p + p * .22, y], [(i + 1) * p - p * .22, y2]); }
      body = fillTo(pts) + line(pts);
      for (let i = 1; i < n; i++) body += `<path d="M${f(i * p)} 0V${H}" stroke="${ICE}" stroke-width="2" stroke-dasharray="${i % 2 ? '14 8' : '3 9'}"/>`;
    }
    if (kind === 'esquina') {
      const s = H * .5, y0 = H * .62, fl = el.dataset.flip === '1';
      let pts = [[0, y0], [W - s, y0], [W, y0 - s]];
      let flap = `<path d="M${f(W - s)} ${f(y0)}L${f(W)} ${f(y0 - s)}L${f(W - s)} ${f(y0 - s)}Z" fill="${NEG}" stroke="${ICE}" stroke-width="3" stroke-linejoin="miter"/>`;
      if (fl) { pts = [[0, y0 - s], [s, y0], [W, y0]]; flap = `<path d="M${f(s)} ${f(y0)}L0 ${f(y0 - s)}L${f(s)} ${f(y0 - s)}Z" fill="${NEG}" stroke="${ICE}" stroke-width="3" stroke-linejoin="miter"/>`; }
      body = fillTo(pts) + line(pts) + flap;
      body += `<path d="M${fl ? 0 : W * .12} ${f(y0 + 14)}H${f(W * (fl ? .88 : 1))}" stroke="${ICE}" stroke-width="2" stroke-dasharray="10 9"/>`;
    }
    if (kind === 'costa') {
      const A = H * .17, pts = [], ph = seed * 1.7;
      for (let x = 0; x <= W + 6; x += 6) pts.push([x, H * .5 + A * (Math.sin(x / (W / 6.5) + ph) + .6 * Math.sin(x / (W / 15) + ph * 2) + .3 * Math.sin(x / (W / 37) + ph * 3))]);
      body = fillTo(pts) + line(pts, 4);
      [-12, -24].forEach((d, k) => { body += line(pts.map(p => [p[0], p[1] + d]), 2, ICE, k ? '4 10' : '16 8'); });
      body += line(pts.map(p => [p[0], p[1] + 12]), 2, ICE, '3 9');
    }
    if (kind === 'meridianos') {
      body = '';
      [.18, .38, .58, .78].forEach((fy, k) => { const y = H * fy, b = H * (.22 - k * .05); body += `<path d="M0 ${f(y)}Q${f(W / 2)} ${f(y - b * 2)} ${W} ${f(y)}" fill="none" stroke="${AZUL}" stroke-width="${6 - k}" stroke-linecap="butt"/>`; });
      for (let i = 1; i < 12; i++) { const x = W * i / 12; body += `<path d="M${f(x)} 0V${H}" stroke="${AZUL}" stroke-width="2" stroke-dasharray="2 12"/>`; }
    }
    el.setAttribute('aria-hidden', 'true');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" preserveAspectRatio="none"><rect width="${W}" height="${H}" fill="${from}"/>${body}</svg>`;
  };
  const cuts = $$('[data-cut]');

  /* ---------- NEATLINE: marco de mapa con segmentos alternos (secciones azules) ---------- */
  const neat = sec => {
    const sc = $('.scene', sec); let sv = $('.neat', sc); if (!sv) { sv = document.createElementNS(ns, 'svg'); sv.setAttribute('class', 'neat'); sv.setAttribute('aria-hidden', 'true'); sc.insertBefore(sv, $('.fr', sc)); }
    const W = sec.clientWidth, H = sec.clientHeight, m = W < 700 ? 8 : 16, t = 8, seg = W < 700 ? 24 : 40; let s = '';
    s += `<rect x="${m}" y="${m}" width="${W - 2 * m}" height="${H - 2 * m}" fill="none" stroke="${ICE}" stroke-width="3"/><rect x="${m + t + 3}" y="${m + t + 3}" width="${W - 2 * (m + t + 3)}" height="${H - 2 * (m + t + 3)}" fill="none" stroke="${ICE}" stroke-width="1.5"/>`;
    for (let x = m + 3, i = 0; x < W - m - 3; x += seg, i++) if (i % 2) { const w = Math.min(seg, W - m - 3 - x); s += `<rect x="${x}" y="${m + 1.5}" width="${w}" height="${t}" fill="${NEG}"/><rect x="${x}" y="${H - m - t - 1.5}" width="${w}" height="${t}" fill="${NEG}"/>`; }
    for (let y = m + 3, i = 0; y < H - m - 3; y += seg, i++) if (i % 2) { const h = Math.min(seg, H - m - 3 - y); s += `<rect x="${m + 1.5}" y="${y}" width="${t}" height="${h}" fill="${NEG}"/><rect x="${W - m - t - 1.5}" y="${y}" width="${t}" height="${h}" fill="${NEG}"/>`; }
    sv.setAttribute('viewBox', `0 0 ${W} ${H}`); sv.innerHTML = s;
  };

  /* ---------- FILAS TIPO NETFLIX ---------- */
  const WA = 'https://wa.me/525527699426', L = n => `assets/logos-mono/${n}_mono_hielo.svg`;
  const juegos = [['Zelda · Breath of the Wild','zelda-botw'],['Mario Kart World','mario-kart-world'],['Hollow Knight','hollow-knight'],['Metroid Dread','metroid-dread'],['Pokémon Escarlata','pokemon-scarlet'],['Super Mario Odyssey','mario-odyssey'],['Hades','hades'],['Cuphead','cuphead'],['Celeste','celeste'],['Kirby y la tierra olvidada','kirby-and-the-forgotten-land'],['Animal Crossing','animal-crossing-new-horizons'],['Mario Wonder','mario-wonder'],['Donkey Kong Bananza','donkey-kong-bananza'],['Zelda · Tears of the Kingdom','zelda-totk']];
  const streaming = [['Netflix',L('netflix'),'Series y películas en pantalla grande.'],['Spotify',L('spotify'),'Tu música y podcasts sin anuncios.'],['HBO Max',L('hbomax'),'Estrenos, series y cine.'],['Disney+',null,'Animación, Marvel y Star Wars.'],['Crunchyroll',L('crunchyroll'),'Anime en simulcast.'],['Prime Video',null,'Series, cine y envíos.'],['Apple TV+',L('appletv'),'Producciones originales.'],['YouTube Music',L('youtubemusic'),'Música y videos oficiales.']];
  const plataformas = [['Nintendo Switch',null,'Juegos, accesorios y cuentas para tu consola.'],['PlayStation',L('playstation'),'Catálogo para PS4 y PS5.'],['Steam',L('steam'),'Juegos para PC con entrega rápida.'],['Xbox Game Pass',null,'Cientos de juegos por suscripción.']];
  const ia = [['ChatGPT',null,'Escribe, resume y resuelve dudas.'],['Claude',L('claude'),'Redacta, analiza documentos y programa.'],['Google Gemini',L('googlegemini'),'Asistente de Google para texto e ideas.'],['Proton VPN',L('protonvpn'),'Navega con más privacidad.']];
  const svc = ([n, img, d], i) => `<article class="card s"><div class="medal"><span class="ring">${img ? `<img src="${img}" alt="Logo de ${n}" loading="lazy" draggable="false">` : `<span class="wm">${n}</span>`}</span></div><div class="in2"><span class="n">Destino ${pad(i)}</span><h4>${n}</h4><p>${d}</p><span class="chip">Consultar precio</span><a class="btn red sm" href="${WA}" rel="noopener">Cotizar →</a></div></article>`;
  const builders = {
    juegos: () => juegos.map(([n, fl], i) => `<article class="card g"><div class="cv"><img src="assets/portadas/${fl}.webp" alt="Portada de ${n}" width="800" height="1000" loading="lazy" draggable="false"></div><div class="in2"><span class="n">Destino ${pad(i)}</span><h4>${n}</h4><span class="chip">Consultar precio</span></div></article>`).join(''),
    streaming: () => streaming.map(svc).join(''), plataformas: () => plataformas.map(svc).join(''), ia: () => ia.map(svc).join('')
  };
  $$('[data-row]').forEach(row => {
    const id = 'row-' + row.dataset.row, title = row.dataset.title; row.classList.add('row');
    row.innerHTML = `<div class="row-head"><h3 id="${id}">${title}</h3><span class="cnt" aria-live="polite"></span><div class="row-ctl"><button type="button" class="prev" aria-label="Anterior: ${title}">←</button><button type="button" class="next" aria-label="Siguiente: ${title}">→</button></div></div><div class="row-wrap"><div class="track" tabindex="0" role="group" aria-labelledby="${id}">${builders[row.dataset.row]()}</div></div>`;
    const tr = $('.track', row), pv = $('.prev', row), nx = $('.next', row), cnt = $('.cnt', row), cards = [...tr.children];
    const stepPx = () => cards[0].offsetWidth + 18;
    const upd = () => { pv.disabled = tr.scrollLeft < 4; nx.disabled = tr.scrollLeft + tr.clientWidth >= tr.scrollWidth - 4; cnt.textContent = String(Math.min(cards.length, Math.round(tr.scrollLeft / stepPx()) + 1)).padStart(2, '0') + ' / ' + String(cards.length).padStart(2, '0'); };
    const go = d => tr.scrollBy({ left: d * Math.max(stepPx(), Math.floor(tr.clientWidth * .8 / stepPx()) * stepPx()), behavior: reduced ? 'auto' : 'smooth' });
    pv.addEventListener('click', () => go(-1)); nx.addEventListener('click', () => go(1));
    tr.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); addEventListener('resize', upd); upd();
    tr.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { go(1); e.preventDefault(); } if (e.key === 'ArrowLeft') { go(-1); e.preventDefault(); } });
    let down = false, sx = 0, sl = 0, moved = 0;
    tr.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse' || e.button !== 0) return; down = true; sx = e.clientX; sl = tr.scrollLeft; moved = 0; });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); if (moved > 5) tr.classList.add('drag'); tr.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; if (moved > 5) { tr.classList.remove('drag'); const s = stepPx(); tr.scrollTo({ left: Math.round(tr.scrollLeft / s) * s, behavior: 'smooth' }); } });
  });

  /* ---------- PARALLAX: azul lento, rojo medio, piezas rápidas (con tope) ---------- */
  const items = $$('.ly[data-speed]'); let tick = false;
  const lim = el => el.classList.contains('bk') ? 26 : 70;
  const par = () => {
    tick = false; if (reduced) return; const vh = innerHeight, k = innerWidth < 700 ? .5 : 1;
    items.forEach(el => { const b = el.parentElement.getBoundingClientRect(); if (b.bottom < -200 || b.top > vh + 200) return;
      const raw = (b.top + b.height / 2 - vh / 2) * -parseFloat(el.dataset.speed) * k, Lm = lim(el); el.style.setProperty('--py', (Lm * Math.tanh(raw / Lm)).toFixed(1) + 'px'); });
  };

  /* ---------- RUTA del viaje (carril izquierdo) + alfiler rojo ---------- */
  const main = $('#contenido'), rutaSvg = $('#ruta'), rutap = $('#rutap'), pin = $('#pin'); let rlen = 0;
  const secs = $$('.sec');
  const ruta = () => {
    const mt = main.getBoundingClientRect().top + scrollY, g = (innerWidth - Math.min(1240, innerWidth - 2 * Math.min(56, innerWidth * .04))) / 2;
    if (g < 44) { rutaSvg.style.display = 'none'; rlen = 0; return; } rutaSvg.style.display = '';
    rutaSvg.setAttribute('viewBox', `0 0 ${innerWidth} ${main.offsetHeight}`);
    const base = g * .5, amp = Math.min(22, g * .3), pts = [];
    secs.forEach((s, i) => { const t = s.getBoundingClientRect().top + scrollY - mt, h = s.offsetHeight; for (let k = 0; k <= 4; k++) pts.push([base + amp * Math.sin((i * 4 + k) * 1.3), t + h * k / 4]); });
    let d = `M${f(pts[0][0])} ${f(pts[0][1])}`;
    for (let i = 0; i < pts.length - 1; i++) { const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2; d += `C${f(p1[0] + (p2[0] - p0[0]) / 6)} ${f(p1[1] + (p2[1] - p0[1]) / 6)} ${f(p2[0] - (p3[0] - p1[0]) / 6)} ${f(p2[1] - (p3[1] - p1[1]) / 6)} ${f(p2[0])} ${f(p2[1])}`; }
    rutap.setAttribute('d', d); rlen = rutap.getTotalLength();
  };
  const viaje = () => {
    if (!rlen) return; const mt = main.getBoundingClientRect().top + scrollY, p = Math.max(0, Math.min(1, (scrollY + innerHeight * .5 - mt) / main.offsetHeight)), pt = rutap.getPointAtLength(p * rlen);
    pin.setAttribute('transform', `translate(${f(pt.x)} ${f(pt.y)})`);
  };

  /* ---------- HUD: nivel actual y aguja ---------- */
  const hn = $('#hudn'), hl = $('#hudl'), needle = $('#needle');
  const hud = () => {
    let cur = secs[0]; secs.forEach(s => { if (s.getBoundingClientRect().top < innerHeight * .45) cur = s; });
    hn.textContent = cur.dataset.nivel; hl.textContent = cur.dataset.name;
    if (!reduced) needle.style.setProperty('--rot', (scrollY * .12 % 360).toFixed(1) + 'deg');
  };

  const layout = () => { cuts.forEach(build); $$('.sheet').forEach(neat); ruta(); par(); viaje(); hud(); };
  layout(); let rz; addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(layout, 140); });
  document.fonts && document.fonts.ready.then(layout); addEventListener('load', layout);
  addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(() => { par(); viaje(); hud(); }); } }, { passive: true });
})();
