# tools.py

from langchain_community.document_loaders import WikipediaLoader
from pydantic import BaseModel, Field
from langchain_core.runnables import chain
import json 
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Runnable 구현 -> tool 변환
@chain
def wikipedia_search(inputs: dict) -> str:
    """
    사용자의 쿼리를 검색어로 위키백과사전(wikipedia)를 검색하고 그 결과 중 k개의 문서내용을 반환한다. 
    Args:
        inputs(dict): key- query, max_result. query(str) 검색할 키워드, max_result(int) 검색할 결과수
    
    Returns:
        str - 검색한 결과들을 json 형식의 문자열로 반환.
              형식: {"result":[{검색된 문서정보들}, {검색된 문서정보들}]}
    """
    print("-------", inputs)
    query = inputs['query']
    max_result = inputs.get("max_result", 3)

    loader = WikipediaLoader(
        query=query, #검색어
        load_max_docs=max_result, # 검색할 문서 최대 개수
        lang="ko" # 검색할 wikipedia 나라.
    )
    cnt = 0
    result_list = []
    while True:
        cnt += 1
        print(f"{cnt}번째 시도")
        try:
            docs = loader.load() # list[Document]
            for doc in docs:
                result_list.append(
                    {
                        "content":doc.page_content, # 조회내용
                        "title": doc.metadata.get("title"),
                        "url": doc.metadata.get("source")
                    }
                )
            break # 정상적으로 종료 되면 break(while문 종료)
        except Exception as e: 
            # loader.load()에서 검색한 결과를 parsing할 때 문제가 발생. 발생여부가 불확실
            if cnt == 4: # 4번째 시도에서도 Exception 발생
                break # load 종료
            continue # 4번째가 아니면 다시 시도

    if result_list:
        result = {"result":result_list}
    else:
        result = {"result":"검색된 문서가 없습니다."}

    # List/Dictionary => str(JSON형식)
    return json.dumps(result, ensure_ascii=False)

class WikiSearchParameter(BaseModel):
    query: str = Field(..., description="한국어 Wikipedia에서 조회할 검색 keyword")
    max_result: int|None = Field(default=3, description="검색할 문서의 최대 개수. 생략하면 기본값으로 3을 사용")

wikipedia_search_tool = wikipedia_search.as_tool(
    name="search_wikipedia_korea", # 툴이름
    description="""이 도구는 한국 위키백과사전에서 정보를 검색할 때 사용한다.
사용자의 질문과 관련된 내용을 한국 위키백과사전 사이트에서 지정한 개수의 문서만큼 검색해서 반환한다.
일반적인 지식이나 백과사전식 정보가 필요할 때 사용한다.""",
    args_schema=WikiSearchParameter
)

######################
# Search Menu Tool
######################
COLLECTION_NAME = "restaurant_menu"
VECTOR_SIZE = 1536  # OpenAIEmbeddings의 벡터 크기
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
client = QdrantClient(host="localhost", port=6333)

vectorstore = QdrantVectorStore(
    client=client, # QdrantClient
    embedding=embeddings, # Embedding Model
    collection_name=COLLECTION_NAME # 연결할 Collection 지정.
)
menu_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}  # 검색할 결과 개수
)


retriever = menu_retriever.configurable_fields(
    search_type=ConfigurableField(
        id="search_type"
    ),
    search_kwargs=ConfigurableField(
        id="search_kwargs"
    ),
)

class SearchMenuToolParameter(BaseModel):
    query:str = Field(..., description="의미기반 검색으로 메뉴를 찾을 query")
    top_k:int = Field(default=3, description="Vector DB에서 조회할 문서 개수. 기본값 3")

@tool(args_schema=SearchMenuToolParameter)
def search_menu_tool(query:str, top_k:int|None=3) -> str:
    """이 도구는 VectorStore에 저장된 restaurant menu를 검색하는 tool입니다. 음식 메뉴에 대한 정보가 필요할 때 사용합니다."""
    result_list = [] # 결과 문서들을 담을 list
    config = {
        "configurable": {
            "search_kwargs": {
                "k": top_k
            }
        }
    }
    docs = retriever.invoke(query, config=config)   
    for doc in docs:
        result_list.append(
            {
                "content":doc.page_content,
                "title":doc.metadata['menu_name'],
                "url": doc.metadata['source']
            }
        )
    if result_list:
        result = {"result": result_list}
    else:
        result = {"result": "검색된 메뉴가 없습니다."}
    
    return json.dumps(result, ensure_ascii=False) # JSON 문자열로 반환.