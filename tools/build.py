"""GTM 코스메틱스 국문 메인 시안 A·B + 선택 화면 생성.
상품·메뉴·푸터는 data/*.json 하나에서 두 시안이 함께 사용한다.
실행: python3 -I tools/build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
P = json.load(open(ROOT / "data" / "products.json", encoding="utf-8"))
S = json.load(open(ROOT / "data" / "site.json", encoding="utf-8"))
REAL = "https://gtm.uriweb.kr"
PROD = {p["idx"]: p for p in P["products"]}
CATS = P["categories"]
FONT = "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"
e = html.escape


def summary(idx):
    return S["summaries"].get(str(idx), "")


def price_html(p, cls="price"):
    if p["asking"] or not p["price"]:
        return f'<p class="{cls}"><span class="ask">가격문의</span></p>'
    if p["sale"]:
        return (f'<p class="{cls}"><del>{e(p["price"])}</del> <span class="pct">{e(p["pct"] or "")}</span> '
                f'<strong>{e(p["sale"])}</strong></p>')
    return f'<p class="{cls}"><strong>{e(p["price"])}</strong></p>'


def card(idx, extra="", show_desc=False):
    p = PROD[idx]
    desc = f'<p class="card-desc">{e(summary(idx))}</p>' if show_desc and summary(idx) else ""
    return (f'<li class="card {extra}"><button type="button" class="card-btn" data-preview="{idx}" aria-label="{e(p["name"])} 미리보기">'
            f'<span class="card-img"><img src="../assets/img/{p["img"]}" alt="{e(p["name"])}" loading="lazy" width="900" height="900"></span>'
            f'<span class="card-body"><span class="card-name">{e(p["name"])}</span>{desc}{price_html(p)}</span></button></li>')


def ext(path, label, cls=""):
    return f'<a href="{REAL}{path}" target="_blank" rel="noopener" class="{cls}">{e(label)}</a>'


def logo(cls="logo"):
    return f'<a href="#top" class="{cls}" aria-label="GTM 코스메틱스 홈"><img src="../assets/img/etc/logo.png" alt="GTM 코스메틱스" width="600" height="321"></a>'


def header(concept):
    items = []
    for n in S["nav"]:
        kids = "".join(f"<li>{ext(c['url'], c['label'])}</li>" for c in n["children"])
        items.append(f'<li class="nav-item"><button type="button" class="nav-top" aria-expanded="false">{e(n["label"])}</button>'
                     f'<ul class="nav-sub">{kids}</ul></li>')
    mobile = []
    for i, n in enumerate(S["nav"]):
        kids = "".join(f"<li>{ext(c['url'], c['label'])}</li>" for c in n["children"])
        mobile.append(f'<li><button type="button" class="m-top" aria-expanded="false" aria-controls="m-sub-{i}">{e(n["label"])}<span aria-hidden="true"></span></button>'
                      f'<ul class="m-sub" id="m-sub-{i}" hidden>{kids}</ul></li>')
    return f"""
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <button type="button" class="menu-btn" aria-label="메뉴 열기" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
    {logo()}
    <nav class="gnb" aria-label="주 메뉴"><ul>{''.join(items)}</ul></nav>
    <div class="util">
      <button type="button" class="icon-btn" aria-label="검색"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg></button>
      <a class="util-text" href="{REAL}/login" target="_blank" rel="noopener">로그인</a>
      <a class="icon-btn cart" href="{REAL}/shop_cart" target="_blank" rel="noopener" aria-label="장바구니"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6.5a3 3 0 016 0V8"/></svg></a>
    </div>
  </div>
  <div class="drawer" id="drawer" hidden>
    <div class="drawer-head">{logo('logo small')}<button type="button" class="drawer-close" aria-label="메뉴 닫기">×</button></div>
    <ul class="m-nav">{''.join(mobile)}</ul>
    <div class="drawer-util"><a href="{REAL}/login" target="_blank" rel="noopener">로그인</a><a href="{REAL}/shop_cart" target="_blank" rel="noopener">장바구니</a><a href="https://en.gtmcosmetic.com" target="_blank" rel="noopener">ENG</a></div>
  </div>
