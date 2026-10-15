# bHIVE clustering through bluster

Run [`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
clustering through
[`clusterRows`](https://rdrr.io/pkg/bluster/man/clusterRows.html), the
bluster interface that
[`bluster::clusterSweep()`](https://rdrr.io/pkg/bluster/man/clusterSweep.html)
builds on. This makes bHIVE a drop-in alternative to the k-means, SOM
and graph-based clustering that bluster already wraps.

## Usage

``` r
bHIVEParam(
  nAntibodies = NULL,
  beta = NULL,
  epsilon = NULL,
  maxIter = NULL,
  k = NULL,
  affinityFunc = NULL,
  distFunc = NULL,
  initMethod = NULL,
  scale = NULL,
  targetK = NULL,
  epsilonQuantile = NULL,
  affinityParams = list(),
  ...
)

# S4 method for class 'bHIVEParam'
.defaultScalarArguments(x)

# S4 method for class 'bHIVEParam'
show(object)

# S4 method for class 'ANY,bHIVEParam'
clusterRows(x, BLUSPARAM, full = FALSE)
```

## Arguments

- nAntibodies, beta, epsilon, maxIter, k, affinityFunc, distFunc,
  initMethod, scale, targetK, epsilonQuantile:

  Scalar arguments passed to
  [`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md).
  `NULL` (the default) uses the
  [`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
  default. These can be varied with
  [`bluster::clusterSweep()`](https://rdrr.io/pkg/bluster/man/clusterSweep.html).

- affinityParams:

  Named list passed to
  [`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md),
  for example `list(alpha = "auto")`. An empty list uses the
  [`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
  default.

- ...:

  Further named arguments passed to
  [`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
  and [`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md),
  such as `coverageBoost`, `consolidate`, `verbose` or immunology
  modules (`shm`, `idiotypic`, ...). Note that R6 modules carry state,
  so a `MemoryPool` passed here is shared across every run that uses
  this parameter object.

- x:

  A numeric matrix-like object with observations in rows, or a
  `bHIVEParam` for `show()`.

- object:

  A `bHIVEParam` object.

- BLUSPARAM:

  A `bHIVEParam` object.

- full:

  Logical. Return the full
  [`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
  result as well as the clusters.

## Value

`bHIVEParam()` returns a `bHIVEParam` object, a subclass of
[BlusterParam](https://rdrr.io/pkg/bluster/man/BlusterParam-class.html).

[`clusterRows()`](https://rdrr.io/pkg/bluster/man/clusterRows.html)
returns a factor of cluster labels, one per row of `x`. With
`full = TRUE` it returns a list with `clusters` and `objects`, where
`objects$bHIVE` is the
[`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
result, including the fitted
[`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md) model
in `objects$bHIVE$model` for labeling new cells.

## Details

bHIVE learns a set of prototypes (antibodies) by clonal selection,
mutation and network suppression, then assigns each observation to its
nearest prototype. By default the number of clusters emerges from
suppression. Set `targetK` to force exactly that many clusters. For mass
cytometry, `scale = "arcsinh"` and
`affinityParams = list(alpha = "auto")` are good starting points.
Progress output is off unless `verbose = TRUE` is passed through `...`.

## See also

[`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md),
[`clusterRows`](https://rdrr.io/pkg/bluster/man/clusterRows.html),
[`clusterSweep`](https://rdrr.io/pkg/bluster/man/clusterSweep.html).

## Examples

``` r
library(bluster)
X <- as.matrix(iris[, 1:4])

p <- bHIVEParam(targetK = 3, maxIter = 10)
p
#> class: bHIVEParam
#> nAntibodies: [default]
#> beta: [default]
#> epsilon: [default]
#> maxIter: 10
#> k: [default]
#> affinityFunc: [default]
#> distFunc: [default]
#> initMethod: [default]
#> scale: [default]
#> targetK: 3
#> epsilonQuantile: [default]
#> affinityParams(0): 
#> extra(0): 
set.seed(1)
clusters <- clusterRows(X, p)
table(clusters, iris$Species)
#>         
#> clusters setosa versicolor virginica
#>        1      0         47        14
#>        2     50          0         0
#>        3      0          3        36

# Full output keeps the fitted model for labeling new cells
out <- clusterRows(X, p, full = TRUE)
out$objects$bHIVE$model$predict(X[1:5, ])
#>      [,1]
#> [1,]    3
#> [2,]    3
#> [3,]    3
#> [4,]    3
#> [5,]    3

# Sweep over parameters
sweep <- clusterSweep(X, bHIVEParam(maxIter = 5), nAntibodies = c(10, 30))
sweep$parameters
#> DataFrame with 2 rows and 1 column
#>                nAntibodies
#>                  <numeric>
#> nAntibodies.10          10
#> nAntibodies.30          30

# Cluster a SingleCellExperiment embedding and store the labels
library(SingleCellExperiment)
sce <- SingleCellExperiment(assays = list(logcounts = t(X)))
reducedDim(sce, "PCA") <- prcomp(X)$x[, 1:3]
colLabels(sce) <- clusterRows(reducedDim(sce, "PCA"), p)
table(colLabels(sce), iris$Species)
#>    
#>     setosa versicolor virginica
#>   1      0         48        14
#>   2     50          0         0
#>   3      0          2        36
```
