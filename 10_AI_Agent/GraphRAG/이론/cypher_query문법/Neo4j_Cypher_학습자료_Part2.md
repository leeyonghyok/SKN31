# Neo4j Cypher 마스터하기 — Part 2

> Part 1의 12개 기초 구문을 익힌 학습자를 위한 **실무 필수 심화 자료**

> 💡 본 자료의 모든 문제는 Part 1에서 만든 **영화 스트리밍 서비스 데이터셋**을 그대로 사용합니다.

---

## 📚 목차

1. [UNWIND - 리스트를 행으로 펼치기](#1-unwind---리스트를-행으로-펼치기)
2. [INDEX & CONSTRAINT - 인덱스와 제약조건](#2-index--constraint---인덱스와-제약조건)
3. [리스트 컴프리헨션과 술어 함수](#3-리스트-컴프리헨션과-술어-함수)
4. [CALL { } 서브쿼리](#4-call---서브쿼리)
5. [파라미터 ($param)](#5-파라미터-param)
6. [주요 함수들 (Functions)](#6-주요-함수들-functions)

---

## 1. UNWIND - 리스트를 행으로 펼치기

### 📖 구문 설명

`UNWIND`는 **리스트(또는 배열)를 여러 행(row)으로 전개**하는 절입니다.  
`collect()`가 여러 행을 하나의 리스트로 모았다면, `UNWIND`는 그 반대 작업을 수행합니다.

**기본 문법:**

```cypher
UNWIND [값1, 값2, 값3, ...] AS 변수
-- 또는 -- 
UNWIND $리스트파라미터 AS 변수
-- 또는 --
WITH [...] AS list
UNWIND list AS x
```

**언제 쓰는가?**

1. **대량 데이터 적재 (Bulk Insert)** — 외부 데이터를 한 번에 그래프로 적재
2. **LLM 출력 처리** — JSON 리스트를 받아 노드/관계로 변환 (Graph RAG의 핵심!)
3. **collect 후 재펼침** — 집계와 매핑이 섞인 복잡한 변환
4. **반복적 패턴 처리** — 정해진 입력 셋트로 동일 작업을 반복

> 🔑 **핵심 동작**: `UNWIND`는 입력 리스트가 N개이면, 그 뒤의 절들이 **N번 실행되는 효과**를 냅니다.

### 💡 예제

```cypher
// 예제 1: 가장 기본적인 UNWIND
UNWIND [1, 2, 3, 4, 5] AS num
RETURN num, num * num AS 제곱;

// 결과: 5개 행
// num | 제곱
//  1  | 1
//  2  | 4
//  3  | 9
//  4  | 16
//  5  | 25

// 예제 2: UNWIND + CREATE로 일괄 노드 생성
UNWIND [
  {name: '이재현', age: 30, joinYear: 2023},
  {name: '손미영', age: 26, joinYear: 2024},
  {name: '김도현', age: 41, joinYear: 2015}
] AS row
CREATE (u:User {name: row.name, age: row.age, joinYear: row.joinYear})
RETURN u;

// 예제 3: UNWIND + MERGE로 중복 방지 일괄 적재
UNWIND ['느와르', '판타지', '뮤지컬', '다큐멘터리'] AS genreName
MERGE (g:Genre {name: genreName})
RETURN g.name;
```

### ✏️ 연습문제

#### 문제 1-1
숫자 리스트 `[10, 20, 30, 40, 50]`을 펼쳐, 각 숫자와 그 숫자의 두 배를 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
UNWIND [10, 20, 30, 40, 50] AS n
RETURN n, n * 2 AS 두배;
```

**해설:** `UNWIND`의 기본 동작 확인용. 리스트의 각 요소가 하나의 행이 됩니다.

</details>

#### 문제 1-2
다음 영화 데이터를 한 번의 쿼리로 일괄 생성하세요.
- `'추격자'` (2008년, 125분)
- `'아저씨'` (2010년, 119분)
- `'7번방의 선물'` (2013년, 127분)

<details>
<summary>💡 정답 보기</summary>

```cypher
UNWIND [
  {title: '추격자', released: 2008, runtime: 125},
  {title: '아저씨', released: 2010, runtime: 119},
  {title: '7번방의 선물', released: 2013, runtime: 127}
] AS row
CREATE (m:Movie {title: row.title, released: row.released, runtime: row.runtime})
RETURN m.title, m.released;
```

**해설:** 대량 적재의 표준 패턴. **`CREATE` N번 작성** 대신 **데이터를 리스트로 정리한 뒤 `UNWIND` + `CREATE`** 로 깔끔하게 처리합니다.

</details>

#### 문제 1-3
위와 동일한 영화 3편을 이번엔 **중복 방지**(`MERGE`)로 적재하되, 이미 존재하면 그대로 두고 새로 만드는 경우에만 속성을 부여하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
UNWIND [
  {title: '추격자', released: 2008, runtime: 125},
  {title: '아저씨', released: 2010, runtime: 119},
  {title: '7번방의 선물', released: 2013, runtime: 127}
] AS row
MERGE (m:Movie {title: row.title})
ON CREATE SET m.released = row.released, m.runtime = row.runtime
RETURN m.title, m.released;
```

**해설:**
- 매칭 키(`title`)만 `MERGE` 패턴에 두고, 부가 속성은 `ON CREATE SET`에 두는 것이 **ETL의 황금률**입니다.
- 같은 쿼리를 여러 번 실행해도 중복 노드가 생기지 않습니다 (멱등성).

</details>

#### 문제 1-4
다음 데이터(감독-영화 쌍)를 한 번의 쿼리로 모두 적재하세요. 인물·영화 노드와 `:DIRECTED` 관계 모두 중복 없이 생성되어야 합니다.

```
[
  ('이창동', '버닝', 2018),
  ('이창동', '시', 2010),
  ('홍상수', '지금은맞고그때는틀리다', 2015),
  ('홍상수', '소설가의 영화', 2022)
]
```

<details>
<summary>💡 정답 보기</summary>

```cypher
UNWIND [
  {director: '이창동', title: '버닝', year: 2018},
  {director: '이창동', title: '시', year: 2010},
  {director: '홍상수', title: '지금은맞고그때는틀리다', year: 2015},
  {director: '홍상수', title: '소설가의 영화', year: 2022}
] AS row
MERGE (d:Person {name: row.director})
MERGE (m:Movie {title: row.title})
ON CREATE SET m.released = row.year
MERGE (d)-[:DIRECTED]->(m)
RETURN d.name, m.title, m.released;
```

**해설:** `UNWIND` + 3중 `MERGE` 패턴은 그래프 ETL의 가장 전형적인 구조입니다.  
- 첫 `MERGE`: 인물 노드
- 두 번째 `MERGE`: 영화 노드  
- 세 번째 `MERGE`: 둘 사이의 관계  
이 순서를 지키지 않으면 안 됩니다.

</details>

#### 문제 1-5
영화 `'기생충'`에 출연한 모든 배우의 이름을 리스트로 모은 뒤, **다시 한 행씩** 펼쳐서 각 배우의 이름과 출생연도를 반환하세요.  
(힌트: `collect()` → `UNWIND` 패턴)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:ACTED_IN]->(:Movie {title: '기생충'})
WITH collect(p) AS actors
UNWIND actors AS actor
RETURN actor.name, actor.born;
```

**해설:**
- 이 문제만 보면 그냥 `MATCH` + `RETURN`으로 푸는 게 더 간단합니다.
- 그러나 실제로는 "어떤 집계 결과를 다시 행 단위로 처리하고 싶을 때" 이 패턴이 자주 등장합니다.
- 예: 평균 평점이 가장 높은 영화의 배우들에 대해서만 추가 작업을 하고 싶을 때.

</details>

#### 문제 1-6
사용자 `'김철수'`가 추천하고 싶은 영화 목록을 친구들에게 `:RATED` 평점 4로 일괄 등록하세요. 영화 제목 목록은 `['살인의 추억', '마더', '설국열차']` 입니다. (이미 평가한 경우 평점만 4로 갱신)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User {name: '김철수'})
UNWIND ['살인의 추억', '마더', '설국열차'] AS title
MATCH (m:Movie {title: title})
MERGE (u)-[r:RATED]->(m)
ON CREATE SET r.rating = 4, r.date = '2024-12-01'
ON MATCH SET r.rating = 4
RETURN u.name, m.title, r.rating;
```

**해설:**
- `MATCH` 다음에 `UNWIND`가 오면, 각 unwind된 값마다 MATCH 결과(`u`)가 결합되어 진행됩니다.
- 한 사용자에 대해 N개의 영화 처리를 안전한 upsert로 한 번에 끝내는 패턴.

</details>

#### 문제 1-7
다음과 같이 한 영화에 여러 장르가 매핑된 데이터를 적재하세요.

```
[
  ('곡성', ['스릴러', '미스터리', '오컬트']),
  ('부산행', ['액션', '좀비', '재난'])
]
```

장르가 그래프에 없다면 새로 생성하고, 영화-장르 관계도 중복 없이 만드세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
UNWIND [
  {title: '곡성', genres: ['스릴러', '미스터리', '오컬트']},
  {title: '부산행', genres: ['액션', '좀비', '재난']}
] AS row
MERGE (m:Movie {title: row.title})
WITH m, row.genres AS genres
UNWIND genres AS gName
MERGE (g:Genre {name: gName})
MERGE (m)-[:IN_GENRE]->(g)
RETURN m.title, collect(g.name) AS 장르;
```

**해설:**
- **2중 `UNWIND`** 패턴 — 바깥 `UNWIND`는 영화 단위, 안쪽 `UNWIND`는 장르 단위.
- 중간의 `WITH m, row.genres AS genres`가 중요합니다. `UNWIND` 후엔 이전 변수가 사라질 수 있으므로 명시적으로 전달해야 합니다.
- 실무에서 JSON 형태의 중첩 데이터를 그래프에 적재할 때 사용하는 패턴.

</details>

---

## 2. INDEX & CONSTRAINT - 인덱스와 제약조건

### 📖 구문 설명

**인덱스(Index)**: 특정 속성에 대한 빠른 조회를 위한 데이터 구조. 인덱스가 없으면 `MATCH`는 해당 라벨의 **모든 노드를 스캔**합니다.  

**제약조건(Constraint)**: 데이터 무결성을 강제하는 규칙. 위반 시 쿼리가 실패합니다.  
참고로 **유일성 제약조건은 내부적으로 인덱스를 자동 생성**하므로 인덱스를 따로 만들 필요가 없습니다.

**주요 종류 (Neo4j 5.x 기준):**

| 종류 | 용도 |
|------|------|
| **RANGE INDEX** | 등호·범위 비교 (`=`, `<`, `>`, `STARTS WITH`) — 기본 인덱스 |
| **TEXT INDEX** | 문자열 패턴 검색 최적화 |
| **POINT INDEX** | 공간 데이터(`point()`) |
| **FULLTEXT INDEX** | 전문(全文) 검색 |
| **VECTOR INDEX** | 임베딩 벡터 검색 — **Graph RAG 핵심** |
| **UNIQUENESS CONSTRAINT** | 속성 유일성 보장 |
| **EXISTENCE CONSTRAINT** | 속성 필수값 (엔터프라이즈 에디션) |
| **NODE KEY** | 유일성 + 필수값 결합 (엔터프라이즈 에디션) |

**기본 문법 (Neo4j 5.x):**

```cypher
-- 인덱스 생성
CREATE INDEX 인덱스이름 IF NOT EXISTS 
  FOR (n:Label) ON (n.속성);

-- 복합 인덱스
CREATE INDEX 인덱스이름 IF NOT EXISTS 
  FOR (n:Label) ON (n.속성1, n.속성2);

-- 관계에 인덱스
CREATE INDEX 인덱스이름 IF NOT EXISTS 
  FOR ()-[r:REL]-() ON (r.속성);

-- 유일성 제약조건
CREATE CONSTRAINT 제약이름 IF NOT EXISTS 
  FOR (n:Label) REQUIRE n.속성 IS UNIQUE;

-- 인덱스/제약조건 조회
SHOW INDEXES;
SHOW CONSTRAINTS;

-- 삭제
DROP INDEX 인덱스이름 IF EXISTS;
DROP CONSTRAINT 제약이름 IF EXISTS;
```

> ⚠️ **버전 주의**: Neo4j 4.x 와 5.x의 문법이 다릅니다. 위 문법은 5.x 기준이며, 4.x는 `ON` 대신 다른 표현을 씁니다. 본인이 쓰는 버전 문서를 확인하세요.

### 💡 예제

```cypher
// 예제 1: 영화 제목에 인덱스 생성
CREATE INDEX movie_title_index IF NOT EXISTS
FOR (m:Movie) ON (m.title);

// 예제 2: 사용자 이름 유일성 제약조건 (인덱스 자동 생성)
CREATE CONSTRAINT user_name_unique IF NOT EXISTS
FOR (u:User) REQUIRE u.name IS UNIQUE;

// 예제 3: 복합 인덱스 (year + runtime으로 검색이 잦을 때)
CREATE INDEX movie_year_runtime IF NOT EXISTS
FOR (m:Movie) ON (m.released, m.runtime);

// 예제 4: 인덱스 사용 여부 확인 (실행 계획)
EXPLAIN MATCH (m:Movie {title: '기생충'}) RETURN m;
// → 결과의 "NodeIndexSeek" 가 있으면 인덱스가 사용됨
// → "NodeByLabelScan" 이 보이면 인덱스 미사용 (전체 스캔)
```

### ✏️ 연습문제

#### 문제 2-1
`Person` 노드의 `name` 속성에 인덱스 `person_name_idx`를 생성하세요. (이미 있으면 무시)

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE INDEX person_name_idx IF NOT EXISTS
FOR (p:Person) ON (p.name);
```

**해설:** 가장 흔한 인덱스 패턴. `IF NOT EXISTS`는 이미 동일 이름 인덱스가 있을 때 에러를 방지합니다. 운영 환경 마이그레이션 스크립트의 필수 패턴.

</details>

#### 문제 2-2
`User` 노드의 `name` 속성이 유일해야 한다는 제약조건 `user_name_unique`를 생성하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE CONSTRAINT user_name_unique IF NOT EXISTS
FOR (u:User) REQUIRE u.name IS UNIQUE;
```

**해설:**
- 이 제약조건을 만든 뒤 같은 이름의 `User`를 또 만들려고 하면 쿼리가 실패합니다.
- 부수 효과로 `User.name`에 대한 인덱스가 자동 생성됩니다.

</details>

#### 문제 2-3
현재 그래프에 정의된 **모든 인덱스와 제약조건**을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
SHOW INDEXES;
SHOW CONSTRAINTS;
```

또는 상세하게:

```cypher
SHOW INDEXES YIELD name, type, labelsOrTypes, properties, state
RETURN name, type, labelsOrTypes, properties, state;
```

**해설:** `SHOW INDEXES`는 일반 쿼리처럼 결과를 반환하므로, 뒤에 `YIELD`로 원하는 컬럼만 추릴 수 있습니다. 운영 환경 점검 시 자주 씁니다.

</details>

#### 문제 2-4
`Movie` 노드의 `released`와 `runtime`을 함께 검색하는 쿼리가 자주 발생한다고 가정하고, 복합 인덱스 `movie_year_runtime_idx`를 만드세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE INDEX movie_year_runtime_idx IF NOT EXISTS
FOR (m:Movie) ON (m.released, m.runtime);
```

**해설:**
- 복합 인덱스는 컬럼 순서가 중요합니다 — `released`로 시작하는 검색에 효과적이고, `runtime`만 단독으로 검색하면 잘 활용되지 않을 수 있습니다.
- 검색 패턴을 분석하고 만들어야 효과적입니다.

</details>

#### 문제 2-5
`:RATED` 관계의 `rating` 속성에 인덱스 `rated_rating_idx`를 만드세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE INDEX rated_rating_idx IF NOT EXISTS
FOR ()-[r:RATED]-() ON (r.rating);
```

**해설:** 관계 인덱스는 `FOR ()-[r:TYPE]-()` 형식을 사용합니다 (Neo4j 4.3+). 평점 기반 필터링이 잦은 쿼리에 유리합니다.

</details>

#### 문제 2-6
어떤 쿼리가 인덱스를 사용하는지 확인하고 싶을 때, **인덱스 사용 여부를 확인하는 쿼리**를 작성하세요. 대상 쿼리는 다음입니다:

```cypher
MATCH (m:Movie {title: '기생충'}) RETURN m;
```

<details>
<summary>💡 정답 보기</summary>

```cypher
EXPLAIN MATCH (m:Movie {title: '기생충'}) RETURN m;
```

또는 실제로 실행하면서 통계까지 보고 싶다면:

```cypher
PROFILE MATCH (m:Movie {title: '기생충'}) RETURN m;
```

**해설:**
- `EXPLAIN`: 쿼리를 실행하지 않고 계획만 표시 (가볍게 확인용).
- `PROFILE`: 실제로 실행하면서 각 단계의 행 수, 페이지 캐시 히트 등 통계까지 표시 (성능 튜닝용).
- 출력 그래프에서 `NodeIndexSeek` → 인덱스 사용 / `NodeByLabelScan` → 전체 스캔.

</details>

#### 문제 2-7
앞서 만든 인덱스 `movie_title_index` 가 더 이상 필요 없다고 가정하고 삭제하세요. (없어도 에러 없이)

<details>
<summary>💡 정답 보기</summary>

```cypher
DROP INDEX movie_title_index IF EXISTS;
```

**해설:** 인덱스도 삭제 가능합니다. 인덱스가 있으면 쓰기(WRITE) 성능이 떨어지므로, 안 쓰는 인덱스는 정리하는 게 좋습니다.

</details>

#### 문제 2-8
**(개념 문제)** `CREATE INDEX ... FOR (m:Movie) ON (m.title)` 을 만들었을 때, 다음 두 쿼리 중 인덱스가 사용되는 것은 무엇이고, 그 이유는 무엇인가요?

```cypher
-- 쿼리 A
MATCH (m:Movie) WHERE m.title = '기생충' RETURN m;

-- 쿼리 B
MATCH (m:Movie) WHERE m.title CONTAINS '생충' RETURN m;
```

<details>
<summary>💡 정답 보기</summary>

**답:** A는 인덱스를 사용하지만, B는 일반적으로 사용하지 않습니다.

**이유:**
- A는 정확히 일치(`=`)하는 검색이므로 RANGE 인덱스로 빠르게 찾을 수 있습니다.
- B는 문자열 중간 일치(`CONTAINS`)이므로 RANGE 인덱스를 활용할 수 없습니다.
- `CONTAINS`나 `ENDS WITH` 처럼 중간/끝 일치 검색이 잦다면 **TEXT INDEX**를 추가로 만들면 일부 시나리오에서 성능이 개선됩니다.
- 정말 본격적인 부분 문자열 검색이 필요하면 **FULLTEXT INDEX**가 정답입니다.

```cypher
-- TEXT 인덱스
CREATE TEXT INDEX movie_title_text IF NOT EXISTS
FOR (m:Movie) ON (m.title);

-- FULLTEXT 인덱스
CREATE FULLTEXT INDEX movie_title_fulltext IF NOT EXISTS
FOR (m:Movie) ON EACH [m.title];
```

</details>

---

## 3. 리스트 컴프리헨션과 술어 함수

### 📖 구문 설명

Cypher는 함수형 언어처럼 **리스트를 다루는 강력한 기능**을 갖고 있습니다.

**(1) 리스트 컴프리헨션 (List Comprehension)**

```cypher
[변수 IN 리스트 WHERE 조건 | 표현식]
```

- `WHERE 조건` (생략 가능): 필터링
- `| 표현식` (생략 가능): 변환

**Python의 `[x*2 for x in list if x > 3]` 과 동일한 개념입니다.**

**(2) 패턴 컴프리헨션 (Pattern Comprehension)**

```cypher
[(a)-[:REL]->(b) WHERE 조건 | b.속성]
```

그래프 패턴 결과를 즉시 리스트로 변환할 때 사용합니다.

**(3) 술어 함수 (Predicate Functions)**

| 함수 | 의미 |
|------|------|
| `any(x IN list WHERE 조건)` | 하나라도 만족하면 true |
| `all(x IN list WHERE 조건)` | 모두 만족하면 true |
| `none(x IN list WHERE 조건)` | 아무도 만족하지 않으면 true |
| `single(x IN list WHERE 조건)` | **정확히 1개만** 만족하면 true |

**(4) `reduce` — 누적 계산**

```cypher
reduce(누적변수 = 초깃값, x IN 리스트 | 누적변수 + x)
```

리스트의 합·곱·문자열 결합 등 누적 계산에 사용합니다.

### 💡 예제

```cypher
// 예제 1: 리스트 컴프리헨션 - 짝수만 골라서 제곱
RETURN [x IN [1,2,3,4,5,6] WHERE x % 2 = 0 | x * x] AS 결과;
// 결과: [4, 16, 36]

// 예제 2: 패턴 컴프리헨션 - 봉준호 영화 제목 리스트
MATCH (bong:Person {name: '봉준호'})
RETURN [(bong)-[:DIRECTED]->(m:Movie) | m.title] AS 봉준호영화;

// 예제 3: 술어 함수 - '스릴러' 장르가 포함된 영화
MATCH (m:Movie)
WHERE any(g IN [(m)-[:IN_GENRE]->(genre) | genre.name] WHERE g = '스릴러')
RETURN m.title;

// 예제 4: reduce - 어떤 리스트의 합
RETURN reduce(s = 0, x IN [1,2,3,4,5] | s + x) AS 합;
// 결과: 15
```

### ✏️ 연습문제

#### 문제 3-1
`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`에서 짝수만 골라 3배한 값의 리스트를 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
RETURN [x IN [1,2,3,4,5,6,7,8,9,10] WHERE x % 2 = 0 | x * 3] AS 결과;
```

**해설:** 리스트 컴프리헨션의 기본형 — `WHERE` 로 필터, `|` 뒤에 변환식.

</details>

#### 문제 3-2
모든 영화의 제목 리스트를 한 행으로 반환하세요. 단, 제목 앞에 `'★ '`를 붙여서.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
WITH collect(m.title) AS titles
RETURN [t IN titles | '★ ' + t] AS 별표제목;
```

또는 패턴 컴프리헨션으로 한 번에:

```cypher
RETURN [(m:Movie) | '★ ' + m.title] AS 별표제목;
```

**해설:** 두 번째 풀이가 더 Cypher스럽습니다. 패턴 컴프리헨션은 노드 매칭 + 리스트 변환을 한 줄로 처리합니다.

</details>

#### 문제 3-3
**`'스릴러'` 장르 영화에 출연한 적이 있는 배우**의 이름을 반환하세요.  
조건: `WHERE any(...)` 술어 함수를 활용하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)
WHERE any(g IN [(p)-[:ACTED_IN]->(:Movie)-[:IN_GENRE]->(genre) | genre.name] 
         WHERE g = '스릴러')
RETURN p.name;
```

또는 더 단순하게 (술어 함수를 안 쓰는 버전):

```cypher
MATCH (p:Person)-[:ACTED_IN]->(:Movie)-[:IN_GENRE]->(:Genre {name: '스릴러'})
RETURN DISTINCT p.name;
```

**해설:**
- 사실 일반 MATCH로 더 깔끔하게 풀 수 있습니다.
- 술어 함수는 "이미 가진 리스트(컬럼)에 대한 조건 검사"에서 진가를 발휘합니다 → 다음 문제 참고.

</details>

#### 문제 3-4
모든 영화의 (제목, 그 영화의 장르 리스트)를 반환하되, **`'스릴러'`와 `'드라마'`가 모두 포함된** 영화만 결과에 남기세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
WITH m, [(m)-[:IN_GENRE]->(g) | g.name] AS genres
WHERE '스릴러' IN genres AND '드라마' IN genres
RETURN m.title, genres;
```

또는 `all()` 활용:

```cypher
MATCH (m:Movie)
WITH m, [(m)-[:IN_GENRE]->(g) | g.name] AS genres
WHERE all(req IN ['스릴러', '드라마'] WHERE req IN genres)
RETURN m.title, genres;
```

**해설:**
- 첫 번째: `IN` 연산자로 직관적.
- 두 번째: 검사할 장르가 늘어나도 동일한 패턴으로 확장 가능.

</details>

#### 문제 3-5
모든 사용자에 대해, 그 사용자가 매긴 평점 리스트와 함께, **모든 평점이 4점 이상인 사용자만** 골라내세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)-[r:RATED]->(:Movie)
WITH u, collect(r.rating) AS ratings
WHERE all(x IN ratings WHERE x >= 4)
RETURN u.name, ratings;
```

**해설:**
- `all()`은 리스트의 모든 요소가 조건을 만족하는지 검사합니다.
- "후한 평점만 주는 사용자"를 찾는 패턴 — 데이터 품질 검사, 이상치 탐지 등에 활용됩니다.

</details>

#### 문제 3-6
1점이나 2점 평가가 **하나도 없는** 사용자만 반환하세요.  
(힌트: `none()` 활용)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)-[r:RATED]->(:Movie)
WITH u, collect(r.rating) AS ratings
WHERE none(x IN ratings WHERE x <= 2)
RETURN u.name, ratings;
```

**해설:** `none()`은 "단 하나도 조건을 만족하지 않을 때" true. `NOT any(...)`와 동치이지만 의도가 더 명확합니다.

</details>

#### 문제 3-7
리스트 `[3, 7, 2, 8, 5, 1, 9]`의 **합**과 **최댓값**을 `reduce`만 사용해서 각각 계산하세요. (built-in `sum`, `max` 사용 금지)

<details>
<summary>💡 정답 보기</summary>

```cypher
WITH [3, 7, 2, 8, 5, 1, 9] AS nums
RETURN 
  reduce(s = 0, x IN nums | s + x) AS 합,
  reduce(m = nums[0], x IN nums | CASE WHEN x > m THEN x ELSE m END) AS 최댓값;
```

**해설:**
- `reduce(누적 = 초깃값, x IN 리스트 | 표현식)` 구조.
- 최댓값은 `CASE`로 분기. 누적 변수의 초깃값을 리스트 첫 요소(`nums[0]`)로 시작하는 것이 안전합니다.

</details>

#### 문제 3-8
각 감독에 대해, 그 감독이 만든 영화의 **상영시간 합계**를 `reduce`로 계산해서 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
WITH p, collect(m.runtime) AS runtimes
RETURN p.name AS 감독, 
       reduce(s = 0, x IN runtimes | s + x) AS 총상영시간;
```

또는 그냥 `sum()`을 써도 됩니다 (실무에선 이게 더 자연스러움):

```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN p.name AS 감독, sum(m.runtime) AS 총상영시간;
```

**해설:** `reduce`는 "내장 집계 함수로 표현 못하는 누적 로직"에 빛납니다. 합계는 그냥 `sum()`이 낫지만, 문자열 연결이나 복잡한 조건 누적엔 `reduce`가 필요합니다.

</details>

#### 문제 3-9
영화 `'기생충'`에 출연한 배우들의 이름을 `' / '`로 구분한 **하나의 문자열**로 만드세요. (예: `'송강호 / 조여정'`)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:ACTED_IN]->(:Movie {title: '기생충'})
WITH collect(p.name) AS names
RETURN reduce(s = '', i IN range(0, size(names)-1) | 
  s + CASE WHEN i = 0 THEN '' ELSE ' / ' END + names[i]
) AS 출연진;
```

또는 더 간단히 (Neo4j 5.x 의 `apoc.text.join` 사용 가능):

```cypher
MATCH (p:Person)-[:ACTED_IN]->(:Movie {title: '기생충'})
RETURN apoc.text.join(collect(p.name), ' / ') AS 출연진;
```

**해설:**
- `reduce`로 문자열을 누적할 때는 첫 요소 앞에 구분자가 들어가지 않도록 분기 처리가 필요합니다.
- 실무에선 APOC 라이브러리의 `apoc.text.join`이 훨씬 깔끔합니다.

</details>

#### 문제 3-10
**친구가 정확히 한 명인** 사용자를 찾으세요. (힌트: `single()` 활용)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
WHERE single(f IN [(u)-[:FRIENDS_WITH]->(friend) | friend] WHERE true)
RETURN u.name;
```

또는 더 직관적인 풀이:

```cypher
MATCH (u:User)
OPTIONAL MATCH (u)-[:FRIENDS_WITH]->(f:User)
WITH u, count(f) AS cnt
WHERE cnt = 1
RETURN u.name, cnt;
```

**해설:**
- `single()`은 리스트의 요소 중 조건을 만족하는 것이 **정확히 1개**일 때 true.
- 위의 첫 풀이에서 `WHERE true`는 "조건 없이 단순히 1개인지 확인"하는 트릭.
- 두 번째 풀이가 가독성이 훨씬 좋습니다 — 실무에선 이쪽 추천.

</details>

---

## 4. CALL { } 서브쿼리

### 📖 구문 설명

`CALL { ... }`는 **쿼리 안에 또 다른 쿼리(서브쿼리)를 격리**해서 실행하는 절입니다. Neo4j 4.x부터 도입된 매우 강력한 기능으로, `WITH` 만으로는 표현하기 어려운 복잡한 흐름을 깔끔하게 처리할 수 있습니다.

**기본 문법:**

```cypher
-- (1) 단순 서브쿼리
CALL {
  -- 독립된 쿼리 (외부 변수 못 씀)
  MATCH (m:Movie) RETURN m LIMIT 5
}
RETURN m;

-- (2) 외부 변수 import (각 외부 행마다 실행)
MATCH (u:User)
CALL (u) {
  -- u를 받아서 사용자별로 실행
  MATCH (u)-[r:RATED]->(m:Movie)
  RETURN m.title AS title, r.rating AS rating
  ORDER BY r.rating DESC
  LIMIT 1
}
RETURN u.name, title, rating;

-- (3) UNION으로 합치기
CALL {
  MATCH (m:Movie) WHERE m.released < 2010 RETURN m, '구작' AS era
  UNION
  MATCH (m:Movie) WHERE m.released >= 2010 RETURN m, '신작' AS era
}
RETURN m.title, era;
```

> ⚠️ **버전 주의**: Neo4j 5.x부터 외부 변수 import 문법이 `CALL (variable) { ... }`로 변경됐습니다. 4.x에서는 서브쿼리 안에서 `WITH variable`로 import 했습니다. 본 자료는 5.x 기준입니다.

**언제 쓰는가?**

1. **외부 행마다 다른 집계/제한 처리** (예: 사용자별 Top 3 영화)
2. **여러 쿼리 결과를 UNION으로 합치기**
3. **WITH로는 흐름 제어가 너무 복잡할 때**
4. **트랜잭션 단위 분리** (`CALL { ... } IN TRANSACTIONS` — 대량 처리)

### 💡 예제

```cypher
// 예제 1: 사용자별 최고 평점 영화 1편씩
MATCH (u:User)
CALL (u) {
  MATCH (u)-[r:RATED]->(m:Movie)
  RETURN m.title AS title, r.rating AS rating
  ORDER BY r.rating DESC
  LIMIT 1
}
RETURN u.name AS 사용자, title AS 최애영화, rating AS 평점;

// 예제 2: UNION으로 다른 카테고리 합치기
CALL {
  MATCH (m:Movie) 
  WHERE m.released >= 2020 
  RETURN m.title AS title, '신작' AS category
  UNION
  MATCH (m:Movie) 
  WHERE m.runtime > 140 
  RETURN m.title AS title, '장편' AS category
}
RETURN title, category
ORDER BY category, title;

// 예제 3: 서브쿼리에서 집계만 따로
MATCH (m:Movie)
CALL (m) {
  MATCH (m)<-[r:RATED]-(:User)
  RETURN count(r) AS ratingCount, avg(r.rating) AS avgRating
}
RETURN m.title, ratingCount, avgRating
ORDER BY avgRating DESC;
```

### ✏️ 연습문제

#### 문제 4-1
각 사용자에 대해 그 사용자가 매긴 평점 중 **가장 높은 점수의 영화 1편**의 제목과 평점을 반환하세요. (사용자별 Top 1)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
CALL (u) {
  MATCH (u)-[r:RATED]->(m:Movie)
  RETURN m.title AS title, r.rating AS rating
  ORDER BY r.rating DESC
  LIMIT 1
}
RETURN u.name AS 사용자, title AS 최고영화, rating AS 평점;
```

**해설:**
- 이 패턴은 일반 `MATCH` + `ORDER BY` + `LIMIT 1`로는 안 됩니다 — 그러면 전체에서 1편만 나옵니다.
- `CALL (u)` 로 사용자별로 격리 실행되며, 각 사용자마다 `LIMIT 1` 이 따로 적용됩니다.
- SQL의 `ROW_NUMBER() OVER (PARTITION BY ...)` 윈도우 함수에 해당하는 패턴입니다.

</details>

#### 문제 4-2
각 감독에 대해 그가 만든 영화 중 **가장 최근에 개봉한 영화 2편**을 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:DIRECTED]->(:Movie)
WITH DISTINCT p
CALL (p) {
  MATCH (p)-[:DIRECTED]->(m:Movie)
  RETURN m.title AS title, m.released AS released
  ORDER BY m.released DESC
  LIMIT 2
}
RETURN p.name AS 감독, title, released
ORDER BY p.name, released DESC;
```

**해설:**
- 외부 `MATCH`에서 감독을 추리고, `CALL`에서 감독별로 최신 2편씩 추출.
- "그룹별 Top N" 의 전형적 패턴.

</details>

#### 문제 4-3
서브쿼리를 사용해 다음 두 결과를 **UNION으로 합쳐서** 반환하세요:
- 평점이 5점인 영화 (제목, `'최고평점'` 라벨)
- 평점이 2점 이하인 영화 (제목, `'저평점'` 라벨)

<details>
<summary>💡 정답 보기</summary>

```cypher
CALL {
  MATCH (m:Movie)<-[r:RATED]-(:User)
  WHERE r.rating = 5
  RETURN DISTINCT m.title AS title, '최고평점' AS category
  UNION
  MATCH (m:Movie)<-[r:RATED]-(:User)
  WHERE r.rating <= 2
  RETURN DISTINCT m.title AS title, '저평점' AS category
}
RETURN title, category
ORDER BY category, title;
```

**해설:**
- `UNION`은 중복을 자동 제거합니다. 중복까지 다 보고 싶으면 `UNION ALL`.
- 서로 다른 패턴의 결과를 한 결과셋으로 합쳐주므로, 여러 조건의 결과를 한 번에 보고 싶을 때 유용.

</details>

#### 문제 4-4
각 영화에 대해 그 영화의 **평균 평점**과 **평가 사용자 수**를 함께 반환하세요. `CALL` 서브쿼리로 작성하세요.  
(주의: 평가가 없는 영화도 포함되어야 합니다 → 평균과 카운트는 0/null)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
CALL (m) {
  OPTIONAL MATCH (m)<-[r:RATED]-(u:User)
  RETURN avg(r.rating) AS avgRating, count(u) AS userCount
}
RETURN m.title AS 영화, 
       coalesce(avgRating, 0) AS 평균평점, 
       userCount AS 평가자수
ORDER BY 평균평점 DESC;
```

**해설:**
- 서브쿼리 안에서 `OPTIONAL MATCH`를 써서 평가 없는 영화도 처리.
- `coalesce(x, 기본값)`은 x가 null이면 기본값을 반환하는 함수 (다음 함수 섹션 참고).
- 이 패턴은 `WITH`만으로도 가능하지만, `CALL`을 쓰면 평균 계산 부분이 시각적으로 격리되어 가독성이 좋아집니다.

</details>

#### 문제 4-5
각 장르에 대해 그 장르의 **영화 수**와 **평균 상영시간**을 함께 반환하세요. `CALL` 서브쿼리로 작성하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (g:Genre)
CALL (g) {
  MATCH (m:Movie)-[:IN_GENRE]->(g)
  RETURN count(m) AS movieCount, avg(m.runtime) AS avgRuntime
}
RETURN g.name AS 장르, movieCount AS 영화수, avgRuntime AS 평균상영시간
ORDER BY 영화수 DESC;
```

**해설:**
- 외부 라벨에 대해 통계를 산출하는 표준 패턴. 대시보드형 쿼리에 적합.

</details>

#### 문제 4-6
각 사용자에 대해 다음 정보를 동시에 반환하세요:
- 평가한 영화 수
- 평균 평점
- **가장 자주 본 장르**(평가한 영화에서 가장 많이 등장한 장르) 1개

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
CALL (u) {
  MATCH (u)-[r:RATED]->(:Movie)
  RETURN count(r) AS cnt, avg(r.rating) AS avgR
}
CALL (u) {
  MATCH (u)-[:RATED]->(:Movie)-[:IN_GENRE]->(g:Genre)
  WITH g.name AS genre, count(*) AS gCount
  ORDER BY gCount DESC
  LIMIT 1
  RETURN genre AS favGenre
}
RETURN u.name AS 사용자, cnt AS 평가수, avgR AS 평균평점, favGenre AS 최애장르;
```

**해설:**
- 두 개의 `CALL` 서브쿼리를 차례로 사용. 각각 다른 종류의 집계를 별도로 처리하므로 가독성이 좋습니다.
- 두 번째 서브쿼리는 "사용자가 평가한 영화의 장르"를 모두 모아 가장 빈도가 높은 것 1개를 추립니다.

</details>

#### 문제 4-7
**(심화)** 각 감독에 대해 그가 감독한 모든 영화의 **평균 평점 합계**를 구한 뒤, 평균이 가장 높은 감독 Top 3를 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:DIRECTED]->(:Movie)
WITH DISTINCT p
CALL (p) {
  MATCH (p)-[:DIRECTED]->(m:Movie)<-[r:RATED]-(:User)
  WITH m, avg(r.rating) AS movieAvg
  RETURN avg(movieAvg) AS directorAvg, count(m) AS movieCount
}
WHERE directorAvg IS NOT NULL
RETURN p.name AS 감독, directorAvg AS 평균, movieCount AS 평가된영화수
ORDER BY directorAvg DESC
LIMIT 3;
```

**해설:**
- 두 단계 집계: 영화별 평균을 먼저 구하고, 그것을 감독별로 다시 평균.
- 평점이 없는 영화는 자동 제외됩니다.
- `WHERE directorAvg IS NOT NULL`: 자신의 영화에 평점이 하나도 없는 감독은 제외.

</details>

---

## 5. 파라미터 ($param)

### 📖 구문 설명

**파라미터(Parameter)** 는 쿼리 안에 값을 직접 박는 대신 **외부에서 주입**하는 방식입니다. SQL의 prepared statement / bind variable과 동일한 개념입니다.

**기본 문법:**

```cypher
-- 단일 값
MATCH (m:Movie {title: $title}) RETURN m;

-- 리스트
UNWIND $titles AS t
MATCH (m:Movie {title: t}) RETURN m;

-- 맵(객체)
CREATE (u:User $userProps);
```

**파라미터를 써야 하는 3가지 이유:**

| 이유 | 설명 |
|------|------|
| 🛡️ **보안** | 문자열 합성을 막아 Cypher 인젝션 방지 |
| ⚡ **성능** | 쿼리 플랜 캐시 재사용 (같은 구조 + 다른 값) |
| ✨ **가독성** | 코드와 데이터가 분리되어 깔끔 |

**파라미터 전달 방법:**

- **Neo4j Browser**: 쿼리 위에 `:param name => value` 명령
  ```
  :param title => '기생충'
  :param ratings => [5, 4, 3]
  :param userProps => {name: '신유저', age: 25}
  ```
- **cypher-shell**: `-P` 옵션 또는 `:param` 명령
- **드라이버 (Python, JS 등)**: 쿼리와 함께 dict/object로 전달

### 💡 예제

```cypher
-- 시나리오: 파라미터 미리 설정
:param title => '기생충'
:param minRating => 4
:param userList => [
  {name: '홍길동', age: 30},
  {name: '김영수', age: 25}
]

-- 예제 1: 단일 값 파라미터
MATCH (m:Movie {title: $title})
RETURN m;

-- 예제 2: 비교 연산 + 파라미터
MATCH (m:Movie)<-[r:RATED]-(:User)
WHERE r.rating >= $minRating
RETURN DISTINCT m.title;

-- 예제 3: 리스트 + UNWIND
UNWIND $userList AS row
MERGE (u:User {name: row.name})
ON CREATE SET u.age = row.age;
```

### ✏️ 연습문제

> 아래 문제는 Neo4j Browser의 `:param` 명령을 미리 사용한 상태를 가정합니다.

#### 문제 5-1
파라미터 `$title`을 받아서 해당 제목의 `Movie` 노드를 조회하는 쿼리를 작성하세요.

```
:param title => '기생충'
```

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie {title: $title})
RETURN m;
```

**해설:** `$파라미터명` 형태로 사용. 클라이언트(드라이버, 셸 등)에서 주입된 값으로 치환되어 실행됩니다.

</details>

#### 문제 5-2
파라미터 `$minRating`(숫자)을 받아, 그 값 이상의 평점이 있는 영화의 제목을 중복 없이 반환하세요.

```
:param minRating => 4
```

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)<-[r:RATED]-(:User)
WHERE r.rating >= $minRating
RETURN DISTINCT m.title;
```

**해설:** 비교 연산자 우변에 파라미터를 두는 가장 흔한 형태.

</details>

#### 문제 5-3
파라미터 `$titles`(영화 제목 리스트)를 받아, 해당 영화들의 (제목, 개봉연도) 정보를 모두 반환하세요.

```
:param titles => ['기생충', '올드보이', '부산행']
```

<details>
<summary>💡 정답 보기</summary>

```cypher
UNWIND $titles AS t
MATCH (m:Movie {title: t})
RETURN m.title, m.released;
```

또는 `IN` 으로:

```cypher
MATCH (m:Movie)
WHERE m.title IN $titles
RETURN m.title, m.released;
```

**해설:**
- 첫 번째: `UNWIND` 사용 — 입력 순서대로 결과가 나오고, 매칭 안 된 제목은 결과에서 빠집니다.
- 두 번째: `IN` 사용 — 더 간단. 보통 이게 더 좋습니다.

</details>

#### 문제 5-4
파라미터 `$userProps`(맵)을 받아 새로운 `User` 노드를 생성하세요.

```
:param userProps => {name: '신유저', age: 28, joinYear: 2024}
```

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE (u:User)
SET u = $userProps
RETURN u;
```

