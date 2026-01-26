# Get Sequence for an HLA Allele

Improved version with session-level caching to avoid redundant API
calls. Uses memoise for automatic caching. Supports both nucleotide and
protein sequences.

## Usage

``` r
getAlleleSequence(
  allele_name,
  type = c("PROT", "NUC"),
  use_cache = TRUE,
  cache_dir = NULL
)
```

## Arguments

- allele_name:

  A character string representing the HLA allele name

- type:

  The type of sequence to retrieve. Either "NUC" for nucleotide or
  "PROT" for protein sequences (default "PROT")

- use_cache:

  Logical, whether to use caching (default TRUE)

- cache_dir:

  Optional directory for persistent cache

## Value

A character string representing the sequence (amino acid or nucleotide)

## Examples

``` r
# \donttest{
# Collecting A*02:01 Protein Sequence (requires internet):
seq <- getAlleleSequence("A*02:01")
nchar(seq)  # Length of sequence
#> [1] 365

# Collecting A*02:01 Nucleotide Sequence:
seq_nuc <- getAlleleSequence("A*02:01", type = "NUC")

# Get sequence for HLA-B allele
seq_b <- getAlleleSequence("B*07:02")
# }
```
