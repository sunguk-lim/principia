# 회전 (∇×F)

## 요약

**회전(curl)**은 [[vector-field]]를 각 점에서의 국소 회전(스핀)을 측정하는 벡터로 바꾼다.
입력: 벡터 → 출력: 벡터.

## 상세 설명

이는 [[del-operator]]와 장(field)의 [[cross-product]]이며, 각 성분은 편미분들의
거울-쌍 차이다:

$$\nabla \times F = \left(\frac{\partial F_z}{\partial y}-\frac{\partial F_y}{\partial z},\ \frac{\partial F_x}{\partial z}-\frac{\partial F_z}{\partial x},\ \frac{\partial F_y}{\partial x}-\frac{\partial F_x}{\partial y}\right)$$

회전은 연산자들 중 유일하게 마이너스 부호를 갖는데, 이는 [[jacobian]]의
*반대칭* 부분(흐름의 강체 회전 성분)을 포착하기 때문이다.

## 선행 개념

- [[del-operator]]
- [[vector-field]]
- [[cross-product]]
- [[jacobian]]

## 출처

- etc/differential-operators-summary.html
