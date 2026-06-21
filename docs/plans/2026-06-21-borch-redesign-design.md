# borch.dev Redesign — Editorial-Minimal, Data-Driven Hugo

**Date:** 2026-06-21
**Status:** Approved design, pending implementation plan

## Goal

Modernize borch.dev aesthetically and structurally. Move off the maintenance-mode
Wowchemy/Academic theme to a modern, actively-maintained Hugo base, adopt an
editorial-minimal visual language, and unify the two parallel publication sources
into one auto-updated source of truth.

## Current state (as found)

- Hugo + Wowchemy/Academic ("dev" theme variant), Hugo 0.87.0 (2021).
- Two parallel publication sources:
  - `data/pubs.bib` — auto-pulled weekly from MyNCBI via
    `scripts/update_pubs_from_ncbi.py`, feeds the CV (`cv.qmd` -> Quarto PDF).
    Complete and current, minimal metadata.
  - `content/publication/*` — 88 hand-maintained Wowchemy folders feeding the
    website. Richer (abstracts, tags, `featured`, code/PDF links) but manual and
    drifting out of sync with the bib.
- `data/cv.yml` (24KB) holds structured education/experience.
- CI: `.github/workflows/build-cv.yml` (push + weekly cron) runs the pub updater
  and builds the CV PDF. `updater-wip.yml` is a Wowchemy news updater.
- Deploy: Netlify (`netlify.toml`) + a GitHub Pages deploy flow.

## Decisions

- **Stack:** Blowfish theme as chrome/plumbing (Tailwind, dark/light toggle,
  search, RSS, SEO, image processing, syntax highlighting). Override layouts and
  CSS for the editorial look.
- **Hugo:** bump 0.87 -> current extended (~0.140+). Update
  `netlify.toml` `HUGO_VERSION`.
- **Aesthetic:** editorial minimal. Serif display (Newsreader) + clean sans body
  (Inter/Mukta). Near-black on warm off-white, single ink-blue accent used for
  links, section numerals, and hairline rules. Warm near-black dark mode. Subtle
  motion only (scroll fade/slide, link/hover transitions). No carousels/parallax.

### Single source of truth for publications

Retire `content/publication/`. Drive the site from the same `data/pubs.bib` the CV
uses, so one NCBI pull updates CV + website.

- Extend `update_pubs_from_ncbi.py` to also emit `data/publications.yaml`
  (Hugo-native) from the bib in the same CI run.
- Curation overlay `data/pub_meta.yaml`, keyed by PMID, holds what the bib lacks:
  `featured`, code/PDF/project links, tags, optional one-line highlight.
- Seed `pub_meta.yaml` automatically by extracting metadata from the existing 88
  folders (one-time script) so no curation is lost.
- Publications page renders from `publications.yaml`, grouped by year. Landing-page
  "Selected" section filters `featured: true`.

### Information architecture

Single-page editorial landing + dedicated full pages for deep content.

Landing (`/`), numbered editorial sections:
- Hero — name, title, WashU affiliation, one-line research statement, social row
  (Scholar/ORCID/GitHub/LinkedIn), CV button.
- 01 · About — short bio markdown + interests, partly from `cv.yml`.
- 02 · Research — 3-4 focus areas as clean text blocks.
- 03 · Software — tools (scRepertoire etc.) as a restrained grid with repo/docs links.
- 04 · Selected publications — featured subset, link to full list.
- 05 · Contact — email, location, links.

Full pages: `/publications` (all, by year, filterable), `/software`, `/posts` +
`/posts/<slug>`, `/talks`. Nav stays minimal.

### Publication detail

- Full list links straight to DOI/PubMed (lean).
- Featured pubs get an inline expandable abstract.
- No per-publication detail pages.

## Preserved vs. changed vs. risk

- **Preserved:** CV pipeline, `pubs.bib` auto-update, `cv.yml`, all publication
  curation (migrated into `pub_meta.yaml`), post/software URLs where feasible.
- **Changed:** homepage moves from Wowchemy widgets to editorial layouts.
  `content/publication/` retired after extraction (kept in git history).
- **Risk/watch:** Hugo version bump interacts with Netlify cache plugin; verify
  build. Confirm GitHub Pages vs Netlify is the live deploy path before cutover.

## Open items resolved with defaults

1. Publications -> link-out + inline abstract for featured. (link-out chosen)
2. Accent -> ink-blue.
3. Display font -> Newsreader.
