# GerminalCenter

Models T follicular helper (Tfh) cell selection pressure on B cells
within a germinal center reaction. Implements resource competition where
antibodies compete for Tfh help, and only helped antibodies survive.

## Details

The germinal center is where B cells undergo affinity maturation through
iterative cycles of mutation and selection. Tfh cells act as
quality-control selectors:

- Each Tfh evaluates B cell (antibody) quality using a task-aware metric

- B cells compete for Tfh help (resource competition)

- Only helped B cells survive to the next round

- Selection pressure controls the stringency of the process

## Public fields

- `nTfh`:

  Number of Tfh selectors (determines how many antibodies survive).

- `selectionPressure`:

  Numeric \[0,1\]. 0 = no selection (all survive), 1 = only the very
  best survive.

- `rounds`:

  Number of selection rounds per call.

## Methods

### Public methods

- [`GerminalCenter$new()`](#method-GerminalCenter-new)

- [`GerminalCenter$select()`](#method-GerminalCenter-select)

- [`GerminalCenter$print()`](#method-GerminalCenter-print)

- [`GerminalCenter$clone()`](#method-GerminalCenter-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new GerminalCenter.

#### Usage

    GerminalCenter$new(nTfh = 10, selectionPressure = 0.5, rounds = 1)

#### Arguments

- `nTfh`:

  Integer. Number of Tfh helper cells. Each helps one B cell.

- `selectionPressure`:

  Numeric \[0,1\]. Stringency of selection.

- `rounds`:

  Integer. Number of competition rounds.

------------------------------------------------------------------------

### Method `select()`

Run germinal center selection on a repertoire.

#### Usage

    GerminalCenter$select(
      repertoire,
      X,
      y = NULL,
      task = "clustering",
      affinityFunc = "gaussian",
      affinityParams = list(alpha = 1, c = 1, p = 2)
    )

#### Arguments

- `repertoire`:

  An
  [`ImmuneRepertoire`](https://www.borch.dev/uploads/bhive/reference/ImmuneRepertoire.md)
  object.

- `X`:

  Numeric matrix of training data.

- `y`:

  Target vector (factor or numeric) or NULL for clustering.

- `task`:

  Character: "clustering", "classification", or "regression".

- `affinityFunc`:

  Character. Affinity function for evaluation.

- `affinityParams`:

  List. Parameters for affinity function.

#### Returns

Invisible self. Repertoire modified in place.

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary.

#### Usage

    GerminalCenter$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    GerminalCenter$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Germinal center selection on Iris
data(iris)
X <- as.matrix(iris[, 1:4])
gc <- GerminalCenter$new(nTfh = 5, selectionPressure = 0.5)
rep <- ImmuneRepertoire$new(X[sample(150, 20), ])
gc$select(rep, X, iris$Species, "classification")
rep$size()  # fewer antibodies after selection
#> [1] 12
```
