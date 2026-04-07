# B-cell-based Hybrid Immune Virtual Evolution (bHIVE) for caret

A wrapper for integrating the B-cell Hybrid Immune Variant Engine
(bHIVE) algorithm with the `caret` package. Supports both classification
and regression tasks, providing compatibility with
[`caret::train()`](https://rdrr.io/pkg/caret/man/train.html) for model
training and validation.

## Usage

``` r
bHIVEmodel
```

## Format

A list containing the components required for integration with the
`caret` package.

## Details

The `bHIVEmodel` wrapper facilitates the use of bHIVE for classification
and regression. It defines the model label, parameter grid, fitting
function, and prediction methods to conform to the `caret` model
specification.

## Components

- `label`:

  Character string. Identifies the model as "B-cell-based Hybrid Immune
  Virtual Evolution".

- `library`:

  Character string. Specifies the R package containing the bHIVE
  implementation. Default is "customPackage".

- `type`:

  Character vector. Specifies the supported tasks: "Classification" and
  "Regression".

- `parameters`:

  A `data.frame` describing the tunable parameters:

  - `parameter`: Name of the parameter.

  - `class`: Data type of the parameter ("numeric").

  - `label`: Short description of the parameter.

- `grid`:

  Function. Generates a grid of tuning parameters for hyperparameter
  optimization.

- `fit`:

  Function. Trains the bHIVE model using specified hyperparameters and
  task type.

- `predict`:

  Function. Generates predictions for new data (classification labels or
  regression values).

- `prob`:

  Function. Calculates class probabilities for classification tasks.

## Parameters

- `nAntibodies`:

  Number of initial antibodies in the bHIVE algorithm.

- `beta`:

  Clone multiplier. Controls the number of clones generated for
  top-matching antibodies.

- `epsilon`:

  Similarity threshold for antibody suppression. Smaller values
  encourage more diversity in the repertoire.

## Functions

- `grid(x, y, len)`: Generates a grid of tuning parameters. Accepts:

  - `x`: Feature matrix or data frame.

  - `y`: Target vector (factor for classification, numeric for
    regression).

  - `len`: Number of grid points for each parameter.

- `fit(x, y, wts, param, lev, last, classProbs, ...)`: Trains the bHIVE
  model. Key arguments:

  - `x`: Feature matrix or data frame.

  - `y`: Target vector.

  - `param`: List of hyperparameters (`nAntibodies`, `beta`, `epsilon`).

  - `...`: Additional arguments passed to the bHIVE function.

- `predict(modelFit, newdata, submodels)`: Generates predictions for new
  data.

  - `modelFit`: Trained bHIVE model.

  - `newdata`: New feature data for prediction.

- `prob(modelFit, newdata, submodels)`: Calculates class probabilities
  (classification only).

## Example Usage

    library(caret)

    # Simulated classification dataset
    set.seed(123)
    X <- matrix(rnorm(100 * 5), ncol = 5)
    y <- factor(sample(c("Class1", "Class2"), 100, replace = TRUE))

    # Train bHIVE model using caret
    trainControl <- trainControl(method = "cv", number = 5, classProbs = TRUE)
    tunedModel <- train(
      x = X,
      y = y,
      method = bHIVEmodel,
      trControl = trainControl,
      tuneLength = 3
    )

    # Predictions
    predictions <- predict(tunedModel, newdata = X)
    probabilities <- predict(tunedModel, newdata = X, type = "prob")

## See also

[`train`](https://rdrr.io/pkg/caret/man/train.html),
[`trainControl`](https://rdrr.io/pkg/caret/man/trainControl.html)

## Examples

``` r
# View model structure
bHIVEmodel$label
#> [1] "Artificial Immune Network (bHIVE)"
bHIVEmodel$parameters
#>     parameter   class                label
#> 1 nAntibodies numeric Number of Antibodies
#> 2        beta numeric     Clone Multiplier
#> 3     epsilon numeric    Epsilon Threshold
```
