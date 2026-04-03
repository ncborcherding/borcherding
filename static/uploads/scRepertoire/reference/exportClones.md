# Export Clonal Data in Various Formats

Exports clonal information (gene sequences, amino acids, nucleotides)
from scRepertoire objects into a file or a data frame. The output format
can be tailored for compatibility with different analysis workflows.

## Usage

``` r
exportClones(
  input.data,
  format = "paired",
  group.by = NULL,
  write.file = TRUE,
  dir = NULL,
  file.name = "clones.csv"
)
```

## Arguments

- input.data:

  The product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md),
  or
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).

- format:

  The format for exporting clones. Options are: `paired`, `airr`,
  `TCRMatch`, `tcrpheno`, `immunarch`.

- group.by:

  The variable in the metadata to use for grouping. If `NULL`, data will
  be grouped by the sample names.

- write.file:

  If `TRUE` (default), saves the output to a CSV file. If `FALSE`,
  returns the data frame or list to the R environment.

- dir:

  The directory where the output file will be saved. Defaults to the
  current working directory.

- file.name:

  The name of the file to be saved.

## Value

A data frame or list in the specified format, either returned to the R
environment or saved as a CSV file.

## Details

The `format` parameter determines the structure of the output:

- `paired`: Exports a data frame where each row represents a barcode,
  with paired chain information (amino acid, nucleotide, genes) in
  separate columns.

- `airr`: Exports a data frame that adheres to the Adaptive Immune
  Receptor Repertoire (AIRR) Community format, with each row
  representing a single receptor chain.

- `TCRMatch`: Exports a data frame specifically for the TCRMatch
  algorithm, containing the TRB chain amino acid sequence and clonal
  frequency.

- `tcrpheno`: Exports a data frame compatible with the `tcrpheno`
  pipeline, with TRA and TRB chains in separate columns.

- `immunarch`: Exports a list containing a data frame and metadata
  formatted for use with the `immunarch` package.

## Author

Jonathan Noonan, Nick Borcherding

## Examples

``` r
if (FALSE) { # \dontrun{
#Making combined contig data
combined <- combineTCR(contig_list,
                       samples = c("P17B", "P17L", "P18B", "P18L",
                                   "P19B", "P19L", "P20B", "P20L"))

# Export as a paired data frame and save to a file
exportClones(combined, format = "paired", file.name = "paired_clones.csv")

# Return an AIRR-formatted data frame to the environment
airr_df <- exportClones(combined, format = "airr", write.file = FALSE)
} # }
```
