# 행렬 곱셈

## 요약

`m×k` 행렬 A와 `k×n` 행렬 B를 결합하여 `m×n` 행렬 C를 만드는 것으로, 각 원소
`C[i][j]`는 A의 `i`행과 B의 `j`열의 곱들의 합이다.

## 상세 설명

각 출력 원소는 `C[i][j] = A[i][1]·B[1][j] + … + A[i][k]·B[k][j]`이다 — 곱셈과
덧셈의 연쇄, 즉 순수한 [[arithmetic]]이다. 이 원소별 패턴(행 × 열, 합산)은 행과
열의 [[vector-dot-product]]와 정확히 같은데, 그 노드는 프런티어에 있으므로 여기서는
[[arithmetic]]에만 의존하고 내적 프레이밍은 나중에 다듬을 것으로 미뤄둔다.

## Prerequisites

- [[arithmetic]]
- [[vector-dot-product]]

## Sources

_none_
