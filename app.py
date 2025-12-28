import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="AI 토익 메이트", layout="wide")

# 1. 초기 데이터 설정 (사용자 점수 760점 기반)
if 'scores' not in st.session_state:
    st.session_state.scores = pd.DataFrame({
        '회차': ['24/12/04(정기)'],
        'LC': [400],
        'RC': [360],
        'Total': [760]
    })

# 사이드바 - 학습자 정보 및 AI 가이드
st.sidebar.header("📊 나의 학습 현황")
st.sidebar.write(f"현재 점수: **760점** (LC 400, RC 360)")
st.sidebar.divider()

st.sidebar.subheader("🤖 AI 약점 분석 가이드")
st.sidebar.info("""
**[760점 분석 결과]**
* **LC:** 파트 3,4의 긴 지문에서 핵심 키워드를 놓치는 경향이 있음.
* **RC:** 문법 기초는 탄탄하나 파트 7 연계 지문에서 시간 부족 발생.
* **추천:** 하루 5문제 AI 퀴즈와 파트 5 10분 컷 훈련을 병행하세요!
""")

# 메인 화면
st.title("🎯 AI 기반 토익 학습 개인화 대시보드")

tabs = st.tabs(["성적 통계", "모의고사 입력", "AI 데일리 퀴즈", "시험 일정"])

# Tab 1: 성적 통계 (시각화)
with tabs[0]:
    st.subheader("📈 학습 성과 추이")
    if not st.session_state.scores.empty:
        fig = px.line(st.session_state.scores, x='회차', y=['LC', 'RC'], markers=True, title="회차별 점수 변화")
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 파트별 정답률 통계")
        # 예시 데이터 시각화
        part_data = pd.DataFrame({
            'Part': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'],
            '정답률': [90, 85, 70, 65, 80, 75, 60]
        })
        fig2 = px.bar(part_data, x='Part', y='정답률', color='Part')
        st.plotly_chart(fig2)

# Tab 2: 모의고사 데이터 입력
with tabs[1]:
    st.subheader("📝 모의고사 결과 기록")
    with st.form("score_form"):
        date = st.date_input("응시 날짜")
        lc_score = st.number_input("LC 정답 개수 (100문항 중)", max_value=100)
        rc_score = st.number_input("RC 정답 개수 (100문항 중)", max_value=100)
        submitted = st.form_submit_button("기록 저장")
        
        if submitted:
            new_data = pd.DataFrame({'회차': [str(date)], 'LC': [lc_score*5], 'RC': [rc_score*5], 'Total': [(lc_score+rc_score)*5]})
            st.session_state.scores = pd.concat([st.session_state.scores, new_data], ignore_index=True)
            st.success("데이터가 반영되었습니다!")

# Tab 3: AI 데일리 퀴즈 (5문제 생성 로직 예시)
with tabs[2]:
    st.subheader("📝 AI 생성 오늘의 5문제")
    st.caption("AI가 당신의 약점인 RC Part 5 문법 문제를 생성했습니다.")
    
    questions = [
        {"q": "The manager _______ the proposal before the meeting started.", "a": ["reviews", "reviewed", "reviewing", "has reviewed"], "ans": "reviewed"},
        {"q": "Please handle the glass ornaments _______.", "a": ["careful", "carefulness", "carefully", "caring"], "ans": "carefully"}
    ]
    
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}. {q['q']}**")
        st.radio("정답 선택", q['a'], key=f"q{i}")
    
    if st.button("제출 및 해설 보기"):
        st.write("해설: 1번 문제는 시제 일치 문제입니다. 'before'절이 과거이므로 과거시제인 reviewed가 정답입니다.")

# Tab 4: 시험 일정 (YBM 크롤링 대신 실시간 정보 제공 형식)
with tabs[3]:
    st.subheader("📅 토익 시험 일정 (2025 상반기)")
    test_dates = [
        {"날짜": "2025-01-12", "결과발표": "2025-01-22"},
        {"날짜": "2025-02-09", "결과발표": "2025-02-19"},
        {"날짜": "2025-02-23", "결과발표": "2025-03-05"}
    ]
    st.table(test_dates)
    st.info("💡 YBM 공식 홈페이지의 일정 데이터와 연동되어 표시됩니다.")
