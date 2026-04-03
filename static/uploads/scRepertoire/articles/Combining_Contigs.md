# Combining Contigs into Clones

There are varying definitions of clones in the literature. For the
purposes of `scRepertoire`, we define a clone as cells with
shared/trackable complementarity-determining region 3 (CDR3) sequences.
Within this definition, one might use amino acid (`aa`) sequences of one
or both chains to define a clone. Alternatively, we could use nucleotide
(`nt`) or the V(D)JC genes (`genes`) to define a clone. The latter,
genes, would be a more permissive definition of “clones,” as multiple
amino acid or nucleotide sequences can result from the same gene
combination. Another option to define a clone is the use of the V(D)JC
and nucleotide sequence (`strict`). `scRepertoire` allows for the use of
all these definitions of clones and enables users to select both or
individual chains to examine.

The first step in getting clones is to use the single-cell barcodes to
organize cells into paired sequences. This is accomplished using
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
and
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md).

## combineTCR

The
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
function processes a list of TCR sequencing results, consolidating them
to the level of individual cell barcodes. It handles potential issues
with repeated barcodes by adding prefixes from `samples` and `ID`
parameters. The output includes combined reads into clone calls by
nucleotide sequence (`CTnt`), amino acid sequence (`CTaa`), VDJC gene
sequence (`CTgene`), or a combination of nucleotide and gene sequence
(`CTstrict`).

Key Parameter(s) for
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)

- `input.data`: A list of filtered contig annotations (e.g.,
  filtered_contig_annotations.csv from 10x Cell Ranger) or outputs from
  [`loadContigs()`](https://www.borch.dev/uploads/scRepertoire/reference/loadContigs.md).
- `samples`: Labels for your samples (recommended).
- `ID`: Additional sample labels (optional).
- `removeNA`: If `TRUE`, removes any cell barcode with an NA value in at
  least one chain (default is `FALSE`).
- `removeMulti`: If `TRUE`, removes any cell barcode with more than two
  immune receptor chains (default is `FALSE`).
- `filterMulti`: If `TRUE`, isolates the top two expressed chains in
  cell barcodes with multiple chains (default is `FALSE`).
- `filterNonproductive`: If `TRUE`, removes non-productive chains if the
  variable exists in the contig data (default is `TRUE`).

To combine TCR contigs from `contig_list` and apply sample prefixes:

``` r
combined.TCR <- combineTCR(contig_list, 
                           samples = c("P17B", "P17L", "P18B", "P18L", 
                                            "P19B","P19L", "P20B", "P20L"),
                           removeNA = FALSE, 
                           removeMulti = FALSE, 
                           filterMulti = FALSE)

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

[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
is the essential first step for organizing raw TCR sequencing data into
a structured format for `scRepertoire` analyses. It allows for flexible
handling of single and paired chains, barcode disambiguation, and
initial filtering, producing a list of data frames where each row
represents a single cell and its associated TCR clonotypes.

## combineBCR

The
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
function is the primary tool for processing raw B cell receptor contig
data into a format ready for analysis. It is analogous to
[`combineTCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineTCR.md)
but includes specialized logic for handling the complexities of BCRs,
such as somatic hypermutation. The function consolidates contigs into a
single data frame per sample, with each row representing a unique cell.

By default `(call.related.clones = TRUE)`,
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
groups B cells into clones based on the similarity of their CDR3
sequences.

### How `combineBCR()` Groups Related Clones

- Internally calling
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  to build a network of related sequences.
- Using the `threshold` parameter to define connections. The `threshold`
  is a normalized Levenshtein distance, where a value closer to 1.0
  requires higher sequence similarity. The default of 0.85 is a good
  starting point.
- Assigning a cluster-based ID to the CTstrict column.

Additionally, the `group.by` argument allows you to constrain the
clustering analysis to only occur within distinct categories in your
metadata. For example, using `group.by = "sample"` ensures that
sequences from different samples are never compared or clustered
together, even if they are identical.

Key Parameter(s) for
[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)

- `call.related.clones`: If `TRUE` (default), uses
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  to identify related clones based on sequence similarity.
- `group.by`: The column header used to group clones for clustering (if
  `NULL`, clusters will be calculated across all samples).
