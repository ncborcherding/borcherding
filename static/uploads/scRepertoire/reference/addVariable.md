# Adding Variables After combineTCR() or combineBCR()

This function adds variables to the product of
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
or
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
to be used in later visualizations. For each element, the function will
add a column (labeled by `variable.name`) with the variable. The length
of the `variables` parameter needs to match the length of the combined
object.

## Usage

``` r
addVariable(input.data, variable.name = NULL, variables = NULL)
```

## Arguments

- input.data:

  The product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
  or
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).

- variable.name:

  A character string that defines the new variable to add.

- variables:

  A character vector defining the desired column value for each list
  element. Must match the length of the product of
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
  or
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).

## Value

input.data list with the variable column added to each element.

## Examples

``` r
combined <- combineTCR(contig_list, 
                       samples = c("P17B", "P17L", "P18B", "P18L", 
                                    "P19B","P19L", "P20B", "P20L"))
combined <- addVariable(combined, 
                        variable.name = "Type", 
                        variables = rep(c("B", "L"), 4))
```
