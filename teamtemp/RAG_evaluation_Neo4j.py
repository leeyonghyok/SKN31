#!/usr/bin/env python
# coding: utf-8

# # 1. RAG 평가 개요
# - RAG 평가란 RAG 시스템이 주어진 입력에 대해 얼마나 효과적으로 관련 정보를 검색하고, 이를 기반으로 정확하고 유의미한 응답을 생성하는지를 측정하는 과정이다. 
# - **평가 요소**
#     - **검색 단계 평가**
#         - 입력 질문에 대해 검색된 문서나 정보의 관련성과 정확성을 평가.
#     - **생성 단계 평가**
#         - 검색된 정보를 기반으로 생성된 응답의 품질, 정확성등을 평가.
# - **평가 방법**
#     - **온/오프라인 평가**
#         1. **오프라인 평가**
#             - 미리 준비된 데이터셋을 활용하여 RAG 시스템의 성능을 측정한다.
#         2. **온라인 평가**
#             - 실제 사용자 트래픽과 피드백을 기반으로 시스템의 실시간 성능을 평가한다.
#     - **정량적/정성적 평가**
#         1. 정량적 평가
#             - 자동화된 지표를 사용하여 생성된 텍스트의 품질을 평가한다.
#         2. 정성적 평가
#             - 전문가나 일반 사용자가 직접 생성된 응답의 품질을 평가하여 주관적인 지표를 평가한다.

# # 2. [RAGAS](https://www.ragas.io/)
# - RAGAS는 RAG 파이프라인을 **정량적으로 평가하는** 오픈소스 프레임 워크이다. 
# - RAGAS 문서: https://docs.ragas.io/en/stable/
# ## 2.1 설치
# - `pip install ragas rapidfuzz`

# ## 2.2 RAGAS 평가 지표 개요
# ![ragas_score](figures/ragas_score.png)
# - **Generation**
#     - llm 모델이 생성한 답변에 대한 평가 지표들.
#     - **Faithfulness(신뢰성)**
#         -  생성된 답변과 검색된 문서(context)간의 관련성을 평가하는 지표
#         -  생성된 답변이 주어진 문맥(context)에 얼마나 충실한지를 평가하는 지표로 할루시네이션에 대한 평가로 볼 수있다.
#     - **Answer relevancy(답변 적합성)**
#         - 생성된 답변과 사용자의 질문간의 관련성을 평가하는 지표
#         - 생성된 답변이 사용자의 질문과 얼마나 관련성이 있는지를 평가하는 지표.
# - **Retrieval**
#     -  질문에 대해 검색한 문서(context)들에 대한 평가
#     -  **Context Precision(문맥 정밀도)**
#         -  검색된 문서(context)들 중 질문과 관련 있는 것들이 **얼마나 상위 순위에 위치하는지** 평가하는 지표.
#     -  **Context Recall(문맥 재현률)**
#         -  검색된 문서(context)가 정답(ground-truth)의 정보를 얼마나 포함하고 있는지 평가하는 지표.
# - 이러한 지표들은 RAG 파이프라인의 성능을 다각도로 평가하는 데 활용된다.
# ![RAGAS_score2](figures/RAGAS_score2.png)