또는 더 간단하게:

```cypher
CREATE (u:User $userProps)
RETURN u;
```

**해설:**
- 맵 파라미터를 노드 속성으로 한 번에 풀어넣는 패턴.
- 두 번째 형태(`(u:User $params)`)는 매우 간결한 Cypher 관용구입니다.

</details>

#### 문제 5-5
파라미터 `$users`(User 리스트, 맵으로 구성)를 받아 일괄로 사용자 노드를 만들되, 같은 이름이 이미 있으면 그대로 두세요.

```
:param users => [
  {name: '홍길동', age: 30, joinYear: 2024},
  {name: '김영수', age: 25, joinYear: 2024}
]
```

<details>
<summary>💡 정답 보기</summary>

```cypher
UNWIND $users AS row
MERGE (u:User {name: row.name})
ON CREATE SET u.age = row.age, u.joinYear = row.joinYear
RETURN u;
```

**해설:** **`UNWIND` + `$파라미터리스트` + `MERGE`** — Graph RAG의 LLM 출력 적재, ETL 파이프라인의 가장 표준적인 패턴입니다. 거의 이 형태를 외워두세요.

</details>

#### 문제 5-6
파라미터 `$skipN`, `$limitN`을 받아 페이지네이션 쿼리를 작성하세요. 모든 영화를 제목 가나다순으로 정렬해 페이지 단위로 반환합니다.

