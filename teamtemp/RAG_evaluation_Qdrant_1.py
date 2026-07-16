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

# In[1]:


# !uv pip install ragas rapidfuzz
# 설치 후 커널 재시작


# In[2]:


# docker run -p 6333:6333 -p 6334:6334   -v qdrant_storage:/qdrant/storage   qdrant/qdrant
# termianal에서 실행


# ## 0. 패키지 설치

# In[3]:


# 필요한 library: pymupdf pdfplumber pillow openai qdrant-client langchain-core langchain-openai langchain-qdrant langchain-text-splitters python-dotenv


# ## 1. 설정 및 클라이언트 준비
# 

# In[4]:


import os
import re
import glob
import uuid
from pathlib import Path

import fitz  # PyMuPDF
import pdfplumber
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, MatchValue

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ----- 설정값 -----
GUIDANCE_DIR = "./길라잡이"          # 이 폴더 안의 모든 PDF를 찾아서 적재

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
COLLECTION_NAME = "guidance_vectordb"

CHAT_MODEL = "gpt-5.4-mini"                          # 표 요약 / 이미지 캐법션용
EMBED_MODEL = "text-embedding-3-large"         # large 임베딩 모델
EMBED_DIM = 3072

CHUNK_SIZE = 800       # 텍스트 청크 최대 글자 수 (splitter 기준)
CHUNK_OVERLAP = 150    # 청크 간 격치는 글자 수 (문맥 끓김 방지)

openai_client = OpenAI()
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
embeddings = OpenAIEmbeddings(model=EMBED_MODEL)


def ensure_collection() -> bool:
    """collection이 이미 있으면 True(기존 데이터 존재), 없으면 새로 만들고 False를 반환"""
    existing = [c.name for c in qdrant_client.get_collections().collections]
    if COLLECTION_NAME in existing:
        print(f"'{COLLECTION_NAME}' collection이 이미 존재합니다.")
        return True
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
    )
    print(f"'{COLLECTION_NAME}' collection 생성 완료 (dim={EMBED_DIM})")
    return False


collection_already_existed = ensure_collection()

vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

pdf_paths = sorted(glob.glob(str(Path(GUIDANCE_DIR) / "*.pdf")))
print(f"'{GUIDANCE_DIR}' 안에서 발견된 PDF {len(pdf_paths)}개")
for p in pdf_paths:
    print(" -", p)


# ## 2. 텍스트 정제

# In[5]:


def clean_text(text: str) -> str:
    # Private Use Area (U+E000–U+F8FF) 문자 제거
    text = re.sub(r'[\ue000-\uf8ff]', '', text)
    # 과도한 공백/빈 줄 정리
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ## 3. 표 추출 → 마크다운 → 요약

# In[6]:


def table_to_markdown(table_rows):
    rows = [[cell if cell is not None else "" for cell in row] for row in table_rows]
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    md_lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    for row in body:
        md_lines.append("| " + " | ".join(row) + " |")
    return "\n".join(md_lines)


def extract_tables(pdf_path: str):
    tables_out = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            for table in page.extract_tables():
                if not table or len(table) < 2:
                    continue
                md_table = table_to_markdown(table)
                tables_out.append({"page": page_num, "markdown": md_table})
    return tables_out


def summarize_table(table_markdown: str) -> str:
    response = openai_client.chat.completions.create(
        model=CHAT_MODEL,
        max_completion_tokens=300,
        messages=[{
            "role": "user",
            "content": (
                "다음은 문서에서 추출한 표입니다. 이 표가 어떤 내용을 담고 있는지 "
                "검색에 활용할 수 있도록 2~4문장의 한국어로 요약해줘. "
                "컬럼이 의미하는 바와 주요 수치/항목을 포함해줘.\n\n"
                f"{table_markdown}"
            ),
        }],
    )
    return response.choices[0].message.content.strip()


# ## 4. 텍스트 청킹 (페이지 단위)

# In[7]:


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
)

# 이 길이를 넘는 페이지만 splitter로 추가 분할 (그 외엔 페이지 통째로 한 청크)
PAGE_OVERFLOW_THRESHOLD = 1200