# ## 2.3 주요 평가지표
# ### 2.3.1 Generation 평가
# - LLM이 생성한 답변에 대한 평가
#   
# #### 2.3.1.1 Faithfulness (신뢰성)
# - 생성된 답변이 얼마나 주어진 검색 문서들(context)를 잘 반영해서 생성되었는지 평가한다. 할루시네이션에 대한 평가라고 할 수 있다. 
# - 점수범위: **0 ~ 1** (1에 가까울수록 좋음)
# - 답변에 포함된 모든 주장이 context에서 얼마나 추출 가능한지를 확인한다.
# 
# ##### 2.3.1.1.1평가 방법
# 1. Answer에서 주장 구문(claim statement)들을 생성(추출)한다. (주장이란, 질문(user input)과 관련된 내용)
#     - 예) 
#         - **질문**: 한국의 수도는 어디이고 인구는 얼마나 되나요? 
#         - **LLM 답변**: 한국의 수도는 서울이고 인구수는 3000만명이다. 
#         - **주장(claim)**: 
#             1. 한국의 수도는 서울이다.
#             2. 인구수는 3000만명이다.
# 2. 각 주장들을 context로 부터 추론 가능한지 판단한다. 이를 바탕으로 faithfulness 점수를 계산한다.
#     - 예)
#         - context: 한국은 동아시아에 위치하고 있는 나라다. 한국의 수도는 서울이다. .... 한국의 인구는 5000만명이고 서울에 1000만이 살고 있다.
#         - 위 context에서 추론 가능한 주장: 
#             - 한국의 수도는 서울이다. -> context에서 추론가능한 주장.
#             - 한국의 인구는 3000만명이다. -> context에서 추론 불가능한 주장.
# 3. **Faithfulness score** 를 계산한다. 총 주장 수 중에서 context로 부터 추론가능한 주장의 개수.    
#     - 예)
#         - Faithfulness Score = $\cfrac{1}{2} = 0.5$ (두 개의 주장 중 한 개의 주장만 context에서 유추할 수있다.)
#     - LLM 답변에서 주장을 추출 하는 것과 각 주장이 context에서 추론 가능한 지를 판단하는 것은 LLM 을 활용한다.
# - 공식
#     $$
#     \text{Faithfulness Score}\;=\;\cfrac{\text{주어진\;context\;에서\;추론할\;수\;있는\;주장의\;개수}}{\text{총\;주장\;개수}}
#     $$

# ### 2.3.2 Answer relevancy (답변 적합성)
# - 생성된 답변이 질문(user input)에 얼마나 잘 부합하는 지를 평가한다.
# - 점수 범위: -1~1 (1에 가까울수록 좋음)
# - LLM이 생성한 답변을 기반으로 질문들을 생성한다. 이렇게 생성한 질문들과 실제 질문(user input) 간의 유사도를 측정한다.
# 
# #### 2.3.2.1 평가방법
# 1. LLM이 생성한 답변을 기반으로 질문들을 생성한다.
#     - 예) 
#         - **LLM** 답변: 한국의 수도는 서울이고 인구수는 3000만명이다. 
#         - **생성된 질문**: 
#             1. 한국의 수도는 어디이고 인구는 얼마나 되나요?
#             2. 한국의 수도는 어디인가요?
#             3. 한국의 인구는 얼마나 되나요?
# 2. 실제 질문과 생성한 질문간의 코사인 유사도를 측정한다. 그 평균이 최종 점수가 된다.
#     - 예)
#         - **실제 질문**: 한국의 수도는 어디이고 인구는 얼마나 되나요?
#         - **생성된 질문**: 
#             1. 한국의 수도는 어디이고 인구는 얼마나 되나요?
#             2. 한국의 수도는 어디인가요?
#             3. 한국의 인구는 얼마나 되나요?
# - 공식
#   $$
#     \cfrac{1}{N} \sum_{i=1}^{N} \text{cosine\_similarity}(q_{\text{user}_{_i}}, q_{\text{generated}})
#   $$

# 

