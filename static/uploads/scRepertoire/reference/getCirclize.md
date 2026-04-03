# Generate Data Frame to Plot Chord Diagram

This function will take the meta data from the product of
[`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)
and generate a relational data frame to be used for a chord diagram.
Each chord will represent the number of clones unique and shared across
the multiple `group.by` variable. If using the downstream circlize R
package, please read and cite the following
[manuscript](https://pubmed.ncbi.nlm.nih.gov/24930139/). If looking for
more advanced ways for circular visualizations, there is a great
[cookbook](https://jokergoo.github.io/circlize_book/book/) for the
circlize package.

## Usage

``` r
getCirclize(
  sc.data,
  clone.call = NULL,
  group.by = NULL,
  method = c("unique", "abundance", "jaccard", "overlap"),
  proportion = FALSE,
  symmetric = TRUE,
  include.self = TRUE,
  include.metadata = FALSE,
  min.shared = 0,
  top.links = NULL,
  filter.sectors = NULL,
  palette = "inferno",
  cloneCall = NULL
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
  grouping) in the metadata to group the analysis by (e.g., "sample",
  "treatment"). If `NULL`, data will be analyzed by active identity.
  When multiple columns are provided, they are combined with "\_"
  separator for multi-level annotations.

- method:

  The method for calculating link values: `"unique"` (default) counts
  unique shared clones, `"abundance"` sums clone frequencies,
  `"jaccard"` calculates Jaccard similarity, `"overlap"` calculates
  overlap coefficient.

- proportion:

  Calculate the relationship by unique clones (`FALSE`, default) or
  normalized by proportion (`TRUE`).

- symmetric:

  If `TRUE` (default), returns symmetric relationships. If `FALSE`,
  returns directional flow showing proportion of source's clones found
  in destination.

- include.self:

  Include counting the clones within a single group.by comparison.

- include.metadata:

  If `TRUE`, returns a list with links data frame and sector-level
  metadata including cell counts, clone counts, and expansion metrics.

- min.shared:

  Minimum number of shared clones to include a link (default 0).

- top.links:

  Keep only the top N links by value. If `NULL` (default), keep all.

- filter.sectors:

  Character vector of sectors to include. If `NULL`, include all.

- palette:

  Colors to use for sector color suggestions - input any hcl.pals.

- cloneCall:

  **\[deprecated\]** Use `clone.call` instead.

## Value

A data frame of shared clones between groups formatted for
[chordDiagram](https://rdrr.io/pkg/circlize/man/chordDiagram.html). If
`include.metadata = TRUE`, returns a list with `links` (the edge data
frame), `sectors` (sector-level statistics), and `colors` (suggested
colors for each sector).

## Author

Dillon Corvino, Nick Borcherding

## Examples

``` r
# Getting the combined contigs
combined <- combineTCR(contig_list,
                        samples = c("P17B", "P17L", "P18B", "P18L",
                                    "P19B","P19L", "P20B", "P20L"))

# Getting a sample of a Seurat object
scRep_example <- get(data("scRep_example"))
scRep_example <- combineExpression(combined,
                                   scRep_example)

# Getting data frame output for Circlize
circles <- getCirclize(scRep_example,
                       group.by = "seurat_clusters")

# Multi-level grouping for hierarchical chord diagrams
scRep_example$Patient <- substring(scRep_example$orig.ident, 1, 3)
circles <- getCirclize(scRep_example,
                       group.by = c("Patient", "seurat_clusters"))

# Get rich output with sector metadata
result <- getCirclize(scRep_example,
                      group.by = "seurat_clusters",
                      include.metadata = TRUE)
```
