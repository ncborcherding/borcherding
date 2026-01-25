# Quantify Eplet Mismatches Between Two Alleles

Counts the number of \*\*eplet mismatches\*\* between two HLA alleles,
using the internal \`deepMatchR_eplets\` dataset. Supports filtering by
\*\*evidence\*\* (e.g., A1/A2), \*\*exposition\*\* (e.g., "High",
"Moderate"), and \*\*reactivity\*\* (e.g., IgG/IgM labels if present in
the table).

## Usage

``` r
quantifyEpletMismatch(
  allele1,
  allele2,
  evidence_level = c("A1", "A2"),
  exposition_filter = NULL,
  reactivity_filter = NULL
)
```

## Arguments

- allele1, allele2:

  Character scalars, e.g. \`"A\*01:01"\`, \`"A\*02:01"\`.

- evidence_level:

  Character vector of evidence levels to include (default
  \`c("A1","A2")\`). Use \`NULL\` for no evidence filter.

- exposition_filter:

  Character vector of exposition classes to include (e.g.,
  \`c("High","Moderate")\`). Default \`NULL\` = no exposition filter.

- reactivity_filter:

  Character vector of reactivity classes to include (dataset-dependent).
  Default \`NULL\` = no reactivity filter.

## Value

Integer: size of the \*\*symmetric difference\*\* of eplet sets between
the two alleles after filters (i.e., eplets present in one allele but
not the other).

## Examples

``` r
# Count eplet mismatches between two alleles
quantifyEpletMismatch("A*01:01", "A*02:01")
#> [1] 13

# With evidence level filter
quantifyEpletMismatch("A*01:01", "A*02:01", evidence_level = "A1")
#> [1] 8

# Same allele returns 0
quantifyEpletMismatch("A*01:01", "A*01:01")
#> [1] 0
```
