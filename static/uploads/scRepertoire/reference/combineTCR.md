# Combine T Cell Receptor Contig Data

This function consolidates a list of TCR sequencing results to the level
of the individual cell barcodes. Using the `samples` and `ID`
parameters, the function will add the strings as prefixes to prevent
issues with repeated barcodes. The resulting new barcodes will need to
match the Seurat or SCE object in order to use,
[`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
Several levels of filtering exist - `remove.na`, `remove.multi`, or
`filter.multi` are parameters that control how the function deals with
barcodes with multiple chains recovered.

## Usage

``` r
combineTCR(
  input.data,
  samples = NULL,
  ID = NULL,
  remove.na = NULL,
  remove.multi = NULL,
  filter.multi = NULL,
  filter.nonproductive = NULL,
  removeNA = NULL,
  removeMulti = NULL,
  filterMulti = NULL,
  filterNonproductive = NULL
)
```

## Arguments

- input.data:

  List of filtered contig annotations or outputs from
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).

- samples:

  The labels of samples (recommended).

- ID:

  The additional sample labeling (optional).

- remove.na:

  This will remove any chain without values.

- remove.multi:

  This will remove barcodes with greater than 2 chains.

- filter.multi:

  This option will allow for the selection of the 2 corresponding chains
  with the highest expression for a single barcode.

- filter.nonproductive:

  This option will allow for the removal of nonproductive chains if the
  variable exists in the contig data. Default is set to TRUE to remove
  nonproductive contigs.

- removeNA:

  **\[deprecated\]** Use `remove.na` instead.

- removeMulti:

  **\[deprecated\]** Use `remove.multi` instead.

- filterMulti:

  **\[deprecated\]** Use `filter.multi` instead.

- filterNonproductive:

  **\[deprecated\]** Use `filter.nonproductive` instead.

## Value

List of clones for individual cell barcodes

## Examples

``` r
combined <- combineTCR(contig_list,
                        samples = c("P17B", "P17L", "P18B", "P18L",
                                    "P19B","P19L", "P20B", "P20L"))
```
