# Adding Clonal Information to Single-Cell Object

This function adds the immune receptor information to the Seurat or SCE
object to the meta data. By default this function also calculates the
frequencies and proportion of the clones by sequencing run (`group.by` =
NULL). To change how the frequencies/proportions are calculated, select
a column header for the `group.by` variable. Importantly, before using
`combineExpression()` ensure the barcodes of the single-cell object
object match the barcodes in the output of the
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
or
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).

## Usage

``` r
combineExpression(
  input.data,
  sc.data,
  clone.call = NULL,
  chain = "both",
  group.by = NULL,
  proportion = TRUE,
  filter.na = NULL,
  clone.size = NULL,
  add.label = NULL,
  cloneCall = NULL,
  cloneSize = NULL,
  filterNA = NULL,
  addLabel = NULL
)
```

## Arguments

- input.data:

  The product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  or a list of both
  c([`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)).

- sc.data:

  The Seurat or Single-Cell Experiment (SCE) object to attach

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

  A column header in lists to group the analysis by (e.g., "sample",
  "treatment"). If `NULL`, will be based on the list element.

- proportion:

  Whether to proportion (`TRUE`) or total frequency (`FALSE`) of the
  clone based on the group.by variable.

- filter.na:

  Method to subset Seurat/SCE object of barcodes without clone
  information

- clone.size:

  The bins for the grouping based on proportion or frequency. If
  proportion is `FALSE` and the clone.sizes are not set high enough
  based on frequency, the upper limit of clone.sizes will be
  automatically updated.

- add.label:

  This will add a label to the frequency header, allowing the user to
  try multiple group.by variables or recalculate frequencies after
  subsetting the data.

- cloneCall:

  **\[deprecated\]** Use `clone.call` instead.

- cloneSize:

  **\[deprecated\]** Use `clone.size` instead.

- filterNA:

  **\[deprecated\]** Use `filter.na` instead.

- addLabel:

  **\[deprecated\]** Use `add.label` instead.

## Value

Single-cell object with clone information added to meta data information

## Examples

``` r
# Getting the combined contigs
combined <- combineTCR(contig_list, 
                        samples = c("P17B", "P17L", "P18B", "P18L", 
                                    "P19B","P19L", "P20B", "P20L"))

# Getting a sample of a Seurat object
scRep_example <- get(data("scRep_example"))

# Using combineExpresion()
scRep_example <- combineExpression(combined, scRep_example)
```
