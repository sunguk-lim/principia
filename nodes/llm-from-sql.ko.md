# SQL에서 LLM 호출하기

## 요약

**SQL에서 LLM 호출하기**란 모델 추론을 질의 안에서 부를 수 있는 평범한 [[sql]]
**함수**로 노출하는 것을 뜻한다. 언어 모델이 별도의 애플리케이션 서비스 뒤에
사는 대신, 데이터베이스가 `ai.openai_chat_complete(model, prompt)` — 프롬프트를
대규모 언어 모델에 보내고 그 텍스트 답변을 돌려받는 **생성(generative)** 호출 —
과 `ai.openai_embed(model, text)` — 텍스트의 [[embedding]]을 돌려주는 호출 —
같은 함수를 제공한다. 이것들은 그저 [[sql]] 함수이므로 [[sql]]이 이미 하는
모든 것과 합성된다: 단일 `SELECT`나 `UPDATE`가 모델을 **행마다 한 번씩** 실행할
수 있어서, 테이블을 읽는 바로 그 문장이 그 행들을 분류하고, 요약하고, 번역하고,
임베딩할 수 있다. 그리고 [[retrieval-augmented-generation]]의 *검색(retrieval)*
절반은 그 자체로 [[sql]] 질의이므로, 검색-후-생성(retrieve-then-generate) 루프
전체를 한 문장으로 쓸 수 있다 — 모델 호출이 행들을 서비스로 실어 나갔다가 다시
실어 오는 외부 파이프라인에 앉아 있는 대신 질의 *안으로* 들어오는 것이다.

## 상세 설명

### "SQL 함수로서의 모델"이 뜻하는 것

[[retrieval-augmented-generation]]이 사용하는 의미에서 언어 모델은 텍스트
프롬프트에서 생성된 텍스트로 가는 함수다: 프롬프트를 건네면 프롬프트에 담긴
문맥에 근거하여 답변을 만들어낸다. 보통 그 함수는 애플리케이션 코드가 네트워크
너머로 접근한다. **SQL에서 LLM 호출하기**는 그 *호출 지점(call site)*을 옮긴다:
데이터베이스가 함수들을 등록해 두고, 평가될 때 모델 제공자(OpenAI, 로컬에서
도는 Ollama, Cohere, …)에 접속하여 결과를 [[sql]] 값으로 돌려준다. 검색 스택이
필요로 하는 두 가지 모델 출력에 대응하는 두 계열이 중요하다:

- **생성** — `ai.openai_chat_complete(model, prompt)`는 모델의 텍스트 완성을
  돌려준다. 이것이 [[retrieval-augmented-generation]]의 생성 언어 모델이며,
  이제 질의 안에서 호출 가능하다.
- **임베딩** — `ai.openai_embed(model, text)`는 [[embedding]]을 돌려준다: 입력
  텍스트의 조밀한 의미 벡터다. 이것은 유사도 검색에 앞서 문서와 질문을 벡터로
  바꿔야 하는 바로 *그* 연산이다.

[[sql]] 함수는 질의가 건드리는 행들에서 **행마다** 평가되므로, 이 호출들 중
하나를 `SELECT` 목록이나 `UPDATE ... SET`에 감싸 넣으면 손으로 쓴 루프 없이
테이블 전체에 모델이 적용된다 — 반복은 [[sql]] 엔진이 한다.

### 왜 모델 호출을 질의 안으로 옮기는가 — 하중을 받치는 아이디어

요점은 문법의 신기함이 아니라 **왕복 파이프라인의 제거**다. 모델로 행을 보강하는
통상적인 방법은 이렇다: 애플리케이션 코드가 행들을 `SELECT`하고, 각 행을 모델
서비스로 실어 보내고, 기다리고, 답을 `UPDATE`로 되쓴다. 그 파이프라인은 추가
코드이고, 추가 장애 표면이며, 모든 행을 프로세스 경계 너머로 두 번 끌고 다닌다.
모델을 [[sql]] 함수로 만들면 그것이 무너져 합쳐진다:

- **데이터 지역성.** 행들은 처리되기 위해 데이터베이스를 떠나지 않는다; 이미
  행들을 손에 쥔 질의가 그 행들에 대해 모델도 호출한다. 보강(enrichment)이
  데이터 계층의 속성이 되고, 다른 모든 것과 같은 [[sql]]로 표현된다.
- **[[sql]]과의 합성 가능성.** 모델 호출은 표현식이므로 `WHERE`, `SELECT`,
  `UPDATE`, 조인, 집계에 끼워 넣을 수 있다. 필터가 선택한 행만 분류할 수도
  있고, 생성된 텍스트를 곧바로 컬럼에 쓸 수도 있다.
