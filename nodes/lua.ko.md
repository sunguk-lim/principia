# Lua

## 요약

Lua는 무엇보다도 더 큰 호스트 프로그램 — 게임 엔진, 웹 서버, 텍스트 에디터 — 안에 그 설정·스크립팅 계층으로 **임베드**(embed)되도록 설계된, 작고 빠른 스크립팅 언어다. 언어의 모든 면이 그 목표에 봉사한다: 아주 작은 구현, 그리고 수많은 특수 기능 대신 어디서나 재사용되는 소수의 개념들. 유일한 자료 구조는 **테이블**(table)로, 배열·레코드·객체·모듈을 겸하는 [[hash-map]]이다. Lua는 **[[dynamic-typing|동적 타입]]**이고(값이 타입을 지니고, 변수는 무엇이든 담는다) **[[garbage-collection|가비지 컬렉션]]**을 갖춘다(수동 메모리 관리가 없다). 함수는 **[[closure]]**를 이루는 일급 값이어서, 내장 클래스 없이도 함수형·객체 관용구를 제공한다. **[[coroutine]]**은 협력적 멀티태스킹을 핵심 기능으로 제공한다. **[[metatable]]**은 테이블이 자신의 동작을 커스터마이즈하게 해 주어, 연산자 오버로딩과 상속이 별도의 객체 시스템이 아니라 테이블 메커니즘에서 자연히 따라 나온다. 그리고 참조 구현은 소스를 바이트코드로 컴파일해 레지스터 기반 **[[bytecode-vm]]** 위에서 실행한다 — 그 유명한 소형·고속성 덕에, 작고 빠르고 이식성 있는 런타임이 중요한 곳에서 Lua가 스크립팅 언어의 첫 선택이 된다.

## 상세 설명

**Lua는 *무엇*이며, 그 성격을 빚은 설계 목표.** Lua는 가볍고 이식성 있는 스크립팅 언어이며, 그 정의적 목적은 *임베드 가능성*(embeddability)이다: 다른 언어로 작성된 호스트 애플리케이션 안에 심어져 그것을 스크립팅하는 데 쓰이도록 만들어졌다. 그 하나의 목표가 언어의 성격을 설명한다 — 구현은 작고 자기 완결적이며, 기능을 쌓아 올리는 대신 소수의 강력한 개념을 어디서나 재사용한다. Lua의 정체성은 아래 특성들의 특정한 *조합*으로 이해하는 것이 가장 좋다. 각 특성은 Lua가 전면적으로 채택한 일반적인 언어 아이디어다.

**단 하나의 자료 구조 — 테이블.** Lua의 유일한 내장 자료 구조는 테이블이다: 키에서 값으로 가는 [[hash-map]]. 연속된 정수 키를 가진 테이블은 배열이고; 문자열 키를 가지면 레코드나 모듈이며; [[metatable]]이 붙으면 객체다. 이 "구조 하나" 결정이 언어가 작게 유지되는 이유다 — 배워야 할 별도의 배열, 구조체, 클래스 구문이 없고, 그저 테이블을 서로 다른 방식으로 쓸 뿐이다.

**확장 가능한 동작 — 메타테이블.** 테이블의 동작은 [[metatable]]을 붙여 커스터마이즈할 수 있다. 연산자 오버로딩, 기본값, 프로토타입식 상속(메타테이블의 `__index` 폴백을 통한)이 모두 이 하나의 메커니즘으로 제공되므로, Lua에는 전용 클래스 시스템이 필요 없다: 객체 지향은 언어 키워드가 아니라 테이블과 [[metatable]] 위에 세워진 *관례*다.

**값과 메모리 — 동적 타입과 가비지 컬렉션.** Lua는 [[dynamic-typing|동적 타입]] 언어다: 타입(nil, boolean, number, string, function, table, 그리고 몇 가지 더)이 값과 함께 다니며, 어떤 변수든 그중 무엇이든 담을 수 있다. 메모리는 점진적(incremental) 마크 앤 스위프 [[garbage-collection|가비지 컬렉터]]가 자동으로 관리한다 — 사용자 중 상당수가 시스템 프로그래머가 아니어서 손으로 메모리를 회수해서는 안 되는 임베디드 스크립팅 계층에는 결정적인 특성이다.

