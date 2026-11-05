# Gradient Boosting Objective

## Meaning

**Gradient boosting** grows an additive predictor one stage at a time. Each new weak learner approximates the direction in which changing current predictions would reduce the chosen objective.

## Mechanism

Given a differentiable [[loss-function]], compute the negative gradient of loss with respect to each training prediction. Fit a weak learner, often a shallow tree, to those pseudo-residuals and add a scaled version to the ensemble. This is functional [[gradient-descent]]: the update changes the prediction function, not just a fixed vector of coefficients. Squared error yields ordinary residuals, while classification objectives produce different gradients; there is no one loss shared by all boosting tasks.

Learning rate, tree size, round count, and regularization interact. Use a held-out set or cross-validation to choose them, watch for overfitting, and compare against a simple tree or linear baseline. For structured data, claims that boosting always beats neural networks require matched preprocessing, tuning, compute, and test splits—not anecdotal competition results.

## One example

For observations $y_i$, define the current prediction $F(x_i)$ and the half-squared loss $\ell_i=\tfrac12(y_i-F(x_i))^2$. Its derivative with respect to the prediction is $F(x_i)-y_i$, so the negative gradient is the residual $r_i=y_i-F(x_i)$. Fit a tree $h$ to those residual targets and update $F_{new}(x)=F(x)+\eta h(x)$, with positive learning-rate factor $\eta$. Other losses produce different derivative targets, and some tree boosting methods additionally use curvature information.

With invented targets $[3,7,4]$ and initial constant prediction $[4,4,4]$, residuals are $[-1,3,0]$. A simple two-leaf tree might group the first and third observations, predicting their mean residual $-0.5$, while the second leaf predicts $3$. At $\eta=0.2$, new predictions are $[3.9,4.6,3.9]$. The sum of half-squared errors falls from $(1+9+0)/2=5$ to $(0.81+5.76+0.01)/2=3.29$. The tree approximated the residual function; it did not perfectly fit each target.

These are training-set calculations, not evidence of better held-out predictions. Tree structure, shrinkage and stopping alter bias and overfitting. Test objective-specific gradients and compare validation loss and task utility under a fixed tuning budget, especially when the operational decision is not identical to the training objective.


## Check your understanding

Does a residual tree perfectly fit all residuals? Not generally. It approximates the local descent target under its tree constraints; shrinkage scales that update and held-out evaluation still controls acceptance.
