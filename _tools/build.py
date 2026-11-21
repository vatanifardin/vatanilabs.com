#!/usr/bin/env python3
"""Builds every page of vatanilabs.com as plain HTML.

Run:  python3 -I _tools/build.py   (from the site folder)
Inputs in this folder: flat_map.json (from make_land.py), terms.json (the
app's terms of use in 7 languages), privacy_old.html + privacy_texts.py
(the privacy policy and its 21 November 2026 changes).
The folder name starts with "_", so GitHub Pages does not publish it.
"""
import html, json, re
from pathlib import Path

T = Path(__file__).resolve().parent
OUT = T.parent
APP = Path('/Users/fardinvatani/Developer/petrogram')

MARK = ('<svg viewBox="0 0 120 100" aria-hidden="true">'
        '<polyline points="15,15 60,85 105,15" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polyline points="35,15 60,55 85,15" fill="none" stroke="#2cc4b8" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">')


def ico(body):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


I_OFFLINE = ico('<path d="M2 8.5a15 15 0 0 1 20 0"/><path d="M5.5 12.2a10 10 0 0 1 13 0"/><path d="M9 15.8a5 5 0 0 1 6 0"/><circle cx="12" cy="19.2" r=".9" fill="currentColor"/><path d="M4 3l16 18"/>')
I_FOCUS = ico('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1" fill="currentColor"/>')
I_CHECK = ico('<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.8 2.8L16 9.5"/>')
I_SHIELD = ico('<path d="M12 3l7 3v5.5c0 4.4-3 8-7 9.5-4-1.5-7-5.1-7-9.5V6l7-3z"/><path d="M9 12l2.2 2.2L15 10.5"/>')
I_SWAP = ico('<path d="M7 4v14m0 0l-3-3m3 3l3-3M17 20V6m0 0l-3 3m3-3l3 3"/>')
I_FLAME = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5c1 3.2 4.5 4.8 4.5 9.2a4.5 4.5 0 0 1-9 0c0-1.7.8-2.9 1.7-3.8.3 1.3 1 2 1.7 2C11 7.800 10.400 5.200 12 2.500z"/></svg>'


def page(title, desc, body, path='/', scripts=()):
    tags = ''.join(f'<script src="{s}" defer></script>\n' for s in scripts)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#04060c">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://vatanilabs.com/assets/img/icon-512.png">
<meta property="og:url" content="https://vatanilabs.com{path}">
<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.VL_READY)document.documentElement.classList.remove('js')}},4000)</script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Vatani Labs home">{MARK}<b>Vatani</b><span>Labs</span></a>
    <nav class="nav" aria-label="Main">
      <a href="/#apps">Apps</a>
      <a href="/#principles">How we build</a>
      <a class="btn" href="/#contact">Contact</a>
    </nav>
  </div>
</header>
{body}
<footer class="site-footer">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Vatani Labs home">{MARK}<b>Vatani</b><span>Labs</span></a>
    <span>© 2026 Vatani Labs · Baku, Azerbaijan</span>
    <nav aria-label="Footer">
      <a href="/petrogram/">PetroGram</a>
      <a href="/petrogram/privacy/">Privacy policy</a>
      <a href="/petrogram/terms/">Terms of use</a>
      <a href="mailto:support@vatanilabs.com">support@vatanilabs.com</a>
    </nav>
  </div>
  <div class="wordmark" aria-hidden="true">Vatani Labs</div>
