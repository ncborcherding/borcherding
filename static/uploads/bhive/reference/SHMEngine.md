# SHMEngine

Somatic Hypermutation Engine implementing five biologically- inspired
mutation strategies for the bHIVE artificial immune system.

## Details

The five strategies are:

- uniform:

  Classic random Gaussian noise. Mutation rate = (1-affinity) \*
  decay^(iter-1). This is the original bHIVE behavior.

- airs:

  AIRS-style affinity-proportional mutation. Rate = c \* exp(-affinity /
  T). From Watkins & Timmis (AIRS2), achieving 50% better data reduction
  than uniform.

- hotspot:

  Feature-importance-weighted mutation. Features with higher gradient
  magnitude mutate more, analogous to AID targeting WRCY motifs in real
  SHM.

- energy:

  Energy-budget-constrained mutation. Total mutation magnitude bounded
  by E = E_0 \* (1-affinity)^2, inspired by Kleinstein's E_SHM ~ N_Mut^2
  model.

- adaptive:

  Per-feature adaptive mutation rate with moment tracking, directly
  implementing SHM as the Adam optimizer.

## Public fields

- `method`:

  Character. One of "uniform", "airs", "hotspot", "energy", "adaptive".

- `params`:

  Named list of method-specific parameters.

- `m1_state`:

  First moment state matrix (for adaptive method).

- `m2_state`:

  Second moment state matrix (for adaptive method).

## Methods

### Public methods

- [`SHMEngine$new()`](#method-SHMEngine-new)

- [`SHMEngine$init_state()`](#method-SHMEngine-init_state)

- [`SHMEngine$reset_state()`](#method-SHMEngine-reset_state)

- [`SHMEngine$print()`](#method-SHMEngine-print)

- [`SHMEngine$clone()`](#method-SHMEngine-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new SHMEngine.

#### Usage

    SHMEngine$new(
      method = "uniform",
      decay = 1,
      mutationMin = 0.01,
      c_rate = 1,
      temperature = 0.5,
      E_0 = 1,
      base_rate = 0.1,
      beta1 = 0.9,
      beta2 = 0.999,
      adam_epsilon = 1e-08
    )

#### Arguments

- `method`:

  Character. Mutation strategy.

- `decay`:

  Numeric. Per-iteration mutation rate decay (uniform method).

- `mutationMin`:

  Numeric. Minimum mutation rate floor.

- `c_rate`:

  Numeric. Scaling constant (airs method).

- `temperature`:

  Numeric. Temperature parameter (airs method).

- `E_0`:

  Numeric. Energy budget base (energy method).

- `base_rate`:

  Numeric. Base mutation rate (hotspot, adaptive methods).

- `beta1`:

  Numeric. First moment decay (adaptive method, like Adam).

- `beta2`:

  Numeric. Second moment decay (adaptive method, like Adam).

- `adam_epsilon`:

  Numeric. Numerical stability (adaptive method).

------------------------------------------------------------------------

### Method `init_state()`

Initialize internal state for adaptive method.

#### Usage

    SHMEngine$init_state(nAntibodies, nFeatures)

#### Arguments

- `nAntibodies`:

  Integer. Number of antibodies.

- `nFeatures`:

  Integer. Number of features.

------------------------------------------------------------------------

### Method `reset_state()`

Reset moment states (e.g., after suppression changes antibody count).

#### Usage

    SHMEngine$reset_state(nAntibodies, nFeatures, kept_idx = NULL)

#### Arguments

- `nAntibodies`:

  Integer. New number of antibodies.

- `nFeatures`:

  Integer. Number of features.

- `kept_idx`:

  Integer vector. Indices of antibodies that were kept.

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Print summary.

#### Usage

    SHMEngine$print(...)

#### Arguments

- `...`:

  Not used.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    SHMEngine$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Create different SHM engines
shm_uniform  <- SHMEngine$new(method = "uniform")
shm_adaptive <- SHMEngine$new(method = "adaptive", base_rate = 0.1)
shm_airs     <- SHMEngine$new(method = "airs", temperature = 0.3)
print(shm_adaptive)
#> <SHMEngine> method='adaptive'
#>   base_rate: 0.1
#>   beta1: 0.9
#>   beta2: 0.999
```
