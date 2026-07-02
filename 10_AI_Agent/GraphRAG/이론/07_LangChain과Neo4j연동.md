# 7. LangChain과 Neo4j 연동

**설치**

```bash
pip install langchain-neo4j
```



## 7.1 Neo4j 연결 설정

`langchain-neo4j` 패키지의 `Neo4jGraph`를 사용해 Neo4j에 연결한다.

```python
import os
from langchain_neo4j import Neo4jGraph

# DB 연결정보
NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
NEO4J_DATABASE = os.environ.get("NEO4J_DATABASE")

# Database 연결
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    database=NEO4J_DATABASE
)

# 연결 확인 (스키마 출력)
print(graph.schema)
```

`Neo4jGraph`는 연결 시 자동으로 DB 스키마(노드 레이블, 관계 타입, 프로퍼티)를 로드해서 `schema` 속성에 저장한다. 이 스키마를 LLM이 참고해서 Cypher 쿼리를 생성한다.


## 7.2 LangChain에서 Neo4j 사용하기

`Neo4jGraph.query()`로 직접 Cypher 쿼리를 실행하거나, `GraphCypherQAChain`으로 자연어 질문을 처리할 수 있다.

**직접 Cypher 쿼리 실행**

```python
# Cypher 쿼리 직접 실행
result = graph.query("""
    MATCH (m:Movie)<-[:ACTED_IN]-(p:Person)
    RETURN m.title AS movie, collect(p.name) AS actors
    LIMIT 5
""")
# 조회결과: list[dict]

for row in result:
    print(row)

```

**GraphCypherQAChain: 자연어로 그래프 질의**

`GraphCypherQAChain`은 자연어 질문을 Cypher 쿼리로 자동 변환하고, 그 결과를 LLM이 자연어로 답변하는 체인(Runnable)이다.

```python
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI

graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    database=NEO4J_DATABASE
)

llm = ChatOpenAI(model="gpt-5.5", temperature=0)

chain = GraphCypherQAChain.from_llm(
    llm=llm, 
    graph=graph, 
    allow_dangerous_requests=True,
    verbose=True
)

response = chain.invoke({"query": "The Matrix에 출연한 배우는 누구인가?"})
print(response["result"])
```

**내부 동작 흐름**

```text
사용자 질문(자연어)
    ↓
스키마와 질문을 LLM에 전달 → Cypher 쿼리 생성
    ↓
Neo4j에서 쿼리 실행 → 결과 반환
    ↓
질문 + 검색 결과를 LLM에 전달 → 자연어 답변 생성
```
