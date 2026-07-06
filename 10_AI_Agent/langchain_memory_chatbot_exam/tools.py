"""LLM 에 bind 할 Tool 정의 모듈.

- ``search_memory``: memories namespace 에서 질문과 의미적으로 유사한 기억을 검색(읽기).
- ``save_memory``: 장기적으로 기억할 사실을 새 UUID key 로 누적 저장(쓰기).
- ``save_preference``: 사용자 답변 선호(톤/포맷/언어)를 고정 key 로 갱신(덮어쓰기).

Tool 함수는 노드와 달리 ``config`` 를 인자로 받지 못한다. 따라서
``langgraph.config.get_config()`` 로 invoke 시 주입된 user_id 를 읽고,
``langgraph.config.get_store()`` 로 컴파일 시 연결된 Store 에 접근한다.
"""
from __future__ import annotations

import uuid
from typing import Optional

from langchain_core.tools import tool
from langgraph.config import get_config, get_store

from config import PREFERENCE_KEY, memories_namespace, preferences_namespace


def _current_user_id() -> str:
    """invoke 시 RunnableConfig 의 configurable 에 주입된 user_id 를 읽는다."""
    return get_config()["configurable"]["user_id"]


@tool
def search_memory(query: str) -> str:
    """사용자에 대해 과거에 저장해 둔 장기 기억을 의미 기반으로 검색한다.

    사용자의 질문이 과거 정보(취미, 가족, 일정, 선호 등)와 관련 있어 보이면
    이 도구로 관련 기억을 먼저 조회한 뒤 그 내용을 활용해 답변하라.

    Args:
        query: 검색할 내용(자연어). 예) "사용자의 반려동물", "다음 달 일정".

    Returns:
        검색된 기억 목록 문자열. 관련 기억이 없으면 안내 문구.
    """
    user_id = _current_user_id()
    store = get_store()
    items = store.search(memories_namespace(user_id), query=query, limit=5)
    if not items:
        return "저장된 관련 기억이 없습니다."
    return "\n".join(f"- {item.value.get('content', '')}" for item in items)


@tool
def save_memory(content: str) -> str:
    """대화 중 알게 된, 장기적으로 기억할 만한 사용자 관련 사실을 저장한다.
    사용자가 경험한 것, 좋아하는 것, 싫어하는 것, 관심있는 것, 알고 싶은 것 등 이후 대화에서 사용자에 대해 참고할 수있는 것들을 저장한다.

    예) "강아지를 키운다", "다음 달 이사 예정", "축구를 좋아한다", "휴대폰은 삼성 브랜드를 좋아한다.".
    호출할 때마다 새로운 key(UUID)로 누적 저장되며 기존 기억을 덮어쓰지 않는다.

    Args:
        content: 기억할 내용을 한 문장으로 요약한 짧은 텍스트.

    Returns:
        저장 완료 메시지.
    """
    user_id = _current_user_id()
    store = get_store()
    # 동적 key 누적 저장. content 필드는 index 설정에 따라 자동 임베딩된다.
    store.put(memories_namespace(user_id), str(uuid.uuid4()), {"content": content})
    return f"기억을 저장했습니다: {content}"


@tool
def save_preference(
    tone: Optional[str] = None,
    response_format: Optional[str] = None,
    language: Optional[str] = None,
) -> str:
    """사용자의 답변 선호(톤/포맷/언어)를 갱신한다(고정 key 덮어쓰기).

    사용자가 "앞으로 ~하게 답해줘", "JSON 으로 답해줘" 처럼 답변 방식 선호를
    표현하면 호출하라. 전달한 항목만 갱신하고 나머지는 기존 값을 유지한다.

    Args:
        tone: 답변 톤. 예) "clear", "friendly", "concise".
        response_format: 출력 포맷. 예) "markdown", "json", "text".
        language: 선호 언어. 예) "Korean", "English".

    Returns:
        갱신된 선호 내용 메시지.
    """
    user_id = _current_user_id()
    store = get_store()
    namespace = preferences_namespace(user_id)

    # 기존 선호를 읽어 부분 갱신(merge)한다.
    existing = store.get(namespace, PREFERENCE_KEY)
    current = dict(existing.value) if existing else {}
    if tone is not None:
        current["tone"] = tone
    if response_format is not None:
        current["format"] = response_format
    if language is not None:
        current["language"] = language

    # 고정 key 덮어쓰기. content 필드가 없으므로 index=False 로 임베딩을 생략한다.
    store.put(namespace, PREFERENCE_KEY, current, index=False)
    return f"선호 정보를 갱신했습니다: {current}"


# 그래프에서 LLM 에 bind 하고 ToolNode 에 등록할 Tool 목록
TOOLS = [search_memory, save_memory, save_preference]
