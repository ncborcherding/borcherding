# AINet

R6 implementation of the Artificial Immune Network algorithm. This is
the core bHIVE algorithm using C++ backends for performance-critical
operations. Supports composable modules for somatic hypermutation,
idiotypic network regulation, germinal center selection, and more.

## Super class

[`bHIVE::ImmuneAlgorithm`](https://www.borch.dev/uploads/bhive/reference/ImmuneAlgorithm.md)
-\> `AINet`

## Methods

### Public methods

- [`AINet$new()`](#method-AINet-new)

- [`AINet$fit()`](#method-AINet-fit)

- [`AINet$clone()`](#method-AINet-clone)

Inherited methods

- [`bHIVE::ImmuneAlgorithm$predict()`](https://www.borch.dev/uploads/bhive/reference/ImmuneAlgorithm.html#method-predict)
- [`bHIVE::ImmuneAlgorithm$print()`](https://www.borch.dev/uploads/bhive/reference/ImmuneAlgorithm.html#method-print)
- [`bHIVE::ImmuneAlgorithm$summary()`](https://www.borch.dev/uploads/bhive/reference/ImmuneAlgorithm.html#method-summary)

------------------------------------------------------------------------

### Method `new()`

Create a new AINet algorithm instance.

#### Usage

    AINet$new(
      nAntibodies = 20,
      beta = 5,
      epsilon = 0.01,
      maxIter = 50,
      k = 3,
      affinityFunc = "gaussian",
      distFunc = "euclidean",
      affinityParams = list(alpha = 1, c = 1, p = 2, Sigma = NULL),
      mutationDecay = 1,
      mutationMin = 0.01,
      maxClones = Inf,
      stopTolerance = 0,
      noImprovementLimit = Inf,
      initMethod = "sample",
      shm = NULL,
      init = NULL,
      activation = NULL,
      idiotypic = NULL,
      germinalCenter = NULL,
      microenvironment = NULL,
      memory = NULL,
      classSwitcher = NULL,
      verbose = TRUE
    )

#### Arguments

- `nAntibodies`:

  Integer. Initial antibody population size.

- `beta`:

  Numeric. Clone multiplier.

- `epsilon`:

  Numeric. Suppression distance threshold.

- `maxIter`:

  Integer. Maximum iterations.

- `k`:

  Integer. Top-k antibodies to clone per data point.

- `affinityFunc`:

  Character. Affinity function name.

- `distFunc`:

  Character. Distance function name.

- `affinityParams`:

  List. Parameters for affinity/distance functions.

- `mutationDecay`:

  Numeric. Per-iteration mutation rate decay.

- `mutationMin`:

  Numeric. Minimum mutation rate.

- `maxClones`:

  Numeric. Maximum clones per antibody.

- `stopTolerance`:

  Numeric. Early stopping tolerance.

- `noImprovementLimit`:

  Integer. Early stopping patience.

- `initMethod`:

  Character. Initialization method.

- `shm`:

  An SHMEngine instance or NULL for default uniform mutation.

- `init`:

  A VDJLibrary instance or NULL for default initialization.

- `activation`:

  An ActivationGate instance or NULL.

- `idiotypic`:

  An IdiotypicNetwork instance or NULL.

- `germinalCenter`:

  A GerminalCenter instance or NULL.

- `microenvironment`:

  A Microenvironment instance or NULL.

- `memory`:

  A MemoryPool instance or NULL.

- `classSwitcher`:

  A ClassSwitcher instance or NULL.

- `verbose`:

  Logical. Print progress.

------------------------------------------------------------------------

### Method `fit()`

Fit the AINet algorithm to data.

#### Usage

    AINet$fit(X, y = NULL, task = NULL, ...)

#### Arguments

- `X`:

  Numeric matrix or data frame (n x d).

- `y`:

  Optional factor target for classification.

- `task`:

  Character: "clustering" or "classification". Inferred from y if NULL.

- `...`:

  Additional arguments (currently unused).

#### Returns

Invisible self, with `result` populated.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    AINet$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Clustering with Iris data
data(iris)
X <- as.matrix(iris[, 1:4])
model <- AINet$new(nAntibodies = 15, maxIter = 10, verbose = FALSE)
model$fit(X, task = "clustering")
table(model$result$assignments)
#> 
#>  1  2  3  4  5  6  7  8  9 10 11 12 13 14 
#> 14 12 22  7 14  8 12  4 14 11 11 14  1  6 

# Classification
model2 <- AINet$new(nAntibodies = 20, maxIter = 10, verbose = FALSE)
model2$fit(X, iris$Species, task = "classification")
mean(model2$result$assignments == as.character(iris$Species))
#> [1] 0.8933333

# Predict on new data
preds <- model2$predict(X[1:10, ])
```
