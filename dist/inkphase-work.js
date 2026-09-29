(() => {
  const root=document.getElementById('selected-work');
  if(!root)return;
  const list=root.querySelector('[data-work-list]');
  const cards=[...list.querySelectorAll('.inkphase-work-card')];
  const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
  root.querySelectorAll('[data-work-layout]').forEach(button=>button.addEventListener('click',()=>{
    const isList=button.dataset.workLayout==='list';
    if(list.classList.contains('is-list')===isList)return;
    const before=cards.map(card=>card.getBoundingClientRect());
    cards.forEach(card=>card.getAnimations().forEach(animation=>animation.cancel()));
    list.classList.toggle('is-list',isList);
    if(!isList)list.scrollLeft=0;
    root.querySelectorAll('[data-work-layout]').forEach(control=>{
      const active=control===button;
      control.classList.toggle('is-active',active);
      control.setAttribute('aria-pressed',String(active));
    });
    if(!reducedMotion.matches){
      cards.forEach((card,index)=>{
        const from=before[index],to=card.getBoundingClientRect();
        // Moving each actual card between its two layouts creates a continuous morph.
        const dx=from.left-to.left,dy=from.top-to.top;
        const sx=from.width/to.width,sy=from.height/to.height;
        if(!Number.isFinite(sx)||!Number.isFinite(sy))return;
        card.animate([
          {transform:`translate(${dx}px,${dy}px) scale(${sx},${sy})`,opacity:.78},
          {transform:'translate(0,0) scale(1,1)',opacity:1}
        ],{duration:700,easing:'cubic-bezier(.22,1,.36,1)'});
      });
    }
  }));

})();