</header>"""


def footer():
    f = S["footer"]
    sns = "".join(f'<a href="{s["url"]}" target="_blank" rel="noopener">{s["label"]}</a>' for s in f["sns"])
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <img class="foot-logo" src="../assets/img/etc/logo.png" alt="GTM 코스메틱스" width="600" height="321" loading="lazy">
      <dl class="foot-contact"><div><dt>TEL</dt><dd>{f['tel']}</dd></div><div><dt>FAX</dt><dd>{f['fax']}</dd></div><div><dt>E-mail</dt><dd>{f['email']}</dd></div></dl>
      <div class="foot-sns">{sns}</div>
    </div>
    <p class="foot-info">상호명 {f['company']} <i></i> 대표자명 {f['ceo']} <i></i> 사업자등록번호 {f['bizno']} <i></i> 통신판매업신고번호 {f['mailorder']}<br>
    회사주소 {f['address']} <i></i> 공장 {f['factory']}</p>
    <p class="foot-links"><a href="{REAL}/?mode=policy" target="_blank" rel="noopener">이용약관</a><a href="{REAL}/?mode=privacy" target="_blank" rel="noopener"><b>개인정보처리방침</b></a><span class="lang"><b>KOR</b><a href="https://en.gtmcosmetic.com" target="_blank" rel="noopener">ENG</a></span></p>
    <p class="copy">{f['copyright']}</p>
  </div>
</footer>"""


def concept_bar(concept):
    other = "b" if concept == "a" else "a"
    name = {"a": "A안 · 피부 과학의 정제된 아름다움", "b": "B안 · 나에게 맞는 스킨케어를 발견하다"}[concept]
    return (f'<aside class="concept-bar" aria-label="시안 이동"><span class="cb-now">{name}</span>'
            f'<a href="../{other}/">{other.upper()}안 보기</a><a href="../">시안 선택</a></aside>')


def modal():
    return """
<div class="modal" id="preview" hidden role="dialog" aria-modal="true" aria-labelledby="pv-name">
  <div class="modal-backdrop" data-close></div>
  <div class="modal-panel">
    <button type="button" class="modal-close" data-close aria-label="닫기">×</button>
    <div class="pv-img"><img alt="" id="pv-img"></div>
    <div class="pv-body">
      <p class="pv-cat" id="pv-cat"></p>
      <h2 id="pv-name"></h2>
      <p class="pv-desc" id="pv-desc"></p>
      <div id="pv-price"></div>
      <a class="btn" id="pv-link" target="_blank" rel="noopener">상품 페이지 보기</a>
    </div>
  </div>
</div>"""



# 히어로 롤링 배너: 국문 홈 메인 배너(PC 가로형 + 모바일 정사각형)와 움직이는 장면(영상). 운영에서는 클라이언트 배너로 교체
HERO = [
    {"key": "motion", "label": "GTM 코스메틱스", "video": True},
    {"key": "lineup", "label": "2026 NEW 라인업", "idx": 105},
    {"key": "pepticule", "label": "펩티큘 앰플 · 크림", "idx": 91},
    {"key": "cellcare", "label": "골드셀 · 멜라셀", "idx": 111},
    {"key": "slimline", "label": "슬림라인", "idx": 94},
    {"key": "exoshine", "label": "엑소샤인", "idx": 53},
]


