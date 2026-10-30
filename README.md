# GTM 코스메틱스 국문 메인 리뉴얼 시안

국문 공개 사이트(https://gtm.uriweb.kr) 자료로 만든 메인 페이지 디자인 시안 2종입니다. 운영 사이트는 수정하지 않습니다.

- `site/` — 공개 화면(정적 HTML/CSS/JS). `index.html` 시안 선택, `a/` A안, `b/` B안
- `data/` — 두 시안이 함께 쓰는 상품·메뉴·푸터 데이터, 이미지 출처 목록
- `tools/` — `prepare_assets.py`(원본 → 웹용 이미지), `build.py`(데이터 → HTML), `qa.py`(PC 1440·모바일 390 점검)
- `docs/` — 자료 수집·출처 기록, 아임웹 적용표

수정 후 `python3 -I tools/build.py` 로 HTML을 다시 만들고 main 에 push 하면 GitHub Pages 에 배포됩니다.
