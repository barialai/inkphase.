INKPHASE WEBSITE PROJECT

The dist/ folder is the ready-to-host website. Upload its contents to a static web host.

To preview locally:
  python -m http.server 8000 --directory dist
  Open http://localhost:8000/

To edit content:
  - inkphase-content.json: homepage, about, project, and contact copy
  - work-gallery.json: work images and captions
  - showcase-hero.html and other section .html files: section structure
  - dist/inkphase-palette.css: six-color site palette
  - dist/inkphase-laptop.css and .js: landing-video layout/playback
  - dist/assets/: website assets, including the supplied landing video

Install Python lxml if needed (python -m pip install lxml), then run
  python build-inkphase.py
This regenerates the pages in dist/. The short intro video retains its source visuals
and its audio is mixed to 50%. Browsers may restrict audible autoplay.
