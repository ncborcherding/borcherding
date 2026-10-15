# bHIVE: B-cell Hybrid Immune Variant Engine

bHIVE implements an artificial immune network (AI-Net) for clustering
and classification of high-dimensional data such as mass cytometry and
single-cell profiles. A population of prototypes, called antibodies,
evolves by clonal selection, somatic hypermutation and network
suppression, and the learned prototypes summarize cell populations in
the original marker units. The same fitted model clusters a dataset and
labels new cells. bHIVE accepts SummarizedExperiment and
SingleCellExperiment objects and integrates with bluster through
bHIVEParam. A C++ backend computes affinities, mutations and
suppression, and optional R6 modules add mechanisms such as germinal
center selection, microenvironment-dependent mutation and isotype
switching. The package also provides multilayer clustering, grid search
and caret model wrappers.

## See also

Useful links:

- <https://www.borch.dev/uploads/bhive/>

- Report bugs at <https://github.com/BorchLab/bHIVE/issues>

## Author

**Maintainer**: Nick Borcherding <ncborch@gmail.com>
([ORCID](https://orcid.org/0000-0003-1427-6342))
