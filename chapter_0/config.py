import os
from dotenv import load_dotenv

# 현재 config.py 파일이 있는 폴더 경로를 찾음
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 해당 폴더 안의 .env 파일을 지정
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 실제투자로 진행할 시 True를 False로 변경
#is_paper_trading = True  # True면 모의투자(paper trading) 모드, False면 실제투자(real trading) 모드로 동작

# 1. 거래 모드 설정 (.env에서 문자열로 읽어오므로 Boolean으로 변환 필요)
# 'true', 'True', 'TRUE' 등을 모두 True로 인식하도록 처리
is_paper_trading_str = os.getenv("IS_PAPER_TRADING", "true")
is_paper_trading = is_paper_trading_str.lower() == "true"

# 2. .env에서 키 값 가져오기
real_app_key = os.getenv("REAL_APP_KEY")            # 실제투자 환경에서 사용할 API 앱 키(발급받은 키 문자열을 따옴표 안에 입력)
real_app_secret = os.getenv("REAL_APP_SECRET")      # 실제투자 환경에서 사용할 API 앱 시크릿(비밀키; 보통 app_secret)

paper_app_key = os.getenv("PAPER_APP_KEY")          # 모의투자 환경에서 사용할 API 앱 키
paper_app_secret = os.getenv("PAPER_APP_SECRET")    # 모의투자 환경에서 사용할 API 앱 시크릿(비밀키)

# 3. URL 정보 (URL은 민감 정보가 아니므로 보통 여기에 두지만, 필요 시 .env로 옮길 수 있음)
real_host_url = "https://api.kiwoom.com"            # 실제투자용 REST API 호스트(HTTP 요청을 보낼 기본 URL)
paper_host_url = "https://mockapi.kiwoom.com"       # 모의투자용 REST API 호스트(모의 서버 기본 URL)

real_socket_url = "wss://api.kiwoom.com:10000"      # 실제투자용 WebSocket 접속 주소(wss=TLS 적용 WebSocket, 포트 10000)
paper_socket_url = "wss://mockapi.kiwoom.com:10000" # 모의투자용 WebSocket 접속 주소

# 4. 모드에 따른 최종 변수 할당 (login.py, main.py가 가져다 쓰는 변수들)
app_key = paper_app_key if is_paper_trading else real_app_key          # 모드에 따라 사용할 app_key를 선택(모의면 paper, 실제면 real)
app_secret = paper_app_secret if is_paper_trading else real_app_secret # 모드에 따라 사용할 app_secret을 선택
host_url = paper_host_url if is_paper_trading else real_host_url       # 모드에 따라 REST API 기본 host_url을 선택
socket_url = paper_socket_url if is_paper_trading else real_socket_url # 모드에 따라 WebSocket 기본 socket_url을 선택

# (디버깅용) 설정이 잘 로드되었는지 확인하고 싶다면 아래 주석을 풀어보세요.
print(f"현재 모드: {'모의투자' if is_paper_trading else '실제투자'}")
print(f"사용 중인 호스트: {host_url}")
print(app_key)