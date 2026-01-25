# HLA Eplet Assignments (Registry-derived)

Per-allele eplet annotations derived from the HLA Epitope Registry,
filtered to retain evidence classes A1, A2, B, and D. Each row links an
eplet to an HLA allele along with Registry metadata fields commonly used
for analysis.

## Usage

``` r
data(deepMatchR_eplets)
```

## Format

A data frame with 5 variables:

- eplet:

  \`character\`. Eplet identifier.

- exposition:

  \`character\`. Structural/surface exposure categorization.

- reactivity:

  \`character\` or \`NA\`. Registry reactivity note/flag.

- evidence:

  \`character\`. Evidence class; subset of {A1, A2, B, D}.

- allele:

  \`character\`. IMGT/HLA allele string.

## Source

HLA Epitope Registry (<https://www.epregistry.com.br/>); processed and
filtered by the package authors for reproducible analyses.

## Details

\*\*Field meanings (as used in this package):\*\*

- **eplet**: Short alphanumeric eplet identifier (e.g., \`"82LR"\`,
  \`"1C"\`).

- **exposition**: Qualitative description of surface exposure or
  structural context (e.g., \`"High"\`). This reflects the Registry’s
  exposition field.

- **reactivity**: Free-text/flag describing observed reactivity patterns
  in the Registry (often \`NA\` if not specified).

- **evidence**: Evidence class label from the Registry; records in this
  dataset are filtered to A1, A2, B, or D.

- **allele**: IMGT/HLA allele string to which the eplet is assigned
  (e.g., \`"B\*07:02"\`).

## Caveats

\- The Registry is a living resource; re-download or update your cache
regularly for production use. - Evidence codes indicate strength/quality
of support and are not equivalent to clinical validity. Apply your lab’s
validation and cutoffs.

## See also

[`deepMatchR_cregs`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_cregs.md)
