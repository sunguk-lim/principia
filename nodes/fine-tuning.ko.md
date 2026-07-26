# 파인튜닝

## 요약

**파인튜닝(fine-tuning)**은 이미 학습된 모델을 새 데이터로 계속 학습시켜, 특정
작업(task)에 맞게 적응시키는 과정이다.

## 상세 설명

먼저 대규모 범용 말뭉치(corpus)에서 가중치를 이미 학습한(사전학습, pretraining)
[[neural-network]]에서 시작한다. 그 다음 작업 특화 데이터에 대해 추가로
[[gradient-descent]] 스텝을 실행하여 가중치를 갱신한다.

$$\theta \leftarrow \theta - \eta\,\nabla \mathcal{L}_{\text{task}}(\theta)$$

*전체(full)* 파인튜닝은 **모든** 가중치를 갱신한다 — 정확하지만 비용이 크다.
모든 파라미터를 복사하고 저장하고 최적화해야 하기 때문이다. lora가 없애는
것이 정확히 이 비용이다: lora는 사전학습된 가중치를 고정(freeze)하고 작은
저랭크(low-rank) 업데이트만 학습하므로, 거대한 모델의 파인튜닝이 저렴해진다.

## 선행 지식

- [[gradient-descent]]
- [[neural-network]]

## 출처

_없음_
