# Algorithm & Biological Foundations

## Overview

This article describes the mathematical formulation and biological
motivation for every component of bHIVE. It is intended as a reference
companion to the tutorial vignettes and is organized to mirror the
algorithm’s execution flow: initialization, affinity computation, clonal
selection, mutation, regulation, and assignment.

Throughout, we use the following notation:

| Symbol                                     | Meaning                                       |
|:-------------------------------------------|:----------------------------------------------|
| $\mathbf{X} \in {\mathbb{R}}^{n \times d}$ | Data matrix ($n$ observations, $d$ features)  |
| $\mathbf{A} \in {\mathbb{R}}^{m \times d}$ | Antibody (prototype) matrix ($m$ antibodies)  |
| $\mathbf{x}_{i}$                           | The $i$-th data point (row of $\mathbf{X}$)   |
| $\mathbf{a}_{j}$                           | The $j$-th antibody (row of $\mathbf{A}$)     |
| $f(\mathbf{x},\mathbf{a})$                 | Affinity between a data point and an antibody |
| $d(\mathbf{x},\mathbf{a})$                 | Distance between a data point and an antibody |

------------------------------------------------------------------------

## Shape Space and Affinity

### Biological context

In immunology, **shape space** (Perelson & Oster 1979) is the abstract
space in which an antibody’s binding site (paratope) and an antigen’s
epitope are represented as points. Affinity is a function of distance in
this space, with closer shapes bind more tightly. The shape space
framework provides the geometric foundation for all AIS algorithms: data
points are antigens, prototypes are antibodies, and learning is the
process of moving antibodies through shape space to maximize affinity to
the data.

### Affinity kernels

bHIVE computes an $n \times m$ affinity matrix $\mathbf{F}$ where
$F_{ij} = f\left( \mathbf{x}_{i},\mathbf{a}_{j} \right)$. Five kernels
are available:

#### Gaussian (RBF)

$$f_{\text{gauss}}(\mathbf{x},\mathbf{a}) = \exp\!( - \alpha \parallel \mathbf{x} - \mathbf{a} \parallel^{2})$$

The default kernel. The bandwidth parameter $\alpha$ controls how
quickly affinity decays with distance. Larger $\alpha$ produces sharper,
more localized affinity peaks.

#### Laplace

$$f_{\text{lap}}(\mathbf{x},\mathbf{a}) = \exp\!( - \alpha \parallel \mathbf{x} - \mathbf{a} \parallel )$$

Similar to Gaussian but decays with L1-like (linear) distance rather
than squared distance. Produces heavier tails, making it more robust to
outliers.

#### Polynomial

$$f_{\text{poly}}(\mathbf{x},\mathbf{a}) = (\mathbf{x} \cdot \mathbf{a} + c)^{p}$$

A dot-product kernel where $c$ is a bias term and $p$ is the polynomial
degree. Captures non-Euclidean similarity structure. Useful when the
relevant signal is in the angle and magnitude of feature vectors rather
than their Euclidean distance.

#### Cosine

$$f_{\text{cos}}(\mathbf{x},\mathbf{a}) = \frac{\mathbf{x} \cdot \mathbf{a}}{\parallel \mathbf{x} \parallel \parallel \mathbf{a} \parallel + \epsilon}$$

Direction-based similarity, invariant to vector magnitude. The small
$\epsilon = 10^{- 12}$ prevents division by zero. Appropriate when
feature magnitudes are uninformative (e.g., normalized expression
profiles).

#### Hamming

$$f_{\text{ham}}(\mathbf{x},\mathbf{a}) = 1 - \frac{1}{d}\sum\limits_{k = 1}^{d}\mathbf{1}\left\lbrack x_{k} \neq a_{k} \right\rbrack$$

Proportion of matching features. Used for categorical or binary data.

### Distance functions

For clustering assignment and network suppression, bHIVE uses distance
rather than affinity. Six metrics are available:

