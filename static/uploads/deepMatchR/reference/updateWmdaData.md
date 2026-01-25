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
if (FALSE) { # \dontrun{
# Update to latest WMDA data
updateWmdaData()

# Update to a specific version
updateWmdaData(version = "3.54.0")

# Force re-download
updateWmdaData(force = TRUE)
} # }
```
