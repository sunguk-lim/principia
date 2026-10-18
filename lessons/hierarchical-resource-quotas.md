# Hierarchical Resource Quotas

## Meaning

A department may own a budget shared among several projects. A hierarchy makes each project subject to both its own policy and the budgets of its ancestors. This is an entitlement structure, not a physical GPU partition.

## Mechanism

A leaf’s request is checked along its ancestor chain. Distinguish a guaranteed share from a hard maximum, and distinguish unused entitlement from borrowable physical capacity. [[cluster-fair-share-scheduling]] decides how active competitors share capacity and when borrowed resources are reclaimed. Policies must specify whether parent and child values are absolute, relative, or derived, how inactive queues redistribute shares, and how non-preemptible work delays guarantees. A nominal quota does not solve topology, memory, device compatibility, or gang feasibility. The management controller stores organizational intent; the scheduling and runtime layers enforce different parts of the contract.

## One example

A cluster has 16 GPUs. Department D has a hard limit of ten; projects A and B have limits of eight each. If A uses seven and B requests five, the leaf limits both permit their individual totals, but D would reach twelve. At most three additional GPUs fit D’s hard cap. A guarantee of four for B is not the same as permission to violate that cap: the policy may need reclaim, queueing, or changed allocations. If D instead has a guarantee of ten and a maximum of sixteen, borrowing may permit twelve when other departments are idle. Test all ancestor boundaries, updates during running work, and reclaim delays.

## Check your understanding

Can child maxima simply be added to infer the parent guarantee? No. Maxima bound use; guarantees describe promised shares under stated policy and feasibility conditions.
