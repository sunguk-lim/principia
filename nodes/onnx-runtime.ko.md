# ONNX Runtime

## 요약

**ONNX Runtime**은 [[onnx]] 모델을 불러오고, [[graph-optimization]]을 적용하고,
지원되는 작업을 [[execution-provider|실행 공급자]] 사이에 분할한 뒤, 하나의 일관된 API로
결과 실행 계획을 수행하는 크로스 플랫폼 모델 가속기다.

## 상세 설명

ONNX는 이식 가능한 모델을 규정하지만 명세 자체가 메모리를 할당하거나 하드웨어를 고르거나
연산을 실행하지는 않는다. ONNX Runtime이 그 실행 계층을 제공한다. 애플리케이션이 세션을
만들면 런타임은 [[onnx]] 계약을 검증하고, 메모리 안에 [[graph]]를 만들고, 공급자와 무관한
[[graph-optimization]]을 적용한 뒤, 등록된 [[execution-provider|실행 공급자]]에 어느
영역을 실행할 수 있는지 묻는다. 공급자 우선순위에 따라 영역을 할당하고 지원되지 않는
노드는 기본 CPU 공급자에 남긴다.

분할 후에는 공급자별 최적화가 이미 백엔드에 할당된 영역을 융합하거나 다시 배열할 수 있다.
그런 다음 런타임은 의존 관계에 따라 노드 순서를 정하고, 중간값을 할당하고, 각 공급자의
구현을 호출하고, 간선이 공급자 경계를 넘을 때 값을 이동하는 실행 계획을 만든다. 불러오기와
계획 수립은 세션마다 한 번 수행되고, 반복 호출은 준비된 계획에 새 입력을 제공한다.

**구체적인 예.** `MatMul → Add`로 표현된 ONNX 계산 `y = xW + b`를 불러오고 공급자를
가속기, CPU 순서로 등록하자. 가속기가 두 노드를 모두 가져가면 런타임은 전체 경로를
가속기에 할당하고 두 연산을 융합할 수 있다. 가속기가 `MatMul`만 가져가면 그 노드는
가속기에서 실행되고 출력은 CPU 공급자로 전달되며 `Add`가 마무리한다. `x = [2, 3]`,
`W`의 행이 `[1, 4]`와 `[2, 5]`, `b = [1, -3]`이면 두 유효한 계획 모두 `[9, 20]`을
반환해야 한다. 공급자 선택은 지연 시간과 데이터 이동을 바꿀 수 있지만 모델이 정의한
결과는 바꾸지 않는다.

이 구조는 이식성과 가속을 분리한다. 같은 [[onnx]] 파일과 세션 API가 서버 CPU, GPU
라이브러리, 엣지 가속기를 대상으로 삼을 수 있으며 설치된 공급자가 구체적인 계획을 정한다.
따라서 ONNX Runtime은 학습 프레임워크도 ONNX 형식 자체도 아니다. 그 형식을 검증하고
효율적으로 실행하는 재사용 가능한 엔진이다.

## 전제 조건

- [[onnx]]
- [[graph-optimization]]
- [[execution-provider]]
- [[graph]]

## 출처

- https://onnxruntime.ai/docs/
- https://onnxruntime.ai/docs/reference/high-level-design.html
- https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html
