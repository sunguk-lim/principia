# 헤시안 (H)

## 요약

**헤시안(Hessian)**은 스칼라 함수의 이계 편도함수들로 이루어진 행렬 —
그래디언트의 야코비안이다. 입력: 스칼라 → 출력: 행렬.

## 상세 설명

헤시안은 [[gradient]] $\nabla f$의 [[jacobian]]이다:

$$H_{ij} = \frac{\partial^2 f}{\partial x_i\, \partial x_j}$$

각 원소는 이계 [[partial-derivative]]다 — $f$를 먼저 $x_j$에 대해 미분하고, 그다음 다시 $x_i$에 대해 미분한다.

헤시안은 $f$의 국소 곡률(local curvature)을 기술한다 — 일계 미분(선형 근사)이 볼 수 없는 이차(second-order) 정보다. 뉴턴 방법(Newton's method) 같은 이차 최적화에 쓰인다. 헤시안은 **대칭(symmetric)**이다 — 혼합 편도함수는 순서를 바꿔도 같기 때문이다 — 그래서 거울 위치의 원소들이 서로 같으며, 그래디언트의 컬(curl)이 0이 되는 이유이기도 하다.

## 선행 개념

- [[jacobian]]
- [[gradient]]
- [[partial-derivative]]
## 출처

- etc/differential-operators-summary.html
