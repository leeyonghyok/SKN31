"""CLI 챗봇 진입점.

단일 고정 user_id 로 동작하며, ``RunnableConfig`` 의 ``configurable`` 에
user_id/thread_id 를 주입하여 그래프를 invoke 한다. 노드는 이 config 에서
user_id 를 읽고, 도구는 ``get_config()`` 로 같은 값을 읽는다.

실행 전 ``python seed_profile.py`` 로 profile/preference 를 먼저 넣어 두면
첫 대화부터 프로필이 시스템 프롬프트에 주입된다.
"""
from __future__ import annotations

from langchain_core.messages import HumanMessage

from config import DEFAULT_THREAD_ID, DEFAULT_USER_ID
from graph import build_graph
from store_setup import create_checkpointer, create_store

# 종료 명령어
_EXIT_COMMANDS = {"!exit", "!quit", "!종료"}


def main() -> None:
    """Store·Checkpointer 생성 → 그래프 컴파일 → CLI 대화 루프 실행."""

    ##################################################### 
    # Store, Checkpointer 생성 ->Graph 생성
    #####################################################
    store = create_store()
    checkpointer = create_checkpointer()
    graph = build_graph(store, checkpointer)


    ##########################
    # RunnableConfig 설정
    ##########################
    user_id = DEFAULT_USER_ID

    user_thread = DEFAULT_THREAD_ID
    # user_id/thread_id 를 RunnableConfig 로 주입
    
    runnable_config = {
        "configurable": {
            "user_id": user_id,
            "thread_id": user_thread,
        }
    }
    print(runnable_config)
    print("=" * 56)
    print(" 장기 기억 챗봇  (종료: !exit / !quit / !종료)")
    print(f" user_id={user_id}, thread_id={user_thread}")
    print("=" * 56)
    
    ##########################
    # Chatbot 실행
    ##########################
    while True:
        try:
            user_input = input("\n나 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            break

        if not user_input:
            continue
        if user_input.lower() in _EXIT_COMMANDS:
            print("종료합니다.")
            break

        # 새 사용자 메시지만 전달한다. 이전 대화는 체크포인터(thread_id)가 복원한다.
        result = graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=runnable_config,
        )
        ai_message = result["messages"][-1]
        print(f"\n비서 > {ai_message.content}")


if __name__ == "__main__":
    main()
