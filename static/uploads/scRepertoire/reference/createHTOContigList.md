# Deconvolute Contig Information from Multiplexed Experiments

This function reprocess and forms a list of contigs for downstream
analysis in scRepertoire, `createHTOContigList()` take the filtered
contig annotation output and the single-cell RNA object to create the
list. If using an integrated single-cell object, it is recommended to
split the object by sequencing run and remove extra prefixes and
suffixes on the barcode before using `createHTOContigList()`.
Alternatively, the variable `multi.run` can be used to separate a list
of contigs by a meta data variable. This may have issues with the
repeated barcodes.

## Usage

``` r
createHTOContigList(contig, sc.data, group.by = NULL, multi.run = NULL)
```

## Arguments

- contig:

  The filtered contig annotation file from multiplexed experiment

- sc.data:

  The Seurat or Single-Cell Experiment object.

- group.by:

  One or more meta data headers to create the contig list based on. If
  more than one header listed, the function combines them into a single
  variable.

- multi.run:

  If using integrated single-cell object, the meta data variable that
  indicates the sequencing run.

## Value

Returns a list of contigs as input for
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
or
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)

## Examples

``` r
if (FALSE) { # \dontrun{
filtered.contig <- read.csv(".../Sample/outs/filtered_contig_annotations.csv")

contig.list <- createHTOContigList(contig = filtered.contig, 
                                   sc.data = Seurat.Obj, 
                                   group.by = "HTO_maxID")
} # }
```