def hero_slider(mode):
    n = len(HERO)
    slides = []
    for i, h in enumerate(HERO):
        lab = f'{i + 1} / {n}'
        if h.get("video"):
            media = ('<video class="hv-pc" muted playsinline loop preload="metadata" poster="../assets/img/hero/motion-pc.webp"><source src="../assets/img/hero/motion-pc.mp4" type="video/mp4"></video>'
                     '<video class="hv-m" muted playsinline loop preload="none" poster="../assets/img/hero/motion-m.webp"><source src="../assets/img/hero/motion-m.mp4" type="video/mp4"></video>')
            inner = f'<div class="hero-media">{media}</div>'
        else:
            pic = (f'<picture><source media="(max-width: 900px)" srcset="../assets/img/hero/{h["key"]}-m.webp">'
                   f'<img src="../assets/img/hero/{h["key"]}-pc.webp" alt="{e(h["label"])} 배너" width="1905" height="715" {"fetchpriority=" + chr(34) + "high" + chr(34) if i == 1 else "loading=" + chr(34) + "lazy" + chr(34)}></picture>')
            inner = f'<button type="button" class="hero-media" data-preview="{h["idx"]}" aria-label="{e(h["label"])} 제품 보기">{pic}</button>'
        slides.append(f'<div class="hero-slide{" is-on" if i == 0 else ""}" role="group" aria-roledescription="slide" aria-label="{lab} · {e(h["label"])}" data-video="{1 if h.get("video") else 0}">{inner}</div>')
    dots = "".join(f'<button type="button" class="hero-dot{" is-on" if i == 0 else ""}" aria-label="{i + 1}번 배너: {e(h["label"])}"><span></span></button>' for i, h in enumerate(HERO))
    return f"""
<section class="hero hero-{mode}" aria-roledescription="carousel" aria-label="메인 배너" data-mode="{mode}">
  <div class="hero-viewport"><div class="hero-track">{''.join(slides)}</div></div>
  <div class="hero-ui">
    <div class="wrap hero-ui-inner">
      <p class="hero-count"><b class="hero-cur">01</b> / {n:02d} <span class="hero-label">{e(HERO[0]['label'])}</span></p>
      <div class="hero-dots">{dots}</div>
      <div class="hero-btns"><button type="button" class="hero-prev" aria-label="이전 배너">‹</button><button type="button" class="hero-pause" aria-label="자동 넘김 멈춤">Ⅱ</button><button type="button" class="hero-next" aria-label="다음 배너">›</button></div>
    </div>
  </div>
</section>"""