# ## 2.4 Retrieval 평가
# Vector store에서 검색한 context에 대한 평가
# 
# ### 2.4.1 Context Precision
# - 검색된 문서(context)들 중 질문과 관련 있는 것들이 얼마나 **상위 순위**에 있는 지 평가.
# - 점수 범위: 0~1 (1에 가까울수록 좋음)
# 
# 
# #### 2.4.1.1평가방법
# 
# - 공식
# $$
#  \text{Context\;Precision@K} = \frac{\sum_{k=1}^{K} \left( \text{Precision@k} \times v_k \right)}{\ 상위\;K개\;결과에서의\;관련\;항목\;수}
# $$
# $$
#  \text{Precision@k} = \frac{\text{True\;positive@k}}{(\text{True\;positive@k} + \text{False\;positive@k})} \\
# $$
# - $\text{Precision@k}$: 개별 문서에 대한 Precision
# - K: context 의 개수(chuck 수)
# - $v_k$: 관련성 여부로 0 또는 1. (0: 관련 없음, 1: 관련 있음)
# 
# #### 2.4.1.2 예시
# - 질문과 context 관련성의 예
#     - 질문: 한국의 수도는 어디이고 인구는 얼마나 되나요?
#     - **높은 정밀도 context들**: 질문과 직접적인 관련이 있는 문서들
#         - 한국의 수도는 서울이고 인구는 5000만명 입니다. 
#         - 한국의 수도는 서울입니다.
#         - 한국은 동아시아에 위치해 있는 국가로 수도는 서울입니다.
#         - 한국의 인구는 5000만명 입니다.
#     - **낮은 정밀도 context**: 한국과 관련있어 검색될 수 있지만 질문과 직접적 관련이 없다. 
#         - 한국은 동아시아에 위치한 국가입니다.
#         - 한국의 K-pop은 전 세계적으로 유명합니다.
#         - 비빔밥, 불고기는 한국의 대표적인 음식입니다.
#     - **높은 정밀도의 context이 상위 순위에 위치했으면 높은 점수를 받는다.**
# 
# - 점수 계산 예:
#     - **상위 5개의 검색 결과 중 1번째, 3번째, 4번째 문서가 관련이 있다고 가정하자.**
#     - **Precision@K 계산**
#         ```bash
#             Precision@1 = 1/1 = 1.0    # True positive@1/(True positive@1 + False positive@1).  1/1(1번 문서 계산 시에는 1개 문서만 있으므로 분모가 1이 된다.)
#             Precision@2 = 1/2 = 0.5
#             Precision@3 = 2/3 ≈ 0.67    
#             Precision@4 = 3/4 = 0.75
#             Precision@5 = 3/5 = 0.6
#         ```
#     - **vk의 값**
#         - 1번째: $v_1 = 1$ - 관련있음
#         - 2번째: $v_2 = 0$ - 관련없음
#         - 3번째: $v_3 = 1$ - 관련있음
#         - 4번째: $v_4 = 1$ - 관련있음
#         - 5번째: $v_5 = 0$ - 관련없음
# 
#     - **Context Precision@5**
#         $$
#         \text{Context\;Precision@5} = \frac{(1.0 \times 1) + (0.5 \times 0) + (0.67 \times 1) + (0.75 \times 1) + (0.6 \times 0)}{3} = \frac{1.0 + 0 + 0.67 + 0.75 + 0}{3} ≈ 0.807
#         $$

# ### 2.4.2 Context Recall (문맥 재현률)
# - 검색된 문서(context)가 얼마나 정답(ground-truth)의 정보를 포함있는 지 평가하는 지표
# - 점수 범위: 0~1 (1에 가까울수록 좋음)
# - **정답(ground truth)의 각 주장(claim)이 검색된 context와 얼마나 일치**하는지 계산함.
# 
# #### 2.4.2.1 평가방법
# 1. 정답에서 주장(claim)들을 생성(추출)한다.
#     - 예) 
#         - **정답**: 한국의 수도는 서울이고 인구수는 5000만명이다. 
#         - **주장(claim)**: 
#             1. 한국의 수도는 서울이다.
#             2. 인구수는 5000만명이다.
# 2. 각 주장(claim)의 정보를 검색된 contexts에서 찾을 수 있는지 판별한다. 이를 바탕으로 context recall 점수를 계산한다.
#     - 예)
#         - context: 한국은 동아시아에 위치하고 있는 나라다. 한국의 수도는 서울이다.
#         - 위 context에서 추론 가능한 주장: 
#             - 한국의 수도는 서울이다. -> context에서 찾을 수 있다.
#             - 한국의 인구는 5000만명이다. -> context에서 찾을 수 없다.
# 3. **Context Recall Score** 를 계산한다. 총 주장 수 중에서 context로 부터 찾을 수 있는 주장의 개수.
#     - 예)
#         - Context Recall Score = $\cfrac{1}{2} = 0.5$ (두 개의 주장 중 한 개의 주장만 context에서 찾을 수 있다.)
# 
# - 공식
#     $$
#     \text{Context Recall Score}\;=\;\cfrac{\text{GT의\;주장\;중\;주어진\;context\;에서\;찾을\;수\;있는\;주장의\;개수}}{\text{GT의\;총\;주장\;개수}}
#     $$ 

# # 3. RAGAS 평가 실습

# In[2]:


# !uv pip install ragas rapidfuzz
# 설치 후 커널 재시작


# In[3]:


