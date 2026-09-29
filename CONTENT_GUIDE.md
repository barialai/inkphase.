# Editing Inkphase

The homepage hero uses the dashboard-style design reference, with the original site sections and motion below it. The blue gradient continues across the other sections and pages, while the original footer is preserved. Edit hero headlines and description in **`inkphase-content.json`**. The hero layout lives in `showcase-hero.html`, with styles in `dist/inkphase-hero.css` and `dist/inkphase-site-gradient.css`.

The Selected Work homepage section uses `selected-work.html`, `dist/inkphase-work.css`, and `dist/inkphase-work.js`. Its five preview cards are generated from `inkphase-content.json.projects`, so project names and routes stay aligned with the Work page and case study placeholders. On desktop, three cards appear at once and the carousel advances slowly; it pauses on interaction and respects reduced-motion settings.

1. Add your actual portrait, hero visual, and project images to `dist/assets/`.
2. Update the text and image paths in `inkphase-content.json`. Image paths should start with `/assets/`, for example `/assets/my-project.jpg`.
3. Add your email to `contact.email` to turn the contact form into a prefilled email draft. Until then, the form copies the inquiry; it does not send anything.
4. Run `python build-inkphase.py` to apply edits across the original layout and all eight pages. Re-publish the site afterward.

The five project slots use the existing reference pages at `/projects/bloom/`, `/projects/roast/`, `/projects/wildly/`, `/projects/lumen/`, and `/projects/forge/`. Their visible names and content are placeholders. Those route slugs are inherited from the reference; changing them requires updating links and page paths together.

**Needed from you:** hero visual, portrait, real work images and project details for any slots you want to use, contact email, and optional social profile URLs. The original reference images currently appear as temporary visual assets. Project cards say “Reference visual,” while the portrait and hero have visible replacement labels; the project detail copy is explicitly marked as a placeholder. Replace these assets with your own before presenting the work as your portfolio.
# Latest project

Edit `latest-project.html` to update the project name, description, website URL, and live preview. The section uses `dist/inkphase-latest.css` and sits directly after Selected Work on the homepage. Some external websites may prohibit embedding.
The Desktop and Mobile preview controls are handled by `dist/inkphase-latest.js`. They resize the live site's viewport rather than loading different project assets.
# About page

`/about/` contains the Who Am I section, founder portrait, and Simple Process section. They are drawn from the saved reference layout by `build-inkphase.py`; edit the written copy and portrait path in `inkphase-content.json`. The Home navigation now opens this page.
# Services

Edit `services-section.html` to update the three service cards and their matching pricing cards. The Services/Pricing switch is handled by `dist/inkphase-services.js`. Pricing is intentionally marked “Custom quote” until actual rates are supplied.

# Work gallery

The fan-shaped Work section after Services uses five selected images from `work-gallery.json`. The `/work/` page displays every image listed there. To add, remove, reorder, or rename portfolio visuals, update that JSON file and place the optimized image at the referenced path inside `dist/assets/work/`. The existing design, image captions, hover effects, and scroll reveals stay in `dist/inkphase-gallery.css`.

# Giveaways

The Giveaways section follows Work and uses `giveaways-section.html` and `dist/inkphase-giveaways.css`. Its previews load standalone HTML/CSS widgets from `dist/assets/giveaways/`. The download buttons provide those same editable `.html` files, each with embedded CSS. The ZIP contains both code files. Edit the widget HTML directly and regenerate the ZIP if you change either one.