def page(concept, title, body):
    data = {str(k): {"name": v["name"], "img": v["img"], "desc": summary(k), "price": v["price"], "sale": v["sale"], "pct": v["pct"],
                     "asking": v["asking"], "url": v["url"], "cats": [CATS[c]["name"] for c in v["cats"] if c not in ("137", "361")][:3]}
            for k, v in PROD.items()}
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="{FONT}">
<link rel="stylesheet" href="../assets/css/common.css">
<link rel="stylesheet" href="../assets/css/{concept}.css">
<link rel="icon" href="../assets/img/etc/logo.png">
</head>
<body class="concept-{concept}">
<a class="skip" href="#main">본문 바로가기</a>
{header(concept)}
<main id="main">
{body}
</main>
{footer()}
{modal()}
{concept_bar(concept)}
<script>window.GTM_PRODUCTS={json.dumps(data, ensure_ascii=False)};window.GTM_HERO={json.dumps([h["label"] for h in HERO], ensure_ascii=False)};</script>
<script src="../assets/js/common.js" defer></script>
</body>
</html>"""


# ───────────────────────── A안: 피부 과학의 정제된 아름다움
def build_a():
    it = S["irritation_test"]
    rows = "".join(f"<tr><th scope='row'>{e(n)}</th><td>{v}</td><td>비자극</td></tr>" for n, v in it["results"])
    skincare = [105, 107, 91, 106, 90, 118, 22, 16]
    tabs = [("new", "NEW & RENEWAL 2026", [105, 106, 107, 118, 110, 108, 104, 119], "/361"),
            ("skin", "스킨케어", skincare, "/137"),
            ("booster", "스킨 부스터", CATS["181"]["idx"][:8], "/181"),
            ("nmn", "NMN LINE", CATS["394"]["idx"][:8], "/394")]
    tab_btns = "".join(f'<button type="button" role="tab" id="pt-{k}" aria-controls="pp-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(n)}</button>' for i, (k, n, _, _) in enumerate(tabs))
    panels = "".join(f'<div role="tabpanel" id="pp-{k}" aria-labelledby="pt-{k}" {"" if i == 0 else "hidden"}><ul class="grid4">' + "".join(card(x) for x in ids) + f'</ul><p class="more">{ext(url, n + " 전체 보기", "text-link")}</p></div>' for i, (k, n, ids, url) in enumerate(tabs))
    def mini(x):
        q = PROD[x]
        return (f'<li><button type="button" class="ls-mini" data-preview="{x}"><img src="../assets/img/{q["img"]}" alt="" loading="lazy" width="900" height="900">'
                f'<span><span class="ls-mini-name">{e(q["name"].replace("지티엠 ", ""))}</span>{price_html(q)}</span></button></li>')
    line_html = f"""
    <article class="ls-main">
      <div class="ls-text"><p class="ls-en">PDRÉNZA</p><h3>피디렌자</h3><p class="ls-lead">PDRN X NMN X Pearl Tomato®<br>{e(summary(118).split('.')[0])}.</p><p class="ls-count">4개 제품</p></div>
      <ul class="ls-cards">{''.join(card(x) for x in [105, 106, 118, 104])}</ul>
    </article>
    <div class="ls-row">
      <article class="ls-photo">
        <img class="ls-photo-img" src="../assets/img/etc/hero-b-pepticule.webp" alt="펩티큘 앰플을 바르는 모델" loading="lazy" width="1200" height="715">
        <div class="ls-body"><p class="ls-en">PEPTICULE</p><h3>펩티큘</h3><p class="ls-lead">고농축 펩타이드 x 4세대 식물성 PDRN 스피큘</p>
          <ul class="ls-minis">{mini(91)}{mini(90)}</ul></div>
      </article>
      <article class="ls-tint">
        <div class="ls-body"><p class="ls-en">BALANCE</p><h3>밸런스</h3><p class="ls-lead">저자극 약산성 토너 · 세럼 · 크림 · 클렌징 젤</p>
          <ul class="ls-minis grid2">{mini(22)}{mini(19)}{mini(16)}{mini(21)}</ul></div>
      </article>
    </div>"""
    sol_desc = {i["cat"]: i["text"] for i in S["ingredients"] if i["key"] != "patent"}
    sols = [c["url"].strip("/") for c in S["nav"][3]["children"]]
    sol_html = "".join(
        f'<li><a href="{REAL}/{c}" target="_blank" rel="noopener"><span class="sol-no">{n:02d}</span><span class="sol-name">{e(CATS[c]["name"])}</span>'
        f'<span class="sol-desc">{e(sol_desc.get(c, ""))}</span><span class="sol-thumbs">' + "".join(f'<img src="../assets/img/{PROD[x]["img"]}" alt="" loading="lazy">' for x in CATS[c]["idx"][:3]) + f'</span><span class="sol-count">{len(CATS[c]["idx"])}종</span></a></li>'
        for n, c in enumerate(sols, 1))
    rv = "".join(f'<li><p class="rv-prod">{e(r["product"])}</p><blockquote>{e(r["text"])}</blockquote><p class="rv-meta">{e(r["author"])} · {e(r["date"])}</p></li>' for r in S["reviews"])
    news = "".join(f'<li><span class="nw-date">{e(x["date"])}</span><span class="nw-title">{e(x["title"])}</span><span class="nw-place">{e(x["place"])}</span></li>' for x in S["news"])
    body = f"""{hero_slider('peek')}

<section class="a-intro" id="philosophy">
  <div class="wrap a-intro-grid">
    <div>
      <p class="eyebrow">GTM COSMETICS</p>
      <h1>성분을 연구하고,<br>피부의 아름다움을 생각합니다.</h1>
    </div>
    <div class="a-intro-side">
      <p class="statement">{e(S['brand']['statement'])}</p>
      <dl class="a-facts">
        <div><dt>국문 온라인몰 제품</dt><dd>{len(PROD)}<small>종</small></dd></div>
        <div><dt>성분별 솔루션</dt><dd>{len(sols)}<small>가지</small></dd></div>
        <div><dt>피부 일차자극 시험 비자극 판정</dt><dd>{len(it['results'])}<small>개 제품</small></dd></div>
      </dl>
      <p class="a-intro-links">{ext('/34', '브랜드 스토리', 'text-link')}{ext('/157', '히스토리 / 인증', 'text-link')}{ext('/158', 'OEM / ODM', 'text-link')}</p>
    </div>
  </div>