# Neo4j를 로컬에서 띄우는 예시 (law_pdfs_to_neo4j_pipeline.ipynb 에서 이미 적재된 DB에 연결만 하면 되므로,
# Neo4j 컨테이너가 이미 떠 있다면 이 셀은 실행할 필요 없습니다)
# docker run -p 7474:7474 -p 7687:7687 -v neo4j_data:/data -e NEO4J_AUTH=neo4j/your_password neo4j:latest


# ## 3.1 Neo4j 연결 및 Retriever 생성
# 앞서 `law_pdfs_to_neo4j_pipeline.ipynb`로 적재해둔 Neo4j DB에 연결만 하고, text-to-Cypher + 벡터 폴백 방식의 retriever를 만듭니다.

# In[4]:


##################################################
# Neo4j 연결 및 retriever 생성
##################################################
import os
import re
from openai import OpenAI
from neo4j import GraphDatabase
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "lawdb")  # law_pdfs_to_neo4j_pipeline.ipynb 와 동일 기본값

CHAT_MODEL = "gpt-5.4-mini"
EMBEDDING_MODEL = "text-embedding-3-large"  # 적재 시 사용한 임베딩 모델과 반드시 동일해야 함

openai_client = OpenAI()
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# 연결 및 적재 상태 확인
with driver.session(database=NEO4J_DATABASE) as session:
    article_count = session.run("MATCH (a:ARTICLE) RETURN count(a) AS c").single()["c"]
    print(f"현재 Neo4j에 적재된 ARTICLE 노드: {article_count}개")
    if article_count == 0:
        print("⚠️ 적재된 데이터가 없습니다. law_pdfs_to_neo4j_pipeline.ipynb를 먼저 실행해주세요.")

FORBIDDEN_KEYWORDS = {"CREATE", "DELETE", "SET", "MERGE", "REMOVE", "DROP", "DETACH"}

# [수정] 관계명 REFERENCE -> REFERENCES
# (law_pdfs_to_neo4j_pipeline.ipynb의 load_references()가 실제로 만드는 관계는
#  MERGE (src)-[:REFERENCES]->(tgt) 이므로 스키마 설명도 이와 일치시켜야 합니다.
#  불일치 시 LLM이 REFERENCE로 Cypher를 짜면 에러 없이 조용히 빈 결과만 나옵니다.)
SCHEMA_DESCRIPTION = """
그래프 DB 스키마:
1. 노드 라벨:
  - LAW (법률/법령 메타데이터)
    * 속성: id (string, 법령명), name (string), law_type (string), promulgation_date (string), effective_date (string)
  - ARTICLE (법령 조문)
    * 속성: id (string, 형식 "법령명::제N조"), name (string, 조문제목), description (string, 본문),
             original_id (string, 예: "제8조"), original_id_normalized (string, 예: "8", "5-2"), law_id (string)

2. 관계(Relationships):
  - (:LAW)-[:CONTAINS]->(:ARTICLE) : 법률이 특정 조문을 포함함.
  - (:ARTICLE)-[:REFERENCES]->(:ARTICLE) : 하나의 조문이 다른 조문을 참조/인용함.

벡터 인덱스: 'article_vector_index' (ARTICLE 노드의 embedding 속성 기준, 의미 검색용, dim=3072, cosine)
"""


