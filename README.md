# borch.dev

Personal academic site for Nick Borcherding, built with [Hugo](https://gohugo.io)
and the [Blowfish](https://github.com/nunocoracao/blowfish) theme. The site is a
single-page editorial landing (About, Research, Software, Publications, Contact)
plus list pages for posts and talks, and a publications view driven entirely
from a BibTeX source of truth.

## Stack

- **Hugo** (extended), theme imported as a Hugo module via `go.mod`. Requires
  Go on the build machine to resolve the module.
- **Blowfish** theme with local overrides in `layouts/` and a custom visual
  system (self-hosted Inter + Newsreader fonts, an ink-blue accent, a `borch`
  color scheme) in `assets/`.
- **Netlify** for hosting and deploys.

### Layout of the repo

```
config/_default/hugo.toml   site config (the only config root Hugo reads)
content/                    _index.md (home copy + software data), posts/, talks/, publications/
layouts/                    overrides on top of the Blowfish theme
assets/                     custom CSS/JS (theme color scheme, fonts, motion)
static/_redirects           legacy URL 301s (generated, see below)
static/fonts/               self-hosted woff2
static/files/               Borcherding_CV.pdf (rendered from cv.qmd in CI)
static/uploads/             managed by a separate deploy pipeline — do not edit by hand
data/                       publication pipeline inputs/outputs (see below)
                            plus legacy_redirects.yaml, the old URL map
scripts/                    publication, CV, and redirect pipeline scripts
cv.qmd                      Quarto CV, rendered to PDF in CI
```

## Publications: one source, two outputs

Publications are data-driven, not per-paper content folders. A single BibTeX
file feeds both the website and the CV.

```
data/pubs.bib  ──(scripts/bib_to_yaml.py)──▶  data/publications.yaml  ──▶  site /publications/
      │                                                                └──▶  cv.qmd ──▶ CV PDF
      └── data/pub_meta.yaml  (hand-curated overlay, keyed by PMID)
```

- **`data/pubs.bib`** is the canonical publication list. CI refreshes it from
  MyNCBI (`scripts/update_pubs_from_ncbi.py`).
- **`scripts/bib_to_yaml.py`** converts the bib into `data/publications.yaml`,
  which both the site and the CV consume.
- **`data/pub_meta.yaml`** is a hand-maintained overlay keyed by PMID. It holds
  the things the bib does not: the `featured` flag, tags, extra links, abstract,
  and highlight text. (`scripts/seed_pub_meta.py` was a one-time seeder from the
  old Wowchemy folders; it is not part of CI.)

### Featuring or curating a publication

Edit `data/pub_meta.yaml`. Find (or add) the entry for the paper's PMID and set
the overlay fields, e.g.:

```yaml
'40123456':
  featured: true
  tags: [single-cell, TCR]
  highlight: One-line takeaway shown on the publications page.
  links:
    pdf: https://...
```

Do not edit `data/publications.yaml` by hand — it is regenerated from the bib.
Put durable, hand-curated metadata in `pub_meta.yaml`.

## Legacy URL redirects

The move off Wowchemy (commit `d78f6ba`) deleted every old content page, so the
URLs Google and Google Scholar still index all 404. `static/_redirects` catches
them with Netlify 301s.

```
data/legacy_redirects.yaml  ──(scripts/gen_redirects.py)──▶  static/_redirects
```

- **`data/legacy_redirects.yaml`** is the map: old publication slug to PMID,
  old tag slugs, renamed post slugs. Hand-maintained. It was seeded once from
  git history by `scripts/seed_legacy_redirects.py`, which is not part of CI
  and should not need running again.
- **`scripts/gen_redirects.py`** writes `static/_redirects`. Netlify does not
  run Python, so the generated file is committed. Hugo copies `static/` into
  `public/` verbatim.

Old per-paper pages land on their own entry in the list, at
`/publications/#pmid-<pmid>`. The anchor comes from the `id` in
`layouts/partials/publications/entry.html`, and `.pub:target` in
`assets/css/custom.css` marks the entry on arrival.

Old `/tag/<slug>/` pages land on `/publications/?q=<slug>`, which prefills the
filter. That works because `entry.html` also emits `data-tags` from the curated
tags in `pub_meta.yaml`, so the filter matches on topic rather than on title
text alone.

Re-run the generator after editing the map, and verify against a real build:

```bash
python3 scripts/gen_redirects.py
hugo --gc --minify && python3 scripts/gen_redirects.py --check
```

`--check` fails if any rule points at a PMID anchor the page no longer renders
or a path that does not exist. Note that `_redirects` is a Netlify feature and
does nothing under `hugo server`; test real 301s on a deploy preview.

## Build and preview locally

Requires Hugo extended and Go (for the theme module).

```bash
hugo server            # live preview at http://localhost:1313
hugo --gc --minify     # production-style build into public/
```

The production build command matches what Netlify runs.

## Deploy

Netlify builds from `netlify.toml`:

```toml
command = "hugo --gc --minify -b $URL"
[build.environment]
HUGO_VERSION = "0.163.3"
```

Because the theme is a Hugo module, the build needs Go available. Netlify's
default build image includes Go; confirm on the first deploy after a Hugo
version bump.

The CV PDF at `static/files/Borcherding_CV.pdf` is rendered separately by the
`Build CV` GitHub Action (`.github/workflows/build-cv.yml`): it refreshes
`pubs.bib` from MyNCBI, regenerates `publications.yaml`, then renders `cv.qmd`
to PDF with Quarto and commits the artifact.
