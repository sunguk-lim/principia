# 손실 함수

## 요약

**손실 함수(loss function)**는 "모델이 얼마나 틀렸는가?"를 최소화할 수 있는
하나의 숫자로 바꾼다.

## 상세 설명

손실 함수는 모델의 파라미터 $\theta$를, 예측값과 목표값으로부터 계산된
음이 아닌 오차(합, 차, 곱 — [[arithmetic]])로 대응시킨다:

$$\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^{N} \ell\big(f_\theta(x_i),\, y_i\big)$$

여기서 $\ell$은 하나의 예측을 그 목표값과 비교해 점수를 매긴다. 학습이란
$\mathcal{L}$을 작게 만드는 $\theta$를 찾는 탐색이며, 그 그래디언트가
gradient-descent에 어느 방향으로 움직일지 알려준다.

**손실이 어디서 오는가.** $\ell$을 원칙에 따라 고르면 [[maximum-likelihood-estimation]]에서
자연스럽게 도출된다: **교차 엔트로피(cross-entropy)** 손실은 목표값들의
**음의 로그-[[likelihood]]**이므로, 이를 최소화하는 것은 곧 데이터의
가능도(likelihood)를 최대화하는 것과 *정확히* 같다 —
$\mathcal{L}(\theta) = -\frac{1}{N}\sum_{i} \log p_\theta(y_i \mid x_i)$.
(평균제곱오차도 가우시안 노이즈 가정 아래에서는 같은 이야기다.) 그러므로
"최대 가능도로 적합시킨다"와 "이 손실을 최소화한다"는 하나의 목적을 두
측면에서 바라본 것일 뿐이다.

## 선행 지식

- [[arithmetic]]
- [[likelihood]]
- [[maximum-likelihood-estimation]]

## 출처

_없음_
