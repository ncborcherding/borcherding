# Tune Hyperparameters for bHIVE (Swarm/Grid Search)

Performs hyperparameter tuning for the bHIVE algorithm over a grid of
hyperparameter values or an externally provided data frame of parameter
combinations. Evaluates each combination using different metrics:

## Usage

``` r
swarmbHIVE(
  X,
  y = NULL,
  task = c("clustering", "classification"),
  grid,
  metric = NULL,
  maxIter = 50,
  BPPARAM = SerialParam(),
  verbose = TRUE
)
```

## Arguments

- X:

  A numeric matrix or data frame of input features (rows = observations,
  columns = features).

- y:

  Optional. A factor target vector for classification. If `NULL`,
  clustering is performed.

- task:

  Character. One of `"clustering"` or `"classification"`.

- grid:

  A data frame specifying the hyperparameter combinations, one row per
  combination. Any column named after a
  [`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md) or
  [`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md)
  argument is tuned (for example `nAntibodies`, `beta`, `epsilon`,
  `targetK`, `scale`, `affinityFunc` or `coverageBoost`). Other columns
  are ignored. Factor columns, as produced by
  [`expand.grid()`](https://rdrr.io/r/base/expand.grid.html), are
  converted to character.

- metric:

  Character. Name of the evaluation metric. Options:

  - **Classification**: "accuracy", "balanced_accuracy", "f1", "kappa"

  - **Clustering**: "silhouette", "davies_bouldin", "calinski_harabasz"

- maxIter:

  Integer. Maximum iterations for each `bHIVE` run (default 50). A
  `maxIter` column in `grid` takes precedence.

- BPPARAM:

  Character. A BiocParallel::bpparam() object that can be used for
  parallelization. The function supports `SerialParam`,
  `MulticoreParam`, `BatchtoolsParam`, and `SnowParam`.

- verbose:

  Logical. If `TRUE`, reports progress with
  [`message()`](https://rdrr.io/r/base/message.html).

## Value

A list:

- `best_params`: A list (row) of the best hyperparameters.

- `results`: A data frame with the full grid search results, including
  the `metric_value` for each combination.

## Details

\- \*\*Classification\*\*: "accuracy", "balanced_accuracy", "f1",
"kappa" - \*\*Clustering\*\*: "silhouette", "davies_bouldin", or
"calinski_harabasz"

\*\*Note\*\*: Some metrics require additional packages or assumptions
(e.g., multi-class classification for "f1" is calculated as a
macro-average).

## Examples

``` r
data(iris)
X <- as.matrix(iris[, 1:4])
y <- iris$Species  # classification

# Define hyperparameter grid
grid <- expand.grid(
  nAntibodies = c(10, 20),
  beta        = c(3, 5),
  epsilon     = c(0.01, 0.05)
)

# Perform hyperparameter tuning for classification
tuning_results <- swarmbHIVE(X = X, 
                             y = y, 
                             task = "classification", 
                             grid = grid, 
                             metric = "balanced_accuracy",
                             maxIter = 10)
#> Starting swarmbHIVE with 8 parameter combinations (task=classification, metric=balanced_accuracy).
#> Evaluating combo 1/8: nAntibodies=10, beta=3, epsilon=0.01
#> Evaluating combo 2/8: nAntibodies=20, beta=3, epsilon=0.01
#> Evaluating combo 3/8: nAntibodies=10, beta=5, epsilon=0.01
#> Evaluating combo 4/8: nAntibodies=20, beta=5, epsilon=0.01
#> Evaluating combo 5/8: nAntibodies=10, beta=3, epsilon=0.05
#> Evaluating combo 6/8: nAntibodies=20, beta=3, epsilon=0.05
#> Evaluating combo 7/8: nAntibodies=10, beta=5, epsilon=0.05
#> Evaluating combo 8/8: nAntibodies=20, beta=5, epsilon=0.05
#> Best parameters: nAntibodies=10, beta=3, epsilon=0.05, metric_value=0.96

# For clustering with silhouette
set.seed(42)
X_clust <- matrix(rnorm(100 * 5), ncol = 5)
grid_clust <- expand.grid(nAntibodies = c(5, 10), 
                          beta = c(3, 5), 
                          epsilon = c(0.01, 0.05))
res_clust <- swarmbHIVE(X_clust, 
                        task = "clustering", 
                        grid = grid_clust, 
                        metric = "silhouette")
#> Precomputing distance matrix for the silhouette metric.
#> Starting swarmbHIVE with 8 parameter combinations (task=clustering, metric=silhouette).
#> Evaluating combo 1/8: nAntibodies=5, beta=3, epsilon=0.01
#> Evaluating combo 2/8: nAntibodies=10, beta=3, epsilon=0.01
#> Evaluating combo 3/8: nAntibodies=5, beta=5, epsilon=0.01
#> Evaluating combo 4/8: nAntibodies=10, beta=5, epsilon=0.01
#> Evaluating combo 5/8: nAntibodies=5, beta=3, epsilon=0.05
#> Evaluating combo 6/8: nAntibodies=10, beta=3, epsilon=0.05
#> Evaluating combo 7/8: nAntibodies=5, beta=5, epsilon=0.05
#> Evaluating combo 8/8: nAntibodies=10, beta=5, epsilon=0.05
#> Best parameters: nAntibodies=5, beta=5, epsilon=0.01, metric_value=0.1721
res_clust$best_params
#>   nAntibodies beta epsilon metric_value
#> 3           5    5    0.01    0.1720884

```