</footer>
{tags}</body>
</html>
'''


# ------------------------------------------------- the living feature tiles
def tile(cls, viz, cap, title, text, d=0):
    return (f'<article class="tile glow rv {cls}" style="--d:{d:.2f}s">\n<div class="viz">{viz}</div>\n'
            f'<div class="cap">{cap}</div><h4>{title}</h4><p>{text}</p>\n</article>')


def t_map(cls, d=0):
    dots = ''.join(f'M{(lon + 180) * 2:g} {(84 - lat) * 2:g}h0' for lon, lat in json.loads((T / 'flat_map.json').read_text()))
    # Well-known oil and gas regions (lon, lat).
    pins = [(-102.5, 32), (-90, 27.5), (-113, 55.5), (-42, -24.5), (2.5, 58.5), (6, 4.8),
            (50.5, 40.3), (50.5, 27), (73, 61.5), (118.5, 38.5), (116, -20.5)]
    marks = ''.join(
        f'<g transform="translate({(lon + 180) * 2:g} {(84 - lat) * 2:g})"><circle class="ring" r="3" style="--d:{(i * 0.37) % 2.8:.2f}s"/><circle class="core" r="2.6"/></g>'
        for i, (lon, lat) in enumerate(pins))
    viz = (f'<div class="vmap"><svg viewBox="0 0 720 284" role="img" aria-label="Dotted world map with oil and gas regions">'
           f'<path class="dots" d="{dots}"/>{marks}</svg></div>')
    return tile(cls, viz, 'Explore', 'Offline maps of the energy world',
                'Basins, fields, pipelines, refineries and active drilling rigs, with no signal needed.', d)


def t_conv(cls, d=0):
    viz = ('<div class="conv" data-conv aria-label="Unit converter example">'
           '<div class="row"><span class="num" data-a>1</span><span class="unit" data-ua>bbl</span></div>'
           f'<div class="swap">{I_SWAP}</div>'
           '<div class="row out"><span class="num" data-b>158.987</span><span class="unit" data-ub>L</span></div></div>')
    return tile(cls, viz, 'Calculate', 'Converter and calculators',
                'Units, drilling, production and well-control formulas, with history and favourites.', d)


def t_flash(cls, d=0):
    viz = ('<div class="flash" aria-label="Flashcard example"><div class="flash-in">'
           '<div class="face front"><small>Term</small><b>Blowout preventer</b></div>'
           '<div class="face back"><small>Meaning</small><span>Valves at the wellhead that seal the well if pressure control is lost.</span></div>'
           '</div></div>')
    return tile(cls, viz, 'Learn', '500 terms, as flashcards',
                'Clear definitions with related terms, and spaced repetition that remembers for you.', d)


def t_quiz(cls, d=0):
    viz = ('<div class="quiz" aria-label="Quiz example">'
           '<div class="q"><span>What does BOP stand for?</span>'
           '<span class="ringbox"><svg viewBox="0 0 44 44"><circle class="tr" cx="22" cy="22" r="18"/><circle class="pr" cx="22" cy="22" r="18"/></svg>8/10</span></div>'
           '<div class="opt"><i></i>Bottom oil pressure</div>'
           '<div class="opt ok"><i>✓</i>Blowout preventer</div>'
           '<div class="opt"><i></i>Barrel of petroleum</div>'
           f'<span class="streak">{I_FLAME} 12-day streak</span></div>')
    return tile(cls, viz, 'Practise', '600 questions and an exam mode',
                'Practise by topic, keep a daily streak, earn badges, and join the scoreboard if you like.', d)


def t_lang(cls, d=0):
    words = 'Knowledge|Bilik|Знание|معرفة|Conocimiento|Savoir|知识'
    chips = ''.join(f'<span class="chip{" on" if i == 0 else ""}">{c}</span>'
                    for i, c in enumerate(['EN', 'AZ', 'RU', 'AR', 'ES', 'FR', '中文']))
    viz = (f'<div class="langs7"><div class="langword" data-words="{words}">Knowledge</div>'
           f'<div class="chips">{chips}</div></div>')
    return tile(cls, viz, 'Understand', 'Seven languages',
                'English, Azerbaijani, Russian, Arabic, Spanish, French and Simplified Chinese, fully translated.', d)


def t_market(cls, d=0):
    l1 = 'M0 122 C 30 112, 50 92, 80 98 S 130 62, 160 72 S 210 112, 240 94 S 300 32, 330 46 S 385 24, 410 30'
    l2 = 'M0 142 C 40 134, 70 122, 100 128 S 160 102, 200 110 S 260 132, 300 114 S 380 72, 410 80'
    viz = ('<div class="chart"><svg viewBox="0 0 420 170" role="img" aria-label="Price chart drawing">'
           '<defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2cc4b8" stop-opacity=".32"/><stop offset="1" stop-color="#2cc4b8" stop-opacity="0"/></linearGradient></defs>'
           '<line class="grid" x1="0" x2="420" y1="40" y2="40"/><line class="grid" x1="0" x2="420" y1="85" y2="85"/><line class="grid" x1="0" x2="420" y1="130" y2="130"/>'
           f'<path class="area" fill="url(#ar)" d="{l1} L410 170 L0 170 Z"/>'
           f'<path class="l2" pathLength="1" d="{l2}"/><path class="l1" pathLength="1" d="{l1}"/>'
           '<g class="end" transform="translate(410 30)"><circle class="ring" r="4"/><circle r="4" fill="#7ff0e4"/></g>'
           '</svg><div class="chips"><span class="chip on">Brent</span><span class="chip">WTI</span><span class="chip">Henry Hub</span><span class="chip">Rig counts</span></div></div>')
    return tile(cls, viz, 'Follow', 'Prices and rig counts',
                'Oil and gas prices and Baker Hughes rig counts, saved so you can read them offline.', d)


def t_talk(cls, d=0):
    viz = ('<div class="talk" aria-label="Interview question example">'
           '<div class="ask">What are the primary and secondary well barriers?</div>'
           '<div class="ans"><small>Model answer</small><div class="ln"></div><div class="ln"></div><div class="ln"></div></div></div>')
    return tile(cls, viz, 'Prepare', 'Interview preparation',
                'Real questions with model answers. Mark what you know and practise the rest.', d)


def t_offline(cls, d=0):
    viz = f'<div class="offline"><span></span><span></span><span></span><div class="core">{I_OFFLINE}</div></div>'
    return tile(cls, viz, 'Anywhere', 'No signal? No problem.',
                'On a rig, at a remote site or on a plane: everything important works offline.', d)


def t_more(cls, d=0):
    items = ['Company structures', 'World map of companies', 'Cheat sheets', 'HSE guides', 'Well tools', 'Events calendar',
             'Question of the day', 'Badges', 'Notes', 'Backup and sync', 'Home-screen widget', 'Dark mode']
    viz = '<div class="chips" style="justify-content:center;max-width:520px">' + ''.join(f'<span class="chip">{i}</span>' for i in items) + '</div>'
    return tile(cls, viz, 'And more', 'Small things that add up',
                'Everything a pocket reference should have, and nothing that gets in the way.', d)


def phone(img, alt, i=None):
    st = f' style="--i:{i};--a:{abs(i)}"' if i is not None else ''
    return f'<div class="phone"{st}><img src="/assets/img/{img}" alt="{html.escape(alt)}" loading="lazy"></div>'


def band(words):
    one = ''.join(f'<span class="{"f" if i % 2 == 0 else ""}">{w}<i>✦</i></span>' for i, w in enumerate(words))
    return f'<div class="band" aria-hidden="true"><div class="band-track">{one}{one}</div></div>'


# ------------------------------------------------------------------ home
HOME = f'''<main>
<section class="hero" aria-label="Introduction">
  <div class="sculpt"><canvas id="sculpture" data-shapes="mark,globe,drop" aria-hidden="true"></canvas><div class="sculpt-cap" id="sculpture-cap"></div></div>
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill rv"><i></i>Independent app studio · Baku</span>
      <h1 class="rv" style="--d:.08s">Knowledge,<br><em class="s">simplified.</em></h1>
      <p class="lead rv" style="--d:.16s">We turn expert knowledge into focused apps you can carry anywhere: fast, clear, multilingual, and working without a signal.</p>
      <div class="actions rv" style="--d:.24s">
        <a class="btn solid" href="#apps">Explore our apps <span class="arr">→</span></a>
        <a class="btn" href="#contact">Get in touch</a>
      </div>
    </div>
  </div>
  <div class="scroll-hint" aria-hidden="true">Scroll</div>
