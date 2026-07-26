# 델 연산자(Del operator) (∇)

## 요약

**델 연산자(del operator)** $\nabla$ 는 *형식적 벡터(formal vector)* — 세 성분이 숫자가 아니라
**미분하라는 지시**인 벡터다. 풀어 쓰면
$\nabla = \left(\tfrac{\partial}{\partial x},\ \tfrac{\partial}{\partial y},\ \tfrac{\partial}{\partial z}\right)$
이다. 그 핵심은 경제성이다: 벡터가 곱해질 수 있는 세 가지 방식으로 함수나 장(field)과
"곱해질" 때, 벡터 미적분학의 1차 미분 연산자 가족 전체를 만들어내는 단 하나의 대상이다.

## 상세 설명

**기본 재료.** $\nabla$ 의 각 성분은 [[partial-derivative]] 연산자다 —
$\tfrac{\partial}{\partial x}$ 는 "다른 변수를 고정한 채 $x$ 가 움직일 때 입력이 어떻게 변하는지
측정하라"는 뜻이다. 그 자체로 $\tfrac{\partial}{\partial x}$ 는 불완전하다: 목적어를 기다리는
동사다. 함수 $f$ 를 건네주어야 비로소 숫자값을 갖는 대상 $\tfrac{\partial f}{\partial x}$ 를
만들어낸다. 세 좌표 편미분을 나란히 쌓으면 $\nabla$ 가 된다.

**왜 "형식적 벡터"라고 부르는가.** $\nabla$ 는 벡터 $(a, b, c)$ 처럼 보이지만, 여기서 $a, b, c$
는 실수가 아니라 연산자다. *형식적(formal)* 이라는 단어가 바로 이 점을 표시한다: 벡터의
*형태*를 가지고 있고, 그 자리에 지시가 들어 있는데도 벡터의 대수 규칙에 따라 기호를 밀고 다니는
것이 허용된다. 이 편리함의 대가는 한 구절의 의미가 바뀐다는 것이다. 벡터의 규칙이 $\nabla$ 의
성분을 장의 조각과 "곱하라"고 말할 때, **"곱한다"는 산술이 아니라 *적용한다*는 뜻이다.**
$\tfrac{\partial}{\partial x}\cdot f$ 라고 쓰는 것은 두 숫자를 곱하는 것이 아니라, 연산자
$\tfrac{\partial}{\partial x}$ 를 함수 $f$ 에 적용해 $\tfrac{\partial f}{\partial x}$ 를
내놓는 것이다.

**이 치환이 왜 정당한가.** 이것은 표기의 엉성한 남용이 아니라 정확한 이유가 있어서 작동한다.
벡터 곱들 — 스칼라 곱, [[vector-dot-product]], [[cross-product]] — 은 곱셈을 합에 걸쳐
**분배**하고 스칼라 인자를 앞으로 빼내는 방식으로 만들어진다. (내적 $a\cdot b = \sum_i a_i b_i$
가 곱들의 합이고, 외적의 성분들이 곱들의 차라는 점을 떠올려 보라.) 미분은 바로 그 두 법칙을
따른다: 미분은 **선형(linear)** 이다. 즉
$\tfrac{\partial}{\partial x}(f + g) = \tfrac{\partial f}{\partial x} + \tfrac{\partial g}{\partial x}$
(합에 대해 분배되고),
상수 $c$ 에 대해 $\tfrac{\partial}{\partial x}(cf) = c\,\tfrac{\partial f}{\partial x}$
(스칼라는 앞으로 빠진다). "$\tfrac{\partial}{\partial x}$ 를 적용한다"가 "숫자를 곱한다"가
따르는 것과 정확히 같은 장부 규칙을 따르기 때문에, 내적과 외적 대수의 모든 단계가 *곱하기*
대신 *적용하기*를 끼워 넣어도 그대로 통과한다. 선형성이 $\nabla$ 가 벡터로 행세할 수 있게
해주는 다리다.

