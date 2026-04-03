# Load Immune Receptor Sequencing Contigs

This function loads and processes contig data from various single-cell
immune receptor sequencing formats. It reads data from a directory
(recursively) or from an already loaded list/data frame, transforms it
to a common structure, and returns a list of contigs ready for
downstream analysis with
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
or
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).

Supported file formats and their expected file names:

- `10X`: "filtered_contig_annotations.csv"

- `AIRR`: "airr_rearrangement.tsv"

- `BD`: "Contigs_AIRR.tsv"

- `Dandelion`: "all_contig_dandelion.tsv"

- `Immcantation`: "\_data.tsv" (or similar)

- “JSON\`: ".json"

- `ParseBio`: "barcode_report.tsv"

- `MiXCR`: "clones.tsv"

- `TRUST4`: "barcode_report.tsv"

- `WAT3R`: "barcode_results.csv"

## Usage

``` r
loadContigs(input, format = "10X")
```

## Arguments

- input:

  A directory path containing contig files or a list/data frame of
  pre-loaded contig data.

- format:

  A string specifying the data format. Must be one of: `auto`, `10X`,
  `AIRR`, `BD`, `Dandelion`, `JSON`, `MiXCR`, `ParseBio`, `TRUST4`,
  `WAT3R`, or `Immcantation`. If "auto", the function attempts automatic
  format detection.

## Value

A list of contigs formatted for use with
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
or
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).
Rows containing only NA values (aside from the barcode) are dropped.

## Examples

``` r
TRUST4 <- read.csv("https://www.borch.dev/uploads/contigs/TRUST4_contigs.csv")
contig.list <- loadContigs(TRUST4, format = "TRUST4")

BD <- read.csv("https://www.borch.dev/uploads/contigs/BD_contigs.csv")
contig.list <- loadContigs(BD, format = "BD")

WAT3R <- read.csv("https://www.borch.dev/uploads/contigs/WAT3R_contigs.csv")
contig.list <- loadContigs(WAT3R, format = "WAT3R")
```
