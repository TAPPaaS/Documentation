/* Landing page behavior (no-op on other pages): reveal-on-scroll, pointer
   parallax on the hero orbs, hover glow on the block cards. Subscribes to
   Material's document$ so it re-runs under instant navigation. */
(function () {
  "use strict";

  function init() {
    var landing = document.querySelector(".tap-landing");
    if (!landing) return;

    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // Reveal on scroll
    var items = landing.querySelectorAll(".tap-reveal");
    if (reduced || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("tap-in"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("tap-in");
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
      items.forEach(function (el) { io.observe(el); });
    }

    // Gentle pointer parallax on the hero orbs
    if (!reduced) {
      var orbs = landing.querySelectorAll("[data-tap-parallax]");
      document.addEventListener("pointermove", function (ev) {
        var cx = ev.clientX / window.innerWidth - 0.5;
        var cy = ev.clientY / window.innerHeight - 0.5;
        orbs.forEach(function (o) {
          var f = parseFloat(o.getAttribute("data-tap-parallax"));
          o.style.transform = "translate(" + cx * f + "px, " + cy * f + "px)";
        });
      }, { passive: true });
    }

    // Hover glow follows the pointer on the building-block cards
    landing.querySelectorAll(".tap-card").forEach(function (card) {
      card.addEventListener("pointermove", function (ev) {
        var r = card.getBoundingClientRect();
        card.style.setProperty("--tap-mx", ev.clientX - r.left + "px");
        card.style.setProperty("--tap-my", ev.clientY - r.top + "px");
      });
    });
  }

  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