class Neo4jRetriever:
    """사용자 질문을 받아 Neo4j(text-to-Cypher + 벡터 폴백)에서 참조 조문을 가져오는 retriever"""

    def __init__(self, client: OpenAI, driver, database: str):
        self.client = client
        self.driver = driver
        self.database = database

    def _is_safe_cypher(self, query: str) -> bool:
        upper = query.upper()
        return not any(re.search(rf"\b{kw}\b", upper) for kw in FORBIDDEN_KEYWORDS)

    def _generate_cypher(self, user_query: str) -> str:
        system_prompt = f"""
당신은 Neo4j Cypher 쿼리를 작성하는 전문가입니다.
아래 그래프 스키마만을 근거로, 사용자 질문에 답하기 위한 최적의 Cypher 쿼리를 작성하세요.

{SCHEMA_DESCRIPTION}

쿼리 작성 가이드라인:
1. 오직 읽기(MATCH) 쿼리만 작성하세요. (CUD 명령어 절대 금지)
2. [특정 조문 지정 질문]: 법령명/조번호가 명시된 경우, 해당 ARTICLE과 REFERENCES로 연결된 조문까지 함께 가져오세요.
3. [주제/의미 검색 질문]: 아래 벡터 검색 형태를 사용하세요:
   CALL db.index.vector.queryNodes('article_vector_index', $top_k, $query_embedding)
   YIELD node, score
   RETURN node.id AS id, node.name AS name, node.description AS description, score
   ORDER BY score DESC
4. RETURN문에는 반드시 'id', 'name', 'description', 'score' 별칭을 사용하세요.
5. 오직 Cypher 쿼리 텍스트만 출력하세요. 마크다운 코드블록이나 설명은 절대 포함하지 마세요.
"""
        response = self.client.chat.completions.create(
            model=CHAT_MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
        )
        cypher = response.choices[0].message.content.strip()
        cypher = re.sub(r'^```(cypher)?\s*|\s*```$', '', cypher, flags=re.MULTILINE).strip()
        return cypher

    def _vector_fallback(self, user_query: str, top_k: int) -> list[dict]:
        embedding = self.client.embeddings.create(
            model=EMBEDDING_MODEL, input=[user_query]
        ).data[0].embedding

        cypher = """
        CALL db.index.vector.queryNodes('article_vector_index', $top_k, $query_embedding)
        YIELD node, score
        RETURN node.id AS id, node.name AS name, node.description AS description, score
        ORDER BY score DESC
        """
        with self.driver.session(database=self.database) as session:
            results = session.run(cypher, top_k=top_k, query_embedding=embedding)
            return [dict(r) for r in results]

    def retrieve(self, user_query: str, top_k: int = 5) -> list[dict]:
        cypher = self._generate_cypher(user_query)

        if not self._is_safe_cypher(cypher):
            return self._vector_fallback(user_query, top_k)

        params = {"top_k": top_k}
        if "query_embedding" in cypher:
            params["query_embedding"] = self.client.embeddings.create(
                model=EMBEDDING_MODEL, input=[user_query]
            ).data[0].embedding

        try:
            with self.driver.session(database=self.database) as session:
                results = session.run(cypher, **params)
                rows = [dict(r) for r in results]
        except Exception:
            return self._vector_fallback(user_query, top_k)

        if not rows:
            return self._vector_fallback(user_query, top_k)

        return rows


neo4j_retriever = Neo4jRetriever(client=openai_client, driver=driver, database=NEO4J_DATABASE)


def _rows_to_documents(rows: list[dict]) -> list[Document]:
    """Neo4jRetriever가 반환하는 list[dict]를 체인이 기대하는 list[Document]로 변환"""
    return [
        Document(
            page_content=row.get("description", ""),
            metadata={"id": row.get("id"), "name": row.get("name"), "score": row.get("score")},
        )
        for row in rows
    ]


# LCEL 체인에서 retriever 자리를 그대로 대체할 수 있도록 Runnable로 감쌈
retriever = RunnableLambda(lambda query: _rows_to_documents(neo4j_retriever.retrieve(query, top_k=5)))


# In[5]:


################################################################################
# 평가할 RAG Chain
################################################################################

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

prompt_txt = """<instruction>
당신은 정보제공을 목적으로하는 유능한 AI Assistant 입니다.
주어진 context의 내용을 기반으로 질문에 답변을 합니다.
Context에 질문에 대한 명확한 정보가 있는 경우 그것을 바탕으로 답변을 합니다.
Context에 질문에 대한 명확한 정보가 없는 경우 "정보가 부족해 답을 할 수없습니다." 라고 답합니다.
절대 추측이나 일반 상식을 바탕으로 답을 하거나 Context 없는 내용을 만들어서 답변해서는 안됩니다.
</instruction>
<context>
{context}
</context>
<question>
{query}
</question>
"""
prompt = ChatPromptTemplate.from_template(template=prompt_txt)

model = ChatOpenAI(model="gpt-5.4-mini")
parser = StrOutputParser()


