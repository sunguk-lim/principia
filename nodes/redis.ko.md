# Redis (인메모리 자료구조 저장소)

## 요약

Redis(REmote DIctionary Server)는 **[[key-value-store]]**다: 그 중심에는 문자열 키를 값에
대응시키는 하나의 거대한 [[hash-map]] — *키스페이스(keyspace)* — 가 있고, 평균 O(1)의
get / set / delete를 제공한다. 두 가지 설계 선택이 이것을 단순한 딕셔너리 이상으로 만든다.
첫째, 키스페이스 전체가 **메모리 안에** 산다([[memory-hierarchy]]): 데이터셋이 디스크가 아니라
RAM에 상주하므로, 모든 연산이 밀리초 단위의 디스크 탐색이 아니라 나노초 지연의 메모리 작업이
된다. 둘째 — 이 시스템의 결정적 기여 — 값이 **불투명한 블롭(blob)이 아니라** 서버가 이해하고
**제자리에서(in place)** 변경하는 *타입 있는 자료구조*라는 점이다: 문자열, 리스트([[linked-list]]),
셋([[hash-set]]), 해시(중첩된 [[hash-map]]), 그리고 정렬 셋(sorted set). 클라이언트는 구조와
편집 내용을 지정하는 작은 명령 하나를 보내고, 서버는 그것을 서버 쪽에서 적용한 뒤 결과를
돌려준다. 단일 스레드가 한 명령을 끝까지 실행한 다음에야 다음 명령으로 넘어가므로, 모든 명령은
공짜로 [[atomic-operation]]이 된다.

## 상세 설명

### 무엇인가 — 타입 있는 구조들을 담은 hash-map인 키스페이스

Redis의 최상위 계층은 그 자체가 [[hash-map]]이다: 키(항상 문자열, 예: `"session:42"`) → 값.
이것이 "키-값 저장소"라는 이름과 평균 O(1) 조회를 부여한다. 반전은 **값 쪽**에 있다. 평범한
캐시에서 값은 통째로 `GET`하고 `SET`할 수만 있는 바이트 블롭이다. Redis에서 값은 **타입**을
지니며, 서버는 *그 타입에 대한* 연산을 노출한다:

| Redis 값 타입 | 기반 자료구조 | 예시 명령 | 서버가 하는 일 |
|---|---|---|---|
| 문자열 / 정수 | 바이트 문자열 | `INCR`, `SET`, `GET` | 덮어쓰기, 또는 제자리에서 파싱-후-1-더하기 |
| 리스트 | [[linked-list]] (이중 연결) | `LPUSH`, `RPOP` | 양쪽 끝에서 O(1) push/pop |
| 셋 | [[hash-set]] | `SADD`, `SISMEMBER` | 삽입 / 멤버십 검사, 중복 없음 |
| 해시 | 중첩된 [[hash-map]] | `HSET`, `HGET` | 한 키 *안의* 필드→값 맵 |
| 정렬 셋 | 점수 순 정렬 구조 | `ZADD`, `ZRANGE` | 멤버를 숫자 점수로 순위 유지 |

즉 데이터 모델은 재귀적이다: 키스페이스는 [[hash-map]]이고, 그 안의 *값 하나*가 다시
[[hash-map]](Redis 해시)일 수도, [[linked-list]](Redis 리스트)일 수도, [[hash-set]](Redis 셋)일
수도 있다. (정렬 셋은 스킵 리스트 + 점수의 [[hash-map]] 위에 만들어져 있다; 스킵 리스트는 여기서
부수적인 세부 사항이므로 선행 개념이 아니라 서술로만 남긴다.)

### 왜 동작하는가 — 세 가지 선택과 각각의 이유

**왜 인메모리인가.** 속도 이야기의 전부는 [[memory-hierarchy]]의 격차다: RAM 접근은 약 100 ns,
디스크 탐색은 약 10 ms — 다섯 자릿수 차이다. 작업 집합을 RAM에 두면 Redis는 모든 읽기와 쓰기를
메모리 연산으로 바꾸고, 지연 시간은 저장 장치가 아니라 네트워크 왕복(Redis는 TCP 위에서 단순한
요청/응답 프로토콜을 사용한다)이 지배하게 된다. 내구성(durability)은 그다음에 선택 사항으로
다시 붙는다 — RAM을 주기적으로 디스크 파일에 *스냅숏*하거나, 각 쓰기 명령을 재시작 시 재생할 수
있는 로그에 *추가*하는 방식 — 그래서 인메모리 저장소도 재부팅에서 살아남을 수 있다. (구체적인
파일 형식은 운영상의 참고 사항이지 개념이 아니므로 서술로만 남긴다.)

