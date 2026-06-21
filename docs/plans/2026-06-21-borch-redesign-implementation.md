# borch.dev Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the maintenance-mode Wowchemy/Academic site with a modern Blowfish-based Hugo site in an editorial-minimal style, driven by a single auto-updated publication source.

**Architecture:** Blowfish provides chrome/plumbing (nav, dark/light, search, SEO). Custom `layouts/` overrides + Tailwind config provide the editorial look. Publications render from `data/publications.yaml` (generated from `data/pubs.bib`, the same file the CV uses) plus a hand-curated `data/pub_meta.yaml` overlay. The Wowchemy widget homepage is replaced by editorial section partials.

**Tech Stack:** Hugo extended (~0.140+), Blowfish theme (Hugo Module), Tailwind, Python 3.11 (bib→yaml + seed extraction), existing Quarto CV pipeline (untouched).

**Domain note on "tests":** This is a static site, so TDD unit tests don't apply to layouts. "Verification" here means: `hugo` builds with zero errors/warnings, generated data files have the expected record counts, rendered HTML contains expected markers, and visual checks via the preview tools. Each task ends with an explicit verification command and expected output, then a commit. Per the repo owner's rule, **commits require a go-ahead** — batch the go-ahead per phase.

**Working branch:** all work on `redesign-editorial` (created in Phase 0), never on `master`. Keep the Wowchemy site building until Phase 6 cutover so we always have a working fallback.

---

## Phase 0 — Pre-flight & safety

### Task 0.1: Confirm the live deploy path

**Why:** `netlify.toml` exists AND there are GitHub Actions deploy commits. We must know which one serves borch.dev before cutover (Phase 6), so we change the right config.

**Steps:**
1. Check Netlify: `gh api repos/ncborcherding/borcherding/deployments --jq '.[0]' 2>/dev/null` and look in repo settings / DNS for borch.dev CNAME target.
   Run: `dig +short borch.dev` and `dig +short www.borch.dev` — note whether it points at Netlify (`*.netlify.app`) or GitHub Pages (`*.github.io`).
2. Inspect what `BorchLab/bHIVE` deploys here: `git log --name-only --pretty=format: -5 $(git log --grep="bHIVE" --format=%H -1) | sort -u | head` — confirm it only writes under `static/uploads/` (or similar). Record the path.

**Expected:** A one-line note in this file (append under this task) stating "Live deploy = Netlify | GitHub Pages" and "bHIVE writes to `<path>`". Do not proceed to cutover planning until known.

**FINDING (2026-06-21):** Live deploy = **Netlify** (`www.borch.dev` CNAME → `infallible-bell-d93b08.netlify.app`; apex on Netlify IPs). bHIVE writes **only** to `static/uploads/bhive/` (pkgdown docs) — isolated; never touch that path. Cutover (Phase 6) = `netlify.toml` change.

### Task 0.2: Install Hugo extended locally

Run: `brew install hugo && hugo version`
Expected: prints `hugo v0.1xx … extended`. If `+extended` is missing, `brew reinstall hugo` (the cask is extended by default on macOS).

### Task 0.3: Create the working branch and baseline snapshot

```bash
git checkout -b redesign-editorial
```
Capture a baseline screenshot of the current live site for before/after reference (use the `run`/preview tooling against `https://borch.dev`). Save nothing to git yet.

**Verification:** `git branch --show-current` → `redesign-editorial`.

---

## Phase 1 — Stand up Blowfish alongside Wowchemy

Goal: a second, parallel Hugo config that builds a Blowfish site, without deleting Wowchemy yet.

### Task 1.1: Add Blowfish as a Hugo Module

**Files:** Modify `go.mod`, create `config/blowfish/` (new config set we build with `--environment blowfish`).

**Steps:**
1. `hugo mod get -u github.com/nunocoracao/blowfish/v2`
2. Create `config/blowfish/hugo.toml` with `theme = ["github.com/nunocoracao/blowfish/v2"]`, `baseURL`, `title = "Nick Borcherding"`, `module.imports.path = "github.com/nunocoracao/blowfish/v2"`.
3. Copy Blowfish's sample `params.toml`, `menus.en.toml`, `languages.en.toml` from its `config/_default/` into `config/blowfish/`.

**Verification:**
Run: `hugo --environment blowfish --gc -d /tmp/bf_build`
Expected: build succeeds (a near-empty site is fine). FAIL here = module path or Hugo version wrong; fix before continuing.

### Task 1.2: Wire minimal identity & nav into Blowfish config

**Files:** `config/blowfish/params.toml`, `config/blowfish/menus.en.toml`