- `threshold`: The similarity threshold for
  [`clonalCluster()`](https://www.borch.dev/uploads/scRepertoire/reference/clonalCluster.md)
  (default: 0.85).
- `dist_type`: The metric for calculating difference: “levenshtein”
  (default), “hamming”, “nw” (Needleman-Wunsch), or “sw”
  (Smith-Waterman).
- `dist_mat:` The substitution matrix used if dist_type is “nw” or “sw”
  (e.g., “BLOSUM62”, “PAM30”)
- `normalize`: How to handle the threshold: “none”, “length”, or
  “maxlen”.
- `chain`: The chain to use for clustering when call.related.clones =
  TRUE (default: `both`).
- `sequence`: The sequence type (`nt` or `aa`) for clustering (default:
  `nt`).
- use.V, use.J: If `TRUE`, sequences must share the same V/J gene to be
  clustered (default: `TRUE`)
- `cluster.method`: The clustering algorithm to apply to the
  edit-distanc network (default: `components`).

First, load the example BCR contig data:

``` r
# Load example BCR contig data
BCR.contigs <- read.csv("https://www.borch.dev/uploads/contigs/b_contigs.csv")
```

Then, combine BCR contigs using the default similarity clustering:

``` r
# Combine using the default similarity clustering
combined.BCR.clustered <- combineBCR(BCR.contigs, 
                                     samples = "Patient1", 
                                     threshold = 0.85)

# The CTstrict column contains cluster IDs (e.g., "cluster.1")
head(combined.BCR.clustered[[1]][, c("barcode", "CTstrict", "IGH", "cdr3_aa1")])
```

    ##                       barcode
    ## 1 Patient1_AAACCTGAGGGCACTA-1
    ## 2 Patient1_AAACCTGAGTACGTTC-1
    ## 3 Patient1_AAACCTGAGTCCGGTC-1
    ## 4 Patient1_AAACCTGCACCAGGTC-1
    ## 5 Patient1_AAACCTGGTAAATGAC-1
    ## 6 Patient1_AAACGGGTCACCTCGT-1
    ##                                                                                                                         CTstrict
    ## 1                                                                            NA_IGLV1-51.TGCGGAACATGGGATAGCAGCCTGAGTGCTGGCGTGTTC
    ## 2                           IGHV3-64.TGTGCGAAATCGTATAGCAGAGACCTGCCGCGGTACTTTGGCTCCTGG_IGKV3-15.TGTCAGCAGTATAGTAACTGGCCGCTCACTTTC
    ## 3                                                                                     NA_IGKV3-20.TGTCAACAGTATGGTGACTCTCTCCCTTTC
    ## 4 IGHV1-69-2.TGTGTGAGAGATGGGGCGGGTCACTATGGTTCGGGGATAGGCTACTACGGTATGGACGTCTGG_IGLV2-14.TGCAGTTCATATATAAGTACCAGCACTCTCGAGGTCCTATTC
    ## 5                  IGHV1-46.TGTTCGAGGGGTCGTCTCCCGATGCCAGCAGCTGGCAGTGGTTTGGTCTCCTGG_IGKV3-15.TGTCAGCACTATCATAACTGGCCTCCGTACACTTTT
    ## 6                                                                                  NA_IGKV3-11.TGTCAGCAGCGTAGCAACTGGCCTCTGACGTTC
    ##                              IGH              cdr3_aa1
    ## 1                           <NA>                  <NA>
    ## 2   IGHV3-64.IGHD6-6.IGHJ4.IGHG1      CAKSYSRDLPRYFGSW
    ## 3                           <NA>                  <NA>
    ## 4 IGHV1-69-2.IGHD3-10.IGHJ6.IGHM CVRDGAGHYGSGIGYYGMDVW
    ## 5  IGHV1-46.IGHD6-13.IGHJ5.IGHA2    CSRGRLPMPAAGSGLVSW
    ## 6                           <NA>                  <NA>

### Advanced: Grouping by Alignment

For more biological accuracy—specifically when analyzing amino acid
sequences—you can use alignment metrics. This allows the clustering to
penalize conservative amino acid changes less than radical changes.

Here we use Needleman-Wunsch alignment with the BLOSUM80 substitution
matrix:

``` r
combined.BCR.aligned <- combineBCR(BCR.contigs, 
                                   samples = "Patient1",
                                   sequence = "aa",        
                                   dist_type = "nw",      
                                   dist_mat = "BLOSUM80",  
                                   threshold = 0.85)

head(combined.BCR.aligned[[1]][, c("barcode", "CTstrict", "IGH", "cdr3_aa1")])
```

    ##                       barcode
    ## 1 Patient1_AAACCTGAGGGCACTA-1
    ## 2 Patient1_AAACCTGAGTACGTTC-1
    ## 3 Patient1_AAACCTGAGTCCGGTC-1
    ## 4 Patient1_AAACCTGCACCAGGTC-1
    ## 5 Patient1_AAACCTGGTAAATGAC-1
    ## 6 Patient1_AAACGGGTCACCTCGT-1
    ##                                                   CTstrict
    ## 1                                NA_IGLV1-51.CGTWDSSLSAGVF
    ## 2           IGHV3-64.CAKSYSRDLPRYFGSW_IGKV3-15.CQQYSNWPLTF
    ## 3                                   NA_IGKV3-20.CQQYGDSLPF
    ## 4 IGHV1-69-2.CVRDGAGHYGSGIGYYGMDVW_IGLV2-14.CSSYISTSTLEVLF
    ## 5        IGHV1-46.CSRGRLPMPAAGSGLVSW_IGKV3-15.CQHYHNWPPYTF
    ## 6                                  NA_IGKV3-11.CQQRSNWPLTF
    ##                              IGH              cdr3_aa1
    ## 1                           <NA>                  <NA>
    ## 2   IGHV3-64.IGHD6-6.IGHJ4.IGHG1      CAKSYSRDLPRYFGSW
    ## 3                           <NA>                  <NA>
    ## 4 IGHV1-69-2.IGHD3-10.IGHJ6.IGHM CVRDGAGHYGSGIGYYGMDVW
    ## 5  IGHV1-46.IGHD6-13.IGHJ5.IGHA2    CSRGRLPMPAAGSGLVSW
    ## 6                           <NA>                  <NA>

### Filtering and Cleaning Data

[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
includes several arguments to filter and clean the contig data during
processing. \* `filterNonproductive = TRUE` (Default): Removes any
contigs that are not classified as productive, ensuring that only
functional receptor chains are included in the analysis. \*
`filterMulti = TRUE` (Default): For cells with more than one heavy or
light chain detected, this automatically selects the chain with the
highest UMI count (read abundance) and discards the others. This helps
resolve cellular multiplets or technical artifacts.

Here is an example applying these filters (though they are on by
default):

``` r
cleaned.BCR <- combineBCR(BCR.contigs,
                          samples = "Patient1",
                          filterNonproductive = TRUE,
                          filterMulti = TRUE)

head(cleaned.BCR[[1]])
```

    ##                       barcode   sample                            IGH
    ## 1 Patient1_AAACCTGAGGGCACTA-1 Patient1                           <NA>
    ## 2 Patient1_AAACCTGAGTACGTTC-1 Patient1   IGHV3-64.IGHD6-6.IGHJ4.IGHG1
    ## 3 Patient1_AAACCTGAGTCCGGTC-1 Patient1                           <NA>
    ## 4 Patient1_AAACCTGCACCAGGTC-1 Patient1 IGHV1-69-2.IGHD3-10.IGHJ6.IGHM
    ## 5 Patient1_AAACCTGGTAAATGAC-1 Patient1  IGHV1-46.IGHD6-13.IGHJ5.IGHA2
    ## 6 Patient1_AAACGGGTCACCTCGT-1 Patient1                           <NA>
    ##                cdr3_aa1
    ## 1                  <NA>
    ## 2      CAKSYSRDLPRYFGSW
    ## 3                  <NA>
    ## 4 CVRDGAGHYGSGIGYYGMDVW
    ## 5    CSRGRLPMPAAGSGLVSW
    ## 6                  <NA>
    ##                                                          cdr3_nt1
    ## 1                                                            <NA>
    ## 2                TGTGCGAAATCGTATAGCAGAGACCTGCCGCGGTACTTTGGCTCCTGG
    ## 3                                                            <NA>
    ## 4 TGTGTGAGAGATGGGGCGGGTCACTATGGTTCGGGGATAGGCTACTACGGTATGGACGTCTGG
    ## 5          TGTTCGAGGGGTCGTCTCCCGATGCCAGCAGCTGGCAGTGGTTTGGTCTCCTGG
    ## 6                                                            <NA>
    ##                   IGLC       cdr3_aa2
    ## 1 IGLV1-51.IGLJ3.IGLC2  CGTWDSSLSAGVF
    ## 2  IGKV3-15.IGKJ4.IGKC    CQQYSNWPLTF
    ## 3  IGKV3-20.IGKJ4.IGKC     CQQYGDSLPF
    ## 4 IGLV2-14.IGLJ2.IGLC2 CSSYISTSTLEVLF
    ## 5  IGKV3-15.IGKJ2.IGKC   CQHYHNWPPYTF
    ## 6  IGKV3-11.IGKJ1.IGKC    CQQRSNWPLTF
    ##                                     cdr3_nt2
    ## 1    TGCGGAACATGGGATAGCAGCCTGAGTGCTGGCGTGTTC
    ## 2          TGTCAGCAGTATAGTAACTGGCCGCTCACTTTC
    ## 3             TGTCAACAGTATGGTGACTCTCTCCCTTTC
    ## 4 TGCAGTTCATATATAAGTACCAGCACTCTCGAGGTCCTATTC
    ## 5       TGTCAGCACTATCATAACTGGCCTCCGTACACTTTT
    ## 6          TGTCAGCAGCGTAGCAACTGGCCTCTGACGTTC
    ##                                                CTgene
    ## 1                             NA_IGLV1-51.IGLJ3.IGLC2
    ## 2    IGHV3-64.IGHD6-6.IGHJ4.IGHG1_IGKV3-15.IGKJ4.IGKC
    ## 3                              NA_IGKV3-20.IGKJ4.IGKC
    ## 4 IGHV1-69-2.IGHD3-10.IGHJ6.IGHM_IGLV2-14.IGLJ2.IGLC2
    ## 5   IGHV1-46.IGHD6-13.IGHJ5.IGHA2_IGKV3-15.IGKJ2.IGKC
    ## 6                              NA_IGKV3-11.IGKJ1.IGKC
    ##                                                                                                         CTnt
    ## 1                                                                 NA_TGCGGAACATGGGATAGCAGCCTGAGTGCTGGCGTGTTC
    ## 2                         TGTGCGAAATCGTATAGCAGAGACCTGCCGCGGTACTTTGGCTCCTGG_TGTCAGCAGTATAGTAACTGGCCGCTCACTTTC
    ## 3                                                                          NA_TGTCAACAGTATGGTGACTCTCTCCCTTTC
    ## 4 TGTGTGAGAGATGGGGCGGGTCACTATGGTTCGGGGATAGGCTACTACGGTATGGACGTCTGG_TGCAGTTCATATATAAGTACCAGCACTCTCGAGGTCCTATTC
    ## 5                TGTTCGAGGGGTCGTCTCCCGATGCCAGCAGCTGGCAGTGGTTTGGTCTCCTGG_TGTCAGCACTATCATAACTGGCCTCCGTACACTTTT
    ## 6                                                                       NA_TGTCAGCAGCGTAGCAACTGGCCTCTGACGTTC
    ##                                   CTaa
    ## 1                     NA_CGTWDSSLSAGVF
    ## 2         CAKSYSRDLPRYFGSW_CQQYSNWPLTF
    ## 3                        NA_CQQYGDSLPF
    ## 4 CVRDGAGHYGSGIGYYGMDVW_CSSYISTSTLEVLF
    ## 5      CSRGRLPMPAAGSGLVSW_CQHYHNWPPYTF
    ## 6                       NA_CQQRSNWPLTF
    ##                                                                                                                         CTstrict
    ## 1                                                                            NA_IGLV1-51.TGCGGAACATGGGATAGCAGCCTGAGTGCTGGCGTGTTC
    ## 2                           IGHV3-64.TGTGCGAAATCGTATAGCAGAGACCTGCCGCGGTACTTTGGCTCCTGG_IGKV3-15.TGTCAGCAGTATAGTAACTGGCCGCTCACTTTC
    ## 3                                                                                     NA_IGKV3-20.TGTCAACAGTATGGTGACTCTCTCCCTTTC
    ## 4 IGHV1-69-2.TGTGTGAGAGATGGGGCGGGTCACTATGGTTCGGGGATAGGCTACTACGGTATGGACGTCTGG_IGLV2-14.TGCAGTTCATATATAAGTACCAGCACTCTCGAGGTCCTATTC
    ## 5                  IGHV1-46.TGTTCGAGGGGTCGTCTCCCGATGCCAGCAGCTGGCAGTGGTTTGGTCTCCTGG_IGKV3-15.TGTCAGCACTATCATAACTGGCCTCCGTACACTTTT
    ## 6                                                                                  NA_IGKV3-11.TGTCAGCAGCGTAGCAACTGGCCTCTGACGTTC

[`combineBCR()`](https://www.borch.dev/uploads/scRepertoire/reference/combineBCR.md)
is designed for processing B cell repertoire data, going beyond simple
contig aggregation to incorporate advanced clustering based on CDR3
sequence similarity. This enables the identification of clonally related
B cells, crucial for studying B cell development, affinity maturation,
and humoral immune responses. Its filtering options further ensure the
quality and interpretability of the processed data.

## Next Steps

- [Additional Processing
  Steps](https://www.borch.dev/uploads/scRepertoire/articles/Processing.md) -
  Add metadata, subset clones, bin by frequency, and export data.
- [Basic Clonal
  Visualizations](https://www.borch.dev/uploads/scRepertoire/articles/Clonal_Visualizations.md) -
  Visualize clonal abundance, length, and composition across samples.
- [Combining Clones and Single-Cell
  Objects](https://www.borch.dev/uploads/scRepertoire/articles/Attaching_SC.md) -
  Attach clonal data to Seurat or SCE objects with
  [`combineExpression()`](https://www.borch.dev/uploads/scRepertoire/reference/combineExpression.md).
