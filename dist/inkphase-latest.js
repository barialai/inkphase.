(() => {
  const stage = document.querySelector('[data-latest-stage]');
  const controls = document.querySelectorAll('[data-latest-device]');
  if (!stage || !controls.length) return;

  const dimensions = { mobile: 390 };
  const updateScale = () => {
    const width = dimensions[stage.dataset.device] || (window.innerWidth <= 760 ? 1440 : 0);
    if (width) {
      const screen = stage.querySelector('.inkphase-latest-screen');
      const scale = screen.clientWidth / width;
      stage.style.setProperty('--device-scale', scale.toFixed(5));
      stage.style.setProperty('--device-height', `${Math.ceil(screen.clientHeight / scale)}px`);
    } else {
      stage.style.removeProperty('--device-scale');
      stage.style.removeProperty('--device-height');
    }
  };

  controls.forEach(button => button.addEventListener('click', () => {
    stage.dataset.device = button.dataset.latestDevice;
    controls.forEach(control => {
      const active = control === button;
      control.classList.toggle('is-active', active);
      control.setAttribute('aria-pressed', String(active));
    });
    updateScale();
  }));

  if ('ResizeObserver' in window) new ResizeObserver(updateScale).observe(stage);
  else window.addEventListener('resize', updateScale);
  updateScale();
})();
