---
title: "T Cell Clonal Analysis Using Single-cell RNA Sequencing and Reference Maps"
authors:
- Massimo Andreatta
- Paul Gueguen
- admin
- Santiago Carmona
date: "2023-08-25T00:00:00Z"
doi: "10.21769/BioProtoc.4735 "

# Schedule page publish date (NOT publication's date).
publishDate: "2023-08-25T00:00:00Z"

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["2"]

# Publication name and optional abbreviated publication name.
publication: In *BioProtocol*
publication_short: In *BioProtocol*

abstract: T cells are endowed with T-cell antigen receptors (TCR) that give them the capacity to recognize specific antigens and mount antigen-specific adaptive immune responses. Because TCR sequences are distinct in each naïve T cell, they serve as molecular barcodes to track T cells with clonal relatedness and shared antigen specificity through proliferation, differentiation, and migration. Single-cell RNA sequencing provides coupled information of TCR sequence and transcriptional state in individual cells, enabling T-cell clonotype-specific analyses. In this protocol, we outline a computational workflow to perform T-cell states and clonal analysis from scRNA-seq data based on the R packages Seurat, ProjecTILs, and scRepertoire. Given a scRNA-seq T-cell dataset with TCR sequence information, cell states are automatically annotated by reference projection using the ProjecTILs method. TCR information is used to track individual clonotypes, assess their clonal expansion, proliferation rates, bias towards specific differentiation states, and the clonal overlap between T-cell subtypes. We provide fully reproducible R code to conduct these analyses and generate useful visualizations that can be adapted for the needs of the protocol user. Key features Computational analysis of paired scRNA-seq and scTCR-seq data Characterizing T-cell functional state by reference-based analysis using ProjecTILs Exploring T-cell clonal structure using scRepertoire Linking T-cell clonality to transcriptomic state to study relationships between clonal expansion and functional phenotype Graphical overview. 

tags:
- Immune Response
- TCR
- Single-Cell
featured: false

links:
- name: Pubmed
  url: https://pubmed.ncbi.nlm.nih.gov/37638293/
url_pdf: https://github.com/ncborcherding/borcherding/blob/master/content/publication/Andreatta2023T/Andreatta2023T.pdf
#url_code: '#'
#url_dataset: '#'
#url_poster: '#'
#url_project: ''
#url_slides: ''
#url_source: '#'
#url_video: '#'
---

