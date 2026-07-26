---
id: maximum-a-posteriori
title: Maximum A Posteriori
summary: "Maximum a posteriori (MAP) estimation is maximum-likelihood-estimation with one addition: a prior belief about the parameter, folded in before you look at the data."
type: concept
tags: [math/probability]
prereqs: [maximum-likelihood-estimation, bayes-rule, probability-distribution, likelihood]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Maximum A Posteriori

## Summary

**Maximum a posteriori (MAP) estimation** is [[maximum-likelihood-estimation]] with one addition: a *prior belief* about the parameter, folded in before you look at the data. Recall that [[maximum-likelihood-estimation]] reports the parameter $\theta$ that makes the observed data $D$ most probable, $\hat\theta_{\text{MLE}} = \arg\max_\theta P(D \mid \theta)$ — and that on thin data it over-commits, declaring a coin two-headed after a single head. MAP fixes the over-commitment by asking a different question: not "which $\theta$ best explains the data?" but "which $\theta$ is most probable *given* the data?" That probability is the **posterior**, and by [[bayes-rule]] the posterior is proportional to likelihood times prior, $P(\theta \mid D) \propto P(D \mid \theta)\,P(\theta)$. MAP returns the *mode* — the single highest peak — of that posterior: $\hat\theta_{\text{MAP}} = \arg\max_\theta P(D \mid \theta)\,P(\theta)$. The mechanics are identical to MLE: take the log so the product becomes a sum, differentiate, set to zero — the *only* change is an extra $+\ln P(\theta)$ term, a **prior penalty** added to the MLE objective. The payoff is regularization: when data is scarce the prior steadies the estimate, and as data accumulates the likelihood overwhelms the prior and MAP smoothly converges back to MLE. For a coin with $h$ heads, $t$ tails, and a prior worth one extra "pseudo-head" and one "pseudo-tail," MAP gives $\hat p = (h+1)/(h+t+2)$ — which turns MLE's reckless $1.0$-from-one-head into a sober $2/3$.

## Grounded explanation

### The gap MAP fills

[[maximum-likelihood-estimation]] is built on a single principle: report the parameter under which the observed data would have been most probable. That principle is honest and assumption-free, but it has a sharp edge, called out explicitly in that node. Flip a coin **once**, see one head and zero tails, and MLE returns $\hat p = 1/(1+0) = 1.0$ — it declares the coin will *never* land tails, on the strength of a single flip. MLE has no built-in skepticism; it trusts the data completely, even when the data is one observation.

The trouble is that we usually *do* have skepticism. Before flipping any coin we believe it is probably close to fair, certainly not guaranteed two-headed. MLE has no channel to express that belief — its only input is the data. MAP adds exactly that channel. It is the estimation principle hinted at, but deliberately deferred, at the end of [[maximum-likelihood-estimation]]: "tempering [the data] with prior belief is the job of a different estimation principle." This node is that principle.

Throughout, as in [[maximum-likelihood-estimation]], $\theta$ ("theta") denotes the unknown **parameter** — the knob we want to estimate — and $D$ denotes the **data** we observed. A hat, as in $\hat\theta$, marks a value *estimated from data*, distinct from the unknown true $\theta$. The notation $\arg\max_\theta f(\theta)$ means "the value of $\theta$ at which $f$ is largest" — the *location* of the peak, not its height.

### From "explains the data best" to "most probable given the data"

MLE maximizes the **likelihood** $P(D \mid \theta)$ — the forward, easy-to-state direction: *how probable is the data, if this $\theta$ were true?* But notice what MLE does **not** claim. As [[maximum-likelihood-estimation]] is careful to say, the likelihood is not a probability distribution over $\theta$; "the most probable $\theta$" is not even defined from the likelihood alone. MLE returns the $\theta$ that best *explains* the data, which is a subtly different — and weaker — thing than the $\theta$ that is most *probable* once you have seen the data.

The quantity we'd actually like to maximize is that latter, reversed conditional: $P(\theta \mid D)$, the probability of the parameter *given* the data. And reversing a conditional — turning "data given $\theta$" into "$\theta$ given data" — is precisely the job of [[bayes-rule]]. Writing it for an unknown $\theta$ and observed $D$:

> $P(\theta \mid D) = \dfrac{P(D \mid \theta)\,P(\theta)}{P(D)}$.

This object, $P(\theta \mid D)$, is the **posterior**: the distribution over $\theta$ *after* folding in the data. Reading the three named pieces from [[bayes-rule]]:

- $P(D \mid \theta)$ is the **[[likelihood]]** — the very thing MLE maximizes. For each candidate $\theta$, how probable the data would be if that $\theta$ held.
- $P(\theta)$ is the **prior** — the [[probability-distribution]] over $\theta$ *before* seeing any data, the formal home for our advance belief ("the coin is probably near fair").
- $P(D)$ is the **evidence** $= \sum_\theta P(D\mid\theta)P(\theta)$, the overall probability of the data, not depending on $\theta$.

