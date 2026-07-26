# 경사 하강법

## 요약

**경사 하강법**(gradient descent)은 손실이 가장 빨리 줄어드는 방향으로 파라미터를 반복해서 한 걸음씩 옮겨 손실을 최소화한다.

## 상세 설명

파라미터에 대한 [[loss-function]]의 [[gradient]]를 구한 뒤, 그 *반대* 방향으로 작은 한 걸음을 옮긴다:

$$\theta \leftarrow \theta - \eta\,\nabla \mathcal{L}(\theta)$$

$-\nabla\mathcal{L}$은 가장 가파른 감소 방향을 가리키므로 매 걸음마다 손실이 낮아지고, 이를 반복하면 손실은 최솟값을 향해 내려간다. 스칼라 $\eta$(학습률, learning rate)는 걸음의 크기를 정한다 — 너무 크면 목표를 지나쳐 버리고, 너무 작으면 기어가듯 느리다. 이것이 파인 튜닝이 실행하는 옵티마이저다.

## 선행 개념

- [[gradient]]
- [[loss-function]]

## 출처

_없음_
