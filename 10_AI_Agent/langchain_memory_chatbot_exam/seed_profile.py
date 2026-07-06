"""profile,preference 사전 입력 스크립트.
Agent 실행 전에 미리 정보의 일부를 저장한다.
"""
from __future__ import annotations

from config import (
    DEFAULT_USER_ID,
    PREFERENCE_KEY,
    PROFILE_KEY,
    preferences_namespace,
    profile_namespace,
)
from store_setup import create_store

# 사전 입력할 사용자 목록 (user_id, profile, preference).
# 첫 번째(DEFAULT_USER_ID)가 챗봇이 실제 사용하는 사용자이다.
USERS = [
    {
        "user_id": DEFAULT_USER_ID,  # "demo_user"
        "profile": {
            "name": <<본인 정보>>,
            "job":  <<본인 정보>>,
            "language": "Korean",
            "timezone": "Asia/Seoul",
        },
        "preference": {"language": "Korean", "tone": "clear", "format": "markdown"},
    },
    {
        "user_id": "minji",
        "profile": {
            "name": "김민지",
            "job": "백엔드 개발자",
            "language": "Korean",
            "timezone": "Asia/Seoul",
        },
        "preference": {"language": "Korean", "tone": "friendly", "format": "text"},
    },
    {
        "user_id": "james",
        "profile": {
            "name": "James Park",
            "job": "데이터 분석가",
            "language": "English",
            "timezone": "America/New_York",
        },
        "preference": {"language": "English", "tone": "concise", "format": "json"},
    },
]


def seed() -> None:
    """USERS 의 각 사용자에 대해 profile·preference 를 put 한다(고정 key, 덮어쓰기)."""
    store = create_store()

    for user in USERS:
        user_id = user["user_id"]
        # 고정 key 덮어쓰기. content 필드가 없으므로 index=False 로 임베딩을 생략한다.
        store.put(
            profile_namespace(user_id), PROFILE_KEY, user["profile"], index=False
        )
        store.put(
            preferences_namespace(user_id),
            PREFERENCE_KEY,
            user["preference"],
            index=False,
        )
        print(f"  - 시드: {user_id} ({user['profile']['name']})")

    print(f"프로필 시드 완료 (사용자 {len(USERS)}명)")


if __name__ == "__main__":
    seed()
