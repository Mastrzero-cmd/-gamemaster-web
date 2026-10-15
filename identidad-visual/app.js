/* GameMaster · Identidad visual v1 · JS vanilla */
(() => {
  const NEG = '#050506', ROJO = '#ff2a1f', HUESO = '#f4f4ef', AIRE = '#9aa8ff';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]reduce/.test(location.search);
  if (reduced) document.documentElement.classList.add('reduce');
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const NS = 'http://www.w3.org/2000/svg';

  /* ---------- CORTES DE SECCIÓN (5 tipos, arte distinto) ---------- */
  const W = 1440, H = 160;
  const R = (x, y, w, h, f, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${f}" ${extra}/>`;
  const cuts = {
    // 1 · Filo diagonal: vector geométrico (hero, bloques de marca)
    diagonal: () => `
      <polygon points="0,${H} 0,96 ${W},14 ${W},${H}" fill="currentColor"/>
      <polygon points="0,84 ${W},2 ${W},14 0,96" fill="${ROJO}"/>
      <polygon points="0,${H} 0,96 ${W},14 ${W},${H}" fill="none"/>
      <g fill="${NEG}">${R(180, 66, 18, 18, NEG)}${R(214, 58, 10, 10, NEG)}</g>
      <polygon points="0,72 ${W},-10 ${W},2 0,84" fill="${NEG}" opacity=".9"/>`,
    // 2 · Cinta de película: streaming
    pelicula: () => {
      let s = `<g transform="rotate(-2.2 720 80)">${R(-60, 38, W + 120, 92, NEG)}`;
      for (let x = -40; x < W + 60; x += 34) s += R(x, 46, 16, 11, HUESO, 'rx="2"') + R(x, 111, 16, 11, HUESO, 'rx="2"');
      for (let x = -30, i = 0; x < W + 60; x += 118, i++) {
        const c = i % 4 === 1 ? ROJO : i % 4 === 3 ? AIRE : '#1a1d3d';
        s += R(x, 64, 96, 42, c) + R(x + 6, 70, 84, 30, 'none', `stroke="${NEG}" stroke-width="3"`);
      }
      return s + '</g>';
    },
    // 3 · Circuito: IA / tecnología
    circuito: () => {
      const pts = []; let x = 0, y = 96; pts.push([0, y]);
      while (x < W) { const run = 60 + Math.floor(rnd() * 120); x = Math.min(W, x + run); pts.push([x, y]);
        if (x < W) { const d = [-36, -18, 0, 18, 36][Math.floor(rnd() * 5)]; if (d) { y = Math.max(46, Math.min(112, y + d)); x = Math.min(W, x + Math.abs(d)); pts.push([x, y]); } } }
      const line = pts.map(p => p.join(',')).join(' ');
      let s = `<polygon points="${line} ${W},${H} 0,${H}" fill="currentColor"/>`;
      [[-14, .9], [-30, .55], [-46, .3]].forEach(([dy, o]) => { s += `<polyline points="${pts.map(p => p[0] + ',' + (p[1] + dy)).join(' ')}" fill="none" stroke="${AIRE}" stroke-width="3" opacity="${o}"/>`; });
      pts.filter((_, i) => i % 3 === 1).forEach((p, i) => { s += R(p[0] - 7, p[1] - 21, 14, 14, i % 3 === 0 ? ROJO : NEG, `stroke="${NEG}" stroke-width="3"`); });
      return s;
    },
    // 4 · Escalera pixel: gaming
    pixel: () => {
      const u = 24; let y = 5, s = '', path = '';
      const cols = Math.ceil(W / u) + 1; const ys = [];
      for (let i = 0; i < cols; i++) { y = Math.max(2, Math.min(6, y + [-1, 0, 0, 1][Math.floor(rnd() * 4)])); ys.push(y); }
      ys.forEach((v, i) => { const top = v * u * .5 + 10; s += R(i * u, top, u + 1, H - top, 'currentColor'); s += R(i * u, top - 6, u + 1, 6, HUESO, 'opacity=".9"'); });
      ys.forEach((v, i) => { if (i % 7 === 3) { const top = v * u * .5 + 10; s += R(i * u + 4, top - 24, 16, 16, ROJO, `stroke="${NEG}" stroke-width="3"`); } });
      return s;
    },
    // 5 · Semitono: puntos que se apagan (transición suave de color)
    semitono: () => {
      let s = R(0, 98, W, 62, 'currentColor'); const step = 20;
      for (let r = 0; r < 6; r++) for (let x = (r % 2) * step / 2; x < W + step; x += step) s += `<circle cx="${x}" cy="${88 - r * 15}" r="${Math.max(1.2, 8.5 - r * 1.5)}" fill="currentColor"/>`;
      s += `<g fill="${ROJO}">${R(300, 40, 12, 12, ROJO)}${R(980, 24, 12, 12, ROJO)}${R(1210, 58, 8, 8, ROJO)}</g>`;
      return s;
    }
  };
  document.querySelectorAll('.cut').forEach(el => {
    seed = (el.dataset.seed | 0) || 7;
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.setAttribute('preserveAspectRatio', 'xMidYMax slice');
    svg.setAttribute('aria-hidden', 'true'); svg.innerHTML = cuts[el.dataset.type]();
    if (el.dataset.flip) svg.style.transform = 'scaleX(-1)';
    el.appendChild(svg);
  });

  /* ---------- PARALLAX: fondo fijo, piezas al frente se mueven ---------- */
  const stages = [...document.querySelectorAll('.stage, [data-parallax]')];
  const layers = stages.map(st => ({ st, items: [...st.querySelectorAll('.layer[data-depth]')] })).filter(s => s.items.length);
  const readout = document.getElementById('readout');
  let ticking = false;
  const tick = () => {
    ticking = false;
    const vh = innerHeight;
    layers.forEach(({ st, items }) => {
      const r = st.getBoundingClientRect(); if (r.bottom < -200 || r.top > vh + 200) return;
      const off = (r.top + r.height / 2 - vh / 2);
      items.forEach(el => { const d = parseFloat(el.dataset.depth); el.style.transform = `translate3d(0,${(off * d).toFixed(1)}px,0)`; });
    });
    if (readout) {
      const st = document.getElementById('parallax'); const r = st.getBoundingClientRect();
      const off = r.top + r.height / 2 - vh / 2;
      readout.innerHTML = `Fondo fijo: <b>0 px</b><br>Pieza lejana (0.10): <b>${(off * .1).toFixed(0)} px</b><br>Pieza media (0.22): <b>${(off * .22).toFixed(0)} px</b><br>Pieza al frente (0.38): <b>${(off * .38).toFixed(0)} px</b>`;
    }
  };
  const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(tick); } };
  if (!reduced) { addEventListener('scroll', req, { passive: true }); addEventListener('resize', req); tick(); }
  else if (readout) readout.innerHTML = 'Movimiento reducido activo: las piezas se quedan quietas.';

  /* ---------- FILAS TIPO NETFLIX ---------- */
  document.querySelectorAll('.rail').forEach(rail => {
    const track = rail.querySelector('.track'), L = rail.querySelector('.arrow.l'), Rt = rail.querySelector('.arrow.r');
    const upd = () => {
      const max = track.scrollWidth - track.clientWidth, x = track.scrollLeft;
      rail.dataset.l = x > 4 ? 1 : 0; rail.dataset.r = x < max - 4 ? 1 : 0;
      L.disabled = x <= 4; Rt.disabled = x >= max - 4;
    };
    const step = dir => track.scrollBy({ left: dir * track.clientWidth * .85, behavior: reduced ? 'auto' : 'smooth' });
    L.addEventListener('click', () => step(-1)); Rt.addEventListener('click', () => step(1));
    track.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); addEventListener('resize', upd);
    track.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { step(1); e.preventDefault(); } if (e.key === 'ArrowLeft') { step(-1); e.preventDefault(); } });
    // arrastre con mouse (en táctil el scroll nativo ya desliza)
    let down = false, sx = 0, sl = 0, moved = 0;
    track.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = track.scrollLeft; moved = 0; });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); if (moved > 5) track.classList.add('drag'); track.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; track.classList.remove('drag'); });
    track.addEventListener('click', e => { if (moved > 5) { e.preventDefault(); e.stopPropagation(); moved = 0; } }, true);
    track.addEventListener('dragstart', e => e.preventDefault());
    upd();
  });

  /* ---------- Catálogo y servicios de la muestra ---------- */
  const games = [
    ['zelda-totk', 'The Legend of Zelda: Tears of the Kingdom', 'Switch'], ['mario-kart-world', 'Mario Kart World', 'Switch 2'],
    ['hades', 'Hades', 'Switch'], ['metroid-dread', 'Metroid Dread', 'Switch'], ['celeste', 'Celeste', 'Switch'],
    ['donkey-kong-bananza', 'Donkey Kong Bananza', 'Switch 2'], ['hollow-knight', 'Hollow Knight', 'Switch'],
    ['kirby-and-the-forgotten-land', 'Kirby and the Forgotten Land', 'Switch'], ['mario-wonder', 'Super Mario Bros. Wonder', 'Switch'],
    ['zelda-botw', 'Zelda: Breath of the Wild', 'Switch'], ['animal-crossing-new-horizons', 'Animal Crossing: New Horizons', 'Switch'],
    ['pokemon-scarlet', 'Pokémon Escarlata', 'Switch'], ['mario-odyssey', 'Super Mario Odyssey', 'Switch'], ['cuphead', 'Cuphead', 'Switch']
  ];
  const gt = document.getElementById('track-cat');
  if (gt) gt.innerHTML = games.map(([f, t, p], i) => `<a class="gcard" href="#ejemplo-catalogo" aria-label="${t}, consultar precio">
    <div class="cover"><img src="assets/portadas/${f}.webp" alt="Portada de ${t}" loading="lazy" width="800" height="1000">${i < 3 ? '<span class="tag">Destacado</span>' : ''}</div>
    <div class="meta">${String(i + 1).padStart(2, '0')} · ${p}</div><h4>${t}</h4><div class="price">Consultar precio</div></a>`).join('');
  const svc = [['netflix', 'Netflix', 'Series y películas'], ['spotify', 'Spotify', 'Música'], ['hbo-max', 'HBO Max', 'Series y películas'], ['crunchyroll', 'Crunchyroll', 'Anime'],
    ['apple-tv-plus', 'Apple TV+', 'Series y películas'], ['disney-plus', 'Disney+', 'Series y películas'], ['amazon-prime', 'Amazon Prime', 'Video'], ['youtube-music', 'YouTube Music', 'Música']];
  const st = document.getElementById('track-stream');
  if (st) st.innerHTML = svc.map(([f, n, d]) => `<a class="scard" href="#ejemplo-streaming" aria-label="${n}, consultar precio">
    <div class="plate"><img src="assets/servicios/${f}.svg" alt="Logo de ${n}" loading="lazy"></div><b>${n}</b><small>${d} · Consultar precio</small></a>`).join('');

  /* decoración: estrellas pixel del fondo fijo */
  document.querySelectorAll('.fx .stars').forEach(g => { seed = 11; for (let i = 0; i < 9; i++) { const s = document.createElement('i'); s.style.left = (rnd() * 96 + 1) + '%'; s.style.top = (rnd() * 46 + 4) + '%'; s.style.opacity = '.85'; g.appendChild(s); } });
  dispatchEvent(new Event('resize'));
})();
