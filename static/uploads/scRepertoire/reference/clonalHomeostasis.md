# Plot Clonal Homeostasis of the Repertoire

This function calculates the space occupied by clone proportions. The
grouping of these clones is based on the parameter `clone.size`, at
default, `clone.size` will group the clones into bins of Rare = 0 to
0.0001, Small = 0.0001 to 0.001, etc. To adjust the proportions, change
the number or labeling of the clone.size parameter. If a matrix output
for the data is preferred, set `export.table` = TRUE.

## Usage

``` r
clonalHomeostasis(
  input.data,
  clone.size = NULL,
  clone.call = NULL,
  chain = "both",
  group.by = NULL,
  order.by = NULL,
  export.table = NULL,
  palette = "inferno",
  cloneSize = NULL,
  cloneCall = NULL,
  exportTable = NULL,
  ...
)
```

## Arguments

- input.data:

  The product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md),
  or
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).

- clone.size:

  The cut points of the proportions.

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

- group.by:

  A column header in the metadata or lists to group the analysis by
  (e.g., "sample", "treatment"). If `NULL`, data will be analyzed by
  list element or active identity in the case of single-cell objects.

- order.by:

  A character vector defining the desired order of elements of the
  `group.by` variable. Alternatively, use `alphanumeric` to sort groups
  automatically.

- export.table:

  If `TRUE`, returns a data frame or matrix of the results instead of a
  plot.

- palette:

  Colors to use in visualization - input any hcl.pals.

- cloneSize:

  **\[deprecated\]** Use `clone.size` instead.

- cloneCall:

  **\[deprecated\]** Use `clone.call` instead.

- exportTable:

  **\[deprecated\]** Use `export.table` instead.

- ...:

  Additional arguments passed to the ggplot theme

## Value

A ggplot object visualizing clonal homeostasis, or a data.frame if
`export.table = TRUE`.

## Examples

``` r
# Making combined contig data
combined <- combineTCR(contig_list,
                        samples = c("P17B", "P17L", "P18B", "P18L",
                                    "P19B","P19L", "P20B", "P20L"))
clonalHomeostasis(combined, clone.call = "gene")

```