MAP's definition is now one line: the **maximum a posteriori estimate** is the value of $\theta$ that maximizes the posterior —

$$ \hat\theta_{\text{MAP}} \;=\; \arg\max_\theta\, P(\theta \mid D). $$

It returns the posterior's **mode**: the single highest point of the after-the-data belief. Where MLE reports the peak of the likelihood, MAP reports the peak of the posterior.

### Why the evidence drops out, and what's left

Maximizing $P(\theta\mid D) = P(D\mid\theta)P(\theta)/P(D)$ looks like it needs the awkward denominator $P(D)$. It does not — and the reason comes straight from [[bayes-rule]]. The evidence $P(D)$ does **not depend on $\theta$**; it is one fixed number, the same for every candidate $\theta$. Dividing every value by the same constant cannot move the *location* of the highest one. So for the purpose of finding the $\arg\max$, the denominator is inert, and [[bayes-rule]]'s proportional form is all we need:

$$ P(\theta \mid D) \;\propto\; P(D \mid \theta)\,P(\theta), $$

where $\propto$ means "proportional to." Therefore

$$ \hat\theta_{\text{MAP}} \;=\; \arg\max_\theta\, P(\theta \mid D) \;=\; \arg\max_\theta\, P(D \mid \theta)\,P(\theta). $$

This is the central identity of the node. Compare it to MLE side by side:

| | objective maximized |
|---|---|
| MLE | $P(D \mid \theta)$ |
| MAP | $P(D \mid \theta)\,P(\theta)$ |

MAP is MLE's objective times one extra factor, the prior $P(\theta)$. That single factor is the whole concept. Everything that makes [[maximum-likelihood-estimation]] mechanical now applies unchanged.

### The mechanics: identical to MLE, plus one term

[[maximum-likelihood-estimation]] does not maximize a product directly — a fragile chain of small factors, ugly to differentiate. It takes the **logarithm** first. The log is strictly increasing, so it never moves the location of a peak ($\arg\max_\theta f = \arg\max_\theta \ln f$), yet by $\ln(ab) = \ln a + \ln b$ it turns the product into a sum that a derivative handles termwise. We use the identical move here. Taking $\ln$ of $P(D\mid\theta)P(\theta)$ and splitting the product:

$$ \ln\big[P(D\mid\theta)\,P(\theta)\big] \;=\; \underbrace{\ln P(D\mid\theta)}_{\text{log-likelihood}} \;+\; \underbrace{\ln P(\theta)}_{\text{log-prior}}. $$

The first term is exactly the **log-likelihood** $\ell(\theta)$ that MLE maximizes. The second, $\ln P(\theta)$, is the **only** addition. So:

$$ \text{MAP objective} \;=\; \text{(MLE objective)} \;+\; \ln P(\theta). $$

The recipe is therefore the four-step MLE algorithm with one inserted term: (1) write the log-likelihood as before; (2) add the log-prior $\ln P(\theta)$; (3) differentiate the sum and set the derivative to zero; (4) confirm a maximum. Because a [[maximum-likelihood-estimation]]-style derivative acts on a sum termwise, the extra $\ln P(\theta)$ just contributes its own derivative alongside the data terms. MLE is the special case where the prior is *flat* (every $\theta$ equally believed in advance, so $\ln P(\theta)$ is a constant whose derivative is zero) — then the extra term vanishes and MAP **is** MLE. This is also the deep "why it regularizes": $\ln P(\theta)$ acts as a **penalty** that pulls the estimate away from data values the prior considers implausible, and toward values the prior favors.

### A prior as pseudo-counts (the Beta prior, defined inline)

To make this concrete on the coin we need a prior $P(p)$ over the heads-probability $p \in [0,1]$. The most natural choice has an interpretation so simple it needs no machinery: a prior that *pretends you have already seen some flips before the experiment starts.* Suppose your advance belief is worth $a-1$ imaginary prior heads and $b-1$ imaginary prior tails, for two chosen numbers $a, b > 0$. The prior that encodes exactly this is

$$ P(p) \;\propto\; p^{\,a-1}\,(1-p)^{\,b-1}, $$

known as the **Beta$(a,b)$ prior** — but you do not need that name or any distribution theory; read it purely as the formula above, "$a-1$ pseudo-heads and $b-1$ pseudo-tails," exactly mirroring the likelihood's real $h$ heads and $t$ tails. Two settings to anchor it:

- $a=b=1$ gives $P(p) \propto p^0(1-p)^0 = 1$: zero pseudo-flips, a perfectly **flat** prior that believes every $p$ equally. By the previous section this recovers MLE.
- $a=b=2$ gives $P(p) \propto p^1(1-p)^1$: **one** pseudo-head and **one** pseudo-tail — a gentle nudge toward fairness ($p=0.5$), the value at which $p(1-p)$ peaks.

### Worked instance: the coin, with and without a prior

Take the same coin as [[maximum-likelihood-estimation]]: each flip lands heads (probability $p$) or tails (probability $1-p$), and after $n=h+t$ flips we have recorded $h$ heads and $t$ tails. From that node, the log-likelihood is

