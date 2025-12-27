import streamlit as st

def show():
    st.header("💬 AI 보증보험 상담사")
    st.caption(f"Secure Connection Active | Key: {st.session_state.api_key[:5]}********")
    
    # 여기에 지난번에 만든 챗봇 코드를 넣으시면 됩니다.
    st.chat_message("assistant").write("안녕하세요! 차량의 어떤 부분이 궁금하신가요?")