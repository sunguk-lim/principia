# Cross Validation

## Meaning

**Cross-validation** repeats a train/validation split so a model is judged on examples not used for that fit. In $K$-fold cross-validation, each fold serves as validation once, and the resulting scores show variation across partitions. This is a performance-estimation and model-selection procedure, not a guarantee of deployment behavior.

## Mechanism

Divide the available training data into $K$ folds. For each iteration, fit preprocessing and the model on $K-1$ folds and evaluate on the held-out fold. Aggregate the measured scores and their variation. Every learned transformation, including imputation, feature selection, and scaling, must be fitted inside the training portion of each iteration; fitting once on all data leaks validation information. An untouched final test set is still useful after model selection.

The split must reflect the actual prediction task. Random folds can leak a patient's repeated records across train and validation; group folds keep the same entity together. For future forecasting, time-ordered validation avoids training on later observations. Class imbalance may call for stratified folds. Nested cross-validation separates hyperparameter selection from performance estimation when the selection procedure itself is being evaluated.

## One example

Fit preprocessing and a classifier separately inside each training fold, then score the untouched validation fold. Keep a final holdout for the chosen procedure.

## Check your understanding

**Question:** Why must preprocessing be refit inside each fold?

**Answer:** Fitting it on all rows leaks validation information into training.