```
:param skipN => 3
:param limitN => 5
```

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title
ORDER BY m.title
SKIP $skipN LIMIT $limitN;
```

**해설:** `SKIP`/`LIMIT`에도 파라미터가 들어갈 수 있습니다. API 백엔드에서 페이지 정보를 받을 때의 표준 패턴.

</details>

#### 문제 5-7
**(개념 문제)** 다음 두 쿼리 중 더 안전하고 효율적인 것은 무엇이며 그 이유는?

```cypher
-- 방식 A: 문자열 합성
"MATCH (m:Movie {title: '" + userInput + "'}) RETURN m"

-- 방식 B: 파라미터
"MATCH (m:Movie {title: $title}) RETURN m" + 파라미터 {title: userInput}
```

<details>
<summary>💡 정답 보기</summary>

**답:** B가 정답입니다.

**이유:**

1. **보안 (Cypher Injection 방어)**  
   A 방식에서 `userInput`이 `' OR true MATCH (n) DETACH DELETE n //` 같은 값이라면, 쿼리가 완전히 다른 의미로 실행됩니다. SQL Injection과 같은 종류의 공격.  
   B 방식은 값이 항상 "값"으로만 취급되므로 인젝션이 원천 차단됩니다.

2. **쿼리 플랜 캐시 재사용**  
   A는 입력값이 다를 때마다 쿼리 문자열이 달라지므로 Neo4j가 매번 새 플랜을 컴파일합니다. → 느림.  
   B는 쿼리 구조가 동일하므로 한 번 컴파일한 플랜을 계속 재사용합니다. → 빠름.

