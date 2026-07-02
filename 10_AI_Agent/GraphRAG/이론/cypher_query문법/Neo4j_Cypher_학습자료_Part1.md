# Neo4j Cypher 문법 마스터하기

> 처음 Cypher를 접하는 학습자를 위한 단계별 실습 자료

---

## 📚 목차

0. [실습 데이터셋 구축](#0-실습-데이터셋-구축)
1. [CREATE - 노드와 관계 생성](#1-create---노드와-관계-생성)
2. [MATCH - 패턴 매칭](#2-match---패턴-매칭)
3. [WHERE - 조건 필터링](#3-where---조건-필터링)
4. [RETURN - 결과 반환](#4-return---결과-반환)
5. [ORDER BY / LIMIT / SKIP - 정렬과 페이징](#5-order-by--limit--skip---정렬과-페이징)
6. [집계 함수 (Aggregation)](#6-집계-함수-aggregation)
7. [WITH - 쿼리 체이닝](#7-with---쿼리-체이닝)
8. [OPTIONAL MATCH - 선택적 매칭](#8-optional-match---선택적-매칭)
9. [SET - 속성 업데이트](#9-set---속성-업데이트)
10. [DELETE / DETACH DELETE - 삭제](#10-delete--detach-delete---삭제)
11. [MERGE - 생성 또는 매칭](#11-merge---생성-또는-매칭)
12. [경로(Path) 쿼리](#12-경로path-쿼리)

---

## 0. 실습 데이터셋 구축

### 📖 데이터셋 설명

영화 스트리밍 서비스를 모델링한 그래프입니다. Cypher 학습에 필요한 거의 모든 패턴(1:1, 1:N, N:M, 속성을 가진 관계, 자기 참조 관계 등)을 포함하고 있습니다.

### 🗂️ 스키마

**노드(Node) 종류:**

| 라벨 | 속성 | 설명 |
|------|------|------|
| `Movie` | title, released, runtime | 영화 |
| `Person` | name, born, nationality | 감독/배우/작가 |
| `Genre` | name | 장르 |
| `Studio` | name, founded | 제작사 |
| `User` | name, age, joinYear | 서비스 사용자 |

**관계(Relationship) 종류:**

| 관계 | 시작 → 끝 | 속성 | 설명 |
|------|----------|------|------|
| `:DIRECTED` | Person → Movie | - | 감독 |
| `:ACTED_IN` | Person → Movie | role | 출연 (역할명 포함) |
| `:WROTE` | Person → Movie | - | 각본 |
| `:IN_GENRE` | Movie → Genre | - | 장르 분류 |
| `:PRODUCED_BY` | Movie → Studio | - | 제작사 |
| `:RATED` | User → Movie | rating, date | 사용자 평점 |
| `:FRIENDS_WITH` | User → User | - | 친구 관계 |
| `:FOLLOWS` | User → Person | - | 인물 팔로우 |

### 🛠️ 데이터 생성 스크립트

> Neo4j Browser나 cypher-shell에서 아래 스크립트를 **한 번에 실행**하세요.

```cypher
// =========================================
// 1) 기존 데이터 초기화 (선택사항)
// =========================================
MATCH (n) DETACH DELETE n;

// =========================================
// 2) Movie 노드 생성
// CREATE (변수: 라벨 {속성명:속성값}) -> 변수는 생성한 노드를 현재 세션에서 사용할 때 준다. 여기서는 뒤에 관계를 생성할 때 참조하기 위해서 지정했다. 단순히 만들기만 할 거면 생략 가능하다.
// =========================================
CREATE (parasite:Movie {title: '기생충', released: 2019, runtime: 132})
CREATE (oldboy:Movie {title: '올드보이', released: 2003, runtime: 120})
CREATE (memories:Movie {title: '살인의 추억', released: 2003, runtime: 132})
CREATE (mother:Movie {title: '마더', released: 2009, runtime: 129})
CREATE (busan:Movie {title: '부산행', released: 2016, runtime: 118})
CREATE (crime:Movie {title: '범죄도시', released: 2017, runtime: 121})
CREATE (insider:Movie {title: '내부자들', released: 2015, runtime: 130})
CREATE (train:Movie {title: '설국열차', released: 2013, runtime: 126})
CREATE (handmaiden:Movie {title: '아가씨', released: 2016, runtime: 145})
CREATE (decision:Movie {title: '헤어질 결심', released: 2022, runtime: 138})
CREATE (namsan:Movie {title: '남산의 부장들', released: 2022, runtime: 103})
CREATE (king:Movie {title: '왕과 사는 남자', released: 2026, runtime: 107})

// =========================================
// 3) Person 노드 생성 (감독)
// =========================================
CREATE (bong:Person {name: '봉준호', born: 1969, nationality: '한국'})
CREATE (park:Person {name: '박찬욱', born: 1963, nationality: '한국'})
CREATE (yeon:Person {name: '연상호', born: 1978, nationality: '한국'})
CREATE (kang:Person {name: '강윤성', born: 1973, nationality: '한국'})
CREATE (woo:Person {name: '우민호', born: 1971, nationality: '한국'})

// =========================================
// 4) Person 노드 생성 (배우)
// =========================================
CREATE (song:Person {name: '송강호', born: 1967, nationality: '한국'})
CREATE (lee_byung:Person {name: '이병헌', born: 1970, nationality: '한국'})
CREATE (choi:Person {name: '최민식', born: 1962, nationality: '한국'})
CREATE (ma:Person {name: '마동석', born: 1971, nationality: '한국'})
CREATE (gong:Person {name: '공유', born: 1979, nationality: '한국'})
CREATE (kim_hyeja:Person {name: '김혜자', born: 1941, nationality: '한국'})
CREATE (won:Person {name: '원빈', born: 1977, nationality: '한국'})
CREATE (cho:Person {name: '조여정', born: 1981, nationality: '한국'})
CREATE (kim_minhee:Person {name: '김민희', born: 1982, nationality: '한국'})
CREATE (tang:Person {name: '탕웨이', born: 1979, nationality: '중국'})
CREATE (park_hae:Person {name: '박해일', born: 1977, nationality: '한국'})
CREATE (chris:Person {name: 'Chris Evans', born: 1981, nationality: '미국'})

// =========================================
// 5) Genre 노드 생성
// =========================================
CREATE (thriller:Genre {name: '스릴러'})
CREATE (drama:Genre {name: '드라마'})
CREATE (action:Genre {name: '액션'})
CREATE (comedy:Genre {name: '코미디'})
CREATE (sf:Genre {name: 'SF'})
CREATE (mystery:Genre {name: '미스터리'})
CREATE (romance:Genre {name: '로맨스'})

// =========================================
// 6) Studio 노드 생성
// =========================================
CREATE (cj:Studio {name: 'CJ ENM', founded: 1995})
CREATE (showbox:Studio {name: '쇼박스', founded: 1999})
CREATE (next:Studio {name: 'NEXT 엔터테인먼트', founded: 2008})

// =========================================
// 7) User 노드 생성
// =========================================
CREATE (u1:User {name: '김철수', age: 28, joinYear: 2020})
CREATE (u2:User {name: '이영희', age: 32, joinYear: 2019})
CREATE (u3:User {name: '박민수', age: 25, joinYear: 2021})
CREATE (u4:User {name: '최지은', age: 30, joinYear: 2018})
CREATE (u5:User {name: '정수진', age: 27, joinYear: 2022})
CREATE (u6:User {name: '한지훈', age: 35, joinYear: 2017})
CREATE (u7:User {name: '이유정', age: 21, joinYear: 2025})
CREATE (u8:User {name: '주민호', age: 27, joinYear: 2025})

// =========================================
// 8) DIRECTED 관계
// =========================================
CREATE (bong)-[:DIRECTED]->(parasite)
CREATE (bong)-[:DIRECTED]->(memories)
CREATE (bong)-[:DIRECTED]->(mother)
CREATE (bong)-[:DIRECTED]->(train)
CREATE (park)-[:DIRECTED]->(oldboy)
CREATE (park)-[:DIRECTED]->(handmaiden)
CREATE (park)-[:DIRECTED]->(decision)
CREATE (yeon)-[:DIRECTED]->(busan)
CREATE (kang)-[:DIRECTED]->(crime)
CREATE (woo)-[:DIRECTED]->(insider)
CREATE (woo)-[:DIRECTED]->(namsan)

// =========================================
// 9) ACTED_IN 관계 (역할명 포함)
// =========================================
CREATE (song)-[:ACTED_IN {role: '기택'}]->(parasite)
CREATE (song)-[:ACTED_IN {role: '두만'}]->(memories)
CREATE (song)-[:ACTED_IN {role: '남궁민수'}]->(train)
CREATE (cho)-[:ACTED_IN {role: '연교'}]->(parasite)
CREATE (choi)-[:ACTED_IN {role: '오대수'}]->(oldboy)
CREATE (kim_hyeja)-[:ACTED_IN {role: '엄마'}]->(mother)
CREATE (won)-[:ACTED_IN {role: '도준'}]->(mother)
CREATE (gong)-[:ACTED_IN {role: '서석우'}]->(busan)
CREATE (ma)-[:ACTED_IN {role: '윤상화'}]->(busan)
CREATE (ma)-[:ACTED_IN {role: '마석도'}]->(crime)
CREATE (lee_byung)-[:ACTED_IN {role: '안상구'}]->(insider)
CREATE (kim_minhee)-[:ACTED_IN {role: '히데코'}]->(handmaiden)
CREATE (tang)-[:ACTED_IN {role: '서래'}]->(decision)
CREATE (park_hae)-[:ACTED_IN {role: '해준'}]->(decision)
CREATE (chris)-[:ACTED_IN {role: '커티스'}]->(train)
CREATE (lee_byung)-[:ACTED_IN {role: '김규평'}]->(namsan)

// =========================================
// 10) IN_GENRE 관계
// =========================================
CREATE (parasite)-[:IN_GENRE]->(thriller)
CREATE (parasite)-[:IN_GENRE]->(drama)
CREATE (oldboy)-[:IN_GENRE]->(thriller)
CREATE (oldboy)-[:IN_GENRE]->(mystery)
CREATE (memories)-[:IN_GENRE]->(thriller)
CREATE (memories)-[:IN_GENRE]->(drama)
CREATE (mother)-[:IN_GENRE]->(drama)
CREATE (mother)-[:IN_GENRE]->(mystery)
CREATE (busan)-[:IN_GENRE]->(action)
CREATE (busan)-[:IN_GENRE]->(thriller)
CREATE (crime)-[:IN_GENRE]->(action)
CREATE (crime)-[:IN_GENRE]->(comedy)
CREATE (insider)-[:IN_GENRE]->(drama)
CREATE (train)-[:IN_GENRE]->(sf)
CREATE (train)-[:IN_GENRE]->(action)
CREATE (handmaiden)-[:IN_GENRE]->(drama)
CREATE (handmaiden)-[:IN_GENRE]->(romance)
CREATE (decision)-[:IN_GENRE]->(romance)
CREATE (decision)-[:IN_GENRE]->(mystery)
CREATE (namsan)-[:IN_GENRE]->(mystery)

// =========================================
// 11) PRODUCED_BY 관계
// =========================================
CREATE (parasite)-[:PRODUCED_BY]->(cj)
CREATE (memories)-[:PRODUCED_BY]->(cj)
CREATE (train)-[:PRODUCED_BY]->(cj)
CREATE (oldboy)-[:PRODUCED_BY]->(showbox)
CREATE (busan)-[:PRODUCED_BY]->(next)
CREATE (crime)-[:PRODUCED_BY]->(showbox)
CREATE (insider)-[:PRODUCED_BY]->(showbox)
CREATE (handmaiden)-[:PRODUCED_BY]->(cj)
CREATE (decision)-[:PRODUCED_BY]->(cj)
CREATE (mother)-[:PRODUCED_BY]->(cj)

// =========================================
// 12) RATED 관계 (평점 포함)
// =========================================
CREATE (u1)-[:RATED {rating: 5, date: '2024-01-15'}]->(parasite)
CREATE (u1)-[:RATED {rating: 4, date: '2024-02-20'}]->(busan)
CREATE (u1)-[:RATED {rating: 3, date: '2024-03-10'}]->(crime)
CREATE (u2)-[:RATED {rating: 5, date: '2024-01-10'}]->(parasite)
CREATE (u2)-[:RATED {rating: 5, date: '2024-02-05'}]->(oldboy)
CREATE (u2)-[:RATED {rating: 4, date: '2024-03-01'}]->(decision)
CREATE (u3)-[:RATED {rating: 4, date: '2024-04-12'}]->(busan)
CREATE (u3)-[:RATED {rating: 5, date: '2024-04-15'}]->(crime)
CREATE (u3)-[:RATED {rating: 2, date: '2024-04-20'}]->(insider)
CREATE (u4)-[:RATED {rating: 5, date: '2024-01-25'}]->(handmaiden)
CREATE (u4)-[:RATED {rating: 4, date: '2024-02-15'}]->(decision)
CREATE (u4)-[:RATED {rating: 5, date: '2024-03-05'}]->(parasite)
CREATE (u5)-[:RATED {rating: 3, date: '2024-04-01'}]->(busan)
CREATE (u5)-[:RATED {rating: 4, date: '2024-04-10'}]->(memories)
CREATE (u6)-[:RATED {rating: 5, date: '2024-02-28'}]->(oldboy)
CREATE (u6)-[:RATED {rating: 4, date: '2024-03-15'}]->(mother)
CREATE (u6)-[:RATED {rating: 3, date: '2024-04-22'}]->(train)

// =========================================
// 13) FRIENDS_WITH 관계
// =========================================
CREATE (u1)-[:FRIENDS_WITH]->(u2)
CREATE (u2)-[:FRIENDS_WITH]->(u1)
CREATE (u1)-[:FRIENDS_WITH]->(u3)
CREATE (u3)-[:FRIENDS_WITH]->(u1)
CREATE (u2)-[:FRIENDS_WITH]->(u4)
CREATE (u4)-[:FRIENDS_WITH]->(u2)
CREATE (u3)-[:FRIENDS_WITH]->(u5)
CREATE (u5)-[:FRIENDS_WITH]->(u3)
CREATE (u4)-[:FRIENDS_WITH]->(u6)
CREATE (u6)-[:FRIENDS_WITH]->(u4)

// =========================================
// 14) FOLLOWS 관계 (사용자 → 인물)
// =========================================
CREATE (u1)-[:FOLLOWS]->(bong)
CREATE (u1)-[:FOLLOWS]->(song)
CREATE (u2)-[:FOLLOWS]->(park)
CREATE (u2)-[:FOLLOWS]->(bong)
CREATE (u3)-[:FOLLOWS]->(ma)
CREATE (u4)-[:FOLLOWS]->(park)
CREATE (u4)-[:FOLLOWS]->(kim_minhee)
CREATE (u6)-[:FOLLOWS]->(choi)

// =========================================
// 15) WROTE 관계 (각본)
// =========================================
CREATE (bong)-[:WROTE]->(parasite)
CREATE (bong)-[:WROTE]->(memories)
CREATE (bong)-[:WROTE]->(mother)
CREATE (park)-[:WROTE]->(oldboy)
CREATE (park)-[:WROTE]->(handmaiden)
CREATE (yeon)-[:WROTE]->(busan);
```


---

## 1. CREATE - 노드와 관계 생성

### 📖 구문 설명

`CREATE` 절은 새로운 노드와 관계를 생성합니다. Cypher의 가장 기본이 되는 쓰기(write) 명령어입니다.

**기본 문법:**

```cypher
// 노드 생성
CREATE (변수:라벨 {속성키: 속성값, ...})

// 관계 생성 (양 노드가 이미 존재할 때)
MATCH (a), (b)
WHERE 조건
CREATE (a)-[:관계타입 {속성}]->(b)

// 노드와 관계 한 번에 생성
CREATE (a:Label1 {...})-[:REL_TYPE]->(b:Label2 {...})
```

**핵심 규칙:**

- 노드는 `()` 소괄호, 관계는 `[]` 대괄호로 표현
- 라벨은 `:` 콜론으로 시작
- 관계는 반드시 방향(`->` 또는 `<-`)이 있어야 함 (방향 없는 관계는 `CREATE`에서 불가)
- 변수명은 같은 쿼리 안에서 재참조 가능

### 💡 예제

```cypher
// 예제 1: 단순 노드 생성
CREATE (m:Movie {title: '괴물', released: 2006, runtime: 119});

// 예제 2: 두 노드와 그 사이의 관계를 한 번에 생성
CREATE (p:Person {name: '봉준호'})-[:DIRECTED]->(m:Movie {title: '괴물'});

// 예제 3: 기존 노드 사이에 관계만 추가
MATCH (p:Person {name: '송강호'}), (m:Movie {title: '괴물'})
CREATE (p)-[:ACTED_IN {role: '강두'}]->(m);
```

### ✏️ 연습문제

> **준비:** 아래 문제는 위에서 만든 데이터셋을 기반으로 합니다. 단, **새로운 데이터를 추가**하는 문제이므로 풀고 나면 데이터가 변경될 수 있습니다.

#### 문제 1-1
`Person` 라벨을 가진 새로운 인물 노드를 생성하세요. 이름(name)은 `'나홍진'`, 출생연도(born)는 `1974`, 국적(nationality)은 `'한국'` 입니다.

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE (p:Person {name: '나홍진', born: 1974, nationality: '한국'});
```

**해설:** 노드 생성의 가장 기본 형태입니다. `CREATE` 키워드 뒤에 소괄호를 사용해 노드를 정의하고, `:Person`으로 라벨을, 중괄호 `{}` 안에 키-값 쌍으로 속성을 지정합니다.

</details>

#### 문제 1-2
`Movie` 노드와 그것을 감독한 `Person` 노드, 그리고 둘 사이의 `:DIRECTED` 관계를 한 번의 쿼리로 모두 생성하세요. 영화 정보는 `title: '왕과 사는 남자', released: 2026, runtime: 117`이고, 감독은 `'장항준'`로 `born:1969, nationality: '한국'` 입니다.

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE (na:Person {name: '나홍진', born: 1974, nationality: '한국'})
       -[:DIRECTED]->
       (gokseong:Movie {title: '곡성', released: 2016, runtime: 156});
```

**해설:** 노드와 관계를 한 줄에 연결해서 만들 수 있습니다. 변수(`na`, `gokseong`)는 같은 쿼리 안에서만 유효합니다.

</details>

#### 문제 1-3
이미 존재하는 영화 `'기생충'`과 배우 `'송강호'` 사이에 `:ACTED_IN` 관계를 추가하되, 관계 속성으로 `role: '기택'`, `salary: 1000000000`을 함께 저장하세요. (실제로는 이미 있을 수 있지만 연습 목적이므로 추가)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person {name: '송강호'}), (m:Movie {title: '기생충'})
CREATE (p)-[r:ACTED_IN {role: '기택', salary: 1000000000}]->(m)
RETURN r;
```

**해설:**
- 기존 노드들 사이에 관계만 추가할 때는 먼저 `MATCH`로 노드를 찾아야 합니다.
- 관계에도 노드처럼 속성을 부여할 수 있습니다 — `[변수:타입 {속성들}]` 형태입니다.
- 관계 변수 `r`을 만들어 두면 `RETURN`에서 확인할 수 있습니다.

</details>

#### 문제 1-4
새로운 사용자 노드 3개를 한 번의 쿼리로 동시에 생성하세요. (`이재현`, `30살`, `2023가입` / `손미영`, `26살`, `2024가입` / `김도현`, `41살`, `2015가입`)

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE 
  (:User {name: '이재현', age: 30, joinYear: 2023}),
  (:User {name: '손미영', age: 26, joinYear: 2024}),
  (:User {name: '김도현', age: 41, joinYear: 2015});
```

**해설:** `CREATE` 절 안에서 콤마 `,`로 여러 패턴을 연결하면 한 번에 여러 개체를 만들 수 있습니다. 변수명이 필요 없으면 `:User`처럼 변수 없이 라벨만 쓰면 됩니다.

</details>

#### 문제 1-5
`'곡성'` 영화에 `:IN_GENRE` 관계로 `'스릴러'`와 `'미스터리'` 두 개의 장르를 동시에 연결하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie {title: '곡성'})
MATCH (g1:Genre {name: '스릴러'}), (g2:Genre {name: '미스터리'})
CREATE (m)-[:IN_GENRE]->(g1),
       (m)-[:IN_GENRE]->(g2);
```

또는 `MATCH`를 한 줄로:

```cypher
MATCH (m:Movie {title: '곡성'}),
      (g1:Genre {name: '스릴러'}),
      (g2:Genre {name: '미스터리'})
CREATE (m)-[:IN_GENRE]->(g1),
       (m)-[:IN_GENRE]->(g2);
```

**해설:** 여러 노드를 미리 매칭한 뒤 `CREATE` 안에서 콤마로 여러 관계를 한 번에 만들 수 있습니다. 동일한 시작 노드에서 여러 관계를 만드는 흔한 패턴입니다.

</details>

#### 문제 1-6
한 줄의 쿼리로 다음을 모두 생성하세요: 2017년 개봉한 상영시간 118분짜리 영화 `'살인자의 기억법'` 영화 노드 → 1969년생 한국 국적의 `'원신연'` 감독 노드 → 두 노드 사이의 `:DIRECTED` 관계.

<details>
<summary>💡 정답 보기</summary>

```cypher
CREATE (d:Person {name: '원신연', born: 1969, nationality: '한국'})
       -[:DIRECTED]->
       (m:Movie {title: '살인자의 기억법', released: 2017, runtime: 118});
```

**해설:** 한 패턴 안에서 노드 생성과 관계 생성을 동시에 할 수 있습니다. 단, 이렇게 만드는 노드는 모두 새로 생성되므로 기존 노드와 중복될 수 있습니다(중복 방지가 필요하면 `MERGE` 사용 — 11번 참고).

</details>

---

## 2. MATCH - 패턴 매칭

### 📖 구문 설명

`MATCH` 절은 그래프에서 특정 패턴(노드, 관계, 경로)을 **조회하는** 읽기(read) 명령어입니다. SQL의 `SELECT ... FROM`에 해당합니다.

**기본 문법:**

```cypher
// 기본구문
MATCH 패턴
[WHERE 조건1 AND/OR 조건2 ...]
RETURN ...
[ORDER BY 정렬기준컬럼 ASC|DESC]

// 모든 노드 찾기
MATCH (n) RETURN n;

// 특정 라벨의 노드 찾기
MATCH (m:Movie) RETURN m;

// 속성 조건이 있는 노드 찾기
MATCH (m:Movie {title: '기생충'}) RETURN m;

// 관계 패턴 찾기
MATCH (p:Person)-[r:DIRECTED]->(m:Movie) RETURN p, r, m;

// 관계 전체를 변수에 저장해서 반환
MATCH path = (:Person)-[:DIRECTED]->(:Movie) RETURN path
```

**핵심 포인트:**

- `MATCH`만으로는 결과를 보여주지 않으며 항상 `RETURN`(또는 쓰기 절)과 함께 사용
- 노드/관계 자체에 변수를 붙여야 이후에 사용 가능
- 관계 방향은 `->`, `<-` 으로 지정 (`-` 양방향)

### 💡 예제

```cypher
// 예제 1: 봉준호가 감독한 모든 영화의 제목과 개봉년도
MATCH (p:Person {name: '봉준호'})-[:DIRECTED]->(m:Movie)
RETURN m.title, m.released;

// 예제 2: 송강호가 출연한 영화와 그의 역할
MATCH (p:Person {name: '송강호'})-[r:ACTED_IN]->(m:Movie)
RETURN m.title, r.role;

// 예제 3: 두 단계 패턴 - 봉준호 영화에 출연한 배우들
MATCH (bong:Person {name: '봉준호'})-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(actor:Person)
RETURN DISTINCT actor.name;
```

### ✏️ 연습문제

#### 문제 2-1
모든 `Movie` 노드의 `title`과 `released`를 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title, m.released;
```

**해설:** 가장 기본적인 `MATCH`. `(m:Movie)`는 "라벨이 Movie인 모든 노드"를 의미합니다. 변수 `m`을 붙여야 `RETURN`에서 속성에 접근(`m.title`)할 수 있습니다.

</details>

#### 문제 2-2
`'박찬욱'` 감독이 만든 모든 영화의 제목을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person {name: '박찬욱'})-[:DIRECTED]->(m:Movie)
RETURN m.title;
```

**해설:** 시작 노드(`Person`)의 속성으로 필터링하고, `:DIRECTED` 관계를 따라 영화 노드에 도달합니다. 화살표 방향 `->`이 매우 중요합니다 — `Person`이 영화를 감독했다는 의미니까 `Person → Movie` 방향이어야 합니다.

</details>

#### 문제 2-3
`'기생충'` 영화에 출연한 모든 배우의 이름과 그들이 맡은 역할을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {title: '기생충'})
RETURN p.name, r.role;
```

**해설:** 관계에도 변수(`r`)를 붙이면 관계의 속성(`r.role`)에 접근할 수 있습니다. 이번엔 끝 노드(`Movie`)의 속성으로 필터링했습니다.

</details>

#### 문제 2-4
`'송강호'` 배우와 함께 같은 영화에 출연한 다른 배우들의 이름을 조회하세요. (단, 송강호 본인은 제외)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (song:Person {name: '송강호'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coactor:Person)
WHERE coactor.name <> '송강호'
RETURN DISTINCT coactor.name, m.title;
```

**해설:**
- 두 화살표가 `Movie`를 가운데에 두고 양쪽으로 향합니다 (`->...<-`).
- `DISTINCT`는 중복을 제거합니다 (같은 배우가 여러 영화에 같이 나오면 중복될 수 있음).
- 자기 자신도 패턴에 매칭되므로 `WHERE`로 제외합니다.

</details>

#### 문제 2-5
`'액션'` 장르에 속하는 모든 영화의 제목을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {name: '액션'})
RETURN m.title;
```

**해설:** 관계 방향을 잘 살펴보세요. `Movie → Genre` 입니다 (영화가 장르에 속함). 화살표를 거꾸로 그리면 결과가 비어버립니다.

</details>

#### 문제 2-6
`'CJ ENM'`에서 제작한 영화 중 `'봉준호'`가 감독한 영화의 제목을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (bong:Person {name: '봉준호'})-[:DIRECTED]->(m:Movie)-[:PRODUCED_BY]->(s:Studio {name: 'CJ ENM'})
RETURN m.title;
```

**해설:** 두 개의 관계를 체이닝한 패턴입니다. `m` 노드가 두 패턴의 공통점이 됩니다 — "봉준호가 감독했고 동시에 CJ에서 제작한" 영화.

</details>

#### 문제 2-7
사용자 `'김철수'`의 친구의 친구(2단계 거리)들을 모두 찾으세요. (자기 자신과 직접 친구 제외)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (me:User {name: '김철수'})-[:FRIENDS_WITH]->(friend:User)-[:FRIENDS_WITH]->(fof:User)
WHERE fof <> me 
  AND NOT (me)-[:FRIENDS_WITH]->(fof)
RETURN DISTINCT fof.name;
```

**해설:**
- 관계를 두 번 따라가는 다단계 패턴입니다.
- `WHERE fof <> me`는 me인 "김철수를 제외"시킨다. me 와 friend 관계에서 다시 fof 로 FRIEND_WITH 관계가 연결되므로 자기 자신(김철수)도 조회된다. 
- `WHERE NOT (me)-[:FRIENDS_WITH]->(fof)`는 "김철수와 직접 친구인 관계는 제외" 라는 뜻이다.
- 친구 추천 시스템의 기본 형태입니다.

</details>

---

## 3. WHERE - 조건 필터링

### 📖 구문 설명

`WHERE` 절은 `MATCH` 결과에 추가 조건을 붙여 필터링합니다. SQL의 `WHERE`와 거의 동일합니다.

**기본 문법:**

```cypher
MATCH 패턴
WHERE 조건1 AND/OR 조건2 ...
RETURN ...
ORDER BY 정렬기준컬럼 ASC|DESC
```

**자주 쓰는 비교/연산자:**

| 연산자 | 의미 |
|--------|------|
| `=`, `<>` | 같다 / 다르다 |
| `<`, `<=`, `>`, `>=` | 비교 |
| `AND`, `OR`, `NOT` | 논리 연산 |
| `IN [...]` | 리스트 포함 |
| `STARTS WITH`, `ENDS WITH`, `CONTAINS` | 문자열 검색 |
| `=~` | 정규식 매칭 |
| `IS NULL`, `IS NOT NULL` | 널 체크 |

> 💡 **MATCH의 인라인 필터 vs WHERE의 차이**  
> `MATCH (m:Movie {title: '기생충'})` 처럼 인라인으로 쓸 수도 있고, `MATCH (m:Movie) WHERE m.title = '기생충'` 처럼 따로 쓸 수도 있습니다. 결과는 동일하지만, 복잡한 조건(범위, OR, 함수 사용 등)은 `WHERE`로 써야 합니다.

### 💡 예제

```cypher
// 예제 1: 2010년 이후 개봉한 영화
MATCH (m:Movie)
WHERE m.released >= 2010
RETURN m.title, m.released;

// 예제 2: 제목에 '의'가 들어간 영화
MATCH (m:Movie)
WHERE m.title CONTAINS '의'
RETURN m.title;

// 예제 3: 미국 국적이거나 1970년대생인 인물
MATCH (p:Person)
WHERE p.nationality = '미국' OR (p.born >= 1970 AND p.born < 1980)
RETURN p.name, p.nationality, p.born;
```

### ✏️ 연습문제

#### 문제 3-1
`runtime`이 130분 이상인 모든 영화의 제목과 상영시간을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
WHERE m.runtime >= 130
RETURN m.title, m.runtime;
```

**해설:** 숫자 비교의 가장 기본 형태. `>=`는 "이상", `<=`는 "이하" 입니다.

</details>

#### 문제 3-2
2010년대(2010~2019년)에 개봉한 영화의 제목과 개봉연도를 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
WHERE m.released >= 2010 AND m.released <= 2019
RETURN m.title, m.released;
```

**해설:** SQL의 `BETWEEN`은 Cypher에 없으므로 `AND`로 범위를 표현합니다.

</details>

#### 문제 3-3
이름이 `'김'` 으로 시작하는 모든 `Person`을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)
WHERE p.name STARTS WITH '김'
RETURN p.name;
```

**해설:** 문자열 검색 연산자.
- `STARTS WITH`: 시작 일치
- `ENDS WITH`: 끝 일치
- `CONTAINS`: 부분 문자열

</details>

#### 문제 3-4
국적이 `'한국'` 또는 `'중국'`인 인물 중에서 1980년 이후 출생한 사람의 이름과 출생연도를 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)
WHERE p.nationality IN ['한국', '중국']
  AND p.born >= 1980
RETURN p.name, p.nationality, p.born;
```

**해설:** `IN [...]`은 SQL의 `IN`과 동일하게 리스트 멤버십을 체크합니다. `OR` 여러 개를 쓰는 것보다 깔끔합니다.

</details>

#### 문제 3-5
사용자가 평점 4점 **이상**으로 평가한 영화의 (사용자 이름, 영화 제목, 평점) 을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)-[r:RATED]->(m:Movie)
WHERE r.rating >= 4
RETURN u.name, m.title, r.rating;
```

**해설:** 관계 속성(`r.rating`)도 `WHERE`에서 동일하게 필터링할 수 있습니다.

</details>

#### 문제 3-6
영화 제목에 `'살인'` 이 포함되거나, 개봉연도가 2020년 이후인 영화를 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
WHERE m.title CONTAINS '살인' OR m.released >= 2020
RETURN m.title, m.released;
```

**해설:** `OR`로 다양한 조건을 결합합니다. 우선순위가 헷갈릴 땐 괄호 `( )`를 적극 활용하세요.

</details>

#### 문제 3-7
`'스릴러'` 장르 영화 중 2010년 이후에 개봉했고, 상영시간이 120분을 초과하는 영화의 제목을 조회하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {name: '스릴러'})
WHERE m.released >= 2010 AND m.runtime > 120
RETURN m.title, m.released, m.runtime;
```

**해설:** 패턴 매칭과 속성 필터를 함께 사용. 라벨/관계 매칭은 패턴(`MATCH`)에서, 값 비교는 `WHERE`에서 처리하는 것이 일반적입니다.

</details>

#### 문제 3-8
어떤 사용자도 평가하지 **않은** 영화의 제목을 조회하세요.  
(힌트: `WHERE NOT (패턴)` 활용)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
WHERE NOT ()-[:RATED]->(m)
RETURN m.title;
```

또는 더 명시적으로:

```cypher
MATCH (m:Movie)
WHERE NOT EXISTS { (:User)-[:RATED]->(m) }
RETURN m.title;
```

**해설:**
- Cypher에서 가장 강력한 기능 중 하나: `WHERE` 안에 **패턴**을 직접 쓸 수 있습니다.
- `NOT ()-[:RATED]->(m)`은 "어떤 노드에서도 m으로 향하는 :RATED 관계가 없다"라는 의미입니다.
- 빈 괄호 `()`는 "아무 노드나"를 뜻합니다.

</details>

---

## 4. RETURN - 결과 반환

### 📖 구문 설명

`RETURN` 절은 쿼리의 결과를 어떻게 반환할지 결정합니다. 단순한 노드 반환부터 표현식, 별칭, 중복 제거까지 가능합니다.

**기본 문법:**

```cypher
RETURN 변수, 변수.속성, 표현식 [AS 별칭]
RETURN DISTINCT ...   -- 중복 제거
```

**반환 가능한 것들:**

- 노드 자체 (`RETURN n`)
- 속성 (`RETURN n.name`)
- 관계 (`RETURN r`)
- 계산 결과 (`RETURN n.born + 10`)
- 문자열 결합 (`RETURN n.firstName + ' ' + n.lastName`)
- 컬렉션 (`RETURN [n.name, n.born]`)

### 💡 예제

```cypher
// 예제 1: 노드 자체 반환
MATCH (m:Movie {title: '기생충'})
RETURN m;

// 예제 2: 속성과 별칭
MATCH (m:Movie)
RETURN m.title AS 제목, m.released AS 개봉연도;

// 예제 3: 계산식
MATCH (p:Person)
WHERE p.born IS NOT NULL
RETURN p.name, 2026 - p.born AS 나이;

// 예제 4: 중복 제거
MATCH (p:Person)-[:DIRECTED]->(m:Movie)-[:IN_GENRE]->(g:Genre)
RETURN DISTINCT g.name;
```

### ✏️ 연습문제

#### 문제 4-1
모든 `Person`의 `name`과 `nationality`를 각각 `이름`, `국적` 이라는 별칭으로 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)
RETURN p.name AS 이름, p.nationality AS 국적;
```

**해설:** `AS`로 별칭을 부여하면 결과 컬럼 이름이 변경됩니다. 한글 별칭도 사용 가능합니다.

</details>

#### 문제 4-2
모든 `Movie`의 제목과 (2026 - 개봉연도)를 계산해 `경과연수` 라는 컬럼으로 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title AS 제목, 2026 - m.released AS 경과연수;
```

**해설:** `RETURN`에서 산술 연산이 가능합니다. SQL의 `SELECT col1 + col2 ...`과 같습니다.

</details>

#### 문제 4-3
영화에 출연한 모든 배우의 이름을 **중복 없이** 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:ACTED_IN]->(:Movie)
RETURN DISTINCT p.name;
```

**해설:** 한 배우가 여러 영화에 출연하면 중복으로 나오므로 `DISTINCT`가 필수입니다. 라벨만 필요한 노드는 변수 없이 `(:Movie)`처럼 쓸 수 있습니다.

</details>

#### 문제 4-4
`'봉준호'` 감독이 만든 영화에 대해 `"<영화제목> (<개봉연도>)"` 형식의 문자열을 만들어 `소개` 컬럼으로 반환하세요. 예: `"기생충 (2019)"`.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person {name: '봉준호'})-[:DIRECTED]->(m:Movie)
RETURN m.title + ' (' + toString(m.released) + ')' AS 소개;
```

또는 `toString()` 없이:

```cypher
MATCH (p:Person {name: '봉준호'})-[:DIRECTED]->(m:Movie)
RETURN m.title + ' (' + m.released + ')' AS 소개;
```

**해설:** Cypher에서 문자열 결합은 `+`로 합니다. Neo4j 4.x 이상에서는 정수와 문자열을 `+`로 이을 때 타입 오류가 발생할 수 있으므로 `toString()`을 명시적으로 쓰는 것이 안전합니다.

</details>

#### 문제 4-5
사용자 `'이영희'`가 평가한 영화에 대해 (영화 제목, 평점, 평가일)을 반환하세요. 컬럼명은 각각 `영화`, `평점`, `날짜`로 하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User {name: '이영희'})-[r:RATED]->(m:Movie)
RETURN m.title AS 영화, r.rating AS 평점, r.date AS 날짜;
```

**해설:** 노드 속성과 관계 속성을 함께 반환할 수 있습니다.

</details>

#### 문제 4-6
모든 영화에 대해, 해당 영화를 감독한 사람의 이름을 함께 반환하세요. (영화제목, 감독이름)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN m.title AS 영화, p.name AS 감독;
```

**해설:** 패턴 안의 양쪽 노드의 속성을 모두 반환할 수 있습니다.  
참고로, 감독이 없는 영화는 결과에서 빠집니다(이런 경우는 8장 `OPTIONAL MATCH` 참고).

</details>

---

## 5. ORDER BY / LIMIT / SKIP - 정렬과 페이징

### 📖 구문 설명

쿼리 결과를 정렬하고, 일부만 가져오고, 건너뛰는 절들입니다.

**기본 문법:**

```cypher
RETURN ...
ORDER BY 컬럼1 [ASC|DESC], 컬럼2 [ASC|DESC]
SKIP N        -- 앞에서 N개 건너뛰기
LIMIT M;      -- 최대 M개만 반환
```

- `ORDER BY`의 기본은 오름차순(`ASC`). 내림차순은 `DESC`.
- `SKIP`과 `LIMIT`은 페이징(pagination)에 자주 사용됩니다.

### 💡 예제

```cypher
// 예제 1: 개봉연도 오래된 순
MATCH (m:Movie)
RETURN m.title, m.released
ORDER BY m.released ASC;

// 예제 2: 상영시간 긴 영화 Top 3
MATCH (m:Movie)
RETURN m.title, m.runtime
ORDER BY m.runtime DESC
LIMIT 3;

// 예제 3: 페이지네이션 - 4번째부터 6번째까지(1-indexed)
MATCH (m:Movie)
RETURN m.title
ORDER BY m.title
SKIP 3 LIMIT 3;
```

### ✏️ 연습문제

#### 문제 5-1
모든 영화를 개봉연도가 **최근 순**으로 정렬해서 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title, m.released
ORDER BY m.released DESC;
```

**해설:** "최근 순"은 큰 값이 먼저 나오는 내림차순(`DESC`)입니다.

</details>

#### 문제 5-2
가장 긴 영화 5편의 제목과 상영시간을 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
RETURN m.title, m.runtime
ORDER BY m.runtime DESC
LIMIT 5;
```

**해설:** `ORDER BY ... DESC` + `LIMIT N` 조합이 "Top N" 쿼리의 기본 패턴입니다.

</details>

#### 문제 5-3
모든 `Person`을 (1) 국적 가나다순 → (2) 같은 국적 안에서는 출생연도 오래된 순으로 정렬해 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)
RETURN p.name, p.nationality, p.born
ORDER BY p.nationality ASC, p.born ASC;
```

**해설:** `ORDER BY`에 컬럼을 콤마로 여러 개 나열하면 1차→2차→3차 정렬이 됩니다. SQL과 동일합니다.

</details>

#### 문제 5-4
`User` 노드를 `name` 가나다순으로 정렬했을 때, **3번째와 4번째** 사용자만 반환하세요. (1-indexed 기준)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
RETURN u.name
ORDER BY u.name ASC
SKIP 2 LIMIT 2;
```

**해설:** `SKIP 2`는 앞 2개를 건너뛰고, `LIMIT 2`는 그 다음 2개만 반환합니다. 즉 3, 4번째.

</details>

#### 문제 5-5
사용자가 매긴 모든 평점 중 **상위 3개의 가장 높은 평점 기록**을 반환하세요. (사용자명, 영화명, 평점, 날짜)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)-[r:RATED]->(m:Movie)
RETURN u.name, m.title, r.rating, r.date
ORDER BY r.rating DESC, r.date DESC
LIMIT 3;
```

**해설:** 관계 속성 기준으로도 정렬 가능합니다. 평점이 같을 때는 최신 날짜를 우선하기 위해 2차 정렬을 추가했습니다.

</details>

#### 문제 5-6
2000년대(2000~2009)에 개봉한 영화를 제목 가나다순으로 정렬하되, 처음 1편은 건너뛰고 그 다음 영화만 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
WHERE m.released >= 2000 AND m.released <= 2009
RETURN m.title, m.released
ORDER BY m.title ASC
SKIP 1 LIMIT 1;
```

**해설:** `WHERE` + `ORDER BY` + `SKIP` + `LIMIT`을 결합한 페이징 패턴입니다.

</details>

---

## 6. 집계 함수 (Aggregation)

### 📖 구문 설명

여러 행을 하나의 값으로 요약하는 함수들입니다. `RETURN`이나 `WITH` 절에서 사용합니다.

**주요 집계 함수:**

| 함수 | 설명 |
|------|------|
| `count(x)` | x의 개수 (null 제외) |
| `count(*)` | 행 개수 |
| `sum(x)` | 합 |
| `avg(x)` | 평균 |
|`stdev(x)`|표준편차|
| `min(x)` / `max(x)` | 최솟값 / 최댓값 |
| `collect(x)` | 리스트로 모으기 |

> 🔑 **암묵적 GROUP BY**  
> Cypher에는 `GROUP BY`가 없습니다. **집계 함수와 함께 등장한 다른 컬럼이 자동으로 그룹화 키**가 됩니다.  
> 예: `RETURN d.name, count(m)` → `d.name`별로 그룹핑 후 영화 수 카운트.

### 💡 예제

```cypher
// 예제 1: 전체 영화 수
MATCH (m:Movie)
RETURN count(m) AS 영화수;

// 예제 2: 감독별 영화 편수
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN p.name AS 감독, count(m) AS 영화편수
ORDER BY 영화편수 DESC;

// 예제 3: 영화별 평균 평점과 평가 수
MATCH (m:Movie)<-[r:RATED]-(:User)
RETURN m.title, avg(r.rating) AS 평균평점, count(r) AS 평가수
ORDER BY 평균평점 DESC;

// 예제 4: collect 사용 - 감독별 영화 제목 리스트
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN p.name, collect(m.title) AS 영화목록;
```

### ✏️ 연습문제

#### 문제 6-1
전체 `User` 노드의 개수를 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
RETURN count(u) AS 사용자수;
```

**해설:** 전체 개수 카운트의 가장 기본 형태.

</details>

#### 문제 6-2
각 감독별로 감독한 영화의 편수를 (감독명, 편수)로 반환하되, 편수 많은 순으로 정렬하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN p.name AS 감독, count(m) AS 편수
ORDER BY 편수 DESC;
```

**해설:** `p.name`을 함께 `RETURN`에 넣으면 자동으로 그룹화 키가 됩니다. SQL이라면 `GROUP BY p.name`이 필요한 자리.

</details>

#### 문제 6-3
영화별 평균 평점을 (영화 제목, 평균 평점)으로 반환하세요. 평점이 없는 영화는 제외합니다.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)<-[r:RATED]-(:User)
RETURN m.title AS 영화, avg(r.rating) AS 평균평점
ORDER BY 평균평점 DESC;
```

**해설:** `MATCH` 패턴에 `:RATED` 관계를 포함했기 때문에 평가 없는 영화는 자동 제외됩니다.

</details>

#### 문제 6-4
각 사용자가 평가한 영화 수와 평균 평점, 그리고 평가한 모든 영화의 **최고 평점**과 **최저 평점**을 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)-[r:RATED]->(m:Movie)
RETURN u.name AS 사용자,
       count(r) AS 평가수,
       avg(r.rating) AS 평균,
       max(r.rating) AS 최고,
       min(r.rating) AS 최저
ORDER BY 평가수 DESC;
```

**해설:** 한 쿼리에서 여러 집계 함수를 동시에 사용 가능합니다. 모두 같은 그룹화 키(`u.name`)를 공유합니다.

</details>

#### 문제 6-5
각 장르별 영화 편수를 반환하세요. (장르명, 편수)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
RETURN g.name AS 장르, count(m) AS 편수
ORDER BY 편수 DESC;
```

**해설:** 한 영화가 여러 장르를 가질 수 있으므로 영화 편수의 합은 전체 영화 수보다 클 수 있습니다.

</details>

#### 문제 6-6
각 감독이 만든 영화 제목 **리스트**를 영화수가 많은 순으로 정렬해서 반환하세요. (감독명, [영화 제목 리스트])

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN p.name AS 감독, collect(m.title) AS 영화목록
ORDER BY size(영화목록) DESC;
```

**해설:** `collect()`는 그룹별 값들을 **리스트**로 모으는 매우 강력한 함수입니다. 결과는 한 행에 리스트 하나로 표시됩니다.

</details>

#### 문제 6-7
각 사용자가 매긴 평점들의 **합계**가 가장 큰 사용자 1명의 이름과 합계를 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)-[r:RATED]->(:Movie)
RETURN u.name AS 사용자, sum(r.rating) AS 합계
ORDER BY 합계 DESC
LIMIT 1;
```

**해설:** 집계 + 정렬 + 제한 조합. 통계 분석의 기본 패턴.

</details>

#### 문제 6-8
영화별 출연 배우 수를 반환하세요.  
(힌트: 8장 `OPTIONAL MATCH`를 미리 학습한 뒤 푸세요.)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie) <-[:ACTED_IN]-(p:Person)
RETURN m.title, count(p) AS 출연배우수
ORDER BY 출연배우수 DESC;
```

**해설:** 일반 `MATCH`는 패턴이 없는 행을 제외하지만, `OPTIONAL MATCH`는 빈 결과(null)도 보존합니다. `count(p)`는 null이면 0으로 계산됩니다 — 단, `count(*)`를 쓰면 1로 나오므로 차이를 주의하세요.

</details>

---

## 7. WITH - 쿼리 체이닝

### 📖 구문 설명

`WITH` 는 쿼리를 단계적으로 쪼개서, 앞 단계의 결과를 뒤 단계의 입력으로 넘겨주는 파이프의 역할을 합니다.

**주요 용도:**

1. 집계 결과를 이후 절에서 추가 필터링/매칭에 사용
   - 집계를 where 절에서 직접 할 수 없다.
   - with 절에 집계함수와 다른 변수가 들어 갈 경우 다른 변수는 group by의 기준이된다.
2. 중간 결과를 줄이거나 정렬한 뒤 다음 단계 진행
   - return 전에만 limit를 할 경우 많은 양의 조회결과를 끝까지 처리해야 한다. with를 이용해 중간에 데이터의 양을 줄인 뒤 다음을 진행할 수있다.
3. 변수 범위(scope) 제어
   - with 절에 명시 하지 않은 변수는 다음 단계에서 완전히 사라진다. with 절을 사용해 변수를 줄여가면서 쿼리가 집중해야 할 대상을 좁혀가도록 설계할 때 with절을 사용한다.

**기본 문법:**

```cypher
MATCH 패턴1
WITH 변수, 표현식 AS 별칭 [WHERE 조건]
MATCH 패턴2
RETURN ...
```

> ⚠️ `WITH` 다음에는 `WITH` 절에 등장한 변수만 사용할 수 있습니다. 이전 변수를 계속 쓰려면 `WITH`에 명시해야 합니다.

### 💡 예제

```cypher
// 예제 1: 평균 평점이 4.5 이상인 영화만 추리기
MATCH (m:Movie)<-[r:RATED]-(:User)
WITH m, avg(r.rating) AS avgRating
WHERE avgRating >= 4.5
RETURN m.title, avgRating;

// 예제 2: 영화당 평가 수가 가장 많은 영화 1편의 출연 배우 조회
MATCH (m:Movie)<-[r:RATED]-(:User)
WITH m, count(r) AS ratingCount
ORDER BY ratingCount DESC LIMIT 1
MATCH (m)<-[:ACTED_IN]-(actor:Person)
RETURN m.title, ratingCount, collect(actor.name) AS 출연진;
```

### ✏️ 연습문제

#### 문제 7-1
평가 횟수가 2회 이상인 영화의 (제목, 평가 횟수)만 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)<-[r:RATED]-(:User)
WITH m, count(r) AS cnt
WHERE cnt >= 2
RETURN m.title, cnt
ORDER BY cnt DESC;
```

**해설:**
- `WHERE cnt >= 2`는 일반 `WHERE`로 쓸 수 없습니다 (집계 결과를 필터링하는 거니까).
- `WITH` 다음에 오는 `WHERE`는 SQL의 `HAVING`과 비슷한 역할을 합니다.

</details>

#### 문제 7-2
감독한 영화가 2편 이상인 감독만의 이름과 영화 편수를 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
WITH p, count(m) AS cnt
WHERE cnt >= 2
RETURN p.name, cnt
ORDER BY cnt DESC;
```

