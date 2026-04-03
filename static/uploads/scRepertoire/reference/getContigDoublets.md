# Get Contig Doublets

**\[experimental\]**

This function identifies potential doublets by finding common barcodes
between TCR and BCR outputs. It extracts unique barcodes from each list
of dataframes, finds the intersection of the barcodes, and joins the
resulting data.

## Usage

``` r
getContigDoublets(tcrOutput, bcrOutput)
```

## Arguments

- tcrOutput:

  Output of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md).
  A list of data.frames containing TCR contig information, each
  dataframe must have a `barcode` column.

- bcrOutput:

  Output of
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).
  A list of data.frames containing BCR contig information, each
  dataframe must have a `barcode` column.

## Value

A dataframe of barcodes that exist in both the TCR and BCR data, with
columns from both sets of data. There will be an additional column
`contigType` of type factor with levels 'TCR' and 'BCR' indicating the
origin of the contig - this will be the new first column.

If there are no doublets, the returned data.frame will have the same
colnames but no rows.
