# 2. Graph DB 개요

## 2.1 지식 그래프란?

지식 그래프(Knowledge Graph)는 현실 세계의 정보를 '객체(엔티티)'와 '객체 간의 관계'로 연결하여 표현한 그래프 형태의 데이터 구조다.

핵심 특징:
- 노드는 실제 세계의 개체(사람, 장소, 개념 등)를 나타낸다.
- 엣지는 개체 간의 의미 있는 관계를 나타낸다.
- 관계에 의미(semantics)가 있다. 단순히 연결되어 있다는 것이 아니라, 어떤 관계인지를 명시한다.

**예시: 영화 지식 그래프**

```text
봉준호 ─[감독했다]─▶ 기생충
송강호 ─[출연했다]─▶ 기생충
기생충 ─[작품상을 수상했다]─▶ 아카데미
```

이 구조를 사용하면 "봉준호가 감독한 영화 중 수상 이력이 있는 작품" 또는 "봉준호가 감독한 영화에 출연한 배우(송강호)"를 자연스럽게 탐색할 수 있다.

**지식 그래프 vs 단순 그래프**

지식 그래프는 단순한 연결 그래프와 달리, 관계의 타입과 방향이 명시적이다. "A와 B가 연결되어 있다"가 아니라 "A가 B를 감독했다", "A가 B에 소속되어 있다"처럼 의미를 담는다.

**GraphRAG에서의 역할**

GraphRAG에서는 문서로부터 지식 그래프를 구축하는 것이 핵심 단계다. LLM을 이용해 텍스트에서 엔티티와 관계를 자동으로 추출하고, 이를 Neo4j 같은 그래프 DB에 저장해서 지식 그래프를 만든다.

---

## 2.2 Graph DB란?

Graph DB(그래프 데이터베이스)는 데이터를 노드(node)와 관계(relationship)로 저장하는 데이터베이스다.

기존 관계형 DB(RDB)는 데이터를 테이블 형태로 저장하고 JOIN으로 연결한다. Graph DB는 처음부터 연결 관계를 데이터의 핵심 구조로 취급한다. 연결이 많아질수록 Graph DB의 탐색 성능은 RDB보다 유리하다.

대표적인 Graph DB:
- **Neo4j**: 가장 널리 쓰이는 Graph DB. Cypher 쿼리 언어 사용.
- Amazon Neptune, ArangoDB, TigerGraph 등도 있다.

---

## 2.3 Node, Relationship, Property

Node, Relationship, Property가 그래프 DB의 핵심 구성 요소다.

- **Node (노드)**
  - 그래프의 객체/엔티티를 나타낸다.
    > - 엔티티(Entity): 현실 세계에서 독립적으로 식별하고 구별할 수 있는 대상(사람, 장소, 사물, 개념등)을 말한다. Graph DB에서는 노드(Node)로 표현되는 실제 객체를 의미.
  - 레이블(Label)로 종류를 구분한다.
    - **노드는 실제 객체, 레이블은 (노드의) 타입**이다.
    (예: 홍길동 : 사람 → 홍길동: Node, 사람: Label)
  - 예: `:Person`, `:Movie`, `:Product`, `:Company`

    ```cypher
    ( :Person {name: "김철수", age: 30} )
    ```

- **Relationship (관계)**
  - 두 노드간의 관계를 표현한다.
    - Relationship는 그래프 구조에서 두 노드를 연결하는 엣지(Edge)이다.
  - 항상 방향(Direction)이 있다.
    - 조회시에는 방향을 무시하여 양방향으로 탐색할 수 있지만 저장할 때는 단방향성으로 설계한다.
  - 타입(type)으로 관계의 의미를 표현한다.
  - 예: `ACTED_IN`, `WORKS_AT`, `PURCHASED`

    ```cypher
    (:Person)-[:ACTED_IN]->(:Movie)
    ```

- **Property (속성)**
  - **노드**나 **관계**에 대한 특징이나 정보를 말하며, 속성은 `Key-Value` 쌍 형태의 데이터이다.
    - 노드 뿐 아니라 관계도 속성을 가진다.
  - 예: `{name: "김수영"}`, `{since: 2020}`

    ```cypher
    ( :Person {name: "유지은", age: 30} ) // {name: "유지은", age: 30} 이 :Person 노드의 Property들 이다.
    ```

- **전체 구조 예시**

  ```cypher
  (:Person {name:"김철수"})-[:WORKS_AT {since:2020}]->(:Company {name:"ABC Corp"})
                                            ↓
  (:Company {name:"ABC Corp"})-[:LOCATED_IN]->(:City {name:"서울"})
  ```

## 2.4 RDB, VectorDB, GraphDB의 차이

세 DB는 서로 다른 데이터 구조와 검색 방식을 갖는다.

| 구분 | RDB | VectorDB | GraphDB |
|------|-----|----------|---------|
| 저장 구조 | 행·열 (테이블) | 고차원 벡터 | 노드·엣지 (그래프) |
| 데이터간 연결 방식 | JOIN | 없음 | 관계(Relationship) |
| 검색 알고리즘 | SQL | 유사도 검색 (ANN) | 그래프 탐색 (패턴 매칭) |
| 강점 | 정형 데이터관리, 조건 일치 조회 | 의미 기반 유사 검색 | 관계 탐색, 다단계 연결 |
| 약점 | 복잡한 JOIN에서 성능 저하 | 관계 표현이 어려움 | 관계 모델링이 어렵고, 대규모 분석(집계)이나 단순 조건 검색에는 비효율적 |
| 쿼리 언어 | SQL | 없음 (API) | Cypher (Neo4j 기준), GQL, Gremlin |

세 DB는 경쟁이 아니라 역할이 다르다. 
특히 GraphRAG를 구현할 때는 GraphDB와 VectorDB를 함께 사용하는 경우가 많다.
