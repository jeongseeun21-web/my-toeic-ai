import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="AI 토익 학습 메이트", layout="wide")

# 1. 데이터 저장소 초기화 (정기 시험 및 모의고사 통합 관리)
if 'toeic_data' not in st.session_state:
    st.session_state.toeic_data = pd.DataFrame([
        {'날짜': '2024-12-04', '구분': '정기시험', 'LC': 400, 'RC': 360, '총점': 760}
    ])

# 사이드바 - AI 분석 가이드
st.sidebar.header("📊 나의 AI 분석 결과")
current_total = st.session_state.toeic_data.iloc[-1]['총점']
st.sidebar.metric("현재 점수", f"{current_total}점")

st.sidebar.info(f"""
**[AI 처방전]**
현재 {current_total}점 상태입니다. 
- **LC(400):** 고득점권 진입을 위해 파트 3,4 오답 노트를 AI로 분석하세요.
- **RC(360):** 파트 5 시간을 15분 이내로 단축하는 것이 800점 돌파의 핵심입니다.
""")

# 메인 화면
st.title("🎯 세은이의 토익 학습 및 성적 관리 대시보드")

tabs = st.tabs(["📈 성적 통계 리포트", "✍️ 성적 입력", "📝 데일리 AI 퀴즈", "📅 시험 일정"])

# Tab 1: 성적 통계 및 시각화
with tabs[0]:
    st.subheader("학습 성장 곡선")
    df = st.session_state.toeic_data
    if not df.empty:
        # 점수 추이 그래프
        fig = px.line(df, x='날짜', y='총점', color='구분', markers=True, title="회차별 총점 변화")
        st.plotly_chart(fig, use_container_width=True)
        
        # 상세 데이터 표
        st.write("### 상세 기록 내역")
        st.dataframe(df.sort_values(by='날짜', ascending=False), use_container_width=True)

# Tab 2: 성적 입력 (정기 시험 / 모의고사 구분)
with tabs[1]:
    st.subheader("새로운 성적 기록하기")
    st.write("정기 시험 성적이나 모의고사 결과를 입력해 주세요.")
    
    with st.form("score_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            input_date = st.date_input("시험/응시 날짜", datetime.now())
            category = st.selectbox("시험 구분", ["정기시험", "모의고사"])
        with col2:
            lc_val = st.number_input("LC 점수 (5단위)", min_value=0, max_value=495, step=5)
            rc_val = st.number_input("RC 점수 (5단위)", min_value=0, max_value=495, step=5)
        
        submit_btn = st.form_submit_button("성적 저장하기")
        
        if submit_btn:
            new_entry = {
                '날짜': input_date.strftime('%Y-%m-%d'),
                '구분': category,
                'LC': lc_val,
                'RC': rc_val,
                '총점': lc_val + rc_val
            }
            st.session_state.toeic_data = pd.concat([st.session_state.toeic_data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"{category} 기록이 성공적으로 저장되었습니다!")
            st.rerun()

# Tab 3: AI 데일리 퀴즈
with tabs[2]:
    st.subheader("📖 AI가 생성한 오늘의 연습 문제")
    st.info("당신의 RC 취약점인 '접속사와 전치사' 구분 문제입니다.")
    
    q_data = [
        {"q": "_______ the heavy rain, the outdoor concert will proceed as scheduled.", "options": ["Despite", "Although", "Nevertheless", "Even though"], "ans": "Despite"},
        {"q": "The shipment was delayed _______ a mechanical failure in the delivery truck.", "options": ["because", "due to", "since", "as"], "ans": "due to"}
    ]
    
    for i, item in enumerate(q_data):
        st.write(f"**Q{i+1}. {item['q']}**")
        st.radio("정답 선택", item['options'], key=f"quiz_{i}")
    
    if st.button("채점하기"):
        st.success("해설: 1번은 명사구(heavy rain) 앞이므로 전치사 Despite가 정답입니다. 2번은 명사구 앞이므로 due to가 적절합니다.")

# Tab 4: 시험 일정
with tabs[3]:
    st.subheader("📅 2025 토익 정기시험 일정")
    schedule = [
        {"회차": "530회", "시험일": "2025.01.12(일)", "성적발표": "2025.01.22"},
        {"회차": "531회", "시험일": "2025.02.09(일)", "성적발표": "2025.02.19"},
        {"회차": "532회", "시험일": "2025.02.23(일)", "성적발표": "2025.03.05"},
    ]
    st.table(schedule)
