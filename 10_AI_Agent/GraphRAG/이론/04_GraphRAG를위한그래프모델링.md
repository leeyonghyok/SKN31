# 4. GraphRAG를 위한 그래프 모델링

그래프 디비(Graph Database) 모델링은 현실의 정보를 Node, Relationship, Property로 어떻게 표현할지 설계하는 과정이다. 모델링이 잘못되면 Cypher 쿼리가 복잡해지고, GraphRAG의 검색 품질도 떨어진다.

## 4.1 어떤 것을 Node로 만들 것인가?

**Node는 독립적으로 존재하거나 다른 개체에 의해 참조될 수 있는 개체(entity)에 사용한다.**

독립적인 존재란, 다른 것과 관계없이 그 자체로 의미를 갖는 것을 말한다. 예를 들어 "사람", "영화", "회사"는 Node로 만들기에 적합하다. 반면 "나이", "평점"처럼 어떤 개체의 속성값에 불과한 것은 Property로 두는 것이 맞다.

**Node로 만드는 기준**

- 여러 관계의 중심이 되는가 → Node
- 다른 개체에서 독립적으로 참조될 수 있는가 → Node
- 그 자체를 직접 검색하거나 탐색의 시작점이 되는가 → Node

**예시: 영화 도메인**

| 후보 | 판단 | 이유 |
|------|------|------|
| 영화 | Node ✅ | 독립 개체, 여러 관계의 중심 |
| 감독 | Node ✅ | 독립 개체, 여러 영화와 연결 |
| 장르 | Node ✅ | 여러 영화가 공유, 직접 검색 대상 |
| 상영 시간 | Property ❌ | 영화의 속성값, 단독 참조 안 됨 |
| 평점 | Property ❌ | 영화의 속성값 |

**예시: 기업 정보 도메인 (GraphRAG 활용 예)**

```
Node:  회사, 인물, 제품, 기술, 업종
Property: 설립연도, 직함, 출시일
```

---

## 4.2 어떤 것을 Relationship으로 만들 것인가?

**Relationship은 두 Node 사이의 연결 그 자체를 표현한다.**   
Relationship은 방향을 가지며, **동사(verb) 형태로 이름**을 붙이는 것이 원칙이다. Relationship도 perperty(속성)들을 가질 수 있다. 

- **Relationship으로 만드는 기준**

  - 두 Node 사이에 어떤 행위, 역할, 연관이 있는가 → Relationship
  - 방향이 있거나 의미 있는 연결인가 → Relationship
  - 연결 자체에 속성(언제, 어느 정도, 어떤 역할)이 붙을 수 있는가 → Relationship + Property

- **Relationship 이름 규칙**

  - 대문자의 스네이크케이스: `DIRECTED`, `ACTED_IN`, `WORKS_FOR`
  - 동사 또는 동사구로 작성
  - 모호한 이름 지양
    -  `RELATED_TO` (❌-관계가 있다. 어떤 관계인지 모호하다.) → `COLLABORATED_WITH` (✅ - 협력관계에 있다. 구체적으로 어떤 관계인지를 설명하고 있다.)

- **예시**

  ```
  (홍길동:Person)-[:DIRECTED]->(명량:Movie)
  (이순신:Person)-[:ACTED_IN {role: "장군"}]->(명량:Movie)
  (명량:Movie)-[:BELONGS_TO]->(액션:Genre)
  ```

- **Relationship에 Property를 붙이는 경우**
  - Relationship 자체에 부가 정보가 있을 때 Property를 붙인다.

  ```cypher
  // 역할을 관계 프로퍼티로 표현
  (배우)-[:ACTED_IN {role: "주인공"}]->(영화)

  // 재직 기간을 관계 프로퍼티로 표현
  (인물)-[:WORKS_FOR {start: 2019, end: 2023}]->(회사)
  ```

## 4.3 어떤 것을 Property로 둘 것인가?

**Property는 Node나 Relationship의 세부 속성값이다.**

Property로 두어야 할 것과 Node로 분리해야 할 것을 구분하는 것이 핵심이다.

**Property로 두는 기준**

- 스칼라 값(문자열, 숫자, 불리언, 날짜)이다
- 여러 개체가 공유하지 않는 값이다
- 직접 탐색의 시작점이 될 필요가 없다
- 해당 개체나 관계를 설명하는 속성이다

**Property vs Node 예**

| 후보 | Property | Node | 판단 기준 |
|------|----------|------|-----------|
| 영화 개봉연도 | ✅ | ❌ | 영화의 속성값, 단독 참조 불필요 |
| 장르 이름 | ❌ | ✅ | 여러 영화가 공유, 직접 검색 대상 |
| 사람의 나이 | ✅ | ❌ | 특정 사람의 속성값 |
| 기술 스택 (Python, Java) | ❌ | ✅ | 여러 인물·회사가 공유, 탐색 중심 가능 |
| 관계의 시작일 | ✅  | ❌ | 관계(Relationship)의 부가 정보 |

**예시**

```cypher
// Node에 Property
CREATE (m:Movie {
  title: "명량",           // 제목
  released: 2014,          // 개봉연도
  runtime: 126,            // 상영시간(분)
  tagline: "두려움을 용기로"  // 홍보 문구
})

// Relationship에 Property
CREATE (p:Person)-[:ACTED_IN {
  role: "이순신",
  award: "최우수연기상"
}]->(m:Movie)
```

