# ImmuneRepertoire

R6 class representing a collection of antibodies (immune cells) with
associated metadata. Core data structure for bHIVE algorithms.

## Details

An ImmuneRepertoire holds a matrix of antibody vectors (each row is one
antibody in feature space) plus per-antibody metadata (isotype, state,
age, lineage). All heavy computation is dispatched to C++ via
RcppArmadillo.

## Public fields

- `cells`:

  Numeric matrix (nAntibodies x nFeatures).

- `metadata`:

  Data frame with per-antibody attributes.

## Methods

### Public methods

- [`ImmuneRepertoire$new()`](#method-ImmuneRepertoire-new)

- [`ImmuneRepertoire$affinity_matrix()`](#method-ImmuneRepertoire-affinity_matrix)

- [`ImmuneRepertoire$distance_matrix()`](#method-ImmuneRepertoire-distance_matrix)

- [`ImmuneRepertoire$suppress()`](#method-ImmuneRepertoire-suppress)

- [`ImmuneRepertoire$size()`](#method-ImmuneRepertoire-size)

- [`ImmuneRepertoire$n_features()`](#method-ImmuneRepertoire-n_features)

- [`ImmuneRepertoire$subset()`](#method-ImmuneRepertoire-subset)

- [`ImmuneRepertoire$add()`](#method-ImmuneRepertoire-add)

- [`ImmuneRepertoire$age_all()`](#method-ImmuneRepertoire-age_all)

- [`ImmuneRepertoire$as_matrix()`](#method-ImmuneRepertoire-as_matrix)

- [`ImmuneRepertoire$print()`](#method-ImmuneRepertoire-print)

- [`ImmuneRepertoire$clone()`](#method-ImmuneRepertoire-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new ImmuneRepertoire.

#### Usage

    ImmuneRepertoire$new(cells, metadata = NULL)

#### Arguments

- `cells`:

  Numeric matrix (nAntibodies x nFeatures).

- `metadata`:

  Optional data frame with columns: isotype, state, age, lineage.

------------------------------------------------------------------------

### Method `affinity_matrix()`

Compute affinity matrix between data X and antibodies.

#### Usage

    ImmuneRepertoire$affinity_matrix(
      X,
      method = "gaussian",
      params = list(alpha = 1, c = 1, p = 2)
    )

#### Arguments

- `X`:

  Numeric matrix (n x d) of data points.

- `method`:

  Affinity function: "gaussian", "laplace", "polynomial", "cosine",
  "hamming".

- `params`:

  List with alpha, c, p parameters.

#### Returns

Numeric matrix (n x m) of affinity values.

------------------------------------------------------------------------

### Method `distance_matrix()`

Compute distance matrix between data X and antibodies.

#### Usage

    ImmuneRepertoire$distance_matrix(
      X,
      method = "euclidean",
      params = list(p = 2, Sigma = NULL)
    )

#### Arguments

- `X`:

  Numeric matrix (n x d).

- `method`:

  Distance function: "euclidean", "manhattan", "minkowski", "cosine",
  "mahalanobis", "hamming".

- `params`:

  List with p, Sigma parameters.

#### Returns

Numeric matrix (n x m) of distances.

------------------------------------------------------------------------

### Method `suppress()`

Network suppression: remove redundant antibodies.

#### Usage

    ImmuneRepertoire$suppress(
      epsilon,
      method = "euclidean",
      params = list(p = 2, Sigma = NULL)
    )

#### Arguments

- `epsilon`:

  Distance threshold for suppression.

- `method`:

  Distance function for suppression.

- `params`:

  List with p, Sigma parameters.

#### Returns

Invisible self (modified in place).

------------------------------------------------------------------------

### Method `size()`

Get number of antibodies.

#### Usage

    ImmuneRepertoire$size()

#### Returns

Integer.

------------------------------------------------------------------------

### Method `n_features()`

Get number of features.

#### Usage

    ImmuneRepertoire$n_features()

#### Returns

Integer.

------------------------------------------------------------------------

### Method [`subset()`](https://rdrr.io/r/base/subset.html)

Subset the repertoire.

#### Usage

    ImmuneRepertoire$subset(idx)

#### Arguments

- `idx`:

  Integer vector of row indices to keep.

#### Returns

Invisible self (modified in place).

------------------------------------------------------------------------

### Method `add()`

Add antibodies to the repertoire.

#### Usage

    ImmuneRepertoire$add(new_cells, new_metadata = NULL)

#### Arguments

- `new_cells`:

  Numeric matrix (k x d) of new antibodies.

- `new_metadata`:

  Optional data frame of metadata for new antibodies.

#### Returns

Invisible self (modified in place).

------------------------------------------------------------------------

### Method `age_all()`

Increment age of all antibodies.

#### Usage

    ImmuneRepertoire$age_all()

#### Returns

Invisible self (modified in place).

------------------------------------------------------------------------

### Method `as_matrix()`

Convert to plain matrix.

#### Usage

    ImmuneRepertoire$as_matrix()

#### Returns

Numeric matrix (nAntibodies x nFeatures).

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary.

#### Usage

    ImmuneRepertoire$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    ImmuneRepertoire$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Create a repertoire from random antibodies
A <- matrix(rnorm(50), nrow = 10, ncol = 5)
rep <- ImmuneRepertoire$new(A)
print(rep)
#> <ImmuneRepertoire> 10 antibodies x 5 features
#>   Isotypes: 10 
#>   States:   10 

# Compute affinity to data
X <- matrix(rnorm(100), nrow = 20, ncol = 5)
aff <- rep$affinity_matrix(X, "gaussian", list(alpha = 1))
dim(aff)  # 20 x 10
#> [1] 20 10

# Network suppression
rep$suppress(epsilon = 1.5, method = "euclidean")
rep$size()  # fewer antibodies after suppression
#> [1] 8
```
