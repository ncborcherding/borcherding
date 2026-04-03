# Bridging Python TCR Tools with immLynx

## Getting Started

**immLynx** is a comprehensive R package that bridges popular
Python-based immune repertoire analysis tools and Hugging Face protein
language models into the R environment. It provides unified interfaces
for:

- TCR distance calculations
  ([tcrdist3](https://github.com/kmayerb/tcrdist3))
- Sequence generation probability
  ([OLGA](https://github.com/statbiophys/OLGA))
- Selection inference ([soNNia](https://github.com/statbiophys/soNNia))
- TCR clustering ([clusTCR](https://github.com/svalkiers/clusTCR))
- Protein language model embeddings
  ([ESM-2](https://github.com/facebookresearch/esm))
- Metaclone discovery
  ([metaclonotypist](https://github.com/emerson-hammer/metaclonotypist))

immLynx is fully compatible with the
[scRepertoire](https://github.com/BorchLab/scRepertoire) and
[immApex](https://github.com/BorchLab/immApex) ecosystem for single-cell
immune repertoire analysis.

More information is available at the [immLynx GitHub
Repo](https://github.com/BorchLab/immLynx).

### Installation

``` r
devtools::install_github("BorchLab/immLynx")
```

#### Python Dependencies

immLynx uses [basilisk](https://bioconductor.org/packages/basilisk/) to
manage Python dependencies automatically. The first time you use
functions that call Python, basilisk will create an isolated conda
environment with all required packages. This may take a few minutes on
first run.

### The Data Set

To demonstrate the analysis functions in immLynx, we will use the
scRepertoire example data derived from T cells of 4 patients with acute
respiratory distress. The data contains paired peripheral-blood (B) and
bronchoalveolar lavage (L) samples across 8 distinct runs from the 10x
Cell Ranger pipeline.

### Loading Libraries and Data

``` r
suppressMessages(library(scRepertoire))
suppressMessages(library(immLynx))
suppressMessages(library(Seurat))
suppressMessages(library(ggplot2))
suppressMessages(library(viridis))
suppressMessages(library(dplyr))

data("contig_list")
combined.TCR <- combineTCR(contig_list,
                           samples = c("P17B", "P17L", "P18B", "P18L",
                                            "P19B","P19L", "P20B", "P20L"))

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

## Extracting and Validating TCR Data

Before running analyses, you can extract and validate TCR data from the
single-cell object:

``` r
# Extract beta chain data
tcr_data <- extractTCRdata(scRep_example, chains = "TRB")
head(tcr_data)

# Extract both chains in wide format
tcr_wide <- extractTCRdata(scRep_example, chains = "both", format = "wide")

# Validate the data
validation <- validateTCRdata(tcr_data)
print(validation)
```

## Summarizing the TCR Repertoire

Get a comprehensive overview of the TCR repertoire:

``` r
summary <- summarizeTCRrepertoire(scRep_example, chains = "TRB")
print(summary)
```

## Analysis Functions

### TCR Clustering with clusTCR

Cluster TCRs based on sequence similarity using the clusTCR algorithm.
The MCL (Markov Clustering) algorithm identifies groups of TCRs with
similar CDR3 sequences:

``` r
scRep_example <- runClustTCR(
  scRep_example,
  chains = "TRB",
  method = "mcl",
  inflation = 2.0
)

table(scRep_example$clustcr_TRB)
```

#### Comparing Clustering Parameters

Different inflation parameters control the granularity of clustering:

``` r
# MCL clustering with different inflation parameters
scRep_example <- runClustTCR(scRep_example, method = "mcl", inflation = 2.0,
                            column_prefix = "mcl_2")
scRep_example <- runClustTCR(scRep_example, method = "mcl", inflation = 3.0,
                            column_prefix = "mcl_3")

# DBSCAN clustering
scRep_example <- runClustTCR(scRep_example, method = "dbscan", eps = 0.5,
                             column_prefix = "dbscan")

# Compare number of clusters
cat("MCL (inflation=2):", length(unique(na.omit(scRep_example$mcl_2_TRB))), "clusters\n")
cat("MCL (inflation=3):", length(unique(na.omit(scRep_example$mcl_3_TRB))), "clusters\n")
cat("DBSCAN:", length(unique(na.omit(scRep_example$dbscan_TRB))), "clusters\n")
```

### TCR Distance Calculations with tcrdist3

Calculate pairwise TCR distances using the tcrdist3 framework:

``` r
dist_results <- runTCRdist(
  scRep_example,
  chains = "beta",
  organism = "human"
)

dim(dist_results$distances$pw_beta)
```

The distance matrix can also be used for hierarchical clustering or
other downstream analyses:

``` r
d <- as.dist(dist_results$distances$pw_beta)
hc <- hclust(d, method = "complete")
clusters <- cutree(hc, k = 50)
```

### Generation Probability with OLGA

Calculate the generation probability (Pgen) for TCR sequences. Pgen
reflects the probability of a given TCR sequence being generated by
V(D)J recombination:

``` r
scRep_example <- runOLGA(
  scRep_example,
  chains = "TRB",
  model = "humanTRB"
)

hist(log10(scRep_example$olga_pgen_TRB),
     breaks = 50,
     main = "Distribution of TCR Generation Probabilities",
     xlab = "log10(Pgen)")
```

#### Comparing Pgen Across Sample Types

Cells with low Pgen may be under stronger selection because they are
rare in the naive repertoire:

``` r
ggplot(scRep_example@meta.data, aes(x = Type, y = olga_pgen_log10_TRB)) +
  geom_boxplot() +
  labs(title = "TCR Generation Probability by Sample Type",
       x = "Sample Type",
       y = "log10(Pgen)") +
  theme_classic()
```

#### Generating Random TCR Sequences

OLGA can also generate random TCR sequences from the recombination
model:

``` r
random_seqs <- generateOLGA(n = 100, model = "humanTRB")
head(random_seqs)
```

### Protein Language Model Embeddings

Generate TCR embeddings using ESM-2 protein language models. These
embeddings capture biochemical and structural properties of the CDR3
sequences:

``` r
scRep_example <- runEmbeddings(
  scRep_example,
  chains = "TRB",
  model_name = "facebook/esm2_t12_35M_UR50D",
  pool = "mean"
)

scRep_example <- RunUMAP(scRep_example,
                          reduction = "tcr_esm",
                          dims = 1:30,
                          reduction.name = "tcr_umap",
                          reduction.key = "tcrUMAP_")

DimPlot(scRep_example, reduction = "tcr_umap")
```

#### Comparing ESM-2 Model Sizes

ESM-2 comes in different sizes. Larger models may capture more nuanced
biochemical properties but require more computational resources:

``` r
# Small model (35M parameters) - fast, lower quality
scRep_example <- runEmbeddings(
  scRep_example,
  model_name = "facebook/esm2_t12_35M_UR50D",
  reduction_name = "esm_small"
)

# Medium model (650M parameters) - balanced
scRep_example <- runEmbeddings(
  scRep_example,
  model_name = "facebook/esm2_t33_650M_UR50D",
  reduction_name = "esm_medium"
)

# Compare embeddings via UMAP
scRep_example <- RunUMAP(scRep_example, reduction = "esm_small", dims = 1:30,
                          reduction.name = "umap_small", reduction.key = "umapSmall_")
scRep_example <- RunUMAP(scRep_example, reduction = "esm_medium", dims = 1:30,
                          reduction.name = "umap_medium", reduction.key = "umapMed_")

p1 <- DimPlot(scRep_example, reduction = "umap_small") + ggtitle("ESM-2 35M")
p2 <- DimPlot(scRep_example, reduction = "umap_medium") + ggtitle("ESM-2 650M")
p1 + p2
```

#### Embedding Both Chains

For paired alpha-beta TCR analysis:

``` r
scRep_example <- runEmbeddings(
  scRep_example,
  chains = "both",
  reduction_name = "tcr_paired"
)

scRep_example <- RunUMAP(scRep_example,
                          reduction = "tcr_paired",
                          dims = 1:30,
                          reduction.name = "paired_umap",
                          reduction.key = "pairedUMAP_")

DimPlot(scRep_example, reduction = "paired_umap")
```

#### Custom Embedding Workflow

For advanced users who need fine-grained control over the embedding
process, immLynx exposes the lower-level functions used internally by
[`runEmbeddings()`](https://rdrr.io/pkg/immLynx/man/runEmbeddings.html):

``` r
# Step 1: Load model and tokenizer
model_info <- huggingModel(model_name = "facebook/esm2_t12_35M_UR50D")

# Step 2: Extract CDR3 sequences
sequences <- scRep_example$CTaa
sequences <- gsub("_.*", "", sequences)  # Get first chain
sequences <- unique(na.omit(sequences))

# Step 3: Tokenize sequences
tokenized <- tokenizeSequences(
  tokenizer = model_info$tokenizer,
  aa_sequences = sequences,
  padding = TRUE,
  truncation = TRUE
)

# Step 4: Generate embeddings with custom settings
embeddings <- proteinEmbeddings(
  model = model_info$model,
  tokenized.batch = tokenized,
  pool = "mean",
  prefer_device = "auto"
)

dim(embeddings)
```

### Metaclone Discovery with Metaclonotypist

Identify TCR metaclones - groups of related T cell receptors that may
recognize similar antigens:

``` r
scRep_example <- runMetaclonotypist(
  scRep_example,
  chains = "beta",
  method = "tcrdist",
  max_edits = 2,
  max_dist = 20
)

table(scRep_example$metaclone)
```

### HLA Association Analysis

If HLA typing data is available, you can test associations between
metaclone membership and HLA alleles using Fisher’s exact test with FDR
correction:

``` r
# First run metaclonotypist
metaclones <- runMetaclonotypist(scRep_example, return_seurat = FALSE)

# Create mock HLA data (replace with real HLA typing data)
hla_data <- data.frame(
  barcode = metaclones$barcode,
  HLA_A_01_01 = sample(c(TRUE, FALSE), nrow(metaclones), replace = TRUE),
  HLA_A_02_01 = sample(c(TRUE, FALSE), nrow(metaclones), replace = TRUE),
  HLA_B_07_02 = sample(c(TRUE, FALSE), nrow(metaclones), replace = TRUE)
)

# Test associations
hla_results <- runHLAassociation(metaclones, hla_data)
head(hla_results)
```

### Selection Inference with soNNia

Infer selection pressures on TCRs using the soNNia framework. This
requires a background set of sequences for comparison:

``` r
# Generate background sequences
background <- generateOLGA(n = 10000, model = "humanTRB")
write.csv(background, "background.csv", row.names = FALSE)

# Run soNNia
scRep_example <- runSoNNia(
  scRep_example,
  chains = "TRB",
  background_file = "background.csv"
)
```

## Combined Analysis Workflow

Here is a complete workflow combining multiple immLynx analyses with the
scRepertoire example data:

``` r
library(immLynx)
library(Seurat)
library(ggplot2)

# Step 1: Cluster TCRs
scRep_example <- runClustTCR(
  scRep_example,
  chains = "TRB",
  method = "mcl"
)

# Step 2: Calculate generation probability
scRep_example <- runOLGA(
  scRep_example,
  chains = "TRB"
)

# Step 3: Generate embeddings
scRep_example <- runEmbeddings(
  scRep_example,
  chains = "TRB"
)

# Step 4: Visualize embeddings
scRep_example <- RunUMAP(
  scRep_example,
  reduction = "tcr_esm",
  dims = 1:30,
  reduction.name = "tcr_umap",
  reduction.key = "tcrUMAP_"
)

# Plot by cluster
plot1 <- DimPlot(scRep_example,
                 reduction = "tcr_umap",
                 group.by = "clustcr_TRB") + NoLegend()

# Plot by Pgen
plot2 <- FeaturePlot(scRep_example,
                     reduction = "tcr_umap",
                     features = "olga_pgen_log10_TRB") +
         scale_color_viridis()

plot1 + plot2
```

## Integration with scRepertoire Clonotypes

immLynx clustering results can be compared directly with scRepertoire
clonotype assignments:

``` r
scRep_example <- runClustTCR(scRep_example, chains = "TRB")

comparison <- table(
  clustcr = scRep_example$clustcr_TRB,
  clonotype = scRep_example$CTstrict
)

cat("Number of clustcr clusters:", nrow(comparison), "\n")
cat("Number of unique clonotypes:", ncol(comparison), "\n")
```

## Exporting Results

Export TCR data for use with external tools:

``` r
# Export TCR data in tcrdist3 format
tcr_data <- extractTCRdata(scRep_example, chains = "both", format = "wide")
tcrdist_format <- convertToTcrdist(tcr_data, chains = "both")
write.csv(tcrdist_format, "tcr_for_tcrdist.csv", row.names = FALSE)

# Export cluster assignments
clusters <- data.frame(
  barcode = colnames(scRep_example),
  clustcr = scRep_example$clustcr_TRB
)
write.csv(clusters, "cluster_assignments.csv", row.names = FALSE)

# Export embeddings
embeddings <- Embeddings(scRep_example, "tcr_esm")
write.csv(embeddings, "tcr_embeddings.csv")
```

## Working with Large Datasets

For large datasets, consider these strategies to manage memory and
computation:

``` r
# 1. Use smaller chunk sizes for embeddings
scRep_example <- runEmbeddings(
  scRep_example,
  chunk_size = 16,  # Smaller chunks for memory
  pool = "mean"
)

# 2. Sample for distance calculations
# For very large datasets, calculate distances on a subset
sample_cells <- sample(colnames(scRep_example), 5000)
subset_obj <- subset(scRep_example, cells = sample_cells)
dist_results <- runTCRdist(subset_obj)
```
