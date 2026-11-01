/* ATHAY · The Twentieth Issue · website edition
   Plain JS, no libraries, works straight from GitHub Pages / Netlify / Cloudflare Pages. */
(() => {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const BIRTH = new Date(2006, 9, 31, 0, 0, 0); // 31 October 2006

  const REASONS = [
    'Your smile, which fixes my worst days.',
    'The way you face every storm in our relationship, calmly and together.',
    'How you keep our story going, with patience and a whole heart.',
    'You make ordinary moments feel like celebrations.',
    'You listen with your whole heart.',
    'Your beautiful, stubborn strength.',
    'The little names you call me. We never need our real ones.',
    'You make me want to be a better man.',
    'Your hand fits perfectly in mine.',
    'You are my calm when everything is loud.',
    'Your honesty, even when it’s hard.',
    'The way you care for the people you love.',
    'You make silence feel comfortable.',
    'The way you dream about our future, and put me in every picture.',
    'The way you look at me, as if I were your whole world.',
    'The way you hold on to my words, and keep every one of them.',
    'You are beautiful, inside and out.',
    'You chose me, and you keep choosing me.',
    'Every day with you feels like a gift.',
    'Because you are you, and there is no one else like you.'
  ];

  // Photos for the "Every moment" marquees (everything that isn't already big elsewhere is welcome here too)
  const MOMENTS_A = ['p001','p085','p059','p009','p019','p024','p071','p072','p073','p037','p050','p079','p104','p026'];
  const MOMENTS_B = ['p002','p054','p013','p045','p056','p063','p066','p062','p083','p070','p015','p044','p012','p068'];

  /* ---------------- sky: drifting sparkles & petals ---------------- */
  const sky = $('#sky'), ctx = sky.getContext('2d');
  let W, H, DPR, motes = [], bursts = [];
  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = sky.width = innerWidth * DPR; H = sky.height = innerHeight * DPR;
    sky.style.width = innerWidth + 'px'; sky.style.height = innerHeight + 'px';
  }
  function mote(initial) {
    const petal = Math.random() < .35;
    return {
      x: Math.random() * W, y: initial ? Math.random() * H : -20 * DPR,
      r: (petal ? 5 + Math.random() * 5 : 1 + Math.random() * 2.2) * DPR,
      vy: (.15 + Math.random() * .45) * DPR, vx: (Math.random() - .5) * .3 * DPR,
      a: Math.random() * Math.PI * 2, va: (Math.random() - .5) * .02,
      tw: Math.random() * Math.PI * 2, petal
    };
  }
  function heartPath(c, x, y, s) {
    c.beginPath();
    c.moveTo(x, y + s * .3);
    c.bezierCurveTo(x, y, x - s * .5, y - s * .1, x - s * .5, y + s * .25);
    c.bezierCurveTo(x - s * .5, y + s * .55, x, y + s * .75, x, y + s);
    c.bezierCurveTo(x, y + s * .75, x + s * .5, y + s * .55, x + s * .5, y + s * .25);
    c.bezierCurveTo(x + s * .5, y - s * .1, x, y, x, y + s * .3);
    c.fill();
  }
  function burst(x, y, n = 70) {
    const colours = ['#e8576f', '#f3a5b4', '#e9cd8b', '#f3dda0', '#c9a04e', '#ffffff'];
    for (let i = 0; i < n; i++) {
      const ang = Math.random() * Math.PI * 2, sp = (2 + Math.random() * 7) * DPR;
      bursts.push({ x: x * DPR, y: y * DPR, vx: Math.cos(ang) * sp, vy: Math.sin(ang) * sp - 3 * DPR,
        s: (6 + Math.random() * 10) * DPR, life: 1, c: colours[i % colours.length], heart: Math.random() < .6 });
    }
  }
  function tick() {
    ctx.clearRect(0, 0, W, H);
    for (const m of motes) {
      m.y += m.vy; m.x += m.vx + Math.sin(m.tw) * .2 * DPR; m.a += m.va; m.tw += .02;
      if (m.y > H + 20) Object.assign(m, mote(false));
      if (m.petal) {
        ctx.save(); ctx.translate(m.x, m.y); ctx.rotate(m.a);
        ctx.fillStyle = 'rgba(232,150,160,.42)';
        ctx.beginPath(); ctx.ellipse(0, 0, m.r, m.r * .55, 0, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
      } else {
        const g = .45 + .45 * Math.sin(m.tw * 2);
        ctx.fillStyle = `rgba(214,175,96,${g})`;
        ctx.beginPath(); ctx.arc(m.x, m.y, m.r, 0, Math.PI * 2); ctx.fill();
      }
    }
    for (let i = bursts.length - 1; i >= 0; i--) {
      const b = bursts[i];
      b.x += b.vx; b.y += b.vy; b.vy += .12 * DPR; b.vx *= .985; b.life -= .011;
      if (b.life <= 0) { bursts.splice(i, 1); continue; }
      ctx.globalAlpha = Math.max(b.life, 0); ctx.fillStyle = b.c;
      if (b.heart) heartPath(ctx, b.x, b.y, b.s); else { ctx.beginPath(); ctx.arc(b.x, b.y, b.s / 4, 0, Math.PI * 2); ctx.fill(); }
      ctx.globalAlpha = 1;
    }
    requestAnimationFrame(tick);
  }
  resize();
  addEventListener('resize', resize);
  const MOTES = reduced ? 0 : (innerWidth < 700 ? 26 : 48);
  for (let i = 0; i < MOTES; i++) motes.push(mote(true));
  requestAnimationFrame(tick);

  /* ---------------- gate / seal ---------------- */
  const gate = $('#gate'), seal = $('#seal'), song = $('#song'), musicBtn = $('#music');
  let musicOK = true, wantMusic = true, fadeTimer = 0;
  song.addEventListener('error', () => { musicOK = false; musicBtn.hidden = true; });
  function fadeTo(target, ms, then) {
    clearInterval(fadeTimer);
    const from = song.volume, t0 = performance.now();
    fadeTimer = setInterval(() => {
      const p = Math.min(1, (performance.now() - t0) / ms);
      song.volume = from + (target - from) * p;
      if (p === 1) { clearInterval(fadeTimer); then && then(); }
    }, 50);
  }
  function playMusic() {
    if (!musicOK) return;
    song.volume = 0;
    song.play().then(() => { musicBtn.classList.add('playing'); fadeTo(.7, 2500); }).catch(() => {});
  }
  function pauseMusic() {
    musicBtn.classList.remove('playing');
    fadeTo(0, 600, () => song.pause());
  }
  // remember where the song was, so the magazine page can carry on from the same moment
  addEventListener('pagehide', () => {
    try { sessionStorage.setItem('song', JSON.stringify({ t: song.currentTime, on: wantMusic && !song.paused })); } catch (e) {}
  });
  // pause when she switches apps/tabs, carry on when she comes back
  document.addEventListener('visibilitychange', () => {
    if (!wantMusic || !musicOK || gate.isConnected && !gate.classList.contains('gone')) return;
    if (document.hidden) { clearInterval(fadeTimer); song.pause(); }
    else playMusic();
  });

  function openGate() {
    seal.classList.add('crack');
    const r = seal.getBoundingClientRect();
    burst(r.left + r.width / 2, r.top + r.height / 2, 90);
    setTimeout(() => {
      gate.classList.add('gone');
      document.body.classList.remove('locked');
      $('#cover').classList.add('ready');
    }, reduced ? 0 : 650);
    if (musicOK) { musicBtn.hidden = false; playMusic(); }
  }
  seal.addEventListener('click', openGate, { once: true });
  musicBtn.addEventListener('click', () => {
    wantMusic = !musicBtn.classList.contains('playing');
    wantMusic ? playMusic() : pauseMusic();
  });

  /* ---------------- reveal on scroll ---------------- */
  $$('[data-reveal-children]').forEach(p => [...p.children].forEach((c, i) => {
    if (!c.style.getPropertyValue('--d')) c.style.setProperty('--d', (i * .1).toFixed(2) + 's');
  }));
  const io = new IntersectionObserver(entries => {
    for (const e of entries) if (e.isIntersecting) {
      e.target.classList.add('in');
      e.target.dispatchEvent(new CustomEvent('revealed'));
      io.unobserve(e.target);
    }
  }, { threshold: .18, rootMargin: '0px 0px -6% 0px' });
  $$('[data-reveal],[data-reveal-children]').forEach(el => io.observe(el));

  /* ---------------- progress bar + chapter dots ---------------- */
  const bar = $('#progress');
  const sections = $$('main > section[data-title]').filter(s => !s.classList.contains('chapter'));
  const dots = $('#dots');
  sections.forEach(s => {
    const a = document.createElement('a');
    a.href = '#' + s.id; a.innerHTML = `<span>${s.dataset.title}</span>`;
    a.setAttribute('aria-label', s.dataset.title);
    dots.appendChild(a);
  });
  const dotLinks = $$('a', dots);
  const spy = new IntersectionObserver(entries => {
    for (const e of entries) if (e.isIntersecting) {
      const i = sections.indexOf(e.target);
      dotLinks.forEach((d, j) => d.classList.toggle('on', i === j));
    }
  }, { rootMargin: '-45% 0px -50% 0px' });
  sections.forEach(s => spy.observe(s));

  /* parallax for a few big photos */
  const centreImg = $('.centre-bg img'), coverCut = $('.cover-cut'), mast = $('.masthead');
  let ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => {
      const y = scrollY, max = document.documentElement.scrollHeight - innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
      if (!reduced) {
        if (y < innerHeight * 1.2) {
          coverCut.style.translate = `0 ${y * .12}px`;
          mast.style.translate = `0 ${y * .35}px`;
        }
        const r = centreImg.parentElement.getBoundingClientRect();
        if (r.bottom > 0 && r.top < innerHeight) centreImg.style.transform = `translateY(${(r.top / innerHeight) * -12 - 8}%)`;
      }
      ticking = false;
    });
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------- live counter ---------------- */
  const cnt = k => $(`[data-count="${k}"]`);
  const fmt = n => n.toLocaleString('en-IN');
  let counterStart = 0;
  function updateCounter() {
    const now = new Date();
    const ms = now - BIRTH;
    let years = now.getFullYear() - BIRTH.getFullYear();
    if (now < new Date(now.getFullYear(), BIRTH.getMonth(), BIRTH.getDate())) years--;
    const target = { years, days: Math.floor(ms / 864e5), hours: Math.floor(ms / 36e5), seconds: Math.floor(ms / 1e3) };
    const t = counterStart ? Math.min(1, (performance.now() - counterStart) / 2200) : 1;
    const ease = 1 - Math.pow(1 - t, 3);
    for (const k in target) cnt(k).textContent = fmt(Math.floor(target[k] * (k === 'seconds' && t === 1 ? 1 : ease)));
  }
  $('.tally').addEventListener('revealed', () => {
    counterStart = performance.now();
    const loop = () => { updateCounter(); if (performance.now() - counterStart < 2300) requestAnimationFrame(loop); };
    loop();
    setInterval(updateCounter, 1000);
  });


  /* ---------------- camera in "Glow" ---------------- */
  const vf = $('#viewfinder'), shots = $$('img', vf);
  let shot = 0;
  function nextShot() {
    shots[shot].classList.remove('on');
    shot = (shot + 1) % shots.length;
    shots[shot].classList.add('on');
    vf.classList.remove('flash'); void vf.offsetWidth; vf.classList.add('flash');
  }
  let camTimer = setInterval(nextShot, 3800);
  $('#shutter').addEventListener('click', () => { clearInterval(camTimer); nextShot(); camTimer = setInterval(nextShot, 3800); });
  vf.addEventListener('click', () => openLightboxSrc(shots[shot].src));

  /* ---------------- 20 reasons cards ---------------- */
  const cardsEl = $('#cards');
  REASONS.forEach((r, i) => {
    const b = document.createElement('button');
    b.className = 'card'; b.style.setProperty('--d', (i * .05).toFixed(2) + 's');
    b.setAttribute('aria-label', `Reason ${i + 1}`);
    b.innerHTML = `<span class="front"><b>${i + 1}</b><small>tap to open</small></span><span class="back"><i>${i + 1}</i>${r}</span>`;
    b.addEventListener('click', e => {
      b.classList.toggle('open');
      if (b.classList.contains('open')) burst(e.clientX || innerWidth / 2, e.clientY || innerHeight / 2, 18);
      if ($$('.card.open').length === REASONS.length) celebrateAll();
    });
    cardsEl.appendChild(b);
  });
  io.observe(cardsEl);
  let celebrated = false;
  function celebrateAll() {
    if (celebrated) return; celebrated = true;
    const r = cardsEl.getBoundingClientRect();
    burst(r.left + r.width / 2, r.top + r.height / 2, 120);
  }
  $('#openAll').addEventListener('click', () => {
    $$('.card').forEach((c, i) => setTimeout(() => { c.classList.add('open'); if (i === REASONS.length - 1) celebrateAll(); }, reduced ? 0 : i * 90));
  });

  /* ---------------- love-language chat ---------------- */
  const chat = $('#chat'), msgs = $$('.msg', chat), typing = $('.typing', chat);
  let chatPlayed = false;
  function playChat() {
    if (chatPlayed) return; chatPlayed = true;
    msgs.forEach((m, i) => {
      setTimeout(() => { typing.classList.add('show'); chat.appendChild(typing); }, i * 1300);
      setTimeout(() => { typing.classList.remove('show'); m.classList.add('show'); }, i * 1300 + 900);
    });
  }
  $('.phone').addEventListener('revealed', playChat);

  /* ---------------- envelope + love letter ---------------- */
  const env = $('#envelope'), letter = $('#letterText');
  env.addEventListener('click', () => {
    env.classList.add('open');
    const r = env.getBoundingClientRect();
    burst(r.left + r.width / 2, r.top + r.height / 3, 60);
    setTimeout(() => {
      letter.hidden = false;
      $$('p', letter).forEach((p, i) => p.style.animationDelay = (0.5 + i * .35) + 's');
      $$('.zoom', letter).forEach(bindZoom);
      letter.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
    }, reduced ? 0 : 1400);
  });

  /* ---------------- every-moment marquees ---------------- */
  function fillMarquee(el, list) {
    const html = list.map(n => `<img class="zoom" src="photos/${n}.jpg" alt="" loading="lazy">`).join('');
    el.innerHTML = html + html; // doubled so the loop is seamless
  }
  fillMarquee($('#marquee'), MOMENTS_A);
  fillMarquee($('#marquee2'), MOMENTS_B);
  // film strips loop seamlessly too
  $$('.film-track').forEach(t => { t.innerHTML += t.innerHTML; });

  /* ---------------- finale: press & hold ---------------- */
  const finale = $('#finale'), hold = $('#hold'), ring = $('#holdRing'), reveal = $('#finaleReveal');
  const HOLD_MS = 2200, CIRC = 340;
  let holdStart = 0, holdRAF = 0, done = false;
  function holdFrame() {
    const p = Math.min(1, (performance.now() - holdStart) / HOLD_MS);
    ring.style.strokeDashoffset = CIRC * (1 - p);
    if (p >= 1) return finish();
    holdRAF = requestAnimationFrame(holdFrame);
  }
  function startHold(e) {
    if (done) return;
    e.preventDefault();
    hold.classList.add('pressing');
    holdStart = performance.now();
    holdRAF = requestAnimationFrame(holdFrame);
    if (navigator.vibrate) navigator.vibrate(30);
  }
  function endHold() {
    if (done || !hold.classList.contains('pressing')) return;
    hold.classList.remove('pressing');
    cancelAnimationFrame(holdRAF);
    ring.style.transition = 'stroke-dashoffset .5s';
    ring.style.strokeDashoffset = CIRC;
    setTimeout(() => ring.style.transition = '', 500);
    $('#holdHint').textContent = 'don’t let go… hold a little longer';
  }
  function finish() {
    done = true;
    finale.classList.add('held');
    reveal.hidden = false;
    if (navigator.vibrate) navigator.vibrate([60, 60, 120]);
    const r = finale.getBoundingClientRect();
    const fire = (k) => burst(innerWidth * (.2 + Math.random() * .6), Math.max(r.top, 0) + innerHeight * (.25 + Math.random() * .3), 80);
    for (let k = 0; k < 6; k++) setTimeout(() => fire(k), k * 380);
  }
  hold.addEventListener('pointerdown', startHold);
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(t => hold.addEventListener(t, endHold));
  hold.addEventListener('contextmenu', e => e.preventDefault());
  hold.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) startHold(e); });
  hold.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') endHold(); });
  $('#again').addEventListener('click', () => scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }));

  /* ---------------- lightbox ---------------- */
  const lb = $('#lightbox'), lbImg = $('img', lb);
  let gallery = [], gi = 0;
  function openLightboxSrc(src) {
    gallery = [...new Set($$('main img.zoom').map(i => i.currentSrc || i.src))];
    gi = Math.max(0, gallery.indexOf(src));
    show();
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
  }
  function show() { lbImg.src = gallery[gi]; lbImg.style.animation = 'none'; void lbImg.offsetWidth; lbImg.style.animation = ''; }
  function close() { lb.hidden = true; document.body.style.overflow = ''; }
  function step(d) { gi = (gi + d + gallery.length) % gallery.length; show(); }
  function bindZoom(img) {
    if (img.dataset.bound) return; img.dataset.bound = 1;
    img.addEventListener('click', () => openLightboxSrc(img.currentSrc || img.src));
  }
  $$('img.zoom').forEach(bindZoom);
  $('.lb-close').addEventListener('click', close);
  $('.lb-prev').addEventListener('click', e => { e.stopPropagation(); step(-1); });
  $('.lb-next').addEventListener('click', e => { e.stopPropagation(); step(1); });
  lb.addEventListener('click', e => { if (e.target === lb) close(); });
  addEventListener('keydown', e => {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'ArrowRight') step(1);
  });
  let tx = 0;
  lb.addEventListener('touchstart', e => tx = e.touches[0].clientX, { passive: true });
  lb.addEventListener('touchend', e => { const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); });

  /* sparkle trail on tap anywhere (tiny, just for joy) */
  addEventListener('pointerdown', e => {
    if (e.target.closest('button, a, #lightbox, .zoom')) return;
    burst(e.clientX, e.clientY, 8);
  });
})();
