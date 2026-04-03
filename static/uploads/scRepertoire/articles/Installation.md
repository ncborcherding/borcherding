# Installation Instructions for scRepertoire

## GitHub (Development Branch)

`scRepertoire` is an active project with frequent updates based on user
feedback. The most up-to-date version is available via GitHub and can be
installed using
[`devtools::install_github()`](https://remotes.r-lib.org/reference/install_github.html)
or
[`remotes::install_github()`](https://remotes.r-lib.org/reference/install_github.html).

[immApex](https://github.com/BorchLab/immApex) is a required dependency
for the underlying processes of `scRepertoire`. Ensure both are called
during installation if not using Bioconductor.

    remotes::install_github(c("BorchLab/immApex", "BorchLab/scRepertoire@devel"))

## Bioconductor (Stable Release)

The current stable version of `scRepertoire` is also available through
[Bioconductor](https://www.bioconductor.org/packages/release/bioc/html/scRepertoire.html).
This will automatically install all dependencies including `immApex`.

    if (!require("BiocManager", quietly = TRUE))
        install.packages("BiocManager")

    BiocManager::install("scRepertoire")

## Verifying Installation

After installation, confirm everything is working:

    library(scRepertoire)

    # Check version
    packageVersion("scRepertoire")

    # Quick test with built-in data
    data("contig_list")
    combined <- combineTCR(contig_list,
                           samples = c("P17B", "P17L", "P18B", "P18L",
                                       "P19B", "P19L", "P20B", "P20L"))

If this runs without errors, you are ready to go.

## Troubleshooting

### Bioconductor Version Mismatch

If you see errors about package versions being incompatible, ensure your
Bioconductor installation is up to date:

    BiocManager::install(version = "release")
    BiocManager::valid()

### Compilation Errors (Rcpp)

`scRepertoire` includes C++ code via Rcpp. If you encounter compilation
errors:

- **macOS**: Ensure Xcode command line tools are installed:
  `xcode-select --install`
- **Windows**: Install
  [Rtools](https://cran.r-project.org/bin/windows/Rtools/)
- **Linux**: Ensure `r-base-dev` or equivalent is installed

### Legacy Version 1

If you need the original version 1 of scRepertoire:

    devtools::install_github("BorchLab/scRepertoire@v1")

## Release Notes

A full copy of the changes in each version can be found in the
[NEWS/ChangeLog](https://borch.dev/uploads/scRepertoire/news/index.html).

## Next Steps

- [Loading Data into
  scRepertoire](https://www.borch.dev/uploads/scRepertoire/articles/Loading.md) -
  Learn how to load contig data from 10x, AIRR, and other formats.
- [Combining Contigs into
  Clones](https://www.borch.dev/uploads/scRepertoire/articles/Combining_Contigs.md) -
  Process contigs into clonal definitions with
  [`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
  and
  [`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).