Set author name "Nick Borcherding", role, the social links (Scholar/ORCID/GitHub/LinkedIn) pulled from `content/authors/admin/_index.md`, color scheme, and `defaultAppearance`. Menu: Home, Research, Software, Publications, Posts, Talks, CV (CV → `files/Borcherding_CV.pdf`).

**Verification:** `hugo --environment blowfish server` then preview `localhost:1313` — header shows the name and all menu items. Screenshot.

**Commit checkpoint (Phase 1).**

---

## Phase 2 — Publication data pipeline (single source of truth)

Goal: generate `data/publications.yaml` from `data/pubs.bib`, and seed `data/pub_meta.yaml` from the 88 legacy folders. This is the load-bearing custom work.

### Task 2.1: Write the bib→yaml converter

**Files:** Create `scripts/bib_to_yaml.py`, output `data/publications.yaml`.

```python
#!/usr/bin/env python3
"""Convert data/pubs.bib -> data/publications.yaml for the Hugo site.
One source of truth shared with the CV. Run in CI after the NCBI update."""
import re, sys, yaml
import bibtexparser

IN_BIB = "data/pubs.bib"
OUT_YAML = "data/publications.yaml"

def split_authors(field: str):
    # bibtex "Last, First and Last, First" -> ["First Last", ...]
    out = []
    for a in field.split(" and "):
        a = a.strip()
        if "," in a:
            last, first = [p.strip() for p in a.split(",", 1)]
            out.append(f"{first} {last}".strip())
        else:
            out.append(a)
    return out

def main():
    with open(IN_BIB, encoding="utf-8") as f:
        db = bibtexparser.load(f)
    entries = []
    for e in db.entries:
        pmid = e.get("pmid", "").strip()
        entries.append({
            "key": e.get("ID"),
            "pmid": pmid,
            "title": re.sub(r"[{}]", "", e.get("title", "")).strip().rstrip("."),
            "authors": split_authors(e.get("author", "")),
            "journal": re.sub(r"[{}]", "", e.get("journal", "")).strip(),
            "year": int(e["year"]) if e.get("year", "").isdigit() else None,
            "volume": e.get("volume", ""),
            "number": e.get("number", ""),
            "pages": e.get("pages", ""),
            "doi": e.get("doi", "").strip(),
            "pubmed": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
        })
    entries.sort(key=lambda x: (x["year"] or 0), reverse=True)
    with open(OUT_YAML, "w", encoding="utf-8") as f:
        yaml.safe_dump({"publications": entries}, f, allow_unicode=True, sort_keys=False)
    print(f"Wrote {len(entries)} publications to {OUT_YAML}")

if __name__ == "__main__":
    sys.exit(main())
```

**Verification:**
Run: `pip install bibtexparser pyyaml && python scripts/bib_to_yaml.py`
Expected: `Wrote N publications to data/publications.yaml` where N ≈ entry count of `pubs.bib`. Cross-check: `grep -c "^@" data/pubs.bib` should equal N. Spot-check the YAML top entry has title/authors/year/doi.

### Task 2.2: Seed the curation overlay from the 88 legacy folders

**Files:** Create `scripts/seed_pub_meta.py`, output `data/pub_meta.yaml`.

Logic: walk `content/publication/*/index.md`, parse front matter (`python-frontmatter`), and for each, derive a PMID where possible (from `links[].url` or `url_pdf` containing `pubmed/<id>`, else from DOI match against `pubs.bib`). Emit a dict keyed by PMID with: `featured`, `tags`, `highlight` (first sentence of abstract, optional), and `links` (code/pdf/project/poster/slides from the `url_*` and `links` fields). Skip entries with no resolvable key and **log them** so none silently vanish.

**Verification:**
Run: `pip install python-frontmatter && python scripts/seed_pub_meta.py`
Expected: prints `Seeded M entries, K unmatched (listed below)`. Manually review the unmatched list; resolve by hand into `pub_meta.yaml` if any were `featured`. Confirm every `featured: true` legacy pub appears in the overlay.

### Task 2.3: Extend the CI updater to emit both files

**Files:** Modify `.github/workflows/build-cv.yml`, modify `scripts/update_pubs_from_ncbi.py` (or just add a step).

Add a workflow step after the NCBI update and before the CV build:
```yaml
      - name: Generate publications.yaml for the website
        run: |
          pip install bibtexparser pyyaml
          python scripts/bib_to_yaml.py
```
Ensure the existing "commit artifacts" step also adds `data/publications.yaml`.

**Verification:** `act` if available, else dry-read the YAML diff. Expected: workflow file is valid (`yamllint .github/workflows/build-cv.yml` or `gh workflow view`).

**Commit checkpoint (Phase 2).**

---

## Phase 3 — Editorial layouts & content migration

Goal: build the single-page editorial landing and the section content, reading from `data/` and existing content.

