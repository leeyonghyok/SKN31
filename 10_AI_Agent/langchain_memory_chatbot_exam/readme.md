- seed_profile.py

# 실행순서
- `python seed_profile.py` 
    - 장기메모리저장소(store)에 기본 정보 저장
- `python main.py`
    - 챗봇 실행


# 구성
- config.py: 설정정보를 저장한 파일
- store_setup.py: store, checkpointer 연결 설정.(Store, Checkpointer)
- seed_profile.py: 장기기억(Store)에 기본 개인정보 저장.
- tools.py - Tool들을 정의한 모듈 (메모리 저장, 조회 툴)
- graph.py - LangGraph를 이용해서 Graph(Agent)를 구성.
- main.py - 실행 스크립트