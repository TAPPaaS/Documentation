/* WS1 Spike A — reveal-on-scroll for the landing page (no-op on other pages). */
(function () {
  "use strict";

  function init() {
    var landing = document.querySelector(".tap-landing");
    if (!landing) return;

    var items = landing.querySelectorAll(".tap-reveal");
    if (!("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("tap-in"); });
      return;
    }
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

  // Material's instant navigation re-renders the page without a full load;
  // document$ fires on every page change (and once on initial load).
  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
