"""수집 원본(_research, 저장소 밖) → site/assets/img 웹용 변환. 제품 이미지는 비율 유지·크롭 없음.
실행: python3 -I tools/prepare_assets.py ../_research
"""
import json, sys, glob
from pathlib import Path
from PIL import Image
RES = Path(sys.argv[1]).resolve()
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "site" / "assets" / "img"

def webp(src, dst, max_side, q=86):
    im = Image.open(src)
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(dst, "WEBP", quality=q, method=6)
    return im.size

def home(prefix):
    return glob.glob(str(RES / "raw" / "home" / f"{prefix}_*"))[0]

def main():
    sources = []
    prods = json.load(open(RES / "products.json", encoding="utf-8"))
    for p in prods["products"]:
        f = glob.glob(str(RES / "raw" / "prod" / f"{p['idx']:03d}_0_*"))
        if not f:
            continue
        size = webp(f[0], IMG / "p" / f"{p['idx']}.webp", 900)
        sources.append({"file": f"p/{p['idx']}.webp", "source": p["images"][0], "use": f"상품 이미지 · {p['name']}", "size": size})
    # 메인 연출용 고해상도 제품컷(홈 화면 원본 1200px)
    for key, pre, use in [("hero-pdrenza-serum", "037", "A안 히어로 · 피디렌자 세럼"), ("pdrenza-mask", "041", "피디렌자 크리스탈 마스크"),
                          ("meladual", "039", "멜라듀얼 데이 & 나이트 크림"), ("snowpeel-kit", "045", "스노우필 라하샷 스타터 키트"),
                          ("collagen", "025", "콜라겐 세럼"), ("pdrenza-cream", "026", "피디렌자 크림"), ("pdrenza-set", "031", "피디렌자 세트")]:
        src = home(pre)
        size = webp(src, IMG / "etc" / f"{key}.webp", 1200)
        sources.append({"file": f"etc/{key}.webp", "source": json_src(src), "use": use, "size": size})
    # 성분 이미지(홈 '원료' 섹션, 700px 판)
    for key, pre in [("biotech-nmn", "050"), ("spicule", "052"), ("repair-pdrn", "054"), ("exosome", "056"),
                     ("peptide", "058"), ("patent", "060"), ("calming", "062"), ("pearl-tomato", "064")]:
        src = home(pre)
        size = webp(src, IMG / "ing" / f"{key}.webp", 700)
        sources.append({"file": f"ing/{key}.webp", "source": json_src(src), "use": f"B안 성분별 탐색 · {key}", "size": size})
    # 메인 배너 원본에서 글자가 없는 연출 장면만 잘라 사용(배너 문구 영역은 쓰지 않음)
    for key, pre, box, use in [
        ("hero-a-banner", "005", (0, 0, 1, 1), "A안 히어로(PC) · 2026 신제품 배너 장면. 원본 문구가 있는 왼쪽 영역은 HTML 패널로 덮어 사용"),
        ("hero-a-stage-m", "005", (0.46, 0, 1, 1), "A안 히어로(모바일) · 2026 신제품 무대 장면(가로 배너 글자 영역 제외)"),
        ("hero-b-lineup", "005", (0.46, 0, 1, 1), "B안 히어로 슬라이드 1 · 2026 신제품 라인업 장면"),
        ("hero-b-pepticule", "006", (0.37, 0, 1, 1), "B안 히어로 슬라이드 2 · 펩티큘 모델 장면")]:
        src = home(pre)
        im = Image.open(src).convert("RGB")
        w, h = im.size
        im = im.crop((round(w * box[0]), round(h * box[1]), round(w * box[2]), round(h * box[3])))
        im.thumbnail((1905, 1905), Image.LANCZOS)
        im.save(IMG / "etc" / f"{key}.webp", "WEBP", quality=84, method=6)
        sources.append({"file": f"etc/{key}.webp", "source": json_src(src), "use": use, "size": im.size})
    # 로고(투명 PNG), 전시 포스터, 피부 자극 시험 팝업
    logo = Image.open(home("131")).convert("RGBA")
    logo = logo.crop(logo.getchannel("A").getbbox())
    logo.thumbnail((600, 600), Image.LANCZOS)
    logo.save(IMG / "etc" / "logo.png", optimize=True)
    sources.append({"file": "etc/logo.png", "source": json_src(home("131")), "use": "로고(헤더·푸터)", "size": logo.size})
    size = webp(home("100"), IMG / "etc" / "cosme-osaka-2026.webp", 900)
    sources.append({"file": "etc/cosme-osaka-2026.webp", "source": json_src(home("100")), "use": "브랜드 소식 · COSME Week Osaka 2026", "size": size})
    json.dump(sources, open(ROOT / "data" / "image_sources.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(sources), "images")

def json_src(path):
    meta = json.load(open(RES / "raw" / "home_images.json"))
    name = Path(path).name
    return next(m["url"] for m in meta if Path(m["file"]).name == name)

if __name__ == "__main__":
    main()
