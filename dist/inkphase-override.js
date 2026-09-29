/* Keeps the saved reference layout and motion while adapting Framer's client rendering. */
(() => {
  const raw = document.getElementById('inkphase-overrides');
  if (!raw) return;
  const config = JSON.parse(raw.textContent);
  const replacements = config.general;
  const projects = config.projects;
  document.body.classList.add('inkphase-site-gradient');
  if (config.route === '/') {
    document.body.classList.add('inkphase-showcase-home');
    const anchorIds = {'framer-1s21fwr':'about','framer-1h97iyt':'services'};
    Object.entries(anchorIds).forEach(([klass,id])=>document.querySelector(`.${klass}`)?.setAttribute('id',id));
  }
  if (config.route === '/contact-me') {
    const email = new URLSearchParams(location.search).get('email');
    if(email) {
      const field=document.querySelector('input[type="email"]');
      if(field && !field.value) field.value=email;
    }
  }
  const sourceImages = {
    GktRoQc:'monogram', iIQm7S1:'monogram', yblJfy:'hero', '0LORqw':'portrait', l7Hz4:'process', wibOh8:'accent'
  };
  const mainProjectImages = {
    '9B8mlXJZLALXTigbl6dDwjNOgM.jpg':'bloom',
    'P2aCEizwIBi5sHsZjvaWC9BWqU.jpg':'roast',
    'NhwFgMbGy8jZyuTdbPttTUyzCs.jpg':'wildly',
    'GqG9IYSRzFo9zjj8up2ugSowK8.jpg':'lumen'
  };
  function setLetters(el,value){
    const walk=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);const nodes=[];while(walk.nextNode())nodes.push(walk.currentNode);
    if(!nodes.length)return;
    if(nodes.length===1){if(nodes[0].nodeValue!==value)nodes[0].nodeValue=value;return}
    let pos=0;nodes.forEach((n,i)=>{let count=i===nodes.length-1?value.length-pos:n.nodeValue.length;let next=value.slice(pos,pos+count);pos+=count;if(n.nodeValue!==next)n.nodeValue=next})
  }
  function smallMatch(el,value){return [...el.children].some(child=>child.textContent.trim()===value)}
  function swapText(){
    document.querySelectorAll('p,h1,h2,h3,h4,span,div').forEach(el=>{
      const before=el.textContent.trim();const after=replacements[before];
      if(after!==undefined&&!smallMatch(el,before))setLetters(el,after)
    });
    projects.forEach(p=>document.querySelectorAll(`a[href*="/projects/${p.slug}"]`).forEach(a=>{
      const h=a.querySelector('h3');if(!h)return;setLetters(h,p.label);
      [...a.querySelectorAll('p')].slice(0,3).forEach((el,i)=>setLetters(el,[p.category,p.scope,p.year][i]));
    }));
    const h2=[...document.querySelectorAll('h2')];
    if(config.route==='/'){
      const homeH2=[...document.querySelectorAll('.framer-hoNGa h2')];
      config.homeHeadings.forEach((group,index)=>homeH2.slice(index*6,index*6+6).forEach((el,i)=>setLetters(el,group[i])));
    }
    h2.forEach((el,index)=>{
      if(index+5<h2.length&&h2.slice(index,index+6).map(x=>x.textContent.trim()).join('|')==="Let's|design|your|next|great|package")
        h2.slice(index,index+6).forEach((word,i)=>setLetters(word,config.footerWords[i]));
    });
    if(config.route==='/'){
      const hero=document.querySelectorAll('.framer-kblsb4 h1');
      if(hero[0])setLetters(hero[0],config.hero.firstLine);
      if(hero[1])setLetters(hero[1],config.hero.secondLine);
    }
    if(config.route.startsWith('/projects/')){
      const slug=config.route.split('/')[2],p=projects.find(x=>x.slug===slug);
      if(p){document.querySelectorAll('h1').forEach(h=>setLetters(h,p.label));
        const paras=[...document.querySelectorAll('p')];
        paras.forEach((el,i)=>{
          const t=el.textContent.trim();
          if(t==='Service'&&paras[i+1])setLetters(paras[i+1],p.category);
          if(t==='Year'&&paras[i+1])setLetters(paras[i+1],p.year);
          if(t==='Timeline'&&paras[i+1])setLetters(paras[i+1],p.scope);
          if(t==='Client'&&paras[i+1])setLetters(paras[i+1],'Add client');
        });
        const replacements=["PORTFOLIO PREVIEW — I’ll add the brief, visuals and outcome of a real project here once it’s ready to share.","This page is a preview of the project layout. The images are reference visuals, not work I’m claiming as mine.","I’ll share the real brief, my role and the challenge when this project is ready to publish.","I’ll show the thinking, creative decisions and production process behind the finished work.","The final deliverables and approved outcome will appear here with the real project images."];
        [3,13,16,17,18].forEach((index,i)=>{if(paras[index])setLetters(paras[index],replacements[i])});
        if(paras[14])setLetters(paras[14],'Inkphase');
      }
    }
  }
  function imageTarget(source){
    let m=source.match(/(?:\/assets\/|\/images\/)([^?]+)/);if(!m)return null;let name=m[1];
    let slug=mainProjectImages[name];let project=projects.find(p=>p.slug===slug);
    if(project&&project.image)return project.image;
    let role=Object.entries(sourceImages).find(([prefix])=>name.startsWith(prefix))?.[1] || 'project';
    if(config.route.startsWith('/projects/')&&role==='project'){
      const active=projects.find(p=>p.slug===config.route.split('/')[2]);if(active?.image)return active.image;
    }
    if(role==='hero'&&config.hero.image)return config.hero.image;
    if(role==='portrait'&&config.about.portrait)return config.about.portrait;
    return role==='monogram'?'/assets/placeholder-monogram.svg':`/assets/${name}`;
  }
  function swapImages(){
    document.querySelectorAll('img').forEach(img=>{
      const src=img.getAttribute('src')||'';if(src.includes('/placeholder-'))return;
      const target=imageTarget(src);if(!target)return;
      img.removeAttribute('srcset');img.removeAttribute('sizes');img.setAttribute('src',target);
      img.setAttribute('alt',target.includes('placeholder-')?'Inkphase monogram':'Reference visual; replace with Inkphase work or portrait');
      const role=Object.entries(sourceImages).find(([prefix])=>src.includes(prefix))?.[1];
      if((role==='hero'&&!config.hero.image)||(role==='portrait'&&!config.about.portrait))img.parentElement?.setAttribute('data-inkphase-reference','portrait');
    });
  }
  function swapLinks(){
    document.querySelectorAll('a[href]').forEach(a=>{
      const href=a.getAttribute('href');
      if(href==='/projects/'||href==='/projects')a.setAttribute('href','/work/');
      if(href?.startsWith('mailto:hellomartin'))a.setAttribute('href',config.contact.email?'mailto:'+config.contact.email:'/contact-me/');
      if(href?.startsWith('tel:+001'))a.setAttribute('href','/contact-me/');
      const social={'https://x.com/home':config.contact.other,'https://www.instagram.com/':config.contact.instagram,'https://dribbble.com/':config.contact.linkedin};
      if(Object.prototype.hasOwnProperty.call(social,href)){
        if(social[href])a.setAttribute('href',social[href]);else{a.removeAttribute('href');a.setAttribute('aria-label','Social link to add')}
      }
    });
  }
  let scheduled=false,active=false;
  function apply(){if(active)return;active=true;document.getElementById('__framer-badge-container')?.remove();swapText();swapImages();swapLinks();if(config.route==='/'){document.querySelector('.framer-1s21fwr')?.setAttribute('id','about');document.querySelector('.framer-1h97iyt')?.setAttribute('id','services')}if(config.route==='/contact-me'){const email=new URLSearchParams(location.search).get('email'),field=document.querySelector('input[type="email"]');if(email&&field&&!field.value)field.value=email}active=false}
  const observer=new MutationObserver(()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;apply()})});
  apply();observer.observe(document.body,{subtree:true,childList:true,characterData:true});
  document.addEventListener('submit',async event=>{
    const form=event.target;if(!form.matches('form'))return;
    event.preventDefault();event.stopImmediatePropagation();
    const values=new FormData(form);
    const brief=`Inkphase project inquiry\nName: ${values.get('Full Name')||''}\nEmail: ${values.get('Email Address')||''}\nProject type: ${values.get('Select Budget')||''}\nMessage: ${values.get('Message')||''}`;
    if(config.contact.email){location.href=`mailto:${encodeURIComponent(config.contact.email)}?subject=${encodeURIComponent('Inkphase project inquiry')}&body=${encodeURIComponent(brief)}`;return}
    const notice=form.querySelector('[data-inkphase-status]')||document.createElement('p');notice.dataset.inkphaseStatus='';notice.style.cssText='font-size:13px;line-height:1.5;color:#616161;margin-top:8px';
    try{await navigator.clipboard.writeText(brief);notice.textContent='Project brief copied. Add your contact email to receive inquiries directly.'}catch{notice.textContent='Add a contact email to enable inquiries.'}
    if(!notice.isConnected)form.append(notice)
  },true);
})();
