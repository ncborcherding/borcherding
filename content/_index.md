---
title: "Nick Borcherding"
description: "Physician-scientist working on computational immunology, clinical pathology, and transplant immunogenetics at Washington University School of Medicine in St. Louis."

# -- Hero -------------------------------------------------------------------
# Identity (name, role, org) is read from site params to avoid duplication.
# Only the one-line research statement lives here.
research_statement: "Integrating systems immunology, single-cell sequencing, and computational frameworks to understand how the adaptive immune system encodes and recalls disease."

# -- 01 About ---------------------------------------------------------------
about:
  lead: "I am a physician-scientist whose work bridges computational immunology, clinical pathology, and transplant immunogenetics."
  body: >
    My clinical practice centers on human leukocyte antigen testing for transplantation,
    autoimmunity, and cancer immunotherapy. My research asks how the adaptive immune
    system records disease experience and recalls it later. I read that record using
    innate and adaptive cellular barcodes, including mitochondrial genomes and immune
    receptor repertoires, to trace clonal relationships across tissues and disease states.
  interests:
    - Tumor Immunology
    - Immunometabolism
    - Single-Cell Immune Profiling
    - Adaptive Immune Receptor Repertoire Analyses
    - Open Data Science

# -- 02 Research ------------------------------------------------------------
research_areas:
  - title: "Adaptive immune receptor repertoires"
    body: >
      T and B cell receptors are natural barcodes. I build methods that read them at
      single-cell scale to track clonal lineages, measure repertoire diversity, and link
      receptor sequence to cell state across tumors, transplants, and autoimmune disease.
  - title: "Single-cell systems immunology"
    body: >
      I pair single-cell sequencing with systems-level models to map immune diversity and
      connect transcriptional programs to function. The goal is a quantitative picture of
      how immune populations shift across disease and therapy.
  - title: "Computational frameworks and machine learning"
    body: >
      I develop open-source software and deep learning models that turn raw immune
      sequencing into interpretable structure, from autoencoders that vectorize receptor
      sequences to enrichment methods that score pathways at single-cell resolution.
  - title: "Clinical immunogenetics"
    body: >
      In the HLA laboratory I work on histocompatibility testing for transplant,
      autoimmunity, and immunotherapy, and on bringing repertoire and network analyses
      to bear on real clinical outcomes such as allograft survival.

# -- 03 Software ------------------------------------------------------------
# Real BorchLab packages, condensed to one line each.
software:
  - name: "scRepertoire"
    url: "https://github.com/BorchLab/scRepertoire"
    desc: "Single-cell immune receptor profiling that pairs TCR and BCR data with scRNA-seq for clonal quantification, diversity, and repertoire overlap."
    role: "Author"
    docs: "https://www.borch.dev/uploads/scRepertoire/"
    pub: "https://doi.org/10.12688/f1000research.22139.2"
  - name: "immReferent"
    url: "https://github.com/BorchLab/immReferent"
    desc: "A clean R interface to IMGT and OGRDB germline references for TCR, BCR, and HLA immunogenomics workflows."
    role: "Author"
  - name: "immLynx"
    url: "https://github.com/BorchLab/immLynx"
    desc: "A unified R interface that runs Python TCR pipelines such as tcrdist3, OLGA, clusTCR, and ESM-2 embeddings inside scRepertoire workflows."
    role: "Author"
  - name: "immGLIPH"
    url: "https://github.com/BorchLab/immGLIPH"
    desc: "An R implementation of GLIPH and GLIPH2 that groups TCRs by CDR3 similarity into specificity clusters likely to share peptide-HLA targets."
    role: "Author"
  - name: "immApex"
    url: "https://github.com/BorchLab/immApex"
    desc: "A unified interface for machine learning on adaptive immune receptor sequences, from featurization to model benchmarking."
    role: "Author"
    pub: "https://www.biorxiv.org/content/10.64898/2026.05.04.722749v1"
  - name: "Trex"
    url: "https://github.com/BorchLab/Trex"
    desc: "Deep learning autoencoders that vectorize TCR CDR3 sequences for receptor-based dimensional reduction."
    role: "Author"
    pub: "https://www.nature.com/articles/s41590-024-01888-9"
  - name: "Ibex"
    url: "https://github.com/BorchLab/Ibex"
    desc: "The BCR counterpart to Trex that vectorizes immunoglobulin CDR3 sequences for repertoire-based clustering."
    role: "Author"
    pub: "https://doi.org/10.1101/2022.11.09.515787"
  - name: "escape"
    url: "https://github.com/BorchLab/escape"
    desc: "Single-cell gene set enrichment analysis integrated with Seurat and SingleCellExperiment objects."
    role: "Author"
    pub: "https://www.nature.com/articles/s42003-020-01625-6"
  - name: "bHIVE"
    url: "https://github.com/BorchLab/bHIVE"
    desc: "B-cell Hybrid Immune Variant Engine, a modular artificial immune system for clustering and classification inspired by somatic hypermutation and germinal-center selection."
    role: "Author"
    docs: "https://www.borch.dev/uploads/bhive/"

# -- 05 Contact -------------------------------------------------------------
contact:
  email: "ncborch@gmail.com"
  location: "St. Louis, MO"
  org: "Washington University School of Medicine in St. Louis"
  org_url: "https://pathology.wustl.edu/"

# -- Social links (single source for hero + contact rows) -------------------
social:
  - name: "Google Scholar"
    url: "https://scholar.google.com/citations?user=_n4TRuIAAAAJ"
  - name: "ORCID"
    url: "https://orcid.org/0000-0003-1427-6342"
  - name: "GitHub"
    url: "https://github.com/BorchLab"
  - name: "LinkedIn"
    url: "https://www.linkedin.com/in/thehumanborch/"
---

This file holds the structured copy for the editorial landing page. The layout in
`layouts/index.html` renders the hero and the five numbered sections from these
front-matter fields. Visual styling lands in a later phase.
