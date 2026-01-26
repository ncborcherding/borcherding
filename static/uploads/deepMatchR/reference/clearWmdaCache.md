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
# Check if cache exists (safe operation, no side effects)
cache_dir <- file.path(tempdir(), "wmda_cache_test")
# This will report "No WMDA cache found" since we use a temp directory
clearWmdaCache(cache_dir = cache_dir)
#> No WMDA cache found

# \donttest{
# Clear the default WMDA cache
clearWmdaCache()
#> No WMDA cache found
# }
```
