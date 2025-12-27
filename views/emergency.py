import streamlit as st
import pandas as pd
from datetime import datetime
from github import Github # PyGithub 라이브러리
import io

# [데이터 엔지니어링] GitHub를 DB로 사용하는 파이프라인 함수
def save_to_github(new_data_dict):
    # 1. Secrets에서 인증 정보 가져오기
    token = st.secrets["my_github"]["token"]
    username = st.secrets["my_github"]["username"]
    repo_name = st.secrets["my_github"]["repo_name"]
    branch = st.secrets["my_github"]["branch"]
    
    # 2. GitHub 접속
    g = Github(token)
    repo = g.get_user(username).get_repo(repo_name)
    file_path = "emergency_reports.csv" # 저장할 파일명
    
    try:
        # 3. 기존 파일이 있는지 확인하고 내용 가져오기
        contents = repo.get_contents(file_path, ref=branch)
        df_old = pd.read_csv(io.StringIO(contents.decoded_content.decode("utf-8")))
        
        # 4. 새 데이터 추가 (Append)
        df_new = pd.DataFrame([new_data_dict])
        df_updated = pd.concat([df_old, df_new], ignore_index=True)
        
        # 5. GitHub에 수정사항 반영 (Commit & Push)
        csv_data = df_updated.to_csv(index=False, encoding="utf-8-sig")
        repo.update_file(contents.path, "🚨 응급 접수 데이터 추가", csv_data, contents.sha, branch=branch)
        return "success"
        
    except Exception as e:
        # 파일이 없을 경우 (최초 생성)
        if "404" in str(e):
            try:
                df_new = pd.DataFrame([new_data_dict])
                csv_data = df_new.to_csv(index=False, encoding="utf-8-sig")
                repo.create_file(file_path, "🎉 최초 응급 데이터 생성", csv_data, branch=branch)
                return "created"
            except Exception as create_error:
                return f"Error creating file: {create_error}"
        else:
            return f"Error: {e}"

def show():
    st.header("🚨 긴급 출동 접수 (GitHub DB 연동)")
    st.error("현재 사고 발생 또는 주행 불가 상태이신가요? 아래 정보를 입력해주시면 본사 서버(GitHub)로 즉시 전송됩니다.")

    with st.form("emergency_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            car_number = st.text_input("1. 차량 번호", placeholder="예: 12가 3456")
            owner_name = st.text_input("3. 차주 성함")
            reporter_contact = st.text_input("5. 접수자 연락처", placeholder="010-0000-0000")
        
        with col2:
            car_model = st.text_input("2. 차종", placeholder="예: 그랜저, 쏘렌토")
            reporter_name = st.text_input("4. 접수자 성함 (선택)")
            
        situation = st.text_area("6. 현재 상황 설명", height=100)
        
        submit = st.form_submit_button("🚀 긴급 접수하기", type="primary")

    if submit:
        if not car_number or not reporter_contact:
            st.toast("⚠️ 차량 번호와 연락처는 필수입니다!")
        else:
            with st.spinner("본사 서버로 데이터를 전송 중입니다..."):
                # 저장할 데이터 딕셔너리 생성
                new_data = {
                    "접수시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "차량번호": car_number,
                    "차종": car_model,
                    "차주명": owner_name,
                    "접수자명": reporter_name if reporter_name else owner_name,
                    "연락처": reporter_contact,
                    "상황": situation
                }
                
                # GitHub 저장 함수 호출
                result = save_to_github(new_data)
                
                if result in ["success", "created"]:
                    st.balloons()
                    st.success("✅ 접수가 완료되었습니다! 담당자가 곧 연락드립니다.")
                    st.info(f"데이터가 GitHub Repository의 '{st.secrets['my_github']['repo_name']}'에 안전하게 저장되었습니다.")
                else:
                    st.error(f"전송 실패: {result}")