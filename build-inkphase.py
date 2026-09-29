"""Apply editable Inkphase content to the saved Martin Luke layout.

Edit inkphase-content.json, then run: python build-inkphase.py
The reference markup and Framer layout/motion remain in reference-pages/.
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from lxml import etree, html

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "inkphase-content.json").read_text())
WORK_GALLERY = json.loads((ROOT / "work-gallery.json").read_text())
SOURCE = ROOT / "reference-pages"
OUTPUT = ROOT / "dist"
WORK_REFERENCE_IMAGES = [
    'P56kWpIGh7vjWbo1RqSRcPXSIpQ.jpg',
    '9B8mlXJZLALXTigbl6dDwjNOgM.jpg',
    'SRmctLTbJyK9iZbfya63L6Q1wI.jpg',
    'GqG9IYSRzFo9zjj8up2ugSowK8.jpg',
    'MTA6quctFkp70IsF4Yn0eMP4kI.jpg',
]

def work_image(item,index):
    return item.get('image') or '/assets/'+WORK_REFERENCE_IMAGES[index % len(WORK_REFERENCE_IMAGES)]

GENERAL = {
    "Martin Luke": "Inkphase",
    "Martin": "Barialai",
    "Bloom": "Project 01", "Roast": "Project 02", "Wildly": "Project 03", "Lumen": "Project 04", "Forge": "Project 05",
    "👋  Hey, I'm Martin": DATA["hero"]["greeting"],
    "Martin Luke - Packaging Designer": "Inkphase — Barialai Nawabi",
    "👋 Hey, I'm Martin": DATA["hero"]["greeting"],
    "Packaging": DATA["hero"]["firstLine"],
    "I craft packaging that turns everyday products into unforgettable, shelf-stopping brand experiences people love.": DATA["hero"]["description"],
    "Hey, I'm Martin — a packaging designer who believes great design should do more than look good, it should make people stop, pick up, and remember. Over the past few years, I've worked with brands across skincare, coffee, snacks, and home fragrance, helping them turn simple products into shelf-stopping experiences.": DATA["about"]["firstParagraph"],
    "My process blends strategy with craft: understanding a brand's story first, then translating it into packaging that feels intentional in every detail, from material to typography. I care about the small things most people overlook, because those small things are usually what make someone choose one box over another.": DATA["about"]["secondParagraph"],
    "Adobe illustrator": "Branding & design", "Dieline & vector design": "Identity & campaign design",
    "Photoshop": "Video & motion", "Mockups & retouching": "Editing & motion graphics",
    "Figma": "AI-assisted production", "Layout & collaboration": "Directed concepts & visuals",
    "Blender": "Performance creative", "3D packaging renders": "Ads & platform assets",
    "Senior Packaging Designer": "5+ years of experience", "Zenpack Studio": "Design, video & AI production",
    "2023 — Present": "Creative practice", "Brand & Packaging Designer": "174+ projects delivered",
    "Forge Creative Co.": "Across multiple industries", "2021 — 2023": "Project experience",
    "Junior Graphic Designer": "Master of Computer Applications", "Studio Verve": "Goa University",
    "2019 — 2021": "Education",
    "Discover & Research": "Understand & Research",
    "I dive into your brand, audience, and market to uncover insights that shape a strong, purposeful creative direction.": "I begin with what you want to communicate, who needs to hear it and where the work will live.",
    "Design & Refine": "Create & Refine",
    "I explore concepts, test materials and finishes, refining every detail until the packaging feels effortless.": "I test ideas across design, video and motion, using AI where it helps me explore faster. Then I refine what works.",
    "Deliver & Launch": "Deliver & Adapt",
    "I finalize production-ready files and mockups, ensuring your packaging translates flawlessly onto the shelf.": "I deliver the right files for each platform and format, with the details ready for real use.",
    "Packaging Design": "Branding & design",
    "Complete packaging systems that make your product impossible to ignore on any shelf.": "I build identities and design systems that carry through campaigns, social content, and digital or print work.",
    "Dieline Structure": "Visual identity", "Material Selection": "Brand systems", "Print Finishing": "Campaign design",
    "Brand Identity": "Video & motion",
    "Full visual identity systems built to make your brand instantly recognizable and trustworthy.": "I edit video and make motion that serves the idea, whether it lives in a campaign, a feed or a longer story.",
    "Logo Design": "Video editing", "Color System": "Motion graphics", "Brand Guidelines": "Platform content",
    "Label Design": "AI-assisted production",
    "Eye-catching label designs crafted to grab attention fast on crowded retail shelves.": "I use AI to explore concepts and produce visuals, then direct, edit and refine the result myself.",
    "Layout Design": "Concept exploration", "Typography System": "Visual production", "Print Prep": "Human direction",
    "Starting from": "Flexible scope", "$1500–$3000": "By brief", "$2000–$4000": "By brief", "$800–$1800": "By brief",
    "Testimonials": "Practice",
    '"Martin transformed our packaging into something customers actually notice and remember, giving Bloom a genuinely premium, trustworthy shelf presence instantly."': 'I build identities that give a brand a clear look and a consistent voice across channels.',
    '"Working with Martin gave Ember an identity that finally matched the passion and craft behind every single roast."': 'I edit for rhythm, meaning and the platform where people will actually watch.',
    '"Martin delivered fast, fun, functional labels that made Nomad impossible to overlook on crowded, competitive retail shelves everywhere."': 'I use AI to widen the search for ideas, then make the creative decisions myself.',
    '"Martin created packaging that feels as calming as our candles themselves, elevated, thoughtful, and genuinely giftable every time."': 'I make ads that earn attention and stay focused on the campaign goal.',
    '"Martin gave Ridgeline an identity that instantly built trust, exactly what we needed as a brand-new company."': 'I connect the details so a story feels like the same brand wherever it appears.',
    '"Martin\'s attention to detail and strategic thinking turned our packaging into a genuine competitive advantage within our entire category."': 'I have worked across trading, crypto, real estate, education, hospitality and digital media, and I am open to other fields.',
    "Sarah Chen": "Branding & design", "Founder & CEO, Bloom": "Capability",
    "David Okafor": "Video & motion", "Founder & Roaster, Ember": "Capability",
    "Priya Nair": "AI-assisted production", "Co-Founder, Nomad": "Capability",
    "Elena Vasquez": "Performance creative", "Creative Director, Solace": "Capability",
    "Marcus Reid": "Creative direction", "CEO, Ridgeline": "Capability",
    "Aisha Thornton": "Industry experience", "Marketing Director, Halcyon": "Experience",
    "Have a product that deserves better packaging? Let's collaborate and turn your idea into something unforgettable.": "Tell me what you're building and where you want it to go. I can help find the visual direction that brings it together.",
    "Email Address": "Email address", "Phone Number": "Direct contact",
    "hellomartin@gmail.com": DATA['contact']['email'] or "Email to add", "+001 234 567 890": "Details coming soon",
    "A collection of packaging projects designed to help brands stand out and feel unforgettable.": "I'm preparing a selection of real design, video and motion projects. The visuals here are temporary previews until the work is ready to share.",
    "Select Budget": "Project type", "$2K-$5K": "Branding & design", "$5K-$7K": "Video & motion",
    "$10K-$15K": "AI-assisted production", "Custom": "Other creative work",
    "Have a project in mind? Reach out and let's design something worth remembering together.": "Have something in mind? Tell me what you need, what it should achieve and when you want to start.",
    "Projects": "Work", "All Projects": "All work", "All projects": "All work", "View projects": "View work"
}

HOME_H2 = [
    ["Selected", "work", "across", "brand", "and", "motion"],
    ["The", "person", "and", "practice", "behind", "Inkphase"],
    ["From", "first", "thought", "to", "final", "delivery"],
    ["Creative", "support", "for", "ideas", "in", "motion"],
    ["What", "I", "bring", "to", "every", "project"],
]
FOOTER_WORDS = ["Let's", "shape", "your", "next", "bold", "idea"]

def text_of(element):
    if not isinstance(element.tag,str):return ''
    return ''.join(element.itertext()).strip()

def assign(element, value):
    """Preserve Framer's letter spans and their individual motion."""
    nodes = [node for node in element.xpath('.//text()') if str(node)]
    if not nodes:
        element.text = value
        return
    if len(nodes) == 1:
        node = nodes[0]
        setattr(node.getparent(), 'tail' if node.is_tail else 'text', value)
        return
    pos = 0
    for i,node in enumerate(nodes):
        old = str(node)
        take = len(old) if i < len(nodes)-1 else len(value)-pos
        new = value[pos:pos+take]
        pos += take
        setattr(node.getparent(), 'tail' if node.is_tail else 'text', new)

