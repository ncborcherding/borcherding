---
title: Utility
summary: Collection of Tumor-Infiltrating Lymphocyte Single-Cell Experiments with TCR 
tags:
- Single-Cell
- TCR
- Immunology
date: "2023-01-06T00:00:00Z"

# Optional external URL for project (replaces project detail page).
external_link: "https://github.com/ncborcherding/utility"

links:
- icon: twitter
  icon_pack: fab
  name: Follow
  url: https://twitter.com/theHumanBorch
url_code: "https://github.com/ncborcherding/utility/tree/dev"
#url_pdf: ""
#url_slides: ""
#url_video: ""
---

The original intent of assembling a data set of publicly-available tumor-infiltrating T cells (TILs) with paired TCR sequencing was to expand 
and improve the [scRepertoire](https://github.com/ncborcherding/scRepertoire) R package. However, after some discussion, we decided to release 
the data set for everyone, a complete summary of the sequencing runs and the sample information can be found in the meta data of the Seurat object. 

### Folder Structure
```
├── Data_conversion.Rmd
├── NEWS.txt
├── Processing_Utility.Rmd
├── README.md
├── Summarize_Data.Rmd
├── annotation
├── data
│   ├── SequencingRuns - 10x Outputs
│ └── processedData - Processed .rds
├── qc
├── scGateDB
└── summaryInfo
    ├── TcellSummaryTable.csv
    ├── cohortSummaryTable.csv
    ├── meta.data.headers.txt - what the meta data headers mean
    ├── sample.directory.xlsx - all the available data for the cohort
    ├── sessionInfo.txt - what I am running in terms of the pipeline
    └── tumorSummaryTable.csv
```

### Sample ID:

<img align="center" src="https://github.com/ncborcherding/utility/blob/dev/www/utility.graphic.png">

#### Cohort Information
Here is the current list of data sources, the number of cells that passed filtering by tissue type. Please cite the data if you are using utility!

|             | Blood | Juxta | LN   | Met | Normal | Tumor | Cancer Type | Date Added | Citation |
|-------------|-------|-------|------|-----|---|-------|-------------|------------|----------|
| CCR-20-4394 | 0     | 0     | 0    | 0   |0      | 26760 | Ovarian     | 6/19/21 |[cite](https://clincancerres.aacrjournals.org/content/early/2021/06/10/1078-0432.CCR-20-4394) |
| EGAS00001004809| 0     | 0     | 0    | 0   | 0      | 181667 | Breast      | 3/30/22 |[cite](https://pubmed.ncbi.nlm.nih.gov/33958794/) |
| GSE114724   | 0     | 0     | 0    | 0   | 0      | 27651 | Breast      | 6/19/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/29961579/) |
| GSE121636   | 12319 | 0     | 0    | 0   | 0      | 11436 | Renal       | 6/19/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/33504936/) |
| GSE123814   | 0     | 0     | 0    | 0   |0      | 77496 | Multiple    | 7/4/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/31359002/) |
| GSE139555   | 20664 | 0     | 0    | 0   | 69827  | 83301 | Multiple    | 6/19/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/32103181/) |
| GSE145370   | 0     | 0     | 0    | 0   | 40916  | 66592 | Esophageal  | 6/19/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/33293583/) |
| GSE148190   | 6201  | 0     | 15644| 0   | 0      | 2263  | Melanoma    | 6/19/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/32539073/) |
| GSE154826   | 0     | 0     | 0    | 0   | 13414   | 14491  | Lung    | 9/21/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/34767762/) |
| GSE159251   | 47721 | 0     | 5705 | 0   | 0      | 8355  | Melanoma    | 9/21/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/32539073/) |
| GSE162500   | 23401 | 3761  | 0    | 0   | 0      | 14644 | Lung        | 6/19/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/33514641/) |
| GSE164522   | 46027 | 0     | 46376|36648 | 86811 | 36990 | Colorectal | 6/25/22 | [cite](https://pubmed.ncbi.nlm.nih.gov/35303421/) |
| GSE176021   | 132673| 0     | 71062|32011 |128387 | 436608 | Lung      | 8/1/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/34290408/) |
| GSE179994   | 0     | 0     | 0    | 0   |0       | 140915 | Lung      | 3/30/22 |[cite](https://pubmed.ncbi.nlm.nih.gov/35121991/) |
| GSE180268   | 0     | 0     | 29699| 0   | 0      | 23215 | HNSCC      | 9/21/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/34471285/) |
| GSE180268   | 40429 | 0     | 0    | 0   | 27622  | 40429 | Renal      | 3/30/31 |[cite](https://pubmed.ncbi.nlm.nih.gov/35668194/) |
| GSE195486   | 0     | 0     | 0    | 0   | 0      | 122511 | Ovarian   | 6/25/22 |[cite](https://pubmed.ncbi.nlm.nih.gov/35427494/) |
| GSE200996   | 1211659| 0    | 0    | 0   | 0      | 86235  | HNSCC     | 7/15/22 | [cite](https://pubmed.ncbi.nlm.nih.gov/35803260/) | 
| PRJNA705465 | 30340 | 0     | 3505 | 0   | 15113  | 97966 | Renal      | 9/21/21 |[cite](https://pubmed.ncbi.nlm.nih.gov/33861994/) |