3. **가독성과 유지보수**  
   B는 코드와 데이터가 분리되어 변경/리뷰가 쉽습니다.

**결론**: **사용자 입력이 들어가는 모든 쿼리는 반드시 파라미터를 써야 합니다.** 예외 없습니다.

</details>

---

## 6. 주요 함수들 (Functions)

### 📖 구문 설명

Cypher는 다양한 내장 함수를 제공합니다. 카테고리별로 정리합니다.

#### (1) 문자열 함수

| 함수 | 설명 | 예시 |
|------|------|------|
| `toUpper(s)`, `toLower(s)` | 대소문자 변환 | `toUpper('abc')` → `'ABC'` |
| `trim(s)` | 양 끝 공백 제거 | `trim('  hi  ')` → `'hi'` |
| `split(s, delim)` | 분리 → 리스트 | `split('a,b,c', ',')` → `['a','b','c']` |
| `replace(s, from, to)` | 치환 | `replace('hello', 'l', 'L')` → `'heLLo'` |
| `substring(s, start, length)` | 부분 문자열 | `substring('hello', 1, 3)` → `'ell'` |
| `size(s)` | 길이 | `size('abc')` → `3` |

#### (2) 수치 함수

| 함수 | 설명 |
|------|------|
| `abs(x)` | 절댓값 |
| `ceil(x)`, `floor(x)` | 올림, 내림 |
| `round(x)`, `round(x, 자릿수)` | 반올림 |
| `sqrt(x)` | 제곱근 |
| `rand()` | 0~1 사이 난수 |

