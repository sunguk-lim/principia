# 트랜스포머 어텐션

## 요약

**어텐션(attention)**은 각 토큰이 *값(value)* 벡터들의 가중 평균을 취해
문맥을 반영한 표현을 만들도록 해주는데, 그 가중치는 해당 토큰의 *질의
(query)*가 각 *키(key)*와 얼마나 잘 맞는지에서 나온다.

## 상세 설명

스케일드 닷프로덕트 어텐션(scaled dot-product attention)은 다음과
같다:

$$\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right) V$$

이를 전제 개념을 통해 읽어보자:

- 각 질의-키 유사도는 하나의 [[vector-dot-product]]이며; 이들 전부를
  한 번에 계산하는 것이 바로 [[matrix-multiplication]] $Q K^{\top}$로,
  $n\times n$짜리 점수 행렬을 준다.
- $\sqrt{d_k}$로 나누는 것은 점수가 차원 수에 따라 커지지 않도록
  막아준다(그래서 [[softmax]]의 그래디언트가 건강하게 유지된다).
- [[softmax]]는 점수 행렬의 각 행을 양수이고 합이 1인 가중치로
  바꾼다.
- 그 가중치들을 $V$에 곱하는 것은(다시 [[matrix-multiplication]])
  각 토큰에 대해 모든 값 벡터의 가중 평균을 취하는 것이다.

이것이 LoRA가 적응시키는 가중치 행렬이다: 실제로는 $W_q, W_k, W_v,
W_o$가 $Q, K, V$와 출력을 만들어내는 투영(projection)이며 — lora는
보통 자신의 저랭크 업데이트를 $W_q$와 $W_v$에 주입한다.

## 전제 조건

- [[softmax]]
- [[vector-dot-product]]
- [[matrix-multiplication]]

## 시각 자료

**1 · 기호** — 🟦 스칼라 · 🟩 벡터 · 🟧 행렬

| 기호 | 종류 | 형태 | 의미 |
|--------|------|-------|---------|
| $Q$ | 🟧 행렬 | $n\times d_k$ | 질의(토큰당 한 행) |
| $K$ | 🟧 행렬 | $n\times d_k$ | 키 |
| $V$ | 🟧 행렬 | $n\times d_v$ | 값 |
| $Q K^{\top}$ | 🟧 행렬 | $n\times n$ | 유사도 점수(모든 토큰 대 모든 토큰) |
| $O$ | 🟧 행렬 | $n\times d_v$ | 출력(문맥이 섞인 값) |
| $d_k$ | 🟦 스칼라 | — | 키/질의 차원($\sqrt{d_k}$ 스케일을 정한다) |
| $n$ | 🟦 스칼라 | — | 토큰 개수 |

**2 · 수식**

$$\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right) V$$

**3 · 형태**

![어텐션 파이프라인: Q와 K-전치를 곱해 n x n 점수 행렬을 얻고, softmax로 각 행을 정규화한 다음, V를 곱해 n x d_v 출력을 얻는다](transformer-attention.svg)

## 출처

_없음_
