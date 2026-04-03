# Visualize Clonal Relationships as a Chord Diagram

This function creates a chord diagram visualization of shared clones
between groups using the circlize package. It provides a convenient
wrapper around
[`getCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/getCirclize.md)
that handles the circlize plotting code automatically.

## Usage

``` r
vizCirclize(
  sc.data,
  clone.call = NULL,
  group.by = NULL,
  method = c("unique", "jaccard", "overlap"),
  proportion = FALSE,
  directional = FALSE,
  self.link = 1,
  include.self = TRUE,
  transparency = 0.5,
  link.visible = TRUE,
  annotate.sectors = TRUE,
  min.shared = 0,
  palette = "inferno",
  sector.colors = NULL,
  export.table = FALSE
)
```

## Arguments

- sc.data:

  The single-cell object after
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).

- clone.call:

  Defines the clonal sequence grouping. Accepted values are: `gene`
  (VDJC genes), `nt` (CDR3 nucleotide sequence), `aa` (CDR3 amino acid
  sequence), or `strict` (VDJC + nt). A custom column header can also be
  used.

- group.by:

  A column header (or vector of column headers for hierarchical
  grouping) in the metadata to group the analysis by.

- method:

  The method for calculating link values: `"unique"` (default) counts
  unique shared clones, `"jaccard"` calculates Jaccard similarity,
  `"overlap"` calculates overlap coefficient.

- proportion:

  Calculate the relationship by unique clones (`FALSE`, default) or
  normalized by proportion (`TRUE`).

- directional:

  If `TRUE`, show directional arrows on chords. Default is `FALSE`.

- self.link:

  How to handle self-links. `1` = show as loops, `2` = show as parallel
  lines. Default is `1`.

- include.self:

  Include self-links (clones within a single group). Default is `TRUE`.

- transparency:

  Transparency of the chord links (0-1). Default is `0.5`.

- link.visible:

  If `FALSE`, hide the chord links and show only sectors.

- annotate.sectors:

  If `TRUE` (default), display sector names.

- min.shared:

  Minimum number of shared clones to include a link (default 0).

- palette:

  Colors to use for sectors - input any hcl.pals.

- sector.colors:

  Named vector of colors for specific sectors. Overrides palette.

- export.table:

  If `TRUE`, returns the data instead of plotting.

## Value

Invisibly returns the circlize data list. If circlize is not installed
or `export.table = TRUE`, returns the data that would be used for
plotting.

## Details

This function requires the circlize package to be installed. If circlize
is not available, the function will return the data that would be used
for plotting and provide instructions for manual plotting.

The chord diagram shows relationships between groups (sectors) where the
width of each chord represents the number or proportion of shared clones
between the connected groups.

## See also

[`getCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/getCirclize.md)
for generating the underlying data

## Author

Nick Borcherding

## Examples

``` r
if (FALSE) { # \dontrun{
# Getting the combined contigs
combined <- combineTCR(contig_list,
                        samples = c("P17B", "P17L", "P18B", "P18L",
                                    "P19B","P19L", "P20B", "P20L"))

# Getting a sample of a Seurat object
scRep_example <- get(data("scRep_example"))
scRep_example <- combineExpression(combined,
                                   scRep_example)

# Simple chord diagram
vizCirclize(scRep_example, group.by = "seurat_clusters")

# Directional chord diagram with arrows
vizCirclize(scRep_example,
            group.by = "seurat_clusters",
            directional = TRUE)

# Multi-level grouping
scRep_example$Patient <- substring(scRep_example$orig.ident, 1, 3)
vizCirclize(scRep_example,
            group.by = c("Patient", "seurat_clusters"))
} # }
```