def replace_exact(root, old, new):
    found = []
    for el in root.iter():
        if not isinstance(el.tag,str) or el.tag in ('script','style') or text_of(el) != old: continue
        if any(text_of(child) == old for child in el): continue
        found.append(el)
    for el in found: assign(el,new)
    return len(found)

def image_role(name):
    if name.startswith('GktRoQc') or name.startswith('iIQm7S1'):return 'monogram'
    if name.startswith('yblJfy'):return 'hero'
    if name.startswith('0LORq'):return 'portrait'
    if name.startswith('l7Hz4'):return 'process'
    if name.startswith('wibOh8'):return 'accent'
    return 'project'

def asset_for(name,route):
    role=image_role(name)
    if role=='hero' and DATA['hero']['image']:return DATA['hero']['image']
    if role=='portrait' and DATA['about']['portrait']:return DATA['about']['portrait']
    if route.startswith('/projects/') and role=='project':
        item=next(p for p in DATA['projects'] if p['slug']==route.split('/')[2])
        if item['image']:return item['image']
    project_names={'9B8mlXJZLALXTigbl6dDwjNOgM.jpg':'bloom','P2aCEizwIBi5sHsZjvaWC9BWqU.jpg':'roast','NhwFgMbGy8jZyuTdbPttTUyzCs.jpg':'wildly','GqG9IYSRzFo9zjj8up2ugSowK8.jpg':'lumen'}
    slug=project_names.get(name)
    if slug:
        item=next(p for p in DATA['projects'] if p['slug']==slug)
        if item['image']:return item['image']
    if role=='monogram':return '/assets/placeholder-monogram.svg'
    return '/assets/'+name