</section>

<div class="stats">
  <div class="wrap">
    <div class="stat rv"><b data-count="500">500</b><span>Glossary terms</span></div>
    <div class="stat rv" style="--d:.08s"><b data-count="600">600</b><span>Quiz questions</span></div>
    <div class="stat rv" style="--d:.16s"><b data-count="7">7</b><span>Languages</span></div>
    <div class="stat rv" style="--d:.24s"><b><span data-count="100">100</span><small>%</small></b><span>Works offline</span></div>
  </div>
</div>
{band(['Offline first', 'Simple', 'Accurate', 'Private', 'Multilingual', 'Focused'])}

<section class="block" id="apps">
  <div class="wrap">
    <div class="block-head">
      <div class="rv">
        <p class="label"><span class="n">01 /</span> Our apps</p>
        <h2>One studio.<br><span class="grey">Focused</span> <em class="s">apps.</em></h2>
      </div>
      <p class="rv" style="--d:.1s">Each app is built for one field and made with the same care: offline first, simple to use, accurate, and respectful of your privacy.</p>
    </div>

    <div class="tabs rv" role="tablist" aria-label="Apps">
      <button class="tab" role="tab" id="tab-petrogram" aria-controls="panel-petrogram" aria-selected="true"><span class="n">01</span>PetroGram</button>
      <button class="tab" role="tab" id="tab-next" aria-controls="panel-next" aria-selected="false" tabindex="-1"><span class="n">02</span>Next app</button>
    </div>

    <div class="panel" role="tabpanel" id="panel-petrogram" aria-labelledby="tab-petrogram">
      <div class="app-line rv">
        <img src="/assets/img/petrogram-icon.png" alt="PetroGram app icon">
        <div><h3>PetroGram</h3><div class="sub">The pocket reference for oil &amp; gas.</div></div>
        <div class="chips"><span class="chip on">Coming soon</span><span class="chip">Android</span><span class="chip">iPhone</span></div>
      </div>
      <div class="bento">
        {t_map('w7')}
        {t_conv('w5', .08)}
        {t_flash('', 0)}
        {t_quiz('', .08)}
        {t_lang('', .16)}
      </div>
      <div class="actions rv" style="margin-top:26px"><a class="btn solid" href="/petrogram/">Discover PetroGram <span class="arr">→</span></a></div>
    </div>

    <div class="panel" role="tabpanel" id="panel-next" aria-labelledby="tab-next" hidden>
      <div class="soon">
        <div class="orbit">{MARK}</div>
        <p class="label">In development</p>
        <h3>More focused apps are <em class="s">on the way.</em></h3>
        <p>New fields, the same principles. Want to hear when they launch? Write to us.</p>
        <div class="actions" style="justify-content:center;margin-top:28px"><a class="btn" href="mailto:support@vatanilabs.com?subject=Tell%20me%20about%20new%20apps">Keep me posted <span class="arr">→</span></a></div>
      </div>
    </div>

    <div class="showcase-foot">
      <span>Built offline-first. Made in Baku.</span>
      <div class="pager">
        <button type="button" id="prev" aria-label="Previous app">←</button>
        <span id="count">01 / 02</span>
        <button type="button" id="next" aria-label="Next app">→</button>
      </div>
    </div>
  </div>
