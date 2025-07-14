import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="지속 가능한 경영 대시보드", layout="wide")

st.title("🌿 지속 가능한 경영 대시보드 (ESG + 환경지표)")

# 💾 가상 지속가능경영 데이터 생성
data = {
    "연도": [2019, 2020, 2021, 2022, 2023, 2024],
    "환경점수(E)": [58, 65, 70, 76, 83, 89],
    "사회점수(S)": [62, 66, 72, 78, 84, 88],
    "지배구조(G)": [70, 73, 75, 77, 80, 82],
    "탄소배출량(톤)": [1800, 1650, 1500, 1300, 1100, 900],
    "재생에너지사용률(%)": [8, 12, 18, 25, 35, 45]
}
df = pd.DataFrame(data)

# 📊 ESG 점수 선그래프
st.subheader("📈 연도별 ESG 점수 추이")
fig_esg = px.line(
    df,
    x="연도",
    y=["환경점수(E)", "사회점수(S)", "지배구조(G)"],
    markers=True,
    title="ESG 각 항목 점수 변화"
)
st.plotly_chart(fig_esg, use_container_width=True)

# ♻️ 탄소 배출량 막대그래프
st.subheader("🌍 탄소 배출량 변화")
fig_carbon = px.bar(
    df,
    x="연도",
    y="탄소배출량(톤)",
    text_auto=True,
    title="연도별 탄소 배출량 감소 추이"
)
st.plotly_chart(fig_carbon, use_container_width=True)

# 🔋 재생에너지 사용률 에어리어 차트
st.subheader("🔋 재생에너지 사용률 증가")
fig_renew = px.area(
    df,
    x="연도",
    y="재생에너지사용률(%)",
    title="연도별 재생에너지 사용률"
)
st.plotly_chart(fig_renew, use_container_width=True)

# 📋 데이터 테이블 출력
st.subheader("📋 ESG 및 환경 데이터 테이블")
st.dataframe(df)
