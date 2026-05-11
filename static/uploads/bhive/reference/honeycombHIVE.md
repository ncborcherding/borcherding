# honeycombHIVE: Multilayer AIS with optional gradient-based fine-tuning

The `honeycombHIVE` function implements a multilayer artificial immune
system that iteratively refines a set of prototypes - referred to as
antibodies - to model the structure of the input data. In each layer,
the function first uses the
[`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
algorithm to generate or update antibodies based on the current data
representation and task (clustering or classification). Optionally, it
applies gradient-based fine-tuning (via
[`refineB`](https://www.borch.dev/uploads/bhive/reference/refineB.md))
to these antibodies, allowing for advanced refinement through various
optimizers (e.g., SGD, Adam, RMSProp) and customizable loss functions.
The final output is a hierarchical set of layers that encapsulate both
the refined prototypes and the corresponding cluster assignments or
predictions for the original observations, making `honeycombHIVE` a
versatile tool for adaptive learning and pattern recognition.

## Usage

``` r
honeycombHIVE(
  X,
  y = NULL,
  task = c("clustering", "classification"),
  layers = 3,
  nAntibodies = 20,
  minAntibodies = 5,
  epsilon = 0.05,
  beta = 5,
  maxIter = 10,
  collapseMethod = c("centroid", "medoid", "median", "mode"),
  minClusterSize = NULL,
  distance = "euclidean",
  verbose = TRUE,
  refine = FALSE,
  refineLoss = "categorical_crossentropy",
  refineSteps = 5,
  refineLR = 0.01,
  refinePushAway = TRUE,
  refineOptimizer = "sgd",
  refineMomentumCoef = 0.9,
  refineBeta1 = 0.9,
  refineBeta2 = 0.999,
  refineRmspropDecay = 0.9,
  refineEpsilon = 1e-08,
  ...
)
```

## Arguments

- X:

  A numeric matrix or data frame of input features (rows = observations,
  columns = features).

- y:

  Optional target factor vector for classification.

- task:

  Character, one of "clustering" or "classification".

- layers:

  Integer, how many layers (AIS iterations) to run.

- nAntibodies:

  Integer, how many antibodies (prototypes) to generate initially in
  each layer.

- minAntibodies:

  Integer, minimal number of antibodies to keep in each layer.

- epsilon:

  Numeric, threshold param for `bHIVE` suppression.

- beta:

  Numeric, selection pressure param for `bHIVE`.

- maxIter:

  Integer, maximum iterations for `bHIVE` each layer.

- collapseMethod:

  One of "centroid","medoid","median","mode".

- minClusterSize:

  Minimum cluster size. Smaller clusters can be merged/discarded if not
  NULL.

- distance:

  Distance metric for medoid calculation, e.g. "euclidean".

- verbose:

  Logical, if TRUE prints progress at each layer.

- refine:

  Logical, if TRUE apply gradient-based refinement via
  [`refineB()`](https://www.borch.dev/uploads/bhive/reference/refineB.md)
  to each layer's prototypes.

- refineLoss:

  Character specifying the loss for
  [`refineB()`](https://www.borch.dev/uploads/bhive/reference/refineB.md)
  (e.g. "categorical_crossentropy", "mae").

- refineSteps:

  Integer, number of gradient steps in
  [`refineB()`](https://www.borch.dev/uploads/bhive/reference/refineB.md).

- refineLR:

  Numeric, learning rate for gradient updates.

- refinePushAway:

  Logical, if TRUE and classification, push prototypes away from
  differently labeled points.

- refineOptimizer:

  Character, one of `"sgd", "momentum", "adagrad", "adam", "rmsprop"` to
  be passed to
  [`refineB()`](https://www.borch.dev/uploads/bhive/reference/refineB.md).

- refineMomentumCoef:

  Numeric, momentum coefficient (if using momentum).

- refineBeta1:

  Numeric, first moment decay rate (if using Adam).

- refineBeta2:

  Numeric, second moment decay rate (if using Adam).

- refineRmspropDecay:

  Numeric, decay rate for the moving average of squared gradients (if
  using RMSProp).

- refineEpsilon:

  Numeric, a small constant for numerical stability (used in adaptive
  optimizers).

- ...:

  Additional arguments passed to `bHIVE`.

## Value

A list of length `layers`. Each element (layer) includes:

- `antibodies`: The prototypes in that layer.

- `assignments`: Antibody index (in that layer) for each row of
  `current_X`.

- `membership`: For each **original** row in `X`, which cluster/antibody
  it belongs to in this layer.

- `predictions`: If classification, predicted label for each original
  row in `X`.

- `task`: The specified task.

## Examples

``` r
# Clustering
data(iris)
X_iris <- iris[, 1:4]
resC <- honeycombHIVE(
  X = X_iris,
  task = "clustering",
  layers = 3,
  nAntibodies = 15,
  beta = 5,
  maxIter = 10
)
#> 
#> === honeycombHIVE: Layer 1 / 3 (task=clustering) ===
#> Iteration 1 | #Antibodies: 15 | noImproveCount: 1
#> Iteration 2 | #Antibodies: 15 | noImproveCount: 2
#> Iteration 3 | #Antibodies: 15 | noImproveCount: 3
#> Iteration 4 | #Antibodies: 15 | noImproveCount: 4
#> Iteration 5 | #Antibodies: 15 | noImproveCount: 5
#> Iteration 6 | #Antibodies: 15 | noImproveCount: 6
#> Iteration 7 | #Antibodies: 15 | noImproveCount: 7
#> Iteration 8 | #Antibodies: 15 | noImproveCount: 8
#> Iteration 9 | #Antibodies: 15 | noImproveCount: 9
#> Iteration 10 | #Antibodies: 15 | noImproveCount: 10
#> Layer 1 completed. Next layer will use 12 prototypes.
#> 
#> === honeycombHIVE: Layer 2 / 3 (task=clustering) ===
#> Iteration 1 | #Antibodies: 11 | noImproveCount: 0
#> Iteration 2 | #Antibodies: 11 | noImproveCount: 1
#> Iteration 3 | #Antibodies: 11 | noImproveCount: 2
#> Iteration 4 | #Antibodies: 11 | noImproveCount: 3
#> Iteration 5 | #Antibodies: 11 | noImproveCount: 4
#> Iteration 6 | #Antibodies: 11 | noImproveCount: 5
#> Iteration 7 | #Antibodies: 11 | noImproveCount: 6
#> Iteration 8 | #Antibodies: 11 | noImproveCount: 7
#> Iteration 9 | #Antibodies: 11 | noImproveCount: 8
#> Iteration 10 | #Antibodies: 11 | noImproveCount: 9
#> Layer 2 completed. Next layer will use 6 prototypes.
#> 
#> === honeycombHIVE: Layer 3 / 3 (task=clustering) ===
#> Iteration 1 | #Antibodies: 5 | noImproveCount: 0
#> Iteration 2 | #Antibodies: 5 | noImproveCount: 1
#> Iteration 3 | #Antibodies: 5 | noImproveCount: 2
#> Iteration 4 | #Antibodies: 5 | noImproveCount: 3
#> Iteration 5 | #Antibodies: 5 | noImproveCount: 4
#> Iteration 6 | #Antibodies: 5 | noImproveCount: 5
#> Iteration 7 | #Antibodies: 5 | noImproveCount: 6
#> Iteration 8 | #Antibodies: 5 | noImproveCount: 7
#> Iteration 9 | #Antibodies: 5 | noImproveCount: 8
#> Iteration 10 | #Antibodies: 5 | noImproveCount: 9
#> Layer 3 completed. Next layer will use 5 prototypes.
```
