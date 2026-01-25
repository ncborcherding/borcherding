# Create an hla_genotype object

Creates a new \`hla_genotype\` object from a data frame of HLA calls.
The object is a list containing the genotype data and a record of the
loci present.

## Usage

``` r
hlaGeno(df)
```

## Arguments

- df:

  A data frame where rows are individuals and columns represent HLA
  alleles (e.g., A_1, A_2, B_1, B_2, ...).

## Value

An object of class \`hla_genotype\`.

## Examples

``` r
# Create a genotype from a data frame
recipient <- data.frame(
  A_1 = "A*01:01", A_2 = "A*02:01",
  B_1 = "B*07:02", B_2 = "B*08:01"
)
geno <- hlaGeno(recipient)
print(geno)
#> HLA Genotype Data
#> -----------------
#> Loci present: A, B 
#> Number of samples: 1 
#> 
#>       A_1     A_2     B_1     B_2
#> 1 A*01:01 A*02:01 B*07:02 B*08:01

# Access components
geno$locus_present
#> [1] "A" "B"
geno$data
#>       A_1     A_2     B_1     B_2
#> 1 A*01:01 A*02:01 B*07:02 B*08:01
```
