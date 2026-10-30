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
<script>window.GTM_PRODUCTS={json.dumps(data, ensure_ascii=False)};</script>
<script src="../assets/js/common.js" defer></script>
</body>
</html>"""


# ───────────────────────── A안: 피부 과학의 정제된 아름다움
def build_a():
    hero = PROD[105]
    line = [105, 106, 118, 104]
    it = S["irritation_test"]
    rows = "".join(f"<tr><th scope='row'>{e(n)}</th><td>{v}</td><td>비자극 (Excellent)</td></tr>" for n, v in it["results"])
    ingr = [i for i in S["ingredients"] if i["key"] in ("repair-pdrn", "biotech-nmn", "pearl-tomato")]
    ingr_html = "".join(
        f'<li><p class="ing-no">0{n}</p><h3>{e(i["sub"])}</h3><p class="ing-kr">{e(i["title"])}</p><p class="ing-text">{e(i["text"])}</p>'
        f'{ext(CATS[i["cat"]]["name"] and "/" + i["cat"], i["catLabel"] + " 제품 " + str(len(CATS[i["cat"]]["idx"])) + "종", "text-link")}</li>'
        for n, i in enumerate(ingr, 1))
    tabs = [("353", "세럼 / 앰플"), ("354", "크림"), ("355", "마스크"), ("352", "토너"), ("356", "클렌징"), ("181", "스킨 부스터")]
    tab_btns = "".join(f'<button type="button" role="tab" id="tab-{c}" aria-controls="panel-{c}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(n)} <small>{len(CATS[c]["idx"])}</small></button>' for i, (c, n) in enumerate(tabs))
    panels = "".join(f'<ul class="grid4" role="tabpanel" id="panel-{c}" aria-labelledby="tab-{c}" {"" if i == 0 else "hidden"}>' + "".join(card(x) for x in CATS[c]["idx"][:8]) + "</ul>" for i, (c, n) in enumerate(tabs))
    news = S["news"]
    news_html = "".join(
        f'<li class="news-item{" has-img" if n.get("img") else ""}">' + (f'<img src="../assets/img/{n["img"]}" alt="{e(n["title"])} 포스터" loading="lazy">' if n.get("img") else "")
        + f'<p class="news-date">{e(n["date"])}</p><h3>{e(n["title"])}</h3><p class="news-place">{e(n["place"])}</p></li>' for n in news)
    body = f"""
<section class="a-hero">
  <div class="wrap a-hero-grid">
    <div class="a-hero-copy">
      <p class="eyebrow">NEW &amp; RENEWAL 2026 · PDRÉNZA</p>
      <h1>성분을 연구하고,<br>피부의 아름다움을 생각합니다.</h1>
      <p class="lead">PDRN X NMN X Pearl Tomato®<br>피부 컨디션을 깨우는 첫 순간, 인텐시브 리쥬비네이션 세럼</p>
      <div class="btns"><a class="btn" href="#line">피디렌자 라인 보기</a><a class="btn line" href="#philosophy">브랜드 이야기</a></div>
    </div>
    <figure class="a-hero-visual">
      <img src="../assets/img/etc/hero-pdrenza-serum.webp" alt="{e(hero['name'])}" width="1200" height="1200" fetchpriority="high">
      <figcaption><button type="button" data-preview="105">{e(hero['name'])}</button>{price_html(hero, 'price small')}</figcaption>
    </figure>
  </div>
</section>

<section class="a-philosophy" id="philosophy">
  <div class="wrap a-phil-grid">
    <p class="eyebrow">BRAND</p>
    <div>
      <p class="statement">순수한 성분, 과학적인 추출,<br>피부 본연의 빛을 되살리다.</p>
      <ul class="link-rows">
        <li>{ext('/34', '브랜드 스토리')}</li><li>{ext('/157', '히스토리 / 인증')}</li><li>{ext('/158', 'OEM / ODM')}</li><li>{ext('/159', '글로벌 비즈니스')}</li>
      </ul>
    </div>
  </div>
</section>

