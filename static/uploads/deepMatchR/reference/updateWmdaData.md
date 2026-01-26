# Update WMDA Nomenclature Data

Downloads fresh WMDA nomenclature data from the IMGT/HLA GitHub
repository and caches it locally for use by
[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md).

## Usage

``` r
updateWmdaData(
  version = "Latest",
  cache_dir = NULL,
  force = FALSE,
  verbose = TRUE
)
```

## Arguments

- version:

  Character. The IMGT/HLA version to download. Default is "Latest" for
  the most recent release. Can also be a specific version tag (e.g.,
  "3.54.0").

- cache_dir:

  Character. Directory to store cached data. If NULL (default), uses the
  package's default cache location.

- force:

  Logical. If TRUE, re-download even if cached data exists.

- verbose:

  Logical. If TRUE (default), print progress messages.

## Value

Invisibly returns the path to the cache directory.

## Details

The WMDA nomenclature files are downloaded from:
<https://github.com/ANHIG/IMGTHLA>

Downloaded files:

- `rel_dna_ser.txt`: DNA to serology mappings

- `rel_ser_ser.txt`: Broad to split relationships

- `hla_nom_p.txt`: P-group definitions

The cache is stored as a single RDS file for fast loading. To clear the
cache and revert to bundled data, delete the cache directory or set the
environment variable `DEEPMATCHR_CACHE_DIR` to a new location.

## See also

[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md)

## Examples

``` r
# Show default cache directory (does not download)
cache_dir <- file.path(tempdir(), "wmda_test")
print(cache_dir)
#> [1] "/var/folders/5t/9wp2ssj13r7btc7fjmg4m68r0000gn/T//RtmpW7Z2q3/wmda_test"

# \donttest{
# Update to latest WMDA data (requires internet)
updateWmdaData()
#> Downloading WMDA data (version: Latest)...
#>   Downloading rel_dna_ser.txt...
#>   Downloading rel_ser_ser.txt...
#>   Downloading hla_nom_p.txt...
#>   Saving to cache...
#> Done! Cached 27260 serology mappings, 23 split mappings, 18757 P-groups
#> Cache location: ~/Library/Caches/deepMatchR

# Force re-download even if cache exists
updateWmdaData(force = TRUE)
#> Downloading WMDA data (version: Latest)...
#>   Downloading rel_dna_ser.txt...
#>   Downloading rel_ser_ser.txt...
#>   Downloading hla_nom_p.txt...
#>   Saving to cache...
#> Done! Cached 27260 serology mappings, 23 split mappings, 18757 P-groups
#> Cache location: ~/Library/Caches/deepMatchR
# }
```
