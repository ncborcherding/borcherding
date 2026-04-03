# **DEPRECATED** Take the meta data in seurat/SCE and place it into a list

**\[deprecated\]**

Allows users to perform more fundamental measures of clonotype analysis
using the meta data from the seurat or SCE object. For Seurat objects
the active identity is automatically added as "cluster". Remaining
grouping parameters or SCE or Seurat objects must appear in the meta
data.

This function is deprecated as of version 2 due to the confusion it
caused to many users. Users are encouraged to remain with the
abstraction barrier of combined single cell objects and the outputs of
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
and
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
for all functions.

We discourage the use of this function, but if you have to use it, set
the `force` argument to `TRUE`.

## Usage

``` r
expression2List(sc, ..., force = FALSE)
```

## Arguments

- sc:

  output of
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).

- ...:

  previously the `group` or `split.by` argument, indicating the column
  header to group the new list by. This should strictly be one argument
  and is an ellipsis for backwards compatibility. Everything after the
  first argument is ignored.

- force:

  logical. If not `TRUE` (default), a deprecation error will be thrown.
  Otherwise the function will run but not guaranteed to be stable.

## Value

list derived from the meta data of single-cell object with elements
divided by the group parameter
