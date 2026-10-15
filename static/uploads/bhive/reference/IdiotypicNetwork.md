# IdiotypicNetwork

Implements Jerne's idiotypic network theory for antibody repertoire
regulation. Replaces crude epsilon-threshold suppression with principled
network dynamics based on Varela & Coutinho's (1991) second- generation
immune network model.

## Value

An [`R6Class`](https://r6.r-lib.org/reference/R6Class.html) generator.
`IdiotypicNetwork$new()` returns an `IdiotypicNetwork` object.

## Details

The idiotypic network models antibody-antibody interactions where each
antibody's variable region can be recognized by other antibodies. This
creates a regulatory network with emergent properties:

\- A bell-shaped (double-threshold) activation function: too little
stimulation leads to cell death, moderate stimulation to activation, and
excessive stimulation to suppression. - Population dynamics with source,
decay, activation, and suppression terms. - Self-organized repertoire
structure with memory and tolerance properties.

This is the single most novel contribution of the overhauled bHIVE
package. No existing AIS implementation uses idiotypic network dynamics
for repertoire regulation.

## Experimental

The activation rule is applied to each antibody pair and the responses
are summed: every neighbor whose affinity falls outside
`[theta_low, theta_high]` counts as one unit of suppression. In a small,
tight repertoire this culls crowded and isolated antibodies as intended
(see the example). In a large or spread-out repertoire most pairs are
far apart, their affinity is near zero, and every antibody is
suppressed. `regulate()` then warns and leaves the repertoire unchanged,
and [`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md)
keeps the top 10% by population and reports it with a message. Treat the
module as experimental and check that antibodies survive on your data. A
field-based form, in which the activation acts on the total stimulation
each antibody receives, is planned.

## Public fields

- `theta_low`:

  Lower activation threshold. Below this, cells die.

- `theta_high`:

  Upper activation threshold. Above this, cells are suppressed.

- `source_rate`:

  Rate of new cell generation (basal production).

- `decay_rate`:

  Natural cell death rate.

- `dt`:

  Time step for Euler integration.

- `timeSteps`:

  Number of simulation time steps.

- `survival_threshold`:

  Minimum population level to survive.

- `last_dynamics`:

  Result from the last regulation step.

## Methods

### Public methods

- [`IdiotypicNetwork$new()`](#method-IdiotypicNetwork-new)

- [`IdiotypicNetwork$regulate()`](#method-IdiotypicNetwork-regulate)

- [`IdiotypicNetwork$get_network()`](#method-IdiotypicNetwork-get_network)

- [`IdiotypicNetwork$get_population()`](#method-IdiotypicNetwork-get_population)

- [`IdiotypicNetwork$format()`](#method-IdiotypicNetwork-format)

- [`IdiotypicNetwork$clone()`](#method-IdiotypicNetwork-clone)

------------------------------------------------------------------------

### Method `new()`

Create a new IdiotypicNetwork regulator.

#### Usage

    IdiotypicNetwork$new(
      theta_low = 0.01,
      theta_high = 0.5,
      source_rate = 0.5,
      decay_rate = 0.1,
      dt = 0.1,
      timeSteps = 20,
      survival_threshold = 0.5
    )

#### Arguments

- `theta_low`:

  Lower activation threshold.

- `theta_high`:

  Upper activation threshold.

- `source_rate`:

  Basal cell production rate.

- `decay_rate`:

  Natural decay rate.

- `dt`:

  Euler integration time step.

- `timeSteps`:

  Number of dynamics simulation steps.

- `survival_threshold`:

  Minimum population to survive.

------------------------------------------------------------------------

### Method `regulate()`

Run idiotypic network dynamics on an antibody repertoire.

#### Usage

    IdiotypicNetwork$regulate(
      repertoire,
      affinityFunc = "gaussian",
      affinityParams = list(alpha = 1, c = 1, p = 2)
    )

#### Arguments

- `repertoire`:

  An
  [`ImmuneRepertoire`](https://www.borch.dev/uploads/bhive/reference/ImmuneRepertoire.md)
  object.

- `affinityFunc`:

  Character. Affinity function for Ab-Ab interactions.

- `affinityParams`:

  List. Parameters for the affinity function.

#### Returns

Invisible self. The repertoire is modified in place (dead antibodies
removed). Access `$last_dynamics` for full results.

------------------------------------------------------------------------

### Method `get_network()`

Get the Ab-Ab affinity matrix from the last regulation.

#### Usage

    IdiotypicNetwork$get_network()

#### Returns

Numeric matrix (m x m) or NULL if not yet run.

------------------------------------------------------------------------

### Method `get_population()`

Get population levels from the last regulation.

#### Usage

    IdiotypicNetwork$get_population()

#### Returns

Numeric vector or NULL if not yet run.

------------------------------------------------------------------------

### Method [`format()`](https://rdrr.io/r/base/format.html)

Format a short summary, one element per line. Used by
[`print()`](https://rdrr.io/r/base/print.html).

#### Usage

    IdiotypicNetwork$format(...)

#### Arguments

- `...`:

  Not used.

#### Returns

A character vector.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    IdiotypicNetwork$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.

## Examples

``` r
# Four antibodies with pairwise affinity 0.25 (inside the default
# activation window) stimulate each other and survive. A fifth, far from
# the rest, is under-stimulated and dies.
a <- sqrt(log(4) / 2)
A <- rbind(cbind(diag(4) * a, 0), c(0, 0, 0, 0, 10))
rep <- ImmuneRepertoire$new(A)
idi <- IdiotypicNetwork$new(theta_low = 0.01, theta_high = 0.5)
idi$regulate(rep, "gaussian", list(alpha = 1))
print(idi)
#> <IdiotypicNetwork>
#>   Activation window: [0.010, 0.500]
#>   Dynamics: 20 steps (dt=0.100)
#>   Source: 0.500  Decay: 0.100  Survival: 0.500
#>   Last run: 4/5 antibodies survived
rep$size()
#> [1] 4
```
