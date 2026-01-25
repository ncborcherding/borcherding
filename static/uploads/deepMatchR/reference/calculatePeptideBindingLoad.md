# Calculate Peptide Binding Load for Transplant Risk Assessment

Predicts transplant risk by calculating peptide-HLA binding affinities
between recipient HLA molecules and donor-mismatched peptides. Supports
multiple binding prediction backends: built-in position weight matrix
(PWM), NetMHCpan, or MHCflurry.

## Usage

``` r
calculatePeptideBindingLoad(
  recipient,
  donor,
  backend = c("pwm", "netmhcpan", "mhcflurry"),
  backend_path = NULL,
  peptide_length = 9L,
  binding_threshold = 500,
  weak_threshold = 5000,
  return = c("total", "summary", "detail"),
  aggregate_method = c("sum", "max", "mean")
)
```

## Arguments

- recipient:

  An \`hla_genotype\` object or character vector of HLA allele names.

- donor:

  An \`hla_genotype\` object, character vector of HLA allele names, or a
  character vector of peptide sequences. If \`hla_genotype\` or allele
  names, mismatched peptides are derived automatically from sequence
  differences.

- backend:

  Character. Binding prediction method: \`"pwm"\` (default, no external
  dependencies), \`"netmhcpan"\`, or \`"mhcflurry"\`.

- backend_path:

  Character. Path to external tool executable. Required for
  \`"netmhcpan"\` backend.

- peptide_length:

  Integer. Peptide length(s) to consider. Default \`9L\`.

- binding_threshold:

  Numeric. IC50 threshold (nM) for "strong binder". Default \`500\`.

- weak_threshold:

  Numeric. IC50 threshold (nM) for "weak binder". Default \`5000\`.

- return:

  Character. One of \`"total"\` (risk score), \`"summary"\`
  (per-allele), or \`"detail"\` (per-peptide table). Default
  \`"total"\`.

- aggregate_method:

  Character. How to combine per-peptide scores: \`"sum"\`, \`"max"\`,
  \`"mean"\`. Default \`"sum"\`.

## Value

Depends on \`return\`: - \`"total"\`: Numeric risk score. -
\`"summary"\`: data.frame with per-HLA-allele binding summary. -
\`"detail"\`: data.frame with columns: \`peptide\`, \`hla_allele\`,
\`predicted_ic50\`, \`binding_level\`, \`contribution\`.

## Details

The function works in several steps: 1. \*\*Input processing\*\*:
Converts inputs to standard format (allele names and peptides) 2.
\*\*Peptide derivation\*\*: If donor is genotype/alleles, derives
mismatched peptides by comparing sequences and generating overlapping
k-mers from mismatch regions 3. \*\*Binding prediction\*\*: Uses
selected backend to predict IC50 values 4. \*\*Risk calculation\*\*:
Aggregates binding predictions into a risk score

The \*\*PWM backend\*\* uses simplified position weight matrices based
on HLA supertypes. For production use with high accuracy requirements,
NetMHCpan is recommended.

Risk score formula: \$\$contribution = (1 - IC50/weak\\threshold) \times
multiplier\$\$ where multiplier is 2 for strong binders, 1 for weak
binders.

## See also

[`calculateMismatchLoad`](https://www.borch.dev/uploads/deepMatchR/reference/calculateMismatchLoad.md),
[`quantifyMismatch`](https://www.borch.dev/uploads/deepMatchR/reference/quantifyMismatch.md)

## Examples

``` r
# Create donor and recipient genotypes
recipient <- data.frame(
  A_1 = "A*02:01", A_2 = "A*03:01",
  B_1 = "B*07:02", B_2 = "B*44:02"
)
donor <- data.frame(
  A_1 = "A*01:01", A_2 = "A*24:02",
  B_1 = "B*08:01", B_2 = "B*35:01"
)
rgeno <- hlaGeno(recipient)
dgeno <- hlaGeno(donor)

if (FALSE) { # \dontrun{
# Calculate total binding load (requires sequence data)
calculatePeptideBindingLoad(rgeno, dgeno)

# Get detailed per-peptide results
calculatePeptideBindingLoad(rgeno, dgeno, return = "detail")

# Use with raw peptides
peptides <- c("GILGFVFTL", "NLVPMVATV", "FLKEKGGL")
calculatePeptideBindingLoad(rgeno, peptides)
} # }
```
