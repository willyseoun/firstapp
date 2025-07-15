import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ESG 시각화 대시보드", layout="wide")

# CSV 불러오기
CSV_FILE = "esg_data.csv"
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    st.error(f"❌ '{CSV_FILE}' 파일이 존재하지 않습니다. 같은 폴더에 올려주세요.")
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

# 🌐 타이틀
st.title("📊 ESG 시각화 대시보드")
st.markdown("한 기업의 ESG(Environment, Social, Governance) 점수와 실적을 직관적으로 확인할 수 있는 대시보드입니다.")

# 📋 사이드바: 기업 정보 + 등급 요약
with st.sidebar:
    st.header("🏢 기업 정보")
    st.markdown(f"""
    - **기업명:** `{df['CompanyName'].iloc[0]}`
    - **산업군:** `{df['Industry'].iloc[0]}`
    - **지역:** `{df['Region'].iloc[0]}`
    """)
    st.subheader("📌 최신 ESG 등급")
    st.success(f"✅ 환경 (E): {get_grade(latest['ESG_Environmental'])}")
    st.success(f"✅ 사회 (S): {get_grade(latest['ESG_Social'])}")
    st.success(f"✅ 지배구조 (G): {get_grade(latest['ESG_Governance'])}")
    st.success(f"✅ 종합 ESG: {get_grade(latest['ESG_Overall'])}")

# 📊 ESG 점수 테이블
st.markdown("---")
st.subheader("🗂 ESG 점수 및 등급 테이블")
st.dataframe(df[[
    "Year", "ESG_Environmental", "Environmental_Grade",
    "ESG_Social", "Social_Grade",
    "ESG_Governance", "Governance_Grade",
    "ESG_Overall", "ESG_Grade"
]])

# 📈 ESG 점수 그래프 카드별로 나누기
st.markdown("---")
st.subheader("📈 ESG 영역별 추이")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🌱 환경 (Environmental)")
    fig_e = px.line(df, x="Year", y="ESG_Environmental", title="환경 점수",
                    markers=True, line_shape="spline",
                    color_discrete_sequence=["green"])
    fig_e.update_traces(line=dict(width=4))
    fig_e.update_layout(height=350)
    st.plotly_chart(fig_e, use_container_width=True)

with col2:
    st.markdown("#### 🧑‍🤝‍🧑 사회 (Social)")
    fig_s = px.line(df, x="Year", y="ESG_Social", title="사회 점수",
                    markers=True, line_shape="spline",
                    color_discrete_sequence=["orange"])
    fig_s.update_traces(line=dict(width=4))
    fig_s.update_layout(height=350)
    st.plotly_chart(fig_s, use_container_width=True)

with col3:
    st.markdown("#### 🏛 지배구조 (Governance)")
    fig_g = px.line(df, x="Year", y="ESG_Governance", title="지배구조 점수",
                    markers=True, line_shape="spline",
                    color_discrete_sequence=["blue"])
    fig_g.update_traces(line=dict(width=4))
    fig_g.update_layout(height=350)
    st.plotly_chart(fig_g, use_container_width=True)

# 🌿 환경 실적 그래프
st.markdown("---")
st.subheader("🌍 환경 성과 지표 (탄소, 에너지, 물 사용량)")

fig_env = px.line(df, x="Year",
                  y=["CarbonEmissions", "EnergyConsumption", "WaterUsage"],
                  title="환경 실적 변화 (배출량 및 소비량)",
                  line_shape="spline", markers=True,
                  labels={"value": "사용량 또는 배출량", "variable": "지표"},
                  color_discrete_map={
                      "CarbonEmissions": "red",
                      "EnergyConsumption": "purple",
                      "WaterUsage": "skyblue"
                  })
fig_env.update_traces(line=dict(width=3))
fig_env.update_layout(height=500)
st.plotly_chart(fig_env, use_container_width=True)

# 🔧 개선 과제 제안
st.markdown("---")
st.subheader("🛠 ESG 개선 과제 제안")

recommend = []
if latest["ESG_Environmental"] < 60:
    recommend.append("🟢 **환경(E)**: 탄소 저감 및 친환경 설비 도입 필요")
if latest["ESG_Social"] < 60:
    recommend.append("🟠 **사회(S)**: 직원 복지 강화 및 지역사회 참여 확대")
if latest["ESG_Governance"] < 60:
    recommend.append("🔵 **지배구조(G)**: 투명한 이사회 운영 및 다양성 확보 필요")

if recommend:
    st.warning("⚠ 다음 영역의 ESG 점수가 낮습니다. 개선이 필요합니다:")
    for r in recommend:
        st.markdown(f"- {r}")
else:
    st.success("🎉 ESG 모든 항목이 양호한 수준입니다.")
