from __future__ import annotations

import os
from pathlib import Path

# =========================================================
# 1) .env 로딩: "config.py(현재 파일) -> 부모 폴더"를 프로젝트 루트로 가정
#    즉, chapter_0/config.py 기준 parents[1] == KIWOOM 루트
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # KIWOOM/
ENV_PATH = PROJECT_ROOT / ".env"

try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv(dotenv_path=ENV_PATH)
except ImportError:
    # python-dotenv가 없으면 OS 환경변수만 읽음
    pass


# =========================================================
# 2) env 문자열을 bool로 엄밀하게 파싱
# =========================================================
def env_bool(name: str, default: bool = False) -> bool:
    """
    환경변수는 문자열이므로 다음 값을 bool로 해석한다.

    True  : "1", "true", "t", "yes", "y", "on"
    False : "0", "false", "f", "no", "n", "off"

    그 외 값이면 ValueError를 발생시켜 설정 오류를 즉시 드러낸다.
    """
    raw = os.getenv(name)
    if raw is None:
        return default

    raw = raw.strip().lower()
    true_set = {"1", "true", "t", "yes", "y", "on"}
    false_set = {"0", "false", "f", "no", "n", "off"}

    if raw in true_set:
        return True
    if raw in false_set:
        return False

    raise ValueError(
        f"환경변수 {name} 값이 bool로 해석 불가: {raw!r} "
        f"(허용: {sorted(true_set | false_set)})"
    )


# =========================================================
# 3) .env와 1:1로 대응되는 설정 상수들
# =========================================================
IS_PAPER_TRADING: bool = env_bool("IS_PAPER_TRADING", default=True)

REAL_APP_KEY: str = os.getenv("REAL_APP_KEY", "")
REAL_APP_SECRET: str = os.getenv("REAL_APP_SECRET", "")

PAPER_APP_KEY: str = os.getenv("PAPER_APP_KEY", "")
PAPER_APP_SECRET: str = os.getenv("PAPER_APP_SECRET", "")

REAL_HOST_URL: str = "https://api.kiwoom.com"
PAPER_HOST_URL: str = "https://mockapi.kiwoom.com"

REAL_SOCKET_URL: str = "wss://api.kiwoom.com:10000"
PAPER_SOCKET_URL: str = "wss://mockapi.kiwoom.com:10000"


# =========================================================
# 4) 현재 모드에 따라 실제로 사용할 값 선택
# =========================================================
APP_KEY: str = PAPER_APP_KEY if IS_PAPER_TRADING else REAL_APP_KEY
APP_SECRET: str = PAPER_APP_SECRET if IS_PAPER_TRADING else REAL_APP_SECRET

HOST_URL: str = PAPER_HOST_URL if IS_PAPER_TRADING else REAL_HOST_URL
SOCKET_URL: str = PAPER_SOCKET_URL if IS_PAPER_TRADING else REAL_SOCKET_URL


# =========================================================
# 5) 필수값 검증: 현재 모드에서 필요한 키가 비어있으면 즉시 에러
# =========================================================
def _require_non_empty(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(
            f"필수 설정 누락: {name} 가 비어있습니다.\n"
            f"- .env 경로: {ENV_PATH}\n"
            f"- 또는 OS 환경변수로 {name}를 설정하세요."
        )

_require_non_empty("APP_KEY", APP_KEY)
_require_non_empty("APP_SECRET", APP_SECRET)


# =========================================================
# 6) (선택) 기존 코드 호환용 별칭
#    네가 이미 login.py 등에서 app_key 같은 소문자 변수를 쓰고 있다면 이거 두면 편함
# =========================================================
is_paper_trading = IS_PAPER_TRADING
app_key = APP_KEY
app_secret = APP_SECRET
host_url = HOST_URL
socket_url = SOCKET_URL
