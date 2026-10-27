# Constrained Counterfactual Recourse

## Meaning

Constrained counterfactual recourse asks what permitted action could change an unfavorable model decision. It is different from attributing an existing prediction: attribution allocates the current score, whereas recourse searches for an attainable alternative input. A short mathematical distance is not sufficient if the proposed change is impossible, prohibited or outside the person's control.

## Mechanism

Let x be the current feature vector, f the deployed decision model, A(x) the [[set]] of allowed actions and c(a) the cost of action a. Search for an action a in A(x) with favorable decision f(x+a), minimizing c(a). The model may be a [[neural-network]] or a simpler score; the allowable actions are a separate policy and domain contract.

Keep immutable attributes fixed. Bound actionable changes and model dependencies: changing employment can affect income, timing and documentation together rather than independently editing a spreadsheet cell. Reject infeasible combinations before ranking cost. Some inputs have no feasible recourse under the chosen model and action set; report that outcome rather than invent a guaranteed path. A counterfactual model input is not automatically a causal intervention in the real world.

## Worked example

Use dimensionless illustrative features. A score is 2u - v and approval requires at least 3. Current u=1 and v=2 give 0. Permit u to increase by at most 1 and v to decrease by at most 2. Each unit change costs one. Increasing u by 1 gives score 2 and still fails; decreasing v by 2 also gives 2. Increasing u by 1 and decreasing v by 1 gives 2*2-1=3 at cost 2. If allowed steps are whole units, no action of cost 1 can succeed, so this feasible cost-2 action is minimal under these stated assumptions. [[arithmetic]] verifies the decision; it does not verify the action's real-world attainability.

## Check your understanding

Is changing age to cross a boundary useful recourse? Not under an action set that treats age as immutable. A favorable synthetic input can be a valid model counterfactual and still be invalid recourse.
