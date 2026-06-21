/* =============================================================================
   reveal.js — subtle scroll-in reveal for editorial sections.

   Adds `.is-visible` to elements marked `.reveal` (the landing sections and
   the hero) as they enter the viewport. The CSS provides the fade + 8px rise
   ONLY inside `@media (prefers-reduced-motion: no-preference)`, so when the
   visitor prefers reduced motion the elements are fully visible and static and
   this script is a harmless no-op.

   Defensive: if IntersectionObserver is unavailable, every target is revealed
   immediately so nothing is ever stuck hidden.
   ========================================================================== */
(function () {
  "use strict";

  function revealAll(els) {
    els.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  function init() {
    var targets = Array.prototype.slice.call(
      document.querySelectorAll(".reveal")
    );
    if (!targets.length) return;

    // Honor reduced motion and missing-API: just show everything.
    var prefersReduced =
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReduced || !("IntersectionObserver" in window)) {
      revealAll(targets);
      return;
    }

    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { root: null, rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );

    targets.forEach(function (el) {
      observer.observe(el);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