def image_attrs(root,route):
    for img in root.xpath('//img'):
        source=img.get('src','')
        match=re.search(r'/assets/([^?]+)',source)
        if not match:continue
        dest=asset_for(match.group(1),route)
        img.set('src',dest)
        img.attrib.pop('srcset',None)
        img.attrib.pop('sizes',None)
        img.set('alt','Inkphase monogram' if 'placeholder' in dest else 'Reference visual; replace with Inkphase work or portrait')
        if image_role(match.group(1)) in ('hero','portrait') and not (DATA['hero']['image'] if image_role(match.group(1))=='hero' else DATA['about']['portrait']):
            img.getparent().set('data-inkphase-reference','portrait')
    for el in root.xpath('//*[@style]'):
        style=el.get('style')
        for name in set(re.findall(r'/assets/([A-Za-z0-9_-]+\.(?:png|jpg|jpeg|webp|svg))',style)):
            style=style.replace('/assets/'+name,asset_for(name,route))
        el.set('style',style)

def cards(root):
    for item in DATA['projects']:
        for a in root.xpath('//a[contains(@href,"/projects/'+item['slug']+'")]'):
            heading=a.find('.//h3')
            if heading is None:continue
            assign(heading,item['label'])
            tags=a.xpath('.//p')[:3]
            for el,value in zip(tags,(item['category'],item['scope'],item['year'])):assign(el,value)

