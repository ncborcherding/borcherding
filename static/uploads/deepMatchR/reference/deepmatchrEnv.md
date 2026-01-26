# Return a Basilisk environment tailored to the current platform

Returns the appropriate Basilisk environment for MHCnuggets based on the
current operating system. This environment is used internally by
[`predictMHCnuggets`](https://www.borch.dev/uploads/deepMatchR/reference/predictMHCnuggets.md)
for Python integration.

## Usage

``` r
deepmatchrEnv(platform = c("auto", "linux", "macos"))
```

## Arguments

- platform:

  Character. One of "auto" (default), "linux", or "macos". When "auto",
  the platform is detected automatically.

## Value

A `BasiliskEnvironment` object configured for the current platform.

## See also

[`predictMHCnuggets`](https://www.borch.dev/uploads/deepMatchR/reference/predictMHCnuggets.md)

## Examples

``` r
# Get the environment for the current platform
env <- deepmatchrEnv()
print(class(env))
#> [1] "BasiliskEnvironment"
#> attr(,"package")
#> [1] "basilisk"

# Explicitly request Linux environment
env_linux <- deepmatchrEnv(platform = "linux")
```