| Distance    | Formula                                                                        | Notes                                       |
|:------------|:-------------------------------------------------------------------------------|:--------------------------------------------|
| Euclidean   | $\sqrt{\sum_{k}\left( x_{k} - a_{k} \right)^{2}}$                              | Default; L2 norm                            |
| Manhattan   | $\sum_{k}\left| x_{k} - a_{k} \right|$                                         | L1 norm; robust to outliers                 |
| Minkowski   | $(\sum_{k}\left| x_{k} - a_{k} \right|^{p})^{1/p}$                             | Generalized; $p = 2$ delegates to Euclidean |
| Cosine      | $1 - f_{\text{cos}}(\mathbf{x},\mathbf{a})$                                    | Angular distance                            |
| Mahalanobis | $\sqrt{(\mathbf{x} - \mathbf{a})^{\top}\Sigma^{- 1}(\mathbf{x} - \mathbf{a})}$ | Accounts for feature covariance             |
| Hamming     | $\frac{1}{d}\sum_{k}\mathbf{1}\left\lbrack x_{k} \neq a_{k} \right\rbrack$     | Categorical features                        |

------------------------------------------------------------------------

## Initialization

### Standard methods

bHIVE provides four initialization strategies for the starting antibody
population:

| Method             | Algorithm                                                                                             | When to use                                 |
|:-------------------|:------------------------------------------------------------------------------------------------------|:--------------------------------------------|
| `"sample"`         | Random rows from $\mathbf{X}$                                                                         | Default; fast, data-representative          |
| `"random"`         | $\mathbf{a} \sim \mathcal{N}\left( \bar{\mathbf{x}},\text{diag}\left( \sigma_{k}^{2} \right) \right)$ | When you want diversity beyond data support |
| `"random_uniform"` | $a_{k} \sim U\left( \min_{i}x_{ik},\max_{i}x_{ik} \right)$                                            | Uniform coverage of feature ranges          |
| `"kmeans++"`       | D2-weighted sampling                                                                                  | Better coverage; $O(nmd)$ cost              |

The **kmeans++** initialization (Arthur & Vassilvitskii 2007) selects
the first antibody uniformly at random, then each subsequent antibody
with probability proportional to its squared distance to the nearest
existing antibody:
$P\left( \mathbf{x}_{i} \right) \propto \min_{j < \text{current}} \parallel \mathbf{x}_{i} - \mathbf{a}_{j} \parallel^{2}$.

### V(D)J Gene Library (`VDJLibrary`)

#### Biological context

Real antibody diversity is generated by **V(D)J recombination**: the
variable region of an immunoglobulin gene is assembled by randomly
combining one V (variable), one D (diversity), and one J (joining) gene
segment from a germline library. This combinatorial mechanism generates
approximately $10^{11}$ distinct antibodies from only \$\$300 gene
segments.

#### Algorithm

`VDJLibrary` translates this to feature space:

1.  **Segment the feature space** into three groups (V, D, J) by
    splitting the $d$ dimensions. Three methods are available:

    - **PCA**: The first $\lfloor d/3\rfloor$ principal components form
      V, the next form D, the remainder form J
    - **Cluster**: k-means clustering within each dimension group
      creates alleles
    - **Random partition**: Dimensions randomly assigned to V, D, J

2.  **Create alleles** for each segment by clustering the data projected
    onto that segment’s dimensions (using k-means with `nV`, `nD`, `nJ`
    centers respectively)

3.  **Generate antibodies** by combinatorial sampling: select one V
    allele, one D allele, and one J allele, then concatenate to form a
    complete $d$-dimensional antibody vector

This produces structured coverage of the data manifold with
$n_{V} \times n_{D} \times n_{J}$ potential combinations, analogous to
the combinatorial diversity of the real immune system.

------------------------------------------------------------------------

## The Core Loop: Clonal Selection

### Biological context

**Clonal selection theory** (Burnet 1959) states that when an antigen
enters the body, the B cells whose receptors best match that antigen are
selected to proliferate (clonal expansion) and undergo mutation (somatic
hypermutation). The result is an iterative refinement process: the
population of antibodies evolves toward higher affinity for the antigen.

This is the mechanism that de Castro & Von Zuben (2001) formalized in
the AI-Net algorithm and that bHIVE implements with C++ acceleration.

### Algorithm

For each iteration $t = 1,\ldots,T$:

