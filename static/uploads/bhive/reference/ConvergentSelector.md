# ConvergentSelector

Identifies "public antibodies" shared across independent repertoires,
implementing the concept of convergent selection from TCR/BCR immunology
as a biologically-motivated ensemble method.

## Details

In real immunity, certain immune receptor sequences appear across
multiple individuals (public clones), suggesting they are driven by
common selection pressures. Similarly, antibodies that appear across
multiple independent bHIVE runs represent the most robust patterns in
the data.

## Public fields

- `tolerance`:

  Distance tolerance for matching antibodies across repertoires.

- `min_appearances`:

  Minimum number of repertoires an antibody must appear in to be
  considered "public".

- `public_antibodies`:

  The identified public antibodies.

## Methods

### Public methods

- [`ConvergentSelector$new()`](#method-ConvergentSelector-new)

- [`ConvergentSelector$find_public()`](#method-ConvergentSelector-find_public)

- [`ConvergentSelector$from_results()`](#method-ConvergentSelector-from_results)

- [`ConvergentSelector$print()`](#method-ConvergentSelector-print)

- [`ConvergentSelector$clone()`](#method-ConvergentSelector-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new ConvergentSelector.

#### Usage

    ConvergentSelector$new(tolerance = 0.5, min_appearances = 2)

#### Arguments

- `tolerance`:

  Numeric. Maximum distance for two antibodies to be considered the same
  across repertoires.

- `min_appearances`:

  Integer. Minimum repertoires for an antibody to be public.

------------------------------------------------------------------------

### Method `find_public()`

Find public antibodies shared across multiple repertoires.

#### Usage

    ConvergentSelector$find_public(repertoires, distFunc = "euclidean")

#### Arguments

- `repertoires`:

  List of ImmuneRepertoire objects or list of antibody matrices.

- `distFunc`:

  Character. Distance function for matching.

#### Returns

Numeric matrix of public (consensus) antibodies.

------------------------------------------------------------------------

### Method `from_results()`

Run convergent selection from multiple bHIVE results.

#### Usage

    ConvergentSelector$from_results(results, distFunc = "euclidean")

#### Arguments

- `results`:

  List of bHIVE result objects (each with \$antibodies).

- `distFunc`:

  Character. Distance function.

#### Returns

Numeric matrix of consensus antibodies.

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary.

#### Usage

    ConvergentSelector$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    ConvergentSelector$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Find public antibodies across multiple runs
data(iris)
X <- as.matrix(iris[, 1:4])
results <- lapply(1:3, function(i) {
  m <- AINet$new(nAntibodies = 15, maxIter = 5, verbose = FALSE)
  m$fit(X, task = "clustering")
  m$result
})
conv <- ConvergentSelector$new(tolerance = 1.0, min_appearances = 2)
public <- conv$from_results(results)
nrow(public)  # consensus antibodies
#> [1] 13
```