**해설:** SQL의 `HAVING COUNT(*) >= 2` 패턴. Cypher에서는 `WITH ... WHERE` 조합으로 표현합니다.

</details>



#### 문제 7-3
평균 평점이 4점 이상인 영화의 (제목, 평균 평점)을 반환하되, 평점이 높은 순으로 정렬하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)<-[r:RATED]-(:User)
WITH m, avg(r.rating) AS avgR
WHERE avgR >= 4
RETURN m.title, avgR
ORDER BY avgR DESC;
```

**해설:** 6장의 집계 + 7장의 `WITH`를 결합한 흔한 분석 패턴입니다.

</details>

#### 문제 7-4
각 사용자가 평가한 영화 평균 평점을 구한 후, 그 평균이 4점 이상인 사용자가 평가한 모든 영화의 제목을 반환하세요. (사용자명, 평균평점, 영화 리스트)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)-[r:RATED]->(m:Movie)
WITH u, avg(r.rating) AS userAvg
WHERE userAvg >= 4
MATCH (u)-[:RATED]->(m2:Movie)
RETURN u.name, userAvg, collect(m2.title) AS 영화목록;
```

**해설:**
- 1단계: 사용자별 평균 평점 계산
- 2단계: 평균이 4 이상인 사용자만 필터
- 3단계: 그 사용자가 평가한 영화를 다시 매칭
- `WITH`는 이렇게 단계별로 데이터를 좁혀가는 데 사용합니다.

