# TCR Specificity Grouping with immGLIPH

## Getting Started

**immGLIPH** provides an R implementation of the GLIPH (Grouping of
Lymphocyte Interactions by Paratope Hotspots) and GLIPH2 algorithms for
clustering T cell receptors (TCRs) that are predicted to bind the same
HLA-restricted peptide antigen.

The package identifies TCR specificity groups by detecting statistically
enriched CDR3$`\beta`$ motifs (local similarity) and structurally
similar CDR3$`\beta`$ sequences (global similarity), then clusters them
into convergence groups and scores each group for biological
significance.

**immGLIPH is an R implementation of existing algorithms. Users should
cite the original publications:**

- **GLIPH**: Glanville, J. et al. *Identifying specificity groups in the
  T cell receptor repertoire.* Nature 547, 94–98 (2017).
  [doi:10.1038/nature22976](https://doi.org/10.1038/nature22976)

- **GLIPH2**: Huang, H. et al. *Analyzing the Mycobacterium tuberculosis
  immune response by T-cell receptor clustering with GLIPH2 and
  genome-wide antigen screening.* Nature Biotechnology 38, 1194–1202
  (2020).
  [doi:10.1038/s41587-020-0505-4](https://doi.org/10.1038/s41587-020-0505-4)

More information is available at the [immGLIPH GitHub
Repo](https://github.com/BorchLab/immGLIPH).

### Installation

``` r
devtools::install_github("BorchLab/immGLIPH")
```

The reference repertoire data (~19 MB) is downloaded automatically the
first time you run `runGLIPH()` and cached locally via
[BiocFileCache](https://bioconductor.org/packages/BiocFileCache/).

### Integration with the scRepertoire Ecosystem

immGLIPH integrates with the
[scRepertoire](https://github.com/BorchLab/scRepertoire) ecosystem
through [immApex](https://github.com/BorchLab/immApex). This means
`runGLIPH()` can directly accept:

- **Seurat** objects with TCR information
- **SingleCellExperiment** objects with TCR information
- **combineTCR()** output lists from scRepertoire
- Standard data frames or character vectors

### The Data Set

To demonstrate immGLIPH, we will use the scRepertoire example data
derived from T cells of 4 patients with acute respiratory distress. The
data contains paired peripheral-blood (B) and bronchoalveolar lavage (L)
samples across 8 distinct runs from the 10x Cell Ranger pipeline.

## Loading Libraries and Data

``` r
scRep_example <- readRDS("scRep_example_full.rds")

scRep_example <- combineExpression(combined.TCR,
                                   scRep_example,
                                   cloneCall="aa",
                                   group.by = "sample",
                                   proportion = TRUE)

#Filtering for single-cells with TCRs
scRep_example <- subset(scRep_example,
                        cells = colnames(scRep_example)[!is.na(scRep_example$CTaa)])
```

## Running GLIPH

### Input Data Formats

`runGLIPH()` accepts multiple input formats. The most direct integration
with scRepertoire is passing the
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
output or a Seurat object:

``` r
# Option 1: Pass combineTCR() output directly
results <- runGLIPH(combined.TCR, 
                    method = "gliph2")

# Option 2: Pass a Seurat object with TCR metadata
results <- runGLIPH(scRep_example, 
                    method = "gliph2", 
                    chains = "TRB")
```

### Running GLIPH2 (Default)

By default `runGLIPH()` downloads a reference repertoire via
BiocFileCache.

``` r
res_gliph2 <- runGLIPH(
  cdr3_sequences = scRep_example,
  method         = "gliph2",
  sim_depth      = 100,
  n_cores        = 1
)
```

### Running GLIPH1

The original GLIPH algorithm uses repeated random sampling for local
similarity detection and Hamming distance for global similarity:

``` r
res_gliph1 <- runGLIPH(
  cdr3_sequences = scRep_example,
  method         = "gliph1",
  sim_depth      = 100,
  n_cores        = 1
)
```

### Method Presets

The `method` parameter configures a coordinated set of algorithm
choices:

| Setting       | `"gliph1"`               | `"gliph2"`            | `"custom"`   |
|:--------------|:-------------------------|:----------------------|:-------------|
| Local method  | Repeated random sampling | Fisher’s exact test   | User-defined |
| Global method | Hamming distance cutoff  | Struct-based + Fisher | User-defined |
| Clustering    | Connected components     | Per-motif isolated    | User-defined |
| Scoring       | GLIPH1 formula           | GLIPH2 formula        | User-defined |

## Understanding the Output

The output is a list with several components:

``` r
names(res_gliph2)
```

    ## [1] "sample_log"         "motif_enrichment"   "global_enrichment" 
    ## [4] "connections"        "cluster_properties" "cluster_list"      
    ## [7] "parameters"

### Cluster Properties

The `cluster_properties` data frame summarizes each convergence group
with enrichment scores:

``` r
head(res_gliph2$cluster_properties)
```

    ##    type      tag cluster_size unique_cdr3_sample unique_cdr3_ref  OvE
    ## 1 local AKDG_1_4            3                  3              21 14.5
    ## 2 local ASDL_1_6            3                  3              21 14.5
    ## 3 local DAFG_2_5            3                  3              28 10.9
    ## 4 local DLQL_2_3            3                  3              15 20.3
    ## 5 local DLRY_2_5            3                  3              27 11.3
    ## 6 local EQTN_2_3            3                  3              28 10.9
    ##   fisher.score total.score network.size.score cdr3.length.score
    ## 1      0.00160     0.00028             0.0062             0.045
    ## 2      0.00160     0.00270             0.0062             0.440
    ## 3      0.00340     0.00280             0.0062             0.450
    ## 4      0.00068     0.00270             0.0062             0.440
    ## 5      0.00310     0.00280             0.0062             0.450
    ## 6      0.00340     0.00280             0.0062             0.460
    ##                                           members
    ## 1    CASAMGAKDGYTF CASAKDGSDTQYF CASSAKDGSSGNTIYF
    ## 2 CASSASDLAKNIQYF CASSSGGGASDLYGYTF CSAASDLGYTQYF
    ## 3 CATSDAFGGAPDTQYF CSASPPGDAFGYTF CASSLDAFGTHGYTF
    ## 4 CATSDLQLGVTDTQYF CASSQDLQLTPLHF CSARDLQLASNEQFF
    ## 5 CASSHRDLRYEQYF CASSDLRYMNTGELFF CASSPTGDLRYEQYF
    ## 6    CASSLEQTNTGELFF CAISEQTNYGYTF CAISEQTNTGELFF

### Cluster Membership

The `cluster_list` is a named list where each element contains the
member TCRs of a convergence group:

``` r
length(res_gliph2$cluster_list)
```

    ## [1] 546

``` r
if (length(res_gliph2$cluster_list) > 0) {
  head(res_gliph2$cluster_list[[1]])
}
```

    ##       seq_ID            CDR3b       v    d       j     c
    ## 7405    6605    CASAMGAKDGYTF TRBV5-4 <NA> TRBJ1-2 TRBC1
    ## 19471  16762    CASAKDGSDTQYF TRBV5-1 <NA> TRBJ2-3 TRBC2
    ## 21069  18097 CASSAKDGSSGNTIYF TRBV5-4 <NA> TRBJ1-3 TRBC1
    ##                       barcode chain ultCDR3b
    ## 7405  P18L_TCACAAGTCTGAGGGA-1   TRB         
    ## 19471 P20B_GAACGGAGTTATTCTC-1   TRB         
    ## 21069 P20B_GTTACAGAGGAGTACC-1   TRB

### Motif Enrichment

The `motif_enrichment` element contains the locally enriched motifs:

``` r
if (!is.null(res_gliph2$motif_enrichment$selected_motifs)) {
  head(res_gliph2$motif_enrichment$selected_motifs)
}
```

    ##      motif counts num_in_ref avgRef topRef  OvE p.value
    ## 668   AKDG      3         21  0.207      0 14.5 0.00160
    ## 1178  ASDL      3         21  0.207      0 14.5 0.00160
    ## 1583  DAFG      3         28  0.276      0 10.9 0.00340
    ## 2087  DLQL      3         15  0.148      0 20.3 0.00068
    ## 2097  DLRY      3         27  0.266      0 11.3 0.00310
    ## 3749  EQTN      3         28  0.276      0 10.9 0.00340

### Network Edges

The `connections` data frame contains the edge list representing the TCR
similarity network:

``` r
if (!is.null(res_gliph2$connections)) {
  head(res_gliph2$connections)
}
```

    ##                 V1               V2  type cluster_tag
    ## 1    CASAMGAKDGYTF CASSAKDGSSGNTIYF local    AKDG_1_4
    ## 2    CASAKDGSDTQYF CASSAKDGSSGNTIYF local    AKDG_1_4
    ## 3  CASSASDLAKNIQYF    CSAASDLGYTQYF local    ASDL_1_6
    ## 4 CATSDAFGGAPDTQYF  CASSLDAFGTHGYTF local    DAFG_2_5
    ## 5   CSASPPGDAFGYTF  CASSLDAFGTHGYTF local    DAFG_2_5
    ## 6  CASSLDAFGTHGYTF  CASSLDAFGTHGYTF local    DAFG_2_5

## Motif Discovery with findMotifs()

The `findMotifs()` function searches for continuous and discontinuous
k-mer motifs in a set of CDR3 sequences. It is used internally by
`runGLIPH()` but can also be called independently:

``` r
# Extracting sequences
sample_seqs <- immApex::getIR(scRep_example, 
                              chains = "TRB")[seq_len(200), "cdr3_aa"]

# Find all 3-mers appearing at least 5 times
motifs <- findMotifs(seqs = sample_seqs, q = 3, kmer_mindepth = 5)
head(motifs[order(motifs$V1, decreasing = TRUE), ])
```

    ##    motif  V1
    ## 56   CAS 164
    ## 22   ASS 157
    ## 31   GEL  92
    ## 61   LFF  92
    ## 71   ELF  90
    ## 76   TGE  89

Including discontinuous motifs (e.g., `C.S` where `.` is any amino
acid):

``` r
disc_motifs <- findMotifs(
  seqs         = sample_seqs,
  q            = 2,
  kmer_mindepth = 5,
  discontinuous = TRUE
)
disc_only <- disc_motifs[grep("\\.", disc_motifs$motif), ]
head(disc_only[order(disc_only$V1, decreasing = TRUE), ])
```

    ##     motif  V1
    ## 91     S. 391
    ## 92     .S 391
    ## 102    .A 344
    ## 112    A. 332
    ## 74     .F 322
    ## 113    R. 292

## Customizing the Analysis

### Using method = “custom”

The `"custom"` method allows independent control over each algorithmic
component:

``` r
res_custom <- runGLIPH(
  cdr3_sequences  = scRep_example,
  method          = "custom",
  local_method    = "fisher",
  global_method   = "cutoff",
  clustering_method = "GLIPH1.0",
  scoring_method  = "GLIPH2.0",
  sim_depth       = 100,
  n_cores         = 1
)
```

### Adjusting Significance Thresholds

For the Fisher-based local method (GLIPH2), you can adjust:

- **`lcminp`**: Maximum p-value for motif enrichment (default 0.01)
- **`lcminove`**: Minimum fold-enrichment per motif length (default
  `c(1000, 100, 10)` for 2-mers, 3-mers, 4-mers)
- **`kmer_mindepth`**: Minimum motif observations in the sample (default
  3)

``` r
res_strict <- runGLIPH(
  cdr3_sequences = scRep_example,
  method         = "gliph2",
  lcminp         = 0.001,
  lcminove       = c(10000, 1000, 100),
  sim_depth      = 100,
  n_cores        = 1
)
```

### Choosing a Reference Database

immGLIPH ships with reference repertoires for human and mouse from the
original GLIPH publications:

| Name                | Species | Version | Subset            |
|:--------------------|:--------|:--------|:------------------|
| `"human_v2.0_CD48"` | Human   | v2.0    | CD4+CD8 (default) |
| `"human_v2.0_CD4"`  | Human   | v2.0    | CD4               |
| `"human_v2.0_CD8"`  | Human   | v2.0    | CD8               |
| `"human_v1.0_CD48"` | Human   | v1.0    | CD4+CD8           |
| `"mouse_v1.0_CD48"` | Mouse   | v1.0    | CD4+CD8           |

## Network Visualization

The `plotNetwork()` function creates an interactive network
visualization of the convergence groups using the visNetwork package:

``` r
plotNetwork(
  clustering_output = res_gliph2,
  color_info        = "total.score",
  cluster_min_size  = 3,
  n_cores           = 1
)
```

## De Novo TCR Generation

The `deNovoTCRs()` function generates artificial CDR3$`\beta`$ sequences
that resemble the positional amino acid composition of a given
convergence group. This can be used to predict novel TCR sequences with
similar binding characteristics:

``` r
de_novo <- deNovoTCRs(
  convergence_group_tag = res_gliph2$cluster_properties$tag[1],
  clustering_output     = res_gliph2,
  sims                  = 10000,
  num_tops              = 100,
  make_figure           = TRUE,
  n_cores               = 1
)

head(de_novo$de_novo_sequences)
```
