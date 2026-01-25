---
title: Trex
summary: Autoencoder for single-cell TCR
tags:
- Deep Learning
- TCR
- Immunology
- R
- Software
date: "2023-01-06T00:00:00Z"

# Optional external URL for project (replaces project detail page).
external_link: "https://github.com/ncborcherding/Trex"

image:
  caption: Approach to autoencoding cdr3 sequence for TCR
  focal_point: Smart

url_code: "https://github.com/ncborcherding/Trex"
#url_pdf: ""
#url_slides: ""
#url_video: ""
---

Single-cell sequencing is now a integral tool in the field of immunology and oncology that allows researchers to couple RNA quantification and other modalities, like immune cell receptor profiling at the level of an individual cell. Towards this end, we developed the scRepertoire R package to assist in the interaction of immune receptor and gene expression sequencing. However, utilization of clonal indices for more complex analyses are still lacking, specifically in using clonality in embedding of single-cells. To this end, we developed an R package that uses deep learning to vectorize TCR sequences using order or translating the sequence into amino acid properties.