**함수와 제어 — 클로저와 코루틴.** Lua의 함수는 일급 값이며, 그 스코핑과 결합하여 [[closure]]를 이룬다 — 주변 지역 변수(*업밸류(upvalue)*)를 포획하는 함수로, 콜백과 테이블-클로저 스타일의 객체를 뒷받침한다. 일반적인 호출을 넘어서는 제어 흐름을 위해 Lua는 [[coroutine]]을 내장한다: 협력적으로 yield/resume하는 루틴으로, 제너레이터·이터레이터·협력적 스케줄러를 손쉽게 만들어 준다.

**어떻게 실행되고, 어떻게 임베드되는가.** 참조 구현은 소스 텍스트를 직접 해석하지 않는다; 각 청크를 바이트코드로 컴파일해 **레지스터 기반** [[bytecode-vm]] 위에서 실행한다. (스택 기반이 아닌) 레지스터 기반 설계는 Lua의 속도에 대해 널리 인용되는 이유다. 존재 이유(raison d'être)인 임베드 가능성은 작은 C API를 통해 이뤄지는데, 이를 통해 호스트 프로그램과 Lua가 값을 주고받고 서로의 함수를 호출한다; 그 API가 Lua를 C나 C++ 애플리케이션 안의 스크립팅 계층으로 만들어 주는 것이다. (그 C 경계의 세부 동작은 이 노드의 범위를 벗어난다.)

**구체적인 작동 예시.** 특성들을 한꺼번에 사용하는 짧은 프로그램 — [[metatable]]을 통해 객체로 쓰이는 테이블, 자동 메모리 관리, 그리고 [[coroutine]]:

```lua
Account = {}
Account.__index = Account                       -- misses delegate here (metatable)
function Account.new(b) return setmetatable({balance = b}, Account) end
function Account:deposit(x) self.balance = self.balance + x end

a = Account.new(100)   -- a is a table; when it becomes unreachable, GC frees it
a:deposit(50)          -- 'deposit' missing on a → __index → found in Account
print(a.balance)       -- 150   (balance is a dynamically typed number)

-- a coroutine as a generator
gen = coroutine.wrap(function() for i = 1, 3 do coroutine.yield(i) end end)
print(gen(), gen(), gen())   -- 1  2  3
```

각 특성이 어디에 나타나는지 따라가 보자: `a`는 테이블, 즉 [[hash-map]]이다; `setmetatable`이 [[metatable]]을 붙여서, 없는 `deposit` 키가 `__index` 위임을 통해 `Account`에서 해석된다; `balance`는 [[dynamic-typing]] 아래에서 숫자를 담고 있으며, 같은 필드가 나중에 다른 타입의 값을 담을 수도 있다; `Account.new`와 `deposit`은 *테이블에 값으로 저장된* 함수이고, 각각은 주변 지역 변수들에 대한 [[closure]]를 이룰 수 있다; `a`가 더 이상 도달 불가능해지면 명시적 해제 없이 [[garbage-collection]]이 회수한다; `gen`은 세 번의 호출에 걸쳐 `1, 2, 3`을 yield하며 그 사이 루프 위치를 기억하는 [[coroutine]]이다; 그리고 청크 전체가 바이트코드로 컴파일되어 레지스터 기반 [[bytecode-vm]]에 의해 실행된다. 이 예시가 퇴화하지 않은(non-degenerate) 이유는 선언된 모든 선수 지식 — 테이블, 메타테이블, 동적 값, 일급 값, 가비지 컬렉션, 코루틴, VM — 을 한꺼번에 건드리기 때문이며, 그것이 바로 "Lua"의 *정체*다: 하나의 작은 언어 안에서의 그것들의 일관된 조합.

## 선수 지식

- [[bytecode-vm]]
- [[garbage-collection]]
- [[dynamic-typing]]
- [[closure]]
- [[coroutine]]
- [[metatable]]
- [[hash-map]]

## 출처

- lua-manual-5.4
- programming-in-lua
- lua-5.0-impl
