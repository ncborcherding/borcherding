# bHIVE: B-cell Hybrid Immune Variant Engine

Implements an artificial immune network algorithm for clustering and
classification tasks. The algorithm evolves a population of "antibodies"
via clonal selection and mutation, applies network suppression to
maintain diversity, and assigns data points based on affinity or
distance metrics.

## Usage

``` r
bHIVE(
  X,
  y = NULL,
  task = NULL,
  nAntibodies = 20,
  beta = 5,
  epsilon = 0.01,
  maxIter = 50,
  affinityFunc = "gaussian",
  distFunc = "euclidean",
  affinityParams = list(alpha = 1, c = 1, p = 2, Sigma = NULL),
  mutationDecay = 1,
  mutationMin = 0.01,
  maxClones = Inf,
  stopTolerance = 0,
  noImprovementLimit = Inf,
  initMethod = c("sample", "random", "random_uniform", "kmeans++"),
  k = 3,
  scale = c("none", "zscore", "robust", "arcsinh"),
  targetK = NULL,
  epsilonQuantile = NULL,
  verbose = TRUE,
  ...
)
```

## Arguments

- X:

  A numeric matrix or data frame of input features, with rows as
  observations and columns as features.

- y:

  Optional. A factor target vector for classification. If NULL,
  clustering will be performed.

- task:

  Character. Specifies the task to perform: `"clustering"` or
  `"classification"`. If NULL, it is inferred based on `y`.

- nAntibodies:

  Integer. The initial population size of antibodies.

- beta:

  Numeric. Clone multiplier (controls how many clones are generated for
  top-matching antibodies).

- epsilon:

  Numeric. Similarity threshold used in network suppression; antibodies
  closer than `epsilon` are considered redundant.

- maxIter:

  Integer. Maximum number of iterations to run the AI-Net algorithm.

- affinityFunc:

  Character. Specifies the affinity (similarity) function to use for
  antibody-data matching. One of `"gaussian"`, `"laplace"`,
  `"polynomial"`, `"cosine"`, or `"hamming"`.

- distFunc:

  Character. Specifies the distance function for clustering and
  suppression. One of `"euclidean"`, `"manhattan"`, `"minkowski"`,
  `"cosine"`, `"mahalanobis"`, or `"hamming"`.

- affinityParams:

  A list of optional parameters for the chosen affinity or distance
  function.

  - `alpha` (for RBF or Laplace kernel),

  - `c`, `p` (for polynomial kernel or Minkowski distance),

  - `Sigma` (for Mahalanobis distance).

- mutationDecay:

  Numeric. Factor by which the mutation rate decays each iteration
  (should be \\\le 1.0\\). Default is 1.0 (no decay).

- mutationMin:

  Numeric. Minimum mutation rate, preventing the mutation scale from
  shrinking to zero.

- maxClones:

  Numeric. Maximum number of clones per top-matching antibody; defaults
  to `Inf`.

- stopTolerance:

  Numeric. If the change in the number of antibodies (repertoire size)
  is \\\le stopTolerance\\ for consecutive iterations, this may trigger
  the `noImprovementLimit`.

- noImprovementLimit:

  Integer. Stops the algorithm early if there is no further improvement
  in antibody count (beyond `stopTolerance`) for this many consecutive
  iterations. Default is `Inf`, meaning no early stop based on
  improvement.

- initMethod:

  Character. Method for initializing antibodies. Can be:

  - `"sample"` - randomly selects rows from `X` as initial antibodies.

  - `"random"` - samples Gaussian noise using `X`'s column means/sds.

  - `"random_uniform"` - samples uniformly in \[min, max\] of each
    column.

  - `"kmeans++"` - tries a kmeans++-like initialization for coverage.

- k:

  Integer. Number of top-matching antibodies (by affinity) to consider
  cloning for each data point.

- scale:

  Character. Per-feature input scaling: `"none"` (default), `"zscore"`,
  `"robust"` (median/IQR), or `"arcsinh"` (CyTOF). Passed to
  [`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md);
  makes `epsilon` and distances behave consistently across datasets of
  different magnitude.

- targetK:

  Integer or NULL. If set, force the clustering result to exactly
  `targetK` clusters via a seeded K-means refinement (the immune network
  supplies the seeds). NULL (default) keeps the emergent cluster count.

- epsilonQuantile:

  Numeric in (0, 1) or NULL. If set, the suppression threshold adapts
  each iteration to this quantile of pairwise antibody distances instead
  of the fixed `epsilon`.

- verbose:

  Logical. If `TRUE`, prints progress messages each iteration.

- ...:

  Additional arguments forwarded to
  [`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md),
  including immunology modules (`shm`, `idiotypic`, `germinalCenter`,
  `microenvironment`, `activation`, `memory`, `classSwitcher`, `init`)
  and `consolidate` / `consolidationSteps`.

## Value

A list:

- `antibodies`: Final antibody vectors (nAntibodies x nFeatures).

- `assignments`: - For clustering: integer cluster IDs in
  \[1..#Antibodies\]. - For classification: predicted labels.

- `task`: The chosen task.

## Examples

``` r
# Example 1: Clustering with the Iris dataset
data(iris)
X <- as.matrix(iris[, 1:4])  # Numeric features only
res <- bHIVE(X = X, 
             task = "clustering", 
             nAntibodies = 30, 
             beta = 5, 
             epsilon = 0.01, 
             maxIter = 20, 
             k = 3, 
             verbose = FALSE)
table(res$assignments)
#> 
#>  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 
#>  4  5  1  1  6  4 11  7 16  5  7  3  8  3  1  6  5  1  5  3 12  1  5  9 12  3 
#> 27 
#>  6 

# Example 2: Classification with Iris species
y <- iris$Species
res <- bHIVE(X = X, 
              y = y, 
              task = "classification", 
              nAntibodies = 30, 
              beta = 5, 
              epsilon = 0.01, 
              maxIter = 20, 
              k = 3, 
              verbose = FALSE)
table(res$assignments, y)
#>             y
#>              setosa versicolor virginica
#>   setosa         50          0         0
#>   versicolor      0         45         2
#>   virginica       0          5        48
```
