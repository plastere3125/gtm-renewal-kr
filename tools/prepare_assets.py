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
    # 히어로 롤링 배너(국문 홈 메인 배너 원본: PC 가로형 + 모바일 정사각형 짝). 운영에서는 클라이언트가 올리는 배너로 교체
    (IMG / "hero").mkdir(exist_ok=True)
    for key, pc, mo, use in [("lineup", "005", "012", "2026 NEW 라인업"), ("pepticule", "006", "014", "펩티큘 앰플·크림"),
                             ("cellcare", "007", "015", "골드셀·멜라셀"), ("slimline", "009", "016", "슬림라인"), ("exoshine", "010", "019", "엑소샤인")]:
        for kind, pre, side in (("pc", pc, 1905), ("m", mo, 1000)):
            size = webp(home(pre), IMG / "hero" / f"{key}-{kind}.webp", side, 84)
            sources.append({"file": f"hero/{key}-{kind}.webp", "source": json_src(home(pre)), "use": f"히어로 배너({'PC' if kind == 'pc' else '모바일'}) · {use}", "size": size})
    # 움직이는 배너(GIF) → MP4 영상 + 첫 장면 포스터
    import subprocess
    for kind, pre in (("pc", "004"), ("m", "013")):
        src = home(pre)
        out = IMG / "hero" / f"motion-{kind}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-movflags", "+faststart", "-pix_fmt", "yuv420p", "-vf", "scale='min(1600,iw)':-2" if kind == "pc" else "scale=720:-2",
                        "-c:v", "libx264", "-crf", "31", "-preset", "slow", "-an", str(out)], check=True)
        im = Image.open(src); im.seek(0); im = im.convert("RGB")
        im.save(IMG / "hero" / f"motion-{kind}.webp", "WEBP", quality=82)
        sources.append({"file": f"hero/motion-{kind}.mp4 (+.webp 포스터)", "source": json_src(src), "use": f"히어로 영상 장면({'PC' if kind == 'pc' else '모바일'}) · 움직이는 GIF 배너를 MP4로 변환", "size": im.size})
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