**왜 블롭 캐시가 아니라 자료구조 서버인가.** 작업 큐(job queue)를 유지한다고 하자. 블롭 값으로는
리스트 전체를 `GET`하고, 클라이언트에서 덧붙이고, 다시 `SET`해야 한다 — 세 단계, 전체 값이
회선을 두 번 건너고, 두 클라이언트가 서로를 덮어쓰는 창이 생긴다. Redis는 이것을 `LPUSH` 하나로
압축한다: [[linked-list]]가 서버 쪽에 살기 때문에 클라이언트는 *연산*과 새 원소만 보내고, 서버는
O(1)로 그것을 이어 붙인다. 구조의 지역성(서버 쪽)과 하나의 작은 명령 — 이것이 이득의 전부다.

**왜 단일 스레드가 버그가 아닌가.** Redis는 명령을 **하나의** 스레드에서, 한 번에 하나씩 끝까지
실행한다. 직관과 달리 이것은 장점이다: 락이 없고, 락 경합이 없고, 문맥 교환(context switch)
오버헤드가 없으며 — 결정적으로 — 각 명령이 *구성에 의해* [[atomic-operation]]이 된다.
`[[atomic-operation]]`은 원자성을 다른 어떤 연산도 끼어들 수 없는 분할 불가능한
읽기-수정-쓰기(read-modify-write)로 정의한다; Redis는 정확히 그 성질을 달성하되, 하드웨어
compare-and-swap이 아니라 *단일 스레드 위의 직렬화*를 통해 달성한다. 각 명령이 이미 메모리
속도로 빠르기 때문에 스레드 하나로 서비스를 포화시킬 수 있고, 락을 한 번도 고민하지 않고
원자성을 얻는다.

### 구체 예시 — 하나의 키스페이스, 한 세션의 명령들

빈 키스페이스(비어 있는 최상위 [[hash-map]])에서 시작해 다음을 순서대로 실행한다:

```
SET   session:42  "alice"      → keyspace now maps "session:42" → (string) "alice"
HSET  user:7  name alice age 30 → key "user:7" → a nested hash-map { name:"alice", age:"30" }
HGET  user:7  age              → "30"           (field lookup inside the value)
LPUSH jobs  "a"               → "jobs" → list [a]
LPUSH jobs  "b"               → list [b, a]     (LPUSH prepends at the head)
RPOP  jobs                    → "a", list now [b]   (pop the tail; O(1), it is a doubly [[linked-list]])
SADD  tags  redis db          → "tags" → set {redis, db}, returns 2 (two new members)
SADD  tags  db                → returns 0       ([[hash-set]] semantics: "db" already present, no dup)
SISMEMBER tags redis          → 1
```

이제 원자성의 이득을 구체화해 보자. 두 클라이언트 **C1**과 **C2**가 같은 키의 페이지 뷰를 세려
하고, 시작 값은 `page:views = 0`이다:

- **클라이언트 쪽 읽기-수정-쓰기라면 생길 경쟁:** C1 `GET`→0, C2 `GET`→0, C1 `SET 1`, C2
  `SET 1`. 조회는 두 번인데 최종 값은 **1** — 갱신 하나가 사라졌다(lost update).
- **Redis `INCR`라면:** 각 클라이언트가 `INCR page:views` 하나씩을 보낸다. 단일 스레드가 이 둘을
  직렬화한다 — C1의 증가 0→1을 *끝까지* 실행한 뒤 C2의 1→2를 실행한다. 최종 값은 **2**로
  정확하며, 어디에도 락을 쓰지 않았다. `INCR`는 [[atomic-operation]]의 읽기-수정-쓰기가 단일
  스레드 규율에 의해 분할 불가능해진 것이다.

이 한 예시가 세 층위를 하나로 묶는다: **구조**(키스페이스는 [[hash-map]]이고 `page:views`의 값은
문자열-정수다), **알고리즘**(명령이 서버 쪽에서 구조를 변경하며 한 번에 하나로 직렬화된다),
그리고 **기반**(이 모든 것이 [[memory-hierarchy]]의 맨 위인 RAM에서 일어나므로 각 `INCR`는
나노초 몇 개에 불과하고 스레드는 디스크에 결코 막히지 않는다).

## 선행 개념

- [[hash-map]] — 키스페이스 그 자체이자 값 타입 중 하나(Redis 해시)
- [[memory-hierarchy]] — "인메모리"란 데이터셋이 RAM에 상주한다는 뜻; RAM 대 디스크의 격차가 속도의 원천
- [[linked-list]] — Redis 리스트 값 타입 (이중 연결 → 양 끝에서 O(1) push/pop)
- [[hash-set]] — Redis 셋 값 타입 (멤버십, 중복 없음)
- [[atomic-operation]] — 각 명령은 분할 불가능한 읽기-수정-쓰기이며, 여기서는 단일 스레드 직렬화로 달성

## 출처

- Redis data types — https://redis.io/docs/latest/develop/data-types/
