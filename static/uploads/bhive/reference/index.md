# Package index

## Core Functions

The primary interface for running bHIVE algorithms. Use
[`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md) for
single-pass analysis,
[`honeycombHIVE()`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVE.md)
for multilayer hierarchical refinement, and
[`refineB()`](https://www.borch.dev/uploads/bhive/reference/refineB.md)
for gradient-based post-processing.

- [`bHIVE()`](https://www.borch.dev/uploads/bhive/reference/bHIVE.md) :
  bHIVE: B-cell Hybrid Immune Variant Engine
- [`honeycombHIVE()`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVE.md)
  : honeycombHIVE: Multilayer AIS with optional gradient-based
  fine-tuning
- [`refineB()`](https://www.borch.dev/uploads/bhive/reference/refineB.md)
  : refineB: Gradient-based fine-tuning for bHIVE antibodies with
  multiple loss functions and optimizers
- [`visualizeHIVE()`](https://www.borch.dev/uploads/bhive/reference/visualizeHIVE.md)
  : Visualize bHIVE/honeycombHIVE Results

## Hyperparameter Tuning

Grid search over bHIVE hyperparameters with BiocParallel support.

- [`swarmbHIVE()`](https://www.borch.dev/uploads/bhive/reference/swarmbHIVE.md)
  : Tune Hyperparameters for bHIVE (Swarm/Grid Search)

## R6 Algorithm Classes

Object-oriented interface for composing immune algorithms with
injectable modules. `AINet` is the primary class; `ImmuneAlgorithm` is
the abstract base.

- [`AINet`](https://www.borch.dev/uploads/bhive/reference/AINet.md) :
  AINet
- [`ImmuneAlgorithm`](https://www.borch.dev/uploads/bhive/reference/ImmuneAlgorithm.md)
  : ImmuneAlgorithm
- [`ImmuneRepertoire`](https://www.borch.dev/uploads/bhive/reference/ImmuneRepertoire.md)
  : ImmuneRepertoire

## Mutation & Selection Modules

Modules controlling how antibodies mutate, compete, and are selected.
Inject these into `AINet$new()` to customize algorithm behavior.

- [`SHMEngine`](https://www.borch.dev/uploads/bhive/reference/SHMEngine.md)
  : SHMEngine
- [`GerminalCenter`](https://www.borch.dev/uploads/bhive/reference/GerminalCenter.md)
  : GerminalCenter
- [`VDJLibrary`](https://www.borch.dev/uploads/bhive/reference/VDJLibrary.md)
  : VDJLibrary

## Network Regulation Modules

Modules for repertoire regulation and activation control.

- [`IdiotypicNetwork`](https://www.borch.dev/uploads/bhive/reference/IdiotypicNetwork.md)
  : IdiotypicNetwork
- [`ActivationGate`](https://www.borch.dev/uploads/bhive/reference/ActivationGate.md)
  : ActivationGate

## Adaptation & Memory Modules

Modules for environment-driven adaptation, memory, and ensemble methods.

- [`Microenvironment`](https://www.borch.dev/uploads/bhive/reference/Microenvironment.md)
  : Microenvironment
- [`MemoryPool`](https://www.borch.dev/uploads/bhive/reference/MemoryPool.md)
  : MemoryPool
- [`ClassSwitcher`](https://www.borch.dev/uploads/bhive/reference/ClassSwitcher.md)
  : ClassSwitcher
- [`ConvergentSelector`](https://www.borch.dev/uploads/bhive/reference/ConvergentSelector.md)
  : ConvergentSelector

## caret Integration

Model objects for use with the caret package’s `train()` function.

- [`bHIVEmodel`](https://www.borch.dev/uploads/bhive/reference/bHIVEModel.md)
  : B-cell-based Hybrid Immune Virtual Evolution (bHIVE) for caret
- [`honeycombHIVEmodel`](https://www.borch.dev/uploads/bhive/reference/honeycombHIVEmodel.md)
  : Mulilayered honeycombHIVE for caret
