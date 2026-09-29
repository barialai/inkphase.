(() => {
  const form = document.getElementById('inkphase-contact-form');
  if (!form) return;
  const steps = [...form.querySelectorAll('.wizard-step')];
  const bars = [...form.querySelectorAll('.wizard-progress i')];
  const back = form.querySelector('.wizard-back');
  const skip = form.querySelector('.wizard-skip');
  const next = form.querySelector('.wizard-next');
  const finish = form.querySelector('.wizard-finish');
  const download = form.querySelector('.wizard-download');
  const emailDraft = form.querySelector('.wizard-email');
  const error = form.querySelector('.wizard-error');
  const result = form.querySelector('.wizard-result');
  const summary = form.querySelector('#brief-summary');
  const amount = form.querySelector('.budget-amount');
  const details = {projectType:'', services:[], description:'', timeline:'', budget:'', budgetRange:'', name:'', email:'', company:''};
  let active = 0;
  function show(step) {
    active = Math.max(0,Math.min(steps.length-1,step));
    form.classList.toggle('is-compact',active===0);
    steps.forEach((item,index) => {item.hidden = index !== active; item.classList.toggle('is-active',index === active)});
    bars.forEach((item,index) => {item.classList.toggle('active',index === active);item.classList.toggle('done',index < active)});
    form.querySelector('.wizard-progress').setAttribute('aria-label',`Step ${active+1} of ${steps.length}`);
    back.hidden = active === 0;
    skip.hidden = active !== 1 && active !== 3 && active !== 4;
    next.hidden = active === 0 || active === 3 || (active === 4 && details.budget !== 'I have a budget') || active === steps.length-1;
    finish.hidden = active !== steps.length-1;
    download.hidden = active !== steps.length-1;
    emailDraft.hidden = active !== steps.length-1 || !form.dataset.recipient;
    error.hidden = true;
    result.hidden = true;
    if (active === 5) updateSummary();
    const heading = steps[active].querySelector('h2');
    if (step !== 0) heading.focus({preventScroll:true});
  }
  steps.forEach(step => step.querySelector('h2').setAttribute('tabindex','-1'));
  function fail(message,field) {error.textContent=message;error.hidden=false;field?.focus();}
  function valid() {
    if (active === 0 && !details.projectType) {fail('Choose a project type to continue.');return false;}
    if (active === 2) {const field=form.elements.description; if(!field.value.trim()){fail('Tell me a little about the project.',field);return false;}details.description=field.value.trim();}
    if (active === 5) {for (const key of ['name','email']) {const field=form.elements[key];if (!field.value.trim() || !field.checkValidity()){fail(key==='email'?'Enter a valid email address.':'Add your name.',field);return false;}details[key]=field.value.trim();}details.company=form.elements.company.value.trim();}
    return true;
  }
  form.querySelectorAll('[data-field]').forEach(button => button.addEventListener('click',() => {
    const field=button.dataset.field;
    details[field]=button.dataset.value;
    form.querySelectorAll(`[data-field="${field}"]`).forEach(item => item.classList.toggle('is-selected',item===button));
    if(field==='budget') {
      amount.hidden=details.budget!=='I have a budget';
      if(details.budget==='I have a budget') {next.hidden=false;error.hidden=true;form.elements.budgetRange.focus();return;}
    }
    if(field==='budget' || field==='timeline' || field==='projectType') show(active+1);
  }));
  form.querySelectorAll('[data-service]').forEach(button => button.addEventListener('click',() => {
    button.setAttribute('aria-pressed',button.getAttribute('aria-pressed')==='true'?'false':'true');
    details.services=[...form.querySelectorAll('[data-service][aria-pressed="true"]')].map(item=>item.dataset.service);
  }));
  next.addEventListener('click',()=>{if(valid())show(active+1)});
  back.addEventListener('click',()=>show(active-1));
  skip.addEventListener('click',()=>show(active+1));
  function updateSummary() {
    const entries=[['Type',details.projectType],['Scope',details.services.join(', ')||'To discuss'],['Timing',details.timeline||'Flexible'],['Budget',details.budget==='I have a budget'?(form.elements.budgetRange.value.trim()||'To discuss'):details.budget||'To discuss']];
    summary.replaceChildren();
    entries.forEach(([label,value])=>{const line=document.createElement('div');const strong=document.createElement('strong');strong.textContent=label+': ';line.append(strong,document.createTextNode(value));summary.append(line)});
  }
  function brief() {
    details.budgetRange=form.elements.budgetRange.value.trim();
    return `INKPHASE — PROJECT BRIEF\n\nName: ${details.name}\nEmail: ${details.email}\nBrand / company: ${details.company||'Not provided'}\nProject type: ${details.projectType||'Not specified'}\nCapabilities: ${details.services.join(', ')||'To discuss'}\nTimeframe: ${details.timeline||'Flexible'}\nBudget: ${details.budgetRange||details.budget||'To discuss'}\n\nProject details:\n${details.description}\n`;
  }
  emailDraft.addEventListener('click',event=>{
    if(!valid()){event.preventDefault();return;}
    const subject=encodeURIComponent('Inkphase project enquiry');
    emailDraft.href=`mailto:${form.dataset.recipient}?subject=${subject}&body=${encodeURIComponent(brief())}`;
  });
  download.addEventListener('click',()=>{
    if(!valid())return;
    const blob=new Blob([brief()],{type:'text/plain'});
    const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download='inkphase-project-brief.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    result.textContent='Your brief was downloaded as a text file.';result.hidden=false;
  });
  finish.addEventListener('click',async()=>{
    if(!valid())return;
    const text=brief();
    try {await navigator.clipboard.writeText(text);result.textContent='Brief copied. You can paste it into an email or save it for later.';result.hidden=false;finish.textContent='Copied';}
    catch {const blob=new Blob([text],{type:'text/plain'});const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download='inkphase-project-brief.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);result.textContent='Your brief was downloaded as a text file.';result.hidden=false;}
  });
  document.querySelectorAll('[data-explore-service]').forEach(link => link.addEventListener('click', event => {
    const target=form.querySelector('[data-service="'+link.dataset.exploreService+'"]');
    if (!target) return;
    event.preventDefault();
    details.projectType='Paid project';
    form.querySelectorAll('[data-field="projectType"]').forEach(button=>button.classList.toggle('is-selected',button.dataset.value==='Paid project'));
    form.querySelectorAll('[data-service]').forEach(button=>button.setAttribute('aria-pressed',String(button===target)));
    details.services=[link.dataset.exploreService];
    show(1);
    form.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'center'});
  }));
  form.addEventListener('submit',event=>event.preventDefault());
  const email=new URLSearchParams(location.search).get('email');
  if(email)form.elements.email.value=email;
  show(0);
})();