def format_docs_for_prompt(documents: list[Document]) -> str:
    """LLM 프롬프트({context})용: 조문 id/제목을 헤더로 표기해서 하나의 문자열로 합침"""
    parts = []
    for doc in documents:
        meta = doc.metadata
        header = f"[{meta.get('id', '')} {meta.get('name', '')}]"
        parts.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def format_docs_for_ragas(documents: list[Document]) -> list[str]:
    """RAGAS 평가용: 검색된 문서 각각의 내용을 list[str]로 추출"""
    return [doc.page_content for doc in documents]


def build_prompt_input(state: dict) -> dict:
    """검색 결과({'documents':..., 'query':...})를 prompt 입력({'context':str, 'query':str})으로 변환"""
    return {
        "context": format_docs_for_prompt(state["documents"]),
        "query": state["query"],
    }


# 1단계: 질문으로 검색 → 원본 Document 리스트 + 질문 보존 (retriever는 여기서 1회만 호출됨)
retrieve_step = {
    "documents": retriever,
    "query": RunnablePassthrough(),
}

# RAG 체인 -> RAG 평가 데이터셋을 만드는 RAG Chain -> 최종응답: LLM 응답(str), 검색한 문서들(list[str]), 질문(str)
chain = (
    RunnablePassthrough()  # dict | dict 가 파이썬 dict 병합 연산으로 취급되는 것을 막기 위해 필요
    | retrieve_step
    | {
        "response": RunnableLambda(build_prompt_input) | prompt | model | parser,
        "retrieved_context": RunnableLambda(lambda state: format_docs_for_ragas(state["documents"])),
        "query": RunnableLambda(lambda state: state["query"]),
    }
)


# In[6]:


res = chain.invoke("군인연금법 제8조는 무엇인가요?")


# In[ ]:





# In[7]:


res["response"]


# In[8]:


res["retrieved_context"]


# # 4. RAGAS 를 이용해 평가를 위한 합성 데이터 셋 만들기
# 
# - 평가 데이터셋 구성
#   - `user_input`: 사용자 질문
#   - `retrieved_contexts`: Vectorstore에서 검색한 context
#   - `response`: LLM의 응답
#   - `reference`: 정답
# 
# ## 4.1 TestsetGenerator
# - **문서(retrieved_contexts)를 기준**으로 **질문**, **정답** 을 생성한다.
# - 평가할 LLM으로 생성된 질문을 넣어 답변을 추출하여 데이터셋을 구성한다.
# 
# 
# > **주의**
# > - TestsetGenerator import 시 `No Module named langchain_community.chat_models.vertexai` Error 발생 
# > - RAGAS와 langchain-community의 버전 호환성 문제 때문에 발생한다.
# > - 해결
# >   1. langchain_google_vertexai 설치
# >       - `!uv pip install langchain_google_vertexai`
# >   2. `.venv\Lib\site-packages\langchain_community\chat_models` 디렉토리 아래 `vertexai.py` 파일을 만들고 아래 코드를 > 넣는다.
# >    ```python
# >       try:
# >          from langchain_google_vertexai import ChatVertexAI
# >       except ImportError:
# >           class ChatVertexAI:
# >               def __init__(self, *args, **kwargs):
# >                   raise ImportError(
# >                       "ChatVertexAI requires langchain-google-vertexai. "
# >                       "Install with: pip install langchain-google-vertexai"
# >                   )
# >    ```

# In[9]:


# !uv pip install langchain_google_vertexai


# In[10]:


# 주피터노트북 환경에서 비동기적 처리 위해 
# script(.py) 로 작성할 경우는 필요 없다.

import nest_asyncio
nest_asyncio.apply()


# In[11]:


from ragas.testset import TestsetGenerator


# In[12]:


#
# testset -> Context들(문서들) - [질문 - 정답답변 + (Retriever가 찾은 문서 + LLM 응답: chain에서 생성)]
# 1. Context(문서들)을 추출 - Neo4j에서 ARTICLE 노드를 랜덤 샘플링 -> TestsetGenerator -> 질문과 정답 답변 생성

with driver.session(database=NEO4J_DATABASE) as session:
    total_docs = session.run("MATCH (a:ARTICLE) RETURN count(a) AS c").single()["c"]

    # rand() 정렬로 랜덤 k(5)개 샘플링 (APOC 없이도 동작)
    results = session.run(
        """
        MATCH (a:ARTICLE)
        RETURN a.id AS id, a.name AS name, a.description AS description
        ORDER BY rand()
        LIMIT $k
        """,
        k=5,
    )
    sample_docs = [dict(r) for r in results]

