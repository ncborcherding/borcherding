# ImmuneAlgorithm

Abstract R6 base class for all immune-inspired algorithms. Subclasses
must implement the `fit` method.

## Public fields

- `repertoire`:

  An
  [`ImmuneRepertoire`](https://www.borch.dev/uploads/bhive/reference/ImmuneRepertoire.md)
  object.

- `config`:

  Named list of algorithm hyperparameters.

- `modules`:

  Named list of injected module instances (SHMEngine, IdiotypicNetwork,
  GerminalCenter, etc.).

- `history`:

  List of per-iteration metrics.

- `result`:

  The result from the last call to `fit()`.

## Methods

### Public methods

- [`ImmuneAlgorithm$new()`](#method-ImmuneAlgorithm-new)

- [`ImmuneAlgorithm$fit()`](#method-ImmuneAlgorithm-fit)

- [`ImmuneAlgorithm$predict()`](#method-ImmuneAlgorithm-predict)

- [`ImmuneAlgorithm$print()`](#method-ImmuneAlgorithm-print)

- [`ImmuneAlgorithm$summary()`](#method-ImmuneAlgorithm-summary)

- [`ImmuneAlgorithm$clone()`](#method-ImmuneAlgorithm-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new ImmuneAlgorithm.

#### Usage

    ImmuneAlgorithm$new(config = list(), modules = list())

#### Arguments

- `config`:

  Named list of hyperparameters.

- `modules`:

  Named list of module instances.

------------------------------------------------------------------------

### Method `fit()`

Fit the algorithm to data. Must be overridden by subclasses.

#### Usage

    ImmuneAlgorithm$fit(X, y = NULL, task = NULL, ...)

#### Arguments

- `X`:

  Numeric matrix (n x d).

- `y`:

  Optional target vector (factor or numeric).

- `task`:

  Character: "clustering", "classification", or "regression".

- `...`:

  Additional arguments.

#### Returns

The algorithm object (invisibly), with `result` populated.

------------------------------------------------------------------------

### Method [`predict()`](https://rdrr.io/r/stats/predict.html)

Predict on new data using the trained repertoire.

#### Usage

    ImmuneAlgorithm$predict(newdata)

#### Arguments

- `newdata`:

  Numeric matrix (n_new x d).

#### Returns

Predictions (class labels, numeric values, or cluster IDs).

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary of the algorithm.

#### Usage

    ImmuneAlgorithm$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method [`summary()`](https://rdrr.io/r/base/summary.html)

Get a summary of the fitting history.

#### Usage

    ImmuneAlgorithm$summary()

#### Returns

Data frame of per-iteration metrics.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    ImmuneAlgorithm$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# ImmuneAlgorithm is abstract; use AINet for concrete instances
algo <- ImmuneAlgorithm$new()
print(algo)
#> <ImmuneAlgorithm>
#>   (not yet fitted)
```