$$ \ell(p) = h\ln p + t\ln(1-p). $$

**Step 2 — add the log-prior.** Take the log of the pseudo-count prior, using $\ln(p^{a-1}(1-p)^{b-1}) = (a-1)\ln p + (b-1)\ln(1-p)$, and drop the proportionality constant (it does not depend on $p$, so its derivative is zero). The full MAP objective is the sum:

$$ g(p) = \underbrace{h\ln p + t\ln(1-p)}_{\text{log-likelihood}} \;+\; \underbrace{(a-1)\ln p + (b-1)\ln(1-p)}_{\text{log-prior}} \;=\; (h+a-1)\ln p + (t+b-1)\ln(1-p). $$

Look at what happened: the real counts and the pseudo-counts simply *added*. The objective is structurally the **same** as MLE's, but with effective counts $h' = h+a-1$ and $t' = t+b-1$. The prior is, quite literally, extra flips you imagined.

**Step 3 — differentiate and set to zero.** This is identical to the MLE derivation with $h', t'$ in place of $h, t$. Using the [[maximum-likelihood-estimation]] derivatives ($\tfrac{d}{dp}\ln p = 1/p$ and $\tfrac{d}{dp}\ln(1-p) = -1/(1-p)$):

$$ g'(p) = \frac{h+a-1}{p} - \frac{t+b-1}{1-p} = 0 \;\Longrightarrow\; (h+a-1)(1-p) = (t+b-1)\,p, $$

which solves (exactly as MLE's "heads over total" solved) to

$$ \boxed{\;\hat p_{\text{MAP}} = \dfrac{h+a-1}{(h+a-1)+(t+b-1)} = \dfrac{h+a-1}{h+t+a+b-2}\;}. $$

**Step 4 — confirm a maximum.** Same argument as in [[maximum-likelihood-estimation]]: as $p$ rises from $0$ to $1$, the first term $\tfrac{h+a-1}{p}$ shrinks and the second $\tfrac{t+b-1}{1-p}$ grows, so $g'$ moves from positive to negative, crossing zero once — a genuine peak.

**Plug in numbers — the $8/2$ case.** Use the same data as [[maximum-likelihood-estimation]], $h=8$, $t=2$, and the one-pseudo-head/one-pseudo-tail prior $a=b=2$ (so $a-1=b-1=1$). Then

$$ \hat p_{\text{MAP}} = \frac{8+1}{8+2+2+2-2} = \frac{9}{12} = 0.75. $$

MLE on this data gave $\hat p_{\text{MLE}} = 8/10 = 0.8$. MAP returns $0.75$ — the prior has pulled the estimate **down from $0.8$ toward $0.5$**, the fair value it gently favors. The pull is small here, because $10$ real flips outweigh $2$ pseudo-flips: $9/12$ is only modestly nearer fairness than $8/10$.

**The case that shows the point — one head.** Now the over-confident edge case from [[maximum-likelihood-estimation]]: flip **once**, see $h=1$ head, $t=0$ tails, same $a=b=2$ prior. MLE returned the reckless $\hat p_{\text{MLE}} = 1/1 = 1.0$ — *never tails*. MAP returns

$$ \hat p_{\text{MAP}} = \frac{1+1}{1+0+2+2-2} = \frac{2}{3} \approx 0.667. $$

Instead of declaring the coin two-headed on one flip, MAP says "probably biased toward heads, but I'm not certain" — exactly the tempered judgment a sensible person would make. The single pseudo-tail supplied by the prior is enough to keep $\hat p$ strictly below $1$. This is the regularization promised in the summary, made arithmetic: the prior's imaginary tail forbids the absurd certainty that a lone real head would otherwise force.

### Why MAP converges to MLE as data grows

The pseudo-count form makes the convergence transparent and worth stating, since it is *why* adding a prior is safe rather than a permanent thumb on the scale. Hold the prior fixed at $a=b=2$ and let the data grow while staying $80\%$ heads. With $h=80$, $t=20$:

$$ \hat p_{\text{MAP}} = \frac{80+1}{80+20+2} = \frac{81}{102} \approx 0.794, \qquad \hat p_{\text{MLE}} = \frac{80}{100} = 0.8. $$

With $h=800$, $t=200$ it would be $801/1002 \approx 0.7994$. The fixed prior contributes a constant $\pm 1$ to numerator and denominator; as the real counts $h, t$ grow without bound, that constant becomes negligible and $\hat p_{\text{MAP}} \to h/(h+t) = \hat p_{\text{MLE}}$. The prior's voice is loud when the data is a whisper and inaudible once the data shouts — which is precisely the behavior we want from a tempering belief. MAP regularizes the small-sample estimate while reducing to plain [[maximum-likelihood-estimation]] in the large-sample limit.

## Prerequisites

- [[maximum-likelihood-estimation]]
- [[bayes-rule]]

## Sources

_none_
