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

  // Pre-compute lowercased searchable text for each entry once.
  entries.forEach(function (el) {
    el._text = (el.textContent || "").toLowerCase();
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
})();
