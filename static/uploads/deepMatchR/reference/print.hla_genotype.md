# Print an hla_genotype object

Print an hla_genotype object

## Usage

``` r
# S3 method for class 'hla_genotype'
print(x, ...)
```

## Arguments

- x:

  An object of class \`hla_genotype\`.

- ...:

  Additional arguments (not used).

## Value

Invisibly returns the original object.

## Examples

``` r
df <- data.frame(A_1 = "A*01:01", B_1 = "B*07:02")
geno <- hlaGeno(df)
print(geno)
#> HLA Genotype Data
#> -----------------
#> Loci present: A, B 
#> Number of samples: 1 
#> 
#>       A_1     B_1
#> 1 A*01:01 B*07:02
```
