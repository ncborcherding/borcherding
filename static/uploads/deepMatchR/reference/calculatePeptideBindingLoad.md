# Calculate Peptide Binding Load for Transplant Risk Assessment

Predicts transplant risk by calculating peptide-HLA binding affinities
between recipient HLA molecules and donor-mismatched peptides. Supports
multiple binding prediction backends: built-in position weight matrix
(PWM), NetMHCpan, or MHCnuggets.

## Usage

``` r
calculatePeptideBindingLoad(
  recipient,
  donor,
  backend = c("pwm", "netmhcpan", "mhcnuggets"),
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
  dependencies), \`"netmhcpan"\`, or \`"mhcnuggets"\`.

- backend_path:

  Character. Path to external tool executable. Required for

  \`"netmhcpan"\` backend. Download NetMHCpan from
  <https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/>.

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
NetMHCpan or MHCnuggets is recommended.

\*\*External backends:\*\* - \*\*NetMHCpan\*\*: A state-of-the-art
method for predicting peptide-MHC class I binding using artificial
neural networks. Available at
<https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/>. -
\*\*MHCnuggets\*\*: A deep learning approach for MHC binding prediction.
Available at <https://github.com/KarchinLab/mhcnuggets>. See
[`predictMHCnuggets`](https://www.borch.dev/uploads/deepMatchR/reference/predictMHCnuggets.md)
for direct access to MHCnuggets predictions.

Risk score formula: \$\$contribution = (1 - IC50/weak\\threshold) \times
multiplier\$\$ where multiplier is 2 for strong binders, 1 for weak
binders.

## References

Reynisson B, et al. (2020). NetMHCpan-4.1 and NetMHCIIpan-4.0: improved
predictions of MHC antigen presentation by concurrent motif
deconvolution and integration of MS MHC eluted ligand data. \*Nucleic
Acids Research\*, 48(W1), W449-W454.
[doi:10.1093/nar/gkaa379](https://doi.org/10.1093/nar/gkaa379)

Shao XM, et al. (2020). High-Throughput Prediction of MHC Class I and II
Neoantigens with MHCnuggets. \*Cancer Immunology Research\*, 8(3),
396-408.
[doi:10.1158/2326-6066.CIR-19-0464](https://doi.org/10.1158/2326-6066.CIR-19-0464)

## See also

[`calculateMismatchLoad`](https://www.borch.dev/uploads/deepMatchR/reference/calculateMismatchLoad.md),
[`quantifyMismatch`](https://www.borch.dev/uploads/deepMatchR/reference/quantifyMismatch.md),
[`predictMHCnuggets`](https://www.borch.dev/uploads/deepMatchR/reference/predictMHCnuggets.md)

## Examples

``` r
# Example 1: Using raw peptides (no external data required)
# Define recipient HLA alleles
recipient_alleles <- c("A*02:01", "A*03:01", "B*07:02", "B*08:01")

# Define peptides to test
peptides <- c("GILGFVFTL", "NLVPMVATV", "FLKEKGGL", "SIINFEKL")

# Calculate binding load with PWM backend
result <- calculatePeptideBindingLoad(
  recipient = recipient_alleles,
  donor = peptides,
  backend = "pwm",
  return = "summary"
)
print(result)
#>   hla_allele n_peptides n_strong n_weak risk_contribution
#> 1    A*02:01          2        0      2              1.75
#> 2    A*03:01          2        0      2              1.75
#> 3    B*07:02          2        0      2              1.25
#> 4    B*08:01          2        0      2              1.25

# Get detailed per-peptide results
detail <- calculatePeptideBindingLoad(
  recipient = recipient_alleles,
  donor = peptides,
  backend = "pwm",
  return = "detail"
)
head(detail)
#>     peptide hla_allele predicted_ic50 binding_level contribution
#> 1 GILGFVFTL    A*02:01            625          weak        0.875
#> 2 NLVPMVATV    A*02:01            625          weak        0.875
#> 3 GILGFVFTL    A*03:01            625          weak        0.875
#> 4 NLVPMVATV    A*03:01            625          weak        0.875
#> 5 GILGFVFTL    B*07:02           1250          weak        0.750
#> 6 NLVPMVATV    B*07:02           2500          weak        0.500

# Example 2: Using hla_genotype objects with peptides
recipient <- data.frame(
  A_1 = "A*02:01", A_2 = "A*03:01",
  B_1 = "B*07:02", B_2 = "B*44:02"
)
rgeno <- hlaGeno(recipient)

# Calculate total risk score
total_risk <- calculatePeptideBindingLoad(
  recipient = rgeno,
  donor = peptides,
  return = "total"
)
print(total_risk)
#> [1] 6

# \donttest{
# Example 3: Using genotypes (requires IMGT database connection)
donor <- data.frame(
  A_1 = "A*01:01", A_2 = "A*24:02",
  B_1 = "B*08:01", B_2 = "B*35:01"
)
dgeno <- hlaGeno(donor)

# Calculate binding load from sequence mismatches
calculatePeptideBindingLoad(rgeno, dgeno, return = "summary")
#>   hla_allele n_peptides n_strong n_weak risk_contribution
#> 1    A*02:01        624        0    354            195.25
#> 2    A*03:01        624        0    354            195.25
#> 3    B*07:02        624        0    299             69.00
#> 4    B*44:02        624        0    299             69.00
# }
```