def chunk_text_by_page(pdf_path: str) -> list[dict]:
    """페이지 단위로 청크를 만든다. 페이지가 너무 길 때만 그 페이지 안에서 추가로 나눈다."""
    doc = fitz.open(pdf_path)
    results = []

    for page_num, page in enumerate(doc, start=1):
        page_text = clean_text(page.get_text("text"))

        if not page_text:
            continue  # 텍스트 없는 페이지(이미지만 있는 페이지 등)는 건너뜀

        if len(page_text) <= PAGE_OVERFLOW_THRESHOLD:
            results.append({"page": page_num, "text": page_text})
        else:
            # 이 페이지만 너무 길어서 임베딩이 흐려질 수 있는 경우 -> 페이지 내부에서만 분할
            sub_chunks = text_splitter.split_text(page_text)
            for sub in sub_chunks:
                results.append({"page": page_num, "text": sub})

    doc.close()
    return results


# ## 5. PDF 1개 → LangChain `Document` 리스트로 통합

# In[8]:


ID_NAMESPACE = uuid.NAMESPACE_URL


def make_id(doc_name: str, chunk_type: str, index: int) -> str:
    """같은 PDF를 다시 적재해도 같은 ID가 나오도록 결정론적으로 생성 (재실행 시 upsert로 덮어씀)"""
    return str(uuid.uuid5(ID_NAMESPACE, f"{doc_name}::{chunk_type}::{index}"))


def build_documents_for_pdf(pdf_path: str) -> tuple[list[Document], list[str]]:
    doc_name = Path(pdf_path).name
    documents = []
    ids = []
    counter = 0

    # 1) 텍스트 청크
    text_chunks = chunk_text_by_page(pdf_path)
    for c in text_chunks:
        documents.append(Document(
            page_content=c["text"],
            metadata={"doc_name": doc_name, "page": c["page"], "type": "text"},
        ))
        ids.append(make_id(doc_name, "text", counter))
        counter += 1

    # 2) 표
    tables = extract_tables(pdf_path)
    for t in tables:
        summary = summarize_table(t["markdown"])
        documents.append(Document(
            page_content=summary,
            metadata={
                "doc_name": doc_name, "page": t["page"], "type": "table",
                "table_markdown": t["markdown"], "summary": summary,
            },
        ))
        ids.append(make_id(doc_name, "table", counter))
        counter += 1

    print(f"[{doc_name}] 텍스트 {len(text_chunks)} / 표 {len(tables)} → 총 {len(documents)}개")
    return documents, ids


# ## 6. 디렉토리 전체 적재 (upsert)

# In[9]:


def upsert_documents(documents: list[Document], ids: list[str], batch_size: int = 100):
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        vectorstore.add_documents(documents=batch_docs, ids=batch_ids)
        print(f"  upsert 진행: {min(i + batch_size, len(documents))}/{len(documents)}")


def run_pipeline(directory: str = GUIDANCE_DIR):
    paths = sorted(glob.glob(str(Path(directory) / "*.pdf")))
    print(f"'{directory}'에서 PDF {len(paths)}개 발견, 적재 시작\n")

    total_chunks = 0
    for pdf_path in paths:
        documents, ids = build_documents_for_pdf(pdf_path)
        upsert_documents(documents, ids)
        total_chunks += len(documents)
        print()

    print(f"완료: PDF {len(paths)}개 / 총 {total_chunks}개 청크 적재")


# collection이 이미 있었다면 재적재를 건너뜀 (PDF 파싱/표 요약/임베딩 API 재호출 비용 방지)
if not collection_already_existed:
    run_pipeline(GUIDANCE_DIR)
else:
    print(f"'{COLLECTION_NAME}' 컴렉션에 이미 데이터가 있어 적재를 건너뜁니다. (재적재하려면 run_pipeline(GUIDANCE_DIR)를 직접 호출하세요)")


# ## 7. 검색 예시

# In[10]:


def search(query: str, k: int = 5, type_filter: str = None):
    qfilter = None
    if type_filter:
        qfilter = Filter(must=[FieldCondition(key="metadata.type", match=MatchValue(value=type_filter))])

    results = vectorstore.similarity_search_with_score(query, k=k, filter=qfilter)

    for doc, score in results:
        print(f"[score={score:.3f}] doc={doc.metadata.get('doc_name')} page={doc.metadata.get('page')} type={doc.metadata.get('type')}")
        print(doc.page_content[:200])
        print("-" * 40)

    return results


# 사용 예시:
search("군인 해택 휴양시설알려줘")
# search("휴가 관련 표", type_filter="table")
# search("기차 할인 안내 이미지", type_filter="image")



# ## 8. Retriever 생성

# In[11]:


##################################################
# retriever 생성
##################################################

def get_retriever(vectorstore, k: int = 5):
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )
    return retriever


retriever = get_retriever(vectorstore)
print(retriever)


