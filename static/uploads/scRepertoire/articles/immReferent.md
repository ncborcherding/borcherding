# Immune Reference Data with immReferent

## Introduction

The [immReferent](https://github.com/BorchLab/immReferent) package
provides a centralized interface for downloading, managing, and loading
immune repertoire and HLA reference sequences from
[IMGT](https://www.imgt.org/),
[IPD-IMGT/HLA](https://www.ebi.ac.uk/ipd/imgt/hla/), and
[OGRDB](https://ogrdb.airr-community.org/). It serves as a core
dependency for immunogenomics packages, ensuring reliable and
high-quality sequence access with local caching for reproducibility.

In the context of scRepertoire, immReferent is useful for:

- Obtaining the reference gene sequences used in TCR/BCR analysis
- Exporting formatted references for tools like MiXCR, TRUST4, Cell
  Ranger, and IgBLAST
- Ensuring offline reproducibility through its caching system

## Installation

``` r
devtools::install_github("BorchLab/immReferent")
```

Or via Bioconductor:

``` r
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("immReferent")
```

## Downloading Reference Sequences

``` r
library(immReferent)
```

### HLA Sequences (IPD-IMGT/HLA)

The IPD-IMGT/HLA database provides reference sequences for the Human
Leukocyte Antigen (HLA) system.

``` r
hla_prot <- getIMGT(gene = "HLA",
                    type = "PROT")

print(hla_prot)
```

    ## AAStringSet object of length 43002:
    ##         width seq                                           names               
    ##     [1]   365 MAVMAPRTLLLLLSGALALTQ...TQAASSDSAQGSDVSLTACKV HLA:HLA00001 A*01...
    ##     [2]   200 MAVMAPRTLLLLLSGALALTQ...GGARGTGLTAGSGPGSHTIQX HLA:HLA02169 A*01...
    ##     [3]   365 MAVMAPRTLLLLLSGALALTQ...TQAASSDSAQGSDVSLTACKV HLA:HLA14798 A*01...
    ##     [4]   365 MAVMAPRTLLLLLSGALALTQ...TQAASSDSAQGSDVSLTACKV HLA:HLA15760 A*01...
    ##     [5]   365 MAVMAPRTLLLLLSGALALTQ...TQAASSDSAQGSDVSLTACKV HLA:HLA16415 A*01...
    ##     ...   ... ...
    ## [42998]   704 MRLPDLRPWTSLLLVDAALLW...AQLQEGQDLYSRLVQQRLMDX HLA:HLA38075 TAP2...
    ## [42999]   704 MRLPDLRPWTSLLLVDAALLW...AQLQEGQDLYSRLVQQRLMDX HLA:HLA38025 TAP2...
    ## [43000]   704 MRLPDLRPWTSLLLADAALLW...AQLQEGQDLYSRLVQQRLMDX HLA:HLA38029 TAP2...
    ## [43001]   704 MRLPDLRPWTSLLLVDAALLW...AQLQEGQDLYSRLVQQRLMDX HLA:HLA38159 TAP2...
    ## [43002]   704 MRLPDLRPWTSLLLVDAALLW...AQLQEGQDLYSRLVQQRLMDX HLA:HLA38463 TAP2...

``` r
cat("Number of sequences:", length(hla_prot), "\n")
```

    ## Number of sequences: 43002

### TCR/BCR Sequences (IMGT)

For T-cell receptor (TCR) and B-cell receptor (BCR) genes, specify the
species and gene or gene family.

``` r
# Download human IGHV nucleotide sequences
ighv_nuc <- getIMGT(species = "human",
                    gene = "IGHV",
                    type = "NUC")
print(ighv_nuc)
```

    ## DNAStringSet object of length 480:
    ##       width seq                                             names               
    ##   [1]   320 CAGGTTCAGCTGGTGCAGTCTG...CCGTGTATTACTGTGCGAGAGA M99641|IGHV1-18*0...
    ##   [2]   300 CAGGTTCAGCTGGTGCAGTCTG...CCTAAGATCTGACGACACGGCC X60503|IGHV1-18*0...
    ##   [3]   320 CAGGTTCAGCTGGTGCAGTCTG...CCGTGTATTACTGTGCGAGAGA HM855463|IGHV1-18...
    ##   [4]   320 CAGGTTCAGCTGGTGCAGTCTG...CCGTGTATTACTGTGCGAGAGA KC713938|IGHV1-18...
    ##   [5]   320 CAGGTGCAGCTGGTGCAGTCTG...TCGTGTATTACTGTGCGAGAGA X07448|IGHV1-2*01...
    ##   ...   ... ...
    ## [476]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA AB019438|IGHV8-51...
    ## [477]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA BK063799|IGHV8-51...
    ## [478]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA IMGT000055|IGHV8-...
    ## [479]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA AC279961|IGHV8-51...
    ## [480]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA BK068299|IGHV8-51...

You can also download entire families of genes at once:

``` r
# Download all mouse TRB genes (V, D, J, and C)
trb_mouse <- getIMGT(species = "mouse",
                     gene = "TRB",
                     type = "NUC")
print(trb_mouse)
```

    ## DNAStringSet object of length 75:
    ##      width seq                                              names               
    ##  [1]   326 GTGACTTTGCTGGAGCAAAACCC...TGTACTGCACCTGCAGTGCAGA AE000663|TRBV1*01...
    ##  [2]   324 GTGACTTTGCTGGAGCAAAACCC...CTTGTACTGCACCTGCAGTGCG X01642|TRBV1*02|M...
    ##  [3]   325 GATGGTGGAATCACCCAGACACC...TTCTGGGCCAGCAGTGAACAAA X16694|TRBV10*01|...
    ##  [4]   324 GATTCTGGGGTTGTCCAGTCTCC...GTACTTCTGTGCCAGCTCTCTC M15614|TRBV12-1*0...
    ##  [5]   321 GATTCTGGGGTTGTCCAGTCTCC...TATGTACTTCTGTGCCAGCTCT M30881|TRBV12-1*0...
    ##  ...   ... ...
    ## [71]    48 CAGCCCTTGCCCTGACTGATTGGCAGCCGATTGAACAGCCTATGCGAG K02802|TRBJ2-6*01...
    ## [72]    47 CTCCTATGAACAGTACTTCGGTCCCGGCACCAGGCTCACGGTTTTAG  K02802|TRBJ2-7*01...
    ## [73]    47 CTCCTATGAACAGTACTTCGGTCCCGGCACTAGGCTCACGGTTTTAG  M16122|TRBJ2-7*02...
    ## [74]   519 NAGGATCTGAGAAATGTGACTCC...CATGGTCAAGAAAAAAAATTCC M26057+M26058+M26...
    ## [75]   519 NAGGATCTGAGAAATGTGACTCC...CATGGTCAAGAAAAAAAATTCC AE000665|TRBC2*03...

### Germline Sets from OGRDB (AIRR)

OGRDB provides AIRR-compliant germline sets for immunoglobulin loci.

``` r
# Human IGH nucleotide sequences (gapped FASTA)
igh_ogrdb <- getOGRDB(
  species = "human",
  locus   = "IGH",
  type    = "NUC",
  format  = "FASTA_GAPPED"
)
igh_ogrdb
```

    ## DNAStringSet object of length 236:
    ##       width seq                                             names               
    ##   [1]    17 GGTACAACTGGAACGAC                               IGHD1-1*01
    ##   [2]    17 GGTATAACCGGAACCAC                               IGHD1-14*01
    ##   [3]    17 GGTATAACTGGAACGAC                               IGHD1-20*01
    ##   [4]    20 GGTATAGTGGGAGCTACTAC                            IGHD1-26*01
    ##   [5]    17 GGTATAACTGGAACTAC                               IGHD1-7*01
    ##   ...   ... ...
    ## [232]   320 CAGGTGCAGCTGGTGCAGTCTG...CCATGTATTACTGTGCGAGATA IGHV7-81*01
    ## [233]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA IGHV8-51-1*02
    ## [234]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA IGHV8-51-1*03
    ## [235]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA IGHV8-51-1*04
    ## [236]   320 GAGGCCCAGCTTACAGAGTCTG...CAGCATTTAACTGTGCAGGAAA IGHV8-51-1*05

## Exporting for External Tools

immReferent can export reference sequences formatted for popular
analysis tools.

``` r
igh_seqs <- getIMGT(species = "human",
                    gene = "IGH",
                    type = "NUC",
                    suppressMessages = TRUE)
```

### MiXCR

``` r
mixcr_dir <- tempdir()
mixcr_files <- exportMiXCR(igh_seqs,
                           mixcr_dir,
                           chain = "IGH")
print(mixcr_files)
```

    ## $v_genes
    ## [1] "/var/folders/g4/n0vf5jk16jl5b66c82xysg7m0000gp/T//RtmpSlB0xL/v-genes.IGH.fasta"
    ## 
    ## $d_genes
    ## [1] "/var/folders/g4/n0vf5jk16jl5b66c82xysg7m0000gp/T//RtmpSlB0xL/d-genes.IGH.fasta"
    ## 
    ## $j_genes
    ## [1] "/var/folders/g4/n0vf5jk16jl5b66c82xysg7m0000gp/T//RtmpSlB0xL/j-genes.IGH.fasta"

### TRUST4

``` r
trust4_file <- tempfile(fileext = ".fa")
exportTRUST4(igh_seqs, trust4_file)
cat(head(readLines(trust4_file), 4), sep = "\n")
```

    ## >IGHV1-18*01
    ## CAGGTTCAGCTGGTGCAGTCTGGAGCT...GAGGTGAAGAAGCCTGGGGCCTCAGTGAAGGTCTCCTGCAAGGCTTCTGG
    ## TTACACCTTT............ACCAGCTATGGTATCAGCTGGGTGCGACAGGCCCCTGGACAAGGGCTTGAGTGGATGG
    ## GATGGATCAGCGCTTAC......AATGGTAACACAAACTATGCACAGAAGCTCCAG...GGCAGAGTCACCATGACCACA

### Cell Ranger VDJ

``` r
cellranger_file <- tempfile(fileext = ".fa")
exportCellRanger(igh_seqs, cellranger_file)
cat(head(readLines(cellranger_file), 4), sep = "\n")
```

    ## >IGHV1-18*01
    ## CAGGTTCAGCTGGTGCAGTCTGGAGCT...GAGGTGAAGAAGCCTGGGGCCTCAGTGAAGGTCTCCTGCAAGGCTTCTGG
    ## TTACACCTTT............ACCAGCTATGGTATCAGCTGGGTGCGACAGGCCCCTGGACAAGGGCTTGAGTGGATGG
    ## GATGGATCAGCGCTTAC......AATGGTAACACAAACTATGCACAGAAGCTCCAG...GGCAGAGTCACCATGACCACA

### IgBLAST

``` r
igblast_dir <- tempdir()
igblast_files <- exportIgBLAST(igh_seqs, igblast_dir,
                               organism = "human",
                               receptor_type = "ig")
print(igblast_files)
```

    ## $v_genes
    ## [1] "/var/folders/g4/n0vf5jk16jl5b66c82xysg7m0000gp/T//RtmpSlB0xL/human_ig_v.fasta"
    ## 
    ## $d_genes
    ## [1] "/var/folders/g4/n0vf5jk16jl5b66c82xysg7m0000gp/T//RtmpSlB0xL/human_ig_d.fasta"
    ## 
    ## $j_genes
    ## [1] "/var/folders/g4/n0vf5jk16jl5b66c82xysg7m0000gp/T//RtmpSlB0xL/human_ig_j.fasta"

## Caching and Offline Usage

immReferent automatically caches all downloaded data locally. On
subsequent requests, the cached copy is loaded without network access.

``` r
# List all cached IMGT files
listIMGT()
```

    ##  [1] "/Users/borcherding.n/.immReferent/human/constant/imgt_human_IGHC.fasta"                                                                                                                                      
    ##  [2] "/Users/borcherding.n/.immReferent/human/hla/hla_nuc.fasta"                                                                                                                                                   
    ##  [3] "/Users/borcherding.n/.immReferent/human/hla/hla_prot.fasta"                                                                                                                                                  
    ##  [4] "/Users/borcherding.n/.immReferent/human/ogrdb/Human_IGH_VDJ_published_gapped.fasta"                                                                                                                          
    ##  [5] "/Users/borcherding.n/.immReferent/human/ogrdb/Human_IGKappa_VJ_aarch64-apple-darwin20_aarch64_darwin20_aarch64, darwin20__4_4.1_2024_06_14_86737_R_R version 4.4.1 (2024-06-14)_Race for Your Life_airr.json"
    ##  [6] "/Users/borcherding.n/.immReferent/human/ogrdb/Human_IGKappa_VJ_published_airr.json"                                                                                                                          
    ##  [7] "/Users/borcherding.n/.immReferent/human/ogrdb/Human_IGKappa_VJ_published_gapped.fasta"                                                                                                                       
    ##  [8] "/Users/borcherding.n/.immReferent/human/ogrdb/Human_IGLambda_VJ_published_ungapped.fasta"                                                                                                                    
    ##  [9] "/Users/borcherding.n/.immReferent/human/vdj_aa/imgt_aa_human_IGHV.fasta"                                                                                                                                     
    ## [10] "/Users/borcherding.n/.immReferent/human/vdj_aa/imgt_aa_human_TRBV.fasta"                                                                                                                                     
    ## [11] "/Users/borcherding.n/.immReferent/human/vdj/imgt_human_IGHD.fasta"                                                                                                                                           
    ## [12] "/Users/borcherding.n/.immReferent/human/vdj/imgt_human_IGHJ.fasta"                                                                                                                                           
    ## [13] "/Users/borcherding.n/.immReferent/human/vdj/imgt_human_IGHV.fasta"                                                                                                                                           
    ## [14] "/Users/borcherding.n/.immReferent/immReferent_log.yaml"                                                                                                                                                      
    ## [15] "/Users/borcherding.n/.immReferent/mouse/constant/imgt_mouse_TRBC.fasta"                                                                                                                                      
    ## [16] "/Users/borcherding.n/.immReferent/mouse/vdj/imgt_mouse_TRBD.fasta"                                                                                                                                           
    ## [17] "/Users/borcherding.n/.immReferent/mouse/vdj/imgt_mouse_TRBJ.fasta"                                                                                                                                           
    ## [18] "/Users/borcherding.n/.immReferent/mouse/vdj/imgt_mouse_TRBV.fasta"                                                                                                                                           
    ## [19] "/Users/borcherding.n/.immReferent/rabbit/vdj_aa/imgt_aa_rabbit_TRBV.fasta"                                                                                                                                   
    ## [20] "/Users/borcherding.n/.immReferent/rat/vdj/imgt_rat_IGHV.fasta"

To load strictly from cache (no downloads):

``` r
cached <- loadIMGT(species = "human",
                   gene = "IGHV",
                   type = "NUC")
```

To force a re-download when the online data has been updated:

``` r
fresh <- refreshIMGT(species = "human",
                     gene = "IGHV",
                     type = "NUC")
```

You can change the cache location for a session or permanently via
`.Rprofile`:

``` r
options(immReferent.cache = "/path/to/shared/cache")
```

## Session Info

``` r
sessionInfo()
```

    ## R version 4.5.1 (2025-06-13)
    ## Platform: aarch64-apple-darwin20
    ## Running under: macOS Sonoma 14.6
    ## 
    ## Matrix products: default
    ## BLAS:   /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/lib/libRblas.0.dylib 
    ## LAPACK: /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/lib/libRlapack.dylib;  LAPACK version 3.12.1
    ## 
    ## locale:
    ## [1] en_US.UTF-8/en_US.UTF-8/en_US.UTF-8/C/en_US.UTF-8/en_US.UTF-8
    ## 
    ## time zone: America/Chicago
    ## tzcode source: internal
    ## 
    ## attached base packages:
    ## [1] stats     graphics  grDevices utils     datasets  methods   base     
    ## 
    ## other attached packages:
    ## [1] immReferent_0.99.6
    ## 
    ## loaded via a namespace (and not attached):
    ##  [1] sass_0.4.10             generics_0.1.4          xml2_1.5.1             
    ##  [4] stringi_1.8.7           digest_0.6.39           magrittr_2.0.4         
    ##  [7] evaluate_1.0.5          fastmap_1.2.0           jsonlite_2.0.0         
    ## [10] processx_3.8.6          GenomeInfoDb_1.44.3     chromote_0.5.1         
    ## [13] ps_1.9.1                promises_1.5.0          httr_1.4.7             
    ## [16] rvest_1.0.5             selectr_0.5-0           UCSC.utils_1.4.0       
    ## [19] Biostrings_2.76.0       textshaping_1.0.4       jquerylib_0.1.4        
    ## [22] cli_3.6.5               rlang_1.1.6             crayon_1.5.3           
    ## [25] XVector_0.48.0          cachem_1.1.0            yaml_2.3.11            
    ## [28] otel_0.2.0              tools_4.5.1             GenomeInfoDbData_1.2.14
    ## [31] BiocGenerics_0.54.1     curl_7.0.0              vctrs_0.6.5            
    ## [34] R6_2.6.1                stats4_4.5.1            lifecycle_1.0.4        
    ## [37] stringr_1.6.0           S4Vectors_0.48.0        fs_1.6.6               
    ## [40] htmlwidgets_1.6.4       IRanges_2.42.0          ragg_1.5.0             
    ## [43] pkgconfig_2.0.3         desc_1.4.3              pkgdown_2.2.0          
    ## [46] bslib_0.9.0             pillar_1.11.1           later_1.4.4            
    ## [49] glue_1.8.0              Rcpp_1.1.0              systemfonts_1.3.1      
    ## [52] xfun_0.54               tibble_3.3.0            rstudioapi_0.17.1      
    ## [55] knitr_1.50              htmltools_0.5.9         websocket_1.4.4        
    ## [58] rmarkdown_2.30          compiler_4.5.1
