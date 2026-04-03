# Highlighting Specific Clones

Use a specific clonal sequence to highlight on top of the dimensional
reduction in single-cell object.

## Usage

``` r
highlightClones(sc.data, clone.call = NULL, sequence = NULL, cloneCall = NULL)
```

## Arguments

- sc.data:

  The single-cell object to attach after
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md)

- clone.call:

  Defines the clonal sequence grouping. Accepted values are: `gene`
  (VDJC genes), `nt` (CDR3 nucleotide sequence), `aa` (CDR3 amino acid
  sequence), or `strict` (VDJC + nt). A custom column header can also be
  used.

- sequence:

  The specific sequence or sequence to highlight

- cloneCall:

  **\[deprecated\]** Use `clone.call` instead.

## Value

Single-cell object object with new meta data column for indicated clones

## Examples

``` r
# Getting the combined contigs
combined <- combineTCR(contig_list, 
                        samples = c("P17B", "P17L", "P18B", "P18L", 
                                    "P19B","P19L", "P20B", "P20L"))

# Getting a sample of a Seurat object
scRep_example  <- get(data("scRep_example"))

# Using combineExpresion()
scRep_example  <- combineExpression(combined, 
                                    scRep_example)

# Using highlightClones()
scRep_example   <- highlightClones(scRep_example,
                                   clone.call= "aa",
                                   sequence = c("CVVSDNTGGFKTIF_CASSVRRERANTGELFF"))
```
