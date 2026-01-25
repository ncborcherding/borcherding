# Quantify Amino Acid Mismatches With Charge/Polarity Awareness (base R)

Compares two amino acid sequences (same length) and quantifies
mismatches. Each mismatch is annotated for whether it changes residue
charge and/or polarity. Users can filter which mismatches to count based
on these properties.

## Usage

``` r
quantifyMismatch(
  sequence1,
  sequence2,
  filter_charge = NULL,
  filter_polarity = NULL,
  return = c("count", "detail"),
  na_action = c("exclude", "error", "count"),
  type = c("global", "local", "overlap"),
  substitutionMatrix = "BLOSUM80",
  gapOpening = 10,
  gapExtension = 1,
  count_gaps = TRUE
)
```

## Arguments

- sequence1, sequence2:

  Character strings of equal length (AAs).

- filter_charge:

  NULL/TRUE/FALSE - \`NULL\` (default): ignore charge when filtering
  (i.e., do not filter). - \`TRUE\`: count only mismatches that change
  charge. - \`FALSE\`: count only mismatches that do \*not\* change
  charge.

- filter_polarity:

  NULL/TRUE/FALSE. - \`NULL\` (default): ignore polarity when
  filtering. - \`TRUE\`: count only mismatches that change polarity. -
  \`FALSE\`: count only mismatches that do \*not\* change polarity.

- return:

  What to return: one of "count" (default) or "detail"

- na_action:

  One of "exclude" (default), "error", "count". Controls handling of
  unknown residues (e.g., X, \*, -).

- type:

  Character string. The type of alignment to perform. Defaults to
  \`"global"\` but allows for \`"local"\` and \`"overlap"\`-based
  alignments of the sequences.

- substitutionMatrix:

  Character string or numeric matrix. Substitution scoring matrix used
  during sequence alignment. Defaults to \`"BLOSUM80"\`, which provides
  a conservative amino acid similarity scheme suitable for closely
  related protein sequences.

- gapOpening:

  Numeric scalar. Penalty score applied when initiating a new gap during
  alignment. Higher values discourage insertion/deletion events and
  yield more contiguous alignments. Default is \`10\`.

- gapExtension:

  Numeric scalar. Penalty score applied when extending an existing gap.
  Smaller values permit longer continuous gaps, while larger values
  favor shorter gaps. Default is \`1\`.

- count_gaps:

  Logical (default \`TRUE\`). If \`TRUE\`, positions where one sequence
  contains a gap (\`-\`) and the other contains an amino acid are
  treated as mismatches and included in the mismatch count.

## Value

\- If return = "count": integer (count after filters). - If return =
"detail": a table with columns: position, ref, alt, is_mismatch,
charge_ref, charge_alt, charge_change, polarity_ref, polarity_alt,
polarity_change, counted.

## Examples

``` r
seq1 <- "YFAMYGEKVAHTHVDTLYVRYHY"
seq2 <- "YFDMYGEKVAHTHVDTLYVRFHY"

# Numerical quantification of mismatches
quantifyMismatch(seq1, seq2)
#> [1] 2

# Count only mismatches that change charge
quantifyMismatch(seq1, seq2, filter_charge = TRUE)
#> [1] 1

# Count only mismatches that change polarity
quantifyMismatch(seq1, seq2, filter_polarity = TRUE)
#> [1] 2

# Count mismatches that change charge AND polarity
quantifyMismatch(seq1, seq2, filter_charge = TRUE, filter_polarity = TRUE)
#> [1] 1
```
