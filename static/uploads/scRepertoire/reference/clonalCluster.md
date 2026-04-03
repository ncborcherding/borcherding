# Cluster clones by sequence similarity

This function clusters TCRs or BCRs based on the edit distance or
alignment score of their CDR3 sequences. It can operate on either
nucleotide (`nt`) or amino acid (`aa`) sequences and can optionally
enforce that clones share the same V and/or J genes. The output can be
the input object with an added metadata column for cluster IDs, a sparse
adjacency matrix, or an `igraph` graph object representing the cluster
network.

## Usage

``` r
clonalCluster(
  input.data,
  chain = "TRB",
  sequence = "aa",
  threshold = 0.85,
  group.by = NULL,
  dist.type = NULL,
  dist.mat = NULL,
  normalize = "length",
  gap.open = NULL,
  gap.extend = NULL,
  cluster.method = "components",
  cluster.prefix = "cluster.",
  use.V = TRUE,
  use.J = FALSE,
  export.adj.matrix = NULL,
  export.graph = NULL,
  dist_type = NULL,
  dist_mat = NULL,
  gap_open = NULL,
  gap_extend = NULL,
  exportAdjMatrix = NULL,
  exportGraph = NULL
)
```

## Arguments

- input.data:

  The product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  or
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).

- chain:

  The TCR/BCR chain to use. Use `both` to include both chains (e.g.,
  TRA/TRB). Accepted values: `TRA`, `TRB`, `TRG`, `TRD`, `IGH`, `IGL`,
  `IGK`, `Light` (for both light chains), or `both` (for TRA/B and
  Heavy/Light).

- sequence:

  Clustering based on either `aa` or `nt` sequences.

- threshold:

  The similarity threshold. If \< 1, treated as normalized similarity
  (higher is stricter). If \>= 1, treated as raw edit distance (lower is
  stricter).

- group.by:

  A column header in the metadata or lists to group the analysis by
  (e.g., "sample", "treatment"). If `NULL`, clusters will be calculated
  across all sequences.

- dist.type:

  The distance metric to use. Options: `"levenshtein"` (default),
  `"hamming"`, `"damerau"` (allows transpositions), `"nw"`
  (Needleman-Wunsch), or `"sw"` (Smith-Waterman).

- dist.mat:

  The substitution matrix to use for alignment-based metrics (`"nw"` or
  `"sw"`). Options: `"BLOSUM45"`, `"BLOSUM50"`, `"BLOSUM62"`,
  `"BLOSUM80"` (default), `"BLOSUM100"`, `"PAM30"`, `"PAM40"`,
  `"PAM70"`, `"PAM120"`, `"PAM250"`, or `"identity"`.

- normalize:

  Method for normalizing distances. Options: `"none"`, `"maxlen"`
  (divide by max sequence length), or `"length"` (default, divide by
  mean sequence length). If `threshold < 1`, this controls how the
  similarity is calculated.

- gap.open:

  Penalty for opening a gap in alignment metrics (default: -10).

- gap.extend:

  Penalty for extending a gap in alignment metrics (default: -1).

- cluster.method:

  The clustering algorithm to use. Defaults to `"components"`, which
  finds connected subgraphs.

- cluster.prefix:

  A character prefix to add to the cluster names (e.g., "cluster.").

- use.V:

  If `TRUE`, sequences must share the same V gene to be clustered
  together.

- use.J:

  If `TRUE`, sequences must share the same J gene to be clustered
  together.

- export.adj.matrix:

  If `TRUE`, the function returns a sparse adjacency matrix
  (`dgCMatrix`) of the network.

- export.graph:

  If `TRUE`, the function returns an `igraph` object of the sequence
  network.

- dist_type:

  **\[deprecated\]** Use `dist.type` instead.

- dist_mat:

  **\[deprecated\]** Use `dist.mat` instead.

- gap_open:

  **\[deprecated\]** Use `gap.open` instead.

- gap_extend:

  **\[deprecated\]** Use `gap.extend` instead.

- exportAdjMatrix:

  **\[deprecated\]** Use `export.adj.matrix` instead.

- exportGraph:

  **\[deprecated\]** Use `export.graph` instead.

## Value

Depending on the export parameters, one of the following:

- An amended `input.data` object with a new metadata column containing
  cluster IDs (default).

- An `igraph` object if `export.graph = TRUE`.

- A sparse `dgCMatrix` object if `export.adj.matrix = TRUE`.

## Details

The clustering process is as follows:

1.  The function retrieves the relevant chain data from the input
    object.

2.  It calculates the distance between all sequences within each group
    (or across the entire dataset if `group.by` is `NULL`).

3.  An edge list is constructed, connecting sequences that meet the
    similarity `threshold`.

4.  The `threshold` parameter behaves differently based on its value:

    - **`threshold` \< 1 (e.g., 0.85):** Interpreted as a *normalized*
      distance. A higher value means greater similarity is required.

    - **`threshold` \>= 1 (e.g., 2):** Interpreted as a maximum *raw*
      edit distance. A lower value means greater similarity is required.

5.  **Distance Metrics:**

    - **Levenshtein/Hamming/Damerau:** Standard edit distance
      calculations.

    - **Alignment (NW/SW):** If `dist.type` is "nw" (Needleman-Wunsch)
      or "sw" (Smith-Waterman), alignment scores are calculated using
      the specified substitution matrix (`dist.mat`). These scores are
      converted to a distance-like metric for clustering.

6.  An `igraph` graph is built from the edge list.

7.  A clustering algorithm is run on the graph (default: connected
    components).

## Examples

``` r
# Getting the combined contigs
combined <- combineTCR(contig_list,
                       samples = c("P17B", "P17L", "P18B", "P18L",
                                   "P19B","P19L", "P20B", "P20L"))

# Standard Levenshtein clustering (85% similarity)
sub_combined <- clonalCluster(combined[c(1,2)],
                              chain = "TRA",
                              sequence = "aa",
                              threshold = 0.85)

# Alignment-based clustering using BLOSUM80
sub_combined_nw <- clonalCluster(combined[c(1,2)],
                                 chain = "TRA",
                                 dist.type = "nw",
                                 dist.mat = "BLOSUM80",
                                 threshold = 0.85)

# Export the graph object instead
graph_obj <- clonalCluster(combined[c(1,2)],
                           chain = "TRA",
                           export.graph = TRUE)
```
