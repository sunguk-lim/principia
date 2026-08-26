# Figure spec — `kubernetes-service`

> Derived from `nodes/kubernetes-service.md`; governed by `protocols/EXPLAIN.md` and
> `protocols/VISUAL_PROTOCOLS.md`.

## Visual teaching contract

- **Audience:** A software engineer who understands ordinary network addresses but is new to Kubernetes.
- **Single job:** Make the reader see that a Service keeps one client-facing identity while its Pod
  membership changes.
- **Visual thesis:** Because Pod addresses change during a rollout, a Kubernetes Service keeps the
  client-facing name and address fixed while updating the eligible backend set, so clients never track
  Pod IPs.
- **Traced object:** One amber client request, shown following the drawn route to an eligible Pod in
  each state.
- **Subject visual vocabulary:** client, DNS name, virtual Service address, Pod endpoints, backend
  membership, routed request, rollout.
- **Signature moment:** The vertically aligned blue Service cards remain identical while Pod A is
  replaced by Pod C around them.
- **Anti-template test:** Without the stable Service identity and concrete Pod-address replacement,
  the composition cannot be relabeled as an unrelated queue or generic workflow.

| channel | semantic job |
|---|---|
| Form | rounded cards are network entities; the containing region is current backend membership |
| Space | top-to-bottom is both the real request route within a state and time across the rollout |
| Scale | the Service and backend pool dominate; support labels remain subordinate |
| Colour | gray = client, blue = Service identity, teal = Pod, amber = selected request/endpoint |
| Rhythm | repeated aligned rows expose what stays fixed and what changes |

| disclosure | figure treatment |
|---|---|
| Intuition | Same Service, different Pods |
| Mechanism | DNS resolves the stable address; the selected request is steered to one current endpoint |
| Precision | Concrete Service and Pod IP:port values from the node's worked instance |

**Comprehension test — intended answers:**

1. **Problem:** Pod A can disappear and its replacement has a new address.
2. **Change:** Backend membership changes from A+B to B+C.
3. **Cause:** Kubernetes updates the Service's current endpoint set and traffic route.
4. **Usefulness:** The client continues using `checkout` / `10.96.0.20:80`.

**First-view constraints:** The mobile-first 560×1040 canvas uses no label below 16 px. Each state has
the same vertical route and retains about 70% of its authored font size on a 390 px phone viewport.
Service types, proxy implementations, and headless behavior stay in prose.

**Plan critique:** A hub-and-spoke cluster map was rejected because it displays connectivity but hides
the time invariant. An animated packet loop was rejected because motion is not required to compare the
two exact states; aligned rows show the transformation more reliably on GitHub and mobile.

**Reduced-motion result:** The figure is static, so its fallback is the complete explanation.

## Figure trigger and spine

Drawing is warranted.

- **SHAPE/structure:** one stable front endpoint sits between a client and a contained backend set.
- **FLOW/routing:** one request follows a visible client → Service → selected-Pod route.
- **CHANGE over steps:** the aligned before/after rows show Pod A leaving and Pod C joining while the
  Service identity stays fixed.

Genre: **timeline-as-grid with a flow overlay**. The invariant is already fully visible in a static
storyboard, so animation would add movement but no additional causal information.

## Entity inventory and ordered states

| entity | drawn as | role |
|---|---|---|
| Client | gray rounded card repeated at the same x-coordinate | source of the traced request |
| Service | blue rounded card, same name/address/horizontal position in both states | persistent structure and stable identity |
| Backend set | pale teal containing region | current EndpointSlice membership |
| Pods A, B, C | labeled teal endpoint cards | eligible backends; B persists, A→C changes |
| Request | amber solid arrow and selected-endpoint ring | traced object and single accent |

1. **Before rollout:** membership is Pod A `10.42.1.8:8080` and Pod B `10.42.1.9:8080`; the request
   is steered to B.
2. **After rollout:** membership is Pod B `10.42.1.9:8080` and Pod C `10.42.2.14:8080`; the same
   Service identity steers the next request to C.

## Rendered critique

The first 960×620 render made the endpoint name and IP compete horizontally and would shrink too far
on a phone. The layout was changed from three columns to a 560×1040 vertical request route; Pod names
and addresses now occupy separate lines. Every route terminates on the next entity boundary, and the
two Service cards remain aligned and identical. **Subtraction pass:** the bottom payoff banner was
removed because it repeated the already-visible stable-Service/different-Pods comparison.