**Step 1: Affinity computation.** Compute the $n \times m$ affinity
matrix $\mathbf{F}$ using the chosen kernel. This is the most expensive
step and is dispatched to BLAS via RcppArmadillo.

**Step 2: Clonal expansion and mutation.** For each data point
$\mathbf{x}_{i}$:

1.  Select the $k$ antibodies with highest affinity:
    $\mathcal{K}_{i} = \text{top-}k_{j}\, f\left( \mathbf{x}_{i},\mathbf{a}_{j} \right)$

2.  For each selected antibody $\mathbf{a}_{j} \in \mathcal{K}_{i}$,
    generate $n_{c}$ clones where:
    $$n_{c} = \text{round}\!\left( \beta \cdot f\left( \mathbf{x}_{i},\mathbf{a}_{j} \right) \right),\quad n_{c} \leq \texttt{𝚖𝚊𝚡𝙲𝚕𝚘𝚗𝚎𝚜}$$

3.  Mutate each clone:
    $$\mathbf{a}\prime = \mathbf{a}_{j} + {\mathbf{ϵ}}$$ where
    $\mathbf{ϵ}$ is drawn from the active SHM strategy (see below). If
    the mutant has higher affinity than the parent, it replaces the
    parent.

**Step 3: Network regulation.** Suppress redundant antibodies (see
Idiotypic Network section) or apply simple $\epsilon$-threshold
suppression: remove $\mathbf{a}_{j}$ if
$d\left( \mathbf{a}_{i},\mathbf{a}_{j} \right) < \epsilon$ for any
$i < j$.

**Step 4: Task-specific assignment.**

- **Clustering**: each data point assigned to the nearest antibody by
  distance
- **Classification**: each antibody labeled by majority vote of its
  assigned data points; predictions via affinity-weighted nearest
  antibody
- **Regression**: each antibody stores the mean target value of its
  assigned points; predictions via affinity-weighted interpolation

**Step 5: Convergence check.** Early stopping if the antibody population
size has not changed by more than `stopTolerance` for
`noImprovementLimit` consecutive iterations.

------------------------------------------------------------------------

## Somatic Hypermutation (SHM)

### Biological context

**Somatic hypermutation** is the process by which activated B cells
introduce point mutations into their antibody genes at a rate
approximately $10^{6}$ times higher than the background mutation rate.
The enzyme activation-induced cytidine deaminase (AID) preferentially
targets WRCY/RGYW DNA motifs (hotspots), creating a non-uniform mutation
landscape. Mutations that improve antigen binding are selected for;
those that reduce it lead to cell death. Over multiple rounds of
mutation and selection (affinity maturation), the antibody population
converges on high-affinity binders.

### Five strategies

#### 1. Uniform

$$\mathbf{a}\prime = \mathbf{a} + \mathcal{N}\!\left( 0,\;(1 - f) \cdot \gamma^{t - 1} \right)$$

where $f$ is the affinity of the parent antibody, $\gamma$ is
`mutationDecay`, and $t$ is the iteration. The mutation rate decreases
with both affinity (better antibodies mutate less) and time (the
population stabilizes).

**When to use:** Default baseline. Simple and robust.

#### 2. AIRS (Affinity-Proportional)

$$\text{rate} = c \cdot \exp( - f/T)$$

where $c$ is a scaling constant (`c_rate`) and $T$ is a temperature
parameter. From Watkins & Timmis (2004), this achieves approximately 50%
better data reduction than uniform mutation by concentrating mutation on
low-affinity antibodies.

**When to use:** When you want the mutation rate to be strictly
controlled by affinity, with a tunable temperature.

#### 3. Hotspot (Feature-Weighted)

$$\epsilon_{k} = \text{base\_rate} \cdot \left| g_{k} \right| \cdot \mathcal{N}(0,1)$$

where $g_{k} = x_{k} - a_{k}$ is the per-feature “gradient” toward the
matched data point. Features with larger discrepancies mutate more,
analogous to AID targeting specific DNA motifs.

**When to use:** When some features are more informative than others and
you want the algorithm to discover this automatically.

#### 4. Energy-Budget

$$\parallel {\mathbf{ϵ}} \parallel^{2} \leq E_{0} \cdot (1 - f)^{2}$$

