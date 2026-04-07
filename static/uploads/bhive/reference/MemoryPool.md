# MemoryPool

Manages long-lived memory cells that can be recalled when distribution
shifts are detected. Implements the immunological distinction between
short-lived effector cells and long-lived memory cells.

## Public fields

- `memory_cells`:

  Numeric matrix of archived memory antibodies.

- `memory_metadata`:

  Data frame of metadata for memory cells.

- `archive_threshold`:

  Affinity threshold for archiving (only high-quality antibodies become
  memory).

- `max_memory`:

  Maximum number of memory cells to store.

- `recall_threshold`:

  Threshold for triggering memory recall.

## Methods

### Public methods

- [`MemoryPool$new()`](#method-MemoryPool-new)

- [`MemoryPool$archive()`](#method-MemoryPool-archive)

- [`MemoryPool$recall()`](#method-MemoryPool-recall)

- [`MemoryPool$size()`](#method-MemoryPool-size)

- [`MemoryPool$print()`](#method-MemoryPool-print)

- [`MemoryPool$clone()`](#method-MemoryPool-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new MemoryPool.

#### Usage

    MemoryPool$new(
      archive_threshold = 0.5,
      max_memory = 100,
      recall_threshold = 0.3
    )

#### Arguments

- `archive_threshold`:

  Numeric. Minimum average affinity to archive.

- `max_memory`:

  Integer. Maximum memory cells.

- `recall_threshold`:

  Numeric. Minimum affinity to recall a memory.

------------------------------------------------------------------------

### Method `archive()`

Archive high-performing antibodies as memory cells.

#### Usage

    MemoryPool$archive(
      repertoire,
      X,
      affinityFunc = "gaussian",
      affinityParams = list(alpha = 1, c = 1, p = 2)
    )

#### Arguments

- `repertoire`:

  An
  [`ImmuneRepertoire`](https://www.borch.dev/uploads/bhive/reference/ImmuneRepertoire.md).

- `X`:

  Training data matrix.

- `affinityFunc`:

  Character. Affinity function.

- `affinityParams`:

  List. Affinity parameters.

#### Returns

Integer. Number of new memory cells archived.

------------------------------------------------------------------------

### Method `recall()`

Recall memory cells relevant to current data.

#### Usage

    MemoryPool$recall(
      X,
      affinityFunc = "gaussian",
      affinityParams = list(alpha = 1, c = 1, p = 2)
    )

#### Arguments

- `X`:

  Data matrix to match against memory.

- `affinityFunc`:

  Character. Affinity function.

- `affinityParams`:

  List. Affinity parameters.

#### Returns

Numeric matrix of recalled memory cells (may be empty).

------------------------------------------------------------------------

### Method `size()`

Get current memory pool size.

#### Usage

    MemoryPool$size()

#### Returns

Integer.

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary.

#### Usage

    MemoryPool$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    MemoryPool$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Archive and recall memory cells
data(iris)
X <- as.matrix(iris[, 1:4])
A <- X[sample(150, 10), ]
mp <- MemoryPool$new(archive_threshold = 0.01)
rep <- ImmuneRepertoire$new(A)
mp$archive(rep, X)
#> [1] 10
mp$size()  # number of archived memories
#> [1] 10
recalled <- mp$recall(X[1:5, ])
nrow(recalled)  # memories relevant to query
#> [1] 5
```