</details>

#### 문제 7-5
가장 많은 영화에 출연한 배우 1명을 찾고, 그 배우와 같은 영화에 출연한 다른 배우들의 이름 리스트를 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WITH p, count(m) AS cnt
ORDER BY cnt DESC
LIMIT 1
MATCH (p)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(coactor:Person)
WHERE coactor <> p
RETURN p.name AS 주연, collect(DISTINCT coactor.name) AS 동료배우;
```

**해설:**
- 1단계: 가장 많은 영화에 출연한 배우 1명 추출
- 2단계: 그 배우와 같은 영화에 출연한 동료를 찾기
- `collect(DISTINCT ...)`로 중복 없는 리스트를 만듭니다.
- WITH는 중간 결과를 다음 절로 넘기는 역할을 한다.  WITH에 명시한 변수(값)만 이후 절에서 사용할 수 있으며, 명시하지 않은 변수는 이후 절에서 사라진다. 따라서 WITH를 이용해 사용할 변수를 제한하거나, 집계·정렬·필터링한 결과를 다음 MATCH, WHERE, RETURN 등에서 이어서 사용할 수 있다.

</details>

---

## 8. OPTIONAL MATCH - 선택적 매칭

### 📖 구문 설명

`MATCH`는 패턴이 일치하지 않으면 결과 행 자체가 사라집니다. 반면 `OPTIONAL MATCH`는 일치하지 않아도 행을 유지하고 매칭되지 않은 변수는 `null`이 됩니다. SQL의 `LEFT OUTER JOIN`과 유사합니다.

**기본 문법:**

```cypher
MATCH (a:Label)
OPTIONAL MATCH (a)-[:REL]->(b)
RETURN a, b   -- b는 null일 수 있음
```

**언제 쓰는가?**

- 어떤 노드와 연결된 정보를 "있으면 보여주고 없으면 null"로 표시하고 싶을 때
- 0건 포함 통계가 필요할 때 (예: "출연 배우가 0명인 영화도 보여줘")
- master 정보를 match로 찾고 부가 정보를 optional match로 정의한다.
### 💡 예제

```cypher
// 예제 1: 모든 영화와 그 영화의 감독 (감독 없으면 null)
MATCH (m:Movie)
OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
RETURN m.title, d.name;

