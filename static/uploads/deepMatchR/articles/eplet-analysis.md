# Eplet Analysis

## Introduction

Eplets are short amino acid sequences that form antibody-binding
epitopes on HLA molecules. They are key determinants of HLA
immunogenicity and play a crucial role in: - Predicting antibody
development risk in transplantation - Understanding patterns of HLA
sensitization - Guiding donor selection strategies

This article covers eplet-based analysis in **deepMatchR**.

## Loading the Package

``` r
library(deepMatchR)
library(dplyr)
```

## Understanding Eplets

### What are Eplets?

Eplets are small configurations of polymorphic amino acid residues on
the molecular surface of HLA molecules. They were originally defined by
the HLAMatchmaker algorithm and are catalogued in the [Eplet
Registry](http://www.epregistry.com.br/).

Key concepts:

- **Evidence Level:** Indicates how well-characterized the eplet is
  - A1/A2: Antibody-verified eplets
  - B: Theoretically predicted
  - D: Deprecated
- **Exposition:** Surface accessibility
  - High: Clearly exposed on molecular surface
  - Intermediate/Low: Less accessible
- **Reactivity:** Whether antibody binding has been confirmed

## Quantifying Eplet Mismatches

### Basic Comparison

The
[`quantifyEpletMismatch()`](https://www.borch.dev/uploads/deepMatchR/reference/quantifyEpletMismatch.md)
function calculates non-shared eplets between two alleles:

``` r
# Basic eplet comparison (A1/A2 evidence level by default)
quantifyEpletMismatch("A*01:01", "A*02:01")
#> [1] 13
```

### Filtering by Evidence Level

``` r
# Only antibody-verified eplets (A1)
quantifyEpletMismatch("A*01:01", "A*02:01", evidence_level = "A1")
#> [1] 8

# All evidence levels including theoretical
quantifyEpletMismatch("A*01:01", "A*02:01", evidence_level = NULL)
#> [1] 59
```

### Filtering by Exposition

``` r
# High-exposition eplets only
quantifyEpletMismatch("B*07:02", "B*44:02", exposition_filter = "High")
#> [1] 6
```

### Filtering by Reactivity

``` r
# Confirmed reactive eplets only
quantifyEpletMismatch("C*07:01", "C*06:02",
                      evidence_level = NULL,
                      reactivity_filter = "Confirmed")
#> [1] 9
```

## Calculating Eplet Load

For donor-recipient matching, use
[`calculateEpletLoad()`](https://www.borch.dev/uploads/deepMatchR/reference/calculateEpletLoad.md)
to compute total donor-specific eplets across all loci.

### Creating Genotypes

``` r
recipient <- data.frame(
  A_1 = "A*01:01", A_2 = "A*02:01",
  B_1 = "B*07:02", B_2 = "B*08:01",
  DQB1_1 = "DQB1*02:02", DQB1_2 = "DQB1*03:01"
)

donor <- data.frame(
  A_1 = "A*03:01", A_2 = "A*24:02",
  B_1 = "B*44:02", B_2 = "B*51:01",
  DQB1_1 = "DQB1*06:02", DQB1_2 = "DQB1*03:01"
)

rgeno <- hlaGeno(recipient)
dgeno <- hlaGeno(donor)
```

### Total Eplet Load

``` r
calculateEpletLoad(rgeno, dgeno)
#> [1] 18
```

### Per-Locus Summary

``` r
per_locus <- calculateEpletLoad(rgeno, dgeno, return = "per_locus")
per_locus
#>   locus eplet_load
#> 1     A          4
#> 2     B          6
#> 3  DQB1          8
```

### Pairwise Allele Matrix

``` r
mB <- calculateEpletLoad(
  rgeno, dgeno,
  return = "pairwise",
  pairwise_locus = "B"
)
mB
#>          donor
#> recipient B*44:02 B*51:01
#>   B*07:02       5       4
#>   B*08:01       4       3
```

### Applying Filters

``` r
# High-exposition eplets only
calculateEpletLoad(rgeno, dgeno, exposition_filter = "High")
#> [1] 14

# Antibody-confirmed eplets only
calculateEpletLoad(rgeno, dgeno, reactivity_filter = "Confirmed")
#> [1] 18

# All evidence levels (no filter)
calculateEpletLoad(rgeno, dgeno, evidence_level = NULL)
#> [1] 77
```

## Clinical Interpretation

### Eplet Load and DSA Risk

Higher eplet mismatch loads are generally associated with increased risk
of donor-specific antibody (DSA) development. However, interpretation
should consider:

1.  **Evidence quality:** A1/A2 eplets have stronger clinical validation
2.  **Surface exposition:** High-exposition eplets are more accessible
    to antibodies
3.  **Previous sensitization:** Patient’s existing antibody profile
4.  **Immunosuppression:** Treatment protocol intensity

### Recommended Thresholds

While specific thresholds vary by center and organ type, general
guidelines suggest:

| Eplet Load | Risk Level |
|------------|------------|
| 0-10       | Low        |
| 11-20      | Moderate   |
| \>20       | High       |

> **Note:** These are general guidelines. Always consult your
> institution’s protocols.

## Function Reference

### `quantifyEpletMismatch()`

| Argument             | Default        | Description                       |
|----------------------|----------------|-----------------------------------|
| `allele1`, `allele2` | –              | Two HLA alleles to compare        |
| `evidence_level`     | `c("A1","A2")` | Filter by evidence level          |
| `exposition_filter`  | `NULL`         | Filter by surface exposition      |
| `reactivity_filter`  | `NULL`         | Filter by reactivity confirmation |

### `calculateEpletLoad()`

| Argument | Default | Description |
|----|----|----|
| `recipient_geno`, `donor_geno` | – | HLA genotypes from [`hlaGeno()`](https://www.borch.dev/uploads/deepMatchR/reference/hlaGeno.md) |
| `loci` | `NULL` | Restrict to specific loci |
| `evidence_level` | `c("A1","A2")` | Filter by evidence level |
| `exposition_filter` | `NULL` | Filter by surface exposition |
| `reactivity_filter` | `NULL` | Filter by reactivity confirmation |
| `return` | `"total"` | `"total"`, `"per_locus"`, or `"pairwise"` |
| `pairwise_locus` | `NULL` | Locus for pairwise matrix |

## Session Information

``` r
sessionInfo()
#> R version 4.5.0 (2025-04-11)
#> Platform: aarch64-apple-darwin20
#> Running under: macOS Sonoma 14.0
#> 
#> Matrix products: default
#> BLAS:   /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/lib/libRblas.0.dylib 
#> LAPACK: /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/lib/libRlapack.dylib;  LAPACK version 3.12.1
#> 
#> locale:
#> [1] en_US.UTF-8/en_US.UTF-8/en_US.UTF-8/C/en_US.UTF-8/en_US.UTF-8
#> 
#> time zone: America/Chicago
#> tzcode source: internal
#> 
#> attached base packages:
#> [1] stats     graphics  grDevices utils     datasets  methods   base     
#> 
#> other attached packages:
#> [1] dplyr_1.1.4       deepMatchR_0.99.0 BiocStyle_2.36.0 
#> 
#> loaded via a namespace (and not attached):
#>  [1] gtable_0.3.6            dir.expiry_1.16.0       xfun_0.55              
#>  [4] bslib_0.9.0             ggplot2_4.0.1           htmlwidgets_1.6.4      
#>  [7] lattice_0.22-7          vctrs_0.6.5             tools_4.5.0            
#> [10] generics_0.1.4          stats4_4.5.0            parallel_4.5.0         
#> [13] tibble_3.3.0            pkgconfig_2.0.3         Matrix_1.7-4           
#> [16] data.table_1.18.0       RColorBrewer_1.1-3      S7_0.2.1               
#> [19] desc_1.4.3              S4Vectors_0.46.0        readxl_1.4.5           
#> [22] lifecycle_1.0.4         GenomeInfoDbData_1.2.14 compiler_4.5.0         
#> [25] farver_2.1.2            textshaping_1.0.4       Biostrings_2.76.0      
#> [28] GenomeInfoDb_1.44.3     htmltools_0.5.9         sass_0.4.10            
#> [31] yaml_2.3.12             pillar_1.11.1           pkgdown_2.2.0          
#> [34] crayon_1.5.3            jquerylib_0.1.4         cachem_1.1.0           
#> [37] basilisk_1.20.0         tidyselect_1.2.1        rvest_1.0.5            
#> [40] digest_0.6.39           bookdown_0.46           fastmap_1.2.0          
#> [43] grid_4.5.0              cli_3.6.5               magrittr_2.0.4         
#> [46] patchwork_1.3.2         filelock_1.0.3          scales_1.4.0           
#> [49] UCSC.utils_1.4.0        pwalign_1.4.0           rmarkdown_2.30         
#> [52] XVector_0.48.0          httr_1.4.7              otel_0.2.0             
#> [55] reticulate_1.44.1       cellranger_1.1.0        ragg_1.5.0             
#> [58] png_0.1-8               memoise_2.0.1           evaluate_1.0.5         
#> [61] knitr_1.51              IRanges_2.42.0          basilisk.utils_1.20.0  
#> [64] immReferent_0.99.0      rlang_1.1.6             Rcpp_1.1.0             
#> [67] glue_1.8.0              BiocManager_1.30.27     xml2_1.5.1             
#> [70] BiocGenerics_0.54.1     rstudioapi_0.17.1       jsonlite_2.0.0         
#> [73] R6_2.6.1                systemfonts_1.3.1       fs_1.6.6
```
