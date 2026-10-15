# Visualize bHIVE/honeycombHIVE Results

Plots the data together with the prototypes learned by
[`bHIVE`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md) or
[`honeycombHIVE`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVE.md).
One or more layers can be shown, faceted by layer:

## Usage

``` r
visualizeHIVE(
  result,
  X = NULL,
  plot_type = c("scatter", "boxplot", "violin", "density"),
  feature = NULL,
  transform = TRUE,
  transformation_method = c("PCA", "UMAP", "tSNE", "none"),
  title = "HIVE Results",
  layer = 1,
  task = NULL,
  ...
)
```

## Arguments

- result:

  A list produced by `bHIVE` or `honeycombHIVE`. For multilayer results,
  each element represents one layer.

- X:

  A numeric matrix or data frame of the original input features, with
  the observations in the same order as the input to `bHIVE` or
  `honeycombHIVE`. Required.

- plot_type:

  Character string specifying the type of plot to generate. Options are:

  - `"scatter"`: A scatterplot of data points and prototypes.

  - `"boxplot"`: A boxplot of a selected feature by group with
    prototypes overlaid.

  - `"violin"`: A violin plot of a selected feature by group with
    prototypes overlaid.

  - `"density"`: Density plots of a selected feature by group with
    prototype markers.

- feature:

  Optional. For `"boxplot"`, `"violin"`, or `"density"` plots, the name
  or index of the feature in `X` to display. If `NULL`, the first column
  is used.

- transform:

  Logical. If `TRUE` and `X` has more than two columns, the
  dimensionality reduction in `transformation_method` is applied for
  scatterplots. Otherwise the first two columns are plotted.

- transformation_method:

  Character. The method used for dimensionality reduction. Options are
  `"PCA"`, `"UMAP"` (needs the umap package), `"tSNE"` (needs the Rtsne
  package), or `"none"`.

- title:

  Character. Title for the plot.

- layer:

  Integer vector indicating which layer(s) of the result to visualize.
  For bHIVE outputs, default is `1`. For multilayer honeycombHIVE
  outputs, specify one or more layer indices.

- task:

  Character, `"clustering"` or `"classification"`, or `NULL` (default)
  to use the task stored in `result`. Decides whether observations are
  grouped by cluster or by predicted class.

- ...:

  Additional arguments passed to the dimensionality reduction:
  [`stats::prcomp()`](https://rdrr.io/r/stats/prcomp.html),
  [`umap::umap()`](https://rdrr.io/pkg/umap/man/umap.html) or
  [`Rtsne::Rtsne()`](https://rdrr.io/pkg/Rtsne/man/Rtsne.html).

## Value

A `ggplot` object representing the visualization.

## Details

- `"scatter"`: The observations, colored by cluster or class, with the
  prototypes drawn on top in the same coordinates. When `X` has more
  than two columns and `transform` is `TRUE`, a dimensionality reduction
  is fitted to `X` and the prototypes are projected into it.

- `"boxplot"`, `"violin"`: A selected feature by group, with the
  prototypes' values overlaid.

- `"density"`: Density of a selected feature by group, with the
  prototypes' values marked.

For scatterplots the reduction is `"PCA"`, `"UMAP"`, `"tSNE"` or
`"none"`. PCA and UMAP are fitted to `X` only and the prototypes are
placed with the fitted model's
[`predict()`](https://rdrr.io/r/stats/predict.html) method, so both
share one coordinate system. UMAP's projection of new points is an
approximation. tSNE has no such projection, so the data and prototypes
are embedded together and the prototypes take a small part in shaping
the layout.

The prototypes drawn are, for a
[`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md)
result, the antibodies in original feature units
(`antibodies_unscaled`), and for a
[`honeycombHIVE()`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVE.md)
layer, the collapsed `prototypes` that summarize each cluster.

## Examples

``` r
data(iris)
X <- as.matrix(iris[, 1:4])

# A single bHIVE clustering, with the prototypes projected onto the PCA
set.seed(1)
res <- bHIVE(X, targetK = 3, maxIter = 10, verbose = FALSE)
visualizeHIVE(res, X = X, plot_type = "scatter", title = "bHIVE prototypes")


# Layers 1 and 2 of a honeycombHIVE hierarchy
res_h <- honeycombHIVE(X = X,
                       task = "clustering",
                       epsilon = 0.05,
                       layers = 3,
                       nAntibodies = 30,
                       beta = 5,
                       maxIter = 10,
                       verbose = FALSE)
visualizeHIVE(res_h, X = X, plot_type = "scatter", layer = 1:2,
              title = "honeycombHIVE layers")


# A feature by class for a classifier, with each antibody's value overlaid
res_c <- bHIVE(X, y = iris$Species, maxIter = 10, verbose = FALSE)
#> This fit cannot predict every class. virginica kept 5 antibodies and recovered 26% of its 50 observations. minPerClass seeds antibodies per class, but suppression removes them afterwards. Raise nAntibodies, lower epsilon, or raise minPerClass. See ?AINet.
visualizeHIVE(res_c, X = X, plot_type = "violin",
              feature = "Petal.Length", title = "Classifier")

```