// 예제 2: 모든 사용자와 그들이 팔로우하는 인물 수 (0명이면 0으로 표시)
MATCH (u:User)
OPTIONAL MATCH (u)-[:FOLLOWS]->(p:Person)
RETURN u.name, count(p) AS 팔로우수;
```

### ✏️ 연습문제

#### 문제 8-1
모든 영화의 제목과 감독 이름을 반환하되, 감독이 등록되지 않은 영화도 결과에 포함시키세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
RETURN m.title AS 영화, d.name AS 감독;
```

**해설:** 일반 `MATCH`였다면 감독 미등록 영화는 누락됩니다. `OPTIONAL MATCH`를 쓰면 `d.name`이 `null`로 표시됩니다.

</details>

#### 문제 8-2
모든 사용자의 이름과 친구 수를 반환하세요. (친구가 0명인 사용자도 포함)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
OPTIONAL MATCH (u)-[:FRIENDS_WITH]->(f:User)
RETURN u.name, count(f) AS 친구수
ORDER BY 친구수 DESC;
```

**해설:** `count(f)`는 매칭 실패 시 0이 됩니다. 만약 `count(*)`를 쓰면 매칭 실패해도 1을 반환하므로 주의.

</details>

#### 문제 8-3
모든 `Person`의 이름과 그가 감독한 영화 제목을 반환하세요. 감독한 영화가 없는 인물도 결과에 포함시키되, 그 경우 영화 제목은 null로 표시되어야 합니다.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)
OPTIONAL MATCH (p)-[:DIRECTED]->(m:Movie)
RETURN p.name AS 인물, m.title AS 감독작
ORDER BY p.name;
```