</section>

<section class="a-products" id="products">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">PRODUCTS</p><h2>GTM 코스메틱스 제품</h2></div><div class="tabs" role="tablist" aria-label="제품 분류">{tab_btns}</div></div>
    {panels}
  </div>
</section>

<section class="a-lines" id="line">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">SIGNATURE LINES</p><h2>대표 라인</h2></div><p class="sec-lead">피부 고민과 루틴에 맞춰 이어 쓰는 GTM 코스메틱스의 라인입니다.</p></div>
    <div class="a-ls">{line_html}</div>
  </div>
</section>

<section class="a-solution" id="ingredient">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">INGREDIENT SOLUTIONS</p><h2>성분별 솔루션</h2></div>{ext('/280', '성분별 솔루션 전체 보기', 'text-link')}</div>
    <ol class="sol-list">{sol_html}</ol>
  </div>
</section>

<section class="a-safety" id="safety">
  <div class="wrap a-safety-grid">
    <div class="a-safety-copy">
      <p class="eyebrow">SAFETY</p>
      <h2>{e(it['headline'])}</h2>
      <p class="a-safety-big">{len(it['results'])}개 제품 모두<br><b>비자극(Excellent)</b> 판정</p>
      <p class="a-safety-body">{e(it['body'])}</p>
      <dl class="a-test-meta"><div><dt>시험기관</dt><dd>{e(it['institute'])}</dd></div><div><dt>시험기간</dt><dd>{e(it['period'])}</dd></div><div><dt>시험대상</dt><dd>{e(it['subjects'])}</dd></div></dl>
    </div>
    <div class="a-test-table">
      <table><caption>인체 피부 일차자극 시험 결과</caption><thead><tr><th scope="col">제품명</th><th scope="col">피부 자극 지수</th><th scope="col">판정</th></tr></thead><tbody>{rows}</tbody></table>
      <p class="note">※ {e(it['criteria'])}<br>※ {e(it['notice'])}</p>
    </div>
  </div>
</section>

<section class="a-voice" id="news">
  <div class="wrap a-voice-grid">
    <div><div class="sec-head small"><div><p class="eyebrow">REVIEW</p><h2>구매평</h2></div></div><ul class="a-reviews">{rv}</ul></div>
    <div><div class="sec-head small"><div><p class="eyebrow">NEWS</p><h2>브랜드 소식</h2></div>{ext('/68', '뉴스 전체 보기', 'text-link')}</div><ul class="a-news">{news}</ul></div>
  </div>
