# OpenTelemetry

## 요약

**OpenTelemetry**(OTel)는 관측 가능성 데이터를 생성하고, 연관 짓고, 수집하고, 내보내기
위한 공급자 중립 명세이자 도구 모음이다. [[observability-instrumentation]]에서 백엔드
전달까지의 경로를 표준화하지만, 데이터를 저장하거나 시각화하는 백엔드는 의도적으로
제공하지 않는다.

## 상세 설명

OTel이 푸는 문제는 파편화다. 공통 계약이 없으면 애플리케이션이 한 공급자의 트레이싱
API, 다른 메트릭 라이브러리, 별도 로깅 형식, 백엔드 전용 익스포터를 함께 쓸 수 있다.
백엔드를 바꾸려면 관찰 코드도 다시 작성해야 한다. OpenTelemetry는 공통 API, 언어 SDK
동작, 데이터 모델, 의미 필드 이름, OTLP 전송을 정의해 생성 방식과 목적지가 독립적으로
바뀔 수 있게 한다.

흐름은 [[observability-instrumentation]]에서 시작한다. 수동 API 호출이나 자동 라이브러리
훅이 애플리케이션 활동을 [[telemetry-signal]] 데이터로 바꾼다. 주된 관점은 스팬으로
만드는 [[distributed-tracing]] 경로, [[telemetry-metric]] 집계, [[log-record]] 발생이다.
공유 [[telemetry-context]]가 현재 작업을 식별하고, [[context-propagation]]이 선택한
식별자를 서비스 경계 너머로 옮겨 서로 다른 프로세스의 신호를 연관 짓게 한다.

Frontend와 Payment를 지나는 결제 요청을 따라가 보자. Frontend 계측이 trace `T`, span
`A`를 시작하고 요청 카운터를 기록한 뒤 Payment를 호출한다. 전파는 나가는 요청에
`T/A`를 주입한다. Payment는 이를 추출해 자식 span `B`를 만들고 카드가 거절되면 오류
로그를 내보낸다. 모든 레코드가 표준 필드 의미를 쓰므로 결합할 수 있다. 카운터는 요청량,
트레이스는 180ms Payment 경로, 로그는 140ms 시점의 거절 이유를 보여 준다.

SDK 익스포터가 백엔드로 직접 보낼 수도 있지만 운영 시스템은 흔히 OTLP를
[[opentelemetry-collector]]로 보낸다. 리시버가 신호를 받고, 프로세서가 배치하거나
민감 정보를 지우며, 익스포터가 하나 이상의 백엔드로 라우팅한다. 백엔드를 바꿀 때
애플리케이션 계측 대신 Collector와 익스포터 설정을 바꾼다. 이것이 공급자 중립 불변식이다.
생산자가 표준 텔레메트리를 소유하고 목적지는 교체 가능하다.

따라서 OpenTelemetry는 [[observability]]를 가능하게 하지만 그 자체가 관측 가능성
백엔드는 아니다. 증거를 만들고 옮기며, 다른 시스템이 그 증거를 저장·질의·경고·시각화한다.

## 전제 조건

- [[observability]]
- [[telemetry-signal]]
- [[observability-instrumentation]]
- [[distributed-tracing]]
- [[telemetry-metric]]
- [[log-record]]
- [[telemetry-context]]
- [[context-propagation]]
- [[opentelemetry-collector]]

## 출처

- https://opentelemetry.io/docs/what-is-opentelemetry/
- https://opentelemetry.io/docs/specs/otel/