### Task 3.1: Landing layout shell with numbered sections

**Files:** Create `layouts/index.html` (overrides Blowfish home), `assets/css/custom.css`.

Render, in order: Hero partial, `01 · About`, `02 · Research`, `03 · Software`, `04 · Selected publications`, `05 · Contact`. Each section wrapped in `<section id="…">` with a numeral element (`<span class="sec-num">01</span>`) and a hairline rule. Pull hero identity from `content/authors/admin/_index.md` (or move those fields into `config/blowfish/params.toml` author block).

**Verification:** build + preview. Expected: five labeled sections render in order with visible numerals. Screenshot.

### Task 3.2: About + Research content

**Files:** Create `content/_index.md` (front matter with `research_areas` list of 3–4 {title, blurb}), reference `data/cv.yml` for education/experience summary if desired.

Bio and interests come from the existing author file. Research areas authored fresh (3–4 focus blocks: Tumor Immunology, Immunometabolism, Single-Cell Immune Profiling, AIRR analysis).

**Verification:** sections show real bio text + 3–4 research blocks, no Lorem.

### Task 3.3: Software section

**Files:** Create `layouts/partials/home/software.html`.

Reuse the existing curated copy in `content/software/_index.md` (scRepertoire, immReferent, etc.) rendered as a restrained 2-col grid: name, one-line description, role, repo/docs links. Do **not** touch `static/uploads/` (bHIVE territory).

**Verification:** software grid lists the real packages with working repo links.

### Task 3.4: Posts and Talks full pages

**Files:** Confirm `content/post/` and `content/event/` (talks) render under Blowfish's list/single templates; add `layouts/` overrides only if styling demands.

**Verification:** `/posts` lists existing posts; clicking one renders the body. `/talks` lists events.

**Commit checkpoint (Phase 3).**

---

## Phase 4 — Publications views

### Task 4.1: Full publications page (by year)

**Files:** Create `content/publications/_index.md` (type page), `layouts/publications/list.html`.

Read `site.Data.publications.publications`, group by `year` desc. For each: authors (bold "Borcherding, N*"/"Borcherding, Nicholas"), title, italic journal + year;vol(no):pages; a links row built from `pub_meta` overlay (DOI, PubMed, Code, PDF). Add a lightweight client-side year/keyword filter (vanilla JS, progressive — list works without JS).

**Verification:**
- `hugo --environment blowfish` build clean.
- Rendered `/publications/` count equals `len(publications.yaml)`; verify: open preview, count headings, compare to `grep -c "^@" data/pubs.bib`.
- A known featured pub shows its Code/PDF links from the overlay.

### Task 4.2: Selected publications on landing

**Files:** `layouts/partials/home/selected-pubs.html`.

Filter `publications` whose PMID is `featured: true` in `pub_meta.yaml`; render compact, each with an inline `<details>` abstract (abstract pulled from overlay `highlight`/abstract field). "See all publications →" links to `/publications/`.

**Verification:** landing shows only featured pubs; abstract expander works; link navigates.

**Commit checkpoint (Phase 4).**

---

## Phase 5 — Editorial visual system

### Task 5.1: Type & color tokens

**Files:** `config/blowfish/params.toml` (color scheme), `assets/css/custom.css`, Blowfish color CSS overrides.

