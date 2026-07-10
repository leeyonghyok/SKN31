"""프로젝트 전역 설정 상수 모듈."""


import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# --- 모델 설정 ---
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-5.4-mini")
# 임베딩: memories 의미 기반 검색(Store index)에 사용.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMS = 1536

# --- 경로 설정 ---
BASE_DIR = Path(__file__).resolve().parent # 프로젝트 root 경로
# Path(__file__).resolve() config.py 파일의 경로


## 장단기 메모리 Database 파일 경로
DATABASE_DIR = BASE_DIR / "database"
LONG_TERM_DB_PATH = str(DATABASE_DIR / "long_term.db")
SHORT_TERM_DB_PATH = str(DATABASE_DIR / "short_term.db")

# --- 사용자/스레드 식별자 ---
# 실제 사용자별로 인증하는 것을 구현하지 않으므로 단일 고정 user_id 를 사용한다.
DEFAULT_USER_ID = "demo_user"
DEFAULT_THREAD_ID = "1"

# --- 장기 메모리에 저장할 profile, preferences KEY ---
PROFILE_KEY = "basic_info"        
PREFERENCE_KEY = "response_style" 

# --- 장기 메모리의 namespace 반환 함수 ---
def profile_namespace(user_id: str) -> tuple[str, ...]:
    """사용자 프로필 namespace 를 반환한다: ("users", user_id, "profile")."""
    return ("users", user_id, "profile")


def preferences_namespace(user_id: str) -> tuple[str, ...]:
    """사용자 선호 namespace 를 반환한다: ("users", user_id, "preferences")."""
    return ("users", user_id, "preferences")


def memories_namespace(user_id: str) -> tuple[str, ...]:
    """사용자 누적 기억 namespace 를 반환한다: ("users", user_id, "memories")."""
    return ("users", user_id, "memories")