# In[12]:


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
    """LLM 프롬프트({context})용: 문서들을 하나의 문자열로 합침 (doc_name/page도 같이 표기)"""
    parts = []
    for doc in documents:
        meta = doc.metadata
        header = f"[{meta.get('doc_name', '')} p.{meta.get('page', '')}]"
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


# In[13]:


res = chain.invoke("병장의 월급은?")


# In[14]:


res["response"]


# In[15]:


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

# In[16]:


# !uv pip install langchain_google_vertexai


# In[17]:


# 주피터노트북 환경에서 비동기적 처리 위해 
# script(.py) 로 작성할 경우는 필요 없다.

import nest_asyncio
nest_asyncio.apply()


# In[18]:


from ragas.testset import TestsetGenerator


# In[19]:


#
# testset -> Context들(문서들) - [질문 - 정답답변 + (Retriever가 찾은 문서 + LLM 응답: chain에서 생성)]
# 1. Context(문서들)을 추출 - TestsetGenerator -> 질문과 정답 답변 생성

import random

# 데이터셋을 생성할 때 사용할 Context를 추출
client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "guidance_vectordb"

info = client.get_collection(COLLECTION_NAME)
total_docs = info.points_count

results, _ = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=total_docs,
)

# random하게 k(5)개를 sampling
sample_docs:"list[PointStruct]" =random.sample(results, 5) # 리스트에서 랜덤하게 k(5)개를 추출

# PointStruct - payload: page_content, metadata
# page_content만 추출해서 list[str]
docs = [point.payload['page_content'] for point in sample_docs]



# In[20]:


total_docs


# In[21]:


sample_docs


# In[22]:


docs


# In[24]:


# testset 생성
from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
#testsetgenerator 는 gpt-5 이후 버전은 사용할 수 없다. 
## Langchain의 모델과 Embedding 모델 -> ragas에서 사용할 수 있도록 변환(wrapping)
generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4.1"))
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-large"))
generator = TestsetGenerator(
    llm=generator_llm,
    embedding_model=generator_embeddings,
    llm_context="""
- 사람들이 현역병 복지에 대해서 궁금해 할 만한 질문들을 생성한다.
- 데이터셋은 반드시 한국어로 작성한다.
- 데이터셋은 JSON 문법읋 지켜서 작성한다. 특히 구두점은 꼭 지켜야 한다.
- 생성된 내용이나 Document에 JSON문법에 맞지 않는 표현이 있으면 반드시 수정해서 처리한다.
""" 
# 질문/답변을 생성할 때 LLM에게 전달할 system Prompt를 설정
)





# In[25]:


testset = generator.generate_with_chunks(
    docs, testset_size=10, # Context 내용 테스트셋 개수(질문 답변 개수)
)


# In[26]:


testset


# In[27]:


sample1 = testset.samples[0].eval_sample
print("사용자질문:", sample1.user_input)
print("Context:", sample1.reference_contexts)
print("생성된 답변(정답):", sample1.reference)
print("평가대상 RAG의 답변:", sample1.response)
print("평가대상 RAG가 검색한 Context:", sample1.retrieved_contexts)


# In[28]:


# 생성된 Testset을 Pandas DataFrame으로 변환
eval_df = testset.to_pandas()


# In[29]:


eval_df.shape


# In[30]:


eval_df


# In[31]:


row_idx = 0
q = eval_df.loc[row_idx, 'user_input']
resp = chain.invoke(q)


# In[32]:


# resp
resp['response']


# In[33]:


# resp
resp['retrieved_context']


# In[36]:


# 모든 testset의 데이터데 대한 llm 응답과 retriever의 검색 겷과를 추가
response_list = []
retrieved_context_list = []

for user_input in eval_df['user_input']:
    resp = chain.invoke(user_input)
    response_list.append(resp["response"])
    retrieved_context_list.append(resp["retrieved_context"])


# In[35]:


print(len(response_list), len(retrieved_context_list))


# In[37]:


response_list


# In[38]:


retrieved_context_list


# In[39]:


#
# eval_df에 컬럼으로 추가
#
eval_df['response'] = response_list
eval_df['retrieved_contexts'] = retrieved_context_list
eval_df


# In[41]:


# eval_df를 ragas의 평가데이터셋 타입으로 변환
from ragas import EvaluationDataset
eval_dataset = EvaluationDataset.from_pandas(
    eval_df[["user_input", "retrieved_contexts", "response", "reference"]]
)
eval_dataset


# In[42]:


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


# In[43]:


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


# In[44]:


eval_result


# In[45]:


result_df = eval_result.to_pandas()
result_df

