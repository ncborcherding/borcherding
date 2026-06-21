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
static/fonts/               self-hosted woff2
static/files/               Borcherding_CV.pdf (rendered from cv.qmd in CI)
static/uploads/             managed by a separate deploy pipeline — do not edit by hand
data/                       publication pipeline inputs/outputs (see below)
scripts/                    publication + CV pipeline scripts
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
