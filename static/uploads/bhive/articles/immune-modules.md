# Composing Immune Modules

## Introduction

The bHIVE package provides two equivalent interfaces: a **functional
API**
([`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md))
for quick, one-liner analysis and an **R6 class API** (`AINet`) for full
compositional control. This vignette focuses on the R6 API and the 9
immune modules that can be injected into `AINet` to customize every
stage of the algorithm.

Each module is an independent R6 class that encapsulates a single
immunological mechanism. You create modules separately and pass them to
`AINet$new()`, allowing you to mix and match any combination.

``` r
model <- AINet$new(
  nAntibodies = 20,
  shm            = SHMEngine$new(method = "adaptive"),
  idiotypic      = IdiotypicNetwork$new(),
  germinalCenter = GerminalCenter$new(),
  microenvironment = Microenvironment$new(),
  init           = VDJLibrary$new(method = "pca"),
  activation     = ActivationGate$new(),
  memory         = MemoryPool$new()
)
```

## Somatic Hypermutation Engine

The `SHMEngine` controls how antibodies mutate after cloning. Five
strategies are available, each grounded in a different aspect of SHM
biology:

| Method       | Biological Analogy                    | When to Use                                       |
|:-------------|:--------------------------------------|:--------------------------------------------------|
| `"uniform"`  | Random point mutations                | Baseline; simple and robust                       |
| `"airs"`     | Affinity-proportional mutation (AIRS) | When high-affinity antibodies should explore less |
| `"hotspot"`  | AID targets WRCY motifs               | When some features matter more than others        |
| `"energy"`   | E_SHM ~ N_Mut^2 budget constraint     | When you want bounded total perturbation          |
| `"adaptive"` | Per-feature Adam-like moment tracking | Best for complex landscapes; most novel           |

The **adaptive** method is the most distinctive in which somatic
hypermutation and the Adam optimizer function the same. Each feature
dimension maintains running mean and variance of past gradients.

``` r
data(iris)
X <- as.matrix(iris[, 1:4])
y <- iris$Species

methods <- c("uniform", "airs", "adaptive")
results <- lapply(methods, function(m) {
  shm <- SHMEngine$new(method = m)
  model <- AINet$new(nAntibodies = 15, 
                     maxIter = 15, 
                     shm = shm,
                     verbose = FALSE)
  model$fit(X, y, task = "classification")
  data.frame(
    method   = m,
    accuracy = mean(model$result$assignments == as.character(y)),
    n_ab     = nrow(model$repertoire$as_matrix())
  )
})
do.call(rbind, results)
```

    ##     method  accuracy n_ab
    ## 1  uniform 0.9600000   14
    ## 2     airs 0.8866667   13
    ## 3 adaptive 0.8533333   15

## Idiotypic Network Regulation

In classical AIS, similar antibodies are suppressed via a simple
distance threshold (epsilon). The `IdiotypicNetwork` module replaces
this with principled network dynamics inspired by Varela & Coutinho’s
(1991) second-generation immune network theory.

The key insight is a **bell-shaped activation function**: too little
stimulation from other antibodies leads to death, moderate stimulation
leads to activation, and excessive stimulation leads to suppression.
This creates emergent self-organized repertoire structure.

``` r
# Standard epsilon suppression (default)
model_std <- AINet$new(nAntibodies = 25, maxIter = 15, verbose = FALSE)
model_std$fit(X, task = "clustering")

# Idiotypic network regulation
model_idi <- AINet$new(
  nAntibodies = 25, maxIter = 15,
  idiotypic = IdiotypicNetwork$new(
    theta_low = 0.01, 
    theta_high = 0.5,
    source_rate = 0.5, 
    timeSteps = 20
  ),
  verbose = FALSE
)
model_idi$fit(X, task = "clustering")

cat("Standard suppression:", model_std$repertoire$size(), "antibodies\n")
```

    ## Standard suppression: 25 antibodies

``` r
cat("Idiotypic regulation:", model_idi$repertoire$size(), "antibodies\n")
```

    ## Idiotypic regulation: 22 antibodies

The idiotypic network typically produces a more parsimonious repertoire
because regulation is based on the *network* of antibody-antibody
interactions rather than pairwise distance alone.

## Germinal Center Selection

The `GerminalCenter` module models the competition for T follicular
helper (Tfh) cell help that occurs in real germinal centers. Only
antibodies that receive Tfh help survive – this implements quality-based
selection pressure.

The quality metric is task-aware:

- **Classification**: proportion of correctly matched labels
- **Regression**: inverse prediction error
- **Clustering**: local density (sum of affinities to assigned data
  points)

``` r
gc <- GerminalCenter$new(
  nTfh = 10,                 # number of Tfh selectors
  selectionPressure = 0.5,   # 0 = no selection, 1 = very strict
  rounds = 1
)

model_gc <- AINet$new(
  nAntibodies = 30, 
  maxIter = 15,
  germinalCenter = gc,
  verbose = FALSE
)
model_gc$fit(X, y, task = "classification")
cat("Antibodies after GC selection:", model_gc$repertoire$size(), "\n")
```

    ## Antibodies after GC selection: 28

``` r
cat("Accuracy:", mean(model_gc$result$assignments == as.character(y)), "\n")
```

    ## Accuracy: 0.9533333

## Microenvironment

The `Microenvironment` module classifies the local context around each
antibody into three zones and adapts mutation rates accordingly:

- **Stable** (high local density): reduce mutation rate to preserve good
  antibodies
- **Explore** (low local density): increase mutation rate to search
  sparse regions
- **Boundary** (intermediate): moderate mutation, potential trigger for
  class switching

``` r
me <- Microenvironment$new(
  high_density_threshold = 0.75,
  low_density_threshold = 0.25,
  stabilization_factor = 0.3,   # reduce mutation to 30% in stable zones
  exploration_factor = 2.0      # double mutation in exploration zones
)

rep <- ImmuneRepertoire$new(X[sample(150, 15), ])
env <- me$assess(rep, X)
table(env$zones)
```

    ## 
    ## boundary  explore   stable 
    ##        7        4        4

## V(D)J Gene Library Initialization

Instead of random sampling, `VDJLibrary` generates antibodies by
combinatorial assembly of gene segments, mimicking V(D)J recombination.
The feature space is split into three segments (V, D, J), each
discretized into alleles, and new antibodies are built by combining one
allele from each segment.

``` r
vdj <- VDJLibrary$new(nV = 5, 
                      nD = 3, 
                      nJ = 3, 
                      method = "pca")
A <- vdj$generate(20, X)
dim(A)  # 20 antibodies x 4 features
```

    ## [1] 20  4

``` r
print(vdj)
```

    ## <VDJLibrary> method='pca' V=5 D=3 J=3
    ##   Combinatorial space: 45 antibodies

Three decomposition methods are available:

- `"pca"`: PCA components define gene segments (best for correlated
  features)
- `"cluster"`: k-means within dimension groups creates alleles
- `"random_partition"`: random feature grouping (simplest)

## Two-Signal Activation Gate

In real immunity, B cells require two signals to activate: antigen
recognition (Signal 1) *and* costimulatory context (Signal 2). The
`ActivationGate` module prevents spurious cloning on isolated outliers.

Signal 2 options:

- `"density"`: local data density around the antibody
- `"danger"`: user-provided danger score per data point
- `"entropy"`: local label entropy (classification only)

``` r
gate <- ActivationGate$new(
  signal2_type = "density",
  threshold1 = 0.1,    # minimum affinity (Signal 1)
  threshold2 = 0.3     # density percentile (Signal 2)
)

A <- X[sample(150, 10), ]
rep <- ImmuneRepertoire$new(A)
aff <- rep$affinity_matrix(X, "gaussian")
activated <- gate$evaluate(aff, X, A)
cat("Activated interactions:", sum(activated), "/", length(activated), "\n")
```

    ## Activated interactions: 499 / 1500

## Memory Pool

The `MemoryPool` archives high-performing antibodies and recalls them
when relevant to current data. This is useful for streaming or
non-stationary data where distribution shifts may occur.

``` r
mp <- MemoryPool$new(
  archive_threshold = 0.01,  # minimum average affinity to archive
  max_memory = 50,
  recall_threshold = 0.01
)

rep <- ImmuneRepertoire$new(X[sample(150, 10), ])
n_archived <- mp$archive(rep, X)
cat("Archived:", n_archived, "memory cells\n")
```

    ## Archived: 10 memory cells

``` r
cat("Pool size:", mp$size(), "\n")
```

    ## Pool size: 10

``` r
# Recall memories relevant to a subset
recalled <- mp$recall(X[1:30, ])
cat("Recalled:", nrow(recalled), "cells for the query\n")
```

    ## Recalled: 3 cells for the query

## Class Switcher

The `ClassSwitcher` module changes the effective kernel width of
antibodies based on their microenvironment zone, analogous to real B
cell isotype switching:

| Isotype | Kernel Width | Matching Style                 |
|:--------|:-------------|:-------------------------------|
| IgM     | alpha = 0.1  | Broad (exploration)            |
| IgG     | alpha = 5.0  | Specific (discrimination)      |
| IgA     | alpha = 1.0  | Intermediate (boundary patrol) |

``` r
cs <- ClassSwitcher$new(alpha_IgM = 0.1, alpha_IgG = 5.0, alpha_IgA = 1.0)

rep <- ImmuneRepertoire$new(X[sample(150, 10), ])
zones <- sample(c("stable", "explore", "boundary"), 10, replace = TRUE)
alphas <- cs$switch_isotypes(rep, zones)
data.frame(zone = zones, isotype = rep$metadata$isotype, alpha = alphas)
```

    ##        zone isotype alpha
    ## 1  boundary     IgA   1.0
    ## 2   explore     IgM   0.1
    ## 3   explore     IgM   0.1
    ## 4  boundary     IgA   1.0
    ## 5   explore     IgM   0.1
    ## 6   explore     IgM   0.1
    ## 7  boundary     IgA   1.0
    ## 8  boundary     IgA   1.0
    ## 9    stable     IgG   5.0
    ## 10 boundary     IgA   1.0

## Convergent Selection

The `ConvergentSelector` identifies “public antibodies” – antibodies
that appear across multiple independent bHIVE runs. This implements the
immunological concept of public clonotypes as a biologically-motivated
ensemble method.

``` r
# Run 3 independent bHIVE analyses
set.seed(42)
results <- lapply(1:3, function(i) {
  m <- AINet$new(nAntibodies = 15, maxIter = 10, verbose = FALSE)
  m$fit(X, task = "clustering")
  m$result
})

conv <- ConvergentSelector$new(tolerance = 1.0, min_appearances = 2)
public <- conv$from_results(results)
cat("Public antibodies:", nrow(public), "\n")
```

    ## Public antibodies: 14

## Putting It All Together

Here is a full example combining multiple modules for a classification
task:

``` r
model <- AINet$new(
  nAntibodies = 25,
  maxIter = 20,
  k = 3,
  beta = 5,
  shm = SHMEngine$new(method = "adaptive", base_rate = 0.1),
  idiotypic = IdiotypicNetwork$new(theta_low = 0.01, theta_high = 0.5),
  germinalCenter = GerminalCenter$new(nTfh = 8, selectionPressure = 0.4),
  verbose = FALSE
)

model$fit(X, y, task = "classification")

cat("Final antibodies:", model$repertoire$size(), "\n")
```

    ## Final antibodies: 23

``` r
cat("Accuracy:", mean(model$result$assignments == as.character(y)), "\n")
```

    ## Accuracy: 0.9333333

Not every module combination will improve every dataset. The modular
design lets you experiment with different biological mechanisms and find
the combination that works best for your data and task.

## Session Information

``` r
sessionInfo()
```

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
