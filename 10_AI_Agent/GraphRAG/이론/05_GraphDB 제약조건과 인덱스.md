
# 5. 제약조건과 인덱스

## 5.1 제약조건(Constraint)

제약조건은 그래프 데이터에 대해 **반드시 지켜야 하는 규칙** 이자 **잘못된 데이터가 들어가지 못하게 막는 역할**을 한다
예를 들어 제약조건을 통해 다음과 같은 요구사항을 DB 차원에서 강제할 수 있다.

- Person 노드의 email은 중복되면 안 된다.
- Movie 노드는 title 속성을 반드시 가져야 한다.
- User 노드는 id와 email을 반드시 가지고, 조합이 유일해야 한다.
- Product 노드의 price는 반드시 INTEGER여야 한다.

### 제약조건 기본 구문
제약 조건은 노드나 관계의 속성에 설정한다.

#### 노드 제약조건 기본형

```cypher
CREATE CONSTRAINT 제약조건이름 [IF NOT EXISTS]
FOR (n:라벨) 
REQUIRE 조건;
```

예:

```cypher
CREATE CONSTRAINT person_email_unique IF NOT EXISTS
FOR (p:Person) 
REQUIRE p.email IS UNIQUE;
```
- `IF NOT EXISTS`는 옵션으로 같은 이름의 제약조건이 이미 있으면 생성하지 않는다.

#### 관계 제약조건 기본형

```cypher
CREATE CONSTRAINT 제약조건이름 [IF NOT EXISTS]
FOR ()-[r:관계타입]-()
REQUIRE 조건;
```

예:

```cypher
CREATE CONSTRAINT review_id_unique IF NOT EXISTS
FOR ()-[r:REVIEWED]-()
REQUIRE r.reviewId IS UNIQUE;
```

#### 제약조건 조회, 삭제

**제약 조건 조회**
```cypher
SHOW CONSTRAINTS;
```

**제약조건 삭제**

```cypher
DROP CONSTRAINT 제약조건이름;
```
예:
```cypher
DROP CONSTRAINT person_email_unique;
```
## 제약조건 종류

Neo4j의 주요 제약조건은 다음과 같다.

| 구문                                 | 의미                             | 비고   |
| ------------------------------------ | -------------------------------- |--------| 
| `IS UNIQUE`                          | 특정 속성값이 중복되지 않도록 함 | 없는 것은 가능       |
| `IS NOT NULL`                        | 특정 속성이 반드시 존재하도록 함 |        |
| `IS NODE KEY`, `IS RELATIONSHIP KEY` | 속성 존재 + 유일성 보장          |   각각     |
| `IS :: 타입`                         | 속성 타입을 제한                 | IS :: INTEGER |


### 여러 속성 조합 제약조건 지정
```cypher
CREATE CONSTRAINT movie_title_year_unique
FOR (m:Movie)
REQUIRE (m.title, m.year) IS UNIQUE;
```
- 이 경우 ``(title, year)` 조합이 유일해야 한다.

### 제약조건 예

**사람 이름은 필수**
```cypher
CREATE CONSTRAINT person_name_exists IF NOT EXISTS
FOR (p:Person)
REQUIRE p.name IS NOT NULL;
```

**사람 email은 유일**

```cypher
CREATE CONSTRAINT person_email_unique IF NOT EXISTS
FOR (p:Person)
REQUIRE p.email IS UNIQUE;
```
**영화 title과 year 조합은 유일**
```cypher
CREATE CONSTRAINT movie_title_year_unique IF NOT EXISTS
FOR (m:Movie)
REQUIRE (m.title, m.year) IS UNIQUE;
```

**사용자 id는 필수이면서 유일**

```cypher
CREATE CONSTRAINT user_id_key IF NOT EXISTS
FOR (u:User)
REQUIRE u.userId IS NODE KEY;
```

**상품 가격은 숫자여야 함**

```cypher
CREATE CONSTRAINT product_price_type IF NOT EXISTS
FOR (p:Product)
REQUIRE p.price IS :: INTEGER;
```



## 5.2 인덱스

인덱스는 데이터를 빠르게 찾기 위한 검색 구조이다.
예를 들어 다음 쿼리를 자주 실행한다고 하자.

```cypher
MATCH (p:Person {email: 'a@test.com'})
RETURN p;
```

`Person.email`에 인덱스가 없으면 Neo4j는 저장된 모든 `Person`의 `email` 속성의 값을 비교해야 할 수 있다.
반대로 `Person.email`에 인덱스가 있으면 DB가 해당 값을 더 빠르게 찾을 수 있다.
즉 **인덱스의 목적은 조회 성능 향상**에 있다.   
**인덱스는 조회를 빠르게 하지만, 쓰기 작업에는 비용이 생기기 때문에 검색에 많이 사용되는 속성에만 인덱스를 생성한다.**

### 인덱스 기본 구문

#### 기본 인덱스 생성

```cypher
CREATE INDEX 인덱스이름 [IF NOT EXISTS]
FOR (n:라벨)
ON (n.속성);
```
- `IF NOT EXISTS`는 옵션으로 같은 이름의 Index가 이미 있으면 생성하지 않는다.

**기본구문 예**
```cypher
CREATE INDEX person_name_index IF NOT EXISTS
FOR (p:Person)
ON (p.name);
```

**여러 속성 복합 인덱스**

```cypher
CREATE INDEX movie_title_year_index
FOR (m:Movie)
ON (m.title, m.year);
```

**관계 속성 인덱스**

```cypher
CREATE INDEX reviewed_rating_index
FOR ()-[r:REVIEWED]-()
ON (r.rating);
```

#### 인덱스 조회, 삭제
**인덱스조회**
```cypher
SHOW INDEXES;
```

**인덱스 삭제**

```cypher
DROP INDEX 인덱스이름;
```

### 인덱스 종류

Neo4j의 인덱스는 크게 두 범주로 나눌 수 있다.

| 인덱스 종류                | 용도          |
| -------------------------- | ------------- |
| Range, Text, Point, Lookup | 일반 조회 성능 향상(Range가 default)   |
| Full-text, Vector          | 전문 검색, 유사도 검색 등 검색방식 |

