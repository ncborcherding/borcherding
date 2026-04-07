# refineB: Gradient-based fine-tuning for bHIVE antibodies with multiple loss functions and optimizers

After running `bHIVE` (or within `honeycombHIVE`), you have a set of
final antibody positions (A) in feature space. This function refines
those prototypes by iterating over the data points assigned to each
antibody and applying gradient-based updates using a user-chosen loss
function and optimizer.

## Usage

``` r
refineB(
  A,
  X,
  y = NULL,
  assignments,
  task = c("clustering", "classification", "regression"),
  loss = c("categorical_crossentropy", "binary_crossentropy", "kullback_leibler",
    "cosine", "mse", "mae", "poisson", "huber"),
  steps = 5,
  lr = 0.01,
  push_away = TRUE,
  huber_delta = 1,
  verbose = TRUE,
  optimizer = c("sgd", "momentum", "adagrad", "adam", "rmsprop"),
  momentum_coef = 0.9,
  beta1 = 0.9,
  beta2 = 0.999,
  rmsprop_decay = 0.9,
  epsilon = 1e-08
)
```

## Arguments

- A:

  Numeric matrix (nAb x d) of antibody/prototype positions.

- X:

  Matrix or data frame (nSamples x d) of feature data.

- y:

  Optional. Factor (classification), numeric (regression), or NULL
  (clustering).

- assignments:

  Integer or character vector (length = nSamples), specifying the
  antibody index (or label) each sample belongs to.

- task:

  One of `c("clustering", "classification", "regression")`.

- loss:

  One of
  `c("categorical_crossentropy", "binary_crossentropy", "kullback_leibler", "cosine", "mse", "mae", "poisson", "huber")`.

- steps:

  Integer. How many gradient steps to run.

- lr:

  Numeric. Learning rate for each update.

- push_away:

  Logical (for classification). Whether to push prototypes away from
  differently-labeled samples.

- huber_delta:

  Numeric. The delta threshold if using huber loss.

- verbose:

  Logical. If `TRUE`, prints progress messages each iteration.

- optimizer:

  One of `c("sgd", "momentum", "adagrad", "adam", "rmsprop")`. Specifies
  the gradient-based optimization approach.

- momentum_coef:

  Numeric. Momentum coefficient (used if `optimizer=="momentum"`).

- beta1:

  Numeric. Exponential decay rate for the first moment estimates (used
  in Adam).

- beta2:

  Numeric. Exponential decay rate for the second moment estimates (used
  in Adam).

- rmsprop_decay:

  Numeric. Decay factor for the squared gradient moving average (used in
  RMSProp).

- epsilon:

  Numeric. A small constant for numerical stability.

## Value

Updated matrix `A` of shape (nAb x d).

## Details

The user must provide: - A numeric matrix `A` of antibody/prototype
positions (nAb x nFeatures). - A numeric matrix/data frame `X` of data
(nSamples x nFeatures). - Optional `y` for classification/regression. If
`task="clustering"`, `y` can be NULL or ignored. - An integer or
character vector `assignments` (length=nSamples) giving the antibody
index (or label) to which each data point is assigned.

\## Available Losses

\### Classification (factor y) - \*\*"categorical_crossentropy"\*\*:
Pull prototypes toward data points if they share the antibody's dominant
label; push away otherwise. - \*\*"binary_crossentropy"\*\*: Similar to
categorical CE, but we interpret factor y as binary (two classes). Pull
for same label, push for different label. - \*\*"kullback_leibler"\*\*:
Very rough approach that treats “dominant label vs. others” as p and q
distributions, pushing/pulling prototypes. - \*\*"cosine"\*\*:
Interpreted as trying to maximize cosine similarity for same-label
points and minimize for different-label points.

\### Regression (numeric y) - \*\*"mse"\*\*: Mean squared error
approximation in feature space (pull prototypes toward assigned
points). - \*\*"mae"\*\*: Mean absolute error approach (sign-based
pull). - \*\*"poisson"\*\*: Poisson deviance (toy approach that scales
the gradient by (pred - y)/pred if we stored a predicted rate; here we
do a naive version). - \*\*"huber"\*\*: Combines L1 and L2 regions, uses
a delta cutoff. We adapt it to a naive per-point gradient in feature
space.

\## Available Optimizers - \*\*"sgd"\*\*: Basic stochastic gradient
descent. - \*\*"momentum"\*\*: SGD with momentum. - \*\*"adagrad"\*\*:
Adaptive gradient descent. - \*\*"adam"\*\*: Adaptive moment
estimation. - \*\*"rmsprop"\*\*: Root Mean Square Propagation.

This function performs gradient-based updates on each antibody using the
selected loss function. Depending on the chosen `optimizer`, it may use
plain SGD, momentum-based updates, Adagrad, Adam, or RMSProp.

## Examples

``` r
data(iris)
X <- as.matrix(iris[, 1:4])
y <- iris$Species
res <- bHIVE(X, y, task = "classification", nAntibodies = 10,
             maxIter = 5, verbose = FALSE)
assignments <- as.integer(factor(res$assignments,
                                 levels = unique(res$assignments)))
A_refined <- refineB(res$antibodies, X, y = y,
                     assignments = assignments,
                     task = "classification",
                     loss = "mse", optimizer = "adam",
                     steps = 3, lr = 0.01, verbose = FALSE)
dim(A_refined)
#> [1] 10  4
```
