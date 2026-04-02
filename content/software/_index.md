---
title: Software & Tools
summary: Open-source packages for immune repertoire analysis, single-cell genomics, and deep learning
type: page
reading_time: false
share: false
profile: false
commentable: false

design:
  columns: '1'
---

I develop and maintain open-source software for computational immunology, single-cell analysis, and adaptive immune receptor repertoire research. All packages are freely available on GitHub under the [BorchLab](https://github.com/BorchLab) organization.

---

## Repertoire Analysis

### [scRepertoire](https://github.com/BorchLab/scRepertoire)

A comprehensive toolkit for single-cell immune receptor profiling. scRepertoire enables researchers to combine T-cell receptor (TCR) and B-cell receptor (BCR) data with single-cell RNA sequencing, providing functions for clonal quantification, diversity analysis, repertoire overlap, and visualization. Integrates directly with Seurat and SingleCellExperiment.

**Role:** Author &middot; **First released:** 2020 &middot; [Documentation](../uploads/scRepertoire/) &middot; [Publication](https://doi.org/10.12688/f1000research.22139.2)

### [immReferent](https://github.com/BorchLab/immReferent)

A clean R interface to the IMGT and OGRDB reference databases for immune receptor gene segments and HLA allele sequences. Standardizes programmatic access to germline V, D, and J gene sequences for TCR and BCR loci, as well as HLA typing references for immunogenomics and transplant immunogenetics workflows.

**Role:** Author &middot; **First released:** 2025

### [dandelionR](https://github.com/tuonglab/dandelionR)

An R implementation of the dandelion framework for single-cell immune repertoire trajectory analysis. Traces developmental and differentiation trajectories of T and B cells using receptor sequences as natural barcodes, integrating receptor information with transcriptomic data.

**Role:** Co-author &middot; **First released:** 2025

---

## Deep Learning

### [Trex](https://github.com/BorchLab/Trex)

Uses deep learning autoencoders to vectorize TCR CDR3 amino acid sequences, enabling unbiased dimensional reduction of T cells based on their receptor repertoire. Integrates with Seurat and SingleCellExperiment for multimodal single-cell analysis.

**Role:** Author &middot; **First released:** 2023

### [Ibex](https://github.com/BorchLab/Ibex)

The BCR counterpart to Trex. Vectorizes immunoglobulin heavy and light chain CDR3 sequences using autoencoders, enabling repertoire-based dimensional reduction and clustering of B cells within single-cell workflows.

**Role:** Author &middot; **First released:** 2023 &middot; [Publication](https://doi.org/10.1101/2022.11.09.515787)

### [immApex](https://github.com/BorchLab/immApex)

A unified interface for applying machine learning and deep learning to adaptive immune receptor sequences. Includes tools for featurizing TCR and BCR sequences with multiple encoding schemes, training antigen specificity models, and benchmarking performance.

**Role:** Author &middot; **First released:** 2024

### [bHIVE](https://github.com/BorchLab/bHIVE)

B-cell Hybrid Immune Virtual Evolution model. An artificial immune system simulator that models BCR diversification, affinity maturation, and clonal selection. Generates synthetic BCR repertoires for benchmarking analysis tools and testing hypotheses about immune dynamics.

**Role:** Author &middot; **First released:** 2025

---

## Enrichment & Pathway Analysis

### [escape](https://github.com/BorchLab/escape)

Easy single-cell analysis platform for enrichment. Performs gene set enrichment analysis (GSEA) at single-cell resolution, enabling characterization of metabolic, signaling, and immune pathways on individual cells. Integrates directly with Seurat and SingleCellExperiment objects.

**Role:** Author &middot; **First released:** 2020

---

## Specialized Tools

### [deepMatchR](https://github.com/BorchLab/deepMatchR)

Tools for antibody matching and analysis. [Documentation](../uploads/deepMatchR/)

**Role:** Author

### [ClamBake](https://github.com/BorchLab)

Metabolic estimation software for CLAM (Comprehensive Lab Animal Monitoring) cages, licensed to Columbus Instruments. Provides automated analysis pipelines for indirect calorimetry data from animal metabolic studies.

**Role:** Author &middot; **First released:** 2023

---

## Data Resources

### [uTILity](https://github.com/ncborcherding/utility)

A curated collection of publicly available tumor-infiltrating lymphocyte (TIL) single-cell experiments with paired TCR sequencing. Includes processed Seurat objects spanning 28 cohorts across multiple cancer types with over 1.8 million T cells.

**Role:** Author &middot; [Browse cohorts](https://github.com/ncborcherding/utility#cohort-information)
