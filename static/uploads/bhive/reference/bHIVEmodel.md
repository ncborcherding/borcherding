# bHIVE classification model for caret

A custom model definition that lets
[`caret::train()`](https://rdrr.io/pkg/caret/man/train.html) tune,
resample and evaluate
[`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
classifiers.

## Usage

``` r
bHIVEmodel
```

## Format

A list with the components caret expects of a custom model.

## Value

A list defining a custom caret model, for use as
`caret::train(method = bHIVEmodel)`.

## Details

Pass `bHIVEmodel` as the `method` of
[`caret::train()`](https://rdrr.io/pkg/caret/man/train.html). Training
fits [`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
with the tuned `nAntibodies`, `beta` and `epsilon`. Further arguments
given to [`caret::train()`](https://rdrr.io/pkg/caret/man/train.html)
(for example `maxIter`, `scale` or immunology modules) are passed on to
[`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md).
Progress output is off unless `verbose = TRUE` is passed. Prediction
labels each new observation with the class of its best-matching
antibody, using the fitted
[`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md) model,
so new data gets the same scaling and kernel as the training data.

caret requires column names on `x`.

## Components

- `label`:

  "Artificial Immune Network (bHIVE)".

- `library`:

  "bHIVE".

- `type`:

  "Classification".

- `parameters`:

  The tunable parameters: `nAntibodies` (initial antibody count), `beta`
  (clone multiplier) and `epsilon` (suppression threshold).

- `grid`:

  `function(x, y, len, search)`. A default tuning grid, regular
  (`search = "grid"`) or random.

- `fit`:

  `function(x, y, wts, param, lev, last, classProbs, ...)`. Fits
  [`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
  and returns its result.

- `predict`:

  `function(modelFit, newdata, submodels)`. Returns a factor of
  predicted classes.

- `prob`:

  `NULL`. Class probabilities are not implemented, so
  [`caret::train()`](https://rdrr.io/pkg/caret/man/train.html) warns and
  continues if `classProbs = TRUE`.

## See also

[`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md),
[`honeycombHIVEmodel`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVEmodel.md),
[`train`](https://rdrr.io/pkg/caret/man/train.html)

## Examples

``` r
bHIVEmodel$label
#> [1] "Artificial Immune Network (bHIVE)"
bHIVEmodel$parameters
#>     parameter   class                label
#> 1 nAntibodies numeric Number of Antibodies
#> 2        beta numeric     Clone Multiplier
#> 3     epsilon numeric    Epsilon Threshold

if (requireNamespace("caret", quietly = TRUE)) {
    X <- as.matrix(iris[, 1:4])
    y <- iris$Species
    set.seed(42)
    fit <- caret::train(
        x = X, y = y, method = bHIVEmodel,
        trControl = caret::trainControl(method = "cv", number = 3),
        tuneGrid = data.frame(nAntibodies = 40, beta = 5, epsilon = 0.05),
        maxIter = 10
    )
    fit
    table(Predicted = predict(fit, X), Actual = y)
}
#> Loading required package: ggplot2
#> Loading required package: lattice
#> 
#> Attaching package: ‘caret’
#> The following object is masked from ‘package:generics’:
#> 
#>     train
#>             Actual
#> Predicted    setosa versicolor virginica
#>   setosa         50          0         0
#>   versicolor      0         43         2
#>   virginica       0          7        48
```