**해설:** 배우만인 인물은 감독작이 null로 표시됩니다.

</details>

#### 문제 8-4
모든 영화의 제목과 그 영화에 출연한 배우 수를 반환하되, 출연 배우가 0명인 영화도 포함하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
RETURN m.title AS 영화, count(a) AS 출연배우수
ORDER BY 출연배우수 DESC;
```

**해설:** 6장의 마지막 문제와 동일한 패턴 — `OPTIONAL MATCH`의 정석적 활용.

</details>

#### 문제 8-5
모든 사용자에 대해 그들이 평가한 영화의 평균 평점을 반환하세요. 평가 기록이 없는 사용자는 평균이 null로 표시되어야 합니다.

<details>
<summary>💡 정답 보기</summary>

```cyphe
MATCH (u:User)
OPTIONAL MATCH (u)-[r:RATED]->(:Movie)
RETURN u.name AS 사용자, avg(r.rating) AS 평균평점
ORDER BY 평균평점 DESC;
```

**해설:** `avg`도 입력이 모두 null이면 null을 반환합니다.

</details>

#### 문제 8-6
모든 사용자와 그들이 팔로우하는 인물 이름의 리스트를 반환하세요. 팔로우 인물이 없으면 빈 리스트 `[]` 가 되어야 합니다.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
OPTIONAL MATCH (u)-[:FOLLOWS]->(p:Person)
RETURN u.name AS 사용자, collect(p.name) AS 팔로잉;
```

