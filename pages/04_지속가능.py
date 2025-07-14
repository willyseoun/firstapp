import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="지속 가능한 경영 ESG 대시보드", layout="wide")     

st.title("🌿 지속 가능한 경영 ESG 대시보드")

# 💾 데이터 생성
data = {
    "연도": [2019, 2020, 2021, 2022, 2023, 2024],
    "환경점수(E)": [58, 65, 70, 76, 83, 89],
    "사회점수(S)": [62, 66, 72, 78, 84, 88],
    "지배구조(G)": [70, 73, 75, 77, 80, 82],
    "탄소배출량(톤)": [1800, 1650, 1500, 1300, 1100, 900],
    "재생에너지사용률(%)": [8, 12, 18, 25, 35, 45]
}
df = pd.DataFrame(data)

# 🎚 연도 범위 선택
year_range = st.slider("🔎 분석 연도 범위", int(df["연도"].min()), int(df["연도"].max()), (2020, 2024))
filtered_df = df[df["연도"].between(year_range[0], year_range[1])]

# 📊 ESG 추이 그래프
st.subheader("📈 ESG 항목별 점수 추이")
fig_esg = px.line(filtered_df, x="연도", y=["환경점수(E)", "사회점수(S)", "지배구조(G)"], markers=True)
st.plotly_chart(fig_esg, use_container_width=True)

# ♻️ 탄소 배출량
st.subheader("🌍 탄소 배출량 감소 추이")
fig_carbon = px.bar(filtered_df, x="연도", y="탄소배출량(톤)", text_auto=True)
st.plotly_chart(fig_carbon, use_container_width=True)

# 🔋 재생에너지 사용률
st.subheader("🔋 재생에너지 사용률 추이")
fig_renew = px.area(filtered_df, x="연도", y="재생에너지사용률(%)")
st.plotly_chart(fig_renew, use_container_width=True)

# 📌 요약 KPI 카드
st.subheader("📌 ESG 핵심 지표")
col1, col2, col3 = st.columns(3)

with col1:
    avg_esg = filtered_df[["환경점수(E)", "사회점수(S)", "지배구조(G)"]].mean().mean()
    st.metric("ESG 평균 점수", f"{avg_esg:.1f}")

with col2:
    carbon_reduction = (1 - filtered_df["탄소배출량(톤)"].iloc[-1] / filtered_df["탄소배출량(톤)"].iloc[0]) * 100
    st.metric("탄소 감축률", f"{carbon_reduction:.1f}%")

with col3:
    renewable = filtered_df["재생에너지사용률(%)"].iloc[-1]
    st.metric("재생에너지 사용률", f"{renewable}%")

# 🏅 ESG 등급 분류 함수
def classify_esg(score):
    if score >= 85:
        return "A등급"
    elif score >= 75:
        return "B등급"
    elif score >= 65:
        return "C등급"
    else:
        return "D등급"

esg_grade = classify_esg(avg_esg)
st.success(f"📊 ESG 등급: **{esg_grade}** (평균 점수 기준)")

# 📋 원본 데이터 확인 및 다운로드
with st.expander("📂 원본 데이터 보기 및 다운로드"):
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("CSV 다운로드", csv, "ESG_지표_데이터.csv", "text/csv")

# 🎯 탄소중립 목표 상태
st.info(f"""
🌱 **탄소중립 2030 목표**: 탄소배출 500톤 이하  
📉 현재 탄소배출량: **{filtered_df['탄소배출량(톤)'].iloc[-1]}톤**  
📏 감축 필요량: **{max(0, filtered_df['탄소배출량(톤)'].iloc[-1] - 500)}톤**
""")

