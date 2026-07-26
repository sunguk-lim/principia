# 기울기

## 요약

**기울기(gradient)**는 여러 입력을 갖는 함수의 편미분들을 모아, 가장 가파른
증가 방향을 가리키는 하나의 벡터로 만든다.

## 상세 설명

여러 매개변수를 갖는 함수 $f(\theta_1,\dots,\theta_n)$에 대해,

$$\nabla f = \left(\frac{\partial f}{\partial \theta_1},\dots,\frac{\partial f}{\partial \theta_n}\right)$$

여기서 각 항목은 $f$의 [[partial-derivative]]다 — 나머지 입력을 고정한 채
하나의 입력에 대해 취한 [[derivative]]다. 이 벡터는 오르막을 가리키므로,
$-\nabla f$는 가장 가파른 *감소* 방향 — 손실을 줄이기 위해 경사하강법이
내딛는 방향 — 을 가리킨다.

## 선행 개념

- [[partial-derivative]]
- [[derivative]]

## 출처

_없음_