The total mutation magnitude is bounded by an energy budget that shrinks
as affinity increases. Inspired by Kleinstein’s observation that the
energetic cost of SHM scales quadratically with the number of mutations
($E_{\text{SHM}} \sim N_{\text{mut}}^{2}$). Individual feature
perturbations are sampled uniformly, then rescaled to satisfy the budget
constraint.

**When to use:** When you want hard bounds on how much any single
mutation event can perturb an antibody.

#### 5. Adaptive (Adam-Like)

Implementation of a convergence hypothesis. For each feature $k$ of each
antibody:

$$g_{k} = x_{k} - a_{k}\quad\text{(gradient toward matched antigen)}$$

$$\left. m_{k}\leftarrow\beta_{1}\, m_{k} + \left( 1 - \beta_{1} \right)\, g_{k}\quad\text{(first moment)} \right.$$

$$\left. v_{k}\leftarrow\beta_{2}\, v_{k} + \left( 1 - \beta_{2} \right)\, g_{k}^{2}\quad\text{(second moment)} \right.$$

$$\epsilon_{k} = \text{base\_rate} \cdot \frac{m_{k}}{\sqrt{v_{k}} + \epsilon_{\text{adam}}}$$

This is identical to the Adam optimizer (Kingma & Ba 2015) applied
per-feature. The biological interpretation: $m_{k}$ represents the
cell’s “memory” of which direction to mutate (accumulated selection
pressure), while $v_{k}$ tracks the variance of past selection signals
(stability of the gradient). Features with consistent directional
pressure get larger mutations; features with noisy signals are damped.

**When to use:** Complex landscapes where different features have
different scales and signal-to-noise ratios. Best general-purpose
choice.

------------------------------------------------------------------------

## Idiotypic Network Regulation

### Biological context

Jerne’s **idiotypic network theory** (1974) proposes that antibodies
don’t just recognize antigens, but also recognize each other. The
variable region of one antibody (its idiotype) can serve as an epitope
for another antibody (an anti-idiotype). This creates a regulatory
network with emergent properties: memory, tolerance, and self-organized
repertoire structure.

Varela & Coutinho (1991) formalized this as a “second generation” immune
network with a **bell-shaped activation function**: below a lower
threshold $\theta_{\text{low}}$, insufficient stimulation leads to cell
death (neglect); between thresholds, moderate stimulation leads to
activation; above $\theta_{\text{high}}$, excessive stimulation leads to
suppression.

This is biologically more realistic than the simple $\epsilon$-threshold
suppression used in classical AIS, and it produces qualitatively
different repertoire dynamics.

### Algorithm

Given the antibody matrix $\mathbf{A}$ with $m$ rows:

**Step 1:** Compute the $m \times m$ pairwise affinity matrix
$\mathbf{S}$ where
$S_{ij} = f\left( \mathbf{a}_{i},\mathbf{a}_{j} \right)$.

**Step 2:** For each pair $(i,j)$, compute the activation signal:

$$h_{ij} = \begin{cases}
{- 1} & {{\text{if}\mspace{6mu}}S_{ij} < \theta_{\text{low}}\quad\text{(death signal)}} \\
{+ 1} & {{\text{if}\mspace{6mu}}\theta_{\text{low}} \leq S_{ij} \leq \theta_{\text{high}}\quad\text{(activation)}} \\
{- 1} & {{\text{if}\mspace{6mu}}S_{ij} > \theta_{\text{high}}\quad\text{(suppression)}}
\end{cases}$$

**Step 3:** Euler-integrate the population dynamics ODE for $T$ steps
with step size $\Delta t$:

$$\frac{dA_{i}}{dt} = s - \delta \cdot A_{i} + A_{i}\sum\limits_{j:h_{ij} > 0}S_{ij} - A_{i}\sum\limits_{j:h_{ij} < 0}S_{ij}$$

where: - $s$ = `source_rate` (basal production of new cells) - $\delta$
= `decay_rate` (natural death) - The activation and suppression terms
are weighted by the actual affinity values

**Step 4:** Remove antibodies whose population level $A_{i}$ falls below
`survival_threshold`.

#### Parameter guidance

