# vatanilabs.com

The Vatani Labs website. Plain HTML, CSS and a little JavaScript: no
framework, nothing to install.

- `index.html`: home. The hero is a cloud of light points that forms the
  logo, a turning Earth (real coastlines from PetroGram's own map) and an
  oil drop (`assets/hero.js`). Then the app showcase, principles, contact.
- `petrogram/`: the PetroGram page, its privacy policy and terms of use
  (7 languages).
- `assets/`: `site.css` (all styles), `site.js` (scroll effects and the small
  animated feature tiles), `hero.js`, `land.js` (globe points), images.
- `_tools/`: the scripts that write the pages. Not published (GitHub Pages
  skips folders that start with "_").
  - `python3 -I _tools/build.py` rebuilds every page.
  - `python3 -I _tools/make_land.py` rebuilds the globe and map dots.
- `CNAME`: the custom domain for GitHub Pages.

Preview: `python3 -m http.server 8765` in this folder, then open
http://localhost:8765.
