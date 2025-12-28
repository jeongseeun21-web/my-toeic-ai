import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="AI 토익 학습 메이트", layout="wide")

# 1. 데이터 저장소 초기화
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
- **RC 집중 공략:** 현재 RC 360점에서 400점대로 올라가기 위해 Part 5 문법 오답률을 5% 미만으로 낮추어야 합니다.
- **데일리 미션:** 아래 제공되는 AI 퀴즈 5개를 매일 풀고 해설을 정독하세요.
""")

# 메인 화면
st.title("🎯 세은이의 토익 학습 및 성적 관리 대시보드")

tabs = st.tabs(["📈 성적 통계 리포트", "✍️ 성적 입력", "📝 데일리 AI 퀴즈 (5문항)", "📅 시험 일정"])

# Tab 1: 성적 통계
with tabs[0]:
    st.subheader("학습 성장 곡선")
    df = st.session_state.toeic_data
    fig = px.line(df, x='날짜', y='총점', color='구분', markers=True)
    st.plotly_chart(fig, use_container_width=True)
    st.write("### 상세 기록 내역")
    st.dataframe(df.sort_values(by='날짜', ascending=False), use_container_width=True)

# Tab 2: 성적 입력
with tabs[1]:
    st.subheader("새로운 성적 기록하기")
    with st.form("score_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            input_date = st.date_input("시험/응시 날짜", datetime.now())
            category = st.selectbox("시험 구분", ["정기시험", "모의고사"])
        with col2:
            lc_val = st.number_input("LC 점수 (5단위)", min_value=0, max_value=495, step=5)
            rc_val = st.number_input("RC 점수 (5단위)", min_value=0, max_value=495, step=5)
        if st.form_submit_button("성적 저장하기"):
            new_entry = {'날짜': input_date.strftime('%Y-%m-%d'), '구분': category, 'LC': lc_val, 'RC': rc_val, '총점': lc_val + rc_val}
            st.session_state.toeic_data = pd.concat([st.session_state.toeic_data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("기록되었습니다!")
            st.rerun()

# Tab 3: AI 데일리 퀴즈 (5문제 및 개별 해설)
with tabs[2]:
    st.subheader("📖 AI 맞춤형 데일리 퀴즈")
    st.caption("사용자님의 760점 데이터를 분석하여 RC Part 5 빈출 유형 5문제를 생성했습니다.")

    # 문제 데이터 (실제 서비스 시에는 LLM API로 생성되는 영역)
    quiz_bank = [
        {
            "q": "The new software update _______ efficiency in the accounting department.",
            "options": ["improves", "improving", "improved", "improvement"],
            "ans": "improves",
            "explain": "주어(update) 뒤에 동사가 필요한 자리입니다. 문맥상 일반적인 사실을 나타내므로 현재 시제인 improves가 적합합니다."
        },
        {
            "q": "Ms. Geller was _______ surprised by the sudden announcement of the merger.",
            "options": ["complete", "completely", "completeness", "completing"],
            "ans": "completely",
            "explain": "과거분사(surprised)를 수식하는 자리이므로 부사인 completely가 정답입니다."
        },
        {
            "q": "Staff members should contact IT support _______ they encounter technical issues.",
            "options": ["during", "while", "whenever", "unless"],
            "ans": "whenever",
            "explain": "~할 때마다라는 의미의 복합관계부사 whenever가 문맥상 가장 적절합니다."
        },
        {
            "q": "The committee will _______ the final decision until next Monday.",
            "options": ["postpone", "postponing", "postponed", "postpones"],
            "ans": "postpone",
            "explain": "조동사 will 뒤에는 동사 원형이 와야 하므로 postpone이 정답입니다."
        },
        {
            "q": "All employees are expected to behave _______ during the international conference.",
            "options": ["professional", "professionally", "professionalism", "profession"],
            "ans": "professionally",
            "explain": "동사 behave(행동하다)를 수식하는 부사 자리이므로 professionally가 적합합니다."
        }
    ]

    user_answers = []
    for i, item in enumerate(quiz_bank):
        st.markdown(f"**Q{i+1}. {item['q']}**")
        user_ans = st.radio("정답 선택:", item['options'], key=f"q{i}", horizontal=True)
        user_answers.append(user_ans)
        st.write("---")

    if st.button("모든 문제 채점 및 상세 해설 보기"):
        correct_count = 0
        for i, item in enumerate(quiz_bank):
            if user_answers[i] == item['ans']:
                st.success(f"Q{i+1}: 정답입니다! 🎉")
                correct_count += 1
            else:
                st.error(f"Q{i+1}: 오답입니다. (선택: {user_answers[i]} / 정답: {item['ans']})")
            
            with st.expander(f"Q{i+1} 상세 해설 확인"):
                st.write(item['explain'])
        
        st.balloons()
        st.write(f"### 최종 결과: {correct_count} / 5")

# Tab 4: 시험 일정
with tabs[3]:
    st.subheader("📅 2025 토익 정기시험 일정")
    schedule = [
        {"회차": "530회", "시험일": "2025.01.12(일)", "성적발표": "2025.01.22"},
        {"회차": "531회", "시험일": "2025.02.09(일)", "성적발표": "2025.02.19"},
        {"회차": "532회", "시험일": "2025.02.23(일)", "성적발표": "2025.03.05"},
    ]
    st.table(schedule)