</section>

<section class="block" id="principles">
  <div class="wrap">
    <div class="block-head">
      <div class="rv">
        <p class="label"><span class="n">02 /</span> How we build</p>
        <h2>Small team.<br><span class="grey">Clear</span> <em class="s">principles.</em></h2>
      </div>
      <p class="rv" style="--d:.1s">Whatever the topic, every Vatani Labs app follows the same four rules.</p>
    </div>
    <div class="grid4">
      <div class="card glow rv"><div class="ico">{I_OFFLINE}</div><h3>Offline first</h3><p>On a rig, at a mine or on a plane: the answer should not depend on a signal.</p></div>
      <div class="card glow rv" style="--d:.08s"><div class="ico">{I_FOCUS}</div><h3>Simple and focused</h3><p>One clear purpose per app, no clutter, readable at any text size.</p></div>
      <div class="card glow rv" style="--d:.16s"><div class="ico">{I_CHECK}</div><h3>Accurate content</h3><p>Carefully prepared, checked against sources, and improved with every report.</p></div>
      <div class="card glow rv" style="--d:.24s"><div class="ico">{I_SHIELD}</div><h3>Privacy respected</h3><p>No unnecessary data. What you write stays on your phone unless you choose otherwise.</p></div>
    </div>
  </div>
</section>

