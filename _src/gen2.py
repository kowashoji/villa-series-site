# -*- coding: utf-8 -*-
# Villa Series — group redesign (Roos + Shippori Mincho + Archivo, white ground)
import json, os, re, shutil, html
from data import B, HOME_HERO, VACANCIES

OUT = "/home/claude/vs/site2"
import hashlib
VER = lambda f: hashlib.md5(open(f"/home/claude/vs/src2/{f}","rb").read()).hexdigest()[:8]
CSSV, JSV = VER("style.css"), VER("site.js")
SITE = "https://www.villa-series.jp"
E = html.escape
def key(i): return re.split(r"[~.]", i)[0][:12]
A = "https://villa-series-assets.pages.dev"
def L(i): return f"{A}/img/{key(i)}-l.webp"
def S(i): return f"{A}/img/{key(i)}-s.webp"
BY = {b["slug"]: b for b in B}
for n, b in enumerate(B): b["no"] = f"{n+1:02d}"
VAC = {v["slug"]: v for v in VACANCIES["buildings"]}

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500&family=Shippori+Mincho:wght@400;500&display=swap">'

def head(title, desc, path, og, lds, body):
    url = SITE + ("/" if path == "index" else "/" + path)
    ldt = "\n".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in lds)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VILLA SERIES">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<meta name="format-detection" content="telephone=no">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://villa-series-assets.pages.dev" crossorigin>
<link rel="preload" href="https://villa-series-assets.pages.dev/fonts/roos.woff2" as="font" type="font/woff2" crossorigin>
{FONTS}
<link rel="stylesheet" href="/style.css?v={CSSV}">
{ldt}
</head>
<body class="{body}">
<a class="skip" href="#main">本文へ移動</a>
"""

def header(active=None):
    bn = "".join(f'<a href="/{b["slug"]}"{" aria-current=\"page\"" if active==b["slug"] else ""}>{b["en"]}</a>' for b in B)
    a = lambda k: ' aria-current="page"' if active == k else ""
    return f"""<header class="hd">
  <div class="hd-in">
    <a class="wm" href="/" aria-label="VILLA SERIES ホーム">VILLA SERIES<sup>®</sup></a>
    <nav class="hd-nav" aria-label="サイト">
      <a href="/availability"{a("availability")}>空室情報</a>
      <a href="/contact"{a("contact")}>お問い合わせ</a>
    </nav>
  </div>
  <nav class="bn" aria-label="物件"><div class="bn-in">{bn}</div></nav>
</header>
<main id="main">
"""

FOOT = f"""</main>
<footer class="ft">
  <div class="ft-in">
    <div class="ft-co">
      <a class="ft-mark" href="https://www.kowa-shoji.co.jp" target="_blank" rel="noopener" aria-label="興和商事株式会社"><img src="/mark.png" alt="" width="34" height="34"></a>
      <div>
        <p class="ft-name">興和商事株式会社　不動産事業部</p>
        <p class="ft-l">〒150-0002 東京都渋谷区渋谷一丁目3番18号</p>
        <p class="ft-l">Tel <a href="tel:0334063661">03-3406-3661</a></p>
        <p class="ft-l">E-mail <a href="mailto:bukken@kowa-shoji.co.jp">bukken@kowa-shoji.co.jp</a></p>
        <p class="ft-l">月曜日～金曜日 8:00～15:00（土日祝日、年末年始休業）</p>
      </div>
    </div>
    <nav class="ft-nav" aria-label="フッター">
      <a href="/availability">空室情報</a><a href="/contact">お問い合わせ</a>
      <a class="ext" href="https://www.kowa-shoji.co.jp" target="_blank" rel="noopener">KOWA-SHOJI.CO.JP <span aria-hidden="true">→</span></a>
    </nav>
  </div>
  <p class="ft-c">© <span class="yr">2026</span> KOWA SHOJI CO., LTD.</p>
