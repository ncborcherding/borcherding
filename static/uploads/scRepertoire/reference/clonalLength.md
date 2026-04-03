# Plot the Distribution of Sequence Lengths

This function displays either the nucleotide `nt` or amino acid `aa`
sequence length. The sequence length visualized can be selected using
the chains parameter, either the combined clone (both chains) or across
all single chains. Visualization can either be a histogram or if `scale`
= TRUE, the output will be a density plot. Multiple sequencing runs can
be group together using the group.by parameter.

## Usage

``` r
clonalLength(
  input.data,
  clone.call = NULL,
  chain = "both",
  group.by = NULL,
  order.by = NULL,
  scale = FALSE,
  export.table = NULL,
  palette = "inferno",
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
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)

- clone.call:

  Defines the clonal sequence grouping. Accepted values are: `nt` (CDR3
  nucleotide sequence) or `aa` (CDR3 amino acid sequence)

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

- scale:

  Converts the graphs into density plots in order to show relative
  distributions.

- export.table:

  If `TRUE`, returns a data frame or matrix of the results instead of a
  plot.

- palette:

  Colors to use in visualization - input any hcl.pals

- cloneCall:

  **\[deprecated\]** Use `clone.call` instead.

- exportTable:

  **\[deprecated\]** Use `export.table` instead.

- ...:

  Additional arguments passed to the ggplot theme

## Value

A ggplot object visualizing the distributions by length, or a data.frame
if `export.table = TRUE`.

## Examples

``` r
# Making combined contig data
combined <- combineTCR(contig_list,
                        samples = c("P17B", "P17L", "P18B", "P18L",
                                    "P19B","P19L", "P20B", "P20L"))
clonalLength(combined, clone.call = "aa", chain = "both")

```
