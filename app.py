import streamlit as st
import time
from views import home, bot, emergency, common, insurance

# 1. 페이지 기본 설정 (반드시 코드 최상단에 위치)
st.set_page_config(
    page_title="CarGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed" # 사이드바를 기본적으로 숨겨서 앱처럼 보이게 함
)

# 2. 스타일링 & CSS 주입 (트렌디한 디자인을 위한 핵심)
def local_css():
    st.markdown("""
    <style>
        /* 메인화면 위쪽 여백 제거 (DW 매뉴얼 수정부분. padding-top이 너무 작아 글씨 상단이 잘려보이는 현상이 발생하여 1rem에서 2rem으로 수정) */
        .block-container { padding-top: 2rem; padding-bottom: 5rem; }
        
        /* 버튼 디자인 커스텀 (그라데이션 효과) */
        div.stButton > button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            color: white;
            border: none;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            transform: scale(1.02);
            color: #ffcc00;
        }
        
        /* API 입력창 디자인 */
        .api-box {
            border: 2px solid #4b6cb7;
            padding: 20px;
            border-radius: 15px;
            background-color: #f0f2f6;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# 3. 세션 상태 초기화 (네비게이션 & 데이터 관리)

if "page" not in st.session_state:
    st.session_state.page = "home" # 기본 페이지
if "api_key" not in st.session_state:
    st.session_state.api_key = None

# PM님이 제안해주신 개발자 모드 추가, 로컬 환경에선 secrets.toml에 저장된 API_KEY를 로드한다.
if "OPENAI_API_KEY" in st.secrets:
    if st.session_state.api_key is None: # 이미 로드된 상태가 아닐 때만
        st.session_state.api_key = st.secrets["OPENAI_API_KEY"]
        st.toast("✅ 개발자 모드: 비밀키가 자동으로 로드되었습니다.")

# --- [네비게이션 함수] ---
def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun() # 화면을 즉시 새로고침하여 페이지 이동 효과

# --- [메인 로직] ---

# 1단계: API Key 보안 체크 (Gatekeeper Pattern)
# 키가 없으면 어떤 페이지도 보여주지 않고 입력창만 띄웁니다.
if not st.session_state.api_key:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='api-box'><h3>🔑 보안 접속</h3><p>서비스 이용을 위해 인증키가 필요합니다.</p></div>", unsafe_allow_html=True)
        st.write("")
        
        # 콜백 함수로 안전하게 저장
        def set_key():
            st.session_state.api_key = st.session_state.temp_key
            
        st.text_input(
            "OpenAI API Key", 
            type="password", 
            key="temp_key", 
            on_change=set_key,
            placeholder="sk-..."
        )
        st.warning("⚠️ 입력하신 키는 브라우저 종료 시 자동 파기됩니다.")
    
    st.stop() # 키 입력 전까지 아래 코드 실행 중단

# 2단계: 페이지 라우팅 (Router)
# 키가 있다면 현재 선택된 페이지(page 변수)에 따라 다른 함수를 실행합니다.

# 상단 네비게이션 바 (선택사항: 모든 페이지에 공통 노출)
with st.sidebar:
    st.title("Navigation")
    if st.button("🏠 홈으로"):
        navigate_to("home")
    if st.button("🤖 AI 상담사"):
        navigate_to("bot")
    st.divider()
    if st.button("🔒 로그아웃 (키 삭제)"):
        st.session_state.api_key = None
        st.rerun()

# 실제 화면 로딩
if st.session_state.page == "home":
    home.show(navigate_to)
    
elif st.session_state.page == "bot":
    bot.show()

elif st.session_state.page == "emergency":
    emergency.show()

elif st.session_state.page == "common":
    common.show()

elif st.session_state.page == "insurance":
    insurance.show()