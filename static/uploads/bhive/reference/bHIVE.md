# bHIVE: B-cell Hybrid Immune Variant Engine

Implements an artificial immune network algorithm for clustering and
classification tasks. The algorithm evolves a population of "antibodies"
via clonal selection and mutation, applies network suppression to
maintain diversity, and assigns data points based on affinity or
distance metrics.

## Usage

``` r
bHIVE(X, ...)

# S4 method for class 'ANY'
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

# S4 method for class 'SummarizedExperiment'
bHIVE(X, y = NULL, ..., assay.type = "logcounts", name = "bHIVE")

# S4 method for class 'SingleCellExperiment'
bHIVE(
  X,
  y = NULL,
  ...,
  assay.type = "logcounts",
  use.dimred = NULL,
  name = "bHIVE"
)
```

## Arguments

- X:

  A numeric matrix or data frame of input features, with rows as
  observations and columns as features. Or a SummarizedExperiment or
  SingleCellExperiment with features in rows and cells in columns.

- ...:

  Additional arguments forwarded to
  [`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md),
  including immunology modules (`shm`, `idiotypic`, `germinalCenter`,
  `microenvironment`, `activation`, `memory`, `classSwitcher`, `init`),
  `consolidate` / `consolidationSteps`, `coverageBoost` and, for
  classification, `minPerClass` (antibodies seeded per class, default
  5). For the SummarizedExperiment methods, all arguments of the matrix
  method.

- y:

  Optional. A factor target vector for classification. If NULL,
  clustering will be performed. For SummarizedExperiment input, `y` may
  also be the name of a
  [`colData()`](https://rdrr.io/pkg/SummarizedExperiment/man/SummarizedExperiment-class.html)
  column holding the labels.

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

  - `alpha` (for RBF or Laplace kernel). `"auto"` sets the bandwidth by
    the median heuristic, which is recommended for high-dimensional data
    such as mass cytometry.

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

  Logical. If `TRUE`, reports progress each iteration with
  [`message()`](https://rdrr.io/r/base/message.html).

- assay.type:

  String or integer. The assay holding the features to cluster, for
  SummarizedExperiment input. Ignored when `use.dimred` is set.

- name:

  String. The
  [`colData()`](https://rdrr.io/pkg/SummarizedExperiment/man/SummarizedExperiment-class.html)
  column (and `metadata()` entry) the results are stored under.

- use.dimred:

  String or integer. The
  [`reducedDim()`](https://rdrr.io/pkg/SingleCellExperiment/man/reducedDims.html)
  embedding to cluster, for SingleCellExperiment input. Takes precedence
  over `assay.type`. Recommended for sparse single-cell RNA-seq, since
  an assay is converted to a dense matrix.

## Value

For matrix or data frame input, a list:

- `antibodies`: Final prototype matrix (prototypes x features), in the
  scaled space the model was trained in.

- `assignments`: For clustering, integer cluster IDs, where cluster `i`
  is row `i` of `antibodies`. For classification, the predicted class
  labels.

- `antibody_classes`: Classification only. The class label of each
  antibody.

- `antibody_index`: Classification only. The row of `antibodies` that
  labeled each observation.

- `antibodies_unscaled`: The prototypes back-transformed to the original
  feature units.

- `task`: The chosen task.

- `model`: The fitted
  [`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md)
  object. Use `res$model$predict(newdata)` to label new observations.

For SummarizedExperiment or SingleCellExperiment input, `X` with the
labels added as a factor column `colData(X)[[name]]` and the full result
list above in `metadata(X)[[name]]`.

## Details

