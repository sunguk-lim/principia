# 분산 트레이싱

## 요약

**분산 트레이싱(distributed tracing)**은 여러 프로세스를 통과하는 요청 하나의 경로를
연관된 [[trace-span]] 레코드로 복원한다. [[context-propagation]]은 원격 작업을 같은
인과 이력에 붙이는 데 필요한 식별자를 보존한다.

## 상세 설명

핵심 불변식은 단순하다. 한 요청의 모든 작업은 같은 트레이스 ID를 유지하고, 각 작업은
서로 다른 스팬 ID와 부모 ID를 가진다. 결과는 단순한 시간순 목록이 아니다. 시계가
겹쳐도 어떤 작업이 어떤 작업을 호출했는지 보여 주는 인과 트리다.

결제 요청 하나를 따라가 보자. Frontend가 0–230ms 동안 루트 스팬 `A`를 만든다.
20–80ms에는 Inventory를 호출해 스팬 `B`가 실행되고, 90–220ms에는 Payment를 호출해
스팬 `C`가 실행된다. [[context-propagation]]이 `A`의 정체성을 각 서비스로 옮기므로 두
원격 [[trace-span]] 레코드는 trace ID `T`를 공유하고 `A`를 부모로 기록한다. 조립된
트레이스는 `A → {B, C}`다. Payment가 110–180ms에 데이터베이스 스팬 `D`를 만들면 그
가지에서는 `A → C → D`가 된다.

이 구조는 지연 위치를 찾게 해 준다. 전체 요청은 230ms, Inventory는 60ms, Payment는
130ms, Payment의 데이터베이스 자식은 70ms를 썼다. 평평한 로그도 네 지속 시간을
보여 줄 수 있지만 부모-자식 관계를 스스로 증명하지는 못한다. 전파된 ID가 그 관계를
명시하고 백엔드가 여러 머신을 가로지르는 종단 간 폭포 그림을 만들게 한다.

## 전제 조건

- [[trace-span]]
- [[context-propagation]]

## 출처

- https://opentelemetry.io/docs/concepts/signals/traces/
