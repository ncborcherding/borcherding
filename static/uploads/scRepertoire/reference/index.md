# Package index

## Loading and Processing Contigs

Functions that load, combine, and process the single-cell contig
information.

- [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md)
  : Load Immune Receptor Sequencing Contigs
- [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
  : Combine T Cell Receptor Contig Data
- [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
  : Combine B Cell Receptor Contig Data
- [`clonalBin()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBin.md)
  : Bin Clones by Frequency or Proportion
- [`addVariable()`](https://www.borch.dev/uploads/scRepertoire/reference/addVariable.md)
  : Adding Variables After combineTCR() or combineBCR()
- [`subsetClones()`](https://www.borch.dev/uploads/scRepertoire/reference/subsetClones.md)
  : Subset The Product of combineTCR() or combineBCR()
- [`exportClones()`](https://www.borch.dev/uploads/scRepertoire/reference/exportClones.md)
  : Export Clonal Data in Various Formats
- [`createHTOContigList()`](https://www.borch.dev/uploads/scRepertoire/reference/createHTOContigList.md)
  : Deconvolute Contig Information from Multiplexed Experiments
- [`getContigDoublets()`](https://www.borch.dev/uploads/scRepertoire/reference/getContigDoublets.md)
  **\[experimental\]** : Get Contig Doublets
- [`annotateInvariant()`](https://www.borch.dev/uploads/scRepertoire/reference/annotateInvariant.md)
  : Annotate invariant T cells (MAIT or iNKT) in single-cell TCR data

## Visualizing Clones

Functions for visualizing clonal data across samples and groups.

- [`clonalAbundance()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalAbundance.md)
  : Plot the Relative Abundance of Clones
- [`clonalCompare()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCompare.md)
  : Compare Clonal Abundance Across Variables
- [`clonalDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalDiversity.md)
  : Calculate Clonal Diversity
- [`clonalHomeostasis()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalHomeostasis.md)
  : Plot Clonal Homeostasis of the Repertoire
- [`clonalLength()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalLength.md)
  : Plot the Distribution of Sequence Lengths
- [`clonalOverlap()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOverlap.md)
  : Examining the clonal overlap between groups or samples
- [`clonalProportion()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalProportion.md)
  : Plot the Clonal Space Occupied by Specific Clones
- [`clonalQuant()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalQuant.md)
  : Plot Number or Proportions of Clones
- [`clonalRarefaction()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalRarefaction.md)
  : Calculate rarefaction based on the abundance of clones
- [`clonalScatter()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalScatter.md)
  : Scatter Plot Comparing Clones Across Two Samples
- [`clonalSizeDistribution()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalSizeDistribution.md)
  : Plot powerTCR Clustering Based on Clonal Size
- [`percentGeneUsage()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  [`percentGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  [`percentVJ()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  : Summarizes and Visualizes Gene Usage

## Summarizing Repertoire

Functions to summarize clonal sequences across the repertoire.

- [`percentGeneUsage()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  [`vizGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  [`percentGenes()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  [`percentVJ()`](https://www.borch.dev/uploads/scRepertoire/reference/percentGeneUsage.md)
  : Summarizes and Visualizes Gene Usage
- [`percentAA()`](https://www.borch.dev/uploads/scRepertoire/reference/percentAA.md)
  : Plot Relative Amino Acid Composition by Position
- [`percentKmer()`](https://www.borch.dev/uploads/scRepertoire/reference/percentKmer.md)
  : Analyze K-mer Motif Composition
- [`positionalEntropy()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalEntropy.md)
  : Examining the Diversity of Amino Acids by Position
- [`positionalProperty()`](https://www.borch.dev/uploads/scRepertoire/reference/positionalProperty.md)
  : Plot Positional Physicochemical Property Analysis

## Clustering and Similarity

Functions for clustering clones by sequence similarity.

- [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  : Cluster clones by sequence similarity

## Single-Cell Object Visualizations

Functions to add or visualize clonal information along a single-cell
object.

- [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)
  : Adding Clonal Information to Single-Cell Object
- [`alluvialClones()`](https://www.borch.dev/uploads/scRepertoire/reference/alluvialClones.md)
  : Alluvial Plotting for Single-Cell Object
- [`clonalBias()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBias.md)
  : Calculate Clonal Bias Towards a Cluster or Compartment
- [`clonalNetwork()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalNetwork.md)
  : Visualize Clonal Network in Dimensional Reductions
- [`clonalOccupy()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOccupy.md)
  : Plot cloneSize by Variable in Single-Cell Objects
- [`clonalOverlay()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalOverlay.md)
  : Visualize Distribution of Clonal Frequency
- [`getCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/getCirclize.md)
  : Generate Data Frame to Plot Chord Diagram
- [`vizCirclize()`](https://www.borch.dev/uploads/scRepertoire/reference/vizCirclize.md)
  : Visualize Clonal Relationships as a Chord Diagram
- [`highlightClones()`](https://www.borch.dev/uploads/scRepertoire/reference/highlightClones.md)
  : Highlighting Specific Clones
- [`StartracDiversity()`](https://www.borch.dev/uploads/scRepertoire/reference/StartracDiversity.md)
  : Calculate Startrac-based Diversity Indices

## Utilities

Helper functions for filtering gene signatures and converting data.

- [`quietVDJgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md)
  [`quietTCRgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md)
  [`quietBCRgenes()`](https://www.borch.dev/uploads/scRepertoire/reference/quietVDJgenes.md)
  : Remove TCR and BCR genes from variable gene results

- [`expression2List()`](https://www.borch.dev/uploads/scRepertoire/reference/expression2List.md)
  **\[deprecated\]** :

  **DEPRECATED** Take the meta data in seurat/SCE and place it into a
  list

## Data

Reference data for package functions.

- [`contig_list`](https://www.borch.dev/uploads/scRepertoire/reference/contig_list.md)
  : A List of Eight Single-cell TCR Sequencing Runs.
- [`scRep_example`](https://www.borch.dev/uploads/scRepertoire/reference/scRep_example.md)
  : A Seurat Object of 500 Single T cells,