#### (3) 컬렉션 함수

| 함수 | 설명 |
|------|------|
| `size(list)` | 길이 |
| `head(list)`, `last(list)`, `tail(list)` | 첫 요소 / 마지막 요소 / 첫 요소 제외한 나머지 |
| `range(start, end[, step])` | 정수 범위 리스트 |
| `reverse(list)` | 뒤집기 |
| `keys(map)` | 맵의 키 리스트 |

#### (4) 날짜·시간 함수

| 함수 | 설명 |
|------|------|
| `date()`, `date('2024-12-01')` | 날짜 생성 |
| `datetime()`, `datetime('2024-12-01T10:00:00')` | 일시 생성 |
| `duration({days: 7})`, `duration.between(a, b)` | 기간 |
| `date.year`, `.month`, `.day` 등 | 구성 요소 추출 |

#### (5) 타입·변환 함수

| 함수 | 설명 |
|------|------|
| `toString(x)`, `toInteger(x)`, `toFloat(x)` | 형 변환 |
| `type(r)` | 관계의 타입 이름 |
| `labels(n)` | 노드의 라벨 리스트 |
| `properties(n)` | 노드/관계의 모든 속성을 맵으로 |
| `id(n)` (deprecated), `elementId(n)` | 내부 ID |

#### (6) Null 처리 / 조건 함수

