/* Progressive-enhancement client-side filter for the publications list.
 *
 * The full list is server-rendered; this script only HIDES non-matching
 * entries. With JS disabled, every publication is visible (additive behaviour).
 * Vanilla JS, no dependencies.
 */
(function () {
  "use strict";

  var root = document.querySelector("[data-pub-filter]");
  var list = document.getElementById("pub-list");
  if (!root || !list) return;

  var search = document.getElementById("pub-search");
  var chips = Array.prototype.slice.call(root.querySelectorAll(".pub-chip"));
  var groups = Array.prototype.slice.call(list.querySelectorAll(".pub-year-group"));
  var entries = Array.prototype.slice.call(list.querySelectorAll(".pub"));
  var countEl = document.getElementById("pub-count");
  var emptyEl = document.querySelector("[data-pub-empty]");

  var activeYear = "all";

  // Pre-compute lowercased searchable text for each entry once. data-tags holds
  // the curated topic vocabulary from pub_meta.yaml, which is not otherwise in
  // the rendered text, so legacy /tag/<slug>/ redirects can match on topic.
  entries.forEach(function (el) {
    var tags = el.getAttribute("data-tags") || "";
    el._text = ((el.textContent || "") + " " + tags).toLowerCase();
  });

  function apply() {
    var q = (search ? search.value : "").trim().toLowerCase();
    var visible = 0;

    entries.forEach(function (el) {
      var matchYear = activeYear === "all" || el.getAttribute("data-year") === activeYear;
      var matchText = q === "" || el._text.indexOf(q) !== -1;
      var show = matchYear && matchText;
      el.hidden = !show;
      if (show) visible++;
    });

    // Hide a year group entirely when none of its entries are visible.
    groups.forEach(function (g) {
      var any = Array.prototype.some.call(g.querySelectorAll(".pub"), function (el) {
        return !el.hidden;
      });
      g.hidden = !any;
    });

    if (countEl) countEl.textContent = visible;
    if (emptyEl) emptyEl.hidden = visible !== 0;
  }

  if (search) {
    search.addEventListener("input", apply);
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      activeYear = chip.getAttribute("data-year") || "all";
      chips.forEach(function (c) {
        c.classList.toggle("is-active", c === chip);
      });
      apply();
    });
  });

  // Prefill from ?q=, which is where the legacy /tag/<slug>/ redirects land.
  var preset = new URLSearchParams(window.location.search).get("q");
  if (preset && search) {
    search.value = preset;
    apply();
  }

  // Legacy /publication/<slug>/ redirects land on #pmid-<id>. The browser's own
  // jump happens before this script runs, and web fonts and images settle after
  // it, which shifts everything above the target. So anchor now and again as
  // those land.
  //
  // Explicitly instant: the site sets scroll-behavior:smooth, and a smooth
  // scroll started this early gets cancelled while the page is still settling,
  // leaving the visitor stranded at the top. Instant is also the right landing
  // for someone arriving from a redirect.
  function anchor() {
    var target;
    try {
      target = document.querySelector(window.location.hash);
    } catch (e) {
      return; // malformed hash
    }
    if (!target) return;
    try {
      target.scrollIntoView({ behavior: "instant", block: "start" });
    } catch (e) {
      // Older browsers reject "instant"; bypass the CSS smooth by hand.
      var root = document.documentElement;
      var prev = root.style.scrollBehavior;
      root.style.scrollBehavior = "auto";
      root.scrollTop = target.getBoundingClientRect().top + root.scrollTop - 96;
      root.style.scrollBehavior = prev;
    }
  }

  if (window.location.hash) {
    anchor();
    window.addEventListener("load", anchor);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(anchor);
    }
  }
})();
