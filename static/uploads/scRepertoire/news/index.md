# Changelog

## scRepertoire VERSION 2.7.2

### NEW FEATURES

- New
  [`clonalBin()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBin.md)
  function to bin clones by frequency or proportion without requiring a
  single-cell object. Adds `clonalFrequency`, `clonalProportion`, and
  `cloneSize` columns to the output of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md),
  or
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
  Supports custom bin thresholds, optional grouping by metadata
  variable, and chain filtering.
- New
  [`vizCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/vizCirclize.md)
  function for quick chord diagram visualization without manual circlize
  code. Supports directional arrows, custom colors, and sector
  annotations.
- [`getCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/getCirclize.md)
  major enhancements:
  - Multi-level hierarchical grouping via `group.by` accepting a vector
    of columns
  - New `method` parameter: `"unique"`, `"abundance"`, `"jaccard"`,
    `"overlap"`
  - New `symmetric` parameter for directional flow analysis
  - New `include.metadata` parameter returning sector statistics
  - New filtering options: `min.shared`, `top.links`, `filter.sectors`
  - Built-in color palette generation with `palette` parameter
- [`alluvialClones()`](https://www.borch.dev/uploads/scRepertoire/reference/alluvialClones.md)
  major enhancements:
  - New `top.clones`, `min.freq`, `highlight.clones`, and
    `highlight.color` parameters
  - Visual customization: `stratum.width`, `flow.alpha`, `show.labels`,
    `label.size`
  - New `order.strata` parameter for controlling level ordering within
    each stratum
  - Enhanced `export.table` output now includes `freq`, `prop`, and
    `rank` columns
- [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  defaults the clustering call to “IGH” instead of “both”

### API CHANGES

- Soft-deprecated camelCase arguments across all exported functions in
  favor of dot.notation (e.g., `cloneCall` to `clone.call`,
  `exportTable` to `export.table`, `cloneSize` to `clone.size`,
  `filterNA` to `filter.na`, `addLabel` to `add.label`, `clonalSplit` to
  `clonal.split`). All deprecated arguments will continue to work with a
  deprecation warning until version 3.0.0.

### BUG FIXES

- Fixed
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)
  failing with “undefined columns selected” when input data already
  contained `clonalFrequency`/`clonalProportion` columns from a prior
  [`clonalBin()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBin.md)
  call.

## scRepertoire VERSION 2.6.2

### UNDERLYING CHANGES

- Expanded functionality in
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  and
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md):
  - New metrics beyond normalized Levenshtein edit distances
  - Support for raw and normalized-based calculations
  - Support for distance matrices to allow for alignment
- Added support for declaring `chains = "IGL"`, `"IGK"`, or `"Light"` to
  get all light chains in downstream quantification.

### BUG FIXES

- Fixed handling of multiple chains in
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md),
  specifically in formatting CTstrict.

## scRepertoire VERSION 2.6.1

Update to match Bioconductor Release 3.22 on 2025/10/30.

### BUG FIXES

- Fixed `order.by` issue in
  [`positionalProperty()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalProperty.md).
- Fixed individual chain call for
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
- Fixed issue with removing kmer with “;” in
  [`percentKmer()`](https://www.borch.dev/uploads/scRepertoire/reference/percentKmer.md).

## scRepertoire VERSION 2.5.7

### BUG FIXES

- Fixed chain handling for BCR genes in
  [`percentGeneUsage()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  and propagated to wrappers:
  [`percentGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md),
  [`percentVJ()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md),
  and
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md).

## scRepertoire VERSION 2.5.6

### BUG FIXES

- Fixed passing `group.by` for
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).

## scRepertoire VERSION 2.5.5

### UNDERLYING CHANGES

- Updated unit tests for ggplot2 v4.

## scRepertoire VERSION 2.5.3

### BUG FIXES

