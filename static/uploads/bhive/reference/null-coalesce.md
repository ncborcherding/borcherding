# Null-coalesce operator

Returns `x` if it is not `NULL`, otherwise returns `y`. Used internally
by bHIVE R6 classes for parameter defaults.

## Usage

``` r
x %||% y
```

## Arguments

- x:

  Value to test.

- y:

  Default value if `x` is NULL.

## Value

`x` if not NULL, otherwise `y`.