- Fonts: Newsreader (display/headings) + Inter or Mukta (body), self-hosted from `data/fonts/` or `static/fonts/` (avoid Google Fonts CDN for privacy — there's a `privacy_pack` heritage). `@font-face` in custom.css.
- Color: define CSS vars — `--bg: #FAF8F4` (warm off-white), `--ink: #15171A`, `--accent: #1F3A5F` (ink-blue), hairline `--rule: #DFD9CF`. Dark mode vars: warm near-black `#16140F`/off-white ink, same accent lightened.
- Apply accent to links, `.sec-num`, rules; large confident heading sizes; generous `line-height`.

**Verification:** preview light + dark. Expected: serif headings, off-white canvas, ink-blue accents, readable contrast (check WCAG AA via the preview/inspect tooling — body text ≥ 4.5:1).

### Task 5.2: Motion & polish

**Files:** `assets/js/reveal.js` (IntersectionObserver scroll-reveal), `assets/css/custom.css`.

Subtle only: fade/slide-in on section enter (respect `prefers-reduced-motion`), link underline transitions, software-card hover lift. No carousels/parallax.

**Verification:** sections fade in on scroll; with `prefers-reduced-motion: reduce` set, content is static and fully visible.

**Commit checkpoint (Phase 5).**

---

## Phase 6 — Build hardening, CI, and cutover

### Task 6.1: Bump Hugo everywhere

**Files:** `netlify.toml` (`HUGO_VERSION`), any GH Actions that build the site.

Set `HUGO_VERSION` to the installed extended version (match Task 0.2). Verify Netlify cache plugin compatibility; if it breaks, drop `netlify-plugin-hugo-cache-resources`.

**Verification:** `hugo --environment blowfish --gc --minify` → clean. Note build time.

### Task 6.2: Promote Blowfish config to default

**Files:** Move `config/blowfish/*` → `config/_default/*` (replace Wowchemy config). Remove Wowchemy module imports from `module.imports`. Keep `config/_default` as the single config.

**Verification:** `hugo --gc --minify` (no `--environment`) builds the Blowfish site. Full preview pass of every page + dark mode. Run a link check: `hugo` + `lychee public/` (or `htmltest`). Expected: zero broken internal links.

### Task 6.3: Deploy verification

Using the finding from Task 0.1, push `redesign-editorial`, open a Netlify deploy preview (or GH Pages preview), and review the live preview URL end to end before any merge to `master`.

**Verification:** deploy preview matches local; CV PDF link resolves; publications populated.

**Commit + open PR (with go-ahead).**

---

## Phase 7 — Cleanup

### Task 7.1: Retire Wowchemy remnants

**Files:** Delete `content/home/` (widgets), `content/publication/` (88 folders, after confirming overlay captured curation), `update_wowchemy.sh`, `theme.toml`, `.github/workflows/updater-wip.yml` (Wowchemy news updater), `config/_default/params.yaml` Wowchemy keys.

**Verification:** `hugo --gc --minify` still clean; `git status` shows only intended deletions; site unaffected (data-driven pubs already live).

### Task 7.2: Docs

**Files:** Update `README.md` to describe the new stack, the `pubs.bib → publications.yaml → site + CV` flow, and how to add a featured pub (edit `pub_meta.yaml`).

**Verification:** README steps reproduce a local build from clean checkout.

**Final commit + merge to master (with go-ahead). Re-run the CV workflow once to confirm the unified pipeline emits both `pubs.bib` and `publications.yaml`.**

---

## Phase 1 outcome notes (2026-06-21)

- **Isolation mechanism changed:** both planned approaches leaked Wowchemy modules (Hugo always reads `config/_default/` as base). Final approach: a separate config root `config-blowfish/_default/hugo.toml` built with `hugo --configDir config-blowfish`, plus an isolated `content-blowfish/` contentDir. Phase 3 builds content under `content-blowfish/`; Phase 6 cutover swaps configDir+contentDir to default.
- **Wowchemy no longer builds locally on Hugo 0.163.3** (pre-existing incompat: `publishdate` parse, `_build` key, `WC_POST_CSS` getenv policy). The real fallback is the **live Netlify site pinned at HUGO_VERSION 0.87.0**, not a local build. Acceptable — we never need a local Wowchemy build.
- **Go toolchain required:** Hugo Modules need `go` (installed locally via brew, go 1.26.4). Phase 6 must confirm Netlify build image provides Go for `hugo mod`.
- **Blowfish ↔ Hugo version:** Blowfish v2.103.0 warns (non-fatal) on Hugo 0.163. Watch for a hard failure on future bumps; pin if needed.

## Phase 2 outcome notes (2026-06-21)

- Bib has **91** entries (not ~88). `publications.yaml` = 91, verified == bib count.
- Overlay `pub_meta.yaml`: 83 seeded, 4 unmatched (all `featured:false` — older editorial pieces + one brand-new preprint not yet in the bib). All **7 featured** pubs preserved. Seeder auto-reconciled 4 stale/copy-pasted PMIDs in legacy folders (printed under RECONCILED).
- **All 91 bib entries lack DOI** (MyNCBI pull populates pmid/year, never doi). Site links use PubMed. If DOI links are wanted later, `update_pubs_from_ncbi.py` must fetch them.
- **CARRY INTO PHASE 4 (Task 4.1):** three titles contain HTML markup (`<i>`/`<sub>`, PMIDs 31619506, 33627663, 40687995 — gene names, subscripts). The publications layout must render titles with `| safeHTML` (or markdownify) so these show as intended italics/subscripts, not literal tags. Do NOT strip in the script.

## Risk register

- **Hugo bump breaks Netlify cache plugin** → drop the plugin (Task 6.1).
- **bib lacks abstracts** → featured abstracts come from the overlay seeded from legacy folders; non-featured pubs link out (by design).
- **PMID↔DOI matching gaps in seed** → Task 2.2 logs unmatched; resolve featured ones by hand.
- **bHIVE deploy collision** → never touch `static/uploads/`; confirm path in Task 0.1.
- **Parallel `jules/website-quality-improvements` branch** → check it before merge to avoid clobbering; cherry-pick anything useful.
```
