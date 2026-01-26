# Peptide Binding Prediction

## Introduction

Peptide-MHC binding prediction is central to understanding T
cell-mediated immunity. In the context of transplantation, predicting
how recipient HLA molecules might present donor-derived peptides helps
assess immunological risk.

This article covers:

- Using MHCnuggets for peptide binding prediction
- Calculating peptide binding load for donor-recipient pairs
- Interpreting binding predictions

## Loading the Package

``` r
library(deepMatchR)
library(dplyr)
```

## Background

### Peptide-MHC Binding

MHC molecules present peptides to T cells. The binding affinity between
a peptide and an MHC molecule determines:

- **Presentation likelihood:** Strong binders are more likely to be
  presented
- **T cell activation potential:** Better presentation leads to stronger
  T cell responses
- **Immunogenicity:** Peptides that bind well and differ from self are
  immunogenic

### Binding Thresholds

Binding affinity is typically measured as IC50 (half-maximal inhibitory
concentration):

| IC50 (nM) | Classification      |
|-----------|---------------------|
| \< 50     | Strong binder       |
| 50-500    | Intermediate binder |
| 500-5000  | Weak binder         |
| \> 5000   | Non-binder          |

## MHCnuggets Prediction

### Overview

[`predictMHCnuggets()`](https://www.borch.dev/uploads/deepMatchR/reference/predictMHCnuggets.md)
provides an R interface to MHCnuggets, a deep learning model for
peptide-MHC binding prediction.

> **Note:** MHCnuggets requires Python dependencies via basilisk. This
> functionality is not available on Windows due to path length
> limitations.

### Basic Usage

``` r
# Define peptides and allele
peptides <- c("SIINFEKL", "LLFGYPVYV", "GILGFVFTL")
allele <- "A*02:01"

# Predict binding affinity
binding_results <- predictMHCnuggets(
  peptides = peptides,
  allele = allele,
  mhc_class = "I"
)
#> Predicting for 3 peptides
#> Number of peptides skipped/total due to length 0 / 0
#> Building model
#> Closest allele found HLA-A02:01
#> BA_to_HLAp model found, predicting with BA_to_HLAp model...
#> Writing output files...

print(binding_results)
#>     peptide    ic50
#> 1  SIINFEKL 5600.06
#> 2 LLFGYPVYV  535.92
#> 3 GILGFVFTL  589.25
```

### Interpretation

The output includes:

- **peptide:** Input peptide sequence
- **allele:** HLA allele tested
- **ic50:** Predicted binding affinity in nM
- **rank:** Percentile rank (if `rank_output = TRUE`)

## Peptide Binding Load

### Concept

The
[`calculatePeptideBindingLoad()`](https://www.borch.dev/uploads/deepMatchR/reference/calculatePeptideBindingLoad.md)
function estimates transplant risk by:

1.  Identifying mismatched peptides from donor sequences
2.  Predicting binding to recipient HLA molecules
3.  Aggregating predictions into a risk score

### Creating Genotypes

``` r
recipient <- data.frame(
  A_1 = "A*02:01", A_2 = "A*03:01",
  B_1 = "B*07:02", B_2 = "B*08:01"
)

donor <- data.frame(
  A_1 = "A*01:01", A_2 = "A*24:02",
  B_1 = "B*44:02", B_2 = "B*51:01"
)

rgeno <- hlaGeno(recipient)
dgeno <- hlaGeno(donor)
```

### Total Risk Score

``` r
total_risk <- calculatePeptideBindingLoad(
  recipient = rgeno,
  donor = dgeno,
  return = "total"
)
print(total_risk)
#> [1] 507.75
```

### Per-Allele Summary

``` r
summary_load <- calculatePeptideBindingLoad(
  recipient = rgeno,
  donor = dgeno,
  return = "summary"
)
print(summary_load)
#>   hla_allele n_peptides n_strong n_weak risk_contribution
#> 1    A*02:01        601        0    346           187.750
#> 2    A*03:01        601        0    346           187.750
#> 3    B*07:02        601        0    293            66.125
#> 4    B*08:01        601        0    293            66.125
```

### Detailed Peptide Results

``` r
detailed_load <- calculatePeptideBindingLoad(
  recipient = rgeno,
  donor = dgeno,
  return = "detail"
)
head(detailed_load)
#>     peptide hla_allele predicted_ic50 binding_level contribution
#> 1 AVMAPRTLL    A*02:01            625          weak        0.875
#> 2 VMAPRTLLL    A*02:01            625          weak        0.875
#> 3 MAPRTLLLL    A*02:01            625          weak        0.875
#> 4 APRTLLLLL    A*02:01           2500          weak        0.500
#> 5 PRTLLLLLS    A*02:01          10000    non_binder        0.000
#> 6 RTLLLLLSG    A*02:01           2500          weak        0.500
```

## Backends

### Available Backends

[`calculatePeptideBindingLoad()`](https://www.borch.dev/uploads/deepMatchR/reference/calculatePeptideBindingLoad.md)
supports multiple prediction backends:

| Backend      | Description                      | Requirements        |
|--------------|----------------------------------|---------------------|
| `pwm`        | Position Weight Matrix (default) | R only              |
| `mhcnuggets` | Deep learning model              | Python              |
| `netmhcpan`  | External tool                    | NetMHCpan installed |
| `mhcflurry`  | Deep learning model              | Python              |

### Using PWM (Default)

The PWM backend uses pre-computed position-specific scoring matrices
based on HLA supertypes:

``` r
result_pwm <- calculatePeptideBindingLoad(
  recipient = rgeno,
  donor = dgeno,
  backend = "pwm",
  return = "summary"
)
print(result_pwm)
#>   hla_allele n_peptides n_strong n_weak risk_contribution
#> 1    A*02:01        601        0    346           187.750
#> 2    A*03:01        601        0    346           187.750
#> 3    B*07:02        601        0    293            66.125
#> 4    B*08:01        601        0    293            66.125
```

### Customizing Thresholds

``` r
# Adjust binding thresholds
result_custom <- calculatePeptideBindingLoad(
  recipient = rgeno,
  donor = dgeno,
  binding_threshold = 100,   # Strong binder threshold
  weak_threshold = 1000,     # Weak binder threshold
  return = "summary"
)
print(result_custom)
#>   hla_allele n_peptides n_strong n_weak risk_contribution
#> 1    A*02:01        601        0     78            29.250
#> 2    A*03:01        601        0     78            29.250
#> 3    B*07:02        601        0      3             1.125
#> 4    B*08:01        601        0      3             1.125
```

## Clinical Applications

### Transplant Risk Assessment

Peptide binding load can complement eplet-based analysis:

1.  **Eplet load:** Predicts antibody-mediated rejection risk
2.  **Peptide binding load:** Predicts T cell-mediated rejection risk

### Integration with Other Metrics

Consider combining peptide binding predictions with:

- HLA mismatch count
- Eplet mismatch load
- Pre-existing antibody profiles
- Clinical risk factors

## Function Reference

### `predictMHCnuggets()`

| Argument      | Default | Description                           |
|---------------|---------|---------------------------------------|
| `peptides`    | –       | Character vector of peptide sequences |
| `allele`      | –       | HLA allele (e.g., “A\*02:01”)         |
| `mhc_class`   | `"I"`   | MHC class: “I” or “II”                |
| `rank_output` | `FALSE` | Include percentile rank               |

### `calculatePeptideBindingLoad()`

| Argument            | Default   | Description                               |
|---------------------|-----------|-------------------------------------------|
| `recipient`         | –         | Recipient genotype or allele vector       |
| `donor`             | –         | Donor peptides or genotype                |
| `backend`           | `"pwm"`   | Prediction backend                        |
| `peptide_length`    | `9L`      | Peptide length for analysis               |
| `binding_threshold` | `500`     | IC50 threshold for strong binding         |
| `weak_threshold`    | `5000`    | IC50 threshold for weak binding           |
| `return`            | `"total"` | Output type: “total”, “summary”, “detail” |
| `aggregate_method`  | `"sum"`   | Aggregation: “sum”, “max”, “mean”         |

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
