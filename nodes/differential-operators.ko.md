# 미분 연산자(Differential operators)

## 요약

그레이디언트(gradient), 발산(divergence), 컬(curl), 라플라시안(Laplacian),
야코비안(Jacobian), 헤시안(Hessian) — **여섯 개의 이름, 하나의 기계**:
[[del-operator]] $\nabla$ 를 가져다 어떤 곱을 통해 장(field)과 결합하고, 필요하면
합성한다.

## 상세 설명

이 가족 전체는 하나의 재료와 두 가지 동작에서 나온다:

- 장과의 **세 가지 곱**: 스칼라 곱 → [[gradient]] (스칼라→벡터),
  내적 → [[divergence]] ([[vector-field]]→스칼라), 외적 → [[curl]] (벡터장→벡터).
- **두 가지 합성 / 전체 도함수:** 그레이디언트 다음에 발산 → [[laplacian]]
  ($\nabla\cdot\nabla$); [[jacobian]] 은 [[differential]] 을 벡터값 함수로 일반화한 것
  (출력마다 행 하나)이고, [[hessian]] 은 그레이디언트의 야코비안이다.

이들 사이에서 달라지는 것은 출력의 **모양**뿐이다 — 열 하나, 합쳐진 셀 하나, 혹은
격자 전체 — 그리고 모든 개별 셀은 입력 성분들의 편미분 하나다. (이것이
differential-operators 아틀라스에서 설치된 "패키지"다.)

## 전제 조건

- [[del-operator]]
- [[gradient]]
- [[divergence]]
- [[curl]]
- [[laplacian]]
- [[jacobian]]
- [[hessian]]
- [[vector-field]]
- [[differential]]

## 그림

![여섯 미분 연산자의 아틀라스 — 각 연산자를 입력 → 출력 모양(스칼라 / 벡터 / 행렬)으로 표시|497](differential-operators.svg)

## 출처

- etc/differential-operators-summary.html