<section class="block" id="contact" style="padding-top:40px">
  <div class="wrap">
    <div class="contact-card rv">
      <p class="label"><span class="n">03 /</span> Contact</p>
      <h2>Questions, ideas<br>or <em class="s">corrections?</em></h2>
      <p>We read every message and reply personally. Reports from the people who use our apps make them better.</p>
      <a class="mail" href="mailto:support@vatanilabs.com">support@vatanilabs.com <span class="arr">→</span></a>
    </div>
  </div>
</section>
</main>'''

# ------------------------------------------------------------- PetroGram
shots = [('2_learn', 'Learning paths'), ('3_upstream', 'Upstream tools'), ('1_home', 'Home'),
         ('5_maps', 'Offline maps'), ('4_quiz', 'Quiz')]
fan = '\n'.join(phone(f'pg-{n}.jpg', a, i - 2) for i, (n, a) in enumerate(shots))
PETRO = f'''<main>
<section class="app-hero">
  <div class="sculpt"><canvas id="sculpture" data-shapes="drop" aria-hidden="true"></canvas></div>
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill rv"><i></i>App 01 · Oil &amp; gas</span>
      <div class="top rv" style="--d:.08s">
        <img class="app-icon" src="/assets/img/petrogram-icon.png" alt="PetroGram app icon">
        <h1>Petro<em class="s">Gram</em></h1>
      </div>
      <p class="lead rv" style="--d:.16s">The offline pocket reference for oil &amp; gas professionals and students. Calculate, learn, explore and prepare, in seven languages.</p>
      <div class="actions rv" style="--d:.24s">
        <span class="btn" aria-disabled="true">App Store · coming soon</span>
        <span class="btn" aria-disabled="true">Google Play · coming soon</span>
      </div>
      <p class="store-note rv" style="--d:.3s">Free with ads · one purchase removes them · no account needed</p>
    </div>
  </div>
</section>
{band(['Calculators', 'Glossary', 'Flashcards', 'Quizzes', 'Maps', 'Market', 'Interviews', 'Cheat sheets'])}

<section class="block">
  <div class="wrap">
    <div class="block-head">
      <div class="rv">
        <p class="label"><span class="n">Inside /</span> Features</p>
        <h2>Everything in one app.<br><span class="grey">Online or</span> <em class="s">offline.</em></h2>
      </div>
      <p class="rv" style="--d:.1s">From the first formula to the next interview: the tools and knowledge of the industry, always in your pocket.</p>
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
        <p class="label"><span class="n">Screens /</span> The real thing</p>
        <h2>Clean, calm,<br><span class="grey">made for</span> <em class="s">work.</em></h2>
      </div>
      <p class="rv" style="--d:.1s">Light and dark mode, large text, right-to-left Arabic: the app adapts to you, not the other way round.</p>
    </div>
    <div class="fan rv" aria-label="Screens of the app">
{fan}
    </div>
  </div>
</section>

<section class="block" style="padding-top:20px">
  <div class="wrap">
    <div class="grid3">
      <div class="card glow rv"><span class="label">Support</span><h3>Need help?</h3><p>Write to <a href="mailto:support@vatanilabs.com">support@vatanilabs.com</a>, or use Contact in the app.</p></div>
      <div class="card glow rv" style="--d:.08s"><span class="label">Privacy</span><h3>Privacy policy</h3><p>What the app stores and sends, in seven languages. <a href="/petrogram/privacy/">Read it →</a></p></div>
      <div class="card glow rv" style="--d:.16s"><span class="label">Terms</span><h3>Terms of use</h3><p>Short and in plain language. <a href="/petrogram/terms/">Read them →</a></p></div>
    </div>
  </div>
</section>
</main>'''

# ----------------------------------------------------------------- terms
LANG_NAMES = {'en': 'English', 'az': 'Azərbaycanca', 'ru': 'Русский', 'ar': 'العربية',
              'es': 'Español', 'fr': 'Français', 'zh': '简体中文'}
terms = json.loads((T / 'terms.json').read_text())
tparts = []
for l, m in terms.items():
    rtl = ' dir="rtl"' if l == 'ar' else ''
    hl = ' lang="zh-Hans"' if l == 'zh' else f' lang="{l}"'
    items = []
    for i in range(1, 13):
        if f'tm_{i}' not in m:
            break
        items.append(f'<h2>{i}. {html.escape(m[f"tm_{i}_t"])}</h2>\n<p>{html.escape(m[f"tm_{i}"])}</p>')
    tparts.append(f'''<section id="{l}"{hl}{rtl}>
