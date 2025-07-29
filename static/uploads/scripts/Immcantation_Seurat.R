library(dplyr)
library(harmony)
library(scDblFinder)
library(scRepertoire)
library(Seurat)

###############################
# Getting Sample Locations
###############################

sequencing.runs <- list.files(
  path = "./Alignments",
  pattern = "filtered_feature_bc_matrix",
  recursive = TRUE
)

######################################
# Iterating Through Sample Processing
######################################

Seurat.list <- lapply(sequencing.runs, function(x) {
  sample <- strsplit(x, "/")[[1]][1]
  tmp_assay <- Read10X_h5(paste0("./Alignments/", x))
  
  # Create a Seurat object with the specified project name (using the sample name)
  SeuratObj <- CreateSeuratObject(counts = tmp_assay, 
                                  assay = "RNA",
                                  project = sample)
  
  # Filter out low-quality cells (cells with fewer than 100 features)
  SeuratObj <- subset(SeuratObj, subset = nFeature_RNA > 100)
  
  # Rename cells to include sample name as a prefix
  SeuratObj <- RenameCells(SeuratObj, new.names = paste0(sample, "_", rownames(SeuratObj[[]])))
  
  
  # Calculate the percentage of mitochondrial and ribosomal gene expression
  SeuratObj[["mito.genes"]] <- PercentageFeatureSet(SeuratObj, pattern = "^MT-")
  SeuratObj[["ribo.genes"]] <- PercentageFeatureSet(SeuratObj, pattern = "^RPS|RPL-")
  
  ##########################################
  # Filtering Step Based on QC Metrics
  ##########################################
  # Compute a cutoff based on 2.5 standard deviations above the mean of log(nCount_RNA)
  standev <- sd(log(SeuratObj$nCount_RNA)) * 2.5
  mean_val <- mean(log(SeuratObj$nCount_RNA))
  cut <- round(exp(standev + mean_val))
  
  # Subset the Seurat object based on mitochondrial and feature count thresholds
  SeuratObj <- subset(SeuratObj, subset = mito.genes < 10 & nCount_RNA < cut)
  
  ##########################################
  # Estimate Doublets using scDblFinder
  ##########################################
  sce <- as.SingleCellExperiment(SeuratObj)
  sce <- scDblFinder(sce)
  doublets <- data.frame(db.class = sce$scDblFinder.class, 
                         db.score = sce$scDblFinder.score)
  rownames(doublets) <- rownames(sce@colData)
  SeuratObj <- AddMetaData(SeuratObj, metadata = doublets)
  
  ##########################################
  # Add BCR Clonotype Information
  ##########################################
  BCR.Contigs <- read.csv(paste0("./Alignments/", sample, "/BCR/filtered_contig_annotations.csv"))
  combinedObject <- combineBCR(BCR.Contigs, 
                               samples = sample, 
                               filterMulti = TRUE, 
                               removeNA = TRUE)
  SeuratObj <- combineExpression(combinedObject, 
                                 SeuratObj, 
                                 cloneCall = "CTstrict")
  
  ##########################################
  #Final Filtering
  ##########################################
  single.chains <- grep("NA_|_NA", SeuratObj$CTaa)
  no.chains <- as.vector(which(is.na(SeuratObj$CTaa)))
  doublets <- which(SeuratObj$db.class == "doublet")
  idx.to.remove <- unique(c(single.chains, no.chains, doublets))
  
  SeuratObj <- subset(SeuratObj, 
                      cells = colnames(SeuratObj)[setdiff(seq_len(length(colnames(SeuratObj))), idx.to.remove)])
  
  return(SeuratObj)
})

###############################
# Dimensional Reduction
###############################
SeuratObject <- merge(Seurat.list[[1]], Seurat.list[-1])
SeuratObject <- SeuratObject %>%
  JoinLayers() %>%
  NormalizeData() %>%
  FindVariableFeatures() 

# Removing IG V(D)J Genes from Variable Features
VariableFeatures(SeuratObject) = scRepertoire::quietBCRgenes(VariableFeatures(SeuratObject))

SeuratObject <- SeuratObject %>%
  ScaleData(vars.to.regress = "mito.genes") %>%
  RunPCA(npcs = 40) %>%
  RunHarmony(group.by.vars = "orig.ident", max_iter = 20) %>%
  RunUMAP(reduction = "harmony", dims = 1:20) %>%
  FindNeighbors(reduction = "harmony", dims = 1:20) %>%
  FindClusters(resolution = 0.4, algorithm = 3)

# Removing Data to minimize size
SeuratObject@assays$RNA$scale.data <- NULL
SeuratObject@graphs$RNA_nn <- NULL
SeuratObject@graphs$RNA_snn <- NULL
SeuratObject@reductions$pca <- NULL

saveRDS(SeuratObject, "Immcantation_SeuratObject.rds")
