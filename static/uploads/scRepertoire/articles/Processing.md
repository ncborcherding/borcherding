# Additional Processing Steps

## addVariable: Adding Variables for Plotting

What if there are more variables to add than just sample and ID? We can
add them by using the
[`addVariable()`](https://www.borch.dev/uploads/scRepertoire/reference/addVariable.md)
function. For each element, the function will add a column (labeled by
`variable.name`) with the `variable`. The length of the `variables`
parameter needs to match the length of the combined object.

Key Parameter(s) for
[`addVariable()`](https://www.borch.dev/uploads/scRepertoire/reference/addVariable.md)

- `variable.name`: A character string that defines the new variable to
  add (e.g., “Type”, “Treatment”).
- `variables`: A character vector defining the desired column value for
  each list element. Its length must match the number of elements in the
  input.data list.

As an example, here we add the Type in which the samples were processed
and sequenced to the `combined.TCR` object:

``` r
combined.TCR <- addVariable(combined.TCR, 
                            variable.name = "Type", 
                            variables = rep(c("B", "L"), 4))

head(combined.TCR[[1]])
```

    ##                    barcode sample                     TCR1           cdr3_aa1
    ## 1  P17B_AAACCTGAGTACGACG-1   P17B       TRAV25.TRAJ20.TRAC        CGCSNDYKLSF
    ## 3  P17B_AAACCTGCAACACGCC-1   P17B TRAV38-2/DV8.TRAJ52.TRAC CAYRSAQAGGTSYGKLTF
    ## 5  P17B_AAACCTGCAGGCGATA-1   P17B      TRAV12-1.TRAJ9.TRAC     CVVSDNTGGFKTIF
    ## 7  P17B_AAACCTGCATGAGCGA-1   P17B      TRAV12-1.TRAJ9.TRAC     CVVSDNTGGFKTIF
    ## 9  P17B_AAACGGGAGAGCCCAA-1   P17B        TRAV20.TRAJ8.TRAC      CAVRGEGFQKLVF
    ## 10 P17B_AAACGGGAGCGTTTAC-1   P17B      TRAV12-1.TRAJ9.TRAC     CVVSDNTGGFKTIF
    ##                                                  cdr3_nt1
    ## 1                       TGTGGGTGTTCTAACGACTACAAGCTCAGCTTT
    ## 3  TGTGCTTATAGGAGCGCGCAGGCTGGTGGTACTAGCTATGGAAAGCTGACATTT
    ## 5              TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT
    ## 7              TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT
    ## 9                 TGTGCTGTGCGAGGAGAAGGCTTTCAGAAACTTGTATTT
    ## 10             TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT
    ##                           TCR2          cdr3_aa2
    ## 1   TRBV5-1.None.TRBJ2-7.TRBC2    CASSLTDRTYEQYF
    ## 3  TRBV10-3.None.TRBJ2-2.TRBC2     CAISEQGKGELFF
    ## 5     TRBV9.None.TRBJ2-2.TRBC2 CASSVRRERANTGELFF
    ## 7     TRBV9.None.TRBJ2-2.TRBC2 CASSVRRERANTGELFF
    ## 9                         <NA>              <NA>
    ## 10    TRBV9.None.TRBJ2-2.TRBC2 CASSVRRERANTGELFF
    ##                                               cdr3_nt2
    ## 1           TGCGCCAGCAGCTTGACCGACAGGACCTACGAGCAGTACTTC
    ## 3              TGTGCCATCAGTGAACAGGGGAAAGGGGAGCTGTTTTTT
    ## 5  TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ## 7  TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ## 9                                                 <NA>
    ## 10 TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ##                                                  CTgene
    ## 1         TRAV25.TRAJ20.TRAC_TRBV5-1.None.TRBJ2-7.TRBC2
    ## 3  TRAV38-2/DV8.TRAJ52.TRAC_TRBV10-3.None.TRBJ2-2.TRBC2
    ## 5          TRAV12-1.TRAJ9.TRAC_TRBV9.None.TRBJ2-2.TRBC2
    ## 7          TRAV12-1.TRAJ9.TRAC_TRBV9.None.TRBJ2-2.TRBC2
    ## 9                                  TRAV20.TRAJ8.TRAC_NA
    ## 10         TRAV12-1.TRAJ9.TRAC_TRBV9.None.TRBJ2-2.TRBC2
    ##                                                                                              CTnt
    ## 1                    TGTGGGTGTTCTAACGACTACAAGCTCAGCTTT_TGCGCCAGCAGCTTGACCGACAGGACCTACGAGCAGTACTTC
    ## 3  TGTGCTTATAGGAGCGCGCAGGCTGGTGGTACTAGCTATGGAAAGCTGACATTT_TGTGCCATCAGTGAACAGGGGAAAGGGGAGCTGTTTTTT
    ## 5  TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT_TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ## 7  TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT_TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ## 9                                                      TGTGCTGTGCGAGGAGAAGGCTTTCAGAAACTTGTATTT_NA
    ## 10 TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT_TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ##                                CTaa
    ## 1        CGCSNDYKLSF_CASSLTDRTYEQYF
    ## 3  CAYRSAQAGGTSYGKLTF_CAISEQGKGELFF
    ## 5  CVVSDNTGGFKTIF_CASSVRRERANTGELFF
    ## 7  CVVSDNTGGFKTIF_CASSVRRERANTGELFF
    ## 9                  CAVRGEGFQKLVF_NA
    ## 10 CVVSDNTGGFKTIF_CASSVRRERANTGELFF
    ##                                                                                                                                               CTstrict
    ## 1                           TRAV25.TRAJ20.TRAC;TGTGGGTGTTCTAACGACTACAAGCTCAGCTTT_TRBV5-1.None.TRBJ2-7.TRBC2;TGCGCCAGCAGCTTGACCGACAGGACCTACGAGCAGTACTTC
    ## 3  TRAV38-2/DV8.TRAJ52.TRAC;TGTGCTTATAGGAGCGCGCAGGCTGGTGGTACTAGCTATGGAAAGCTGACATTT_TRBV10-3.None.TRBJ2-2.TRBC2;TGTGCCATCAGTGAACAGGGGAAAGGGGAGCTGTTTTTT
    ## 5          TRAV12-1.TRAJ9.TRAC;TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT_TRBV9.None.TRBJ2-2.TRBC2;TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ## 7          TRAV12-1.TRAJ9.TRAC;TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT_TRBV9.None.TRBJ2-2.TRBC2;TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ## 9                                                                                      TRAV20.TRAJ8.TRAC;TGTGCTGTGCGAGGAGAAGGCTTTCAGAAACTTGTATTT_NA;NA
    ## 10         TRAV12-1.TRAJ9.TRAC;TGTGTGGTCTCCGATAATACTGGAGGCTTCAAAACTATCTTT_TRBV9.None.TRBJ2-2.TRBC2;TGTGCCAGCAGCGTAAGGAGGGAAAGGGCGAACACCGGGGAGCTGTTTTTT
    ##    Type
    ## 1     B
    ## 3     B
    ## 5     B
    ## 7     B
    ## 9     B
    ## 10    B

## subsetClones: Filter Out Clonal Information

Likewise, we can remove specific list elements after
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
or
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
using the
[`subsetClones()`](https://www.borch.dev/uploads/scRepertoire/reference/subsetClones.md)
function. In order to subset, we need to identify the column header we
would like to use for subsetting (`name`) and the specific values to
include (`variables`).

Key Parameter(s) for
[`subsetClones()`](https://www.borch.dev/uploads/scRepertoire/reference/subsetClones.md)

- `name`: The column header/name in the metadata of input.data to use
  for subsetting (e.g., “sample”, “Type”).
- `variables`: A character vector of the specific values within the
  chosen name column to retain in the subsetted data.

Below, we isolate just the two sequencing results from “P18L” and “P18B”
samples:

``` r
subset1 <- subsetClones(combined.TCR, 
                        name = "sample", 
                        variables = c("P18L", "P18B"))

head(subset1[[1]][,1:4])
```

    ##                    barcode sample                 TCR1         cdr3_aa1
    ## 1  P18B_AAACCTGAGGCTCAGA-1   P18B TRAV26-1.TRAJ37.TRAC  CIVRGGSSNTGKLIF
    ## 3  P18B_AAACCTGCATGACATC-1   P18B    TRAV3.TRAJ20.TRAC    CAVQRSNDYKLSF
    ## 5  P18B_AAACCTGGTATGCTTG-1   P18B TRAV26-1.TRAJ53.TRAC   CIGSSGGSNYKLTF
    ## 8  P18B_AAACGGGCAGATGGGT-1   P18B                 <NA>             <NA>
    ## 9  P18B_AAACGGGTCTTACCGC-1   P18B    TRAV20.TRAJ9.TRAC CAVQAKRYTGGFKTIF
    ## 12 P18B_AAAGATGAGTTACGGG-1   P18B   TRAV8-3.TRAJ8.TRAC   CAVGGDTGFQKLVF

Alternatively, we can also just select the list elements after
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
or
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).

``` r
subset2 <- combined.TCR[c(3,4)]
head(subset2[[1]][,1:4])
```

    ##                    barcode sample                 TCR1         cdr3_aa1
    ## 1  P18B_AAACCTGAGGCTCAGA-1   P18B TRAV26-1.TRAJ37.TRAC  CIVRGGSSNTGKLIF
    ## 3  P18B_AAACCTGCATGACATC-1   P18B    TRAV3.TRAJ20.TRAC    CAVQRSNDYKLSF
    ## 5  P18B_AAACCTGGTATGCTTG-1   P18B TRAV26-1.TRAJ53.TRAC   CIGSSGGSNYKLTF
    ## 8  P18B_AAACGGGCAGATGGGT-1   P18B                 <NA>             <NA>
    ## 9  P18B_AAACGGGTCTTACCGC-1   P18B    TRAV20.TRAJ9.TRAC CAVQAKRYTGGFKTIF
    ## 12 P18B_AAAGATGAGTTACGGG-1   P18B   TRAV8-3.TRAJ8.TRAC   CAVGGDTGFQKLVF

## exportClones: Save Clonal Data

After assigning the clone by barcode, we can export the clonal
information using
[`exportClones()`](https://www.borch.dev/uploads/scRepertoire/reference/exportClones.md)
to save for later use or to integrate with other bioinformatics
pipelines. This function supports various output formats tailored for
different analytical needs.

Key Parameter(s) for
[`exportClones()`](https://www.borch.dev/uploads/scRepertoire/reference/exportClones.md)
\* `format`: The desired output format for the clonal data. \* `airr`:
Exports data in an Adaptive Immune Receptor Repertoire (AIRR)
Community-compliant format, with each row representing a single receptor
chain. \* `immunarch`: Exports a list containing a data frame and
metadata formatted for use with the `immunarch` package. \* `paired`:
Exports a data frame with paired chain information (amino acid,
nucleotide, genes) per barcode. This is the default. \* `TCRMatch`:
Exports a data frame specifically for the TCRMatch algorithm, containing
TRB chain amino acid sequence and clonal frequency. \* `tcrpheno`:
Exports a data frame compatible with the `tcrpheno` pipeline, with TRA
and TRB chains in separate columns. \* `write.file`: If `TRUE`
(default), saves the output to a CSV file. If `FALSE`, returns the data
frame or list to the R environment. \* `dir`: The directory where the
output file will be saved. Defaults to the current working directory. \*
`file.name`: The name of the CSV file to be saved.

To export the combined clonotypes as a `paired` data frame and save it
to a specified directory:

``` r
exportClones(combined, 
             write.file = TRUE,
             dir = "~/Documents/MyExperiment/Sample1/"
             file.name = "clones.csv")
```

To return an `immunarch`-formatted data frame directly to your R
environment without saving a file:

``` r
immunarch <- exportClones(combined.TCR, 
                          format = "immunarch", 
                          write.file = FALSE)
head(immunarch[[1]][[1]])
```

    ##   Clones   Proportion                                             CDR3.nt
    ## 1      1 0.0003565062    NA;TGCGCCAGCAGTCGGGGACTAGCGGGATACAATGAGCAGTTCTTC
    ## 2      1 0.0003565062       NA;TGTGCCATCAGCGCGGACCCCCGCTACAATGAGCAGTTCTTC
    ## 3      1 0.0003565062 NA;TGTGCCAGCAGCTTGAGGGACAGCTATCGGTACTATGGCTACACCTTC
    ## 4      2 0.0007130125          NA;TGTGCCAGCAGCCGGCAGGGCGCAGATACGCAGTATTTT
    ## 5      1 0.0003565062       NA;TGTGCCAGCAGTCCCTTTACAGGGTTCTATGGCTACACCTTC
    ## 6      1 0.0003565062          NA;TGTGCCAGCTCATCCGGGATCAATCAGCCCCAGCATTTT
    ##               CDR3.aa      V.name  D.name     J.name   C.name
    ## 1  NA;CASSRGLAGYNEQFF NA;TRBV10-2 NA;None NA;TRBJ2-1 NA;TRBC2
    ## 2   NA;CAISADPRYNEQFF NA;TRBV10-3 NA;None NA;TRBJ2-1 NA;TRBC2
    ## 3 NA;CASSLRDSYRYYGYTF NA;TRBV11-3 NA;None NA;TRBJ1-2 NA;TRBC1
    ## 4    NA;CASSRQGADTQYF NA;TRBV11-3 NA;None NA;TRBJ2-3 NA;TRBC2
    ## 5   NA;CASSPFTGFYGYTF NA;TRBV12-4 NA;None NA;TRBJ1-2 NA;TRBC1
    ## 6    NA;CASSSGINQPQHF   NA;TRBV18 NA;None NA;TRBJ1-5 NA;TRBC1
    ##                                           Barcode
    ## 1                         P17B_AGCGGTCCAAAGGAAG-1
    ## 2                         P17B_GGCTCGAGTCGCGGTT-1
    ## 3                         P17B_CGCGTTTTCGGCTACG-1
    ## 4 P17B_CACCAGGGTTCCTCCA-1;P17B_TCTATTGCAGGTGCCT-1
    ## 5                         P17B_GCTGGGTGTACGAAAT-1
    ## 6                         P17B_AGGGTGACATTGGTAC-1

## clonalBin: Bin Clones by Frequency or Proportion

The
[`clonalBin()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBin.md)
function adds a clonal grouping variable (`cloneSize`) to the output of
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md),
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md),
or
[`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
This function calculates the clonal frequency and proportion, then bins
clones into categories based on customizable thresholds. This is useful
for categorizing clones prior to downstream analysis or visualization,
without needing to attach the data to a single-cell object.

Key Parameter(s) for
[`clonalBin()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBin.md)

- `clone.call`: Defines the clonal sequence grouping (`gene`, `nt`,
  `aa`, or `strict`).
- `chain`: The TCR/BCR chain to use (`both`, `TRA`, `TRB`, `TRG`, `TRD`,
  `IGH`, `IGL`).
- `group.by`: A column header in the metadata to group the analysis by
  (e.g., “sample”, “Type”).
- `proportion`: Whether to use proportion (`TRUE`) or total frequency
  (`FALSE`) for binning.
- `clone.size`: The bins for grouping based on proportion or frequency.

### Basic Usage with Proportion

By default,
[`clonalBin()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalBin.md)
uses proportion-based binning with the following default bins:
`c(Rare = 1e-4, Small = 0.001, Medium = 0.01, Large = 0.1, Hyperexpanded = 1)`.

``` r
combined.TCR <- clonalBin(combined.TCR, clone.call = "strict")

# Check the cloneSize column
head(combined.TCR[[1]][, c("barcode", "CTstrict", "clonalProportion", "clonalFrequency", "cloneSize")])
```

    ##                   barcode
    ## 1 P17B_AGCGGTCCAAAGGAAG-1
    ## 2 P17B_GGCTCGAGTCGCGGTT-1
    ## 3 P17B_CGCGTTTTCGGCTACG-1
    ## 4 P17B_CACCAGGGTTCCTCCA-1
    ## 5 P17B_TCTATTGCAGGTGCCT-1
    ## 6 P17B_GCTGGGTGTACGAAAT-1
    ##                                                                             CTstrict
    ## 1    NA;NA_TRBV10-2.None.TRBJ2-1.TRBC2;TGCGCCAGCAGTCGGGGACTAGCGGGATACAATGAGCAGTTCTTC
    ## 2       NA;NA_TRBV10-3.None.TRBJ2-1.TRBC2;TGTGCCATCAGCGCGGACCCCCGCTACAATGAGCAGTTCTTC
    ## 3 NA;NA_TRBV11-3.None.TRBJ1-2.TRBC1;TGTGCCAGCAGCTTGAGGGACAGCTATCGGTACTATGGCTACACCTTC
    ## 4          NA;NA_TRBV11-3.None.TRBJ2-3.TRBC2;TGTGCCAGCAGCCGGCAGGGCGCAGATACGCAGTATTTT
    ## 5          NA;NA_TRBV11-3.None.TRBJ2-3.TRBC2;TGTGCCAGCAGCCGGCAGGGCGCAGATACGCAGTATTTT
    ## 6       NA;NA_TRBV12-4.None.TRBJ1-2.TRBC1;TGTGCCAGCAGTCCCTTTACAGGGTTCTATGGCTACACCTTC
    ##   clonalProportion clonalFrequency                  cloneSize
    ## 1     0.0003565062               1 Small (1e-04 < X <= 0.001)
    ## 2     0.0003565062               1 Small (1e-04 < X <= 0.001)
    ## 3     0.0003565062               1 Small (1e-04 < X <= 0.001)
    ## 4     0.0007130125               2 Small (1e-04 < X <= 0.001)
    ## 5     0.0007130125               2 Small (1e-04 < X <= 0.001)
    ## 6     0.0003565062               1 Small (1e-04 < X <= 0.001)

``` r
# View the distribution of clone sizes
table(combined.TCR[[1]]$cloneSize)
```

    ## 
    ## Hyperexpanded (0.1 < X <= 1)      Large (0.01 < X <= 0.1) 
    ##                          952                          784 
    ##   Medium (0.001 < X <= 0.01)   Small (1e-04 < X <= 0.001) 
    ##                          340                          729 
    ##        Rare (0 < X <= 1e-04)             None ( < X <= 0) 
    ##                            0                            0

### Using Frequency-Based Binning

When using frequency-based binning (`proportion = FALSE`), the
`clone.size` values must be integers. If the maximum frequency exceeds
the upper bin limit, it will be automatically adjusted.

``` r
combined.TCR.freq <- combineTCR(contig_list,
                                samples = c("P17B", "P17L", "P18B", "P18L",
                                            "P19B","P19L", "P20B", "P20L"))

combined.TCR.freq <- clonalBin(combined.TCR.freq,
                               clone.call = "strict",
                               proportion = FALSE,
                               clone.size = c(Rare = 1, Small = 5, Medium = 20,
                                              Large = 100, Hyperexpanded = 500))

# Check the frequency-based binning
head(combined.TCR.freq[[1]][, c("barcode", "clonalFrequency", "cloneSize")])
```

    ##                   barcode clonalFrequency          cloneSize
    ## 1 P17B_AGCGGTCCAAAGGAAG-1               1  Rare (0 < X <= 1)
    ## 2 P17B_GGCTCGAGTCGCGGTT-1               1  Rare (0 < X <= 1)
    ## 3 P17B_CGCGTTTTCGGCTACG-1               1  Rare (0 < X <= 1)
    ## 4 P17B_CACCAGGGTTCCTCCA-1               2 Small (1 < X <= 5)
    ## 5 P17B_TCTATTGCAGGTGCCT-1               2 Small (1 < X <= 5)
    ## 6 P17B_GCTGGGTGTACGAAAT-1               1  Rare (0 < X <= 1)

### Grouping by a Variable

You can calculate clonal frequency and proportion across samples grouped
by a variable (e.g., “Type” or “sample”). This is particularly useful
when you want consistent binning across experimental conditions.

``` r
combined.TCR.grouped <- combineTCR(contig_list,
                                   samples = c("P17B", "P17L", "P18B", "P18L",
                                               "P19B","P19L", "P20B", "P20L"))

combined.TCR.grouped <- addVariable(combined.TCR.grouped,
                                    variable.name = "Type",
                                    variables = rep(c("B", "L"), 4))

combined.TCR.grouped <- clonalBin(combined.TCR.grouped,
                                  clone.call = "strict",
                                  group.by = "Type")

# Check grouped binning
head(combined.TCR.grouped[[1]][, c("barcode", "Type", "clonalProportion", "cloneSize")])
```

    ##                   barcode Type clonalProportion                  cloneSize
    ## 1 P20B_TACTCGCAGAGGTTGC-1    B     4.983554e-05      Rare (0 < X <= 1e-04)
    ## 2 P18L_CGTGTCTGTGTATGGG-1    L     1.404692e-04 Small (1e-04 < X <= 0.001)
    ## 3 P18L_AGTGTCAGTAGCGCAA-1    L     1.404692e-04 Small (1e-04 < X <= 0.001)
    ## 4 P18L_TTTACTGCAAGTTCTG-1    L     1.404692e-04 Small (1e-04 < X <= 0.001)
    ## 5 P19L_GTGTGCGCAAAGGAAG-1    L     1.404692e-04 Small (1e-04 < X <= 0.001)
    ## 6 P20L_CCCTCCTAGTAGCGGT-1    L     1.404692e-04 Small (1e-04 < X <= 0.001)

## annotateInvariant

The
[`annotateInvariant()`](https://www.borch.dev/uploads/scRepertoire/reference/annotateInvariant.md)
function enables the identification of mucosal-associated invariant T
(`MAIT`) cells and invariant natural killer T (`iNKT`) cells in
single-cell sequencing datasets. These specialized T-cell subsets are
defined by their characteristic TCR usage, making them distinguishable
within single-cell immune profiling data. The function extracts TCR
chain information from the provided single-cell dataset and evaluates it
against known invariant TCR criteria for either MAIT or iNKT cells. Each
cell is assigned a score indicating the presence (1) or absence (0) of
the specified invariant T-cell population.

Key Parameter(s) for `annotateInavriant()`

- `type`: Character string specifying the type of invariant T cell to
  annotate (`MAIT` or `iNKT`).
- `species`: Character string specifying the species (`mouse` or
  `human`).

``` r
combined <- annotateInvariant(combined, 
                              type = "MAIT", 
                              species = "human")

combined <- annotateInvariant(combined,
                              type = "iNKT",
                              species = "human")
```

## Next Steps

- [Basic Clonal
  Visualizations](https://www.borch.dev/uploads/scRepertoire/articles/Clonal_Visualizations.md) -
  Visualize clonal abundance, length, and composition across samples.
- [Combining Clones and Single-Cell
  Objects](https://www.borch.dev/uploads/scRepertoire/articles/Attaching_SC.md) -
  Attach clonal data to Seurat or SCE objects with
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
- [Summarizing
  Repertoires](https://www.borch.dev/uploads/scRepertoire/articles/Repertoire_Summary.md) -
  Analyze gene usage, amino acid properties, and k-mer motifs.