<h1>PetroGram – {html.escape(m["tm_title"])}</h1>
<p>{html.escape(m["tm_intro"])}</p>
{chr(10).join(items)}
<p class="meta">{html.escape(m["tm_date"])}</p>
</section>''')
langnav = '<nav class="langs" aria-label="Languages">' + ''.join(
    f'<a href="#{l}">{n}</a>' for l, n in LANG_NAMES.items()) + '</nav>'
TERMS = f'''<main class="doc">
<p class="label"><span class="n">PetroGram /</span> Terms of use</p>
{langnav}
{chr(10).join(tparts)}
</main>'''

# --------------------------------------------------------------- privacy
exec((T / 'privacy_texts.py').read_text())  # defines PRIV and ZH_SECTION
old = (T / 'privacy_old.html').read_text()


def block_6b(lang_label):
    md = (APP / 'docs/ACCOUNT_SETUP.md').read_text()
    i = md.index(f'**{lang_label}.** ')
    j = md.find('\n\n', i)
    txt = ' '.join(md[i:j].split('\n')).split('** ', 1)[1]
    num, rest = txt.split(' ', 1)
    title, body = rest.split('. ', 1)
    return f'<h2>{num.rstrip(".")}. {html.escape(title)}</h2>\n  <p>{html.escape(body)}</p>'


def blocks_6c(heading):
    md = (APP / 'docs/PRIVACY_ADDITIONS.md').read_text()
    i = md.index(f'## {heading}\n')
    j = md.find('\n## ', i + 3)
    chunk = md[i:j if j > 0 else None]
    out = [f'<h2>{m.group(1).rstrip(".")}. {html.escape(m.group(2))}</h2>\n  <p>{html.escape(m.group(3))}</p>'
           for m in re.finditer(r'\*\*(6\S+?)\s(.+?)[.。]\*\*\s(.+)', chunk)]
    assert len(out) == 4, (heading, len(out))
    return '\n\n  '.join(out)


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
    sec = sec[:k] + block_6b(p['label6b']) + '\n\n  ' + blocks_6c(p['heading6c']) + '\n\n  ' + sec[k:]
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
privacy_body = '\n\n'.join(secs.values()) + '\n\n' + ZH_SECTION.replace('{BLOCKS6CF}', blocks_6c('简体中文'))
PRIVACY = f'''<main class="doc">
<p class="label"><span class="n">PetroGram /</span> Privacy policy</p>
{langnav}
{privacy_body}
</main>'''

NOTFOUND = '''<main class="doc" style="text-align:center;padding:160px 24px">
<p class="label">404</p>
<h1>This page does <em class="s">not exist.</em></h1>
<p><a href="/">Go to the home page →</a></p>
</main>'''

JS = ['/assets/site.js']
(OUT / 'index.html').write_text(page('Vatani Labs · Knowledge, simplified',
    'Vatani Labs is an independent app studio building focused, offline-first apps that put expert knowledge in your pocket.',
    HOME, '/', ['/assets/land.js', '/assets/hero.js'] + JS))
(OUT / 'petrogram/index.html').write_text(page('PetroGram · Vatani Labs',
    'PetroGram: the offline pocket reference for oil & gas, in seven languages.', PETRO, '/petrogram/', ['/assets/hero.js'] + JS))
(OUT / 'petrogram/terms/index.html').write_text(page('PetroGram terms of use · Vatani Labs',
    'Terms of use of the PetroGram app.', TERMS, '/petrogram/terms/', JS))
(OUT / 'petrogram/privacy/index.html').write_text(page('PetroGram privacy policy · Vatani Labs',
    'Privacy policy of the PetroGram app, in seven languages.', PRIVACY, '/petrogram/privacy/', JS))
(OUT / '404.html').write_text(page('Not found · Vatani Labs', 'Page not found.', NOTFOUND, '/404.html', JS))
print('built')
