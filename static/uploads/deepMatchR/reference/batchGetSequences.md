# Batch Get Sequences with Parallel Processing

Retrieves sequences for multiple alleles in parallel for better
performance. Supports both nucleotide and protein sequences.

## Usage

``` r
batchGetSequences(
  alleles,
  type = c("PROT", "NUC"),
  n_cores = 2,
  use_cache = TRUE,
  cache_dir = NULL,
  verbose = FALSE
)
```

## Arguments

- alleles:

  Character vector of HLA allele names

- type:

  The type of sequence to retrieve. Either "NUC" for nucleotide or
  "PROT" for protein sequences (default "PROT")

- n_cores:

  Number of cores to use (default: detectCores() - 1)

- use_cache:

  Whether to use caching (default TRUE)

- cache_dir:

  Optional directory for persistent cache

- verbose:

  Logical, whether to print progress messages (default FALSE)

## Value

Named list of sequences

## Examples

``` r
# Get protein sequences for multiple alleles
alleles <- c("A*01:01", "A*02:01", "B*07:02", "B*08:01")
prot_seqs <- batchGetSequences(alleles, type = "PROT")

# Get nucleotide sequences with parallel processing
nuc_seqs <- batchGetSequences(alleles, type = "NUC", n_cores = 4)

```
