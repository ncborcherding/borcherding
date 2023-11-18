---
title: Utility
summary: Collection of Tumor-Infiltrating Lymphocyte Single-Cell Experiments with TCRs
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
url_code: "https://github.com/ncborcherding/utility/"
#url_pdf: ""
#url_slides: ""
#url_video: ""
---

The original intent of assembling a data set of publicly-available tumor-infiltrating T cells (TILs) with paired TCR sequencing was to expand 
and improve the [scRepertoire](https://github.com/ncborcherding/scRepertoire) R package. However, after some discussion, we decided to release 
the data set for everyone, a complete summary of the sequencing runs and the sample information can be found in the meta data of the Seurat object. 

### Folder Structure
```
├── code
│   ├── Processing_Utility.Rmd - general processing script
│   └── Summarize_Data.Rmd - script to get summary data
├── data
│   ├── SequencingRuns - 10x Outputs
│   └── processedData - Processed .rds and larger combined cohorts
├── NEWS.txt - changes made
├── outputs
│   └── qc - plots for quality control purposes
├── README.md
└── summaryInfo
    ├── TcellSummaryTable.csv
    ├── cohortSummaryTable.csv
    ├── meta.data.headers.txt - what the meta data headers mean
    ├── sample.directory.xlsx - all the available data for the cohort
    ├── sessionInfo.txt - what I am running in terms of the pipeline
    └── tumorSummaryTable.csv

```

### Sample ID:

<img align="center" src="https://github.com/ncborcherding/utility/blob/main/www/utility_info.png">


#### Cohort Information
Here is the current list of data sources, the number of cells that passed filtering by tissue type. **Please cite** the data if you are using uTILity.


|                  | Tumor  | Normal | Blood  | Juxta | LN    | Met   | Cancer Type   | Citations                                         |
|------------------|--------|--------|--------|-------|-------|-------|---------------|---------------------------------------------------|
| CCR-20-4394      | 26760  | 0      | 0      | 0     | 0     | 0     | Ovarian       | [cite](https://pubmed.ncbi.nlm.nih.gov/33963000/) |
| EGAS00001004809  | 181667 | 0      | 0      | 0     | 0     | 0     | Breast        | [cite](https://pubmed.ncbi.nlm.nih.gov/33958794/) |
| GSE114724        | 27651  | 0      | 0      | 0     | 0     | 0     | Breast        | [cite](https://pubmed.ncbi.nlm.nih.gov/29961579/) |
| GSE121636        | 11436  | 0      | 12319  | 0     | 0     | 0     | Renal         | [cite](https://pubmed.ncbi.nlm.nih.gov/33504936/) |
| GSE123814        | 78034  | 0      | 0      | 0     | 0     | 0     | Multiple      | [cite](https://pubmed.ncbi.nlm.nih.gov/31359002/) |
| GSE139555        | 93160  | 78625  | 25363  | 0     | 0     | 0     | Multiple      | [cite](https://pubmed.ncbi.nlm.nih.gov/32103181/) |
| GSE145370        | 66592  | 40916  | 0      | 0     | 0     | 0     | Esophageal    | [cite](https://pubmed.ncbi.nlm.nih.gov/33293583/) |
| GSE148190        | 2263   | 0      | 6201   | 0     | 15644 | 0     | Melanoma      | [cite](https://pubmed.ncbi.nlm.nih.gov/32539073/) |
| GSE154826        | 14491  | 13414  | 0      | 0     | 0     | 0     | Lung          | [cite](https://pubmed.ncbi.nlm.nih.gov/34767762/) |
| GSE159251        | 8356   | 0      | 47721  | 0     | 5705  | 0     | Melanoma      | [cite](https://pubmed.ncbi.nlm.nih.gov/32539073/) |
| GSE162500        | 14644  | 0      | 23401  | 3761  | 0     | 0     | Lung          | [cite](https://pubmed.ncbi.nlm.nih.gov/33514641/) |
| GSE164522        | 36990  | 86811  | 46027  | 0     | 46376 | 36648 | Colorectal    | [cite](https://pubmed.ncbi.nlm.nih.gov/35303421/) |
| GSE168844        | 0      | 0      | 55302  | 0     | 0     | 0     | Lung          | [cite](https://pubmed.ncbi.nlm.nih.gov/36219677/) |
| GSE176021        | 436609 | 128411 | 132673 | 0     | 71063 | 32011 | Lung          | [cite](https://pubmed.ncbi.nlm.nih.gov/34290408/) |
| GSE179994        | 78574  | 0      | 0      | 0     | 0     | 62341 | Lung          | [cite](https://pubmed.ncbi.nlm.nih.gov/35121991/) |
| GSE180268        | 23215  | 0      | 0      | 0     | 29699 | 0     | HNSCC         | [cite](https://pubmed.ncbi.nlm.nih.gov/34471285/) |
| GSE181061        | 40429  | 27622  | 37426  | 0     | 0     | 0     | Renal         | [cite](https://pubmed.ncbi.nlm.nih.gov/35668194/) |
| GSE185206        | 163294 | 17231  | 0      | 0     | 9820  | 0     | Lung          | [cite](https://pubmed.ncbi.nlm.nih.gov/37001526/) |
| GSE195486        | 122512 | 0      | 0      | 0     | 0     | 0     | Ovarian       | [cite](https://pubmed.ncbi.nlm.nih.gov/35427494/) |
| GSE200218        | 0     | 0       | 0      | 0     | 0     | 18495 | Melanoma      | [cite](https://pubmed.ncbi.nlm.nih.gov/35803246/) |
| GSE200996        | 86235 | 0       | 152722 | 0     | 0     | 0     | HNSCC         | [cite](https://pubmed.ncbi.nlm.nih.gov/35803260/) |
| GSE201425        | 22888 | 0       | 27781  | 0     | 11350 | 12253 | Biliary       | [cite](https://pubmed.ncbi.nlm.nih.gov/35982235/) | 
| GSE211504        | 0     | 0       | 33685  | 0     | 0     | 0     | Melanoma      | [cite](https://pubmed.ncbi.nlm.nih.gov/35907015/) |
| GSE212217        | 0     | 0       | 229505 | 0     | 0     | 0     | Endometrial   | [cite](https://pubmed.ncbi.nlm.nih.gov/36301137/) |
| GSE213243        | 2835  | 0       | 18363  | 0     | 0     | 2693  | Ovarian       | [cite](https://pubmed.ncbi.nlm.nih.gov/36248860/) |
| GSE215219        | 26303 | 0       | 66000  | 0     | 0     | 0     | Lung          | [cite](https://pubmed.ncbi.nlm.nih.gov/37476074/) |
| GSE227708        | 53087 | 0       | 0      | 0     | 0     | 0     | Merkel Cell   | [cite](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi) |
| GSE242477        | 41595 | 0       | 21595  | 0     | 0     | 0     | Melanoma      | [cite](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE242477) |
| PRJNA705464      | 98892 | 15113   | 30340  | 0     | 3505  | 0     | Renal         | [cite](https://pubmed.ncbi.nlm.nih.gov/33861994/) |