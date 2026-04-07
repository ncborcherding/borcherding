# ClassSwitcher

Implements antibody isotype/class switching, allowing antibodies to
change their matching breadth. Inspired by real B cell class switching
from IgM (broad, pentameric) to IgG (specific, monomeric) to IgA
(mucosal).

## Details

In bHIVE, class switching modifies the effective affinity kernel width:

- `IgM`: Broad matching (large kernel width) – good for initial
  exploration and capturing general patterns

- `IgG`: Specific matching (small kernel width) – good for fine-grained
  discrimination after patterns are identified

- `IgA`: Boundary patrol (medium kernel width) – good for maintaining
  coverage at decision boundaries

## Public fields

- `alpha_IgM`:

  Kernel width for IgM mode (broad).

- `alpha_IgG`:

  Kernel width for IgG mode (specific).

- `alpha_IgA`:

  Kernel width for IgA mode (boundary).

## Methods

### Public methods

- [`ClassSwitcher$new()`](#method-ClassSwitcher-new)

- [`ClassSwitcher$switch_isotypes()`](#method-ClassSwitcher-switch_isotypes)

- [`ClassSwitcher$get_alpha()`](#method-ClassSwitcher-get_alpha)

- [`ClassSwitcher$print()`](#method-ClassSwitcher-print)

- [`ClassSwitcher$clone()`](#method-ClassSwitcher-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new ClassSwitcher.

#### Usage

    ClassSwitcher$new(alpha_IgM = 0.1, alpha_IgG = 5, alpha_IgA = 1)

#### Arguments

- `alpha_IgM`:

  Numeric. Kernel width for broad matching.

- `alpha_IgG`:

  Numeric. Kernel width for specific matching.

- `alpha_IgA`:

  Numeric. Kernel width for boundary matching.

------------------------------------------------------------------------

### Method `switch_isotypes()`

Determine appropriate isotype for each antibody based on its
microenvironment zone.

#### Usage

    ClassSwitcher$switch_isotypes(repertoire, zones)

#### Arguments

- `repertoire`:

  An
  [`ImmuneRepertoire`](https://www.borch.dev/uploads/bhive/reference/ImmuneRepertoire.md).

- `zones`:

  Character vector from Microenvironment assessment.

#### Returns

Named numeric vector of alpha values per antibody.

------------------------------------------------------------------------

### Method `get_alpha()`

Get alpha value for a given isotype.

#### Usage

    ClassSwitcher$get_alpha(isotype)

#### Arguments

- `isotype`:

  Character. "IgM", "IgG", or "IgA".

#### Returns

Numeric.

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary.

#### Usage

    ClassSwitcher$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    ClassSwitcher$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Switch antibody isotypes based on microenvironment zones
A <- matrix(rnorm(50), nrow = 10, ncol = 5)
rep <- ImmuneRepertoire$new(A)
cs <- ClassSwitcher$new(alpha_IgM = 0.1, alpha_IgG = 5.0)
zones <- sample(c("stable", "explore", "boundary"), 10, replace = TRUE)
alphas <- cs$switch_isotypes(rep, zones)
table(rep$metadata$isotype)  # IgM, IgG, IgA distribution
#> 
#> IgA IgG IgM 
#>   1   3   6 
```
