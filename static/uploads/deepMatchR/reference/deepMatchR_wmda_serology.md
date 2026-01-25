# WMDA DNA-to-Serology Mapping

A lookup table mapping HLA alleles to their serological equivalents
based on WMDA (World Marrow Donor Association) nomenclature. Used
internally by
[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md)
for allele-to-serology conversion.

## Usage

``` r
data(deepMatchR_wmda_serology)
```

## Format

A data.table with the following columns:

- locus:

  \`character\`. HLA locus with asterisk (e.g., \`"A\*"\`, \`"B\*"\`,
  \`"DRB1\*"\`).

- allele_2f:

  \`character\`. Two-field allele designation (e.g., \`"01:01"\`,
  \`"07:02"\`).

- serology:

  \`character\`. Serological antigen number (e.g., \`"1"\`, \`"7"\`).

## Source

WMDA nomenclature files from IMGT/HLA GitHub repository
(<https://github.com/ANHIG/IMGTHLA/tree/Latest/wmda>).

## Details

The mapping prioritizes serology assignments in this order:

1.  Unambiguous assignments

2.  Possible assignments

3.  Assumed assignments

4.  Expert assignments

## See also

[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md),
[`updateWmdaData`](https://www.borch.dev/uploads/deepMatchR/reference/updateWmdaData.md),
[`deepMatchR_wmda_splits`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_wmda_splits.md),
[`deepMatchR_wmda_pgroups`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_wmda_pgroups.md)
