# Predict peptide–MHC binding with mhcnuggets

Calls Python's `mhcnuggets.src.predict.predict` inside a
basilisk-managed environment to score peptides against a given MHC
allele. By default the predictions are written by Python to a temporary
CSV and read back in R, which avoids Python stdout capture and is
typically faster and more robust.

## Usage

``` r
predictMHCnuggets(
  peptides,
  allele,
  mhc_class = "I",
  output_path = NULL,
  normalize_allele = TRUE,
  model = "lstm",
  mass_spec = FALSE,
  ic50_threshold = 500L,
  max_ic50 = 50000L,
  embed_peptides = FALSE,
  binary_preds = FALSE,
  ba_models = FALSE,
  rank_output = FALSE,
  hla_env = deepmatchrEnv()
)
```

## Arguments

- peptides:

  Character vector of peptide sequences (one per peptide).

- allele:

  MHC allele string. If `normalize_allele=TRUE`, common forms like
  `"A0201"` are normalized to `"HLA-A02:01"` for class I and
  `"HLA-DRB101:01"` for class II.

- mhc_class:

  Either `"I"` or `"II"` (default `"I"`).

- output_path:

  Optional file path for Python to write CSV results. If `NULL`
  (default), a secure temporary file is used and deleted on exit.

- normalize_allele:

  Logical; normalize `allele` to mhcnuggets' expected format (default
  `TRUE`). Set `FALSE` if you already use exact mhcnuggets allele names.

- model:

  Model architecture string (default `"lstm"`).

- mass_spec:

  Logical; use MS-calibrated settings (default `FALSE`).

- ic50_threshold:

  Numeric IC50 threshold (nM) for binding calls (default `500`).

- max_ic50:

  Numeric max IC50 (nM) for capping (default `50000`).

- embed_peptides:

  Logical; use embedding (default `FALSE`).

- binary_preds:

  Logical; request binary predictions (default `FALSE`).

- ba_models:

  Logical; force binding affinity models (default `FALSE`).

- rank_output:

  Logical; request rank output (default `FALSE`).

- hla_env:

  A basilisk environment object that contains Python + mhcnuggets (e.g.,
  `hlaFerretEnv`).

## Value

A `data.frame`. Columns depend on options:

- Default: `peptide`, `ic50`

- If `binary_preds=TRUE`: `peptide`, `binary_pred` (plus `ic50` if
  emitted by model)

- If `rank_output=TRUE`: includes `rank` (0–1 or percentile)

## Details

This wrapper exposes most of mhcnuggets' arguments so advanced users can
fully control model choice, thresholds, and output format. It also
applies a small, session-local patch so older mhcnuggets code that calls
`keras.optimizers.Adam(lr=...)` works on newer Keras (maps `lr` to
`learning_rate`).

## License and Citation

mhcnuggets is licensed under the GNU General Public License v3.0. If you
use MHCnuggets in your work, please cite: Shao, B., et al. (2020).
MHCnuggets: A deep learning method for peptide-MHC binding prediction.
bioRxiv. GitHub: https://github.com/KarchinLab/mhcnuggets

## Examples

``` r
res <- predictMHCnuggets(
  peptides = c("SIINFEKL","LLFGYPVYV"),
  allele   = "A*02:01",
  mhc_class = "I",
  rank_output = TRUE
)
head(res)
#>     peptide    ic50
#> 1  SIINFEKL 5600.06
#> 2 LLFGYPVYV  535.92
```
