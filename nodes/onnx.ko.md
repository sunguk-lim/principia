# ONNX (Open Neural Network Exchange)

## 요약

**ONNX(Open Neural Network Exchange)**는 기계학습 모델을 교환하기 위한 개방형이며
런타임에 독립적인 [[intermediate-representation]]이다. 형식이 지정된
[[computation-graph]]와 버전이 있는 [[operator-set]] 가져오기를 묶어, 한 도구에서
내보낸 모델을 다른 도구가 검증하고 실행하거나 변환할 수 있게 한다.

## 상세 설명

학습된 [[neural-network]]에는 매개변수와 순방향 계산이 있지만 학습 프레임워크마다 이를
다르게 저장할 수 있다. ONNX는 중간의 공통 계약을 정의한다. 모델은 IR 버전, 가져온
연산자 집합의 도메인과 버전, 메타데이터, [[computation-graph]]를 기록한다. 정점과 간선의
뼈대는 [[graph]]이고, 특수한 계산 의미는 이름이 붙은 입력과 출력, 연산 노드, 상수
매개변숫값, 노드 사이를 흐르는 값의 자료형 및 형상 정보에서 나온다.

각 구성 요소의 책임은 분명하다. [[computation-graph]]는 **어느 연산이 어느 이름의 값을
사용하는지** 나타낸다. 각 [[operator-set]] 가져오기는 **어느 공개 스키마가 그 연산의
의미를 정하는지** 나타낸다. [[intermediate-representation]]은 이 구성 요소와 메타데이터가
어떻게 결합되는지 정한다. 생산자는 내부 모델을 이 계약으로 내보내고, 소비자는 해석,
최적화, 변환 전에 IR과 연산자 집합 버전을 확인한다. ONNX는 실행 전략이 아니라 모델을
규정한다. 소비자는 [[computation-graph|계산 구조]]를 해석하거나 코드를 생성하거나 연산을 특수 하드웨어에 대응시킬
수 있다.

**구체적인 예.** `x = [2, 3]`, 행이 `[1, 4]`와 `[2, 5]`인 매개변수 `W`,
`b = [1, -3]`인 두 출력 아핀 계산 `y = xW + b`를 내보내자. ONNX [[computation-graph|계산 구조]]에는 `m`을
만드는 `MatMul` 노드와, `m`과 `b`를 받아들이는 `Add` 노드가 들어 있다.

1. `MatMul([2,3], W)`는 `m = [2×1 + 3×2, 2×4 + 3×5] = [8, 23]`을 만든다.
2. `Add(m, b)`는 `y = [8+1, 23-3] = [9, 20]`을 만든다.

파일은 `x`, `W`, `b`, `m`, `y`의 형상과 원소 형식, 그리고 `MatMul`과 `Add`를
정의하는 연산자 집합 버전도 기록한다. 두 번째 프레임워크는 생산자의 클래스나 소스 코드가
필요 없다. 공통 이름, 의존 관계, 자료형, 상수, 스키마를 이용해 같은 두 단계를 재구성한다.
이것이 교환 보장이다. 속도나 내부 배치까지 같다고 보장하지는 않으며, 이는 소비 런타임의
선택으로 남는다.

## 전제 조건

- [[intermediate-representation]]
- [[computation-graph]]
- [[operator-set]]
- [[neural-network]]
- [[graph]]

## 출처

- https://onnx.ai/onnx/intro/concepts.html
- https://onnx.ai/onnx/repo-docs/IR.html
- https://onnx.ai/onnx/repo-docs/Versioning.html
