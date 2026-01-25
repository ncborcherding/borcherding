# CREG–Allele Mapping Data

A curated mapping of IMGT/HLA allele strings to their corresponding
serologic antigen assignments and Cross-Reactive Groups (CREGs). This
table is intended for convenience functions that summarize antibody
specificity, collapse alleles to serology, or group responses by CREG
for reporting.

## Usage

``` r
data(deepMatchR_cregs)
```

## Format

A data frame with the following variables:

- allele:

  \`character\`. IMGT/HLA allele (e.g., \`"B\*07:02"\`).

- serology:

  \`character\`. Serologic antigen assignment (e.g., \`"B7"\`).

- CREG:

  \`character\`. Cross-Reactive Group label (e.g., \`"CREG07"\`).

## Details

\- \*\*Allele strings\*\* follow IMGT/HLA nomenclature (e.g.,
\`"A\*02:01"\`). - \*\*Serology\*\* uses conventional two-digit antigen
labels (e.g., \`"A2"\`, \`"B8"\`). Depending on your workflow, you may
want to harmonize with vendor-specific naming. - \*\*CREG\*\* indicates
the cross-reactive group label used in many transplant workflows to
approximate serologic cross-reactivity.

## Note

Source is an internal curation aligned to common CREG practice; see the
package vignette for curation notes and limitations. Always verify
against your lab’s approved references.

## Typical use

\- Collapsing allele-level reactivity to serology/CREG. - Building
summary tables/plots by serology or CREG.

## See also

[`deepMatchR_eplets`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_eplets.md),
[`deepMatchR_example`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_example.md)
