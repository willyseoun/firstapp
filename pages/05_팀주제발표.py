import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ESG 시각화 대시보드", layout="wide")

# CSV 파일 불러오기
CSV_FILE = "esg_data.csv"
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    st.error(f"❌ '{CSV_FILE}' 파일이 없습니다. 같은 폴더에 올려주세요.")
    st.stop()

# 등급 계산 함수
def get_grade(score):
    if score >= 80:
        return "A (우수)"
    elif score >= 60:
        return "B (보통)"
    elif score >= 40:
        return "C (주의)"
    else:
        return "D (위험)"

# 등급 열 추가
df["Environmental_Grade"] = df["ESG_Environmental"].apply(get_grade)
df["Social_Grade"] = df["ESG_Social"].apply(get_grade)
df["Governance_Grade"] = df["ESG_Governance"].apply(get_grade)
df["ESG_Grade"] = df["ESG_Overall"].apply(get_grade)
latest = df.iloc[-1]

# 페이지 제목
st.title("📊 ESG 시각화 대시보드")

# ===== 1. ESG 영역별 통합 그래프 =====
st.markdown("---")
st.subheader("📈 ESG 점수 추이 (환경, 사회, 지배구조)")

df_esg_melt = df.melt(id_vars="Year", value_vars=[
    "ESG_Environmental", "ESG_Social", "ESG_Governance"
], var_name="ESG 영역", value_name="점수")

# 컬럼명 보기 쉽게 변환
df_esg_melt["ESG 영역"] = df_esg_melt["ESG 영역"].replace({
    "ESG_Environmental": "환경 (E)",
    "ESG_Social": "사회 (S)",
    "ESG_Governance": "지배구조 (G)"
})

fig_esg = px.line(df_esg_melt, x="Year", y="점수", color="ESG 영역",
                  title="ESG 영역별 점수 변화",
                  markers=True, line_shape="spline",
                  color_discrete_map={
                      "환경 (E)": "green",
                      "사회 (S)": "orange",
                      "지배구조 (G)": "blue"
                  })
fig_esg.update_traces(line=dict(width=4))
fig_esg.update_layout(legend_title_text="ESG 항목", height=500)
st.plotly_chart(fig_esg, use_container_width=True)

# ===== 2. 에너지 소비 현황 =====
st.markdown("---")
st.subheader("⚡ 에너지 소비 및 환경 자원 사용 현황")

col1, col2, col3 = st.columns(3)

# (1) 탄소 배출
with col1:
    st.markdown("### 🔴 탄소 배출량 (Carbon Emissions)")
    fig_c = px.line(df, x="Year", y="CarbonEmissions", title="연도별 탄소 배출량",
                    markers=True, line_shape="spline", color_discrete_sequence=["red"])
    fig_c.update_traces(line=dict(width=4))
    fig_c.update_layout(height=350)
    st.plotly_chart(fig_c, use_container_width=True)

# (2) 에너지 소비량
with col2:
    st.markdown("### 🟣 에너지 소비량 (Energy Consumption)")
    fig_e = px.line(df, x="Year", y="EnergyConsumption", title="연도별 에너지 소비량",
                    markers=True, line_shape="spline", color_discrete_sequence=["purple"])
    fig_e.update_traces(line=dict(width=4))
    fig_e.update_layout(height=350)
    st.plotly_chart(fig_e, use_container_width=True)

# (3) 물 사용량
with col3:
    st.markdown("### 🔵 물 사용량 (Water Usage)")
    fig_w = px.line(df, x="Year", y="WaterUsage", title="연도별 물 사용량",
                    markers=True, line_shape="spline", color_discrete_sequence=["skyblue"])
    fig_w.update_traces(line=dict(width=4))
    fig_w.update_layout(height=350)
    st.plotly_chart(fig_w, use_container_width=True)