| 함수 | 설명 |
|------|------|
| `coalesce(a, b, c, ...)` | 첫 번째 non-null 값 반환 |
| `CASE WHEN ... THEN ... ELSE ... END` | 조건 분기 |
| `n.속성 IS NULL` / `IS NOT NULL` | null 체크 |

### 💡 예제

```cypher
// 예제 1: 문자열 가공
MATCH (m:Movie {title: '기생충'})
RETURN toUpper(m.title), size(m.title), substring(m.title, 0, 2);

// 예제 2: 날짜 다루기
RETURN date() AS 오늘, 
       date('2019-05-30') AS 기생충개봉일,
       duration.between(date('2019-05-30'), date()).days AS 경과일;

// 예제 3: null 안전 처리
MATCH (m:Movie)
RETURN m.title, coalesce(m.language, '미지정') AS 언어;

// 예제 4: 조건 분기
MATCH (m:Movie)
RETURN m.title, 
  CASE 
    WHEN m.runtime > 130 THEN '장편'
    WHEN m.runtime > 100 THEN '중편'
    ELSE '단편'
  END AS 분류;
```

### ✏️ 연습문제

> 카테고리별로 문제를 구성했습니다. 총 15문제.

---

### 🔤 문자열 함수

#### 문제 6-1
모든 영화의 제목을 **대문자**로 변환해 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title AS 원본, toUpper(m.title) AS 대문자;
```

**해설:** 한글은 대소문자 개념이 없어서 그대로지만, 라틴 문자가 섞이면 변환됩니다 (예: `Chris Evans` → `CHRIS EVANS`).

</details>

#### 문제 6-2
모든 영화 제목의 **글자 수**를 반환하세요. 글자 수가 많은 순으로 정렬.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title, size(m.title) AS 글자수
ORDER BY 글자수 DESC;
```

