# vatanilabs.com

The Vatani Tech website. Plain HTML, CSS and a little JavaScript: no
framework, nothing to install.

The site is in three languages. English is the top of the site, Azerbaijani
is the same pages under `/az/` and Russian under `/ru/`. The language menu
in the header (and the links in the footer) lead to the same page in the
other languages.

- `index.html`: home. The hero is a cloud of light points that forms the
  logo, a turning Earth (real coastlines from PetroGram's own map) and an
  oil drop (`assets/hero.js`). Then the app showcase, principles, contact.
  The showcase has one tab per app: PetroGram, then the apps still being
  made (Mining Atlas, Domino Freedom, Domino Global), which are the `SOON`
  list in `_tools/build.py`. Icons and logo come from the PetroGram
  repository's `branding/` folder.
- `petrogram/`: the PetroGram page, its privacy policy and terms of use
  (7 languages on one page; the app links to these).
- `az/`, `ru/`: the same pages in Azerbaijani and Russian. Their privacy
  and terms pages show that one language and link to the others.
- `assets/`: `site.css` (all styles), `site.js` (scroll effects and the small
  animated feature tiles), `hero.js`, `land.js` (globe points), images.
  Shared by all three languages.
- `_tools/`: the scripts that write the pages. Not published (GitHub Pages
  skips folders that start with "_").
  - `python3 -I _tools/build.py` rebuilds every page in every language, and
    `sitemap.xml`. Never edit the built pages by hand.
  - `_tools/site_texts.py`: every text of the site, one row per text:
    English, Azerbaijani, Russian. To change or add a text, edit it there
    and rebuild. The build stops if a language is missing.
  - `python3 -I _tools/make_land.py` rebuilds the globe and map dots.
- `CNAME`: the custom domain for GitHub Pages.

The build reads a few privacy texts from the PetroGram app folder
(`~/Developer/petrogram` on the Mac, `~/petrogram` on the PC). The PC has no
Python of its own; the one inside the Android SDK works:
`%LOCALAPPDATA%\Android\Sdk\ndk\<version>\toolchains\llvm\prebuilt\windows-x86_64\python3\python.exe -I _tools\build.py`.

Preview: `python3 -m http.server 8765` in this folder, then open
http://localhost:8765 (and `/az/`, `/ru/`).
