# 회전의 발산은 0이다

## 요약

*임의의* [[vector-field]] $F$에 대해, 그 [[curl]]의 [[divergence]]는 정확히
0이다: $\nabla \cdot (\nabla \times F) = 0$. 회전 장은 결코 퍼져나가거나
수렴할 수 없다 — 어디에도 원천(source)이나 흡입원(sink)이 없다. 그런 장을
**솔레노이드형(solenoidal)**(또는 *무원천*) 장이라 부른다. 그 이면도
똑같이 유용하다: 어떤 장이 어딘가에서 0이 아닌 발산을 갖는다면, 그것은
어떤 것의 회전으로도 쓰일 수 없다.

## 상세 설명

여기서 다루는 두 연산자는 이미 알고 있는 것이다. 장 $F$의 [[curl]]은 편미분들의
성분-쌍 차이를 취해 새로운 벡터로 묶는다; 이는 $F$가 변하는 방식의
*반대칭* 부분이며, 마이너스 부호를 갖는 유일한 연산자다. 장의 [[divergence]]는
그 장의 세 *대각선* 편미분 — 각 성분이 자신의 축을 따라 변하는 속도 — 를
취해 순유출량을 측정하는 하나의 스칼라로 더한다.

주장은 [[curl]]의 출력을 [[divergence]]에 넣으면, $F$가 무엇이든 상관없이
항상 0이 나온다는 것이다. *왜* 그런지 보려면 도함수를 따라가 보자.

$F = (P, Q, R)$로 써서 그 세 성분 함수에 이름을 붙이자. 그 [[curl]]은 벡터

$$\nabla \times F = \left(\frac{\partial R}{\partial y}-\frac{\partial Q}{\partial z},\ \ \frac{\partial P}{\partial z}-\frac{\partial R}{\partial x},\ \ \frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)$$

이다. 각 성분은 *거울-쌍* 차이다: 변수를 바꾼 거울상을 뺀 어떤 편미분이다.
이제 이 벡터의 [[divergence]]를 취하자 — 그것은 첫 성분을 $x$로, 두 번째
성분을 $y$로, 세 번째 성분을 $z$로 미분한 다음 세 결과를 더한다는 뜻이다:

$$\nabla \cdot (\nabla \times F) = \frac{\partial}{\partial x}\!\left(\frac{\partial R}{\partial y}-\frac{\partial Q}{\partial z}\right) + \frac{\partial}{\partial y}\!\left(\frac{\partial P}{\partial z}-\frac{\partial R}{\partial x}\right) + \frac{\partial}{\partial z}\!\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right).$$

여섯 항을 전개하면, 모든 항이 *혼합 이계 편미분* — 서로 다른 두 변수로
한 번씩 취한 [[partial-derivative]] — 이다. 여기 핵심 단계가 있다. 혼합
편미분은 어떤 순서로 취하든 같다: $R$을 먼저 $y$로 미분하고 그다음 $x$로
미분하는 것은 먼저 $x$로 그다음 $y$로 미분하는 것과 같은 함수를 주며,
$\frac{\partial^2 R}{\partial x\,\partial y} = \frac{\partial^2 R}{\partial y\,\partial x}$로 쓴다. (이는 그
이계 도함수들이 연속일 때 언제나 성립한다 — 통상적인 매끄러운 장에서는
항상 참이다.) 이 등식이 이 항등식 전체의 엔진이다.

이 등식을 손에 쥐고, 여섯 항을 어느 성분에서 나왔는지에 따라 묶어보자.
$R$에서 나온 두 항은 (첫 번째 자리에서) $\frac{\partial^2 R}{\partial x\,\partial y}$와
(두 번째 자리에서) $-\frac{\partial^2 R}{\partial y\,\partial x}$이다. 이들은 같은 혼합
편미분에 *반대* 부호가 붙은 것이므로 상쇄된다. $Q$에서 나온 두 항은
$-\frac{\partial^2 Q}{\partial x\,\partial z}$와 $+\frac{\partial^2 Q}{\partial z\,\partial x}$이며 — 마찬가지로
같고 반대이므로 상쇄된다. $P$의 두 항, $+\frac{\partial^2 P}{\partial y\,\partial z}$와
$-\frac{\partial^2 P}{\partial z\,\partial y}$도 상쇄된다. 세 쌍이 상쇄되어, 합은 0이다.

이 반대 부호는 우연이 아니다: 이는 [[curl]]을 *정의하는* 마이너스 부호로부터
물려받은 것이다. [[curl]]은 각 성분을 한 편미분에서 그 거울상을 뺀 것으로
만들고, [[divergence]]는 그다음 그 거울들 각각을 대응하는 외부 미분으로
때리므로, 모든 항이 부호가 뒤집힌 쌍둥이를 만난다. 이는 기울기의 회전이
사라지게 만드는 것과 같은 반대칭성을, 한 단계 아래에서 적용한 것이다:
거기서는 대칭적 대상이 반대칭적 연산자를 만났고; 여기서는 반대칭적 대상이
대칭적 연산자를 만난다. 어느 쪽이든 대칭 부분과 반대칭 부분이 서로를
소멸시킨다.

**예시.** $F = (xy,\ yz,\ zx)$를 취해, $P = xy$, $Q = yz$, $R = zx$로 —
퇴화하지 않은, 진짜 교차 결합을 가진 장이다. 먼저 그 [[curl]]을 성분별로
계산하면:

- 첫 번째 자리: $\dfrac{\partial R}{\partial y} - \dfrac{\partial Q}{\partial z} = \dfrac{\partial (zx)}{\partial y} - \dfrac{\partial (yz)}{\partial z} = 0 - y = -y.$
- 두 번째 자리: $\dfrac{\partial P}{\partial z} - \dfrac{\partial R}{\partial x} = \dfrac{\partial (xy)}{\partial z} - \dfrac{\partial (zx)}{\partial x} = 0 - z = -z.$
- 세 번째 자리: $\dfrac{\partial Q}{\partial x} - \dfrac{\partial P}{\partial y} = \dfrac{\partial (yz)}{\partial x} - \dfrac{\partial (xy)}{\partial y} = 0 - x = -x.$

그래서 $\nabla \times F = (-y,\ -z,\ -x)$다. 이제 그 [[divergence]] —
각 성분을 자신의 축으로 미분해 더하면:

$$\nabla \cdot (\nabla \times F) = \frac{\partial (-y)}{\partial x} + \frac{\partial (-z)}{\partial y} + \frac{\partial (-x)}{\partial z} = 0 + 0 + 0 = 0.$$

각 항이 사라지는 이유는, 회전이 $x$축에는 $y$에만 의존하는 성분을, $y$축에는
$z$에만 의존하는 성분을, $z$축에는 $x$에만 의존하는 성분을 넘겨주었기
때문이다 — 거울-차이들이 남기는 교차 결합은 항상 *대각선 밖에* 있으며,
바로 발산이 들여다보지 않는 곳이다. 항등식이 모든 장에 대해 보장하는 대로,
결과는 0이다.

## 선행 개념

- [[vector-field]]
- [[divergence]]
- [[curl]]
- [[partial-derivative]]

## 출처

- etc/differential-operators-summary.html
