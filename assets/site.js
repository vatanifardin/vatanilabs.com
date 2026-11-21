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

  if (still) return;
  const playing = (el) => { const t = el.closest('.tile'); return !t || t.classList.contains('live'); };

  // Converter: real conversions, numbers roll into place
  const pairs = [
    ['1', 'bbl', '158.987', 'L'], ['1,000', 'psi', '68.948', 'bar'],
    ['10,000', 'ft', '3,048', 'm'], ['1', 'm³', '6.2898', 'bbl'],
  ];
  all('[data-conv]').forEach((box) => {
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
  const terms = [
    ['Blowout preventer', 'Valves at the wellhead that seal the well if pressure control is lost.'],
    ['Kick', 'An unwanted flow of formation fluid into the wellbore.'],
    ['Porosity', 'The share of a rock’s volume made of pores that can hold fluids.'],
  ];
  all('.flash').forEach((card) => {
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
