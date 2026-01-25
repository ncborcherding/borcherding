# Calculate Mismatch Load Between Donor and Recipient Genotypes

Computes amino-acid mismatch burden between donor and recipient across
HLA loci by calling \`quantifyMismatch()\` on each recipient–donor
allele pair per locus. Can return (1) a single total, (2) a per-locus
summary table, or (3) a pairwise recipient-vs-donor allele matrix for
one locus.

## Usage

``` r
calculateMismatchLoad(
  recipient_geno,
  donor_geno,
  loci = NULL,
  filter_charge = NULL,
  filter_polarity = NULL,
  na_action = c("exclude", "error", "count"),
  return = c("total", "per_locus", "pairwise"),
  pairwise_locus = NULL,
  parallel = TRUE,
  n_cores = 2
)
```

## Arguments

- recipient_geno:

  An \`hla_genotype\` object for the recipient.

- donor_geno:

  An \`hla_genotype\` object for the donor.

- loci:

  Character vector of loci to include (e.g., c("A","B","C")), or NULL to
  use all shared loci.

- filter_charge:

  NULL/TRUE/FALSE. Passed to \[quantifyMismatch()\].

- filter_polarity:

  NULL/TRUE/FALSE. Passed to \[quantifyMismatch()\].

- na_action:

  One of "exclude" (default), "error", "count". Passed through.

- return:

  What to return: "total" (default), "per_locus", or "pairwise".

- pairwise_locus:

  When \`return = "pairwise"\`, the locus to visualize (e.g., "A", "B",
  "C"). Ignored otherwise.

- parallel:

  Logical, whether to use parallel processing

- n_cores:

  Number of cores for parallel processing

## Value

\- If \`return = "total"\`: single integer total mismatch load. - If
\`return = "per_locus"\`: data.frame with columns \`locus\`,
\`mismatch_load\`. - If \`return = "pairwise"\`: numeric matrix of
pairwise counts (rows = recipient alleles, columns = donor alleles) for
\`pairwise_locus\`.

## Examples

``` r
# Toy genotypes
recipient <- data.frame(
  A_1 = "A*01:01", A_2 = "A*02:01",
  B_1 = "B*07:02", B_2 = "B*08:01"
)
donor <- data.frame(
  A_1 = "A*01:01", A_2 = "A*03:01",
  B_1 = "B*44:02", B_2 = "B*51:01"
)
rgeno <- hlaGeno(recipient)
dgeno <- hlaGeno(donor)

# 1) Total load (all loci, all mismatches)
calculateMismatchLoad(rgeno, dgeno)
#> [1] 199

# 2) Per-locus summary
calculateMismatchLoad(rgeno, 
                      dgeno, 
                      return = "per_locus")
#>   locus mismatch_load
#> 1     A            71
#> 2     B           128

# 3) Pairwise matrix for B locus
mB <- calculateMismatchLoad(rgeno, 
                            dgeno, 
                            return = "pairwise", 
                            pairwise_locus = "B")
mB
#>          donor
#> recipient B*44:02 B*51:01
#>   B*07:02      37      33
#>   B*08:01      31      27

# 4) Apply biophysical filters
# charge-changing only
calculateMismatchLoad(rgeno, 
                      dgeno, 
                      filter_charge = TRUE)               
#> [1] 75

# polarity-changing only
calculateMismatchLoad(rgeno, 
                      dgeno, 
                      filter_polarity = TRUE)             
#> [1] 66

# Both polarity and charge-changing
calculateMismatchLoad(rgeno, 
                      dgeno, 
                      filter_charge = TRUE, 
                      filter_polarity = TRUE) 
#> [1] 26
```
