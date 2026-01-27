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

| Argument                       | Default        | Description                                                                                     |
|--------------------------------|----------------|-------------------------------------------------------------------------------------------------|
| `recipient_geno`, `donor_geno` | –              | HLA genotypes from [`hlaGeno()`](https://www.borch.dev/uploads/deepMatchR/reference/hlaGeno.md) |
| `loci`                         | `NULL`         | Restrict to specific loci                                                                       |
| `evidence_level`               | `c("A1","A2")` | Filter by evidence level                                                                        |
| `exposition_filter`            | `NULL`         | Filter by surface exposition                                                                    |
| `reactivity_filter`            | `NULL`         | Filter by reactivity confirmation                                                               |
| `return`                       | `"total"`      | `"total"`, `"per_locus"`, or `"pairwise"`                                                       |
| `pairwise_locus`               | `NULL`         | Locus for pairwise matrix                                                                       |

## Session Information

``` r
sessionInfo()
#> R version 4.5.2 (2025-10-31)
#> Platform: x86_64-pc-linux-gnu
#> Running under: Ubuntu 24.04.3 LTS
#> 
#> Matrix products: default
#> BLAS:   /usr/lib/x86_64-linux-gnu/openblas-pthread/libblas.so.3 
#> LAPACK: /usr/lib/x86_64-linux-gnu/openblas-pthread/libopenblasp-r0.3.26.so;  LAPACK version 3.12.0
#> 
#> locale:
#>  [1] LC_CTYPE=C.UTF-8       LC_NUMERIC=C           LC_TIME=C.UTF-8       
#>  [4] LC_COLLATE=C.UTF-8     LC_MONETARY=C.UTF-8    LC_MESSAGES=C.UTF-8   
#>  [7] LC_PAPER=C.UTF-8       LC_NAME=C              LC_ADDRESS=C          
#> [10] LC_TELEPHONE=C         LC_MEASUREMENT=C.UTF-8 LC_IDENTIFICATION=C   
#> 
#> time zone: UTC
#> tzcode source: system (glibc)
#> 
#> attached base packages:
#> [1] stats     graphics  grDevices utils     datasets  methods   base     
#> 
#> other attached packages:
#> [1] dplyr_1.1.4       deepMatchR_0.99.0 BiocStyle_2.38.0 
#> 
#> loaded via a namespace (and not attached):
#>  [1] sass_0.4.10         generics_0.1.4      xml2_1.5.2         
#>  [4] lattice_0.22-7      immReferent_0.99.6  digest_0.6.39      
#>  [7] magrittr_2.0.4      evaluate_1.0.5      grid_4.5.2         
#> [10] RColorBrewer_1.1-3  bookdown_0.46       fastmap_1.2.0      
#> [13] cellranger_1.1.0    jsonlite_2.0.0      Matrix_1.7-4       
#> [16] BiocManager_1.30.27 rvest_1.0.5         httr_1.4.7         
#> [19] scales_1.4.0        Biostrings_2.78.0   textshaping_1.0.4  
#> [22] jquerylib_0.1.4     cli_3.6.5           rlang_1.1.7        
#> [25] crayon_1.5.3        XVector_0.50.0      cachem_1.1.0       
#> [28] yaml_2.3.12         tools_4.5.2         dir.expiry_1.18.0  
#> [31] parallel_4.5.2      memoise_2.0.1       ggplot2_4.0.1      
#> [34] filelock_1.0.3      basilisk_1.22.0     BiocGenerics_0.56.0
#> [37] reticulate_1.44.1   vctrs_0.7.1         R6_2.6.1           
#> [40] png_0.1-8           stats4_4.5.2        lifecycle_1.0.5    
#> [43] pwalign_1.6.0       Seqinfo_1.0.0       IRanges_2.44.0     
#> [46] S4Vectors_0.48.0    fs_1.6.6            ragg_1.5.0         
#> [49] pkgconfig_2.0.3     desc_1.4.3          pkgdown_2.2.0      
#> [52] pillar_1.11.1       bslib_0.10.0        gtable_0.3.6       
#> [55] data.table_1.18.0   glue_1.8.0          Rcpp_1.1.1         
#> [58] systemfonts_1.3.1   xfun_0.56           tibble_3.3.1       
#> [61] tidyselect_1.2.1    knitr_1.51          farver_2.1.2       
#> [64] patchwork_1.3.2     htmltools_0.5.9     rmarkdown_2.30     
#> [67] compiler_4.5.2      S7_0.2.1            readxl_1.4.5
```