**해설:** `size()`는 문자열·리스트 모두에 작동하는 다목적 함수입니다.

</details>

#### 문제 6-3
사용자 `'김철수'`의 모든 평가 날짜에서 **연도와 월만** 추출해서(`'2024-01'` 형태), 평가 영화와 함께 반환하세요. (`date` 속성은 `'2024-01-15'` 같은 문자열로 저장돼 있음)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User {name: '김철수'})-[r:RATED]->(m:Movie)
RETURN m.title, substring(r.date, 0, 7) AS 연월;
```

또는 `split`을 활용:

```cypher
MATCH (u:User {name: '김철수'})-[r:RATED]->(m:Movie)
WITH m, split(r.date, '-') AS parts
RETURN m.title, parts[0] + '-' + parts[1] AS 연월;
```

**해설:**
- `substring(s, 0, 7)`: 0번째부터 7글자 — `'2024-01-15'` → `'2024-01'`.
- 두 번째 풀이는 분할 후 재조합. 더 안전합니다 (날짜 형식이 일정하지 않을 때).

</details>

#### 문제 6-4
영화 제목에 공백이 있는 영화(예: `'살인의 추억'`)의 제목을 공백 기준으로 분리해 첫 단어만 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
WHERE m.title CONTAINS ' '
RETURN m.title, split(m.title, ' ')[0] AS 첫단어;
```

**해설:**
- `split(s, ' ')`는 공백 기준으로 분리해 리스트로 반환.
- `[0]`은 리스트의 첫 요소(인덱스 0번)에 접근.
- Cypher의 리스트 인덱싱은 Python처럼 0-based 입니다.

</details>

---

### 🔢 수치 함수

#### 문제 6-5
모든 영화에 대해 `runtime` 을 **시간 단위(소수점 1자리 반올림)** 로 변환해 반환하세요. (예: 132분 → 2.2시간)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title, 
       m.runtime AS 분, 
       round(m.runtime / 60.0, 1) AS 시간;
```

**해설:**
- 정수 나눗셈을 피하려면 분모를 `60.0` 으로 만들어야 합니다 (`60`만 쓰면 정수 나눗셈이 됩니다 — 일부 버전에서).
- `round(x, n)`: 소수점 n자리에서 반올림.

</details>

#### 문제 6-6
모든 사용자의 나이를 받아, 그 나이의 절댓값을 반환하되, 음수가 있으면 절대값을 보여주세요. (실제 데이터엔 음수가 없지만 함수 학습 목적)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
RETURN u.name, u.age, abs(u.age) AS 절댓값;
```

**해설:** 실용성보단 함수 사용법 익히기 위한 문제. 실제로는 음수 나이가 없는 경우라도, `abs`는 시간차 계산 등에 자주 활용됩니다.

</details>

---

### 📚 컬렉션 함수

#### 문제 6-7
`'봉준호'` 감독의 모든 영화 제목 리스트와 그 **첫 번째 영화 제목**, **마지막 영화 제목**, 그리고 **총 편수**를 한 행으로 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person {name: '봉준호'})-[:DIRECTED]->(m:Movie)
WITH collect(m.title) AS titles
RETURN titles AS 전체, 
       head(titles) AS 첫영화, 
       last(titles) AS 마지막영화, 
       size(titles) AS 편수;
```

**해설:**
- `head()` / `last()`: 리스트의 첫/마지막 요소.
- 단, "첫"과 "마지막"은 리스트가 만들어진 순서에 따라 달라집니다. 의도가 "가장 오래된/최신"이라면 먼저 정렬해야 합니다.

</details>

#### 문제 6-8
`range(1, 10)` 함수를 이용해 1부터 10까지의 수 중 짝수만 골라낸 리스트를 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
RETURN [x IN range(1, 10) WHERE x % 2 = 0 | x] AS 짝수;
```

**해설:**
- `range(1, 10)` → `[1,2,3,4,5,6,7,8,9,10]`
- 리스트 컴프리헨션과 함께 사용하는 매우 흔한 패턴.
- `range(start, end, step)` 으로 step 지정도 가능: `range(0, 20, 5)` → `[0,5,10,15,20]`.

</details>

#### 문제 6-9
영화 `'기생충'` 노드의 **모든 속성 키와 모든 속성을 맵 형태**로 함께 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie {title: '기생충'})
RETURN keys(m) AS 속성키들, properties(m) AS 속성맵;
```

**해설:**
- `keys(n)`: 노드/관계의 속성 키 리스트.
- `properties(n)`: 모든 속성을 맵으로.
- 스키마 분석이나 동적 쿼리에 매우 유용.

</details>

---

### 📅 날짜·시간 함수

#### 문제 6-10
오늘 날짜와 지금 시각을 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
RETURN date() AS 오늘, datetime() AS 지금;
```

**해설:** 인수 없이 호출하면 "현재" 값을 반환합니다.

</details>

