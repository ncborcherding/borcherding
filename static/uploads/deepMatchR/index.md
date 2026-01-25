# deepMatchR

Tools for HLA Testing and Matching

## Introduction

![](reference/figures/logo.png)

There are currently several computational approaches to quantifying the
risk of the development of donor-specific antibodies during organ
transplantation. These include
[HLAmatchmaker](https://www.borch.dev/uploads/deepMatchR/http.www.epitopes.net/)
for eplet quantification and [PIRCHE-II](https://www.pirche.com/) for
CD4+ T cell epitope prediction, which have demonstrated predictive
ability across the literature. Newer deep learning methods for structure
predictions, eplet/epitope immunogenicity estimates, and classification
can be leveraged to produce a clinical tool for patients. **deepMatchR**
aims to be a centralized repository for tools and models to help in
assisting HLA matching.

## Core Functions

`deepMatchR` provides a suite of functions for HLA analysis, from basic
sequence comparison to complex visualization and deconvolution. Here is
an overview of the main functions:

### Sequence & Eplet Analysis

- **`getAlleleSequence(allele_name)`**: Retrieves the full amino acid
  sequence for a given HLA allele from the IMGT/HLA database.

  ``` r
  # Note: Requires internet connection
  getAlleleSequence("A*01:01")
  ```

- **`quantifyMismatch(seq1, seq2)`**: Calculates the total number of
  amino acid mismatches between two sequences.

  ``` r
  seq1 <- "YFAMYGEKVAHTHVDTLYVRYHY"
  seq2 <- "YFDMYGEKVAHTHVDTLYVRFHY"
  quantifyMismatch(seq1, seq2)
  ```

- **`quantifyEpletMismatch(allele1, allele2)`**: Calculates the number
  of mismatched eplets between two HLA alleles based on the internal
  eplet registry.

  ``` r
  quantifyEpletMismatch("A*01:01", "A*02:01")
  ```

### Antibody Analysis & Visualization

- **`plotAntibodies(result_file, type)`**: Visualizes SAB or PRA results
  as a bar plot, with an optional table of antigen specificities.

  ``` r
  data(deepMatchR_example)
  plotAntibodies(deepMatchR_example[[1]], type = "SAB")
  ```

- **`plotEplets(result_file, plot_type)`**: Visualizes eplet-level
  reactivity from SAB results using a treemap, bar plot, or AUC plot.

  ``` r
  data(deepMatchR_example)
  plotEplets(deepMatchR_example[[1]], plot_type = "treemap")
  ```

- **`calculateAUC(...)` / `epletAUC(...)`**: Calculates the Area Under
  the Curve (AUC) for feature reactivity (like eplets or CREGs) across a
  range of MFI cutoffs.

  ``` r
  data(deepMatchR_example)
  epletAUC(deepMatchR_example[[1]], plot_results = TRUE)
  ```

## System requirements

deepMatchR has been tested on R versions \>= 4.0. Please consult the
DESCRIPTION file for more details on required R packages. deepMatchR has
been tested on OS X and Windows platforms.

## Installation

To run deepMatchR, open R and install deepMatchR from github:

``` r
devtools::install_github("BorchLab/deepMatchR")
```

------------------------------------------------------------------------

## Bug Reports/New Features

#### If you run into any issues or bugs please submit a [GitHub issue](https://github.com/ncborcherding/deepMatchR/issues) with details of the issue.

- If possible please include a [reproducible
  example](https://reprex.tidyverse.org/). Alternatively, an example
  with the internal **deepMatchR_example** would be extremely helpful.

#### Any requests for new features or enhancements can also be submitted as [GitHub issues](https://github.com/ncborcherding/deepMatchR/issues).

#### [Pull Requests](https://github.com/ncborcherding/deepMatchR/pulls) are welcome for bug fixes, new features, or enhancements.
