// Small behaviours shared by every page: things appear as you scroll,
// cards light up under the pointer, numbers count up, and the little
// feature scenes (converter, flashcard, languages) play while on screen.
(function () {
  window.VL_READY = true;   // tells the page the scripts loaded (else everything is simply shown)
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const all = (s, r) => Array.from((r || document).querySelectorAll(s));
  const io = 'IntersectionObserver' in window;

  // Appear on scroll
  if (io && !still) {
    const seen = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); seen.unobserve(e.target); }
    }), { threshold: 0.12 });
    all('.rv').forEach((el) => seen.observe(el));
  } else all('.rv').forEach((el) => el.classList.add('in'));

  // Tiles play only while visible ("live"); "seen" stays once shown.
  if (io) {
    const live = new IntersectionObserver((es) => es.forEach((e) => {
      e.target.classList.toggle('live', e.isIntersecting);
      if (e.isIntersecting) e.target.classList.add('seen');
    }), { threshold: 0.25 });
    all('.tile').forEach((el) => live.observe(el));
  } else all('.tile').forEach((el) => el.classList.add('live', 'seen'));

  // Light under the pointer
  all('.glow').forEach((el) => el.addEventListener('pointermove', (e) => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    el.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true }));

  // Count up
  function countUp(el) {
    const end = Number(el.dataset.count), t0 = performance.now(), dur = 1500;
    (function step(now) {
      const p = Math.min(1, (now - t0) / dur), k = 1 - Math.pow(1 - p, 4);
      el.firstChild.nodeValue = Math.round(end * k);
      if (p < 1) requestAnimationFrame(step);
    })(t0);
  }
  if (io && !still) {
    const cnt = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { countUp(e.target); cnt.unobserve(e.target); }
    }), { threshold: 0.6 });
    all('[data-count]').forEach((el) => { el.firstChild.nodeValue = '0'; cnt.observe(el); });
  }

  // App tabs with a pager
  const tabs = all('.tab');
  if (tabs.length) {
    const count = document.getElementById('count');
    let cur = 0;
    const two = (n) => String(n).padStart(2, '0');
    const show = (i) => {
      cur = (i + tabs.length) % tabs.length;
      tabs.forEach((t, j) => {
        const on = j === cur;
        t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (count) count.textContent = two(cur + 1) + ' / ' + two(tabs.length);
      // With many apps the row of tabs is wider than the page: bring the
      // open tab into sight (the row moves sideways, the page stays put).
      const row = tabs[cur].parentElement, a = tabs[cur].getBoundingClientRect(), b = row.getBoundingClientRect();
      if (a.left < b.left || a.right > b.right) row.scrollBy({ left: a.left < b.left ? a.left - b.left - 20 : a.right - b.right + 20, behavior: 'smooth' });
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => show(i));
      t.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          show(cur + (e.key === 'ArrowRight' ? 1 : -1)); tabs[cur].focus();
        }
      });
    });
    const prev = document.getElementById('prev'), next = document.getElementById('next');
    if (prev) prev.onclick = () => show(cur - 1);
    if (next) next.onclick = () => show(cur + 1);
  }

  // Email links: besides opening the mail app (where there is one), copy
  // the address and say so, so the click always does something visible.
  let toast, toastTimer;
  function say(text) {
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'toast'; toast.setAttribute('role', 'status');
      document.body.appendChild(toast);
    }
    toast.textContent = text;
    toast.classList.add('on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('on'), 3200);
  }
  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise((ok, fail) => {          // older browsers
      const t = document.createElement('textarea');
      t.value = text; t.style.position = 'fixed'; t.style.opacity = '0';
      document.body.appendChild(t); t.select();
      try { document.execCommand('copy') ? ok() : fail(); } catch (e) { fail(e); }
      t.remove();
    });
  }
  // The page carries these two messages in its own language (see build.py).
  const own = document.body.dataset;
  all('a[href^="mailto:"]').forEach((a) => a.addEventListener('click', () => {
    const address = a.getAttribute('href').slice(7).split('?')[0];
    copy(address).then(
      () => say((own.copied || 'Email address copied: ') + address),
      () => say((own.write || 'Write to us at ') + address));
  }));

  // Language menu: close it with a click elsewhere or with Escape.
  const menu = document.querySelector('.lang');
  if (menu) {
    document.addEventListener('click', (e) => { if (menu.open && !menu.contains(e.target)) menu.open = false; });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && menu.open) { menu.open = false; menu.querySelector('summary').focus(); }
    });
  }

  if (still) return;
  const playing = (el) => { const t = el.closest('.tile'); return !t || t.classList.contains('live'); };
  // Lists the page hands over in its own language, as data- attributes.
  const given = (el, name, fallback) => {
    try { return JSON.parse(el.dataset[name]) || fallback; } catch (e) { return fallback; }
  };

  // Converter: real conversions, numbers roll into place
  all('[data-conv]').forEach((box) => {
    const pairs = given(box, 'pairs', [
      ['1', 'bbl', '158.987', 'L'], ['1,000', 'psi', '68.948', 'bar'],
      ['10,000', 'ft', '3,048', 'm'], ['1', 'm³', '6.2898', 'bbl'],
    ]);
    const a = box.querySelector('[data-a]'), ua = box.querySelector('[data-ua]');
    const b = box.querySelector('[data-b]'), ub = box.querySelector('[data-ub]');
    let i = 0;
    const roll = (el, text) => {
      const t0 = performance.now();
      (function step(now) {
        const p = Math.min(1, (now - t0) / 520);
        el.textContent = p < 1 ? text.replace(/[0-9]/g, () => Math.floor(Math.random() * 10)) : text;
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    };
    setInterval(() => {
      if (!playing(box)) return;
      i = (i + 1) % pairs.length;
      roll(a, pairs[i][0]); ua.textContent = pairs[i][1];
      roll(b, pairs[i][2]); ub.textContent = pairs[i][3];
    }, 2600);
  });

  // Flashcard: flip, then the next term
  all('.flash').forEach((card) => {
    const terms = given(card, 'cards', [
      ['Blowout preventer', 'Valves at the wellhead that seal the well if pressure control is lost.'],
      ['Kick', 'An unwanted flow of formation fluid into the wellbore.'],
      ['Porosity', 'The share of a rock’s volume made of pores that can hold fluids.'],
    ]);
    const front = card.querySelector('.front b'), back = card.querySelector('.back span');
    let i = 0, flipped = false;
    setInterval(() => {
      if (!playing(card)) return;
      flipped = !flipped;
      card.classList.toggle('flip', flipped);
      if (!flipped) {
        setTimeout(() => {
          i = (i + 1) % terms.length;
          front.textContent = terms[i][0]; back.textContent = terms[i][1];
        }, 450);
      }
    }, 2700);
  });

  // Seven languages
  all('.langs7').forEach((box) => {
    const word = box.querySelector('.langword'), chips = all('.chip', box);
    const words = (word.dataset.words || '').split('|');
    let i = 0;
    setInterval(() => {
      if (!playing(box)) return;
      word.classList.add('out');
      setTimeout(() => {
        i = (i + 1) % words.length;
        word.textContent = words[i];
        chips.forEach((c, j) => c.classList.toggle('on', j === i));
        word.classList.remove('out');
      }, 360);
    }, 1900);
  });
})();