`bHIVE()` accepts a plain matrix or data frame (observations in rows) or
a
[SummarizedExperiment](https://rdrr.io/pkg/SummarizedExperiment/man/SummarizedExperiment-class.html)
/
[SingleCellExperiment](https://rdrr.io/pkg/SingleCellExperiment/man/SingleCellExperiment.html)
(features in rows, cells in columns, the Bioconductor convention). For
the latter, the cells are clustered or classified using an assay or, for
a SingleCellExperiment, a
[`reducedDim()`](https://rdrr.io/pkg/SingleCellExperiment/man/reducedDims.html)
embedding, and the labels are stored in
[`colData()`](https://rdrr.io/pkg/SummarizedExperiment/man/SummarizedExperiment-class.html).
To use bHIVE through bluster, see
[`bHIVEParam`](https://www.borch.dev/uploads/bhive/reference/bHIVEParam.md).

## See also

[`bHIVEParam`](https://www.borch.dev/uploads/bhive/reference/bHIVEParam.md)
for bluster integration,
[`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md) for
the underlying R6 engine.

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
#>  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 
#>  2 13  7  6  8  4 11  6  3  1 11  1 21  3 12  2  7  2 12  3 15 

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
#>   versicolor      0         47        14
#>   virginica       0          3        36

# Example 3: SingleCellExperiment input (features x cells)
library(SingleCellExperiment)
#> Loading required package: SummarizedExperiment
#> Loading required package: MatrixGenerics
#> Loading required package: matrixStats
#> 
#> Attaching package: ‘MatrixGenerics’
#> The following objects are masked from ‘package:matrixStats’:
#> 
#>     colAlls, colAnyNAs, colAnys, colAvgsPerRowSet, colCollapse,
#>     colCounts, colCummaxs, colCummins, colCumprods, colCumsums,
#>     colDiffs, colIQRDiffs, colIQRs, colLogSumExps, colMadDiffs,
#>     colMads, colMaxs, colMeans2, colMedians, colMins, colOrderStats,
#>     colProds, colQuantiles, colRanges, colRanks, colSdDiffs, colSds,
#>     colSums2, colTabulates, colVarDiffs, colVars, colWeightedMads,
#>     colWeightedMeans, colWeightedMedians, colWeightedSds,
#>     colWeightedVars, rowAlls, rowAnyNAs, rowAnys, rowAvgsPerColSet,
#>     rowCollapse, rowCounts, rowCummaxs, rowCummins, rowCumprods,
#>     rowCumsums, rowDiffs, rowIQRDiffs, rowIQRs, rowLogSumExps,
#>     rowMadDiffs, rowMads, rowMaxs, rowMeans2, rowMedians, rowMins,
#>     rowOrderStats, rowProds, rowQuantiles, rowRanges, rowRanks,
#>     rowSdDiffs, rowSds, rowSums2, rowTabulates, rowVarDiffs, rowVars,
#>     rowWeightedMads, rowWeightedMeans, rowWeightedMedians,
#>     rowWeightedSds, rowWeightedVars
#> Loading required package: GenomicRanges
#> Loading required package: stats4
#> Loading required package: BiocGenerics
#> Loading required package: generics
#> 
#> Attaching package: ‘generics’
#> The following objects are masked from ‘package:base’:
#> 
#>     as.difftime, as.factor, as.ordered, intersect, is.element, setdiff,
#>     setequal, union
#> 
#> Attaching package: ‘BiocGenerics’
#> The following objects are masked from ‘package:stats’:
#> 
#>     IQR, mad, sd, var, xtabs
#> The following objects are masked from ‘package:base’:
#> 
#>     Filter, Find, Map, Position, Reduce, anyDuplicated, aperm, append,
#>     as.data.frame, basename, cbind, colnames, dirname, do.call,
#>     duplicated, eval, evalq, get, grep, grepl, is.unsorted, lapply,
#>     mapply, match, mget, order, paste, pmax, pmax.int, pmin, pmin.int,
#>     rank, rbind, rownames, sapply, saveRDS, table, tapply, unique,
#>     unsplit, which.max, which.min
#> Loading required package: S4Vectors
#> 
#> Attaching package: ‘S4Vectors’
#> The following object is masked from ‘package:utils’:
#> 
#>     findMatches
#> The following objects are masked from ‘package:base’:
#> 
#>     I, expand.grid, unname
#> Loading required package: IRanges
#> Loading required package: Seqinfo
#> Loading required package: Biobase
#> Welcome to Bioconductor
#> 
#>     Vignettes contain introductory material; view with
#>     'browseVignettes()'. To cite Bioconductor, see
#>     'citation("Biobase")', and for packages 'citation("pkgname")'.
#> 
#> Attaching package: ‘Biobase’
#> The following object is masked from ‘package:MatrixGenerics’:
#> 
#>     rowMedians
#> The following objects are masked from ‘package:matrixStats’:
#> 
#>     anyMissing, rowMedians
sce <- SingleCellExperiment(assays = list(logcounts = t(X)),
                            colData = DataFrame(species = iris$Species))
sce <- bHIVE(sce, targetK = 3, maxIter = 10, verbose = FALSE)
table(sce$bHIVE, sce$species)
#>    
#>     setosa versicolor virginica
#>   1     50          0         0
#>   2      0         48        14
#>   3      0          2        36

# Cluster on an embedding, or classify with a colData column as labels
reducedDim(sce, "PCA") <- prcomp(X)$x[, 1:2]
sce <- bHIVE(sce, use.dimred = "PCA", name = "bHIVE_pca", verbose = FALSE)
sce <- bHIVE(sce, y = "species", name = "bHIVE_class", verbose = FALSE)
mean(sce$bHIVE_class == sce$species)
#> [1] 0.8466667
```
