---
id: load-balancing
title: Load Balancing
summary: Load balancing places one traffic-distribution decision in front of multiple interchangeable backends so clients use one endpoint while work is spread across the available capacity.
type: concept
tags: [networking]
prereqs: [ip-routing]
sources:
  - https://cdn.haproxy.com/documentation/haproxy-configuration-manual/new/latest/intro/
  - https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/
status: explained
created: 2026-08-26
updated: 2026-08-26
---

# Load Balancing

## Summary

**Load balancing** places one traffic-distribution decision in front of a pool of interchangeable
backends. Clients send every connection or request to one stable endpoint; the load balancer chooses
an available backend for each unit of work and forwards it there. This does not make one request run
faster. It lets several requests run at the same time, uses otherwise idle capacity, and lets an
unavailable backend leave the pool without forcing clients to learn a new destination.

## Grounded explanation

### One address, several possible destinations

Ordinary [[ip-routing]] answers, for each packet, which next network interface and next device lead
toward the packet's destination address. If every client addresses one server directly, that address
also fixes which server receives the work. Adding a second server does not help those clients: they
still route to the first address.

A load balancer separates the **front endpoint** from the **backend pool**. The front endpoint is the
address clients use. The backend pool is the current set of servers capable of performing the same
operation. On each new connection or request, the balancer selects one member of that pool and steers
the traffic toward it. The client therefore knows *where to ask*, while the balancer decides *who
answers*.

The selection rule is the load-balancing algorithm. **Round robin** chooses each available backend in
turn. **Least connections** chooses the backend currently serving the fewest open connections. A
hash-based rule repeatedly maps the same request property, such as a client address, to the same
backend when that continuity matters. The rule changes how work is distributed; it does not change
the defining structure of one front endpoint and several interchangeable backends.

### Worked instance: three checkout servers

Suppose clients connect to `203.0.113.10:443`, and the pool contains servers A, B, and C. With round
robin, three new connections are assigned A, B, and C respectively; a fourth returns to A. Three
connections can now be processed concurrently, but each individual connection still runs on exactly
one server.

Now B fails its availability check. The balancer removes B from the eligible pool, so the next
connections alternate between C and A. The front endpoint remains `203.0.113.10:443`; clients neither
discover B's failure nor choose a replacement. If B later becomes available, it can re-enter the pool
without changing the client-facing address.

This reveals the two independent jobs a practical balancer performs: maintain an accurate set of
eligible backends, then apply a selection rule to each new unit of work. Distribution improves total
throughput only when enough independent work exists to occupy multiple backends. Availability
improves only when failed backends are excluded and at least one healthy backend remains.

### Where the decision can happen

At the network or transport layers, the unit is usually a flow identified by addresses, ports, and
protocol; the balancer steers packets without understanding an application message. At an application
layer, a proxy can first read an HTTP request and choose by hostname, path, or header. Both are load
balancing because both preserve the same invariant: the client uses one front endpoint while a
selection decision maps its work onto one member of a changing backend pool.

## Prerequisites

- [[ip-routing]]

## Sources

- [HAProxy Configuration Manual — introduction to load balancing](https://cdn.haproxy.com/documentation/haproxy-configuration-manual/new/latest/intro/)
- [NGINX — HTTP Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
