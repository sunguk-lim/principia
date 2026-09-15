# 기울기의 회전은 0이다

## 요약

임의의 스칼라 함수 $f$에 대해, 그 [[gradient]]의 [[curl]]은 항상 영벡터다:
$\nabla \times (\nabla f) = 0$. 기울기로 만들어진 장은 결코 국소 스핀을
가질 수 없다 — 이는 *비회전적(irrotational)*이다. 그 이유는 기울기의
도함수 행렬이 [[hessian]]이고, 헤시안이 대칭이라서 회전이 측정할 것이
아무것도 남지 않기 때문이다.

## 상세 설명

여기서 다루는 개념은 어떤 스칼라 함수에서 시작하든 성립하는 단일 항등식이다:
여러 변수의 함수 $f$를 아무거나 취해, 그 [[gradient]] $\nabla f$([[partial-derivative]]들의
벡터로, 오르막 방향을 가리킨다)를 만든 다음, 그 [[vector-field]]의 [[curl]]을
취한다. 결과는 항상 영벡터다. 말로 하면: *무언가*의 기울기인 장은 어디서나
회전이 0이다. 그런 장을 *비회전적*(회전 없음) 또는 *보존적(conservative)*이라
부른다. 이 노드의 요점은 그저 $\nabla \times (\nabla f) = 0$이라는 사실이
아니라, 그것이 왜 성립할 수밖에 없는가다.

이유를 보려면 각 연산자가 무엇을 측정하는지 나란히 놓아보자. 벡터장의 [[curl]]은
편미분들의 거울-쌍 차이를 취한다: 각 출력 성분은
$\partial F_j/\partial x_i - \partial F_i/\partial x_j$의 형태를 가지며, 이는
장의 $j$번째 조각이 $x_i$를 따라 어떻게 변하는지와 $i$번째 조각이 $x_j$를 따라
어떻게 변하는지 사이의 차이다. 회전은 [[differential-operators]] 중 마이너스
부호를 갖는 유일한 연산자인데, 정확히 그 이유는 장의 도함수 행렬 중 이
*반대칭* 부분 — 두 교차 변화율이 서로 일치하지 않을 때만 살아남는 부분 —
을 골라내기 때문이다.

이제 이 기계에 기울기를 대입해보자. 장은 $F = \nabla f$이므로, 그 $i$번째
성분은 $F_i = \partial f/\partial x_i$이다. 이 특정한 장의 도함수 행렬 —
$(i,j)$ 항목이 $\partial F_i/\partial x_j$인 행렬 — 은 정의상 $f$의
[[hessian]], 즉 이계 편미분들의 행렬 $H_{ij} = \partial^2 f / \partial x_i\, \partial x_j$이다.
그러므로 회전이 다루는 바로 그 양이 헤시안이다.

정당화하는 이유는 그 행렬의 한 성질이다: **헤시안은 대칭이다.** 그 거울
칸들은 서로 같다, $\partial^2 f/\partial x_i\,\partial x_j =
\partial^2 f/\partial x_j\,\partial x_i$ — $x_i$로 먼저 미분하고 $x_j$로
미분하는 것이 그 역순과 같은 결과를 준다. (이 혼합 편미분의 교환은 클레로의
정리(Clairaut's theorem)이며, 그 이계 도함수들이 연속인 통상적인 경우
언제나 성립한다.) 대칭 행렬은 자기 자신의 거울상이므로 **반대칭 부분이
전혀 없다**: 모든 거울-쌍 차이는 어떤 양에서 그 자신의 동일한 복사본을
뺀 것이므로 0이다. 회전은 정확히 그 반대칭 부분을 측정하는데 — 대칭 행렬에는
측정할 것이 남아 있지 않다. 이것이 그 메커니즘이다: $\nabla f$의 각 회전
성분은 대칭성에 의해 서로 같은 두 혼합 편미분의 차이이므로, 각 성분은
0으로 상쇄된다.

예시. $f(x,y,z) = x^2 y$를 취하자. 그 [[gradient]]는 일계 편미분들의
벡터다: $\partial f/\partial x = 2xy$, $\partial f/\partial y = x^2$,
$\partial f/\partial z = 0$이므로, $\nabla f = (2xy,\ x^2,\ 0)$이다. 이제
이 장의 [[curl]]을 $\nabla \times F = (\partial F_z/\partial y
- \partial F_y/\partial z,\ \partial F_x/\partial z - \partial F_z/\partial x,\
\partial F_y/\partial x - \partial F_x/\partial y)$를 써서 $F_x = 2xy$,
$F_y = x^2$, $F_z = 0$으로 성분별로 계산하자. 첫 번째 성분:
$\partial F_z/\partial y - \partial F_y/\partial z =
\partial(0)/\partial y - \partial(x^2)/\partial z = 0 - 0 = 0$. 두 번째
성분: $\partial F_x/\partial z - \partial F_z/\partial x = \partial(2xy)/\partial z -
\partial(0)/\partial x = 0 - 0 = 0$. 세 번째 성분 — 상쇄되기 전 두 항이
모두 0이 아니라는 점에서 흥미로운 항: $\partial F_y/\partial x -
\partial F_x/\partial y = \partial(x^2)/\partial x - \partial(2xy)/\partial y =
2x - 2x = 0$. 이 마지막 상쇄는 명시적인 대칭 거울 쌍이다: $2x$는
한 방향으로 계산한 $\partial^2 f/\partial x\,\partial y$($f \to x^2 \to 2x$)이고
$2x$는 다른 순서로 계산한 같은 이계 도함수다($f \to 2xy \to 2x$). 혼합
편미분이 같으므로 차이가 사라진다. 회전은 $(0,0,0)$이며, 이는 항등식이
보장하는 바다.

이 항등식은 거꾸로도 성립하며, 그 역이 이를 검사 도구로 유용하게 만든다.
주어진 어떤 벡터장의 [[curl]]을 계산했는데 *0이 아닌* 답이 나온다면, 그
장은 어떤 스칼라 함수의 [[gradient]]도 될 수 없다 — 만약 그랬다면 그 회전은
0으로 강제되었을 것이기 때문이다. 0이 아닌 회전은 비보존성의 증명서다.

## 선행 개념

- [[curl]]
- [[gradient]]
- [[hessian]]
- [[partial-derivative]]
- [[vector-field]]

## 출처

- etc/differential-operators-summary.html
