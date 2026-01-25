# Convert HLA Alleles to Serological Equivalents

Converts HLA alleles in IMGT/HLA nomenclature (e.g., "A\*01:01") to
their serological equivalents (e.g., "A1") using WMDA standard
nomenclature.

## Usage

``` r
toSerology(
  x,
  locus = NULL,
  resolve_splits = TRUE,
  return = c("serology", "genotype", "data.frame"),
  na_action = c("NA", "warn", "error")
)
```

## Arguments

- x:

  Character vector of HLA alleles OR an `hla_genotype` object.

- locus:

  Optional character. Override locus detection for ambiguous cases.

- resolve_splits:

  Logical. If TRUE (default), attempts to infer split antigens from
  broad antigens (e.g., DR2 -\> DR15 or DR16 based on the allele).

- return:

  Character. Output format:

  - `"serology"` (default): Returns character vector of serology strings

  - `"genotype"`: Returns hla_genotype with `*_ser_*` columns added

  - `"data.frame"`: Returns data.frame with allele, locus, serology
    columns

- na_action:

  Character. How to handle alleles without serology mapping:

  - `"NA"` (default): Return NA for unknown alleles

  - `"warn"`: Return NA and issue a warning

  - `"error"`: Stop with an error

## Value

Depends on `return` parameter. See above.

## Details

This function uses the WMDA (World Marrow Donor Association)
nomenclature files to map HLA alleles to their serological equivalents.
The mapping considers:

- Unambiguous assignments (highest priority)

- Possible assignments

- Assumed assignments

- Expert assignments

When `resolve_splits = TRUE`, broad antigens like DR2 are resolved to
their split antigens (DR15 or DR16) based on the specific allele.

P-group notation (e.g., "A\*01:01P") is automatically resolved to the
reference allele.

## Examples

``` r
# Single allele conversion
toSerology("A*01:01")
#> [1] "A1"

# Vector of alleles
toSerology(c("A*01:01", "B*07:02", "DRB1*03:01"))
#> [1] "A1"   "B7"   "DR17"

# Get detailed data.frame
toSerology(c("A*01:01", "B*07:02"), return = "data.frame")
#>    allele locus allele_2f serology serology_full
#> 1 A*01:01     A     01:01        1            A1
#> 2 B*07:02     B     07:02        7            B7

# With hla_genotype object
geno <- hlaGeno(data.frame(
  A_1 = "A*01:01", A_2 = "A*02:01",
  B_1 = "B*07:02", B_2 = "B*08:01",
  stringsAsFactors = FALSE
))
toSerology(geno, return = "serology")
#> A*01:01 A*02:01 B*07:02 B*08:01 
#>    "A1"    "A2"    "B7"    "B8" 
toSerology(geno, return = "genotype")
#> HLA Genotype Data
#> -----------------
#> Loci present: A, B 
#> Number of samples: 1 
#> 
#>       A_1     A_2     B_1     B_2 A_ser_1 A_ser_2 B_ser_1 B_ser_2
#> 1 A*01:01 A*02:01 B*07:02 B*08:01      A1      A2      B7      B8
```