</section>"""
    return page("a", "GTM 코스메틱스 | 성분을 연구하고, 피부의 아름다움을 생각합니다", body)


# ───────────────────────── B안: 나에게 맞는 스킨케어를 발견하다
def build_b():
    shortcuts = S["category_shortcuts"]
    rep = {"181": 29, "352": 22, "353": 107, "354": 106, "355": 118, "356": 21, "357": 59, "358": 30}
    sc_btns = "".join(
        f'<button type="button" role="tab" class="sc-tile" id="sc-{c}" aria-controls="sc-panel-{c}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
        f'<span class="sc-img"><img src="../assets/img/{PROD[rep[c]]["img"]}" alt="" loading="lazy"></span><span class="sc-name">{e(CATS[c]["name"])}</span><span class="sc-count">{len(CATS[c]["idx"])}개 제품</span></button>'
        for i, c in enumerate(shortcuts))
    sc_panels = "".join(f'<ul class="row-scroll" role="tabpanel" id="sc-panel-{c}" aria-labelledby="sc-{c}" {"" if i == 0 else "hidden"}>' + "".join(card(x) for x in CATS[c]["idx"]) + "</ul>"
                        for i, c in enumerate(shortcuts))
    renewal = [105, 106, 107, 118, 110, 108, 109, 104, 119]
    lines = S["lines"]
    line_btns = "".join(f'<button type="button" role="tab" id="ln-{l["key"]}" aria-controls="ln-panel-{l["key"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" style="--lc:{l["color"]}"><span class="ln-en">{e(l["en"])}</span><span class="ln-kr">{e(l["name"])}</span><span class="ln-n">{len(l["idx"])}</span></button>' for i, l in enumerate(lines))
    line_panels = "".join(
        f'<div class="ln-panel" role="tabpanel" id="ln-panel-{l["key"]}" aria-labelledby="ln-{l["key"]}" {"" if i == 0 else "hidden"} style="--lc:{l["color"]}">'
        f'<div class="ln-intro"><p class="ln-en">{e(l["en"])}</p><h3>{e(l["name"])} 라인</h3><p>{e(l["lead"])}</p></div>'
        f'<ul class="grid3">' + "".join(card(x, show_desc=True) for x in l["idx"][:6]) + "</ul></div>" for i, l in enumerate(lines))
    ing = S["ingredients"]
    ing_btns = "".join(f'<button type="button" role="tab" id="ig-{i["key"]}" aria-controls="ig-panel-{i["key"]}" aria-selected="{"true" if n == 0 else "false"}" tabindex="{0 if n == 0 else -1}" class="ig-chip"><img src="../assets/img/ing/{i["key"]}.webp" alt="" loading="lazy"><span>{e(i["title"])}<small>{e(i["sub"])}</small></span></button>' for n, i in enumerate(ing))
    ing_panels = "".join(
        f'<div role="tabpanel" id="ig-panel-{i["key"]}" aria-labelledby="ig-{i["key"]}" {"" if n == 0 else "hidden"} class="ig-panel">'
        f'<div class="ig-desc"><h3>{e(i["title"])} <small>{e(i["sub"])}</small></h3><p>{e(i["text"])}</p>{ext("/" + i["cat"], i["catLabel"] + " 전체 " + str(len(CATS[i["cat"]]["idx"])) + "종", "text-link")}</div>'
        f'<ul class="row-scroll">' + "".join(card(x) for x in CATS[i["cat"]]["idx"][:10]) + "</ul></div>" for n, i in enumerate(ing))
    rv = "".join(
        f'<li class="review"><p class="rv-prod">{e(r["product"])}</p><blockquote>“{e(r["text"])}”</blockquote><p class="rv-meta">{e(r["author"])} · {e(r["date"])}</p></li>' for r in S["reviews"])
    news = "".join(f'<li><span class="nw-date">{e(n["date"])}</span><span class="nw-title">{e(n["title"])}</span><span class="nw-place">{e(n["place"])}</span></li>' for n in S["news"])
    body = f"""
{hero_slider('fade')}

<section class="b-intro">
  <div class="wrap b-intro-grid">
    <div><p class="eyebrow">GTM 코스메틱스 · NEW &amp; RENEWAL 2026</p><h1>오늘의 피부를 위한,<br>나만의 케어를 만나보세요.</h1></div>
    <div><p class="lead">토너부터 마스크, 스킨 부스터까지. 피부 고민과 루틴에 맞는 제품을 찾아보세요.</p>
      <div class="b-hero-chips"><a href="#find" data-jump="353">세럼 / 앰플</a><a href="#find" data-jump="354">크림</a><a href="#find" data-jump="355">마스크</a><a href="#ingredient" data-jump-ing="repair-pdrn">PDRN</a><a href="#ingredient" data-jump-ing="biotech-nmn">NMN</a><a href="#lines">라인으로 고르기</a></div></div>
  </div>
</section>

<section class="b-find" id="find">
  <div class="wrap">
    <div class="b-head"><h2>어떤 제품을 찾고 계신가요?</h2><p>제품군을 고르면 바로 아래에서 해당 제품을 볼 수 있어요.</p></div>
    <div class="sc-grid" role="tablist" aria-label="제품군">{sc_btns}</div>
    <div class="sc-panels">{sc_panels}</div>
  </div>
</section>