<section class="a-line" id="line">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">SIGNATURE LINE</p><h2>피디렌자</h2></div><p class="sec-lead">PDRN, NMN, 펄토마토® 세 가지 원료를 담은 2026 리뉴얼 라인입니다.</p></div>
    <div class="a-line-grid">
      <button type="button" class="a-line-feature" data-preview="118">
        <img src="../assets/img/etc/pdrenza-mask.webp" alt="{e(PROD[118]['name'])}" loading="lazy" width="1200" height="1200">
        <span class="feat-body"><span class="feat-name">{e(PROD[118]['name'])}</span><span class="feat-desc">{e(summary(118))}</span>{price_html(PROD[118])}</span>
      </button>
      <ul class="a-line-list">{''.join(card(x, show_desc=True) for x in [105, 106, 104])}</ul>
    </div>
  </div>
</section>

<section class="a-ingredient" id="ingredient">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">INGREDIENT</p><h2>세 가지 원료 이야기</h2></div><p class="sec-lead">피디렌자 라인에 담긴 세 가지 원료를 소개합니다.</p></div>
    <ol class="ing-list">{ingr_html}</ol>
    <div class="a-test">
      <div class="a-test-copy">
        <p class="eyebrow">SAFETY</p>
        <h3>{e(it['headline'])}</h3>
        <p class="a-test-title">{e(it['title'])}</p>
        <p>{e(it['body'])}</p>
        <dl class="a-test-meta"><div><dt>시험기관</dt><dd>{e(it['institute'])}</dd></div><div><dt>시험기간</dt><dd>{e(it['period'])}</dd></div><div><dt>시험대상</dt><dd>{e(it['subjects'])}</dd></div></dl>
      </div>
      <div class="a-test-table">
        <table><caption>인체 피부 일차자극 시험 결과 (9개 제품)</caption><thead><tr><th scope="col">제품명</th><th scope="col">피부 자극 지수</th><th scope="col">판정</th></tr></thead><tbody>{rows}</tbody></table>
        <p class="note">※ {e(it['criteria'])}<br>※ {e(it['notice'])}</p>
      </div>
    </div>
  </div>
</section>

<section class="a-collection" id="collection">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">COLLECTION</p><h2>제품 컬렉션</h2></div>{ext('/137', '제품 라인업 전체 보기', 'text-link')}</div>
    <div class="tabs" role="tablist" aria-label="제품 분류">{tab_btns}</div>
    {panels}
  </div>
</section>

<section class="a-news" id="news">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">NEWS</p><h2>브랜드 소식</h2></div>{ext('/68', '뉴스 전체 보기', 'text-link')}</div>
    <ul class="news-list">{news_html}</ul>
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
<section class="b-hero">
  <div class="b-hero-grid">
    <div class="b-hero-copy">
      <p class="eyebrow">GTM 코스메틱스 · NEW &amp; RENEWAL 2026</p>
      <h1>오늘의 피부를 위한,<br>나만의 케어를 만나보세요.</h1>
      <p class="lead">토너부터 마스크, 스킨 부스터까지.<br>피부 고민과 루틴에 맞는 제품을 찾아보세요.</p>
      <div class="b-hero-chips">
        <a href="#find" data-jump="353">세럼 / 앰플</a><a href="#find" data-jump="354">크림</a><a href="#find" data-jump="355">마스크</a><a href="#ingredient" data-jump-ing="repair-pdrn">PDRN</a><a href="#ingredient" data-jump-ing="biotech-nmn">NMN</a>
      </div>
    </div>
    <div class="b-hero-visual">
      <button type="button" class="hv hv-1" data-preview="118"><img src="../assets/img/etc/pdrenza-mask.webp" alt="{e(PROD[118]['name'])}" width="1200" height="1200" fetchpriority="high"><span>{e(PROD[118]['name'])}</span></button>
      <button type="button" class="hv hv-2" data-preview="107"><img src="../assets/img/etc/collagen.webp" alt="{e(PROD[107]['name'])}" width="1000" height="1000"><span>{e(PROD[107]['name'])}</span></button>
      <button type="button" class="hv hv-3" data-preview="109"><img src="../assets/img/etc/snowpeel-kit.webp" alt="{e(PROD[109]['name'])}" width="1200" height="1200"><span>{e(PROD[109]['name'])}</span></button>
    </div>
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
