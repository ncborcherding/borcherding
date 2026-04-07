# ActivationGate

Two-signal activation gate implementing the immunological principle that
immune cell activation requires both antigen-specific recognition
(Signal 1) AND costimulatory context (Signal 2).

## Details

Prevents spurious activation on isolated outliers. An antibody is only
allowed to clone if both signals exceed their thresholds. This is
biologically-principled regularization.

Signal 2 options:

- `"density"`: Local data density around the antibody

- `"danger"`: User-provided danger signal vector

- `"entropy"`: Local label entropy (classification only)

## Public fields

- `signal2_type`:

  Type of costimulatory signal.

- `threshold1`:

  Minimum affinity for Signal 1 (antigen recognition).

- `threshold2`:

  Minimum costimulatory signal for Signal 2.

- `danger_signals`:

  User-provided danger signal vector (for "danger" type).

## Methods

### Public methods

- [`ActivationGate$new()`](#method-ActivationGate-new)

- [`ActivationGate$evaluate()`](#method-ActivationGate-evaluate)

- [`ActivationGate$print()`](#method-ActivationGate-print)

- [`ActivationGate$clone()`](#method-ActivationGate-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new ActivationGate.

#### Usage

    ActivationGate$new(
      signal2_type = "density",
      threshold1 = 0.1,
      threshold2 = 0.3,
      danger_signals = NULL
    )

#### Arguments

- `signal2_type`:

  Character. "density", "danger", or "entropy".

- `threshold1`:

  Numeric. Minimum affinity threshold.

- `threshold2`:

  Numeric. Minimum Signal 2 threshold.

- `danger_signals`:

  Numeric vector. Per-data-point danger scores.

------------------------------------------------------------------------

### Method `evaluate()`

Evaluate which antibody-data interactions pass the two-signal gate.

#### Usage

    ActivationGate$evaluate(affinity_matrix, X, A, y = NULL, task = "clustering")

#### Arguments

- `affinity_matrix`:

  Numeric matrix (n x m) of affinities.

- `X`:

  Numeric matrix of data (n x d).

- `A`:

  Numeric matrix of antibodies (m x d).

- `y`:

  Target vector or NULL.

- `task`:

  Character. Task type.

#### Returns

Logical matrix (n x m) where TRUE means the interaction is activated.

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary.

#### Usage

    ActivationGate$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    ActivationGate$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Two-signal activation gate
data(iris)
X <- as.matrix(iris[, 1:4])
A <- X[sample(150, 10), ]
rep <- ImmuneRepertoire$new(A)
gate <- ActivationGate$new(signal2_type = "density", threshold2 = 0.3)
aff <- rep$affinity_matrix(X, "gaussian")
activated <- gate$evaluate(aff, X, A)
sum(activated)  # number of activated interactions
#> [1] 411
```