- Fixed `clonalProportion` calculation to use grouping properly during
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
- Fixed immunarch support for
  [`exportClones()`](https://www.borch.dev/uploads/scRepertoire/reference/exportClones.md)
  TRA/Light chain column handling.

## scRepertoire VERSION 2.5.2

### UNDERLYING CHANGES

- Added support for mouse genes in
  [`quietBCRgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md)
  and
  [`quietTCRgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md).

## scRepertoire VERSION 2.5.1

### UNDERLYING CHANGES

- Introduced pairwise calculations to
  [`StartracDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/StartracDiversity.md).
- Internal function conversion for
  [`clonalSizeDistribution()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalSizeDistribution.md) -
  removed cubature, truncdist, and VGAM from dependencies.
- Increased speed of
  [`clonalSizeDistribution()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalSizeDistribution.md).

## scRepertoire VERSION 2.5.0

### UNDERLYING CHANGES

- Updated and improved code for
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- Consolidated support for discrete AIRR formats under the umbrella of
  AIRR.
- Added `"tcrpheno"` and `"immunarch"` to
  [`exportClones()`](https://www.borch.dev/uploads/scRepertoire/reference/exportClones.md).
- Converted
  [`exportClones()`](https://www.borch.dev/uploads/scRepertoire/reference/exportClones.md)
  to base R to reduce dependencies.
- Added dandelionR and tcrpheno vignettes to pkgdown site.
- [`percentAA()`](https://www.borch.dev/uploads/scRepertoire/reference/percentAA.md)
  refactored to minimize dependencies and use immApex
  [`calculateFrequency()`](https://rdrr.io/pkg/immApex/man/calculateFrequency.html).
- [`positionalEntropy()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalEntropy.md)
  refactored to minimize dependencies and use immApex
  [`calculateEntropy()`](https://rdrr.io/pkg/immApex/man/calculateEntropy.html).
- [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  refactored for performance - now calculates a single diversity metric
  at a time and includes new estimators like `"gini"`, `"d50"`, and
  supports hill numbers.
- [`percentKmer()`](https://www.borch.dev/uploads/scRepertoire/reference/percentKmer.md)
  refactored to use immApex
  [`calculateMotif()`](https://rdrr.io/pkg/immApex/man/calculateMotif.html)
  for both aa and nt sequences. No longer calculates all possible
  motifs, but only motifs present.
- [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  now allows for dual-chain clustering, V/J filtering, normalized or
  straight edit distance calculations, and return of clusters, igraph
  objects, or adjacency matrix.
- [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  offers single/dual chain clustering, aa or nt sequences, adaptive
  filtering of V and J genes, and normalized or straight edit distance
  calculations.
- [`percentGeneUsage()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  is now the underlying function for
  [`percentGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md),
  [`percentVJ()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md),
  and
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  and allows for percent, proportion, and raw count quantification.
- Added common theme (internal `.themeRepertoire()`) to all plots and
  allow users to pass arguments to it.

### BUG FIXES

- [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md)
  issue with plotting a 0 row data frame now errors with message.
- [`clonalScatter()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalScatter.md)
  `group.by`/axes call now works for non-single-cell objects.
- Fixed issue with NULL and “none” `group.by` in
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
- Allowing multi groupings via `x.axis` and `group.by` in
  [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md).

## scRepertoire VERSION 2.3.4

### UNDERLYING CHANGES

- Updated internal `.parseContigs()` to function with more complex
  groupings.
- Added
  [`annotateInvariant()`](https://www.borch.dev/uploads/scRepertoire/reference/annotateInvariant.md)
  functionality for mouse and human TCRs.
- Added
  [`quietTCRgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md),
  [`quietBCRgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md),
  [`quietVDJgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md).
- Fixed issue with
  [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md)
  assertthat statements.
- Started integration with immApex API package.

## scRepertoire VERSION 2.3.2

### BUG FIXES

- Fixed issue with denominator in
  [`getCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/getCirclize.md).
- Fixed chain issue with
  [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md) -
  expanded assertthat statement.

## scRepertoire VERSION 2.2.1

Update for Bioconductor version 3.20.

### NEW FEATURES

- Added support for BCRs for loading ParseBio sequences.
- Added
  [`quietBCRgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md),
  [`quietTCRgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md),
  and
  [`quietVDJgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md)
  for filtering out known TCR and/or BCR gene signatures.

### UNDERLYING CHANGES

- Added `Seurat` to the `Suggests` field in the DESCRIPTION file.

## scRepertoire VERSION 2.0.8

### NEW FEATURES

- Added
  [`getContigDoublets()`](https://www.borch.dev/uploads/scRepertoire/reference/getContigDoublets.md)
  experimental function to identify TCR and BCR doublets as a
  preprocessing step to
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
- Added `proportion` argument to
  [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md)
  so that when set to FALSE, the comparison will be based on frequency
  normalized by per-sample repertoire diversity.

### UNDERLYING CHANGES

- Fixed issue with single chain output for
  [`clonalLength()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalLength.md).
- Removed unnecessary code remnant in
  [`clonalLength()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalLength.md).
- Allow one sample to be plotted by
  [`percentVJ()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md).
- Fixed issue with
  [`positionalProperty()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalProperty.md)
  and `exportTable`.
- Fixed issue with
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md)
  edge case when TRUST4 data only has 1 row.
- Converted documentation to use markdown (roxygen2md).
- Imported `lifecycle`, `purrr`, `withr`.
- Fixed issue with
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  and `exportGraph = TRUE`.
- Improved performance of
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  by a constant factor with C++.
- Restructured functions to `exportTable` before plotting.

## scRepertoire VERSION 2.0.7

### BUG FIXES

- Fixed issue with `group.by` in
  [`clonalOverlap()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOverlap.md).
- Fixed issue with `group.by` in
  [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md).

## scRepertoire VERSION 2.0.6

### BUG FIXES

- Fixed issue with custom column headers for clones.

## scRepertoire VERSION 2.0.5

### UNDERLYING CHANGES

- Added type checks using assertthat.
- Updated conditional statements in `constructConDFAndparseTCR.cpp`.
- Fixed issue in
  [`clonalQuant()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalQuant.md)
  and factor-based `group.by` variable.

## scRepertoire VERSION 2.0.4

### UNDERLYING CHANGES

- [`getCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/getCirclize.md)
  refactored to prevent assumptions and added `include.self` argument.
- Added `.count.clones()` internal function for
  [`getCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/getCirclize.md)
  and
  [`clonalNetwork()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalNetwork.md).
- Added `order.by` parameter to visualizations to specifically call
  order of plotting using a vector or `"alphanumeric"`.
- Fixed issue with
  [`clonalLength()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalLength.md)
  and NA handling.
- [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md)
  now retains the original clonal info if using `relabel.clones`.
- Added Dandelion support to
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md)
  and testthat.
- Fixed issue with
  [`positionalProperty()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalProperty.md)
  assumption that clones will all have 20 amino acids.
- Fixed issue with
  [`positionalProperty()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalProperty.md)
  and removing non-amino acids.
- Fixed IGH/K/L mistaking gene issue in
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md).
- Added error message for NULL results in
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  with `export.graph = TRUE`.
- Fixed issue with “full.clones” missing in
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)
  when using 1 chain.

## scRepertoire VERSION 2.0.3

### UNDERLYING CHANGES

- Modified support for Omniscope format to allow for dual chains.
- Added ParseBio support to
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md)
  and testthat.
- Added support for productive variable to
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md)
  for BD, Omniscope, and Immcantation formats.
- Replaced numerical indexing with name indexing for
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  and
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
  now allow for unproductive contig inclusions with new
  `filterNonproductive` parameter.
- [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  will now prompt user if `samples` is not included instead of erroring.
- Added base threshold by length for internal `.lvCompare()`.
- Ensured internal `.lvCompare()` only looks at first set of sequences
  in multi-sequence chain.
- Fixed bug in exporting graph for
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md).
- Fixed conflict in functions between igraph and dplyr packages.

## scRepertoire VERSION 2.0.2

### BUG FIXES

- [`clonalOccupy()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOccupy.md)
  rewrite counting and NA handling.

## scRepertoire VERSION 2.0.1

### UNDERLYING CHANGES

- [`clonalOverlay()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOverlay.md)
  arguments now `cutpoint` and use `cut.category` to select either
  `clonalProportion` or `clonalFrequency`.

## scRepertoire VERSION 2.0.0 (2024-01-10)

### NEW FEATURES

- Added
  [`percentAA()`](https://www.borch.dev/uploads/scRepertoire/reference/percentAA.md),
  [`percentGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md),
  [`percentVJ()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md),
  [`percentKmer()`](https://www.borch.dev/uploads/scRepertoire/reference/percentKmer.md),
  [`exportClones()`](https://www.borch.dev/uploads/scRepertoire/reference/exportClones.md),
  [`positionalEntropy()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalEntropy.md),
  [`positionalProperty()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalProperty.md).
- Renamed functions: `compareClonotypes` to
  [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md),
  `clonotypeSizeDistribution` to
  [`clonalSizeDistribution()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalSizeDistribution.md),
  `scatterClonotypes` to
  [`clonalScatter()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalScatter.md),
  `quantContig` to
  [`clonalQuant()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalQuant.md),
  `highlightClonotypes` to
  [`highlightClones()`](https://www.borch.dev/uploads/scRepertoire/reference/highlightClones.md),
  `lengthContigs` to
  [`clonalLength()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalLength.md),
  `occupiedscRepertoire` to
  [`clonalOccupy()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOccupy.md),
  `abundanceContig` to
  [`clonalAbundance()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalAbundance.md),
  `alluvialClonotypes` to
  [`alluvialClones()`](https://www.borch.dev/uploads/scRepertoire/reference/alluvialClones.md).
- Added features to
  [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md)
  to allow for highlighting sequences and relabeling clonotypes.

### UNDERLYING CHANGES

- Removed internal `.quiet()` function.
- `.theCall()` now allows for a custom header/variable and checks the
  colnames.
- Replaced data arguments to be more descriptive: `df` to `input.data`,
  `dir` to `input`, `sc` to `sc.data`.
- Deep clean on documentation for increased consistency and
  explainability.
- [`StartracDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/StartracDiversity.md)
  metric re-implemented to remove startrac-class object intermediary.
- Implemented powerTCR locally to reduce dependencies and continue
  support.
- Universalized underlying function language and intermediate variables.
- License change to MIT.
- `group.by` and `split.by` consolidated into single `group.by`
  parameter.
- Added support for Immcantation pipeline, .json, Omniscope, and MiXCR
  formats for
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- Made GitHub.io website for support/vignettes/FAQ.
- Added testthat for all exported and internal functions.
- Fixed issue with
  [`clonalQuant()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalQuant.md)
  for instance of `scale = FALSE` and `group.by` being set.
- [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  no longer automatically orders samples.
- Removed `order` parameter from
  [`clonalQuant()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalQuant.md),
  [`clonalLength()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalLength.md),
  and
  [`clonalAbundance()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalAbundance.md).
- `x.axis` parameter in
  [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  separated from `group.by` parameter.
- Filtering chains will not eliminate non-matching chains.

### DEPRECATED AND DEFUNCT

- Deprecated `stripBarcodes()`.
- Deprecated
  [`expression2List()`](https://www.borch.dev/uploads/scRepertoire/reference/expression2List.md)
  (now only an internal function).
- Deprecated `checkContigs()`.

## scRepertoire VERSION 1.11.0

- Rebasing for Bioconductor version.

## scRepertoire VERSION 1.7.5

- Fixed
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  to allow for non-related sequences.

## scRepertoire VERSION 1.7.4

### NEW FEATURES

- `checkContigs()` function to quantify the percentages of NA values by
  genes or sequences.
- `exportClones` to
  [`clonalNetwork()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalNetwork.md)
  to isolate clones shared across identities.

### UNDERLYING CHANGES

- Fixed issue with
  [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  and skipping boots.
- Fixed underlying assumptions with
  [`clonalBias()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBias.md).
- Added reads variable to `parseAIRR`.
- Fixed handling of samples parameter in combine functions.
- Removed need to relevel the cloneType factor after
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
- Set up [`lapply()`](https://rdrr.io/r/base/lapply.html) for
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  and `clusterTCR()` - no more pairwise distance matrix calculation.
- [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md)
  support for data.frames or lists of contigs.
- Added examples for
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- Removed requirement for T cell type designation - will combine A/B and
  G/D simultaneously.
- Updated
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  to chunk nucleotide edit distance calculations by V gene and give
  option to skip edit distance calculation with
  `call.related.clones = FALSE`.
- Updated `clusterTCR()` to use `lvCompare()` and base edit distances on
  V gene usage.

## scRepertoire VERSION 1.7.3

### UNDERLYING CHANGES

- Fixed misspellings for parse functions.
- Optimized WAT3R and 10x
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- Removed `combineTRUST4` - superseded by
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- Added support of TRUST4 for
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).
- Added support for BD in
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md)
  TRUST4 parsing allows for all NA values in a chain.
- [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)
  `group.by = NULL` will now collapse the whole list.

## scRepertoire VERSION 1.7.2

### UNDERLYING CHANGES

- [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  now has `skip.boots` to stop bootstrapping and downsampling.

## scRepertoire VERSION 1.7.0

### UNDERLYING CHANGES

- Rebumping the version change with new release of Bioconductor.
- Added mean call to the heatmap of
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md).
- `filteringMulti` in `combineTCR` now checks to remove list elements
  with 0 cells.
- Removed [`top_n()`](https://dplyr.tidyverse.org/reference/top_n.html)
  call (deprecated), using
  [`slice_max()`](https://dplyr.tidyverse.org/reference/slice.html)
  without ties.
- Added
  [`arrange()`](https://dplyr.tidyverse.org/reference/arrange.html) call
  during `parseTCR()` to organize the chains.
- Corrected the gd flip in combine functions.
- Removed viridis call in
  [`clonalNetwork()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalNetwork.md)
  that was leading to errors.
- Matched syntax for strict clonotype in
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).
- Added `group.by` variable to all applicable visualizations.
- Added `return.boots` to
  [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  to allow export of all bootstrapped values.

## scRepertoire VERSION 1.5.4

### BUG FIXES

- Modified `grabMeta()` internal function to no longer assume the active
  identity is clusters.
- `checkBlanks()` now checks if a blank was detected before trying to
  remove it.
- [`clonalNetwork()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalNetwork.md)
  automatically resulted in default error message - bug now removed.
- [`clonalBias()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBias.md)
  now adds z-score of bias when matrix is exported. `exportTable`
  parameter is now fixed.

## scRepertoire VERSION 1.5.3

### UNDERLYING CHANGES

- Added
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md)
  for non-10X formatted single-cell data.
- Removed `combineTRUST4`, superseded by
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
  now allows for \> 3 recovered TCRs per barcode.
- Re-added filtering steps to
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
  will detect if data is from 10X and automatically remove nonproductive
  or multi chains.
- Updated `parseTCR()` to include evaluation for gamma/delta chains.

## scRepertoire VERSION 1.5.2

### UNDERLYING CHANGES

- [`highlightClones()`](https://www.borch.dev/uploads/scRepertoire/reference/highlightClones.md)
  now returns the specific clones instead of clonotype 1, etc.
- [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md)
  `numbers` parameter now for group-wide numbers and not overall top X
  numbers.
- Fixed issue with
  [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  that caused errors when `group.by` parameter was used.
- Modified `parseBCR()` to reduce complexity and assume lambda \>\>
  kappa.
- Fixed
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  function broken with Seurat Objects.
- `checkContigs` now ensures data frames and that “” are converted into
  NAs.
- Modified `makeGenes()` internal function changing `na.omit` to
  [`str_replace_na()`](https://stringr.tidyverse.org/reference/str_replace_na.html)
  and separating the BCR calls by chain to prevent combination errors.

## scRepertoire VERSION 1.3.5

### UNDERLYING CHANGES

- Modified `parseBCR()` to check for contents of the chains. Resolved
  issue with placing light chain into heavy chain slots when 2 contigs
  are present.
- Updated `checkBlanks()` to include NA evaluation and placed the check
  in all viz functions.
- Added
  [`clonalNetwork()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalNetwork.md)
  function.
- Modified diversity visualization to remove outliers and place graphs
  on a single line.
- Modified
  [`clonalOverlay()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOverlay.md)
  to use new internal `getCoord()` function like
  [`clonalNetwork()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalNetwork.md).
- Added `threshold` parameter to
  [`clonalSizeDistribution()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalSizeDistribution.md).
- Added support for single-cell objects to
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md).

## scRepertoire VERSION 1.3.4

### UNDERLYING CHANGES

- Modified
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  and
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  to speed up comparison and use less memory.
- `filteringMulti` now isolates the top contig by chain, then for
  barcodes with chains \> 2, isolates the top expressing chains.
- Modified `makeGenes()` internal function to use
  [`str_c()`](https://stringr.tidyverse.org/reference/str_c.html).
- Added `threshold` parameter to `combineTRUST4` for B cell
  manipulation.
- Changed `combineTCR` function to prevent cell type mix up.
- [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  can now look at other component genes of the receptor and `separate`
  parameter replaced by `y.axis`.
- Added
  [`clonalBias()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBias.md)
  function for inter-cluster comparison.
- Fixed
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  and
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  assumption that you will have unrelated clones.

## scRepertoire VERSION 1.3.3

### UNDERLYING CHANGES

- [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  auto naming function updated to actually name the list elements.
- Added
  [`createHTOContigList()`](https://www.borch.dev/uploads/scRepertoire/reference/createHTOContigList.md)
  function to create contig list of multiplexed experiments. Fixed issue
  with `groupBy` variable.
- Added Inverse Pielou metric to diversity call.
- Added `include.na` and `split.by` to
  [`clonalOccupy()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOccupy.md)
  and changed labeling depending on frequency vs proportion.
- Added support for single-cell objects for most visualizations, list
  organizing by single-cell object can be called using `split.by`
  variable.
- All `group` and `groupBy` parameters are now `group.by`.

## scRepertoire VERSION 1.3.2

### UNDERLYING CHANGES

- Added `dot.size` parameter to
  [`clonalScatter()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalScatter.md).
- `filteringMulti` now subsets clonotypes with contigs \>= 2, to prevent
  2 of the same chains.
- Changed how coldata is added to SCE objects using merge instead of
  union.
- Can now add BCR and TCR simultaneously by making large list.
- Scatter plotting code allows for user to select `dot.size` as a
  variable on the x or y axis.
- Removed `regressClonotype` function - too many dependencies required.
- Added `chain` option to visualizations and
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)
  to allow users to facilitate single chains - removed `chain` option
  from `combineTCR`/`combineBCR`/`combineTRUST4`.
- Added NA filter to `combineTCR`/`combineBCR`/`combineTRUST4` for cell
  barcodes with only NA values.
- Added NA filter to
  [`expression2List()`](https://www.borch.dev/uploads/scRepertoire/reference/expression2List.md)
  for cells with NA clonotypes.
- Updated
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  to order genes automatically by highest to lowest variance.
- Updated
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  to pull the correct genes based on selection.
- Updated parse method for V/J/D placement in TRB/Heavy chains.
- Simplified
  [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  to allow for more options in organizing plot and box plots.
- [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)
  adds the `groupBy` variable to Frequency, allowing for multiple
  calculations to be saved in the meta data.

## scRepertoire VERSION 1.2.3

### UNDERLYING CHANGES

- Changed the access of the sample data to github.io repo.

## scRepertoire VERSION 1.2.2

### DEPRECATED AND DEFUNCT

- Removed Startrac-based functions to pass build on Bioconductor.
- Deprecated
  [`StartracDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/StartracDiversity.md).

## scRepertoire VERSION 1.2.0

### UNDERLYING CHANGES

- Added support for `SingleCellExperiment` format.

### DEPRECATED AND DEFUNCT

- Deprecated `combineSeurat` in favor of
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
- Deprecated `seurat2List` in favor of
  [`expression2List()`](https://www.borch.dev/uploads/scRepertoire/reference/expression2List.md).

## scRepertoire VERSION 1.1.4

### NEW FEATURES

- Added `proportion` to
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)
  function.
- Added
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  and
  [`clonalOverlay()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOverlay.md)
  functions.

### UNDERLYING CHANGES

- Replaced `hammingCompare` with `lvCompare` to enable superior
  clonotype calling in
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).
- Added downsampling to diversity calculations.
- Fixed Clonal Overlap Coefficient issue - was comparing unique barcodes
  and not clonotypes.
- Added `checkBlanks()` function to remove list elements without
  clonotypes.
- Re-added Startrac metrics by stripping down the package.
- Heavily modified dependencies to reduce total number.

## scRepertoire VERSION 1.0.0

### UNDERLYING CHANGES

- Removed dependencies ggfittext and ggdendrogram.
- [`clonalSizeDistribution()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalSizeDistribution.md)
  now returns a [`plot()`](https://rdrr.io/r/graphics/plot.default.html)
  function.

## scRepertoire VERSION 0.99.0

- Initial Bioconductor submission.
- Added
  [`getCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/getCirclize.md),
  `exportTable` to visualization functions.
- Added `screp_example` data to package.
- Added
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  function and support for monocle in
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
