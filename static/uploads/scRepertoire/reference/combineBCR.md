# Combine B Cell Receptor Contig Data

This function consolidates a list of BCR sequencing results to the level
of the individual cell barcodes. Using the samples and ID parameters,
the function will add the strings as prefixes to prevent issues with
repeated barcodes. The resulting new barcodes will need to match the
Seurat or SCE object in order to use,
[`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
Unlike
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
combineBCR produces a column `CTstrict` based on the edit distance
clustering from
[`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md).
The `CTstrict` column is formatted as `Heavy_Light`
(underscore-separated) for downstream compatibility. Connected clones
are labeled with `cluster.X`, while unconnected clones (singlets) are
labeled with the V gene and CDR3 sequence (e.g.,
`IGHV3-64.CAKSYS..._IGKV3-15.CQQYSN...`).

## Usage

``` r
combineBCR(
  input.data,
  samples = NULL,
  ID = NULL,
  chain = "both",
  sequence = "nt",
  dist.type = NULL,
  dist.mat = NULL,
  normalize = "length",
  gap.open = NULL,
  gap.extend = NULL,
  call.related.clones = TRUE,
  group.by = NULL,
  threshold = 0.85,
  cluster.method = "components",
  use.V = TRUE,
  use.J = TRUE,
  remove.na = NULL,
  remove.multi = NULL,
  filter.multi = NULL,
  filter.nonproductive = NULL,
  removeNA = NULL,
  removeMulti = NULL,
  filterMulti = NULL,
  filterNonproductive = NULL,
  dist_type = NULL,
  dist_mat = NULL,
  gap_open = NULL,
  gap_extend = NULL
)
```

## Arguments

- input.data:

  List of filtered contig annotations or outputs from
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).

- samples:

  A character vector of sample labels. Must be the same length as the
  input list.

- ID:

  An optional character vector for additional sample identifiers.

- chain:

  The chain to use for clustering when `call.related.clones = TRUE`.
  Passed to
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md).
  Default is `"both"`.

- sequence:

  The sequence type (`"nt"` or `"aa"`) to use for clustering. Passed to
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md).
  Default is `"nt"`.

- dist.type:

  The distance metric to use. Options: `"levenshtein"` (default),
  `"hamming"`, `"damerau"`, `"nw"` (Needleman-Wunsch), or `"sw"`
  (Smith-Waterman).

- dist.mat:

  The substitution matrix to use for alignment-based metrics (`"nw"` or
  `"sw"`). Options include `"BLOSUM62"`, `"PAM30"`, etc.

- normalize:

  Method for normalizing distances. Options: `"none"` (default),
  `"maxlen"`, or `"length"`.

- gap.open:

  Penalty for opening a gap in alignment metrics (default: -10).

- gap.extend:

  Penalty for extending a gap in alignment metrics (default: -1).

- call.related.clones:

  Logical. If `TRUE`, uses
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  to identify related clones based on sequence similarity. If `FALSE`,
  defines clones by the exact V-gene and CDR3 amino acid sequence.

- group.by:

  The column header used for to group clones. If (\`NULL“), clusters
  will be calculated across samples.

- threshold:

  The similarity threshold passed to
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  if `call.related.clones = TRUE`. See
  [`?clonalCluster`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  for details.

- cluster.method:

  The clustering algorithm to use. Defaults to `"components"`, which
  finds connected subgraphs.

- use.V:

  Logical. If `TRUE`, sequences must share the same V gene to be
  clustered together.

- use.J:

  Logical. If `TRUE`, sequences must share the same J gene to be
  clustered together.

- remove.na:

  This will remove any chain without values.

- remove.multi:

  Logical. If `TRUE`, removes cells that have more than one distinct
  heavy or light chain after processing.

- filter.multi:

  Logical. If `TRUE`, filters multi-chain cells to retain only the most
  abundant IGH and IGL/IGK chains.

- filter.nonproductive:

  Logical. If `TRUE`, removes non-productive contigs from the analysis.

- removeNA:

  **\[deprecated\]** Use `remove.na` instead.

- removeMulti:

  **\[deprecated\]** Use `remove.multi` instead.

- filterMulti:

  **\[deprecated\]** Use `filter.multi` instead.

- filterNonproductive:

  **\[deprecated\]** Use `filter.nonproductive` instead.

- dist_type:

  **\[deprecated\]** Use `dist.type` instead.

- dist_mat:

  **\[deprecated\]** Use `dist.mat` instead.

- gap_open:

  **\[deprecated\]** Use `gap.open` instead.

- gap_extend:

  **\[deprecated\]** Use `gap.extend` instead.

## Value

A list of data frames, where each data frame represents a sample. Each
row corresponds to a unique cell barcode, with columns detailing the BCR
chains and the assigned clone ID.

## Examples

``` r
# Data derived from the 10x Genomics intratumoral NSCLC B cells
BCR <- read.csv("https://www.borch.dev/uploads/contigs/b_contigs.csv")
combined <- combineBCR(BCR,
                       samples = "Patient1",
                       threshold = 0.85)
```