| Parameter            | Default | Effect of increasing                                |
|:---------------------|:--------|:----------------------------------------------------|
| `theta_low`          | 0.01    | More antibodies die from neglect                    |
| `theta_high`         | 0.5     | Narrower activation window; more suppression        |
| `source_rate`        | 0.5     | More new cells enter; larger final repertoire       |
| `decay_rate`         | 0.1     | Faster natural death; smaller repertoire            |
| `dt`                 | 0.1     | Larger integration steps (less stable if too large) |
| `timeSteps`          | 20      | Longer simulation; more time for dynamics to settle |
| `survival_threshold` | 0.5     | Stricter survival; fewer antibodies remain          |

------------------------------------------------------------------------

## Germinal Center Selection

### Biological context

The **germinal center** (GC) is a specialized microstructure within
lymph nodes where B cells undergo iterative rounds of mutation (in the
dark zone) and selection (in the light zone). In the light zone, B cells
compete for help from **T follicular helper (Tfh) cells**. A Tfh cell
evaluates the quality of the B cell’s antigen presentation and provides
survival signals only to the best competitors. B cells that fail to
receive Tfh help undergo apoptosis.

This is a quality-control bottleneck: it ensures that only improved
antibodies survive each round.

### Algorithm

The `GerminalCenter` module implements this as resource competition:

1.  Compute a **quality score** $q_{j}$ for each antibody
    $\mathbf{a}_{j}$. The scoring is task-aware:

    - **Classification**: $q_{j}$ = proportion of assigned data points
      whose label matches the antibody’s majority label
    - **Regression**: $q_{j}$ = $1/\left( 1 + \text{MSE}_{j} \right)$
      where MSE is computed over assigned data points
    - **Clustering**: $q_{j}$ = mean affinity to assigned data points
      (cohesion)

2.  Apply selection pressure $p \in \lbrack 0,1\rbrack$ to compute a
    survival threshold:
    $$\tau = q_{\min} + p \cdot \left( q_{\max} - q_{\min} \right)$$

3.  For each of `nTfh` helper cells, the Tfh selects the antibody with
    highest quality among those not yet helped. Antibodies below the
    threshold $\tau$ that do not receive Tfh help are removed.

4.  Repeat for `rounds` cycles.

#### Parameter guidance

| Parameter           | Default | Effect                                        |
|:--------------------|:--------|:----------------------------------------------|
| `nTfh`              | 10      | Determines maximum survivors per round        |
| `selectionPressure` | 0.5     | 0 = everything survives; 1 = only the best    |
| `rounds`            | 1       | Multiple rounds compound the selection effect |

------------------------------------------------------------------------

## Microenvironment

### Biological context

B cell fate is strongly influenced by the **tissue microenvironment**:
chemokine gradients direct migration, cytokines influence
differentiation, and local cell density affects competition for
resources. In the germinal center, the dark zone
(proliferation/mutation) and light zone (selection) create spatially
distinct functional regions.

### Algorithm

The `Microenvironment` module classifies each antibody’s local context
by computing kernel density estimates from the data:

$$\rho_{j} = \frac{1}{n}\sum\limits_{i = 1}^{n}f\left( \mathbf{x}_{i},\mathbf{a}_{j} \right)$$

Based on the percentile of $\rho_{j}$ within the antibody population:

| Zone         | Condition                    | Mutation modifier        | Biological analog                    |
|:-------------|:-----------------------------|:-------------------------|:-------------------------------------|
| **Stable**   | $\rho_{j} > P_{\text{high}}$ | $\times 0.3$ (reduce)    | Light zone; protect good solutions   |
| **Explore**  | $\rho_{j} < P_{\text{low}}$  | $\times 2.0$ (increase)  | Dark zone; search sparse regions     |
| **Boundary** | otherwise                    | $\times 1.0$ (no change) | Transitional; potential class switch |

where $P_{\text{high}}$ and $P_{\text{low}}$ are the
`high_density_threshold` and `low_density_threshold` percentiles,
respectively.

#### Chemokine-like gradients

The module also computes a directional gradient for each antibody,
pointing toward the local center of mass of nearby data:

