# Clear Sequence Cache

Utility function to clear the sequence cache, either in-memory or
filesystem-based.

## Usage

``` r
clearSequenceCache(cache_dir = NULL, type = NULL)
```

## Arguments

- cache_dir:

  If provided, clears the filesystem cache at this location. If NULL,
  clears the in-memory cache for the current session.

- type:

  If provided, only clears cache entries for this sequence type.
  Options: "PROT", "NUC", or NULL for all types.

## Value

Invisible NULL

## Examples

``` r
# Clear in-memory cache
clearSequenceCache()
#> Note: In-memory cache clearing requires restarting R session or re-sourcing functions

# Clear filesystem cache
clearSequenceCache(cache_dir = "~/.hla_cache")
#> Cache directory does not exist
```
