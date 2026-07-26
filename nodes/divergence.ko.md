# 발산 (∇·F)

## 요약

**발산(divergence)**은 [[vector-field]]를 각 점에서의 순유출량을 측정하는
스칼라로 바꾼다. 입력: 벡터장 → 출력: 스칼라.

## 상세 설명

이는 [[del-operator]]와 장의 [[vector-dot-product]]다:

$$\nabla \cdot F = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z}$$

— *대각선* 편미분들의 합이다; 각 $\partial F_i/\partial x_i$는 해당 장 성분의
[[differential]]에서 나온 한 항목이다(F의 [[jacobian]]의 대각합). 발산이
양수이면 장이 퍼져나가고 있다는(source) 뜻이고, 음수이면 수렴하고 있다는(sink)
뜻이다.

## 선행 개념

- [[del-operator]]
- [[vector-dot-product]]
- [[vector-field]]
- [[differential]]
- [[jacobian]]

## 출처

- etc/differential-operators-summary.html