#### 문제 6-11
영화 `'기생충'`의 개봉일을 `2019-05-30`으로 가정하고, **그 날로부터 오늘까지의 경과 일수**를 계산하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
RETURN duration.between(date('2019-05-30'), date()).days AS 경과일;
```

**해설:**
- `duration.between(a, b)`: 두 날짜의 차이를 `duration` 타입으로 반환.
- `.days`로 일수 추출. `.months`, `.years` 등도 있지만 의미가 약간 다릅니다 (월 단위 차이라서 정확한 계산엔 `.days`가 안전).

</details>

#### 문제 6-12
사용자의 `joinYear`를 사용해, **올해(2024년 기준) 가입 N년차** 인 사용자를 (이름, 가입년차) 형태로 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
RETURN u.name, 
       date().year - u.joinYear + 1 AS 가입년차
ORDER BY 가입년차 DESC;
```

**해설:**
- `date().year`: 현재 연도. 하드코딩 대신 동적으로 가져옵니다.
- `+1` 은 "가입한 해를 1년차로 세겠다"는 의미. 비즈니스 규칙에 따라 빼도 됩니다.

</details>

---

### 🔧 타입·변환 / Null 처리 함수

#### 문제 6-13
모든 노드의 **라벨**과 **노드 ID(elementId)**를 함께 반환하세요. (`Person`, `Movie` 등 라벨 종류 확인용)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (n)
RETURN labels(n) AS 라벨들, elementId(n) AS 노드ID
LIMIT 10;
```

**해설:**
- `labels(n)`: 한 노드의 모든 라벨을 리스트로.
- `elementId(n)`: Neo4j 5.x 이상에서 권장되는 노드 고유 ID. 4.x의 `id(n)`은 deprecated.
- 디버깅과 데이터 점검 시 핵심 함수.

</details>

#### 문제 6-14
`Movie` 노드 중 `language` 속성이 없거나 null인 영화의 제목을 반환하되, `language` 표시는 `'미지정'`으로 채우세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title, coalesce(m.language, '미지정') AS 언어;
```

**해설:**
- `coalesce(x, y, z, ...)` 는 인수를 순서대로 검사해 **첫 번째 non-null 값**을 반환합니다.
- SQL의 `COALESCE`, `IFNULL`과 동일.
- 데이터의 누락값을 안전하게 처리할 때 거의 매번 등장하는 함수.

</details>

#### 문제 6-15
모든 영화에 대해 상영시간을 **장편(>130분), 중편(100~130분), 단편(<100분)** 으로 구분해서 (제목, 분류)로 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title, m.runtime,
  CASE 
    WHEN m.runtime > 130 THEN '장편'
    WHEN m.runtime >= 100 THEN '중편'
    ELSE '단편'
  END AS 분류
ORDER BY m.runtime DESC;
```

**해설:**
- `CASE WHEN ... THEN ... [WHEN ... THEN ...] [ELSE ...] END`: 조건 분기.
- 위에서 아래로 검사하며 처음 만족하는 분기로 갑니다.
- SQL의 `CASE`와 동일하며, Cypher에서 가장 자주 쓰이는 조건 표현 방식.

</details>

#### 문제 6-16
모든 노드를 라벨별로 그룹화해서 **각 라벨의 노드 수**를 반환하세요. (`labels(n)` 활용)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (n)
UNWIND labels(n) AS label
RETURN label, count(*) AS 개수
ORDER BY 개수 DESC;
```

**해설:**
- `labels(n)`은 리스트이므로, 한 노드가 여러 라벨을 가질 수도 있습니다.
- `UNWIND`로 펼친 후 그룹핑하면, 라벨별 누적 카운트가 나옵니다.
- 그래프 데이터의 전체 현황을 한눈에 보는 점검 쿼리 — 매우 자주 씁니다.

</details>

#### 문제 6-17
모든 관계의 **타입 이름**과 그 관계 개수를 집계해서 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH ()-[r]->()
RETURN type(r) AS 관계타입, count(*) AS 개수
ORDER BY 개수 DESC;
```

**해설:**
- `type(r)`: 관계의 타입 이름 문자열(`'DIRECTED'`, `'ACTED_IN'` 등).
- 라벨 집계의 관계 버전. 데이터 점검 시 라벨 카운트와 함께 거의 항상 같이 씁니다.

</details>

---

## 🎯 종합 실전 문제

### 종합 문제 1
다음 파이프라인을 한 쿼리로 작성하세요:
- 영화별 평균 평점을 구해서, **평균 4점 이상**인 영화만 골라낸 뒤
- 각 영화에 대해 **출연 배우 수**와 **장르 리스트**를 함께 반환
- 평균 평점이 높은 순으로 정렬, **상위 5개**

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)<-[r:RATED]-(:User)
WITH m, avg(r.rating) AS avgR
WHERE avgR >= 4
CALL (m) {
  MATCH (m)<-[:ACTED_IN]-(a:Person)
  RETURN count(a) AS actorCount
}
CALL (m) {
  MATCH (m)-[:IN_GENRE]->(g:Genre)
  RETURN collect(g.name) AS genres
}
RETURN m.title AS 영화, avgR AS 평균평점, actorCount AS 배우수, genres AS 장르
ORDER BY avgR DESC
LIMIT 5;
```

**해설:** `WITH` + `WHERE` + 2개의 `CALL` 서브쿼리를 조합한 대시보드형 쿼리. 6번 종합문제와 비슷한 구조이지만 `CALL`을 적극 활용해 가독성을 개선했습니다.

</details>

### 종합 문제 2
다음을 한 쿼리로 처리하세요:
- 파라미터 `$director`로 감독 이름을 받아
- 그 감독이 연출한 영화의 (제목, 개봉연도, 평균 평점, 평가 수)를 반환
- 평가가 없는 영화도 결과에 포함 (평점은 `null`이 아니라 `'N/A'` 로)
- 개봉연도 내림차순

```
:param director => '봉준호'
```

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person {name: $director})-[:DIRECTED]->(m:Movie)
OPTIONAL MATCH (m)<-[r:RATED]-(:User)
WITH m, avg(r.rating) AS avgR, count(r) AS cnt
RETURN m.title AS 영화, 
       m.released AS 개봉, 
       coalesce(toString(round(avgR, 2)), 'N/A') AS 평균평점,
       cnt AS 평가수
ORDER BY m.released DESC;
```

**해설:**
- 파라미터(`$director`) + `OPTIONAL MATCH` + `coalesce` + `toString` + `round` 의 조합.
- 평가 없는 영화의 `avg(r.rating)`은 `null`이 되는데, `toString(null) = null`이므로 `coalesce`로 `'N/A'` 대체.
- 실무 보고서 쿼리의 흔한 형태.

</details>

---

## 📌 마무리

지금까지 다룬 추가 6개 주제 (`UNWIND`, 인덱스/제약조건, 리스트 컴프리헨션·술어 함수, `CALL` 서브쿼리, 파라미터, 주요 함수)를 Part 1의 12개 기초 구문과 함께 익히면, **실무 Cypher 쿼리의 95% 이상**을 자신 있게 작성할 수 있습니다.

**다음 학습 추천 (Graph RAG 관점):**

1. **벡터 인덱스 & 임베딩 검색**
   ```cypher
   CALL db.index.vector.queryNodes('movieEmbeddings', 5, $queryVector)
   ```
2. **전문 검색 (Full-text Search)**
   ```cypher
   CALL db.index.fulltext.queryNodes('movieTitles', $searchText)
   ```
3. **APOC 라이브러리** — 배치 처리(`apoc.periodic.iterate`), JSON 로딩, 문자열 처리 등
4. **Neo4j Python 드라이버** — Cypher와 LLM을 연결하는 실제 코드
5. **LangChain·LlamaIndex의 Neo4j 통합** — Graph RAG 파이프라인 구축

> 💪 **연습 팁**: 12 + 6 개 주제를 한 번 학습한 뒤, **데이터셋을 직접 자기 도메인(논문, 인사 정보, 제품 카탈로그 등)으로 바꿔서** 동일한 문제 패턴을 재구성해보면 체득이 빨라집니다.
