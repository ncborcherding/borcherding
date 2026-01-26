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

### Peptide Binding Prediction

- **`predictMHCnuggets(peptides, allele)`**: Predicts peptide-MHC
  binding affinity using
  [MHCnuggets](https://github.com/KarchinLab/mhcnuggets), a deep
  learning model for MHC binding prediction.

  ``` r
  peptides <- c("SIINFEKL", "LLFGYPVYV", "GILGFVFTL")
  predictMHCnuggets(peptides, allele = "A*02:01", mhc_class = "I")
  ```

- **`calculatePeptideBindingLoad(recipient, donor)`**: Estimates
  transplant risk by predicting peptide-HLA binding between recipient
  HLA molecules and donor-mismatched peptides. Supports multiple
  backends:

  - `pwm`: Built-in position weight matrix (no external dependencies)
  - `mhcnuggets`: Deep learning via
    [MHCnuggets](https://github.com/KarchinLab/mhcnuggets)
  - `netmhcpan`: External tool via [NetMHCpan
    4.1](https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/)

  ``` r
  recipient <- hlaGeno(data.frame(A_1 = "A*02:01", A_2 = "A*03:01"))
  donor <- hlaGeno(data.frame(A_1 = "A*01:01", A_2 = "A*24:02"))
  calculatePeptideBindingLoad(recipient, donor, return = "summary")
  ```

## System requirements

deepMatchR has been tested on R versions \>= 4.5. Please consult the
DESCRIPTION file for more details on required R packages. deepMatchR has
been tested on OS X and Windows platforms.

### Setting up NetMHCpan (Optional)

To use the `netmhcpan` backend for peptide binding prediction, you need
to install NetMHCpan 4.1 separately:

1.  **Request a license**: Go to
    <https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/> and
    request an academic license (free for academic users).

2.  **Download and extract**: After receiving the download link via
    email, extract the archive:

    ``` bash
    tar -xzvf netMHCpan-4.1.Linux.tar.gz
    cd netMHCpan-4.1
    ```

3.  **Configure the installation**: Edit the `netMHCpan` script to set
    the correct paths:

    ``` bash
    # Open the script and modify these lines:
    setenv NMHOME /path/to/netMHCpan-4.1
    setenv TMPDIR /tmp
    ```

4.  **Download data files**: Follow the instructions in the
    `netMHCpan-4.1.readme` file to download required data files and
    place them in the `data` directory.

5.  **Test the installation**:

    ``` bash
    ./netMHCpan -p test.pep -a HLA-A02:01
    ```

6.  **Use in deepMatchR**: Provide the path to the executable:

    ``` r
    calculatePeptideBindingLoad(
      recipient = rgeno,
      donor = dgeno,
      backend = "netmhcpan",
      backend_path = "/path/to/netMHCpan-4.1/netMHCpan"
    )
    ```

> **Note:** NetMHCpan is available for Linux and macOS. Windows users
> should use WSL (Windows Subsystem for Linux) or the `pwm`/`mhcnuggets`
> backends instead.

## Installation

To run deepMatchR, open R and install deepMatchR from github:

``` r
devtools::install_github("BorchLab/deepMatchR")
```

------------------------------------------------------------------------

## Bug Reports/New Features

#### If you run into any issues or bugs please submit a [GitHub issue](https://github.com/BorchLab/deepMatchR/issues) with details of the issue.

- If possible please include a [reproducible
  example](https://reprex.tidyverse.org/). Alternatively, an example
  with the internal **deepMatchR_example** would be extremely helpful.

#### Any requests for new features or enhancements can also be submitted as [GitHub issues](https://github.com/BorchLab/deepMatchR/issues).

#### [Pull Requests](https://github.com/BorchLab/deepMatchR/pulls) are welcome for bug fixes, new features, or enhancements.
