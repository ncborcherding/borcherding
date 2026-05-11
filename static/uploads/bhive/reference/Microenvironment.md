# Microenvironment

Models local microenvironment cues that influence antibody behavior
based on the density and structure of nearby data points.

## Details

In real immunity, B cell fate is strongly influenced by local signals:
chemokines, cytokines, and interactions with stromal cells in specific
tissue microenvironments. This module translates that concept into
density-dependent adaptation:

- **High density zones**: Promote memory formation (stabilize
  antibodies, reduce mutation rate)

- **Low density zones**: Promote exploration (increase mutation rate for
  broader search)

- **Boundary zones**: Trigger class switching (change matching breadth
  between IgM-like broad and IgG-like specific modes)

- **Chemokine-like gradients**: Bias mutation direction toward
  higher-density regions

## Public fields

- `density_bandwidth`:

  Bandwidth for kernel density estimation.

- `high_density_threshold`:

  Density percentile above which antibodies stabilize.

- `low_density_threshold`:

  Density percentile below which antibodies explore.

- `stabilization_factor`:

  Mutation rate multiplier for high-density zones.

- `exploration_factor`:

  Mutation rate multiplier for low-density zones.

- `last_densities`:

  Per-antibody local density from last assessment.

- `last_zones`:

  Per-antibody zone classification from last assessment.

## Methods

### Public methods

- [`Microenvironment$new()`](#method-Microenvironment-new)

- [`Microenvironment$assess()`](#method-Microenvironment-assess)

- [`Microenvironment$print()`](#method-Microenvironment-print)

- [`Microenvironment$clone()`](#method-Microenvironment-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new Microenvironment module.

#### Usage

    Microenvironment$new(
      density_bandwidth = NULL,
      high_density_threshold = 0.75,
      low_density_threshold = 0.25,
      stabilization_factor = 0.3,
      exploration_factor = 2
    )

#### Arguments

- `density_bandwidth`:

  Numeric. KDE bandwidth (NULL for auto).

- `high_density_threshold`:

  Numeric \[0,1\]. Percentile threshold for stabilization.

- `low_density_threshold`:

  Numeric \[0,1\]. Percentile threshold for exploration.

- `stabilization_factor`:

  Numeric. Mutation rate multiplier for stable zones.

- `exploration_factor`:

  Numeric. Mutation rate multiplier for exploration zones.

------------------------------------------------------------------------

### Method `assess()`

Assess the microenvironment around each antibody.

#### Usage

    Microenvironment$assess(
      repertoire,
      X,
      affinityFunc = "gaussian",
      affinityParams = list(alpha = 1, c = 1, p = 2)
    )

#### Arguments

- `repertoire`:

  An
  [`ImmuneRepertoire`](https://www.borch.dev/uploads/bhive/reference/ImmuneRepertoire.md)
  object.

- `X`:

  Numeric matrix of training data (n x d).

- `affinityFunc`:

  Character. Affinity function.

- `affinityParams`:

  List. Affinity parameters.

#### Returns

Named list with densities, zones, and mutation_modifiers per antibody.

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary.

#### Usage

    Microenvironment$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    Microenvironment$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Assess microenvironment around antibodies
data(iris)
X <- as.matrix(iris[, 1:4])
me <- Microenvironment$new()
rep <- ImmuneRepertoire$new(X[sample(150, 15), ])
env <- me$assess(rep, X)
table(env$zones)  # stable, explore, boundary
#> 
#> boundary  explore   stable 
#>        7        4        4 
env$mutation_modifiers  # per-antibody rate scaling
#>  [1] 2.0 1.0 0.3 1.0 2.0 1.0 2.0 1.0 1.0 1.0 1.0 0.3 0.3 2.0 0.3
```
