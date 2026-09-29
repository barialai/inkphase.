(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  const targets = [
    ...document.querySelectorAll('.inkphase-gallery, .inkphase-giveaways, .inkphase-workpage-heading, .inkphase-workpage-item')
  ];
  if (!targets.length) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-inview');
      observer.unobserve(entry.target);
    });
  }, {threshold:0.08,rootMargin:'0px 0px 45px 0px'});
  targets.forEach(target => {
    target.classList.add('is-motion-ready');
    observer.observe(target);
  });
})();

(() => {
  const fan = document.querySelector('.inkphase-gallery-fan');
  if (!fan || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const cards = [...fan.querySelectorAll('.inkphase-gallery-image')];
  if (cards.length < 2) return;
  let offset = 0;
  let visible = false;
  let paused = false;
  const edgeSlot = Math.floor(cards.length / 2);
  const shuffle = () => {
    offset = (offset + 1) % cards.length;
    cards.forEach((card, index) => {
      let slot = (index - Math.floor(cards.length / 2) - offset + cards.length) % cards.length;
      if (slot > Math.floor(cards.length / 2)) slot -= cards.length;
      if (Number(card.dataset.slot) === -edgeSlot && slot === edgeSlot) {
        card.classList.add('is-recycling');
        card.dataset.slot = String(slot);
        requestAnimationFrame(() => requestAnimationFrame(() => card.classList.remove('is-recycling')));
      } else card.dataset.slot = String(slot);
    });
  };
  const observer = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; }, {threshold:.2});
  observer.observe(fan);
  fan.addEventListener('pointerenter', () => { paused = true; });
  fan.addEventListener('pointerleave', () => { paused = false; });
  setInterval(() => { if (visible && !paused && !document.hidden) shuffle(); }, 2900);
})();
