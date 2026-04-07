# Mulilayered honeycombHIVE for caret

A `caret` wrapper for the
[`honeycombHIVE`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVE.md)
function, enabling seamless integration with the `caret` package for
hyperparameter tuning, cross-validation, and performance evaluation.

## Usage

``` r
honeycombHIVEmodel
```

## Format

An object of class `list` of length 8.

## Value

A `caret` model definition list. Pass it to
[`train`](https://rdrr.io/pkg/caret/man/train.html) for model training
and evaluation.

## Parameters

- `nAntibodies`: Number of initial antibodies in the network.

- `beta`: Clone multiplier controlling the number of clones per
  antibody.

- `epsilon`: Threshold for network suppression to remove redundant
  antibodies.

- `layers`: Number of hierarchical layers for iterative refinement.

- `refineOptimizer`: Optimizer for gradient-based refinement (e.g.
  "sgd", "momentum", "adagrad", "adam", "rmsprop").

- `refineSteps`: Number of gradient update steps in refinement.

- `refineLR`: Learning rate for refinement.

- `refineHuberDelta`: Delta parameter used if the "huber" loss is
  chosen.

## Supported Tasks

- `"Regression"`: Predicts numeric target values.

- `"Classification"`: Assigns class labels to input observations.

- `"Clustering"`: Groups data points based on similarity (though
  typically `caret` is used for supervised tasks).

## See also

[`train`](https://rdrr.io/pkg/caret/man/train.html),
[`trainControl`](https://rdrr.io/pkg/caret/man/trainControl.html)

## Examples

``` r
if (FALSE) { # \dontrun{
  library(caret)
  # Example: Classification with Iris
  data(iris)
  X <- as.matrix(iris[, 1:4])
  y <- iris$Species

  train_control <- trainControl(method = "cv", number = 5)
  set.seed(42)
  model <- train(
    x = X,
    y = y,
    method = honeycombHIVEmodel,
    trControl = train_control,
    tuneGrid = expand.grid(
      nAntibodies = c(10, 20),
      beta = c(3, 5),
      epsilon = c(0.01, 0.05),
      layers = c(1, 2),
      refineOptimizer = "adam",
      refineSteps = 5,
      refineLR = 0.01,
      refineHuberDelta = 1.0
    )
  )
  print(model)
} # }
```
