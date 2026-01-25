# WMDA Broad-to-Split Antigen Relationships

A lookup table mapping broad serological antigens to their split
antigens based on WMDA nomenclature. Used internally by
[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md)
when `resolve_splits = TRUE`.

## Usage

``` r
data(deepMatchR_wmda_splits)
```

## Format

A data.table with the following columns:

- locus:

  \`character\`. Serology locus prefix (e.g., \`"A"\`, \`"B"\`,
  \`"DR"\`).

- broad:

  \`character\`. Broad antigen number (e.g., \`"2"\`, \`"5"\`).

- splits:

  \`character\`. Pipe-separated split antigen numbers (e.g.,
  \`"15\|16"\`).

## Source

WMDA nomenclature files from IMGT/HLA GitHub repository
(<https://github.com/ANHIG/IMGTHLA/tree/Latest/wmda>).

## Details

Common examples of broad-to-split relationships:

- DR2 -\> DR15, DR16

- DR5 -\> DR11, DR12

- B5 -\> B51, B52

## See also

[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md),
[`deepMatchR_wmda_serology`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_wmda_serology.md)
