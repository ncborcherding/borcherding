# Example SAB (Class I/II) and PRA Panels

A small, fixed-format example object demonstrating the input structure
used by this package’s utilities for single antigen bead (SAB) Class I /
Class II and panel reactive antibody (PRA) data. Useful for examples,
vignettes, and unit tests without requiring PHI or proprietary vendor
exports.

## Usage

``` r
data(deepMatchR_example)
```

## Format

A named list of length 3 containing data frames as described above.

## Details

**Structure:** a named list of length 3:

- `ClassI_example`: data frame with columns `BeadID` (\`integer\`),
  `SpecAbbr` (\`character\`, antigen abbreviations), `Specificity`
  (\`character\`, comma-delimited allele list), `NormalValue`
  (\`numeric\`, normalized MFI or vendor-provided normalization),
  `RawData` (\`numeric\`, raw MFI), `CountValue` (\`integer\`,
  bead/event count).

- `ClassII_example`: same schema as Class I, but for class II
  specificities (e.g., DR, DQ, DP).

- `PRA`: data frame with columns `BeadID` (\`integer\`), `SpecAbbr`
  (\`character\`), `Specificity` (\`character\`), `NormalValue`
  (\`numeric\` or \`NA\`), `RawData` (\`numeric\`), `CountValue`
  (\`integer\`).

**Notes:** - Column names are kept vendor-agnostic but mimic common
exports. - `SpecAbbr` values are comma-separated antigen abbreviations
with padding dashes, e.g., \`"A2,-,-,-,..."\`. - `Specificity` values
are comma-separated IMGT/HLA alleles aligned to the abbreviations in
`SpecAbbr`. - `NormalValue` may be `NA` when not supplied by the
instrument export or when illustrative only.

## See also

[`deepMatchR_eplets`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_eplets.md),
[`deepMatchR_cregs`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_cregs.md)
