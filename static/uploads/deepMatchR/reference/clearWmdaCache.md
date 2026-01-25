# Clear WMDA Cache

Removes the cached WMDA data, causing
[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md)
to revert to using the bundled package data.

## Usage

``` r
clearWmdaCache(cache_dir = NULL, verbose = TRUE)
```

## Arguments

- cache_dir:

  Character. Directory containing cached data. If NULL, uses the default
  cache location.

- verbose:

  Logical. If TRUE (default), print status message.

## Value

Invisibly returns TRUE if cache was cleared, FALSE if no cache existed.

## See also

[`updateWmdaData`](https://www.borch.dev/uploads/deepMatchR/reference/updateWmdaData.md),
[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md)

## Examples

``` r
if (FALSE) { # \dontrun{
# Clear cached WMDA data
clearWmdaCache()
} # }
```