def detail(root,slug):
    item=next(p for p in DATA['projects'] if p['slug']==slug)
    for h in root.xpath('//h1'):
        if text_of(h).lower()==slug:assign(h,item['label'])
    paragraphs=[p for p in root.xpath('//p') if len(text_of(p))>70]
    if paragraphs:
        assign(paragraphs[0],"PORTFOLIO PREVIEW — I’ll add the brief, visuals and outcome of a real project here once it’s ready to share.")
    if len(paragraphs)>1:
        assign(paragraphs[1],"This page is a preview of the project layout. The images are reference visuals, not work I’m claiming as mine.")
    for p,value in zip(paragraphs[2:5],[
        "I’ll share the real brief, my role and the challenge when this project is ready to publish.",
        "I’ll show the thinking, creative decisions and production process behind the finished work.",
        "The final deliverables and approved outcome will appear here with the real project images."
    ]):assign(p,value)
    for p in root.xpath('//p'):
        t=text_of(p)
        if t in ('2025','2024'):assign(p,item['year'])
        elif t in ('3 Weeks','4 Weeks','2 Weeks','5 Weeks'):assign(p,item['scope'])
        elif t in ('Packaging Design','Brand Identity','Label Design'):assign(p,item['category'])
        elif t in ('Verde','Ember','Nomad','Solace','Ridgeline'):assign(p,'Add client')
        elif t in ('Sarah Chen','David Okafor','Priya Nair','Elena Vasquez','Marcus Reid'):assign(p,'Inkphase')
        elif t in ('Founder & CEO','Founder & Roaster','Co-Founder','Creative Director','CEO'):assign(p,'Project slot')
    ps=root.xpath('//p')
    for index,p in enumerate(ps[:-1]):
        if text_of(p)=='Service':assign(ps[index+1],item['category'])
    for p in ps:
        if text_of(p) in ('Branding & design','Video & motion','AI-assisted production') and p is not ps[6]:
            # The former testimonial author becomes a neutral project label.
            if p.getparent() is not ps[6].getparent():assign(p,'Inkphase')

def page_specific(root,route):
    if route in ('/','/about'):
        heads=root.xpath('//h1')
        for el,value in zip(heads,(DATA['hero']['firstLine'],DATA['hero']['secondLine'])):assign(el,value)
        h2=root.xpath('//h2')
        for group,values in enumerate(HOME_H2):
            for el,value in zip(h2[group*6:group*6+6],values):assign(el,value)
    if route.startswith('/projects/'):
        detail(root,route.split('/')[2])
    if route=='/projects':
        h1=root.xpath('//h1')
        for el,value in zip(h1,['Inkphase','portfolio']):assign(el,value)
    h2=root.xpath('//h2')
    for i in range(len(h2)-5):
        if [text_of(x) for x in h2[i:i+6]]==["Let's",'design','your','next','great','package']:
            for el,value in zip(h2[i:i+6],FOOTER_WORDS):assign(el,value)
    cards(root)
    for option,value in zip(root.xpath('//select/option')[1:],['Branding & design','Video & motion','AI-assisted production','Other creative work']):
        option.text=value;option.set('value',value)
    for field in root.xpath('//input[@placeholder]'):
        if field.get('placeholder')=='hellomartin@gmail.com':field.set('placeholder','you@example.com')
        if field.get('placeholder')=='Jane Smith':field.set('placeholder','Your name')

