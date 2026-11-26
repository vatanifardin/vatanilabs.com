#!/usr/bin/env python3
"""Builds every page of vatanilabs.com as plain HTML, in three languages.

Run:  python3 -I _tools/build.py   (from the site folder)

English is the top of the site (/, /petrogram/ ...); Azerbaijani is the same
pages under /az/ and Russian under /ru/. Every text of the site is one row of
site_texts.py (English, Azerbaijani, Russian); the page layout is here.

Other inputs in this folder: flat_map.json (from make_land.py), terms.json
(the app's terms of use in 7 languages), privacy_old.html + privacy_texts.py
(the privacy policy and its 21 November 2026 changes), delete_texts.py (the
page for deleting an account, in 7 languages), georulers_texts.py (what the
Geo-Rulers privacy policy, delete page and terms say differently from
PetroGram's).
The folder name starts with "_", so GitHub Pages does not publish it.
"""
import html, json, os, re
from pathlib import Path
from urllib.parse import quote

T = Path(__file__).resolve().parent
OUT = T.parent


def app_folder(folder, env):
    """The folder of an app (some privacy texts are read from its docs): the
    Mac keeps it in ~/Developer/<folder>, the PC in ~/<folder>. Another place
    can be given for one run in the environment variable <env>, for example
    GEO_RULERS_APP=/path/to/geo-rulers python3 -I _tools/build.py"""
    places = [Path('/Users/fardinvatani/Developer') / folder,
              Path.home() / 'Developer' / folder, Path.home() / folder]
    if os.environ.get(env):
        places = [Path(os.environ[env]).expanduser()]
    return next((p for p in places if (p / 'docs').is_dir()), None)


APP = app_folder('petrogram', 'PETROGRAM_APP')
assert APP, 'PetroGram app folder not found'
GEO = app_folder('geo-rulers', 'GEO_RULERS_APP')
assert GEO, 'Geo-Rulers app folder not found'


def rd(p):
    """Read a text file (always UTF-8, on the Mac and on the PC)."""
    return Path(p).read_text(encoding='utf-8')


def wr(p, text):
    """Write a text file: UTF-8, Unix line ends, folders made as needed."""
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


# ------------------------------------------------------------- languages
SITE = 'https://vatanilabs.com'
LANGS = ('en', 'az', 'ru')                  # the order of the rows in site_texts.py
NAMES = {'en': 'English', 'az': 'Azərbaycanca', 'ru': 'Русский'}
PRE = {'en': '', 'az': '/az', 'ru': '/ru'}  # where each language lives on the site
LOCALE = {'en': 'en_US', 'az': 'az_AZ', 'ru': 'ru_RU'}
L = 'en'                                    # the language being built (set in the loop at the end)

exec(rd(T / 'site_texts.py'))               # defines TX
for _k, _row in TX.items():
    assert len(_row) == len(LANGS) and all(_row), ('a text is missing in site_texts.py', _k)


def t(key):
    """A text of the site in the language being built."""
    return TX[key][LANGS.index(L)]


def e(key):
    """The same, made safe to sit inside an HTML attribute."""
    return html.escape(t(key))


def u(path):
    """A link to a page of the site, in the language being built."""
    return PRE[L] + path


def data(value):
    """A list or table handed to the scripts through a data- attribute."""
    return html.escape(json.dumps(value, ensure_ascii=False))


