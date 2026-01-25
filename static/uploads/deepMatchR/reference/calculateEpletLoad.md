# Calculate Eplet Load Between Donor and Recipient Genotypes

Aggregates \*\*donor-specific eplets\*\* (present in donor, absent in
recipient) over loci. Can return a single total, a per-locus summary, or
a pairwise recipient-vs-donor allele matrix for a chosen locus. Supports
filtering by \*\*evidence\*\*, \*\*exposition\*\*, and
\*\*reactivity\*\*.

## Usage

``` r
calculateEpletLoad(
  recipient_geno,
  donor_geno,
  loci = NULL,
  evidence_level = c("A1", "A2"),
  exposition_filter = NULL,
  reactivity_filter = NULL,
  return = c("total", "per_locus", "pairwise"),
  pairwise_locus = NULL
)
```

## Arguments

- recipient_geno, donor_geno:

  \`hla_genotype\` objects.

- loci:

  Character vector of loci to include (e.g. \`c("A","B","C")\`), or
  \`NULL\` (default) for all shared loci.

- evidence_level:

  Character vector of evidence levels to include (default
  \`c("A1","A2")\`). Use \`NULL\` for no evidence filter.

- exposition_filter:

  Character vector of exposition classes to include; \`NULL\` for no
  filter.

- reactivity_filter:

  Character vector of reactivity classes to include; \`NULL\` for no
  filter.

- return:

  What to return: \`"total"\` (default), \`"per_locus"\`, or
  \`"pairwise"\`.

- pairwise_locus:

  When \`return = "pairwise"\`, the single locus to compute (e.g.,
  \`"B"\`). Ignored otherwise.

## Value

\- If \`return="total"\`: integer total donor-specific eplet load. - If
\`return="per_locus"\`: \`data.frame\` with columns \`locus\`,
\`eplet_load\`. - If \`return="pairwise"\`: numeric matrix where entry
\`\[i,j\]\` is the count of donor-specific eplets for donor allele \`j\`
vs recipient allele \`i\` at \`pairwise_locus\`.

## Examples

``` r
# Dummy genotypes
recipient <- data.frame(
  A_1 = "A*01:01", A_2 = "A*02:01",
  B_1 = "B*07:02", B_2 = "B*08:01"
)
donor <- data.frame(
  A_1 = "A*03:01", A_2 = "A*24:02",
  B_1 = "B*44:02", B_2 = "B*51:01"
)
rgeno <- hlaGeno(recipient); dgeno <- hlaGeno(donor)

# Total donor-specific eplet load (A1/A2 evidence)
calculateEpletLoad(rgeno, dgeno)
#> [1] 10

# Per locus
calculateEpletLoad(rgeno, dgeno, return = "per_locus")
#>   locus eplet_load
#> 1     A          4
#> 2     B          6

# Pairwise matrix for B locus (rows=recipient alleles, cols=donor alleles)
mB <- calculateEpletLoad(rgeno, dgeno, return = "pairwise", pairwise_locus = "B")
mB
#>          donor
#> recipient B*44:02 B*51:01
#>   B*07:02       5       4
#>   B*08:01       4       3

# Apply additional filters
calculateEpletLoad(rgeno, dgeno, exposition_filter = "High")
#> [1] 8
calculateEpletLoad(rgeno, dgeno, reactivity_filter = c("IgG"))
#> [1] 0
```
