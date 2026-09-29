(() => {
  const template = document.getElementById('inkphase-services-template');
  const initialized = new WeakSet();
  let scheduled = false;

  function activate(section) {
    if (initialized.has(section)) return;
    initialized.add(section);
    const buttons = [...section.querySelectorAll('[data-services-view]')];
    const panels = [...section.querySelectorAll('[data-services-panel]')];
    buttons.forEach(button => button.addEventListener('click', () => {
      const view = button.dataset.servicesView;
      buttons.forEach(item => {
        const selected = item === button;
        item.classList.toggle('is-active', selected);
        item.setAttribute('aria-pressed', String(selected));
      });
      panels.forEach(panel => {
        const selected = panel.dataset.servicesPanel === view;
        panel.classList.toggle('is-active', selected);
        panel.setAttribute('aria-hidden', String(!selected));
        panel.inert = !selected;
      });
    }));
  }

  function ensure() {
    if (!document.querySelector('section.inkphase-services') && template) {
      const original = document.querySelector('section.framer-1h97iyt');
      if (original) {
        const holder = document.createElement('div');
        holder.innerHTML = template.textContent;
        original.after(holder.firstElementChild);
      }
    }
    document.querySelectorAll('section.inkphase-services').forEach(activate);
  }

  ensure();
  new MutationObserver(() => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { scheduled = false; ensure(); });
  }).observe(document.getElementById('main') || document.body, { childList:true, subtree:true });
})();