- **RAG가 한 곳에.** [[retrieval-augmented-generation]]은 *관련성이 가장 높은
  상위 `k`개의 청크를 검색하고, 그것들을 조건으로 답을 생성한다*는 것이다.
  검색이 [[sql]] 유사도 질의이고 생성이 [[sql]] 함수일 때, 두 절반이 모두
  데이터베이스 안에 산다: 한 문장이 가장 가까운 청크들을 선택하고, 이어 붙여
  프롬프트를 만들고, 그 프롬프트를 생성 호출에 넘길 수 있다 —
  [[retrieval-augmented-generation]]이 기술하는 루프 전체가, 외부 오케스트레이터
  없이.

비용도 실재하고 언급할 가치가 있다: 각 호출은 **모델 제공자로 가는 네트워크
요청**이고(보통의 [[sql]]에 비해 느리고 속도 제한이 있다), 대개 토큰당 돈이
들며, 실패하거나 타임아웃될 수 있다 — 그래서 백만 행 테이블에 대해 단일
트랜잭션 안에서 이를 돌리는 것은 흔히 잘못된 모양이다(이것이 바로 대량 임베딩을
인라인이 아니라 관리되는 백그라운드 작업으로 하도록 압박하는 바로 그 요인이다).

### 동작 예시 — 질의 하나가 보강을 해낸다

애플리케이션 코드 없이, 제자리에서 모든 리뷰의 감성을 분류하기:

```sql
SELECT id,
       ai.openai_chat_complete(
         'gpt-4o-mini',
         'Reply with POSITIVE or NEGATIVE only. Review: ' || body
       ) AS sentiment
FROM reviews
WHERE created_at > now() - interval '1 day';
```

추적해 보자. `FROM reviews WHERE ...`는 평범한 [[sql]]이다 — 어제의 행들을
선택한다. 선택된 **각** 행에 대해 [[sql]] 엔진은 `SELECT` 목록의 표현식을
평가하는데, 이는 고정된 지시문과 그 행의 `body`를 이어 붙여 프롬프트를 만들고
생성 모델 호출에 넘긴다; 함수는 모델의 텍스트(`POSITIVE`/`NEGATIVE`)를 돌려주고,
그것이 그 행의 `sentiment` 값이 된다. 한 문장, 일치하는 행마다 한 번의 모델
호출, 결과는 평범한 결과 집합으로 — 내보내기도 없고, 되쓰기 스크립트도 없다.

임베딩 쪽도 같은 모양으로, 벡터를 컬럼에 써 넣는다:

```sql
UPDATE documents
SET embedding = ai.openai_embed('text-embedding-3-small', body)
WHERE embedding IS NULL;             -- embed only rows not yet embedded
```

여기서 모델 호출은 [[embedding]]을 돌려주고 `UPDATE`가 그것을 `vector` 컬럼에
저장하므로, 나중에 유사도 검색이 순위를 매길 바로 그 행들이 [[sql]] 문장 하나로
채워진다. 이 둘을 합쳐 보자 — [[embedding]] 유사도로 가장 가까운 청크들을
검색하는 내부 질의와, 그 청크들을 프롬프트로 받아먹는 외부 생성 호출 — 그러면
[[retrieval-augmented-generation]]이 단일 [[sql]] 질의로 표현된다. 검색-후-생성
파이프라인이 질의 그 자체로 무너져 합쳐지는 것, 그것이 "SQL에서 LLM 호출하기"가
기여하는 바다.

## 선행 개념

- [[sql]] — 인터페이스이자 합성의 매체: 모델 추론이 행마다 평가되는 [[sql]]
  함수로 노출되므로 `SELECT`/`UPDATE`/`WHERE`에 끼워지고, 엔진이 손으로 쓴
  반복 없이 테이블 전체에 모델을 적용한다.
- [[retrieval-augmented-generation]] — 채팅 완성 호출이 부르는 생성 언어
  모델(프롬프트 → 텍스트)을 공급하며, [[sql]] 안에서 모델 호출을 원하게 만드는
  대표적 이유: 그 검색-후-생성 루프가 두 절반이 모두 [[sql]]일 때 데이터베이스
  내부의 단일 질의가 된다.
- [[embedding]] — 임베딩 모델 호출(`ai.*_embed`)의 출력: 같은 문장이 계산하고
  저장할 수 있는 조밀한 의미 벡터로, 유사도 검색에 먹인다.

## 출처

- pgai — https://github.com/timescale/pgai (OpenAI, Ollama, Cohere 등에 걸쳐 SQL에서 LLM 및 임베딩 모델 호출).
- pgai 모델 호출 문서 — https://github.com/timescale/pgai/blob/main/docs/model_calling/openai.md (`ai.openai_chat_complete`, `ai.openai_embed` 및 관련 SQL 함수).
