# Visualize Cross-Locus Peptide Binding Results

Creates visualizations of peptide binding predictions across all loci

## Usage

``` r
visualizePeptideBinding(
  binding_results,
  plot_type = c("heatmap", "bar_by_recipient", "bar_by_donor", "scatter"),
  palette = "spectral",
  ...
)
```

## Arguments

- binding_results:

  Results from calculatePeptideBindingLoad with return="detailed"

- plot_type:

  Type of plot: "heatmap", "bar_by_recipient", "bar_by_donor", or
  "scatter"

- palette:

  Character. A color palette name. Defaults to "spectral".

- ...:

  Additional arguments passed to the ggplot theme.

## Value

ggplot object