MARK = ('<svg viewBox="0 0 120 100" aria-hidden="true">'
        '<polyline points="15,15 60,85 105,15" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polyline points="36.7,15 60,51.4 83.3,15" fill="none" stroke="#2cc4b8" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def fonts():
    # The italic accent font, Instrument Serif, has no Cyrillic letters and no
    # Azerbaijani "ə", so those two languages use Playfair Display instead.
    serif = 'Instrument+Serif:ital@1' if L == 'en' else 'Playfair+Display:ital@1'
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family={serif}&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">')


def ico(body):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


I_OFFLINE = ico('<path d="M2 8.5a15 15 0 0 1 20 0"/><path d="M5.5 12.2a10 10 0 0 1 13 0"/><path d="M9 15.8a5 5 0 0 1 6 0"/><circle cx="12" cy="19.2" r=".9" fill="currentColor"/><path d="M4 3l16 18"/>')
I_FOCUS = ico('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1" fill="currentColor"/>')
I_CHECK = ico('<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.8 2.8L16 9.5"/>')
I_SHIELD = ico('<path d="M12 3l7 3v5.5c0 4.4-3 8-7 9.5-4-1.5-7-5.1-7-9.5V6l7-3z"/><path d="M9 12l2.2 2.2L15 10.5"/>')
I_SWAP = ico('<path d="M7 4v14m0 0l-3-3m3 3l3-3M17 20V6m0 0l-3 3m3-3l3 3"/>')
I_GLOBE = ico('<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9s1.3-6.4 3.8-9z"/>')
I_FLAME = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5c1 3.2 4.5 4.8 4.5 9.2a4.5 4.5 0 0 1-9 0c0-1.7.8-2.9 1.7-3.8.3 1.3 1 2 1.7 2C11 7.800 10.400 5.200 12 2.500z"/></svg>'


def lang_links(path):
    """The same page in each language (the one being read is marked)."""
    return ''.join(
        f'<a href="{PRE[l]}{path}" lang="{l}" hreflang="{l}"' + (' aria-current="true"' if l == L else '') + f'>{NAMES[l]}</a>'
        for l in LANGS)


def page(key, body, path='/', scripts=(), found=True, name=None, app=None):
    """One whole page. key picks its title and description in site_texts.py;
    path is its address in English ("/petrogram/"), the same in every language.
    name: another app, whose name replaces PetroGram in the title and
    description; app: that app's folder on the site, for the footer."""
    title, desc = html.escape(t(key + '_title')), html.escape(t(key + '_desc'))
    if name:
        title, desc = title.replace('PetroGram', name), desc.replace('PetroGram', name)
    tags = ''.join(f'<script src="{s}" defer></script>\n' for s in scripts)
    if found:   # tell search engines where the page is and where its other languages are
        seo = (f'<link rel="canonical" href="{SITE}{u(path)}">\n'
               # proves to Google Search Console that the site is ours (not a secret)
               + '<meta name="google-site-verification" content="VTXQPLOQSYm-PyBicOfBXb4ScrtuZDwoSpe1uawuOJQ">\n'
               + ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{PRE[l]}{path}">\n' for l in LANGS)
               + f'<link rel="alternate" hreflang="x-default" href="{SITE}{path}">\n')
        switch = lang_links(path)
    else:       # the "not found" page: its language menu leads to the home pages
        seo = '<meta name="robots" content="noindex">\n'
        switch = lang_links('/')
        if L == 'en':
            # GitHub Pages shows this one page for every wrong address, so a
            # wrong address under /az/ or /ru/ is sent on to that language's own page.
            seo += ('<script>(function(){var m=location.pathname.match(/^\\/(az|ru)(\\/|$)/);'
                    "if(m&&!/\\/404\\.html$/.test(location.pathname))location.replace('/'+m[1]+'/404.html')})()</script>\n")
    # The footer leads to PetroGram's pages; on the pages of another app, to
    # that app's own page, privacy policy and terms of use.
    fname, fapp = (name, app) if app else ('PetroGram', 'petrogram')
    foot = f'''<a href="{u(f'/{fapp}/')}">{fname}</a>
      <a href="{u(f'/{fapp}/privacy/')}">{t('privacy')}</a>
      <a href="{u(f'/{fapp}/terms/')}">{t('terms')}</a>'''
    return f'''<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#04060c">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://vatanilabs.com/assets/img/icon-512.png">
<meta property="og:url" content="https://vatanilabs.com{u(path)}">
<meta property="og:locale" content="{LOCALE[L]}">
{seo}<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
{fonts()}
<link rel="stylesheet" href="/assets/site.css">
<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.VL_READY)document.documentElement.classList.remove('js')}},4000)</script>
</head>
<body data-copied="{e('copied')}" data-write="{e('write_to')}">
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{u('/')}" aria-label="{e('home_aria')}">{MARK}<b>Vatani</b><span>Tech</span></a>
    <nav class="nav" aria-label="{e('nav_main')}">
      <a href="{u('/#apps')}">{t('nav_apps')}</a>
      <a href="{u('/#principles')}">{t('nav_how')}</a>
      <a class="btn" href="{u('/#contact')}">{t('nav_contact')}</a>
    </nav>
    <details class="lang">
      <summary aria-label="{e('lang')}: {NAMES[L]}">{I_GLOBE}<span>{L.upper()}</span></summary>
      <div class="lang-menu">{switch}</div>
    </details>
  </div>
</header>
{body}
<footer class="site-footer">
  <div class="wrap">
    <a class="brand" href="{u('/')}" aria-label="{e('home_aria')}">{MARK}<b>Vatani</b><span>Tech</span></a>
    <span>© 2026 Vatani Tech · {t('foot_place')}</span>
    <nav aria-label="{e('nav_footer')}">
      {foot}
      <a href="mailto:support@vatanilabs.com">support@vatanilabs.com</a>
    </nav>
    <nav class="foot-langs" aria-label="{e('lang')}">{switch}</nav>
  </div>
  <div class="wordmark" aria-hidden="true">Vatani Tech</div>
</footer>
{tags}</body>
</html>
'''


# ------------------------------------------------- the living feature tiles
def tile(cls, viz, cap, title, text, d=0):
    return (f'<article class="tile glow rv {cls}" style="--d:{d:.2f}s">\n<div class="viz">{viz}</div>\n'
            f'<div class="cap">{cap}</div><h4>{title}</h4><p>{text}</p>\n</article>')


def t_map(cls, d=0):
    dots = ''.join(f'M{(lon + 180) * 2:g} {(84 - lat) * 2:g}h0' for lon, lat in json.loads(rd(T / 'flat_map.json')))
    # Well-known oil and gas regions (lon, lat).
    pins = [(-102.5, 32), (-90, 27.5), (-113, 55.5), (-42, -24.5), (2.5, 58.5), (6, 4.8),
            (50.5, 40.3), (50.5, 27), (73, 61.5), (118.5, 38.5), (116, -20.5)]
    marks = ''.join(
        f'<g transform="translate({(lon + 180) * 2:g} {(84 - lat) * 2:g})"><circle class="ring" r="3" style="--d:{(i * 0.37) % 2.8:.2f}s"/><circle class="core" r="2.6"/></g>'
        for i, (lon, lat) in enumerate(pins))
    viz = (f'<div class="vmap"><svg viewBox="0 0 720 284" role="img" aria-label="{e("map_aria")}">'
           f'<path class="dots" d="{dots}"/>{marks}</svg></div>')
    return tile(cls, viz, t('map_cap'), t('map_h'), t('map_p'), d)


def t_conv(cls, d=0):
    pairs = t('conv_pairs')     # site.js rolls through them; the first one is shown at the start
    viz = (f'<div class="conv" data-conv data-pairs="{data(pairs)}" aria-label="{e("conv_aria")}">'
           f'<div class="row"><span class="num" data-a>{pairs[0][0]}</span><span class="unit" data-ua>{pairs[0][1]}</span></div>'
           f'<div class="swap">{I_SWAP}</div>'
           f'<div class="row out"><span class="num" data-b>{pairs[0][2]}</span><span class="unit" data-ub>{pairs[0][3]}</span></div></div>')
    return tile(cls, viz, t('conv_cap'), t('conv_h'), t('conv_p'), d)


def t_flash(cls, d=0):
    cards = t('flash_cards')    # site.js flips through them
    viz = (f'<div class="flash" data-cards="{data(cards)}" aria-label="{e("flash_aria")}"><div class="flash-in">'
           f'<div class="face front"><small>{t("flash_term")}</small><b>{cards[0][0]}</b></div>'
           f'<div class="face back"><small>{t("flash_meaning")}</small><span>{cards[0][1]}</span></div>'
           '</div></div>')
    return tile(cls, viz, t('flash_cap'), t('flash_h'), t('flash_p'), d)


def t_quiz(cls, d=0):
    viz = (f'<div class="quiz" aria-label="{e("quiz_aria")}">'
           f'<div class="q"><span>{t("quiz_q")}</span>'
           '<span class="ringbox"><svg viewBox="0 0 44 44"><circle class="tr" cx="22" cy="22" r="18"/><circle class="pr" cx="22" cy="22" r="18"/></svg>8/10</span></div>'
           '<div class="opt"><i></i>Bottom oil pressure</div>'
           '<div class="opt ok"><i>✓</i>Blowout preventer</div>'
           '<div class="opt"><i></i>Barrel of petroleum</div>'
           f'<span class="streak">{I_FLAME} {t("quiz_streak")}</span></div>')
    return tile(cls, viz, t('quiz_cap'), t('quiz_h'), t('quiz_p'), d)


def t_lang(cls, d=0):
    words = 'Knowledge|Bilik|Знание|معرفة|Conocimiento|Savoir|知识'
    chips = ''.join(f'<span class="chip{" on" if i == 0 else ""}">{c}</span>'
                    for i, c in enumerate(['EN', 'AZ', 'RU', 'AR', 'ES', 'FR', '中文']))
    viz = (f'<div class="langs7"><div class="langword" data-words="{words}">Knowledge</div>'
           f'<div class="chips">{chips}</div></div>')
    return tile(cls, viz, t('lang_cap'), t('lang_h'), t('lang_p'), d)


def t_market(cls, d=0):
    l1 = 'M0 122 C 30 112, 50 92, 80 98 S 130 62, 160 72 S 210 112, 240 94 S 300 32, 330 46 S 385 24, 410 30'
    l2 = 'M0 142 C 40 134, 70 122, 100 128 S 160 102, 200 110 S 260 132, 300 114 S 380 72, 410 80'
    viz = (f'<div class="chart"><svg viewBox="0 0 420 170" role="img" aria-label="{e("market_aria")}">'
           '<defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2cc4b8" stop-opacity=".32"/><stop offset="1" stop-color="#2cc4b8" stop-opacity="0"/></linearGradient></defs>'
           '<line class="grid" x1="0" x2="420" y1="40" y2="40"/><line class="grid" x1="0" x2="420" y1="85" y2="85"/><line class="grid" x1="0" x2="420" y1="130" y2="130"/>'
           f'<path class="area" fill="url(#ar)" d="{l1} L410 170 L0 170 Z"/>'
           f'<path class="l2" pathLength="1" d="{l2}"/><path class="l1" pathLength="1" d="{l1}"/>'
           '<g class="end" transform="translate(410 30)"><circle class="ring" r="4"/><circle r="4" fill="#7ff0e4"/></g>'
           '</svg><div class="chips"><span class="chip on">Brent</span><span class="chip">WTI</span><span class="chip">Henry Hub</span>'
           f'<span class="chip">{t("market_rigs")}</span></div></div>')
    return tile(cls, viz, t('market_cap'), t('market_h'), t('market_p'), d)


def t_talk(cls, d=0):
    viz = (f'<div class="talk" aria-label="{e("talk_aria")}">'
           f'<div class="ask">{t("talk_q")}</div>'
           f'<div class="ans"><small>{t("talk_model")}</small><div class="ln"></div><div class="ln"></div><div class="ln"></div></div></div>')
    return tile(cls, viz, t('talk_cap'), t('talk_h'), t('talk_p'), d)


def t_offline(cls, d=0):
    viz = f'<div class="offline"><span></span><span></span><span></span><div class="core">{I_OFFLINE}</div></div>'
    return tile(cls, viz, t('off_cap'), t('off_h'), t('off_p'), d)


def t_more(cls, d=0):
    viz = ('<div class="chips" style="justify-content:center;max-width:520px">'
           + ''.join(f'<span class="chip">{i}</span>' for i in t('more_items')) + '</div>')
    return tile(cls, viz, t('more_cap'), t('more_h'), t('more_p'), d)


def phone(img, alt, i=None):
    st = f' style="--i:{i};--a:{abs(i)}"' if i is not None else ''
    return f'<div class="phone"{st}><img src="/assets/img/{img}" alt="{html.escape(alt)}" loading="lazy"></div>'


def band(words):
    one = ''.join(f'<span class="{"f" if i % 2 == 0 else ""}">{w}<i>✦</i></span>' for i, w in enumerate(words))
    return f'<div class="band" aria-hidden="true"><div class="band-track">{one}{one}</div></div>'


# The apps that are still being made: address name, name, the colour of the
# glow under the icon, and the captions of its three cards (rows of
# site_texts.py; the texts of an app are its rows "<key>_sub", "<key>_lead",
# "<key>_h1" ... "<key>_p3"). The icon is assets/img/<address name>-icon.png.
# An app in PAGES has its own page at /<address name>/, and its panel links to it.
SOON = [
    ('geo-rulers', 'Geo-Rulers', 'gr', '194,97,28', ('conv_cap', 'flash_cap', 'map_cap')),
    ('domino-freedom', 'Domino Freedom', 'df', '22,160,102', ('off_cap', 'cap_together', 'cap_light')),
    ('domino-global', 'Domino Global', 'dg', '139,53,201', ('more_cap', 'cap_together', 'cap_family')),
]
PAGES = {'geo-rulers'}


def soon_tab(n, app):
    slug, name = app[0], app[1]
    return (f'      <button class="tab" role="tab" id="tab-{slug}" aria-controls="panel-{slug}" aria-selected="false" tabindex="-1">'
            f'<span class="n">{n:02d}</span>{name}</button>\n')


def soon_panel(app):
    slug, name, k, glow, caps = app
    cards = ''.join(
        f'        <div class="card glow"><span class="label">{t(c)}</span><h3>{t(f"{k}_h{i}")}</h3><p>{t(f"{k}_p{i}")}</p></div>\n'
        for i, c in enumerate(caps, 1))
    subject = quote(t('next_subject') + ': ' + name)
    own = (f'<a class="btn solid" href="{u(f"/{slug}/")}">{t("discover_of").format(name)} <span class="arr">→</span></a>'
           if slug in PAGES else '')
    return f'''    <div class="panel" role="tabpanel" id="panel-{slug}" aria-labelledby="tab-{slug}" hidden>
      <div class="app-line">
        <img src="/assets/img/{slug}-icon.png" alt="{html.escape(t('icon_alt_of').format(name))}" style="--glow:rgba({glow},.9)">
        <div><h3 lang="en">{name}</h3><div class="sub">{t(k + '_sub')}</div></div>
        <div class="chips"><span class="chip on">{t('dev')}</span><span class="chip" lang="en">Android</span><span class="chip" lang="en">iPhone</span></div>
      </div>
      <p class="app-lead">{t(k + '_lead')}</p>
      <div class="grid3">
{cards}      </div>
      <div class="actions" style="margin-top:26px">{own}<a class="btn" href="mailto:support@vatanilabs.com?subject={subject}">{t('next_cta')} <span class="arr">→</span></a></div>
    </div>

'''


# ------------------------------------------------------------------ home
def home():
    # Captions under the hero picture: number, text and, for the studio's
    # name, its language (so that capital letters follow English rules).
    caps = {'mark': ['01', 'Vatani Tech', 'en'], 'globe': ['02', t('cap_globe')], 'drop': ['03', t('cap_drop')]}
    return f'''<main>
<section class="hero" aria-label="{e('hero_aria')}">
  <div class="sculpt"><canvas id="sculpture" data-shapes="mark,globe,drop" data-captions="{data(caps)}" aria-hidden="true"></canvas><div class="sculpt-cap" id="sculpture-cap"></div></div>
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill rv"><i></i>{t('hero_pill')}</span>
      <h1 class="rv" style="--d:.08s">{t('hero_h1')}</h1>
      <p class="lead rv" style="--d:.16s">{t('hero_lead')}</p>
      <div class="actions rv" style="--d:.24s">
        <a class="btn solid" href="#apps">{t('hero_cta1')} <span class="arr">→</span></a>
        <a class="btn" href="#contact">{t('hero_cta2')}</a>
      </div>
    </div>
  </div>
  <div class="scroll-hint" aria-hidden="true">{t('scroll')}</div>
</section>

<div class="stats">
  <div class="wrap">
    <div class="stat rv"><b data-count="500">500</b><span>{t('st_terms')}</span></div>
    <div class="stat rv" style="--d:.08s"><b data-count="600">600</b><span>{t('st_quiz')}</span></div>
    <div class="stat rv" style="--d:.16s"><b data-count="7">7</b><span>{t('st_langs')}</span></div>
    <div class="stat rv" style="--d:.24s"><b><span data-count="100">100</span><small>%</small></b><span>{t('st_offline')}</span></div>
  </div>
</div>
{band(t('band_home'))}

<section class="block" id="apps">
  <div class="wrap">
    <div class="block-head">
      <div class="rv">
        <p class="label"><span class="n">01 /</span> {t('apps_label')}</p>
        <h2>{t('apps_h2')}</h2>
      </div>
      <p class="rv" style="--d:.1s">{t('apps_p')}</p>
    </div>

    <div class="tabs rv" role="tablist" aria-label="{e('nav_apps')}">
      <button class="tab" role="tab" id="tab-petrogram" aria-controls="panel-petrogram" aria-selected="true"><span class="n">01</span>PetroGram</button>
{''.join(soon_tab(n, a) for n, a in enumerate(SOON, 2))}    </div>

    <div class="panel" role="tabpanel" id="panel-petrogram" aria-labelledby="tab-petrogram">
      <div class="app-line rv">
        <img src="/assets/img/petrogram-icon.png" alt="{e('icon_alt')}">
        <div><h3>PetroGram</h3><div class="sub">{t('pg_sub')}</div></div>
        <div class="chips"><span class="chip on">{t('soon')}</span><span class="chip" lang="en">Android</span><span class="chip" lang="en">iPhone</span></div>
      </div>
      <div class="bento">
        {t_map('w7')}
        {t_conv('w5', .08)}
        {t_flash('', 0)}
        {t_quiz('', .08)}
        {t_lang('', .16)}
      </div>
      <div class="actions rv" style="margin-top:26px"><a class="btn solid" href="{u('/petrogram/')}">{t('discover')} <span class="arr">→</span></a></div>
    </div>

{''.join(soon_panel(a) for a in SOON)}
    <div class="showcase-foot">
      <span>{t('made')}</span>
      <div class="pager">
        <button type="button" id="prev" aria-label="{e('prev_app')}">←</button>
        <span id="count">01 / {len(SOON) + 1:02d}</span>
        <button type="button" id="next" aria-label="{e('next_app')}">→</button>
      </div>
    </div>
  </div>
</section>

<section class="block" id="principles">
  <div class="wrap">
    <div class="block-head">
      <div class="rv">
        <p class="label"><span class="n">02 /</span> {t('nav_how')}</p>
        <h2>{t('how_h2')}</h2>
      </div>
      <p class="rv" style="--d:.1s">{t('how_p')}</p>
    </div>
    <div class="grid4">
      <div class="card glow rv"><div class="ico">{I_OFFLINE}</div><h3>{t('p1_h')}</h3><p>{t('p1_p')}</p></div>
      <div class="card glow rv" style="--d:.08s"><div class="ico">{I_FOCUS}</div><h3>{t('p2_h')}</h3><p>{t('p2_p')}</p></div>
      <div class="card glow rv" style="--d:.16s"><div class="ico">{I_CHECK}</div><h3>{t('p3_h')}</h3><p>{t('p3_p')}</p></div>
      <div class="card glow rv" style="--d:.24s"><div class="ico">{I_SHIELD}</div><h3>{t('p4_h')}</h3><p>{t('p4_p')}</p></div>
    </div>
  </div>
</section>

<section class="block" id="contact" style="padding-top:40px">
  <div class="wrap">
    <div class="contact-card rv">
      <p class="label"><span class="n">03 /</span> {t('nav_contact')}</p>
      <h2>{t('contact_h2')}</h2>
      <p>{t('contact_p')}</p>
      <a class="mail" href="mailto:support@vatanilabs.com">support@vatanilabs.com <span class="arr">→</span></a>
    </div>
  </div>
</section>
</main>'''


# ------------------------------------------------------------- PetroGram
def petro():
    shots = ['2_learn', '3_upstream', '1_home', '5_maps', '4_quiz']
    fan = '\n'.join(phone(f'pg-{n}.jpg', a, i - 2) for i, (n, a) in enumerate(zip(shots, t('shots'))))
    return f'''<main>
<section class="app-hero">
  <div class="sculpt"><canvas id="sculpture" data-shapes="drop" aria-hidden="true"></canvas></div>
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill rv"><i></i>{t('pg_pill')}</span>
      <div class="top rv" style="--d:.08s">
        <img class="app-icon" src="/assets/img/petrogram-icon.png" alt="{e('icon_alt')}">
        <h1>Petro<em class="s">Gram</em></h1>
      </div>
      <p class="lead rv" style="--d:.16s">{t('pg_lead')}</p>
      <div class="actions rv" style="--d:.24s">
        <span class="btn" aria-disabled="true">{t('store_ios')}</span>
        <span class="btn" aria-disabled="true">{t('store_play')}</span>
      </div>
      <p class="store-note rv" style="--d:.3s">{t('store_note')}</p>
    </div>
  </div>
</section>
{band(t('band_pg'))}

<section class="block">
  <div class="wrap">
    <div class="block-head">
      <div class="rv">
        <p class="label"><span class="n">{t('feat_n')}</span> {t('feat_label')}</p>
        <h2>{t('feat_h2')}</h2>
      </div>
      <p class="rv" style="--d:.1s">{t('feat_p')}</p>
    </div>
    <div class="bento">
      {t_map('w8')}
      {t_conv('', .08)}
      {t_flash('')}
      {t_quiz('', .08)}
      {t_offline('', .16)}
      {t_market('w7')}
      {t_talk('w5', .08)}
      {t_lang('w5')}
      {t_more('w7', .08)}
    </div>
  </div>
</section>

<section class="block" style="padding-top:20px">
  <div class="wrap">
    <div class="block-head">
      <div class="rv">
        <p class="label"><span class="n">{t('scr_n')}</span> {t('scr_label')}</p>
        <h2>{t('scr_h2')}</h2>
      </div>
      <p class="rv" style="--d:.1s">{t('scr_p')}</p>
    </div>
    <div class="fan rv" aria-label="{e('scr_aria')}">
{fan}
    </div>
  </div>
</section>

<section class="block" style="padding-top:20px">
  <div class="wrap">
    <div class="grid3">
      <div class="card glow rv"><span class="label">{t('sup_label')}</span><h3>{t('sup_h')}</h3><p>{t('sup_p')}</p></div>
      <div class="card glow rv" style="--d:.08s"><span class="label">{t('prv_label')}</span><h3>{t('privacy')}</h3><p>{t('prv_p')} <a href="{u('/petrogram/privacy/')}">{t('read_it')}</a></p></div>
      <div class="card glow rv" style="--d:.16s"><span class="label">{t('trm_label')}</span><h3>{t('terms')}</h3><p>{t('trm_p')} <a href="{u('/petrogram/terms/')}">{t('read_them')}</a></p></div>
    </div>
  </div>
</section>
</main>'''


# ------------------------------------------------------------ Geo-Rulers
# The page of an app that is still being made: like PetroGram's, but with
# no store buttons and no screenshots (there are none yet). The hero shows
# the turning Earth (the app's maps of mines and deposits); the icon stands
# where the screens would be. The slogans are English on the English page and rhyming translations on the others (owner, 26 Nov 2026).
def geo():
    slug, name, k, glow = SOON[0][:4]
    assert slug == GEO_APP and name == GEO_NAME, 'Geo-Rulers must be the first app of SOON'
    icon = f'/assets/img/{slug}-icon.png'
    alt = e('icon_alt_of').format(name)
    ore, _, dig = t('gr_slogans')   # the second one heads the features (gr_feat_h2)
    mail = f'mailto:support@vatanilabs.com?subject={quote(t("next_subject") + ": " + name)}'
    caps = ['conv_cap', 'flash_cap', 'quiz_cap', 'gr_cap_read', 'map_cap', 'gr_cap_companies', 'market_cap', 'lang_cap', 'off_cap']
    heads = [f'gr_c{i}_h' for i in range(1, 8)] + ['lang_h', 'off_h']
    texts = [f'gr_c{i}_p' for i in range(1, 8)] + ['lang_p', 'gr_c9_p']
    cards = '\n'.join(
        f'      <div class="card glow rv" style="--d:{(i % 3) * .08:.2f}s"><span class="label">{t(c)}</span><h3>{t(h)}</h3><p>{t(p)}</p></div>'
        for i, (c, h, p) in enumerate(zip(caps, heads, texts)))
    return f'''<main>
<section class="app-hero">
  <div class="sculpt"><canvas id="sculpture" data-shapes="globe" aria-hidden="true"></canvas></div>
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill rv"><i></i>{t('gr_pill')}</span>
      <div class="top rv" style="--d:.08s">
        <img class="app-icon" src="{icon}" alt="{alt}" style="--glow:rgba({glow},.95)">
        <h1>Geo-<em class="s">Rulers</em></h1>
      </div>
      <p class="slogan rv" style="--d:.12s"><em class="s">{ore}</em></p>
      <p class="lead rv" style="--d:.16s">{t('gr_page_lead')}</p>
      <div class="actions rv" style="--d:.24s">
        <span class="btn" aria-disabled="true">{t('dev')}</span>
        <a class="btn solid" href="{mail}">{t('next_cta')} <span class="arr">→</span></a>
      </div>
      <p class="store-note rv" style="--d:.3s">{t('gr_note')}</p>
    </div>
  </div>
</section>
{band(t('gr_band'))}

<section class="block">
  <div class="wrap">
    <div class="block-head">
      <div class="rv">
        <p class="label"><span class="n">{t('feat_n')}</span> {t('feat_label')}</p>
        <h2>{t('gr_feat_h2')}</h2>
      </div>
      <p class="rv" style="--d:.1s">{t('gr_feat_p')}</p>
    </div>
    <div class="grid3">
{cards}
    </div>
  </div>
</section>

<section class="block" style="padding-top:20px">
  <div class="wrap">
    <div class="soon rv">
      <div class="orbit"><img src="{icon}" alt="{alt}" style="--glow:rgba({glow},.9)"></div>
      <p class="label">{t('dev')}</p>
      <h3>{dig}</h3>
      <p>{t('gr_soon_p')}</p>
      <div class="actions" style="justify-content:center;margin-top:28px"><a class="btn" href="{mail}">{t('next_cta')} <span class="arr">→</span></a></div>
    </div>
  </div>
</section>

<section class="block" style="padding-top:20px">
  <div class="wrap">
    <div class="grid3">
      <div class="card glow rv"><span class="label">{t('sup_label')}</span><h3>{t('sup_h')}</h3><p>{t('sup_p')}</p></div>
      <div class="card glow rv" style="--d:.08s"><span class="label">{t('prv_label')}</span><h3>{t('privacy')}</h3><p>{t('prv_p')} <a href="{u(f'/{slug}/privacy/')}">{t('read_it')}</a><br><a href="{u(f'/{slug}/delete-account/')}">{t('delete-account')} →</a></p></div>
      <div class="card glow rv" style="--d:.16s"><span class="label">{t('trm_label')}</span><h3>{t('terms')}</h3><p>{t('trm_p')} <a href="{u(f'/{slug}/terms/')}">{t('read_them')}</a></p></div>
    </div>
  </div>
</section>
</main>'''


# ------------------------------------------------------ privacy and terms
# The app's two long texts exist in seven languages. The English page shows
# all seven, one after the other (the app links to it); the Azerbaijani and
# Russian pages show their own language and link to the others.
DOC_LANGS = {'en': 'English', 'az': 'Azərbaycanca', 'ru': 'Русский', 'ar': 'العربية',
             'es': 'Español', 'fr': 'Français', 'zh': '简体中文'}


def langnav(slug, app='petrogram'):
    def link(l):
        if L == 'en':
            return f'<a href="#{l}">'
        if l == L:
            return f'<a href="#{l}" aria-current="true">'
        if l in PRE and l != 'en':
            return f'<a href="{PRE[l]}/{app}/{slug}/">'
        return f'<a href="/{app}/{slug}/#{l}">'
    return (f'<nav class="langs" aria-label="{e("doc_langs")}">'
            + ''.join(link(l) + n + '</a>' for l, n in DOC_LANGS.items()) + '</nav>')


def doc(slug, sections, app='petrogram', name='PetroGram'):
    """A long text page: all languages in English, one language elsewhere.
    app and name: the app's folder on the site and the name people see."""
    shown = list(sections.values()) if L == 'en' else [sections[L]]
    sep = '\n' if slug == 'terms' else '\n\n'
    return f'''<main class="doc">
<p class="label"><span class="n">{name} /</span> {t(slug)}</p>
{langnav(slug, app)}
{sep.join(shown)}
</main>'''


def terms(name='PetroGram', changes=None):
    """The terms of use (language -> HTML). For another app: its name in place
    of PetroGram, then changes, a list of (old text, new text) per language."""
    secs = {}
    for l, m in json.loads(rd(T / 'terms.json')).items():
        m = {k: v.replace('PetroGram', name) for k, v in m.items()}
        for x, y in (changes or {}).get(l, []):
            hit = [k for k, v in m.items() if x in v]
            assert len(hit) == 1 and m[hit[0]].count(x) == 1, ('terms', name, l, x[:60])
            m[hit[0]] = m[hit[0]].replace(x, y)
        rtl = ' dir="rtl"' if l == 'ar' else ''
        hl = ' lang="zh-Hans"' if l == 'zh' else f' lang="{l}"'
        items = []
        for i in range(1, 13):
            if f'tm_{i}' not in m:
                break
            items.append(f'<h2>{i}. {html.escape(m[f"tm_{i}_t"])}</h2>\n<p>{html.escape(m[f"tm_{i}"])}</p>')
        secs[l] = f'''<section id="{l}"{hl}{rtl}>
<h1>{name} – {html.escape(m["tm_title"])}</h1>
<p>{html.escape(m["tm_intro"])}</p>
{chr(10).join(items)}
<p class="meta">{html.escape(m["tm_date"])}</p>
</section>'''
    return secs


terms_secs = terms()

exec(rd(T / 'privacy_texts.py'))  # defines PRIV and ZH_SECTION
old = rd(T / 'privacy_old.html')


def block_6b(app, lang_label):
    md = rd(app / 'docs/ACCOUNT_SETUP.md')
    i = md.index(f'**{lang_label}.** ')
    j = md.find('\n\n', i)
    txt = ' '.join(md[i:j].split('\n')).split('** ', 1)[1]
    num, rest = txt.split(' ', 1)
    title, body = rest.split('. ', 1)
    return f'<h2>{num.rstrip(".")}. {html.escape(title)}</h2>\n  <p>{html.escape(body)}</p>'


def blocks_6c(app, heading):
    md = rd(app / 'docs/PRIVACY_ADDITIONS.md')
    i = md.index(f'## {heading}\n')
    j = md.find('\n## ', i + 3)
    chunk = md[i:j if j > 0 else None]
    out = [f'<h2>{m.group(1).rstrip(".")}. {html.escape(m.group(2))}</h2>\n  <p>{html.escape(m.group(3))}</p>'
           for m in re.finditer(r'\*\*(6\S+?)\s(.+?)[.。]\*\*\s(.+)', chunk)]
    assert len(out) == 5, (heading, len(out))
    return '\n\n  '.join(out)


def policy(app):
    """The PetroGram privacy policy (language -> HTML), with sections 6b to 6g
    read from the docs of the app folder given."""
    secs = {}
    for l in ['en', 'az', 'ru', 'ar', 'es', 'fr']:
        a = old.index(f'<section id="{l}"')
        sec = old[a:old.index('</section>', a) + len('</section>')]
        p = PRIV[l]
        for x, y in p['replace']:
            assert sec.count(x) == 1, (l, x[:60], sec.count(x))
            sec = sec.replace(x, y)
        s0 = sec.index(p['sum_start'])
        s1 = sec.index(p['sum_end'], s0) + len(p['sum_end'])
        sec = sec[:s0] + p['summary'] + sec[s1:]
        k = sec.index('<h2>7.')
        sec = sec[:k] + block_6b(app, p['label6b']) + '\n\n  ' + blocks_6c(app, p['heading6c']) + '\n\n  ' + sec[k:]
        for marker, add in [(p['sec3'], p['bullet3']), (p['sec8'], p['bullets8'])]:
            m0 = sec.index(marker)
            m1 = sec.index('</ul>', m0)
            if marker == p['sec8']:          # the old last item ended the list with "."
                last = sec.rindex('.</li>', m0, m1)
                sec = sec[:last] + p['semi'] + sec[last + 1:]
                m1 = sec.index('</ul>', m0)
            sec = sec[:m1] + add + '\n  ' + sec[m1:]
        assert 'gmail' not in sec, l
        secs[l] = sec
    secs['zh'] = ZH_SECTION.replace('{BLOCKS6CF}', blocks_6c(app, '简体中文'))
    return secs


privacy_secs = policy(APP)

exec(rd(T / 'delete_texts.py'))   # defines delete_secs() and its rows of TX

# Geo-Rulers: the same policy with the sections 6b to 6g of its own app
# folder, then the differences listed in georulers_texts.py.
exec(rd(T / 'georulers_texts.py'))  # defines GEO_NAME, GEO_APP, geo_adapt(), GEO_TERMS
geo_privacy_secs = {l: geo_adapt(sec, GEO_PRIV[l], l, 25) for l, sec in policy(GEO).items()}
geo_terms_secs = terms(GEO_NAME, GEO_TERMS)


def geo_delete_secs():
    return {l: geo_adapt(sec, GEO_DELETE.get(l, []), l, 22)
            for l, sec in delete_secs(GEO_APP).items()}


def notfound():
    return f'''<main class="doc" style="text-align:center;padding:160px 24px">
<p class="label">404</p>
<h1>{t('nf_h1')}</h1>
<p><a href="{u('/')}">{t('nf_go')}</a></p>
</main>'''


# ----------------------------------------------- write every page, 3 times
JS = ['/assets/site.js']
for L in LANGS:
    out = OUT / PRE[L].lstrip('/')
    wr(out / 'index.html', page('home', home(), '/', ['/assets/land.js', '/assets/hero.js'] + JS))
    wr(out / 'petrogram/index.html', page('pg', petro(), '/petrogram/', ['/assets/hero.js'] + JS))
    wr(out / 'petrogram/terms/index.html', page('terms', doc('terms', terms_secs), '/petrogram/terms/', JS))
    wr(out / 'petrogram/privacy/index.html', page('privacy', doc('privacy', privacy_secs), '/petrogram/privacy/', JS))
    wr(out / 'petrogram/delete-account/index.html',
       page('delete', doc('delete-account', delete_secs()), '/petrogram/delete-account/', JS))
    # Geo-Rulers: its page, and its privacy policy, delete page and terms of use.
    wr(out / GEO_APP / 'index.html',
       page('gr', geo(), f'/{GEO_APP}/', ['/assets/land.js', '/assets/hero.js'] + JS, name=GEO_NAME, app=GEO_APP))
    wr(out / GEO_APP / 'privacy/index.html',
       page('privacy', doc('privacy', geo_privacy_secs, GEO_APP, GEO_NAME), f'/{GEO_APP}/privacy/', JS, name=GEO_NAME, app=GEO_APP))
    wr(out / GEO_APP / 'delete-account/index.html',
       page('delete', doc('delete-account', geo_delete_secs(), GEO_APP, GEO_NAME), f'/{GEO_APP}/delete-account/', JS, name=GEO_NAME, app=GEO_APP))
    wr(out / GEO_APP / 'terms/index.html',
       page('terms', doc('terms', geo_terms_secs, GEO_APP, GEO_NAME), f'/{GEO_APP}/terms/', JS, name=GEO_NAME, app=GEO_APP))
    wr(out / '404.html', page('nf', notfound(), '/404.html', JS, found=False))

# The list of pages for search engines, each with its other languages.
PATHS = ['/', '/petrogram/', '/petrogram/privacy/', '/petrogram/terms/', '/petrogram/delete-account/',
         f'/{GEO_APP}/', f'/{GEO_APP}/privacy/', f'/{GEO_APP}/terms/', f'/{GEO_APP}/delete-account/']
rows = ''.join(
    f'  <url><loc>{SITE}{PRE[l]}{p}</loc>'
    + ''.join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{SITE}{PRE[x]}{p}"/>' for x in LANGS)
    + '</url>\n' for p in PATHS for l in LANGS)
wr(OUT / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n'
   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
   + rows + '</urlset>\n')
print('built', ', '.join(LANGS))