**해설:** `collect()`는 null을 자동으로 제외하므로 팔로우가 없는 사용자는 `[]` 빈 리스트로 결과가 나옵니다 — 이게 `count(p)`와 다른 점입니다.

</details>

---

## 9. SET - 속성 업데이트

### 📖 구문 설명

`SET` 절은 이미 존재하는 노드나 관계의 속성(property), 라벨(label)을 추가하거나 수정하는 절입니다.    
CREATE가 새 노드나 관계를 만드는 절이라면, SET은 조회된 데이터의 값을 변경하는 절입니다.

**기본 문법:**

```cypher
MATCH 패턴
SET n.속성 = 값                -- 단일 속성 변경/추가
SET n.속성1 = v1, n.속성2 = v2 -- 여러 속성 변경/추가
SET n += {key: value, ...}    -- 여러 속성 변경/추가
SET n = {key: value, ...}     -- 전체 교체(주의: 기존 속성 삭제됨)
SET n:NewLabel               -- 라벨 추가
```

### 💡 예제

```cypher
// 예제 1: 단일 속성 변경/추가
MATCH (p:Person {name: '봉준호'})
SET p.nationality = '대한민국'
RETURN p;

// 예제 2: 여러 속성 변경/추가
MATCH (m:Movie {title: '기생충'})
SET m.language = '한국어', m.budget = 11000000;

// 예제 3: 라벨 추가 (Person 위에 Director 라벨 추가)
MATCH (p:Person {name: '봉준호'})
SET p:Director;

// 예제 4: 여러 속성 변경/추가
MATCH (m:Movie {title: '기생충'})
SET m += {country: 'KR', oscarWinner: true};
```

### ✏️ 연습문제

#### 문제 9-1
영화 `'기생충'`에 `language` 속성을 `'한국어'`로 추가하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie {title: '기생충'})
SET m.language = '한국어'
RETURN m;
```

**해설:** 가장 기본적인 속성 추가. `RETURN`은 결과 확인용으로 선택입니다.

</details>

#### 문제 9-2
모든 한국 국적 인물에게 `language` 속성을 `'Korean'`으로 일괄 추가하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person {nationality: '한국'})
SET p.language = 'Korean'
RETURN p.name, p.language;
```

**해설:** `MATCH`로 여러 노드가 매칭되면 `SET`은 그 모두에 적용됩니다. SQL의 `UPDATE ... WHERE`와 유사.

</details>

#### 문제 9-3
영화 `'올드보이'`의 `runtime`을 `120`에서 `121`로 수정하고, `language: '한국어'`, `country: 'KR'`을 동시에 추가하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie {title: '올드보이'})
SET m.runtime = 121,
    m.language = '한국어',
    m.country = 'KR'
RETURN m;
```

**해설:** 콤마로 여러 속성을 동시에 설정 가능합니다.

</details>

#### 문제 9-4
감독한 영화가 있는 모든 `Person`에게 `:Director` 라벨을 추가하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)-[:DIRECTED]->(:Movie)
SET p:Director
RETURN DISTINCT p.name, labels(p);
```

**해설:**
- `SET p:Director`로 라벨을 추가합니다(기존 `Person` 라벨도 유지).
- `labels(p)`는 노드가 가진 모든 라벨을 리스트로 반환하는 함수입니다.
- 한 노드는 여러 라벨을 가질 수 있습니다.

</details>

#### 문제 9-5
사용자 `'김철수'`가 영화 `'기생충'`에 매긴 평점을 `5`에서 `4`로 수정하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User {name: '김철수'})-[r:RATED]->(m:Movie {title: '기생충'})
SET r.rating = 4
RETURN u.name, m.title, r.rating;
```

**해설:** 관계 속성도 `SET`으로 수정 가능합니다. 관계 변수(`r`)를 사용해야 함을 잊지 마세요.

</details>

#### 문제 9-6
2010년 이전 개봉 영화에 `era: 'classic'`, 2010년 이후 영화에 `era: 'modern'` 속성을 일괄 추가하세요. (두 개의 별도 쿼리로 작성)

<details>
<summary>💡 정답 보기</summary>

```cypher
// 2010년 이전
MATCH (m:Movie)
WHERE m.released < 2010
SET m.era = 'classic';

// 2010년 이후
MATCH (m:Movie)
WHERE m.released >= 2010
SET m.era = 'modern';
```

**해설:** 데이터 마이그레이션 시 자주 쓰는 패턴입니다. 조건별 일괄 업데이트.

</details>

#### 문제 9-7
사용자 `'이영희'`의 정보를 부분 업데이트하세요. (`age`는 `33`으로, 새로운 속성 `email: 'lyh@example.com'` 추가, 다른 속성은 그대로 유지)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User {name: '이영희'})
SET u += {age: 33, email: 'lyh@example.com'}
RETURN u;
```

**해설:**
- `SET u += {...}` 는 **병합(merge)** — 명시한 키만 업데이트, 나머지 속성은 보존.
- `SET u = {...}` 는 **전체 교체** — 명시 안 한 기존 속성은 모두 삭제됨. 매우 위험하니 주의!

</details>

---

## 10. DELETE / DETACH DELETE - 삭제

### 📖 구문 설명

- `DELETE`: 노드/관계 삭제
- `DETACH DELETE`: 노드와 그에 연결된 모든 관계를 함께 삭제

> ⚠️ **중요:** Neo4j는 **관계가 연결된 노드를 일반 `DELETE`로 삭제할 수 없습니다.** 그러면 고아 관계가 생기기 때문이죠. 그래서 `DETACH DELETE`를 사용합니다.

**기본 문법:**

```cypher
// 관계만 삭제
MATCH (a)-[r:REL]->(b) DELETE r;

// 노드만 삭제 (연결 관계가 없을 때)
MATCH (n:Label) DELETE n;

// 노드 + 연결된 모든 관계 삭제
MATCH (n:Label) DETACH DELETE n;

// 전체 그래프 초기화
MATCH (n) DETACH DELETE n;

// 속성 삭제
MATCH (n) REMOVE n.속성명;

// 노드의 라벨 삭제
MATCH (n) REMOVE n:라벨명;
```

### 💡 예제

```cypher
// 예제 1: 특정 관계만 삭제
MATCH (u:User {name: '김철수'})-[r:FRIENDS_WITH]->(:User {name: '이영희'})
DELETE r;

// 예제 2: 노드와 모든 관계 삭제
MATCH (u:User {name: '김철수'})
DETACH DELETE u;

// 예제 3: 속성 삭제 (REMOVE 키워드 사용)
MATCH (m:Movie {title: '기생충'})
REMOVE m.language;

// 예제 4: 라벨 제거
MATCH (p:Person:Director {name: '봉준호'})
REMOVE p:Director;
```

### ✏️ 연습문제

> ⚠️ **경고:** 아래 문제들은 데이터를 영구적으로 변경합니다. 연습 후엔 데이터셋을 다시 생성하는 게 좋습니다.

