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
#> [1] 0
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
#> 1    A*02:01          0        0      0                 0
#> 2    A*03:01          0        0      0                 0
#> 3    B*07:02          0        0      0                 0
#> 4    B*08:01          0        0      0                 0
```

### Detailed Peptide Results

``` r
detailed_load <- calculatePeptideBindingLoad(
  recipient = rgeno,
  donor = dgeno,
  return = "detail"
)
head(detailed_load)
#> [1] peptide        hla_allele     predicted_ic50 binding_level  contribution  
#> <0 rows> (or 0-length row.names)
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
#> 1    A*02:01          0        0      0                 0
#> 2    A*03:01          0        0      0                 0
#> 3    B*07:02          0        0      0                 0
#> 4    B*08:01          0        0      0                 0
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
#> 1    A*02:01          0        0      0                 0
#> 2    A*03:01          0        0      0                 0
#> 3    B*07:02          0        0      0                 0
#> 4    B*08:01          0        0      0                 0
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
#> [46] patchwork_1.3.2         withr_3.0.2             filelock_1.0.3         
#> [49] scales_1.4.0            UCSC.utils_1.4.0        pwalign_1.4.0          
#> [52] rmarkdown_2.30          XVector_0.48.0          httr_1.4.7             
#> [55] otel_0.2.0              reticulate_1.44.1       cellranger_1.1.0       
#> [58] ragg_1.5.0              png_0.1-8               memoise_2.0.1          
#> [61] evaluate_1.0.5          knitr_1.51              IRanges_2.42.0         
#> [64] basilisk.utils_1.20.0   immReferent_0.99.0      rlang_1.1.6            
#> [67] Rcpp_1.1.0              glue_1.8.0              BiocManager_1.30.27    
#> [70] xml2_1.5.1              BiocGenerics_0.54.1     rstudioapi_0.17.1      
#> [73] jsonlite_2.0.0          R6_2.6.1                systemfonts_1.3.1      
#> [76] fs_1.6.6
```
