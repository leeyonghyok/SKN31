"""SQLite 기반 장기 기억(Store), 단기 기억(Checkpointer) 생성 모듈.

- 장기 기억: `SqliteStore`. memories 의 의미 기반 검색을 위해 임베딩 `index` 를 설정한다.
- 단기 기억: `SqliteSaver`(체크포인터). 스레드별 대화 상태(단기 메모리)를 저장한다.

두 저장소 모두 영속성을 위해 `:memory:` 가 아닌 파일 경로를 사용한다.
seed 스크립트와 챗봇이 **동일한 DB 파일**을 공유하도록 경로는 `config` 에서 가져온다.
"""
import sqlite3

from langchain_openai import OpenAIEmbeddings
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.sqlite import SqliteStore

from config import (
    DATABASE_DIR,
    EMBEDDING_DIMS,
    EMBEDDING_MODEL,
    LONG_TERM_DB_PATH,
    SHORT_TERM_DB_PATH,
)


def _connect(db_path: str, *, autocommit: bool = False) -> sqlite3.Connection:
    """DB 디렉터리를 보장한 뒤 SQLite 연결을 생성한다.

    - `check_same_thread=False`: CLI 루프 등에서 프로세스 수명 동안 동일 연결을
      재사용하므로 스레드 제약을 완화한다.
    - `autocommit=True` 이면 `isolation_level=None`(autocommit 모드)로 연다.
      SqliteStore 는 `BEGIN`/`COMMIT` 트랜잭션을 **직접** 관리하므로, 파이썬
      sqlite3 의 암묵적 트랜잭션 관리와 충돌하지 않도록 autocommit 모드가 필요하다.
      (라이브러리의 `SqliteStore.from_conn_string` 도 동일하게 설정한다.)
    """
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    # isolation_level="" 는 sqlite3 기본값(암묵적 트랜잭션), None 은 autocommit.
    isolation_level = None if autocommit else ""
    return sqlite3.connect(
        db_path, check_same_thread=False, isolation_level=isolation_level
    )


def create_store() -> SqliteStore:
    """장기 기억용 `SqliteStore` 를 생성·초기화하여 반환한다.

    `index` 설정 덕분에 `put` 시 value 의 `content` 필드가 임베딩되어,
    `store.search(namespace, query=...)` 로 의미 기반 검색이 가능해진다.
    (`content` 필드가 없는 값은 자동으로 임베딩 대상에서 제외된다.)
    """
    conn = _connect(LONG_TERM_DB_PATH, autocommit=True)
    store = SqliteStore(
        conn,
        index={
            "embed": OpenAIEmbeddings(model=EMBEDDING_MODEL),
            "dims": EMBEDDING_DIMS,
            "fields": ["content"],  # 이 필드만 임베딩(검색) 대상
        },
    )
    store.setup()  # 테이블/인덱스 생성 (멱등)
    return store


def create_checkpointer() -> SqliteSaver:
    """단기 기억용 `SqliteSaver`(체크포인터)를 생성·초기화하여 반환한다."""
    conn = _connect(SHORT_TERM_DB_PATH)
    saver = SqliteSaver(conn)
    saver.setup()  # 체크포인트 테이블 생성 (멱등)
    return saver