#### 문제 10-1
사용자 `'김철수'`와 `'이영희'` 사이의 `:FRIENDS_WITH` 관계만 삭제하세요. (양방향 모두)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (a:User {name: '김철수'})-[r:FRIENDS_WITH]-(b:User {name: '이영희'})
DELETE r;
```

**해설:** 화살표 없이 `-[r:FRIENDS_WITH]-`로 매칭하면 양방향 관계 모두를 잡습니다. `DELETE r`은 관계만 삭제하고 노드는 그대로 둡니다.

</details>

#### 문제 10-2
영화 `'범죄도시'`와 그에 연결된 모든 관계를 삭제하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie {title: '범죄도시'})
DETACH DELETE m;
```

**해설:** 노드에 관계가 있을 땐 반드시 `DETACH DELETE`를 사용해야 합니다. 일반 `DELETE`를 쓰면 에러가 납니다.

</details>

#### 문제 10-3
가입연도가 2017년 이전인 모든 사용자를 (관계 포함하여) 삭제하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
WHERE u.joinYear < 2017
DETACH DELETE u;
```

**해설:** 조건부 일괄 삭제. `MATCH` + `WHERE` + `DETACH DELETE`의 조합.

</details>

#### 문제 10-4
모든 영화에서 `runtime` 속성을 제거하세요. (속성만 제거, 노드는 유지)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)
REMOVE m.runtime
RETURN m.title, m.runtime;
```

**해설:** `DELETE`는 노드/관계 삭제 전용이고, **속성 삭제는 `REMOVE` 키워드**를 사용합니다. 이름은 다르지만 같은 카테고리(쓰기 명령)이므로 한꺼번에 학습합니다.

</details>

#### 문제 10-5
평점이 2점 이하인 모든 `:RATED` 관계를 삭제하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (:User)-[r:RATED]->(:Movie)
WHERE r.rating <= 2
DELETE r;
```

**해설:** 관계 속성으로 필터링한 후 관계만 삭제. 노드(사용자, 영화)는 그대로 둡니다.

</details>

#### 문제 10-6
출연 영화도 없고, 감독 영화도 없는 `Person` 노드를 모두 삭제하세요. (외톨이 인물 삭제)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person)
WHERE NOT (p)-[:ACTED_IN]->(:Movie)
  AND NOT (p)-[:DIRECTED]->(:Movie)
DETACH DELETE p;
```

**해설:**
- 패턴 술어(pattern predicate)를 `WHERE`에서 활용한 데이터 정리 패턴입니다.
- 사용자가 팔로우하는 관계는 남아있을 수 있으므로 `DETACH DELETE`로 안전하게 삭제.

</details>

#### 문제 10-7
**(주의)** 그래프 데이터 전체를 초기화하는 쿼리를 작성하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (n)
DETACH DELETE n;
```

**해설:**
- 모든 노드와 관계를 삭제하는 가장 일반적인 초기화 쿼리.
- 운영 DB에서는 절대 함부로 실행하면 안 됩니다.
- 매우 큰 그래프에서는 메모리 부족이 날 수 있으므로 배치 처리(`apoc.periodic.iterate`)를 고려해야 합니다.

</details>

---

## 11. MERGE - 생성 또는 매칭

### 📖 구문 설명

`MERGE`는 "있으면 찾고(MATCH), 없으면 만든다(CREATE)" 하는 절입니다. 데이터의 **중복 생성을 방지**하면서 멱등성(idempotent) 있는 쿼리를 작성하는 핵심적 구문이다.

> 멱등성(idempotent) 이란 같은 작업을 여러 번 실행해도 결과가 한 번 실행한 것과 같게 유지되는 성질을 말한다.

**기본 문법:**

```cypher
// 노드 MERGE
MERGE (n:Label {key: value})

// 관계 MERGE (보통 양 노드를 먼저 MATCH/MERGE한 뒤)
MATCH (a), (b) WHERE ...
MERGE (a)-[:REL]->(b)

// MERGE에 따른 추가 동작
// ON CREATE SET: 생성했을 때 실행되어 속성을 추가한다.
// ON MERGE SET: 조회했을 때 실행되어 속성을 추가/변경한다.
MERGE (n:Label {id: 1})
ON CREATE SET n.createdAt = timestamp(), n.count = 1
ON MATCH SET n.updatedAt = timestamp(), n.count = n.count + 1
```

> 🔑 **핵심 주의사항**  
> `MERGE`는 **명시한 모든 속성**을 매칭 키로 사용합니다.  
> `MERGE (m:Movie {title: '기생충', released: 2019})` 은 title과 released가 모두 일치하는 영화가 있을 때만 매칭하고, 없으면 그 둘을 가진 새 영화를 만듭니다. 매칭 키 외 속성은 `ON CREATE SET`에서 추가하는 것이 안전합니다.

### 💡 예제

```cypher
// 예제 1: 단순 MERGE - 있으면 매칭, 없으면 생성
MERGE (g:Genre {name: '느와르'});

// 예제 2: ON CREATE / ON MATCH 분기
MERGE (u:User {name: '신규유저'})
ON CREATE SET u.joinYear = 2024, u.age = 30
ON MATCH SET u.lastVisit = '2024-12-01';

// 예제 3: 노드 + 관계를 안전하게 MERGE
MERGE (p:Person {name: '봉준호'})
MERGE (m:Movie {title: '괴물'})
MERGE (p)-[:DIRECTED]->(m);
```

### ✏️ 연습문제

#### 문제 11-1
`Genre` 노드 중 `name: '판타지'` 가 없으면 새로 생성하고, 이미 있으면 그대로 두세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MERGE (g:Genre {name: '판타지'})
RETURN g;
```

**해설:** `MERGE`의 가장 단순한 형태. 동일 쿼리를 여러 번 실행해도 노드는 1개만 존재합니다 — 이것이 멱등성입니다.

</details>

#### 문제 11-2
사용자 이름이 `'박민수'`인 노드를 찾고, 없으면 새로 생성하되 생성된 경우에만 `joinYear: 2025`, `age: 26` 속성을 부여하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MERGE (u:User {name: '박민수'})
ON CREATE SET u.joinYear = 2025, u.age = 26
RETURN u;
```

**해설:** `ON CREATE SET`은 새로 생성된 경우에만 실행됩니다. 기존 노드의 속성을 덮어쓰지 않으므로 안전합니다.

</details>

#### 문제 11-3
`'송강호'` 와 `'기생충'` 사이에 `:ACTED_IN` 관계가 없으면 만들고, 있으면 그대로 두세요. (단, 양 노드는 이미 존재한다고 가정)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (p:Person {name: '송강호'}), (m:Movie {title: '기생충'})
MERGE (p)-[r:ACTED_IN]->(m)
RETURN r;
```

**해설:** 관계 `MERGE`는 보통 양 노드를 `MATCH`로 먼저 잡은 뒤에 사용합니다. `MERGE` 안에서 노드까지 새로 만들면 의도치 않은 노드가 생성될 수 있습니다.

</details>

#### 문제 11-4
사용자 `'김철수'`가 영화 `'살인의 추억'`에 평점 `5`로 평가한 기록을 추가하되, 이미 평가 기록이 있다면 평점만 `5`로 갱신하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User {name: '김철수'}), (m:Movie {title: '살인의 추억'})
MERGE (u)-[r:RATED]->(m)
ON CREATE SET r.rating = 5, r.date = '2024-12-01'
ON MATCH SET r.rating = 5
RETURN u.name, m.title, r.rating, r.date;
```

**해설:**
- 처음 평가하는 경우(`ON CREATE`)에는 날짜까지 기록.
- 이미 평가했던 경우(`ON MATCH`)에는 평점만 덮어쓰기.
- 이런 "upsert" 패턴은 실무에서 매우 자주 등장합니다.

</details>

#### 문제 11-5
`'기생충'` 영화에 새로운 장르 `'블랙코미디'`를 안전하게 추가하세요. (장르가 없으면 만들고, 관계도 중복 없이)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie {title: '기생충'})
MERGE (g:Genre {name: '블랙코미디'})
MERGE (m)-[:IN_GENRE]->(g)
RETURN m.title, g.name;
```

**해설:** 두 개의 `MERGE`를 차례로 사용. 첫 번째는 장르 노드, 두 번째는 관계. 이렇게 하면 같은 쿼리를 여러 번 실행해도 안전합니다.

</details>

#### 문제 11-6
`MERGE`를 사용하여 `'박찬욱'`(1963년생, 국적 한국) 감독이 `'친절한 금자씨'`(2005년, 112분) 영화를 감독했다는 데이터를 한 번에 안전하게 생성하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MERGE (p:Person {name: '박찬욱'})
ON CREATE SET p.born = 1963, p.nationality = '한국'
MERGE (m:Movie {title: '친절한 금자씨'})
ON CREATE SET m.released = 2005, m.runtime = 112
MERGE (p)-[:DIRECTED]->(m)
RETURN p, m;
```

**해설:**
- 매칭 키 (`name`, `title`)는 `MERGE`의 패턴에 둡니다.
- 부가 속성(`born`, `released` 등)은 `ON CREATE SET`에서 처리해 기존 데이터를 보호합니다.
- 데이터 적재 ETL에서 가장 표준적인 패턴.

</details>

#### 문제 11-7
**`CREATE` 와 `MERGE`의 차이**를 이해하기 위해, 다음 두 쿼리를 차례로 실행하면 결과가 어떻게 달라지는지 설명하세요.

```cypher
// 쿼리 A
CREATE (g:Genre {name: '액션'});

// 쿼리 B
MERGE (g:Genre {name: '액션'});
```

<details>
<summary>💡 정답 보기</summary>

**설명:**
- 쿼리 A는 항상 새 노드를 생성하므로, 이미 `'액션'` 장르 노드가 있어도 또 하나 생성합니다 → **중복 노드 발생**.
- 쿼리 B는 `'액션'` 노드가 있으면 매칭만 하고 새 노드를 만들지 않습니다 → **중복 방지**.

**확인 쿼리:**

```cypher
MATCH (g:Genre {name: '액션'})
RETURN count(g);
```

A를 실행한 만큼 카운트가 늘어나지만, B는 아무리 실행해도 처음 1개로 유지됩니다.

**결론:** "이미 있을 수도 있는 데이터를 안전하게 넣고 싶다" → `MERGE`. "확실히 새것을 만든다" → `CREATE`.

</details>

---

## 12. 경로(Path) 쿼리

### 📖 구문 설명

- 그래프 데이터베이스의 가장 강력한 능력 중 하나는 **여러 단계 떨어진 노드 사이의 경로**를 쉽게 찾을 수 있다는 점입니다.
- 조회하려고 하는 관계의 단계를 지정하여 검색할 수 있습니다.

**핵심 문법:**

```cypher
// 변수 길이 패턴: 1~3 hop
MATCH (a)-[:REL*1..3]->(b)

// 정확히 N hop (hop: 관계 단계)
MATCH (a)-[:REL*2]->(b)

