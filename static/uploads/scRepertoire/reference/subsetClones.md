# Subset The Product of combineTCR() or combineBCR()

This function allows for the subsetting of the product of
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
or
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
by the name of the individual list element.

## Usage

``` r
subsetClones(input.data, name, variables = NULL)
```

## Arguments

- input.data:

  The product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
  or
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).

- name:

  The column header/name to use for subsetting.

- variables:

  The values to subset by, must be in the in the variable.

## Value

list of contigs that have been filtered for the name parameter

## Examples

``` r
combined <- combineTCR(contig_list, 
                        samples = c("P17B", "P17L", "P18B", "P18L", 
                                    "P19B","P19L", "P20B", "P20L"))
subset <- subsetClones(combined, name = "sample", variables = c("P17B"))
```