# description(조문 본문)만 추출해서 list[str]
docs = [d["description"] for d in sample_docs]


# In[13]:


total_docs


# In[14]:


sample_docs


# In[15]:


docs


# In[16]:


# testset 생성
from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# testsetgenerator 는 gpt-5 이후 버전은 사용할 수 없다.
## Langchain의 모델과 Embedding 모델 -> ragas에서 사용할 수 있도록 변환(wrapping)
generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4.1"))
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-large"))
generator = TestsetGenerator(
    llm=generator_llm,
    embedding_model=generator_embeddings,
    llm_context="""
- 군 관련 법령(공무원보수규정, 군인사법, 병역법, 군인연금법 등)에 대해 사람들이 궁금해 할 만한 질문들을 생성한다.
- 특정 조문 번호나 법령명을 명시한 질문과, 주제/상황 기반 질문을 골고루 섞는다.
- 데이터셋은 반드시 한국어로 작성한다.
- 데이터셋은 JSON 문법을 지켜서 작성한다. 특히 구두점은 꼭 지켜야 한다.
- 생성된 내용이나 Document에 JSON문법에 맞지 않는 표현이 있으면 반드시 수정해서 처리한다.
"""
    # 질문/답변을 생성할 때 LLM에게 전달할 system Prompt를 설정
)


# In[17]:


testset = generator.generate_with_chunks(
    docs, testset_size=10, # Context 내용 테스트셋 개수(질문 답변 개수)
)


# In[18]:


testset


# In[19]:


sample1 = testset.samples[0].eval_sample
print("사용자질문:", sample1.user_input)
print("Context:", sample1.reference_contexts)
print("생성된 답변(정답):", sample1.reference)
print("평가대상 RAG의 답변:", sample1.response)
print("평가대상 RAG가 검색한 Context:", sample1.retrieved_contexts)


# In[20]:


# 생성된 Testset을 Pandas DataFrame으로 변환
eval_df = testset.to_pandas()


# In[21]:


eval_df.shape


# In[22]:


eval_df


# In[23]:


row_idx = 0
q = eval_df.loc[row_idx, 'user_input']
resp = chain.invoke(q)


# In[24]:


# resp
resp['response']


# In[25]:


# resp
resp['retrieved_context']


# In[26]:


# 모든 testset의 데이터데 대한 llm 응답과 retriever의 검색 겷과를 추가
response_list = []
retrieved_context_list = []

for user_input in eval_df['user_input']:
    resp = chain.invoke(user_input)
    response_list.append(resp["response"])
    retrieved_context_list.append(resp["retrieved_context"])


# In[27]:


print(len(response_list), len(retrieved_context_list))


# In[28]:


response_list


# In[29]:


retrieved_context_list


# In[30]:


#
# eval_df에 컬럼으로 추가
#
eval_df['response'] = response_list
eval_df['retrieved_contexts'] = retrieved_context_list
eval_df


# In[31]:


# eval_df를 ragas의 평가데이터셋 타입으로 변환
from ragas import EvaluationDataset
eval_dataset = EvaluationDataset.from_pandas(
    eval_df[["user_input", "retrieved_contexts", "response", "reference"]]
)
eval_dataset


# In[32]:


#
# 평가
#
from ragas.metrics import (
    LLMContextRecall,
    LLMContextPrecisionWithReference,
    Faithfulness,
    AnswerRelevancy,
)
from ragas import evaluate


# In[33]:


# 평가할 때 사용할 LLM embedding 모델
eval_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4.1"))
eval_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-large"))

metrics = [
    LLMContextRecall(llm=eval_llm),
    LLMContextPrecisionWithReference(llm=eval_llm),
    Faithfulness(llm=eval_llm),
    AnswerRelevancy(llm=eval_llm, embeddings=eval_embeddings)

]
eval_result = evaluate(dataset=eval_dataset, metrics=metrics)


# In[37]:


eval_result


# In[35]:


result_df = eval_result.to_pandas()
result_df


# In[33]:


driver.close()

