# Multilayered honeycombHIVE classification model for caret

A custom model definition that lets
[`caret::train()`](https://rdrr.io/pkg/caret/man/train.html) tune,
resample and evaluate
[`honeycombHIVE`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVE.md)
classifiers with gradient-based refinement.

## Usage

``` r
honeycombHIVEmodel
```

## Format

A list with the components caret expects of a custom model.

## Value

A list defining a custom caret model, for use as
`caret::train(method = honeycombHIVEmodel)`.

## Details

Training runs `honeycombHIVE(refine = TRUE)` with the tuned parameters.
Further arguments given to
[`caret::train()`](https://rdrr.io/pkg/caret/man/train.html) are passed
on to
[`honeycombHIVE()`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVE.md).
Progress output is off unless `verbose = TRUE` is passed. Prediction
uses the fitted
[`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md) model
of the final layer. caret requires column names on `x`. Class
probabilities are not implemented (`prob = NULL`).

## Parameters

- `nAntibodies`: Number of initial antibodies per layer.

- `beta`: Clone multiplier controlling the number of clones per
  antibody.

- `epsilon`: Threshold for network suppression to remove redundant
  antibodies.

- `layers`: Number of hierarchical layers.

- `refineOptimizer`: Optimizer for gradient-based refinement ("sgd",
  "momentum", "adagrad", "adam" or "rmsprop").

- `refineSteps`: Number of gradient update steps in refinement.

- `refineLR`: Learning rate for refinement.

## See also

[`honeycombHIVE`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVE.md),
[`bHIVEmodel`](https://www.borch.dev/uploads/bhive/reference/bHIVEmodel.md),
[`train`](https://rdrr.io/pkg/caret/man/train.html)

## Examples

``` r
if (requireNamespace("caret", quietly = TRUE)) {
    X <- as.matrix(iris[, 1:4])
    y <- iris$Species
    set.seed(42)
    fit <- caret::train(
        x = X, y = y, method = honeycombHIVEmodel,
        trControl = caret::trainControl(method = "cv", number = 3),
        tuneGrid = data.frame(nAntibodies = 30, beta = 5, epsilon = 0.05,
                              layers = 2, refineOptimizer = "adam",
                              refineSteps = 3, refineLR = 0.01),
        maxIter = 10
    )
    fit
    table(Predicted = predict(fit, X), Actual = y)
}
#>             Actual
#> Predicted    setosa versicolor virginica
#>   setosa         50          0         0
#>   versicolor      0         37         5
#>   virginica       0         13        45
```