<section class="b-renewal" id="renewal">
  <div class="wrap">
    <div class="b-head row"><div><p class="eyebrow">RENEWAL 2026</p><h2>새로워진 GTM</h2></div>
      <div class="slider-nav"><button type="button" class="sl-prev" aria-label="이전 제품">‹</button><button type="button" class="sl-next" aria-label="다음 제품">›</button></div></div>
    <ul class="slider" tabindex="0" aria-label="리뉴얼 제품 목록">{''.join(card(x, 'slide', show_desc=True) for x in renewal)}</ul>
  </div>
</section>

<section class="b-lines" id="lines">
  <div class="wrap">
    <div class="b-head"><p class="eyebrow">LINE</p><h2>라인으로 고르기</h2></div>
    <div class="ln-wrap"><div class="ln-tabs" role="tablist" aria-label="제품 라인">{line_btns}</div><div class="ln-panels">{line_panels}</div></div>
  </div>
</section>

<section class="b-ingredient" id="ingredient">
  <div class="wrap">
    <div class="b-head"><p class="eyebrow">INGREDIENT</p><h2>성분으로 찾기</h2><p>관심 있는 성분을 고르면 그 성분이 담긴 제품을 모아 보여드려요.</p></div>
    <div class="ig-chips" role="tablist" aria-label="성분">{ing_btns}</div>
    {ing_panels}
  </div>
</section>

<section class="b-voice" id="voice">
  <div class="wrap b-voice-grid">
    <div>
      <div class="b-head"><p class="eyebrow">REVIEW</p><h2>실제 구매평</h2></div>
      <ul class="reviews">{rv}</ul>
      <a class="text-link" href="{REAL}/" target="_blank" rel="noopener">구매평 더 보기</a>
    </div>
    <div class="b-sns">
      <div class="b-head"><p class="eyebrow">BRAND NEWS</p><h2>GTM 소식</h2></div>
      <ul class="nw-list">{news}</ul>
      <a class="btn soft" href="https://www.instagram.com/cmedemi/" target="_blank" rel="noopener">인스타그램 @cmedemi</a>
    </div>
  </div>
</section>"""
    return page("b", "GTM 코스메틱스 | 오늘의 피부를 위한, 나만의 케어를 만나보세요", body)


def build_index():
    return """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>GTM 코스메틱스 국문 메인 시안</title>
<link rel="stylesheet" href="%s">
<link rel="stylesheet" href="assets/css/index.css">
<link rel="icon" href="assets/img/etc/logo.png">
</head>
<body>
<main class="pick">
  <header><img src="assets/img/etc/logo.png" alt="GTM 코스메틱스" width="600" height="321"><h1>국문 메인 디자인 시안</h1><p>두 가지 방향의 메인 페이지를 실제 화면으로 비교해 보세요.</p></header>
  <ul class="pick-list">
    <li><a href="a/"><span class="thumb"><img src="assets/img/etc/thumb-a.webp" alt="A안 메인 화면" width="1440" height="900"></span>
      <span class="pk-label">A안</span><strong>피부 과학의 정제된 아름다움</strong>
      <span class="pk-desc">대표 라인 피디렌자를 중심으로 원료와 피부 자극 시험 결과를 차분하게 전하는 방향. 화이트·웜그레이에 로고 레드를 포인트로 사용했습니다.</span></a></li>
    <li><a href="b/"><span class="thumb"><img src="assets/img/etc/thumb-b.webp" alt="B안 메인 화면" width="1440" height="900"></span>
      <span class="pk-label">B안</span><strong>나에게 맞는 스킨케어를 발견하다</strong>
      <span class="pk-desc">제품군·라인·성분 세 가지 길로 제품을 쉽게 찾아가는 방향. 아이보리·소프트 핑크에 제품 패키지 색을 포인트로 사용했습니다.</span></a></li>
  </ul>
</main>
</body>
</html>""" % FONT


if __name__ == "__main__":
    (SITE / "a").mkdir(parents=True, exist_ok=True)
    (SITE / "b").mkdir(parents=True, exist_ok=True)
    (SITE / "a" / "index.html").write_text(build_a(), encoding="utf-8")
    (SITE / "b" / "index.html").write_text(build_b(), encoding="utf-8")
    (SITE / "index.html").write_text(build_index(), encoding="utf-8")
    print("built")