$$\mathbf{g}_{j} = \frac{\sum\limits_{i}f\left( \mathbf{x}_{i},\mathbf{a}_{j} \right) \cdot \mathbf{x}_{i}}{\sum\limits_{i}f\left( \mathbf{x}_{i},\mathbf{a}_{j} \right)} - \mathbf{a}_{j}$$

This gradient can bias mutation direction toward higher-density regions,
analogous to chemokine-directed B cell migration.

------------------------------------------------------------------------

## Two-Signal Activation Gate

### Biological context

In real immunity, B cell activation requires **two signals**:

- **Signal 1**: Specific antigen recognition by the B cell receptor
  (affinity-dependent)
- **Signal 2**: Costimulatory signals from helper T cells, danger
  signals (DAMPs/PAMPs), or cytokines

This **two-signal model** (Bretscher & Cohn 1970, formalized for AIS by
Freitas 2006) prevents autoimmune activation: a B cell that binds
self-antigen without costimulation is anergized (silenced) rather than
activated. It serves as a biologically-principled regularization
mechanism.

### Algorithm

An antibody-antigen interaction $(i,j)$ is activated only if both
signals exceed their thresholds:

$$\text{activated}_{ij} = \mathbf{1}\!\left\lbrack f\left( \mathbf{x}_{i},\mathbf{a}_{j} \right) > \tau_{1} \right\rbrack\; \land \;\mathbf{1}\!\left\lbrack \text{Signal2}_{j} > \tau_{2} \right\rbrack$$

Three options for Signal 2:

| Type        | Computation                                            | Use case                                        |
|:------------|:-------------------------------------------------------|:------------------------------------------------|
| `"density"` | Local data density around $\mathbf{a}_{j}$             | Default; prevents activation in sparse regions  |
| `"danger"`  | User-provided per-data-point danger scores             | When you have external quality annotations      |
| `"entropy"` | Local label entropy among $\mathbf{a}_{j}$’s neighbors | Classification; high entropy = uncertain region |

------------------------------------------------------------------------

## Class Switching

### Biological context

During an immune response, B cells can **switch** the constant region of
their antibody (isotype) while retaining the same antigen-binding
variable region. The functional consequence is a change in effector
properties:

- **IgM**: Pentameric; broad, low-affinity binding. First responder.
- **IgG**: Monomeric; high-affinity, highly specific. Dominant in
  secondary responses.
- **IgA**: Dimeric; secreted at mucosal surfaces. Boundary patrol.

### Algorithm

In bHIVE, class switching changes the effective **kernel width** of the
affinity function, modifying the matching breadth without changing the
antibody’s position in feature space:

| Isotype | $\alpha$     | Matching behavior                                  |
|:--------|:-------------|:---------------------------------------------------|
| IgM     | 0.1 (broad)  | Large receptive field; captures general patterns   |
| IgG     | 5.0 (narrow) | Small receptive field; fine-grained discrimination |
| IgA     | 1.0 (medium) | Intermediate; boundary patrol                      |

Switching rules are driven by the `Microenvironment` zone assignments:

- **Stable zone** $\rightarrow$ IgG: data-dense regions benefit from
  specific matching
- **Explore zone** $\rightarrow$ IgM: sparse regions need broad coverage
  to find signal
- **Boundary zone** $\rightarrow$ IgA: intermediate regions need
  balanced matching

------------------------------------------------------------------------

## Memory Pool

### Biological context

After an immune response resolves, a subset of activated B cells
differentiate into long-lived **memory B cells** that persist for years.
Upon re-encounter with the same antigen, memory cells mount a faster and
stronger secondary response.

### Algorithm

The `MemoryPool` module maintains an archive of high-performing
antibodies:

**Archive**: After each iteration, antibodies whose mean affinity to
their assigned data exceeds `archive_threshold` are copied into the
memory pool, up to `max_memory` total cells. If the pool is full, the
lowest- affinity memories are evicted.

**Recall**: When new data arrive (or when the data distribution shifts),
memory antibodies whose affinity to the new data exceeds
`recall_threshold` are reintroduced into the active repertoire. This
provides a warm start for the next round of adaptation.

------------------------------------------------------------------------

## Convergent Selection

### Biological context