## 4.4 좋은 스키마와 나쁜 스키마 예시

GraphRAG용 스키마는 특히 "LLM이 생성하는 Cypher 쿼리로 탐색하기 쉬운 구조"여야 한다.

### 예시 도메인: IT 기업 정보 시스템

**나쁜 스키마 ❌**

```cypher
(회사:Company {
  name: "카카오",
  ceo: "홍길동",                       // ← CEO를 문자열로 저장함.
  products: "카카오톡, 카카오맵",         // ← 제품 목록을 문자열로 저장함.
  tech_stack: "Python, Java, Kotlin"   // ← 기술을 문자열로 저장함
})
```

문제점:
- CEO, Product, tech_stack의 entity 들을 노드로 정의하고 Company와 관계를 연결하는 방식을 설계한다.
- 그래야 "홍길동이 CEO인 회사는?", "python을 사용하는 회사는?", "카카오가 만든 제품은?" 와 같은 질문을 관계 기반 그래프 탐색으로 조회할 수 있다.
  
**좋은 스키마 ✅**

```cypher
// 독립 Node로 분리
CREATE (kakao:Company {name: "카카오", founded: 2010})
CREATE (hong:Person {name: "홍길동", title: "대표이사"})
CREATE (kakao_talk:Product {name: "카카오톡", launched: 2010})
CREATE (python:Technology {name: "Python"})

// Relationship으로 연결
CREATE (hong)-[:CEO_OF]->(kakao)
CREATE (kakaotalk)-[:MADE_BY]->(kakao)
CREATE (kakao)-[:USES]->(python)
```

이렇게 하면 다음 질문을 Cypher로 바로 처리할 수 있다:
- "홍길동이 CEO인 회사는?" → `MATCH (p:Person {name:"홍길동"})-[:CEO_OF]->(c:Company) RETURN c`
- "Python을 사용하는 회사는?" → `MATCH (c:Company)-[:USES]->(:Technology {name:"Python"}) RETURN c`
- "카카오가 만든 제품은?" → `MATCH (:Company {name:"카카오"})<-[:MADE_BY]-(p:Product) RETURN p`



## 4.5 GraphRAG 질문에서 스키마가 중요한 이유

GraphRAG는 사용자의 자연어 질문을 Cypher 쿼리로 변환하여 그래프를 탐색한다. 이 변환 과정에서 스키마가 결정적인 역할을 한다.

**스키마가 검색 품질을 결정하는 이유**

LLM은 그래프의 실제 데이터를 모른다. LLM이 알 수 있는 것은 스키마(Node 레이블, Relationship 타입, Property 이름)뿐이다. 스키마가 명확해야 LLM이 정확한 Cypher query를 생성할 수 있다.

```
사용자: "Python을 쓰는 회사의 CEO는?"

LLM이 생성하는 Cypher query(좋은 스키마일 때 - Company, Person-CEO, Technology로 Label이 잘 분리되고 그 관계가 잘 표현되있는 경우):
MATCH (c:Company)-[:USES]->(:Technology {name:"Python"})
      <-[:CEO_OF]-(p:Person)
RETURN c.name, p.name

LLM이 생성하는 Cypher (나쁜 스키마일 때 - Company Node에 CEO, Technology가 property로 다 들어가 있는 스키마):
MATCH (c:Company)
WHERE c.tech_stack CONTAINS "Python"   ← 정확하지 않음, CONTAINS는 부분 문자열 검색
RETURN c.name, c.ceo                   ← CEO가 문자열이라 추가 탐색 불가
```

**스키마 설계 시 GraphRAG 관점에서 확인할 것**

- 자주 물어볼 질문을 미리 떠올린다: "누가 무엇을 했는가", "A와 B의 관계는?", "C를 통해 연결된 것은?"
- 그 질문을 Cypher로 표현할 수 있는지 확인한다.
- Cypher로 표현되지 않는다면 스키마를 재설계한다.
  - 정리하면 **그래프 스키마를 먼저 만들고 질문을 끼워 맞추는 것이 아니라, 자주 물어볼 질문을 먼저 정하고 그 질문이 자연스럽게 Cypher 패턴으로 표현되는지 확인** 한다.


## 모델링 체크리스트

그래프 스키마를 설계한 뒤 아래 항목을 점검한다.

```
□ 자주 묻는 질문을 Cypher로 표현할 수 있는가?
□ Node Label(레이블)은 명사 단수형인가? (Person, Company, Product)
□ Relationship 이름은 동사 대문자인가? (DIRECTED, WORKS_FOR)
□ 다른 Node로 분리해야 할 대상을 단순 문자열이나 문자열 배열로만 저장하지 않았는가? (Movie {actor: '전지현, 구교환, 지창욱' } -> Movie와 Actor로 분리하고 관계를 연결한다.)
□ Relationship에 부가 정보가 있다면 Property로 추가 하였는가? ((p:Person)-[:WORKS_FOR {since: 2020, position: '책임연구원'}]->(c:Company))
□ LangChain의 graph.schema 출력이 사람이 읽기 쉬운가?
```
