# 문맥 전파

## 요약

**문맥 전파(context propagation)**는 프로세스나 서비스 경계를 넘어 상관관계 정체성을
옮긴다. 송신자는 [[telemetry-context]]에서 선택한 필드를 전송 매개체에 직렬화하고,
수신자는 작업을 시작하기 전에 그 필드를 추출해 자기 로컬 문맥을 파생한다.

## 상세 설명

매개체(carrier)는 전송 계층이 메시지와 함께 보낼 수 있는 공간이다. [[http]]에서는
보통 요청 헤더다. OpenTelemetry의 기본 W3C Trace Context 표현은 버전, 트레이스 ID,
부모 스팬 ID, 플래그를 담는 `traceparent` 헤더를 쓴다. 주입(injection)은 현재
식별자를 헤더에 쓰고, 추출(extraction)은 수신 경계에서 읽고 검증한다.

Frontend 서비스가 trace ID `7fa1`, 현재 span ID `a10c`를 가진 채 Inventory를
호출한다고 하자. 단순화한 `traceparent: 00-7fa1-a10c-01` 헤더를 보낸다. Inventory는
trace ID와 원격 부모를 추출한 뒤 새 ID `b205`를 가진 로컬 스팬을 시작한다. 관계는
trace `7fa1`, parent `a10c`, child `b205`가 된다. 전파가 없으면 Inventory가 새 trace
ID를 만들어 한 사용자 요청의 두 절반이 서로 무관해 보인다.

전파는 보통 비즈니스 로직이 아니라 송신·수신 경계의 계측이 수행한다. 들어오는 문맥은
신뢰할 수 없는 입력으로 다뤄야 한다. 잘못된 식별자는 무시하고 민감한 배기지는 외부
서비스로 보내지 않아야 한다. 이 메커니즘은 상관관계를 보존할 뿐 권한을 부여하지 않는다.

## 전제 조건

- [[telemetry-context]]
- [[http]]

## 출처

- https://opentelemetry.io/docs/concepts/context-propagation/
