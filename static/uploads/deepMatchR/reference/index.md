# Package index

## HLA Genotypes

Create and work with HLA genotype objects

- [`hlaGeno()`](https://www.borch.dev/uploads/deepMatchR/reference/hlaGeno.md)
  : Create an hla_genotype object
- [`validateHlaGeno()`](https://www.borch.dev/uploads/deepMatchR/reference/validateHlaGeno.md)
  : Validate an hla_genotype object
- [`print(`*`<hla_genotype>`*`)`](https://www.borch.dev/uploads/deepMatchR/reference/print.hla_genotype.md)
  : Print an hla_genotype object

## Sequence Analysis

Functions for retrieving and comparing HLA sequences

- [`getAlleleSequence()`](https://www.borch.dev/uploads/deepMatchR/reference/getAlleleSequence.md)
  : Get Sequence for an HLA Allele
- [`quantifyMismatch()`](https://www.borch.dev/uploads/deepMatchR/reference/quantifyMismatch.md)
  : Quantify Amino Acid Mismatches With Charge/Polarity Awareness (base
  R)
- [`calculateMismatchLoad()`](https://www.borch.dev/uploads/deepMatchR/reference/calculateMismatchLoad.md)
  : Calculate Mismatch Load Between Donor and Recipient Genotypes
- [`getSequenceStats()`](https://www.borch.dev/uploads/deepMatchR/reference/getSequenceStats.md)
  : Get Sequence Statistics
- [`clearSequenceCache()`](https://www.borch.dev/uploads/deepMatchR/reference/clearSequenceCache.md)
  : Clear Sequence Cache

## Eplet Analysis

Functions for eplet-based immunogenicity analysis

- [`quantifyEpletMismatch()`](https://www.borch.dev/uploads/deepMatchR/reference/quantifyEpletMismatch.md)
  : Quantify Eplet Mismatches Between Two Alleles
- [`calculateEpletLoad()`](https://www.borch.dev/uploads/deepMatchR/reference/calculateEpletLoad.md)
  : Calculate Eplet Load Between Donor and Recipient Genotypes

## Peptide Binding Prediction

Deep learning models for peptide-MHC binding prediction

- [`predictMHCnuggets()`](https://www.borch.dev/uploads/deepMatchR/reference/predictMHCnuggets.md)
  : Predict peptide–MHC binding with mhcnuggets
- [`calculatePeptideBindingLoad()`](https://www.borch.dev/uploads/deepMatchR/reference/calculatePeptideBindingLoad.md)
  : Calculate Peptide Binding Load for Transplant Risk Assessment
- [`visualizePeptideBinding()`](https://www.borch.dev/uploads/deepMatchR/reference/visualizePeptideBinding.md)
  : Visualize Cross-Locus Peptide Binding Results

## Serology Conversion

Convert between molecular and serological HLA nomenclature

- [`toSerology()`](https://www.borch.dev/uploads/deepMatchR/reference/toSerology.md)
  : Convert HLA Alleles to Serological Equivalents
- [`updateWmdaData()`](https://www.borch.dev/uploads/deepMatchR/reference/updateWmdaData.md)
  : Update WMDA Nomenclature Data
- [`clearWmdaCache()`](https://www.borch.dev/uploads/deepMatchR/reference/clearWmdaCache.md)
  : Clear WMDA Cache

## Antibody Visualization

Visualize SAB and PRA assay results

- [`plotAntibodies()`](https://www.borch.dev/uploads/deepMatchR/reference/plotAntibodies.md)
  [`plotSAB()`](https://www.borch.dev/uploads/deepMatchR/reference/plotAntibodies.md)
  [`plotPRA()`](https://www.borch.dev/uploads/deepMatchR/reference/plotAntibodies.md)
  : Plot Antibody Data with Optional Antigen-Level Table or Time-Series
  Trend
- [`plotEplets()`](https://www.borch.dev/uploads/deepMatchR/reference/plotEplets.md)
  : Plot Eplet Results from SPI Assay
- [`calculateAUC()`](https://www.borch.dev/uploads/deepMatchR/reference/calculateAUC.md)
  [`epletAUC()`](https://www.borch.dev/uploads/deepMatchR/reference/calculateAUC.md)
  [`cregAUC()`](https://www.borch.dev/uploads/deepMatchR/reference/calculateAUC.md)
  [`serologyAUC()`](https://www.borch.dev/uploads/deepMatchR/reference/calculateAUC.md)
  : Calculate Antigen AUC Based on MFI

## Data

Built-in datasets

- [`deepMatchR_example`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_example.md)
  : Example SAB (Class I/II) and PRA Panels
- [`deepMatchR_cregs`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_cregs.md)
  : CREG–Allele Mapping Data
- [`deepMatchR_eplets`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_eplets.md)
  : HLA Eplet Assignments (Registry-derived)
- [`deepMatchR_wmda_pgroups`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_wmda_pgroups.md)
  : WMDA P-Group Definitions
- [`deepMatchR_wmda_serology`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_wmda_serology.md)
  : WMDA DNA-to-Serology Mapping
- [`deepMatchR_wmda_splits`](https://www.borch.dev/uploads/deepMatchR/reference/deepMatchR_wmda_splits.md)
  : WMDA Broad-to-Split Antigen Relationships

## Utilities

Helper functions and internal utilities

- [`deepmatchrEnv()`](https://www.borch.dev/uploads/deepMatchR/reference/deepmatchrEnv.md)
  : Return a Basilisk environment tailored to the current platform
- [`batchGetSequences()`](https://www.borch.dev/uploads/deepMatchR/reference/batchGetSequences.md)
  : Batch Get Sequences with Parallel Processing