</footer>
<script src="/site.js?v=JSVPLACEHOLDER" defer></script>
</body>
</html>
"""

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "興和商事株式会社", "alternateName": "Kowa Shoji Co., Ltd.",
       "url": "https://www.kowa-shoji.co.jp", "logo": SITE + "/apple-touch-icon.png", "telephone": "+81-3-3406-6414",
       "email": "bukken@kowa-shoji.co.jp", "foundingDate": "1950-06-16",
       "address": {"@type": "PostalAddress", "postalCode": "150-0002", "addressRegion": "東京都", "addressLocality": "渋谷区",
                   "streetAddress": "渋谷一丁目3番18号", "addressCountry": "JP"}}

def write(path, h): open(f"{OUT}/{path}.html", "w", encoding="utf-8").write(h.replace("JSVPLACEHOLDER", JSV))
def ym(b): return b["built"][:4], b["built"][5:7]

def unit_html(v, u):
    return f'''<a class="unit" href="{A}/files/{u["pdf"]}" target="_blank" rel="noopener">
          <img src="{S(u["flyer"])}" alt="{E(BY[v["slug"]]["jp"])} {E(u["room"])} 物件資料" loading="lazy">
          <span class="u-t"><span class="u-room">{E(u["room"])}</span><span class="u-badge">{E(u["badge"])}</span>
          <span class="u-row"><span class="u-k">専有面積</span>{E(u["area"])}</span><span class="u-row"><span class="u-k">賃料（税込）</span>{E(u["rent"])}</span>
          <span class="u-pdf">物件資料 PDF <span aria-hidden="true">↗</span></span></span>
        </a>'''

def build():
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)

    # ---------------- home ----------------
    slides = "".join(f'<img src="{L(i)}" alt="" {"fetchpriority=\"high\" " if n==0 else "loading=\"lazy\" "}class="{"on" if n==0 else ""}">' for n, i in enumerate(HOME_HERO))
    cards = []
    for b in B:
        y, m = ym(b)
        cards.append(f'''      <li><a class="card" href="/{b["slug"]}">
        <span class="card-img"><img src="{S(b["thumb"])}" alt="{E(b["jp"])}（VILLA {b["en"]}）外観" loading="lazy"></span>
        <span class="card-meta"><span class="card-y">{y}</span><span class="card-no">No.{b["no"]}</span></span>
        <span class="card-jp">{E(b["jp"])}</span>
        <span class="card-en">VILLA {b["en"]}</span>
        <span class="card-d">{E(b["district"])}<span class="cd-x"><span class="dot">・</span>{y}年{m}月竣工</span></span>
      </a></li>''')
    rows = []
    for v in VACANCIES["buildings"]:
        for u in v["units"]:
            rows.append(f'<li><a href="{A}/files/{u["pdf"]}" target="_blank" rel="noopener" aria-label="{E(BY[v["slug"]]["jp"])} {E(u["room"])} 物件資料（PDF）"><span class="vr-b">{E(BY[v["slug"]]["jp"])}</span><span class="vr-r">{E(u["room"])}</span><span class="vr-a">{E(u["area"])}</span><span class="vr-p">{E(u["rent"])}</span><span class="vr-n">{E(u["badge"])}</span><span class="arr" aria-hidden="true">↗</span></a></li>')
    desc_home = "VILLA SERIES（ビラ・シリーズ）は、興和商事株式会社 不動産事業部が手がける都市型デザイナーズ・マンションブランドです。洗練されたデザインと上質な暮らしを追求し、独創性ある住宅空間を提供しています。"
    home = header() + f'''<section class="intro wrap">
  <div class="intro-t">
    <h1><span class="h1-jp">ビラ・シリーズ</span><span class="h1-sub">1964年より</span></h1>
  </div>
  <div class="intro-img hero-show" aria-hidden="true">{slides}</div>
</section>

<section class="sec wrap" id="residences">
  <h2 class="lab">物件<span>PROPERTIES</span></h2>
  <ul class="grid">
{chr(10).join(cards)}
  </ul>
</section>

<section class="sec wrap" id="vacancies">
  <h2 class="lab">空室<span>AVAILABILITY</span></h2>
  <div class="vt">
    <p class="vt-asof"><span class="js-asof">{VACANCIES["updated"]}</span> 現在</p>
    <ul class="vrows" id="vrows">
      {"".join(rows)}
    </ul>
    <p class="more"><a href="/availability">空室情報をすべて見る <span aria-hidden="true">→</span></a></p>
  </div>
</section>
''' + FOOT
    site_ld = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "VILLA SERIES", "inLanguage": "ja", "publisher": {"@id": SITE + "/#org"}},
        {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": n+1, "url": f"{SITE}/{b['slug']}", "name": b["jp"]} for n, b in enumerate(B)]}]}
    write("index", head("VILLA SERIES｜デザイナーズマンション｜興和商事株式会社", desc_home, "index", L(HOME_HERO[0]), [site_ld], "home") + home)

    # ---------------- buildings ----------------
    for n, b in enumerate(B):
        ids = b["imgs"].split(); hero, gal = ids[0], ids[1:]
        label = f'{b["jp"]}（Villa {b["en"].title()}）'
        y, m = ym(b)
        prev_b, next_b = B[n-1] if n > 0 else None, B[n+1] if n < len(B)-1 else None
        slides = "\n".join(f'        <img src="{L(i)}" alt="{E(label)} 写真 {k+1}" {"" if k==0 else "loading=\"lazy\" "}class="{"on" if k==0 else ""}">' for k, i in enumerate(gal))
        thumbs = "\n".join(f'        <button class="th{" on" if k==0 else ""}" type="button" aria-label="写真 {k+1}"><img src="{S(i)}" alt="" loading="lazy"></button>' for k, i in enumerate(gal))
        credit = f'\n      <p class="credit"><a href="{b["credit"][1]}" target="_blank" rel="noopener">{E(b["credit"][0])}</a></p>' if b.get("credit") else ""
        specs = [("名称", f'{b["jp"]}（{b["meaning"]}）'), ("竣工", b["built"]), ("所在地", b["address"]),
                 ("設計", b["architect"]), ("施工", b["builder"]), ("概要", b["overview"])]
        dl = "\n".join(f"        <div><dt>{k}</dt><dd>{E(v)}</dd></div>" for k, v in specs)
        model = ""
        if b.get("model"):
            mo = b["model"]; ph = mo["photos"].split()
            imgs = "".join(f'<a href="{L(i)}" class="lb"><img src="{L(i)}" alt="モデルルーム 写真 {k+1}" loading="lazy"></a>' for k, i in enumerate(ph))
            model = f'''
  <section class="row">
    <h2 class="lab">モデルルーム<span>MODEL ROOM</span></h2>
    <div class="row-c">
      <p class="prose">{"<br>".join(E(x) for x in mo["text"])}</p>
      <div class="model">
        <a href="{L(mo["plan"])}" class="lb plan"><img src="{L(mo["plan"])}" alt="モデルルーム間取り" loading="lazy"></a>
        <div class="model-ph">{imgs}</div>
      </div>
    </div>
  </section>'''
        vac = ""
        if VAC.get(b["slug"], {}).get("units"):
            us = VAC[b["slug"]]["units"]
            vac = f'''
  <section class="row">
    <h2 class="lab">空室<span>AVAILABILITY</span></h2>
    <div class="row-c">
      <p class="callout"><a href="/availability#{b["slug"]}">現在、{len(us)}件の募集住戸があります（{"、".join(E(u["room"]) for u in us)}） <span aria-hidden="true">→</span></a></p>
    </div>
  </section>'''
        pn = '<nav class="pn wrap" aria-label="前後の物件">'
        pn += (f'<a class="pn-p" href="/{prev_b["slug"]}"><span class="pn-k"><span aria-hidden="true">←</span> No.{prev_b["no"]}</span><span class="pn-n">{E(prev_b["jp"])}</span></a>' if prev_b else '<span></span>')
        pn += (f'<a class="pn-n2" href="/{next_b["slug"]}"><span class="pn-k">No.{next_b["no"]} <span aria-hidden="true">→</span></span><span class="pn-n">{E(next_b["jp"])}</span></a>' if next_b else '<span></span>')
        pn += '</nav>'
        content = header(b["slug"]) + f'''<article class="bld">
  <header class="bh wrap">
    <p class="bh-k"><span>No.{b["no"]}</span><span class="bh-y">{y}</span></p>
    <div class="bh-t">
      <h1>{E(b["jp"])}</h1>
      <p class="bh-en">VILLA {b["en"]}<sup>®</sup></p>
      <p class="bh-m">{E(b["meaning"])}<span class="dot">・</span>{E(b["district"])}</p>
    </div>
  </header>
  <figure class="bimg wrap"><img src="{L(hero)}" alt="{E(label)} 外観" fetchpriority="high"></figure>
  <div class="wrap">
  <section class="row">
    <h2 class="lab">紹介<span>ABOUT</span></h2>
    <div class="row-c"><p class="prose about">{E("".join(b["intro"]))}</p></div>
  </section>
  <section class="row">
    <h2 class="lab">物件概要<span>DETAILS</span></h2>
    <div class="row-c">
      <dl class="specs">
{dl}
      </dl>
    </div>
  </section>
  <section class="row">
    <h2 class="lab">写真<span>GALLERY</span></h2>
    <div class="row-c gallery">
      <div class="stage">
{slides}
        <button class="nav prev" type="button" aria-label="前の写真"></button>
        <button class="nav next" type="button" aria-label="次の写真"></button>
        <span class="count" aria-hidden="true"><span class="cur">1</span> / {len(gal)}</span>
      </div>
      <div class="thumbs">
{thumbs}
      </div>{credit}
    </div>
  </section>{model}{vac}
  </div>
  {pn}
</article>
''' + FOOT
        bld = {"@context": "https://schema.org", "@graph": [
            {"@type": "ApartmentComplex", "name": b["jp"], "alternateName": "Villa " + b["en"].title(),
             "url": f"{SITE}/{b['slug']}", "description": "".join(b["intro"]),
             "image": [L(hero)] + [L(i) for i in gal[:3]],
             "numberOfAccommodationUnits": b["units"],
             "address": {"@type": "PostalAddress", "addressRegion": "東京都", "addressLocality": b["locality"], "streetAddress": b["street"], "addressCountry": "JP"},
             "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in specs[1:5]],
             "provider": ORG},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "VILLA SERIES", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": b["jp"], "item": f"{SITE}/{b['slug']}"}]}]}
        write(b["slug"], head(f'{b["jp"]}（Villa {b["en"].title()}）｜{b["district"]}・{b["year"]}年竣工｜VILLA SERIES',
                               "".join(b["intro"])[:120], b["slug"], L(hero), [bld], "building") + content)

    # ---------------- availability ----------------
    blocks = []
    for v in VACANCIES["buildings"]:
        b = BY[v["slug"]]
        us = "\n        ".join(unit_html(v, u) for u in v["units"]) if v["units"] else '<p class="full">ただいま満室となっております</p>'
        blocks.append(f'''  <section class="row" id="{v["slug"]}">
    <div class="lab vb-h"><a href="/{v["slug"]}"><span class="vb-jp">{E(b["jp"])}</span><span>VILLA {b["en"]}</span></a></div>
    <div class="row-c">
      <p class="tag">{"<br>".join(E(t) for t in v["tagline"])}</p>
      <div class="units">
        {us}
      </div>
      <iframe class="map" title="{E(b["jp"])} 地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={b["address"]}&amp;z=16&amp;output=embed"></iframe>
    </div>
  </section>''')
    info = '''      <dl class="specs">
        <div><dt>問い合わせ先</dt><dd>興和商事株式会社　不動産事業部</dd></div>
        <div><dt>Tel</dt><dd><a href="tel:0334063661">03-3406-3661</a>（不動産事業部直通）</dd></div>
        <div><dt>Fax</dt><dd>03-3406-3662</dd></div>
        <div><dt>E-mail</dt><dd><a href="mailto:bukken@kowa-shoji.co.jp?subject=%E7%89%A9%E4%BB%B6%E6%83%85%E5%A0%B1">bukken@kowa-shoji.co.jp</a>（物件情報）</dd></div>
        <div><dt>営業日・時間</dt><dd>月曜日～金曜日の8：00～15：00<br>土日祝日、年末年始はお休みをいただいております</dd></div>
      </dl>'''
    av = header("availability") + f'''<div class="page wrap">
  <header class="ph">
    <p class="eyebrow">AVAILABILITY</p>
    <h1>空室情報</h1>
    <p class="asof"><span class="js-asof">{VACANCIES["updated"]}</span>　現在の空室情報をご覧いただけます。</p>
  </header>
  <div id="vblocks">
{chr(10).join(blocks)}
  </div>
</div>
''' + FOOT
    write("availability", head("空室情報｜VILLA SERIES（ビラ・シリーズ）", f'ビラ・シリーズの空室情報（{VACANCIES["updated"]}現在）。募集住戸の賃料・専有面積・物件資料をご覧いただけます。', "availability", L(HOME_HERO[0]), [], "avail") + av)

    # ---------------- contact ----------------
    ct = header("contact") + f'''<div class="page wrap">
  <header class="ph">
    <p class="eyebrow">CONTACT</p>
    <h1>お問い合わせ</h1>
    <p class="asof">興和商事株式会社　不動産事業部</p>
  </header>
  <section class="row">
    <h2 class="lab">不動産事業部<span>REAL ESTATE</span></h2>
    <div class="row-c">
      <dl class="specs">
        <div><dt>Tel</dt><dd><a href="tel:0334063661">03-3406-3661</a>（不動産事業部直通）</dd></div>
        <div><dt>Fax</dt><dd>03-3406-3662</dd></div>
        <div><dt>E-mail</dt><dd><a href="mailto:bukken@kowa-shoji.co.jp?subject=%E7%89%A9%E4%BB%B6%E6%83%85%E5%A0%B1">bukken@kowa-shoji.co.jp</a>（物件情報）</dd></div>
        <div><dt>営業日・時間</dt><dd>月曜日～金曜日の8：00～15：00<br>土日祝日、年末年始はお休みをいただいております</dd></div>
      </dl>
    </div>
  </section>
  <section class="row">
    <h2 class="lab">会社案内<span>COMPANY</span></h2>
    <div class="row-c">
      <dl class="specs">
        <div><dt>事業所名</dt><dd>興和商事株式会社</dd></div>
        <div><dt>創業設立</dt><dd>1950年06月16日</dd></div>
        <div><dt>住所</dt><dd>〒150-0002 東京都渋谷区渋谷一丁目3番18号</dd></div>
        <div><dt>Tel</dt><dd><a href="tel:0334066414">03-3406-6414</a>（代表）</dd></div>
        <div><dt>Fax</dt><dd>03-5485-8681</dd></div>
        <div><dt>Homepage</dt><dd><a href="https://www.kowa-shoji.co.jp" target="_blank" rel="noopener">www.kowa-shoji.co.jp</a></dd></div>
        <div><dt>免許証番号</dt><dd>東京都知事免許 ( 17 )第5258号</dd></div>
      </dl>
      <iframe class="map wide" title="興和商事株式会社 地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=東京都渋谷区渋谷1-3-18&amp;z=16&amp;output=embed"></iframe>
    </div>
  </section>
</div>
''' + FOOT
    write("contact", head("お問い合わせ｜VILLA SERIES（ビラ・シリーズ）", "ビラ・シリーズに関するお問い合わせ。興和商事株式会社 不動産事業部 Tel 03-3406-3661（月～金 8:00～15:00）、E-mail bukken@kowa-shoji.co.jp。", "contact", L(HOME_HERO[0]), [{"@context": "https://schema.org", **ORG}], "contact") + ct)

    write("404", head("ページが見つかりません｜VILLA SERIES", "お探しのページは見つかりませんでした。", "404", L(HOME_HERO[0]), [], "nf") + header() +
          '<div class="page wrap"><header class="ph"><p class="eyebrow">404</p><h1>ページが見つかりません</h1><p class="asof">お探しのページは移動または削除された可能性があります。</p><p class="links"><a href="/">VILLA SERIES トップへ <span aria-hidden="true">→</span></a></p></header></div>\n' + FOOT)

    # ---------------- data + static ----------------
    vj = {"_使い方": "空室情報はこのファイルだけで更新できます。updated に日付、units に住戸を追加・削除してください。満室の場合は units を [] にします。", "updated": VACANCIES["updated"],
          "buildings": [{"slug": v["slug"], "name": BY[v["slug"]]["jp"], "en": "VILLA " + BY[v["slug"]]["en"], "address": BY[v["slug"]]["address"], "tagline": v["tagline"],
                         "units": [{"room": u["room"], "badge": u["badge"], "area": u["area"], "rent": u["rent"], "flyer": S(u["flyer"]), "pdf": A + "/files/" + u["pdf"]} for u in v["units"]]}
                        for v in VACANCIES["buildings"]]}
    json.dump(vj, open(f"{OUT}/vacancies.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for f in ("style.css", "site.js"): shutil.copy(f"/home/claude/vs/src2/{f}", OUT)
    for f in ("favicon-32.png", "apple-touch-icon.png", "mark.png"): shutil.copy(f"/home/claude/vs/src/{f}", OUT)
    urls = ["/"] + [f"/{b['slug']}" for b in B] + ["/availability", "/contact"]
    open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    open(f"{OUT}/_headers", "w").write("/vacancies.json\n  Cache-Control: no-cache\n")
    open(f"{OUT}/_redirects", "w").write("/index /  301\n/home /  301\n")
build()