**단 하나의 함정: 순서가 중요하다.** 보통의 숫자 곱셈은 교환된다 — $3\times 5 =
5\times 3$. 연산자의 적용은 교환되지 **않으며**, 형식적 벡터라는 위장을 조심스럽게 읽어야
하는 지점이 바로 여기다. 같은 기호를 두 가지로 배열해 비교해 보자.
$\tfrac{\partial}{\partial x}\,f$ 는 "$f$ 를 $x$ 에 대해 미분하라"는 뜻으로, 함수
$\tfrac{\partial f}{\partial x}$ 를 준다. 그러나 $f\,\tfrac{\partial}{\partial x}$ 는
"먼저 $f$ 를 곱한 뒤, 다음에 오는 것을 미분하라"는 뜻 — 여전히 연산자, 목적어를 기다리는
동사이지 완성된 함수가 아니다. 둘은 서로 다른 *종류의 대상*이다. 이런 모든 모호함을 해소하는
규칙은 간단하다: **$\nabla$ 는 항상 자기 오른쪽에 작용한다.** $\nabla$ 는 배가 고프고, 자기
뒤에 쓰인 장을 먹어치운다.

**세 가지 곱 — 그 보상.** 벡터는 정확히 세 가지 방식으로 곱해질 수 있고, $\nabla$ 는 그
셋을 모두 물려받는다. $f$ 를 스칼라 함수(점마다 숫자 하나를 내놓는 함수)라 하고,
$F = (F_1, F_2, F_3)$ 를 *벡터장(vector field)* (점마다 벡터 하나를 내놓는 것 — 예컨대
흐르는 유체의 속도)이라 하자. 그러면:

- **스칼라 곱.** 벡터 $\nabla$ 를 스칼라 $f$ 와 곱하면 각 성분이 스케일된다. 즉 각 편미분이
  $f$ 에 적용된다:
  $\nabla f = \left(\tfrac{\partial f}{\partial x},\ \tfrac{\partial f}{\partial y},\ \tfrac{\partial f}{\partial z}\right)$.
  이것이 **그레이디언트(gradient)** — $f$ 가 가장 빨리 증가하는 방향을 가리키는 벡터다.
  (그레이디언트는 같은 편미분들의 행 형태인 미분 $Df$ 를 열벡터로 전치한 것이다; 둘은 동일한
  정보를 담지만 반대 역할을 한다: $Df$ 는 방향을 먹는 사상이고, $\nabla f$ 는 그 자체가
  하나의 방향이다.)

- **내적.** [[vector-dot-product]] 는 대응하는 성분끼리 짝지어 더한다.
  $\tfrac{\partial}{\partial x}$ 를 $F_1$ 과 짝짓는다는 것은 *적용한다*는 뜻이므로,
  $\nabla\cdot F = \tfrac{\partial F_1}{\partial x} + \tfrac{\partial F_2}{\partial y} + \tfrac{\partial F_3}{\partial z}$.
  내적은 항상 숫자 하나를 돌려주므로 이것은 **스칼라** 장 — 각 점에서 장이 바깥으로 얼마나
  퍼져 나가는지를 재는 **발산(divergence)** 이다.

- **외적.** 두 벡터의 [[cross-product]] 는 성분들의 교차 차이로 만들어진 제3의 벡터를
  돌려준다. 곱하기 자리에 *적용하기*를 넣으면,
  $\nabla\times F = \left(\tfrac{\partial F_3}{\partial y} - \tfrac{\partial F_2}{\partial z},\ \ \tfrac{\partial F_1}{\partial z} - \tfrac{\partial F_3}{\partial x},\ \ \tfrac{\partial F_2}{\partial x} - \tfrac{\partial F_1}{\partial y}\right)$.
  외적은 벡터를 돌려주므로 이것은 **벡터** 장 — 장이 얼마나 빨리, 어느 축을 중심으로
  회전하는지를 재는 **컬(curl)** 이다.

연산자 하나, 곱셈 세 가지, 그리고 서로 다른 연산자 셋이 나온다. 이것이 이 엔진의 전부다.

