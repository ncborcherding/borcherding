# Get Sequence Statistics

Analyzes sequences to provide statistics about length, composition, and
optionally comparison metrics (reference similarity, pairwise identity),
k-mer entropy, and data-quality flags.

## Usage

``` r
getSequenceStats(
  sequences,
  type = c("PROT", "NUC"),
  ref = NULL,
  k = 2L,
  ignore_chars = c("*", "-", " "),
  compute_pairs = FALSE,
  warn_invalid = TRUE
)
```

## Arguments

- sequences:

  Named list (or named character vector) of sequences (e.g., output from
  batchGetSequences). Names should be allele IDs.

- type:

  Type of sequences: "PROT" (amino acids) or "NUC" (nucleotides).

- ref:

  Optional reference for comparison; either the \*name\* of one sequence
  in \`sequences\` or a raw sequence string of the same \`type\`.

- k:

  Integer k for k-mer Shannon entropy (default 2).

- ignore_chars:

  Characters to ignore when computing counts/identity (default c("\*",
  "-", " ")). Useful for protein stop symbols or gaps.

- compute_pairs:

  Logical; if TRUE, also compute a pairwise percent identity matrix
  (alignment-free, position-wise) and return a list with \`stats\` and
  \`pairwise_identity\`. Default FALSE (returns only \`stats\`).

- warn_invalid:

  Logical; if TRUE (default), warn when invalid symbols for the chosen
  \`type\` are detected.

## Value

If \`compute_pairs = FALSE\` (default): a data.frame with per-sequence
stats. If \`compute_pairs = TRUE\`: a list with elements: - \`stats\`:
per-sequence stats data.frame - \`pairwise_identity\`: numeric matrix
(0..1) of

## Examples

``` r
alleles <- c("A*01:01", "A*02:01", "B*07:02")
seqs <- batchGetSequences(alleles)
stats <- getSequenceStats(seqs, type = "PROT")
```