In adaptive immunology, certain TCR/BCR sequences appear in multiple
unrelated individuals responding to the same pathogen. These **public
clonotypes** are driven by convergent selection: the structure of the
antigen imposes such strong selective pressure that independent immune
systems arrive at the same solution.

### Algorithm

The `ConvergentSelector` module finds public antibodies across multiple
independent bHIVE runs:

1.  Run $R$ independent bHIVE analyses (with different random seeds) on
    the same data
2.  For each antibody from run 1, check how many other runs contain an
    antibody within distance `tolerance`
3.  Antibodies that appear in $\geq$`min_appearances` runs are declared
    **public** and retained as consensus prototypes

This implements a biologically-motivated ensemble: rather than averaging
predictions, it identifies the prototypes that multiple independent
optimization trajectories converge on.

------------------------------------------------------------------------

## Parameter Guidance

The tables below provide practical starting points and tuning advice for
the most important parameters. These are rules of thumb – the optimal
settings depend on your data.

### Core Parameters

| Parameter      | Default      | Start here                                   | Tune if…                                                        |
|:---------------|:-------------|:---------------------------------------------|:----------------------------------------------------------------|
| `nAntibodies`  | 20           | $\sqrt{n}$ to $2\sqrt{n}$                    | Underfitting (too few) or slow (too many)                       |
| `beta`         | 5            | 3–10                                         | Low affinity at convergence (increase)                          |
| `epsilon`      | 0.01         | 0.01–0.1                                     | Too many or too few final antibodies                            |
| `maxIter`      | 50           | 20–100                                       | Not converged (increase) or slow (decrease)                     |
| `k`            | 3            | 2–5                                          | Underfitting (increase) or overfitting (decrease)               |
| `affinityFunc` | `"gaussian"` | `"gaussian"`                                 | Non-Euclidean data (try cosine, polynomial)                     |
| `alpha`        | 1            | $1/\left( 2\sigma_{\text{data}}^{2} \right)$ | All affinities $\approx 0$ (decrease) or $\approx 1$ (increase) |

### SHM Parameters

| Parameter     | Default        | When to change                                        |
|:--------------|:---------------|:------------------------------------------------------|
| `method`      | `"uniform"`    | Try `"adaptive"` for complex landscapes               |
| `decay`       | 1.0            | Set $< 1$ if population oscillates and won’t converge |
| `mutationMin` | 0.01           | Increase if algorithm stalls at local optima          |
| `temperature` | 0.5 (airs)     | Lower = less mutation on high-affinity antibodies     |
| `base_rate`   | 0.1 (adaptive) | Scale with feature magnitudes                         |

### Module Interactions

| Combination                      | Effect                                   | Recommendation                                                   |
|:---------------------------------|:-----------------------------------------|:-----------------------------------------------------------------|
| SHM adaptive + Microenvironment  | Zone-dependent adaptive mutation rates   | Strong synergy; recommended for complex data                     |
| Idiotypic + GerminalCenter       | Network regulation + quality selection   | Complementary; idiotypic controls diversity, GC controls quality |
| VDJLibrary + ActivationGate      | Structured init + regularized activation | Good for high-dimensional data                                   |
| ClassSwitcher + Microenvironment | Zone-driven kernel width changes         | Requires Microenvironment to define zones                        |

------------------------------------------------------------------------

## References

- Arthur, D. & Vassilvitskii, S. (2007). k-means++: The advantages of
  careful seeding. *SODA*.
- Bretscher, P. & Cohn, M. (1970). A theory of self-nonself
  discrimination. *Science*, 169, 1042–1049.
- Burnet, F.M. (1959). *The Clonal Selection Theory of Acquired
  Immunity*. Cambridge University Press.
- de Castro, L.N. & Von Zuben, F.J. (2001). aiNet: Artificial immune
  network for data analysis. In *Data Mining: A Heuristic Approach*,
  231–260.
- de Castro, L.N. & Timmis, J. (2003). Artificial immune systems as a
  novel soft computing paradigm. *Soft Computing*, 7, 526–544.
- Freitas, A.A. (2006). *Immunoinformatics*. Springer.
- Jerne, N.K. (1974). Towards a network theory of the immune system.
  *Annales d’Immunologie (Institut Pasteur)*, 125C, 373–389.
