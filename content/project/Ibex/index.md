---
title: Ibex
summary: Autoencoder for single-cell BCR
tags:
- Deep Learning
- BCR
- Immunology
- R
- Software
date: "2023-01-06T00:00:00Z"

# Optional external URL for project (replaces project detail page).
external_link: "https://github.com/ncborcherding/Ibex"

image:
  caption: Approach to autoencoding cdr3 sequence for BCR
  focal_point: Smart

links:
- icon: twitter
  icon_pack: fab
  name: Follow
  url: https://twitter.com/theHumanBorch
url_code: "https://github.com/ncborcherding/Ibex"
url_pdf: "https://www.biorxiv.org/content/10.1101/2022.11.09.515787v1.full.pdf+html"
#url_slides: ""
#url_video: ""
---

B cells are critical for adaptive immunity and are governed by the recognition of an antigen by the B cell receptor (BCR), a process that drives a coordinated series of signaling events and modulation of various transcriptional programs. Single-cell RNA sequencing with paired BCR profiling could offer insights into numerous physiological and pathological processes. However, unlike the plethora of single-cell RNA analysis pipelines, computational tools that utilize single-cell BCR sequences for further analyses are not yet well developed. Here we report Ibex, which vectorizes the amino acid sequence of the complementarity-determining region 3 (cdr3) of the immunoglobulin heavy and light chains, allowing for unbiased dimensional reduction of B cells using their BCR repertoire. Ibex is implemented as an R package with integration into both the Seurat and Single-Cell Experiment framework, enabling the incorporation of this new analytic tool into many single-cell sequencing analytic workflows and multimodal experiments.