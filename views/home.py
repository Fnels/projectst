import streamlit as st

# [UI 유틸리티 함수] 수직 여백을 픽셀 단위로 조정
def v_spacer(height, sb=False):
    target = st.sidebar if sb else st
    target.markdown(f'<div style="height: {height}px;"></div>', unsafe_allow_html=True)

def show(nav_callback):
    # 상단 여백 및 헤더
    st.title("🚗 현대해상 중고차 성능보증 센터")
    st.markdown("### 👨‍🔧 무엇을 도와드릴까요?")
    st.caption("고객님의 상황에 맞는 메뉴를 선택해주세요.")
    st.write("---") # 구분선으로 깔끔하게 정리

    # [디자인 전략]
    # Wide 모드에서 버튼이 너무 길어지는 것을 방지하기 위해 
    # 좌우에 여백(Spacer)을 두어 중앙에 컨텐츠를 집중시킵니다.
    # 비율: [1 (여백), 2 (본문), 1 (여백)]  !! DW 매뉴얼 수정 > 사람이 보기 편한 간격으로 조정했습니다. 비율 : [5, 3, 9]
    col_spacer1, col_content, col_spacer2 = st.columns([5, 3, 9])

    with col_spacer1: # !! DW 매뉴얼 수정 > 글씨는 왼쪽 column에 배치하고 버튼은 중앙 column에 배치
        # 1. 응급 접수 (가장 위급하므로 최상단 배치 + 붉은색 뉘앙스 강조 추천하지만 일단 기본 통일)
        st.markdown("##### 🚨 **응급 접수**")
        st.write("주행 중 시동꺼짐 등 긴급 상황이신가요?")
        
        st.write("") # 버튼 사이 수직 여백(Whitespace) 추가
        st.write("") 

        # 2. 일반 접수
        st.markdown("##### 📝 **일반 접수**")
        st.write("성능·상태점검 책임보험 접수가 필요하신가요?")

        st.write("") 
        st.write("") 

        # 3. 챗봇 상담
        st.markdown("##### 🤖 **AI 챗봇 상담**")
        st.write("상황에 맞는 보험 상담이 필요하신가요?")

        st.write("") 
        st.write("") 

        # 4. 보험 안내
        st.markdown("##### 📖 **보험 안내**")
        st.write("책임보험 제도가 궁금하신가요?")
    
    with col_content: # !! DW 매뉴얼 수정 > 글씨는 왼쪽 column에 배치하고 버튼은 중앙 column에 배치, 간격은 v_spacer로 조정
        # 1. 응급 접수 (가장 위급하므로 최상단 배치 + 붉은색 뉘앙스 강조 추천하지만 일단 기본 통일)
        v_spacer(10)
        if st.button("응급 상황 접수하기 ->", key="btn_emergency"):
            nav_callback("emergency")

        v_spacer(56)
        # 2. 일반 접수
        if st.button("일반 접수하기 ->", key="btn_common"):
            nav_callback("common")

        v_spacer(57)
        # 3. 챗봇 상담
        if st.button("AI 상담 시작하기 ->", key="btn_bot"):
            nav_callback("bot")

        v_spacer(55)
        # 4. 보험 안내
        if st.button("보험 안내 보기 ->", key="btn_insurance"):
            nav_callback("insurance")

    # 하단 저작권 표시 (선택사항 - 전문성 강조)
    st.write("---")
    st.markdown("<div style='text-align: center; color: grey; font-size: 0.8em;'>© 2025 LeeYongSu_Project. All rights reserved.</div>", unsafe_allow_html=True)