- Kingma, D.P. & Ba, J. (2015). Adam: A method for stochastic
  optimization. *ICLR*.
- Perelson, A.S. & Oster, G.F. (1979). Theoretical studies of clonal
  selection: Minimal antibody repertoire size and reliability of
  self-non-self discrimination. *Journal of Theoretical Biology*, 81,
  645–670.
- Varela, F.J. & Coutinho, A. (1991). Second generation immune networks.
  *Immunology Today*, 12, 159–166.
- Watkins, A. & Timmis, J. (2004). Artificial immune recognition system
  (AIRS): An immune-inspired supervised learning algorithm. *Genetic
  Programming and Evolvable Machines*, 5, 291–317.

&nbsp;

    ## R version 4.5.3 (2026-03-11)
    ## Platform: x86_64-pc-linux-gnu
    ## Running under: Ubuntu 24.04.4 LTS
    ## 
    ## Matrix products: default
    ## BLAS:   /usr/lib/x86_64-linux-gnu/openblas-pthread/libblas.so.3 
    ## LAPACK: /usr/lib/x86_64-linux-gnu/openblas-pthread/libopenblasp-r0.3.26.so;  LAPACK version 3.12.0
    ## 
    ## locale:
    ##  [1] LC_CTYPE=C.UTF-8       LC_NUMERIC=C           LC_TIME=C.UTF-8       
    ##  [4] LC_COLLATE=C.UTF-8     LC_MONETARY=C.UTF-8    LC_MESSAGES=C.UTF-8   
    ##  [7] LC_PAPER=C.UTF-8       LC_NAME=C              LC_ADDRESS=C          
    ## [10] LC_TELEPHONE=C         LC_MEASUREMENT=C.UTF-8 LC_IDENTIFICATION=C   
    ## 
    ## time zone: UTC
    ## tzcode source: system (glibc)
    ## 
    ## attached base packages:
    ## [1] stats     graphics  grDevices utils     datasets  methods   base     
    ## 
    ## other attached packages:
    ## [1] viridis_0.6.5     viridisLite_0.4.3 ggplot2_4.0.2     bHIVE_0.99.1     
    ## [5] BiocStyle_2.38.0 
    ## 
    ## loaded via a namespace (and not attached):
    ##  [1] sass_0.4.10         generics_0.1.4      lattice_0.22-9     
    ##  [4] digest_0.6.39       magrittr_2.0.5      evaluate_1.0.5     
    ##  [7] grid_4.5.3          RColorBrewer_1.1-3  bookdown_0.46      
    ## [10] fastmap_1.2.0       jsonlite_2.0.0      Matrix_1.7-4       
    ## [13] umap_0.2.10.0       RSpectra_0.16-2     gridExtra_2.3      
    ## [16] BiocManager_1.30.27 scales_1.4.0        codetools_0.2-20   
    ## [19] textshaping_1.0.5   jquerylib_0.1.4     cli_3.6.5          
    ## [22] rlang_1.2.0         withr_3.0.2         cachem_1.1.0       
    ## [25] yaml_2.3.12         otel_0.2.0          Rtsne_0.17         
    ## [28] tools_4.5.3         parallel_4.5.3      BiocParallel_1.44.0
    ## [31] dplyr_1.2.1         reticulate_1.45.0   png_0.1-9          
    ## [34] vctrs_0.7.2         R6_2.6.1            lifecycle_1.0.5    
    ## [37] fs_2.0.1            htmlwidgets_1.6.4   ragg_1.5.2         
    ## [40] cluster_2.1.8.2     pkgconfig_2.0.3     desc_1.4.3         
    ## [43] pkgdown_2.2.0       pillar_1.11.1       bslib_0.10.0       
    ## [46] gtable_0.3.6        glue_1.8.0          Rcpp_1.1.1         
    ## [49] systemfonts_1.3.2   xfun_0.57           tibble_3.3.1       
    ## [52] tidyselect_1.2.1    knitr_1.51          farver_2.1.2       
    ## [55] htmltools_0.5.9     rmarkdown_2.31      clusterCrit_1.3.0  
    ## [58] compiler_4.5.3      S7_0.2.1            askpass_1.2.1      
    ## [61] openssl_2.3.5
