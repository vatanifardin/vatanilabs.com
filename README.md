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
  made (Geo-Rulers, OreGram, Domino Freedom, Domino Global), which are the
  `SOON` list in `_tools/build.py`. Icons and logo come from the PetroGram
  repository's `branding/` folder; the Geo-Rulers icon
  (`assets/img/geo-rulers-icon.png`, 256 × 256) from the Geo-Rulers
  repository's `branding/apps/geo-rulers/icon-1024.png`, and the OreGram
  icon (`assets/img/oregram-icon.png`, 256 × 256) from the OreGram
  repository's `branding/apps/oregram/icon-1024.png`.
- `petrogram/`: the PetroGram page, its privacy policy and terms of use
  (7 languages on one page; the app links to these).
- `geo-rulers/`: the Geo-Rulers page (the app is still being made: no
  store buttons, no screenshots yet; the slogans "Ore what?", "Mine your
  business." and "Dig it." stay in English in every language), its privacy
  policy, terms of use and page for deleting an account (7 languages on
  one page; the app links to these).
- `oregram/`: the same four pages for OreGram (26 November 2026), a twin
  of Geo-Rulers: the same app and texts with another name, icon (ore on
  gold) and colour (gold, `#B8860B`). The build makes them from the same
  code and the same rows of text as Geo-Rulers' pages (the `PAGES` list in
  `_tools/build.py`), with OreGram in place of Geo-Rulers.
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
  - `_tools/georulers_texts.py`: what the privacy policy, delete page and
    terms of use of the two mining apps, Geo-Rulers and OreGram, say
    differently from PetroGram's (name, date, what the app is about,
    prices), in seven languages; the same differences for both apps (there
    is no separate `oregram_texts.py`). Everything else in those three
    pages is PetroGram's text, so a change to PetroGram's policy or terms
    reaches both apps too; the build stops if a text to be replaced is no
    longer found. Their terms must say what the apps' own terms say
    (`lib/strings_services.dart` and `lib/zh/zh_services.dart` in the
    Geo-Rulers and OreGram repositories): change them together.
  - `python3 -I _tools/make_land.py` rebuilds the globe and map dots.
- `CNAME`: the custom domain for GitHub Pages.
- `geo-rulers/data/prices.json` and `oregram/data/prices.json`: the
  monthly metal and mineral prices that the Geo-Rulers and OreGram apps
  read (World Bank "Pink Sheet" data, CC BY 4.0, adapted; monthly
  averages, not live prices). The two files are always the same. **A robot
  rewrites them once a month**: the GitHub Actions workflow
  `.github/workflows/geo-rulers-prices.yml` runs on the 6th and the 16th,
  downloads the current World Bank file, runs
  `_tools/geo-rulers/build_prices.py`, copies the result to
  `oregram/data/prices.json` and commits both files if they changed. Nobody has to do anything. Because the robot commits to `main`,
  **always `git pull` before changing the site**. To run it by hand: on
  GitHub, Actions → "Geo-Rulers monthly prices" → Run workflow. If a run
  fails, GitHub sends an email and the old file stays. The script's master
  copy is in the Geo-Rulers repository (`tool/prices/`); copy it here
  after changing it there. Never edit `prices.json` by hand, and do not
  move it: each app has its address built in.

The build reads a few privacy texts (sections 6b to 6g of each policy) from
the three app folders: PetroGram (`~/Developer/petrogram` on the Mac,
`~/petrogram` on the PC), Geo-Rulers (`~/Developer/geo-rulers`,
`~/geo-rulers`) and OreGram (`~/Developer/oregram`, `~/oregram`), from
`docs/ACCOUNT_SETUP.md` part 3 and `docs/PRIVACY_ADDITIONS.md` of each. All
three folders must be there and up to date (`git pull`). To read an app
from another folder for one run, name it in `PETROGRAM_APP`,
`GEO_RULERS_APP` or `OREGRAM_APP`:
`GEO_RULERS_APP=/path/to/geo-rulers python3 -I _tools/build.py`. The PC has no
Python of its own; the one inside the Android SDK works:
`%LOCALAPPDATA%\Android\Sdk\ndk\<version>\toolchains\llvm\prebuilt\windows-x86_64\python3\python.exe -I _tools\build.py`.

Preview: `python3 -m http.server 8765` in this folder, then open
http://localhost:8765 (and `/az/`, `/ru/`).
