"""LangGraph 그래프 정의 모듈.

흐름::

    START → load_context → agent ⇄ tools → END

- `load_context`: 그래프 진입 시 profile·preference 를 Store 에서 읽어
  시스템 프롬프트를 구성한다(항상 주입). 노드는 `config` 인자에서 user_id 를 읽는다.
- `agent`: 시스템 프롬프트 + 대화 메시지로 도구를 bind 한 LLM 을 호출한다.
- `tools`: LLM 이 호출한 `save_memory`/`search_memory`/`save_preference` 를 실행한다.
- `agent` 가 더 이상 도구를 호출하지 않으면 종료(END).
"""
from __future__ import annotations

import json
from typing import Optional

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.config import get_store
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.store.base import BaseStore

from config import (
    LLM_MODEL,
    PREFERENCE_KEY,
    PROFILE_KEY,
    preferences_namespace,
    profile_namespace,
)

from tools import TOOLS


_llm_with_tools = ChatOpenAI(model=LLM_MODEL).bind_tools(TOOLS)


class State(MessagesState):
    """그래프 상태.

    `MessagesState` 의 `messages` 에 더해, load_context 가 채우는
    `system_prompt` 필드를 둔다(매 invoke 마다 새로 계산되어 덮어써진다).
    """

    system_prompt: str


def build_system_prompt(
    profile: Optional[dict], preference: Optional[dict]
) -> str:
    """장기기억에 저장된 profile, preference 정보를 이용해 시스템 프롬프트 작성한다.

    Args:
        profile: profile namespace 의 basic_info value (없으면 None).
        preference: preferences namespace 의 response_style value (없으면 None).
    """
    
    parts = ["당신은 사용자의 장기 기억을 활용해 도와주는 한국어 개인 비서입니다."]

    if profile:
        parts.append(
            "\n## 사용자 프로필\n"
            + json.dumps(profile, ensure_ascii=False, indent=2)
        )
    if preference:
        parts.append(
            "\n## 사용자 선호(답변 방식)\n"
            + json.dumps(preference, ensure_ascii=False, indent=2)
        )

    parts.append(
        "\n## 지침\n"
        "- 위 '사용자 선호'의 언어/톤/포맷에 맞춰 답변하라.\n"
        "- 사용자의 질문이 과거 정보와 관련될 수 있으면 먼저 `search_memory` 로 검색해 활용하라.\n"
        "- 대화 중 장기적으로 기억할 만한 사용자 정보가 나오면 `save_memory` 를 호출해 저장하라.\n"
        "- 사용자가 답변 방식 선호를 표현하면 `save_preference` 로 갱신하라."
    )
    return "\n".join(parts)


def load_context(state: State, config: RunnableConfig) -> dict:
    """진입 노드: 
    profile, preference 를 읽어 시스템 프롬프트를 만든다.

    노드는 `config` 파라미터에서 user_id 를 읽어 namespace 를 구성하고,
    Store 는 `get_store()` 로 접근한다.

    주의) user_id는 원래 현재 대화중인 사용자의 id를 사용해야 한다.
    """
    user_id = config["configurable"]["user_id"]
    store = get_store()

    profile_item = store.get(profile_namespace(user_id), PROFILE_KEY)
    pref_item = store.get(preferences_namespace(user_id), PREFERENCE_KEY)
    profile = profile_item.value if profile_item else None
    preference = pref_item.value if pref_item else None

    return {"system_prompt": build_system_prompt(profile, preference)}


def agent(state: State) -> dict:
    """LLM 호출 노드: 
    매 호출마다 시스템 프롬프트를 메시지 앞에 붙인다.

    시스템 프롬프트는 state["messages"] 에 누적하지 않고 호출 시에만 앞에 붙여 체크포인터에 중복 저장되지 않게 된다.
    """
    messages = [SystemMessage(content=state.get("system_prompt", ""))] + state["messages"]
    response = _llm_with_tools.invoke(messages)
    return {"messages": [response]}


def build_graph(store: BaseStore, checkpointer: BaseCheckpointSaver):
    """노드/엣지를 구성하고 store·checkpointer 와 함께 compile 하여 반환한다.

    Args:
        store: 장기 기억 Store (노드/도구가 get_store() 로 접근).
        checkpointer: 단기 기억 체크포인터 (스레드별 대화 상태 저장).
    """
    builder = StateGraph(State)
    builder.add_node("load_context", load_context)
    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "load_context")
    builder.add_edge("load_context", "agent")
    
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    return builder.compile(store=store, checkpointer=checkpointer)
