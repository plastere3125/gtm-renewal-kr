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

  // B안 히어로 장면 전환(6초 자동, 멈춤 가능, 동작 줄이기 설정 존중)
  document.querySelectorAll(".b-hero-slides").forEach(function (box) {
    var slides = box.querySelectorAll(".hs-slide");
    var dots = box.querySelectorAll(".hs-dot");
    var pause = box.querySelector(".hs-pause");
    var cur = 0, timer = null;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    function show(n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle("is-on", i === cur); s.setAttribute("aria-hidden", String(i !== cur)); });
      dots.forEach(function (d, i) { d.classList.toggle("is-on", i === cur); d.setAttribute("aria-current", String(i === cur)); });
    }
    function play() { stop(); timer = setInterval(function () { show(cur + 1); }, 6000); pause.textContent = "Ⅱ"; pause.setAttribute("aria-label", "자동 넘김 멈춤"); }
    function stop() { if (timer) clearInterval(timer); timer = null; }
    dots.forEach(function (d, i) { d.addEventListener("click", function () { show(i); if (timer) play(); }); });
    pause.addEventListener("click", function () {
      if (timer) { stop(); pause.textContent = "▶"; pause.setAttribute("aria-label", "자동 넘김 시작"); } else play();
    });
    box.addEventListener("focusin", stop);
    show(0);
    if (!reduce) play(); else { pause.textContent = "▶"; pause.setAttribute("aria-label", "자동 넘김 시작"); }
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