**구체적 계산 예.** 3차원에서 $\nabla$ 를 써 보자:
$$\nabla = \left(\frac{\partial}{\partial x},\ \frac{\partial}{\partial y},\ \frac{\partial}{\partial z}\right).$$
구체적인 장 $F = (x,\ y,\ z)$ 를 잡자 — 모든 점에서 화살표가 원점으로부터 곧장 바깥을
가리키는, 팽창하는 기체 같은 장이다.

먼저 **$\nabla\cdot F$ 와 $F\cdot\nabla$ 가 서로 다른 종류의 대상**임을 보자. 짝짓고-적용하는
방식으로 $\nabla\cdot F$ 를 만들면: $\tfrac{\partial}{\partial x}$ 를 $F_1 = x$ 에 적용하면
$1$; $\tfrac{\partial}{\partial y}$ 를 $F_2 = y$ 에 적용하면 $1$;
$\tfrac{\partial}{\partial z}$ 를 $F_3 = z$ 에 적용하면 $1$. 더하면
$\nabla\cdot F = 1 + 1 + 1 = 3$ — 평범한 **숫자**다 (발산: 장이 어디서나 비율 $3$ 으로 퍼지고
있다). 이제 순서를 뒤집자. $F\cdot\nabla$ 는 $F_1 = x$ 를 $\tfrac{\partial}{\partial x}$ 와
*반대* 순서로 짝지어
$x\tfrac{\partial}{\partial x} + y\tfrac{\partial}{\partial y} + z\tfrac{\partial}{\partial z}$
를 준다 — 이것은 여전히 **연산자**, 아직 작용할 대상이 없는 동사다; 함수 $g$ 를 건네주면
$x\tfrac{\partial g}{\partial x} + y\tfrac{\partial g}{\partial y} +
z\tfrac{\partial g}{\partial z}$ 를 돌려준다. 그래서 $\nabla\cdot F$ (숫자) $\neq$
$F\cdot\nabla$ (연산자): 비가환성은 여기서 사소한 세부가 아니라, 답의 *타입*을 바꾼다.

이제 같은 $\nabla$ 를 세 가지 곱에 모두 통과시켜 그 가족이 나타나는 것을 보자. 스칼라
$f = x^2 + y^2 + z^2$ 를 잡는다.

- *그레이디언트(스칼라 곱):*
  $\nabla f = (2x,\ 2y,\ 2z)$ — 방사상 바깥을 가리키는 벡터, $f$ 의 오르막 방향.
- *발산(내적):* $\nabla\cdot F = 3$ — 위에서 계산한 스칼라.
- *컬(외적):* $F = (x, y, z)$ 를 쓰면, 첫 성분은
  $\tfrac{\partial F_3}{\partial y} - \tfrac{\partial F_2}{\partial z} = \tfrac{\partial z}{\partial y} - \tfrac{\partial y}{\partial z} = 0 - 0 = 0$,
  같은 상쇄로 나머지 두 성분도 $0$ 이어서 $\nabla\times F = (0,0,0)$
  — 벡터, 여기서는 영벡터이며, 순수하게 바깥으로만 뿜어져 나가는 장에는 회전이 없다는 것을
  말해 준다.

같은 기호 $\nabla$ 가 스칼라 곱, 내적, 외적을 통해 장과 결합하여 벡터, 스칼라, 벡터를 —
그레이디언트, 발산, 컬을 — 만들어냈다. 각각은 미분이 선형이기 때문에 정당한 결과이고, 각각은
$\nabla$ 가 자기 오른쪽에 작용하게 함으로써 읽힌다.

## 전제 조건

- [[partial-derivative]]
- [[vector-dot-product]]
- [[cross-product]]
## 출처

- `etc/differential-operators-summary.html` — "Reading ∇ correctly" ("곱하기"는
  *적용하기*를 뜻한다; 미분이 선형이기 때문에 $\nabla$ 는 *형식적 벡터*다;
  비가환성, $\nabla\cdot F \neq F\cdot\nabla$, $\nabla$ 는 오른쪽으로 읽는다), 그리고
  "The three products" (스칼라 곱 → 그레이디언트, 내적 → 발산, 외적 → 컬).
