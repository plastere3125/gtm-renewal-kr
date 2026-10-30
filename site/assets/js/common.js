// 공통 동작: 모바일 메뉴, 데스크톱 드롭다운(키보드), 탭, 슬라이더, 상품 미리보기
(function () {
  "use strict";
  var body = document.body;

  // 모바일 메뉴
  var drawer = document.getElementById("drawer");
  var menuBtn = document.querySelector(".menu-btn");
  function openDrawer(open) {
    if (!drawer) return;
    drawer.hidden = !open;
    menuBtn.setAttribute("aria-expanded", String(open));
    body.classList.toggle("lock", open);
    if (open) drawer.querySelector(".drawer-close").focus();
    else menuBtn.focus();
  }
  if (menuBtn) menuBtn.addEventListener("click", function () { openDrawer(true); });
  if (drawer) {
    drawer.querySelector(".drawer-close").addEventListener("click", function () { openDrawer(false); });
    drawer.querySelectorAll(".m-top").forEach(function (b) {
      b.addEventListener("click", function () {
        var sub = document.getElementById(b.getAttribute("aria-controls"));
        var open = b.getAttribute("aria-expanded") !== "true";
        b.setAttribute("aria-expanded", String(open));
        sub.hidden = !open;
      });
    });
    drawer.querySelectorAll("a[href^='#']").forEach(function (a) { a.addEventListener("click", function () { openDrawer(false); }); });
  }

  // 데스크톱 드롭다운: 클릭으로도 열고 닫기
  document.querySelectorAll(".nav-item").forEach(function (item) {
    var btn = item.querySelector(".nav-top");
    btn.addEventListener("click", function () {
      var open = !item.classList.contains("open");
      document.querySelectorAll(".nav-item.open").forEach(function (x) { x.classList.remove("open"); x.querySelector(".nav-top").setAttribute("aria-expanded", "false"); });
      item.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function (ev) {
    if (!ev.target.closest(".nav-item")) document.querySelectorAll(".nav-item.open").forEach(function (x) { x.classList.remove("open"); x.querySelector(".nav-top").setAttribute("aria-expanded", "false"); });
  });

  // 탭(role=tablist): 클릭·좌우 방향키
  function selectTab(tab) {
    var list = tab.closest("[role='tablist']");
    list.querySelectorAll("[role='tab']").forEach(function (t) {
      var on = t === tab;
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      var panel = document.getElementById(t.getAttribute("aria-controls"));
      if (panel) panel.hidden = !on;
    });
  }
  document.querySelectorAll("[role='tablist']").forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll("[role='tab']"));
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { selectTab(t); });
      t.addEventListener("keydown", function (ev) {
        var d = ev.key === "ArrowRight" || ev.key === "ArrowDown" ? 1 : ev.key === "ArrowLeft" || ev.key === "ArrowUp" ? -1 : 0;
        if (!d) return;
        ev.preventDefault();
        var n = tabs[(i + d + tabs.length) % tabs.length];
        n.focus();
        selectTab(n);
      });
    });
  });

  // B안 히어로 바로가기 칩 → 해당 탭 선택
  document.querySelectorAll("[data-jump]").forEach(function (a) {
    a.addEventListener("click", function () { var t = document.getElementById("sc-" + a.dataset.jump); if (t) selectTab(t); });
  });
  document.querySelectorAll("[data-jump-ing]").forEach(function (a) {
    a.addEventListener("click", function () { var t = document.getElementById("ig-" + a.dataset.jumpIng); if (t) selectTab(t); });
  });

  // 슬라이더 버튼
  document.querySelectorAll(".slider").forEach(function (sl) {
    var sec = sl.closest("section");
    var step = function () { var li = sl.querySelector("li"); return li ? li.getBoundingClientRect().width + 24 : 300; };
    var prev = sec.querySelector(".sl-prev");
    var next = sec.querySelector(".sl-next");
    if (prev) prev.addEventListener("click", function () { sl.scrollBy({ left: -step(), behavior: "smooth" }); });
    if (next) next.addEventListener("click", function () { sl.scrollBy({ left: step(), behavior: "smooth" }); });
  });

  // 히어로 롤링 배너: 이미지 5초, 영상 장면은 영상 길이만큼. 멈춤·이전·다음·막대 선택, 동작 줄이기 설정 존중
  document.querySelectorAll(".hero").forEach(function (hero) {
    var mode = hero.dataset.mode;
    var track = hero.querySelector(".hero-track");
    var slides = Array.prototype.slice.call(hero.querySelectorAll(".hero-slide"));
    var dots = hero.querySelectorAll(".hero-dot");
    var cur = 0, timer = null, paused = false;
    var labels = window.GTM_HERO || [];
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var curEl = hero.querySelector(".hero-cur"), labelEl = hero.querySelector(".hero-label"), pauseBtn = hero.querySelector(".hero-pause");
    function video(slide) {
      var vs = slide.querySelectorAll("video");
      for (var i = 0; i < vs.length; i++) if (vs[i].offsetParent !== null) return vs[i];
      return null;
    }
    function place() {
      if (mode !== "peek") return;
      var s = slides[cur], vw = hero.querySelector(".hero-viewport").clientWidth;
      track.style.transform = "translateX(" + (vw / 2 - (s.offsetLeft + s.offsetWidth / 2)) + "px)";
    }
    function schedule() {
      clearTimeout(timer);
      if (paused) return;
      var v = video(slides[cur]);
      var dur = v && v.duration && isFinite(v.duration) ? Math.max(v.duration, 4) * 1000 : 5000;
      hero.style.setProperty("--hero-dur", dur / 1000 + "s");
      timer = setTimeout(function () { go(cur + 1); }, dur);
    }
    function go(n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) {
        var on = i === cur;
        s.classList.toggle("is-on", on);
        s.setAttribute("aria-hidden", String(!on));
        s.querySelectorAll("button").forEach(function (b) { b.tabIndex = on ? 0 : -1; });
        s.querySelectorAll("video").forEach(function (v) { if (on && !paused) { v.currentTime = 0; var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause(); });
      });
      dots.forEach(function (d, i) {
        d.classList.toggle("is-on", i === cur);
        d.setAttribute("aria-current", String(i === cur));
        var sp = d.querySelector("span"); sp.replaceWith(sp.cloneNode(true)); // 진행 막대 다시 시작
      });
      if (curEl) curEl.textContent = String(cur + 1).padStart(2, "0");
      if (labelEl) labelEl.textContent = labels[cur] || "";
      place();
      schedule();
    }
    function setPaused(p) {
      paused = p;
      hero.classList.toggle("paused", p);
      pauseBtn.textContent = p ? "▶" : "Ⅱ";
      pauseBtn.setAttribute("aria-label", p ? "자동 넘김 시작" : "자동 넘김 멈춤");
      var v = video(slides[cur]);
      if (v) { if (p) v.pause(); else { var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } }
      if (p) clearTimeout(timer); else schedule();
    }
    hero.querySelector(".hero-prev").addEventListener("click", function () { go(cur - 1); });
    hero.querySelector(".hero-next").addEventListener("click", function () { go(cur + 1); });
    pauseBtn.addEventListener("click", function () { setPaused(!paused); });
    dots.forEach(function (d, i) { d.addEventListener("click", function () { go(i); }); });
    slides.forEach(function (s, i) { s.addEventListener("click", function (ev) { if (mode === "peek" && i !== cur) { ev.preventDefault(); ev.stopPropagation(); go(i); } }, true); });
    window.addEventListener("resize", place);
    hero.querySelectorAll("video").forEach(function (v) { v.addEventListener("loadedmetadata", function () { if (slides[cur].contains(v)) schedule(); }); });
    if (reduce) { paused = true; hero.classList.add("paused"); pauseBtn.textContent = "▶"; pauseBtn.setAttribute("aria-label", "자동 넘김 시작"); }
    go(0);
  });

  // 상품 미리보기
  var modal = document.getElementById("preview");
  var data = window.GTM_PRODUCTS || {};
  var lastFocus = null;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function priceHtml(p) {
    if (p.asking || !p.price) return '<p class="price"><span class="ask">가격문의</span></p>';
    if (p.sale) return '<p class="price"><del>' + esc(p.price) + '</del> <span class="pct">' + esc(p.pct || "") + "</span> <strong>" + esc(p.sale) + "</strong></p>";
    return '<p class="price"><strong>' + esc(p.price) + "</strong></p>";
  }
  function openPreview(id) {
    var p = data[id];
    if (!p || !modal) return;
    lastFocus = document.activeElement;
    var img = document.getElementById("pv-img");
    img.src = "../assets/img/" + p.img;
    img.alt = p.name;
    document.getElementById("pv-name").textContent = p.name;
    document.getElementById("pv-cat").textContent = p.cats.join(" · ");
    document.getElementById("pv-desc").textContent = p.desc || "";
    document.getElementById("pv-price").innerHTML = priceHtml(p);
    document.getElementById("pv-link").href = p.url;
    modal.hidden = false;
    body.classList.add("lock");
    modal.querySelector(".modal-close").focus();
  }
  function closePreview() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    body.classList.remove("lock");
    if (lastFocus) lastFocus.focus();
  }
  document.addEventListener("click", function (ev) {
    var t = ev.target.closest("[data-preview]");
    if (t) { ev.preventDefault(); openPreview(t.getAttribute("data-preview")); return; }
    if (ev.target.closest("[data-close]")) closePreview();
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "Escape") return;
    closePreview();
    if (drawer && !drawer.hidden) openDrawer(false);
  });
})();
