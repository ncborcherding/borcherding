# scRepertoire

## Introduction

Single-cell sequencing is an emerging technology in the field of
immunology and oncology that allows researchers to couple RNA
quantification and other modalities, like immune cell receptor profiling
at the level of an individual cell. Unlike the transcriptomic field,
there is a lack of options for software that allow for single-cell
immune receptor profiling. Enabling users to easily combine RNA and
immune profiling, the scRepertoire framework supports 10x, AIRR, BD,
MiXCR, TRUST4, and WAT3R single-cell clonal formats and interaction with
popular R-based single-cell data pipelines.

## Quick Start

``` r
library(scRepertoire)

# Load and combine contigs into clones
combined.TCR <- combineTCR(contig_list,
                           samples = c("P17B", "P17L", "P18B", "P18L",
                                       "P19B", "P19L", "P20B", "P20L"))

# Visualize clonal frequency
clonalQuant(combined.TCR, clone.call = "strict", chain = "both")

# Attach clonal data to a single-cell object
scRep_example <- combineExpression(combined.TCR, scRep_example)
```

For a full walkthrough, start with
[Installation](https://www.borch.dev/uploads/scRepertoire/articles/Installation.md),
then [Loading
Data](https://www.borch.dev/uploads/scRepertoire/articles/Loading.md)
and [Combining
Contigs](https://www.borch.dev/uploads/scRepertoire/articles/Combining_Contigs.md).

## Installation

#### Development Branch

[immApex](https://github.com/BorchLab/immApex) is a required dependency.
If not using Bioconductor, install both:

``` r
remotes::install_github(c("BorchLab/immApex", "BorchLab/scRepertoire@devel"))
```

#### Bioconductor

The current stable version is available on
[Bioconductor](https://www.bioconductor.org/packages/release/bioc/html/scRepertoire.html):

``` r
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("scRepertoire")
```

#### Legacy Version 1

``` r
devtools::install_github("BorchLab/scRepertoire@v1")
```

## Getting Data

GitHub limits the size of individual files. To access the full Seurat
object paired with scRepertoire, download the .rda from
[Zenodo](https://zenodo.org/records/18187313). A smaller version of the
cohort is built into scRepertoire as **scRep_example**.

## Deep Learning Extensions

scRepertoire is compatible with [Trex](https://github.com/BorchLab/Trex)
for deep-learning-based autoencoding of T cell receptors and
[Ibex](https://github.com/BorchLab/Ibex) for B cell receptors. For
building custom deep-learning models with immune receptors, see
[immApex](https://github.com/BorchLab/immApex).

## Citation

- **Version 2**: Yang, Q, & Safina, K., Nguyen, K., Tuong, Z.K., &
  Borcherding, N. (2025). “scRepertoire 2: Enhanced and efficient
  toolkit for single-cell immune profiling.” *PLoS Computational
  Biology* <https://doi.org/10.1371/journal.pcbi.1012760>
- **Version 1**: Borcherding, Nicholas, Nicholas L. Bormann, and Gloria
  Kraus. “scRepertoire: An R-based toolkit for single-cell immune
  receptor analysis.” *F1000Research*
  <https://doi.org/10.12688/f1000research.22139.2>

## Bug Reports / Feature Requests

- Submit issues on
  [GitHub](https://github.com/BorchLab/scRepertoire/issues). If
  possible, include a [reproducible
  example](https://reprex.tidyverse.org/) using the built-in
  **scRep_example** and **contig_list** data.
- [Pull requests](https://github.com/BorchLab/scRepertoire/pulls) are
  welcome. Please target the “devel” branch.
