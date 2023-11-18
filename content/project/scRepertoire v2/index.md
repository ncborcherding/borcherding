---
title: scRepertoire v2
summary: A toolkit for single-cell immune profiling
tags:
- TCR
- BCR
- Single-Cell
- Immunology
- R
- Software
date: "2023-01-06T00:00:00Z"

# Optional external URL for project (replaces project detail page).
external_link: "https://github.com/ncborcherding/scRepertoire"

image:
  caption: Attaching single-cell repertoires to gene expression data
  focal_point: Smart

links:
- icon: twitter
  icon_pack: fab
  name: Follow
  url: https://twitter.com/theHumanBorch
url_code: "https://github.com/ncborcherding/scRepertoire"
#url_pdf: 
#url_slides: ""
#url_video: ""
---

Single-cell sequencing is an emerging technology in the field of immunology and oncology that allows researchers to couple RNA quantification and other modalities, like immune cell receptor profiling at the level of an individual cell. A number of workflows and software packages have been created to process and analyze single-cell transcriptomic data. These packages allow users to take the vast dimensionality of the data generated in single-cell-based experiments and distill the data into novel insights. Unlike the transcriptomic field, there is a lack of options for software that allow for single-cell immune receptor profiling. Enabling users to easily combine RNA and immune profiling, scRepertoire was built to process data derived from the 10x Genomics Chromium Immune Profiling for both T-cell receptor (TCR) and immunoglobulin (Ig) enrichment workflows and subsequently interacts with the popular Seurat R package.