"""시안 QA: 1440·390 전체 캡처, 이미지 누락·가로 넘침·콘솔 오류·링크 점검.
실행: /usr/bin/python3 tools/qa.py <BASE_URL> <OUT_DIR>"""
import json, sys, urllib.request
from playwright.sync_api import sync_playwright
BASE = sys.argv[1].rstrip("/"); OUT = sys.argv[2]
PAGES = ["", "a/", "b/"]
VP = {"pc": (1440, 900), "mobile": (390, 844)}
res = {"pages": [], "links": {}}
with sync_playwright() as p:
    b = p.chromium.launch()
    for vp, (w, h) in VP.items():
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, locale="ko-KR")
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for path in PAGES:
            errs.clear(); pg.goto(f"{BASE}/{path}", wait_until="networkidle")
            if vp == "pc" and path in ("a/", "b/") and "--thumbs" in sys.argv:
                pg.add_style_tag(content=".concept-bar{display:none!important}"); pg.wait_for_timeout(400)
                pg.screenshot(path=f"{OUT}/thumb-{path[0]}.png")
                pg.evaluate("document.querySelector('.concept-bar').style.display=''")
            pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            pg.wait_for_load_state("networkidle")
            hgt = pg.evaluate("document.body.scrollHeight")
            for y in range(0, hgt, 600): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(40)
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
            info = pg.evaluate("""() => ({
              broken: [...document.images].filter(i => i.getAttribute('src') && i.complete && i.naturalWidth === 0).map(i => i.src),
              overflow: document.documentElement.scrollWidth - window.innerWidth,
              wide: [...document.querySelectorAll('body *')].filter(el => { const r = el.getBoundingClientRect(); return r.right > window.innerWidth + 1 && getComputedStyle(el).position !== 'fixed' && !el.closest('.row-scroll,.slider,.ln-tabs,.drawer,.tabs,.hero-viewport') }).slice(0, 5).map(el => el.className || el.tagName),
              smallTargets: [...document.querySelectorAll('a,button')].filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && (r.height < 32 || r.width < 32) && !el.closest('.site-footer,.foot-links,.nav-sub') && !el.classList.contains('text-link') }).slice(0, 8).map(el => (el.className || el.tagName) + ':' + (el.innerText || '').slice(0, 12)),
              font: getComputedStyle(document.body).fontFamily.slice(0, 30),
              links: [...document.querySelectorAll('a[href]')].map(a => a.href)
            })""")
            name = (path.strip("/") or "index")
            pg.screenshot(path=f"{OUT}/{name}_{vp}.png", full_page=True)
            res["pages"].append({"page": name, "vp": vp, "errors": list(errs), **{k: v for k, v in info.items() if k != "links"}})
            for l in info["links"]: res["links"].setdefault(l, None)
        # 모바일 메뉴 동작
        if vp == "mobile":
            for path in ["a/", "b/"]:
                pg.goto(f"{BASE}/{path}", wait_until="networkidle")
                pg.click(".menu-btn"); pg.wait_for_timeout(300)
                pg.click(".m-top >> nth=1"); pg.wait_for_timeout(300)
                pg.screenshot(path=f"{OUT}/{path.strip('/')}_mobile_menu.png")
                opened = pg.evaluate("!document.getElementById('drawer').hidden && !document.getElementById('m-sub-1').hidden")
                pg.click(".drawer-close"); closed = pg.evaluate("document.getElementById('drawer').hidden")
                pg.click(".card-btn >> nth=0"); pg.wait_for_timeout(300)
                pv = pg.evaluate("!document.getElementById('preview').hidden && document.getElementById('pv-name').textContent")
                pg.screenshot(path=f"{OUT}/{path.strip('/')}_mobile_preview.png")
                pg.keyboard.press("Escape")
                res.setdefault("menu", []).append({"page": path, "drawer_open_sub": opened, "closed": closed, "preview": pv})
        ctx.close()
    b.close()
for l in list(res["links"]):
    if l.startswith(BASE) and "#" not in l:
        try: res["links"][l] = urllib.request.urlopen(l, timeout=15).status
        except Exception as e: res["links"][l] = str(e)
json.dump(res, open(f"{OUT}/qa.json", "w"), ensure_ascii=False, indent=1)
bad = [x for x in res["pages"] if x["broken"] or x["overflow"] > 0 or x["wide"] or x["errors"]]
print("pages", len(res["pages"]), "bad", len(bad)); [print(x["page"], x["vp"], x["broken"][:2], x["overflow"], x["wide"], x["errors"][:2]) for x in bad]
print("small", {f'{x["page"]}_{x["vp"]}': x["smallTargets"] for x in res["pages"] if x["smallTargets"]})
print("menu", res.get("menu")); print("internal links", {k: v for k, v in res["links"].items() if k.startswith(BASE) and v != 200 and "#" not in k})
print("font", res["pages"][1]["font"])
