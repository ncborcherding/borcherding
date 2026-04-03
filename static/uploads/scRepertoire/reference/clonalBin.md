# Bin Clones by Frequency or Proportion

This function adds a clonal grouping variable (`cloneSize`) to the
output of
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md),
or
[`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
It calculates the clonal frequency and proportion, then bins clones into
categories based on customizable thresholds. This is useful for
categorizing clones prior to downstream analysis or visualization.

## Usage

``` r
clonalBin(
  input.data,
  clone.call = NULL,
  chain = "both",
  group.by = NULL,
  proportion = TRUE,
  clone.size = NULL,
  cloneCall = NULL,
  cloneSize = NULL
)
```

## Arguments

- input.data:

  The product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md),
  or
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).

- clone.call:

  Defines the clonal sequence grouping. Accepted values are: `gene`
  (VDJC genes), `nt` (CDR3 nucleotide sequence), `aa` (CDR3 amino acid
  sequence), or `strict` (VDJC + nt). A custom column header can also be
  used.

- chain:

  The TCR/BCR chain to use. Use `both` to include both chains (e.g.,
  TRA/TRB). Accepted values: `TRA`, `TRB`, `TRG`, `TRD`, `IGH`, `IGL`
  (for both light chains), `both`.

- group.by:

  A column header in the metadata to group the analysis by (e.g.,
  "sample", "treatment"). If `NULL`, data will be analyzed by list
  element.

- proportion:

  Whether to use proportion (`TRUE`) or total frequency (`FALSE`) of the
  clone for binning.

- clone.size:

  The bins for the grouping based on proportion or frequency. If
  proportion is `FALSE` and the clone.size values are not set high
  enough based on frequency, the upper limit of clone.size will be
  automatically updated.

- cloneCall:

  **\[deprecated\]** Use `clone.call` instead.

- cloneSize:

  **\[deprecated\]** Use `clone.size` instead.

## Value

A list of data frames with clonal frequency, clonal proportion, and
cloneSize columns added.

## Author

Nick Borcherding

## Examples

``` r
# Getting the combined contigs
combined <- combineTCR(contig_list,
                        samples = c("P17B", "P17L", "P18B", "P18L",
                                    "P19B","P19L", "P20B", "P20L"))

# Adding clonal bins with default settings (proportion-based)
combined <- clonalBin(combined)

# Adding clonal bins based on frequency
combined <- clonalBin(combined,
                      proportion = FALSE,
                      clone.size = c(Rare = 1, Small = 5, Medium = 20,
                                     Large = 100, Hyperexpanded = 500))

# Using a custom grouping variable
combined <- addVariable(combined,
                        variable.name = "Type",
                        variables = rep(c("B", "L"), 4))
combined <- clonalBin(combined, group.by = "Type")
```
