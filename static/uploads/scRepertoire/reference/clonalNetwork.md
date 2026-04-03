# Visualize Clonal Network in Dimensional Reductions

This function generates a network based on clonal proportions of an
indicated identity and then superimposes the network onto a single-cell
object dimensional reduction plot.

## Usage

``` r
clonalNetwork(
  sc.data,
  clone.call = NULL,
  chain = "both",
  reduction = "umap",
  group.by = "ident",
  filter.clones = NULL,
  filter.identity = NULL,
  filter.proportion = NULL,
  filter.graph = FALSE,
  export.clones = NULL,
  export.table = NULL,
  palette = "inferno",
  cloneCall = NULL,
  exportClones = NULL,
  exportTable = NULL,
  ...
)
```

## Arguments

- sc.data:

  The single-cell object after
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).

- clone.call:

  Defines the clonal sequence grouping. Accepted values are: `gene`
  (VDJC genes), `nt` (CDR3 nucleotide sequence), `aa` (CDR3 amino acid
  sequence), or `strict` (VDJC + nt). A custom column header can also be
  used.

- chain:

  The TCR/BCR chain to use. Use `both` to include both chains (e.g.,
  TRA/TRB). Accepted values: `TRA`, `TRB`, `TRG`, `TRD`, `IGH`, `IGL`,
  `IGK`, `Light` (for both light chains), or `both` (for TRA/B and
  Heavy/Light).

- reduction:

  The name of the dimensional reduction of the single-cell object.

- group.by:

  A column header in the metadata or lists to group the analysis by
  (e.g., "sample", "treatment"). This will be the nodes overlaid onto
  the graph.

- filter.clones:

  Use to select the top n clones (e.g.,
  `` filter.clones`**` = 2000) or n of clones based on the minimum number of all the comparators (e.g., `filter.clone ``
  = "min").

- filter.identity:

  Display the network for a specific level of the indicated identity.

- filter.proportion:

  Remove clones from the network below a specific proportion.

- filter.graph:

  Remove the reciprocal edges from the half of the graph, allowing for
  cleaner visualization.

- export.clones:

  Exports a table of clones that are shared across multiple identity
  groups and ordered by the total number of clone copies.

- export.table:

  If `TRUE`, returns a data frame or matrix of the results instead of a
  plot.

- palette:

  Colors to use in visualization - input any hcl.pals.

- cloneCall:

  **\[deprecated\]** Use `clone.call` instead.

- exportClones:

  **\[deprecated\]** Use `export.clones` instead.

- exportTable:

  **\[deprecated\]** Use `export.table` instead.

- ...:

  Additional arguments passed to the ggplot theme

## Value

ggplot object

## Examples

``` r
if (FALSE) { # \dontrun{
# Getting the combined contigs
combined <- combineTCR(contig_list,
                        samples = c("P17B", "P17L", "P18B", "P18L",
                                    "P19B","P19L", "P20B", "P20L"))

# Getting a sample of a Seurat object
scRep_example  <- get(data("scRep_example"))

# Using combineExpresion()
scRep_example  <- combineExpression(combined, scRep_example)

# Using clonalNetwork()
clonalNetwork(scRep_example,
              reduction = "umap",
              group.by = "seurat_clusters")
} # }
```
