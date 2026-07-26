# 신경망 (Neural Network)

## 요약

**신경망(neural network)**은 선형 변환(linear transformation)과 단순한
비선형성(nonlinearity)을 번갈아 쌓아 레이어로 구성함으로써 입력을
출력으로 매핑한다.

## 상세 설명

각 레이어는 입력에 가중치 행렬을 곱하고 ([[matrix-multiplication]]),
편향(bias)을 더한 뒤, 비선형 함수 $\sigma$를 적용한다:

$$h^{(l)} = \sigma\!\big(W^{(l)} h^{(l-1)} + b^{(l)}\big)$$

레이어를 쌓는 것은 이 매핑들을 합성하는 것이며, 출력 레이어는 흔히
확률을 만들어내기 위해 [[softmax]]를 사용한다. 가중치 행렬 $W^{(l)}$은
훈련 중 학습되는 **파라미터**다 — 그리고 이것이 바로
transformer-attention이 만들어지는 재료이며 lora가 적응시키는 대상이다.

## 전제 조건

- [[matrix-multiplication]]
- [[softmax]]

## 출처

_없음_
