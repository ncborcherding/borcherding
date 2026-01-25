# WMDA P-Group Definitions

A lookup table containing HLA P-group definitions from WMDA
nomenclature. P-groups are sets of alleles with identical protein
sequences in the antigen recognition site. Used internally by
[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md)
to resolve P-group notation.

## Usage

``` r
data(deepMatchR_wmda_pgroups)
```

## Format

A data.table with the following columns:

- locus:

  \`character\`. HLA locus (e.g., \`"A"\`, \`"B"\`, \`"DRB1"\`).

- p_group:

  \`character\`. P-group designation (e.g., \`"01:01P"\`).

- reference_2f:

  \`character\`. Reference two-field allele for the P-group.

## Source

WMDA nomenclature files from IMGT/HLA GitHub repository
(<https://github.com/ANHIG/IMGTHLA/tree/Latest/wmda>).

## Details

P-group notation (e.g., \`"A\*01:01P"\`) indicates that multiple alleles
share the same protein sequence in the antigen recognition domain. This
table maps P-groups to their representative reference alleles for
serology lookup.

## See also

[`toSerology`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md),
[`deepMatchR_wmda_serology`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_wmda_serology.md)