def make_page(source,route_override=None):
    route=route_override or ('/' if source.parent==SOURCE else '/'+str(source.parent.relative_to(SOURCE)))
    root=html.fromstring(source.read_text())
    for old,new in GENERAL.items():replace_exact(root,old,new)
    page_specific(root,route)
    image_attrs(root,route)
    for a in root.xpath('//a[@href]'):
        href=a.get('href')
        if href in ('/projects','/projects/'):
            a.set('href','/work/')
            continue
        if href in ('/#about','#about'):
            a.set('href','/about/')
            continue
        if href.startswith('mailto:hellomartin'):
            a.set('href','mailto:'+DATA['contact']['email'] if DATA['contact']['email'] else '/contact-me/')
        elif href.startswith('tel:+001'):a.set('href','/contact-me/')
        elif href in ('https://x.com/home','https://www.instagram.com/','https://dribbble.com/'):
            replacement={'https://x.com/home':DATA['contact']['other'],'https://www.instagram.com/':DATA['contact']['instagram'],'https://dribbble.com/':DATA['contact']['linkedin']}[href]
            if replacement:a.set('href',replacement)
            else:a.attrib.pop('href',None);a.set('aria-label','Social link to add')
    route_label='Home' if route=='/' else (next(p['label'] for p in DATA['projects'] if p['slug']==route.split('/')[-1]) if route.startswith('/projects/') else route.strip('/').replace('/',' · ').title())
    for title in root.xpath('//title'):title.text='Inkphase — '+route_label
    for meta in root.xpath('//meta[@name="description"]'):meta.set('content','Inkphase is the independent creative practice of Barialai Nawabi across brand, video, motion and AI-assisted production.')
    for meta in root.xpath('//meta[@property="og:title"]|//meta[@name="twitter:title"]'):meta.set('content','Inkphase — '+route_label)
    for meta in root.xpath('//meta[@property="og:description"]|//meta[@name="twitter:description"]'):meta.set('content','The creative practice of Barialai Nawabi.')
    for meta in root.xpath('//meta[@property="og:image"]|//meta[@name="twitter:image"]'):meta.getparent().remove(meta)
    for link in root.xpath('//link[@rel="icon"]'):link.set('href','/assets/placeholder-monogram.svg')
    # The original form belongs to the template owner. Keep its visual design, but prepare a local brief instead.
    if route=='/contact-me' and not DATA['contact']['email']:
        form=root.xpath('//form')
        if form:
            notice=html.Element('p',style='font-size:13px;line-height:1.5;color:#616161;margin-top:8px')
            notice.text='Contact email needed — this form copies your brief until I add my email.'
            form[0].append(notice)
    body=root.find('body')
    head=root.find('head')
    body.set('class',((body.get('class') or '')+' inkphase-site-gradient').strip())
    if route=='/about':body.set('class',((body.get('class') or '')+' inkphase-about-page').strip())
    if route=='/about':
        nav_markup=re.search(r'<nav class="inkphase-showcase-nav".*?</nav>',(ROOT/'showcase-hero.html').read_text(),re.S).group()
        about_nav=html.Element('div',{'class':'inkphase-showcase inkphase-about-navigation'})
        about_nav.append(html.fragment_fromstring(nav_markup))
        root.get_element_by_id('main').addprevious(about_nav)
        head.append(html.Element('link',rel='stylesheet',href='/inkphase-hero.css'))
    if route=='/':
        body.set('class',((body.get('class') or '')+' inkphase-showcase-home').strip())
        hero_template=(ROOT/'showcase-hero.html').read_text()
        for marker,key in (('{{headline1}}','showcaseHeadline1'),('{{headline2}}','showcaseHeadline2'),('{{description}}','showcaseDescription')):
            hero_template=hero_template.replace(marker,escape(DATA['hero'][key]))
        showcase=html.fragment_fromstring(hero_template)
        main=root.get_element_by_id('main')
        main.addprevious(showcase)
        cards_markup=[]
        for index,item in enumerate(DATA['selectedWork'],start=1):
            name=escape(item['name'])
            url=escape(item['url'],quote=True)
            kind=escape(item['type'])
            description=escape(item['description'])
            cards_markup.append(f'''<article class="inkphase-work-card inkphase-work-card-live tone-{index}"><span class="inkphase-work-card-orbit" aria-hidden="true"></span><span class="inkphase-work-card-icon" aria-hidden="true">{index:02d}</span><span class="inkphase-work-card-badge">LIVE WEBSITE</span><h3 class="inkphase-work-card-name">{name}</h3><div class="inkphase-work-card-number">{kind} <small>{index:02d} / {len(DATA['selectedWork']):02d}</small></div><p>{description}</p><a class="inkphase-work-card-link" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="View {name} live website">View live website</a></article>''')
        work_template=(ROOT/'selected-work.html').read_text().replace('{{WORK_CARDS}}',''.join(cards_markup))
        latest_template=(ROOT/'latest-project.html').read_text()
        projects_surface=html.Element('div',{'class':'inkphase-projects-surface'})
        projects_surface.append(html.fragment_fromstring(work_template))
        projects_surface.append(html.fragment_fromstring(latest_template))
        services_markup=(ROOT/'services-section.html').read_text()
        projects_surface.append(html.fragment_fromstring(services_markup))
        fan_positions=list(range(-(len(WORK_GALLERY['featured'])//2),len(WORK_GALLERY['featured'])//2+1))
        fan_images=[]
        image_by_id={item['id']:item for item in WORK_GALLERY['images']}
        for image_id,slot in zip(WORK_GALLERY['featured'],fan_positions):
            item=image_by_id[image_id]
            image_source=escape(item['image'],quote=True)
            fan_images.append(f'<span class="inkphase-gallery-image" data-slot="{slot}"><img src="{image_source}" alt=""></span>')
        gallery_markup=(ROOT/'work-gallery.html').read_text().replace('{{FAN_IMAGES}}',''.join(fan_images))
        projects_surface.append(html.fragment_fromstring(gallery_markup))
        contact_markup=(ROOT/'contact-page.html').read_text()
        contact_inner=re.search(r'(<div class="contact-intro">.*?</form>)',contact_markup,re.S).group(1)
        contact_inner=contact_inner.replace('{{CONTACT_EMAIL}}',escape(DATA['contact']['email'],quote=True))
        home_contact=html.fragment_fromstring('<section class="contact-main inkphase-home-contact" id="contact" aria-label="Start a project with Inkphase"><div class="contact-beam" aria-hidden="true"></div>'+contact_inner+'</section>')
        projects_surface.append(home_contact)
        projects_surface.append(html.fragment_fromstring((ROOT/'review-section.html').read_text()))
        main.addprevious(projects_surface)
        hero_css=html.Element('link',rel='stylesheet',href='/inkphase-hero.css')
        head.append(hero_css)
        head.append(html.Element('link',rel='stylesheet',href='/inkphase-work.css'))
        head.append(html.Element('link',rel='stylesheet',href='/inkphase-latest.css'))
        head.append(html.Element('link',rel='stylesheet',href='/inkphase-services.css'))
        head.append(html.Element('link',rel='stylesheet',href='/inkphase-gallery.css'))
        head.append(html.Element('link',rel='stylesheet',href='/inkphase-contact.css'))
        services_template=html.Element('script',type='text/html',id='inkphase-services-template')
        services_template.text=services_markup
        body.append(services_template)
    head.append(html.Element('link',rel='stylesheet',href='/inkphase-site-gradient.css'))
    if route in ('/','/about'):
        # Keep the same Framer sections and assets, but give About its own route.
        remove_on_home=('framer-1s21fwr','framer-1pdf24y','framer-m0yhsr','framer-1h97iyt','framer-1dln4dg','framer-kblsb4','framer-13fl2ty')
        remove_on_about=('framer-kblsb4','framer-13fl2ty','framer-1h97iyt','framer-1dln4dg')
        for section in root.xpath('//section|//header'):
            classes=(section.get('class') or '').split()
            if any(name in classes for name in (remove_on_home if route=='/' else remove_on_about)):
                section.getparent().remove(section)
    for badge in root.xpath('//*[@id="__framer-badge-container"]'):
        badge.getparent().remove(badge)
    head.append(html.Element('link',rel='stylesheet',href='/inkphase-typography.css'))
    if route=='/':head.append(html.Element('link',rel='stylesheet',href='/inkphase-laptop.css'))
    head.append(html.Element('link',rel='stylesheet',href='/inkphase-palette.css'))
    label_style=html.Element('style',id='inkphase-asset-labels')
    label_style.text='[data-inkphase-reference]::after{content:"REFERENCE VISUAL · REPLACE WITH YOUR PHOTO";position:absolute;bottom:12px;left:12px;z-index:10;background:#000;color:#fff;font:600 10px/1.3 Arial,sans-serif;letter-spacing:.08em;padding:7px 9px;max-width:calc(100% - 24px);pointer-events:none} [data-inkphase-reference]{position:relative} #__framer-badge-container,.__framer-badge{display:none!important} @media(max-width:600px){[data-inkphase-reference]::after{font-size:8px;bottom:7px;left:7px;padding:5px}}'
    head.append(label_style)
    config=html.Element('script',type='application/json',id='inkphase-overrides')
    config.text=json.dumps({'general':GENERAL,'projects':DATA['projects'],'hero':DATA['hero'],'about':DATA['about'],'contact':DATA['contact'],'route':route,'homeHeadings':HOME_H2,'footerWords':FOOTER_WORDS},ensure_ascii=False).replace('</','<\\/')
    body.append(config)
    script=html.Element('script',src='/inkphase-override.js')
    body.append(script)
    if route=='/':
        body.append(html.Element('script',src='/inkphase-laptop.js'))
        body.append(html.Element('script',src='/inkphase-work.js'))
        body.append(html.Element('script',src='/inkphase-latest.js'))
        body.append(html.Element('script',src='/inkphase-services.js'))
        body.append(html.Element('script',src='/inkphase-gallery.js'))
        body.append(html.Element('script',src='/inkphase-contact.js'))
    result=etree.tostring(root,encoding='unicode',method='html',doctype='<!doctype html>')
    # Framer's hydration data also contains image URLs. Point it at the same placeholders.
    for name in sorted(set(re.findall(r'/assets/([A-Za-z0-9_-]+\.(?:png|jpg|jpeg|webp|svg))',result))):
        if not name.startswith('placeholder-'):
            result=result.replace('/assets/'+name,asset_for(name,route))
    dest=OUTPUT/('about/index.html' if route=='/about' else str(source.relative_to(SOURCE)))
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(result)
    print(route,len(result))

for source in sorted(SOURCE.glob('**/index.html')):make_page(source)
make_page(SOURCE/'index.html',route_override='/about')

nav_markup=re.search(r'<nav class="inkphase-showcase-nav".*?</nav>',(ROOT/'showcase-hero.html').read_text(),re.S).group()
work_figures=[]
for item in WORK_GALLERY['images']:
    source=escape(item['image'],quote=True)
    alt=escape(item['alt'],quote=True)
    caption=escape(item['title'])
    work_figures.append(f'<figure class="inkphase-workpage-item"><img src="{source}" alt="{alt}" loading="lazy"><figcaption>{caption}</figcaption></figure>')
work_page=(ROOT/'work-page.html').read_text().replace('{{NAV}}',nav_markup).replace('{{WORK_IMAGES}}',''.join(work_figures))
work_dest=OUTPUT/'work/index.html';work_dest.parent.mkdir(parents=True,exist_ok=True);work_dest.write_text(work_page)
contact_page=(ROOT/'contact-page.html').read_text().replace('{{NAV}}',nav_markup).replace('{{CONTACT_EMAIL}}',escape(DATA['contact']['email'],quote=True))
contact_dest=OUTPUT/'contact-me/index.html';contact_dest.parent.mkdir(parents=True,exist_ok=True);contact_dest.write_text(contact_page)
