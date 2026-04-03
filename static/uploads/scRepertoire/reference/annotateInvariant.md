# Annotate invariant T cells (MAIT or iNKT) in single-cell TCR data

The `annotateInvariant()` function identifies potential
mucosal-associated invariant T
(``` MAIT``) cells or invariant natural killer T ( ```iNKT\`) cells from
single-cell sequencing datasets based on their characteristic TCR usage.
It extracts TCR chain information from the provided single-cell data,
checks it against known invariant T-cell receptor criteria for either
MAIT or iNKT cells, and returns a score indicating the presence (1) or
absence (0) of these invariant cell populations for each individual
cell. The function supports data from mouse and human samples, providing
a convenient method to annotate specialized T-cell subsets within
single-cell analyses.

## Usage

``` r
annotateInvariant(
  input.data,
  type = c("MAIT", "iNKT"),
  species = c("mouse", "human")
)
```

## Arguments

- input.data:

  The product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
  or
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).

- type:

  Character specifying the type of invariant cells to annotate (`MAIT`
  or `iNKT`).

- species:

  Character specifying the species ('mouse' or 'human').

## Value

A single-cell object or list with the corresponding annotation scores (0
or 1) added.

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

# Using annotateInvariant()
annotateInvariant(input.data = scRep_example, type = "MAIT", species = "human")
#> An object of class Seurat 
#> 2000 features across 500 samples within 1 assay 
#> Active assay: RNA (2000 features, 2000 variable features)
#>  2 layers present: counts, data
#>  1 dimensional reduction calculated: umap
annotateInvariant(input.data = scRep_example, type = "iNKT", species = "human")
#> An object of class Seurat 
#> 2000 features across 500 samples within 1 assay 
#> Active assay: RNA (2000 features, 2000 variable features)
#>  2 layers present: counts, data
#>  1 dimensional reduction calculated: umap
```
