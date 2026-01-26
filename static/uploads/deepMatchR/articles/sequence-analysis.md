# Sequence & Mismatch Analysis

## Introduction

This article covers sequence-level HLA analysis in **deepMatchR**,
including:

- Retrieving allele sequences from IMGT/HLA
- Quantifying amino acid mismatches between sequences
- Calculating mismatch load between donor-recipient pairs

These tools provide the foundation for understanding immunogenicity at
the molecular level.

## Loading the Package

``` r
library(deepMatchR)
library(dplyr)
```

## Retrieving HLA Sequences

### Basic Usage

The
[`getAlleleSequence()`](https://www.borch.dev/uploads/deepMatchR/reference/getAlleleSequence.md)
function retrieves protein sequences from the IMGT/HLA database.

``` r
# Get the amino acid sequence for A*01:01
a0101_seq <- getAlleleSequence("A*01:01")
```

``` r
# View first 60 amino acids
substr(a0101_seq, 1, 60)
#> [1] "MAVMAPRTLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRF"

# Full sequence length
nchar(a0101_seq)
#> [1] 365
```

### Batch Retrieval

For multiple alleles, use
[`batchGetSequences()`](https://www.borch.dev/uploads/deepMatchR/reference/batchGetSequences.md)
for efficient parallel retrieval:

``` r
alleles <- c("A*01:01", "A*02:01", "B*07:02")
sequences <- batchGetSequences(alleles)
```

``` r
# View sequence lengths
sapply(sequences, nchar)
#> A*01:01 A*02:01 B*07:02 
#>     365     365     362
```

## Quantifying Amino Acid Mismatches

### Basic Mismatch Counting

The
[`quantifyMismatch()`](https://www.borch.dev/uploads/deepMatchR/reference/quantifyMismatch.md)
function compares two protein sequences and counts differences:

``` r
seq1 <- "YFAMYGEKVAHTHVDTLYVRYHY"
seq2 <- "YFDMYGEKVAHTHVDTLYVRFHY"

# Count all mismatches
quantifyMismatch(seq1, seq2)
#> [1] 2
```

### Biophysical Property Filters

You can filter mismatches by biophysical properties to focus on
functionally significant changes:

#### Charge Classification

- **Positive:** K, R, H
- **Negative:** D, E
- **Neutral:** All others

#### Polarity Classification

- **Nonpolar:** A, V, L, I, P, M, F, W, G
- **Polar:** S, T, N, Q, Y, C, H, K, R, D, E

``` r
# Only charge-changing mismatches
quantifyMismatch(seq1, seq2, filter_charge = TRUE)
#> [1] 1

# Only polarity-changing mismatches
quantifyMismatch(seq1, seq2, filter_polarity = TRUE)
#> [1] 2

# Both charge AND polarity changing
quantifyMismatch(seq1, seq2, filter_charge = TRUE, filter_polarity = TRUE)
#> [1] 1
```

### Detailed Position Analysis

Get position-by-position breakdown:

``` r
details <- quantifyMismatch(seq1, seq2, return = "detail")
head(details)
#>   alignment_position ref alt is_gap_ref is_gap_alt is_mismatch charge_ref
#> 1                  1   Y   Y      FALSE      FALSE       FALSE        neu
#> 2                  2   F   F      FALSE      FALSE       FALSE        neu
#> 3                  3   A   D      FALSE      FALSE        TRUE        neu
#> 4                  4   M   M      FALSE      FALSE       FALSE        neu
#> 5                  5   Y   Y      FALSE      FALSE       FALSE        neu
#> 6                  6   G   G      FALSE      FALSE       FALSE        neu
#>   charge_alt charge_change polarity_ref polarity_alt polarity_change counted
#> 1        neu         FALSE        polar        polar           FALSE   FALSE
#> 2        neu         FALSE     nonpolar     nonpolar           FALSE   FALSE
#> 3        neg          TRUE     nonpolar        polar            TRUE    TRUE
#> 4        neu         FALSE     nonpolar     nonpolar           FALSE   FALSE
#> 5        neu         FALSE        polar        polar           FALSE   FALSE
#> 6        neu         FALSE     nonpolar     nonpolar           FALSE   FALSE
```

The detail output includes:

| Column            | Description                          |
|-------------------|--------------------------------------|
| `position`        | Position in the sequence             |
| `aa1` / `aa2`     | Amino acid in each sequence          |
| `is_mismatch`     | Whether amino acids differ           |
| `charge_change`   | Whether charge class changed         |
| `polarity_change` | Whether polarity changed             |
| `counted`         | Whether position counts toward total |

### Handling Unknown Residues

The `na_action` parameter controls how unknown residues (X, -, etc.) are
handled:

``` r
seq_with_unknown <- "YFAMYGEKVAHTHVDTLYVRXHY"

# Exclude unknown positions (default)
quantifyMismatch(seq1, seq_with_unknown, na_action = "exclude")
#> [1] 1

# Count unknowns as mismatches
quantifyMismatch(seq1, seq_with_unknown, na_action = "count")
#> [1] 1
```

## Donor-Recipient Mismatch Load

### Creating HLA Genotypes

First, create genotype objects using
[`hlaGeno()`](https://www.borch.dev/uploads/deepMatchR/reference/hlaGeno.md):

``` r
recipient <- data.frame(
  A_1 = "A*01:01", A_2 = "A*02:01",
  B_1 = "B*07:02", B_2 = "B*08:01",
  DRB1_1 = "DRB1*03:01", DRB1_2 = "DRB1*04:01"
)

donor <- data.frame(
  A_1 = "A*03:01", A_2 = "A*24:02",
  B_1 = "B*44:02", B_2 = "B*51:01",
  DRB1_1 = "DRB1*07:01", DRB1_2 = "DRB1*11:01"
)

rgeno <- hlaGeno(recipient)
dgeno <- hlaGeno(donor)
```

### Calculating Total Mismatch Load

``` r
calculateMismatchLoad(rgeno, dgeno, parallel = FALSE)
#> [1] 310
```

### Per-Locus Breakdown

``` r
per_locus <- calculateMismatchLoad(
  rgeno, dgeno,
  return = "per_locus",
  parallel = FALSE
)
per_locus
#>   locus mismatch_load
#> 1     A            96
#> 2     B           128
#> 3  DRB1            86
```

### Pairwise Allele Matrix

View mismatches between each recipient-donor allele pair:

``` r
mB <- calculateMismatchLoad(
  rgeno, dgeno,
  return = "pairwise",
  pairwise_locus = "B",
  parallel = FALSE
)
mB
#>          donor
#> recipient B*44:02 B*51:01
#>   B*07:02      37      33
#>   B*08:01      31      27
```

### Applying Filters

``` r
# Charge-changing mismatches only
calculateMismatchLoad(rgeno, dgeno, filter_charge = TRUE, parallel = FALSE)
#> [1] 123

# Polarity-changing mismatches only
calculateMismatchLoad(rgeno, dgeno, filter_polarity = TRUE, parallel = FALSE)
#> [1] 108

# Restrict to specific loci
calculateMismatchLoad(rgeno, dgeno, loci = c("A", "B"), parallel = FALSE)
#> [1] 224
```

## Function Reference

### `quantifyMismatch()`

| Argument                 | Default     | Description                                                |
|--------------------------|-------------|------------------------------------------------------------|
| `sequence1`, `sequence2` | –           | Two protein sequences (same length)                        |
| `filter_charge`          | `NULL`      | Filter by charge change                                    |
| `filter_polarity`        | `NULL`      | Filter by polarity change                                  |
| `return`                 | `"count"`   | Output type: `"count"` or `"detail"`                       |
| `na_action`              | `"exclude"` | Handle unknown residues: `"exclude"`, `"error"`, `"count"` |

### `calculateMismatchLoad()`

| Argument                           | Default   | Description                                                                                     |
|------------------------------------|-----------|-------------------------------------------------------------------------------------------------|
| `recipient_geno`, `donor_geno`     | –         | HLA genotypes from [`hlaGeno()`](https://www.borch.dev/uploads/deepMatchR/reference/hlaGeno.md) |
| `loci`                             | `NULL`    | Restrict to specific loci                                                                       |
| `filter_charge`, `filter_polarity` | `NULL`    | Biophysical filters                                                                             |
| `return`                           | `"total"` | `"total"`, `"per_locus"`, or `"pairwise"`                                                       |
| `pairwise_locus`                   | `NULL`    | Locus for pairwise matrix                                                                       |
| `parallel`                         | `TRUE`    | Use parallel processing                                                                         |

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
#> [52] pillar_1.11.1       bslib_0.9.0         gtable_0.3.6       
#> [55] data.table_1.18.0   glue_1.8.0          Rcpp_1.1.1         
#> [58] systemfonts_1.3.1   xfun_0.56           tibble_3.3.1       
#> [61] tidyselect_1.2.1    knitr_1.51          farver_2.1.2       
#> [64] patchwork_1.3.2     htmltools_0.5.9     rmarkdown_2.30     
#> [67] compiler_4.5.2      S7_0.2.1            readxl_1.4.5
```
