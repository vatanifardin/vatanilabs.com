// Hero background: a field of points rolling like a calm sea, seen in
// perspective. Pure canvas, no libraries; pauses when off screen and
// stays still for people who prefer reduced motion.
(function () {
  const canvas = document.getElementById('field');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let w = 0, h = 0, dpr = 1, t = 0, visible = true;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.clientWidth; h = canvas.clientHeight;
    canvas.width = w * dpr; canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  const COLS = 120, ROWS = 100;

  function frame() {
    ctx.clearRect(0, 0, w, h);
    const horizon = h * 0.40, cx = w * 0.62;
    for (let r = 0; r < ROWS; r++) {
      const z = 1.15 + r * 0.13;              // distance
      const scale = 1 / z;
      const y0 = horizon + (h * 0.75) * scale; // farther rows sit higher
      for (let c = 0; c < COLS; c++) {
        const x = (c - COLS / 2) * 24;
        const wave =
          Math.sin(c * 0.18 + t * 0.9 + r * 0.25) * 22 +
          Math.sin(c * 0.05 - t * 0.5 + r * 0.6) * 30 +
          Math.cos(r * 0.32 + t * 0.7) * 12;
        const px = cx + x * scale * 1.6;
        const py = y0 - wave * scale * 1.6;
        if (px < -10 || px > w + 10 || py < 0 || py > h) continue;
        const near = 1 - r / ROWS;
        const tealMix = Math.max(0, Math.sin(c * 0.08 + r * 0.05 + t * 0.4)) * near;
        const a = 0.18 + near * 0.7;
        ctx.fillStyle = tealMix > 0.45
          ? `rgba(44,196,184,${a})`
          : `rgba(220,228,255,${a * 0.75})`;
        const s = Math.max(0.7, 2.6 * scale * 1.5);
        ctx.fillRect(px, py, s, s);
      }
    }
  }

  function loop() {
    if (visible) { t += 0.012; frame(); }
    if (!still) requestAnimationFrame(loop);
  }

  window.addEventListener('resize', () => { resize(); frame(); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((e) => { visible = e[0].isIntersecting; }).observe(canvas);
  }
  resize();
  frame();
  loop();
})();