// 1 이상 (제한 없음 - 주의!)
MATCH (a)-[:REL*]->(b)

// 경로 변수
MATCH path = (a)-[:REL*1..3]->(b)
RETURN path, length(path), nodes(path), relationships(path);

//length(path): 경로에 포함된 관계의 개수, 즉 hop 수를 반환
//nodes(path): 경로에 포함된 노드들을 리스트로 반환
//relationships(path): 경로에 포함된 관계들을 리스트로 반환

// 최단 경로 조회
MATCH path = shortestPath((a)-[:REL*..10]->(b))
RETURN path;

// 모든 최단 경로(같은 길이일 때)
MATCH path = allShortestPaths((a)-[:REL*..10]->(b))
RETURN path;
```

> ⚠️ 변수 길이 쿼리는 깊이가 깊어질수록 계산비용이 커진다. 항상 상한(`*1..N`)을 두는 것이 원칙입니다.

### 💡 예제

```cypher
// 예제 1: 친구의 친구 (정확히 2단계)
MATCH (me:User {name: '김철수'})-[:FRIENDS_WITH*2]->(fof:User)
WHERE fof <> me
RETURN DISTINCT fof.name;

// 예제 2: 1~3 단계 친구
MATCH (me:User {name: '김철수'})-[:FRIENDS_WITH*1..3]->(other:User)
WHERE other <> me
RETURN DISTINCT other.name;

// 예제 3: 최단 경로 찾기
MATCH path = shortestPath(
  (a:User {name: '김철수'})-[:FRIENDS_WITH*..6]-(b:User {name: '한지훈'})
)
RETURN [n IN nodes(path) | n.name] AS 경로, length(path) AS 거리;
```

### ✏️ 연습문제

#### 문제 12-1
사용자 `'김철수'`의 정확히 **2단계** 떨어진 친구의 친구의 이름을 모두 반환하세요. (자기 자신 제외)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (me:User {name: '김철수'})-[:FRIENDS_WITH*2]->(fof:User)
WHERE fof <> me
RETURN DISTINCT fof.name;
```

**해설:**
- `*2`는 **정확히** 2단계 떨어진 관계 경로를 의미합니다.
- `me`로 다시 돌아오는 경로도 포함될 수 있으므로 `WHERE fof <> me`로 제외.

</details>

#### 문제 12-2
사용자 `'김철수'`로부터 **1단계 ~ 3단계** 안에 있는 모든 사용자의 이름을 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (me:User {name: '김철수'})-[:FRIENDS_WITH*1..3]->(other:User)
WHERE other <> me
RETURN DISTINCT other.name;
```

**해설:** `*1..3`은 1, 2, 3단계 모두 포함합니다. 깊이가 길어질수록 같은 사용자가 여러 경로로 닿을 수 있어 `DISTINCT`가 필수.

</details>

#### 문제 12-3
사용자 `'김철수'`와 `'한지훈'` 사이의 **최단 친구 경로**를 찾아 경로상의 모든 사용자 이름을 순서대로 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH path = shortestPath(
  (a:User {name: '김철수'})-[:FRIENDS_WITH*..10]-(b:User {name: '한지훈'})
)
RETURN [n IN nodes(path) | n.name] AS 경로,
       length(path) AS 단계수;
```

**해설:**
- `shortestPath()` 함수에 패턴을 넣어 호출합니다.
- `[n IN nodes(path) | n.name]`은 **리스트 컴프리헨션** — 경로의 노드들에서 이름만 추출.
- 방향 없는 친구 관계(`-[:FRIENDS_WITH*..10]-`, 화살표 없음)로 검색.
- 상한 `..10`은 안전장치(무한 탐색 방지).

</details>

#### 문제 12-4
같은 영화에 출연한 적이 있는 두 배우 사이의 관계를 "공동출연"이라 부릅니다.  
`'송강호'`와 다른 모든 배우 사이의 **공동출연 1~2단계 거리** 안의 배우 이름을 반환하세요.  
(직접 같이 출연했거나, 한 다리 건너 같이 출연한 배우들)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (song:Person {name: '송강호'})-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(co:Person)
WITH song, collect(DISTINCT co) AS direct
MATCH (song)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(mid:Person)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(co2:Person)
WHERE co2 <> song
RETURN DISTINCT co2.name AS 배우, 
       CASE WHEN co2 IN direct THEN '직접 공동출연' ELSE '한 다리 건너' END AS 거리
ORDER BY 거리, 배우;
```

또는 좀 더 간단히:

```cypher
MATCH path = (song:Person {name: '송강호'})-[:ACTED_IN*2..4]-(other:Person)
WHERE other <> song AND length(path) % 2 = 0
RETURN DISTINCT other.name, length(path)/2 AS 공동출연거리
ORDER BY 공동출연거리;
```

**해설:**
- ACTED_IN 관계는 `Person -> Movie` 방향이라, 공동출연 1단계는 `Person -> Movie <- Person` 즉 `:ACTED_IN` 관계 2개를 거칩니다.
- 그래서 변수 길이를 `*2..4`로 잡으면 1~2단계 공동출연이 됩니다 (관계 수 기준).
- `length(path)/2`로 공동출연 거리를 구합니다.
- 이런 "Bacon number" 같은 패턴은 추천 시스템의 기본입니다.

</details>

#### 문제 12-5
`'봉준호'` 감독의 영화에 출연한 배우들이 **다시 다른 감독의 영화에 출연**한 경우를 모두 찾으세요. (봉준호 감독, 출연배우, 다른 영화, 다른 영화의 감독)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (bong:Person {name: '봉준호'})-[:DIRECTED]->(m1:Movie)<-[:ACTED_IN]-(actor:Person),
      (actor)-[:ACTED_IN]->(m2:Movie)<-[:DIRECTED]-(other:Person)
WHERE other <> bong
RETURN bong.name AS 봉준호, 
       actor.name AS 배우, 
       m2.title AS 다른영화, 
       other.name AS 그감독;
```

**해설:**
- 두 개의 패턴을 콤마로 연결한 **다중 패턴 매칭**입니다.
- 공통 변수(`actor`)가 두 패턴을 잇는 다리 역할.
- 봉준호 자기 자신을 제외하기 위해 `WHERE`로 필터.

</details>

#### 문제 12-6
어떤 두 사용자(`'김철수'`와 `'한지훈'`) 사이의 **최단 친구 경로의 길이(hop 수)**가 몇인지 반환하세요. 경로 자체는 반환할 필요 없습니다.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH path = shortestPath(
  (a:User {name: '김철수'})-[:FRIENDS_WITH*..15]-(b:User {name: '한지훈'})
)
RETURN length(path) AS 거리;
```

**해설:** `length(path)`는 경로의 관계(hop) 개수를 반환합니다. 노드 개수가 아닙니다 — 노드 개수는 `length(path) + 1`.

</details>

#### 문제 12-7
사용자 `'김철수'`로부터 **친구의 친구가 평가한** 영화 중 본인이 아직 평가하지 않은 영화를 추천 후보로 반환하세요. (영화 제목, 추천한 친구의 친구 수)

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (me:User {name: '김철수'})-[:FRIENDS_WITH*2]->(fof:User)-[:RATED]->(m:Movie)
WHERE fof <> me
  AND NOT (me)-[:RATED]->(m)
RETURN m.title AS 추천영화, count(DISTINCT fof) AS 추천한_친친구수
ORDER BY 추천한_친친구수 DESC;
```

**해설:**
- 친구의 친구 → 그들이 평가한 영화 → 내가 안 본 것만
- 이게 그래프 DB의 가장 큰 강점입니다. 같은 쿼리를 SQL로 짜면 JOIN 지옥입니다.
- 이 쿼리가 추천 시스템의 단순한 형태입니다.

</details>

---

## 🎯 마무리: 종합 실전 문제

> 위 12개 절을 모두 활용하는 통합 문제들입니다. 자유롭게 풀어보세요.

### 종합 문제 1
가장 평균 평점이 높은 영화 Top 3의 (제목, 평균 평점, 평가 수, 감독 이름, 장르 리스트)를 한 번의 쿼리로 반환하세요.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (m:Movie)<-[r:RATED]-(:User)
WITH m, avg(r.rating) AS avgR, count(r) AS cnt
ORDER BY avgR DESC, cnt DESC
LIMIT 3
OPTIONAL MATCH (d:Person)-[:DIRECTED]->(m)
OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
RETURN m.title AS 영화,
       avgR AS 평균평점,
       cnt AS 평가수,
       d.name AS 감독,
       collect(DISTINCT g.name) AS 장르;
```

**해설:** 집계 → 정렬·제한 → 추가 매칭 → 리스트 수집의 종합형. 실무 분석 쿼리의 전형입니다.

</details>

### 종합 문제 2
각 사용자에게 다음 정보를 한 줄로 보여주세요:
- 이름, 평가한 영화 수, 평균 평점, 친구 수, 팔로우하는 인물 수.  
모든 사용자가 결과에 포함되어야 합니다.

<details>
<summary>💡 정답 보기</summary>

```cypher
MATCH (u:User)
OPTIONAL MATCH (u)-[r:RATED]->(:Movie)
WITH u, count(r) AS 평가수, avg(r.rating) AS 평균평점
OPTIONAL MATCH (u)-[:FRIENDS_WITH]->(f:User)
WITH u, 평가수, 평균평점, count(DISTINCT f) AS 친구수
OPTIONAL MATCH (u)-[:FOLLOWS]->(p:Person)
RETURN u.name AS 사용자, 평가수, 평균평점, 친구수, count(DISTINCT p) AS 팔로잉수
ORDER BY 사용자;
```

**해설:** 여러 `OPTIONAL MATCH`와 `WITH`를 단계적으로 결합한 대시보드형 쿼리. 그래프 데이터의 다양한 측면을 한 번에 뽑아낼 수 있습니다.

</details>

---

## 📌 학습 후기 / 다음 단계

이 12개 핵심 절(Clause)을 익히면, 실무 Cypher 쿼리의 약 **80~90%**는 충분히 작성할 수 있습니다.

**다음 단계로 추천:**
1. **인덱스와 제약조건 (`CREATE INDEX`, `CREATE CONSTRAINT`)** - 성능 최적화
2. **`UNWIND`** - 리스트를 행으로 펼치기
3. **`CALL` 과 APOC 라이브러리** - 고급 함수와 절차
4. **그래프 알고리즘 라이브러리 (GDS)** - PageRank, 커뮤니티 검출 등
5. **Graph RAG와의 연계** - LLM과 결합한 지식 그래프 검색

---

> 💡 **꿀팁:** Neo4j Browser의 `:play movie graph`나 `:play got` 같은 내장 튜토리얼도 함께 활용해보세요!
