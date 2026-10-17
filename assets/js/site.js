/* Atelier Culemborg — kleine, afhankelijkheidsvrije scripts */
(function () {
  "use strict";

  /* ---------- mobiel menu ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function closeNav() {
    document.body.classList.remove("nav-open");
    if (toggle) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Menu openen");
    }
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeNav();
    });
  }

  /* ---------- submenu "Cursussen" ---------- */
  var groups = document.querySelectorAll(".nav__group");
  Array.prototype.forEach.call(groups, function (group) {
    var btn = group.querySelector("button");
    if (!btn) return;
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var open = group.getAttribute("data-open") !== "true";
      Array.prototype.forEach.call(groups, function (g) {
        g.setAttribute("data-open", "false");
        var b = g.querySelector("button");
        if (b) b.setAttribute("aria-expanded", "false");
      });
      group.setAttribute("data-open", open ? "true" : "false");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav__group")) {
      Array.prototype.forEach.call(groups, function (g) {
        g.setAttribute("data-open", "false");
        var b = g.querySelector("button");
        if (b) b.setAttribute("aria-expanded", "false");
      });
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      closeNav();
      Array.prototype.forEach.call(groups, function (g) {
        g.setAttribute("data-open", "false");
      });
    }
  });

  /* ---------- jaartal in de footer ---------- */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- afbeeldingen in beeld laten komen ---------- */
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reveals = document.querySelectorAll(".reveal");
  if (reduced || !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(reveals, function (el) {
      el.classList.add("is-in");
    });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    Array.prototype.forEach.call(reveals, function (el) {
      io.observe(el);
    });
  }

  /* ---------- lightbox ---------- */
  var dialog = document.getElementById("lightbox");
  var items = Array.prototype.slice.call(document.querySelectorAll(".gallery__item"));
  if (!dialog || !items.length) return;

  var img = dialog.querySelector("img");
  var caption = dialog.querySelector(".lightbox__caption");
  var current = 0;

  function show(index) {
    current = (index + items.length) % items.length;
    var item = items[current];
    img.src = item.getAttribute("data-full");
    img.alt = item.getAttribute("data-alt") || "";
    if (caption) caption.textContent = item.getAttribute("data-alt") || "";
    dialog.querySelector(".lightbox__prev").hidden = items.length < 2;
    dialog.querySelector(".lightbox__next").hidden = items.length < 2;
  }

  items.forEach(function (item, i) {
    item.addEventListener("click", function () {
      show(i);
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    });
  });

  dialog.querySelector(".lightbox__close").addEventListener("click", function () {
    dialog.close ? dialog.close() : dialog.removeAttribute("open");
  });
  dialog.querySelector(".lightbox__prev").addEventListener("click", function () {
    show(current - 1);
  });
  dialog.querySelector(".lightbox__next").addEventListener("click", function () {
    show(current + 1);
  });
  dialog.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") show(current + 1);
    if (e.key === "ArrowLeft") show(current - 1);
  });
  dialog.addEventListener("click", function (e) {
    if (e.target === dialog) dialog.close();
  });
})();
