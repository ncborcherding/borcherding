# Examining the Diversity of Amino Acids by Position

This function the diversity amino acids along the residues of the CDR3
amino acid sequence. Please see
[`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
for more information on the underlying methods for diversity/entropy
calculations. Positions without variance will have a value reported as 0
for the purposes of comparison.

## Usage

``` r
positionalEntropy(
  input.data,
  chain = "TRB",
  group.by = NULL,
  order.by = NULL,
  aa.length = 20,
  method = "norm.entropy",
  export.table = NULL,
  palette = "inferno",
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

- chain:

  The TCR/BCR chain to use. Use `both` to include both chains (e.g.,
  TRA/TRB). Accepted values: `TRA`, `TRB`, `TRG`, `TRD`, `IGH`, `IGL`,
  `IGK`, `Light` (for both light chains), or `both` (for TRA/B and
  Heavy/Light).

- group.by:

  A column header in the metadata or lists to group the analysis by
  (e.g., "sample", "treatment"). If `NULL`, data will be analyzed as by
  list element or active identity in the case of single-cell objects.

- order.by:

  A character vector defining the desired order of elements of the
  `group.by` variable. Alternatively, use `alphanumeric` to sort groups
  automatically.

- aa.length:

  The maximum length of the CDR3 amino acid sequence.

- method:

  The method to calculate the entropy/diversity - `"shannon"`,
  `"inv.simpson"`, `"gini.simpson"`, `"norm.entropy"`, `"pielou"`,
  `"hill0"`, `"hill1"`, `"hill2"`

- export.table:

  If `TRUE`, returns a data frame or matrix of the results instead of a
  plot.

- palette:

  Colors to use in visualization - input any hcl.pals

- exportTable:

  **\[deprecated\]** Use `export.table` instead.

- ...:

  Additional arguments passed to the ggplot theme

## Value

A ggplot object displaying entropy or diversity by amino acid position.
If `exportTable = TRUE`, a matrix of the raw data is returned.

## Examples

``` r
# Making combined contig data
combined <- combineTCR(contig_list, 
                        samples = c("P17B", "P17L", "P18B", "P18L", 
                                    "P19B","P19L", "P20B", "P20L"))

# Using positionalEntropy()
positionalEntropy(combined, 
                  chain = "TRB", 
                  aa.length = 20)

                  
```
