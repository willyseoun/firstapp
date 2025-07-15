import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ESG 시각화 대시보드", layout="wide")

# 파일명
CSV_FILE = "esg_data.csv"

# CSV 불러오기
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    st.error(f"❌ '{CSV_FILE}' 파일을 찾을 수 없습니다. 같은 폴더에 올려주세요.")
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

# 등급 추가
df["Environmental_Grade"] = df["ESG_Environmental"].apply(get_grade)
df["Social_Grade"] = df["ESG_Social"].apply(get_grade)
df["Governance_Grade"] = df["ESG_Governance"].apply(get_grade)
df["ESG_Grade"] = df["ESG_Overall"].apply(get_grade)

# 최신 연도 정보
latest = df.iloc[-1]

# 헤더
st.title("📊 ESG 분석 시각화 대시보드")
st.markdown("기업의 연도별 **환경(E), 사회(S), 지배구조(G)** 데이터를 보기 쉽게 시각화했습니다.")

# 📌 기본 기업 정보
with st.sidebar:
    st.header("🏢 기업 정보")
    st.markdown(f"""
    - **기업명**: `{df['CompanyName'].iloc[0]}`
    - **산업군**: `{df['Industry'].iloc[0]}`
    - **지역**: `{df['Region'].iloc[0]}`
    """)
    st.subheader("📊 최신 등급 요약")
    st.markdown(f"""
    - 환경 (E): `{get_grade(latest['ESG_Environmental'])}`
    - 사회 (S): `{get_grade(latest['ESG_Social'])}`
    - 지배구조 (G): `{get_grade(latest['ESG_Governance'])}`
    - 종합 ESG: `{get_grade(latest['ESG_Overall'])}`
    """)

# 📈 ESG 점수 테이블
st.subheader("🗂️ ESG 점수 및 등급")
st.dataframe(df[[
    "Year", "ESG_Environmental", "Environmental_Grade",
    "ESG_Social", "Social_Grade",
    "ESG_Governance", "Governance_Grade",
    "ESG_Overall", "ESG_Grade"
]])

# 🌍 시각화 섹션
st.markdown("---")
st.subheader("📈 ESG 분야별 점수 추이 (Plotly)")

col1, col2 = st.columns(2)

with col1:
    fig_e = px.line(df, x="Year", y="ESG_Environmental", markers=True, title="환경 (Environmental) 점수",
                    line_shape="spline", color_discrete_sequence=["green"])
    fig_e.update_traces(line=dict(width=4))
    st.plotly_chart(fig_e, use_container_width=True)

with col2:
    fig_s = px.line(df, x="Year", y="ESG_Social", markers=True, title="사회 (Social) 점수",
                    line_shape="spline", color_discrete_sequence=["orange"])
    fig_s.update_traces(line=dict(width=4))
    st.plotly_chart(fig_s, use_container_width=True)

fig_g = px.line(df, x="Year", y="ESG_Governance", markers=True, title="지배구조 (Governance) 점수",
                line_shape="spline", color_discrete_sequence=["blue"])
fig_g.update_traces(line=dict(width=4))
st.plotly_chart(fig_g, use_container_width=True)

# 🌿 환경 성과 그래프
st.markdown("---")
st.subheader("🌱 환경 성과 지표 (탄소, 에너지, 물 소비량)")

fig_env = px.line(df, x="Year",
                  y=["CarbonEmissions", "EnergyConsumption", "WaterUsage"],
                  title="환경 부문 실적 지표 변화",
                  line_shape="spline",
                  markers=True,
                  labels={
                      "value": "사용량/배출량",
                      "variable": "환경 지표"
                  },
                  color_discrete_map={
                      "CarbonEmissions": "red",
                      "EnergyConsumption": "purple",
                      "WaterUsage": "skyblue"
                  })
fig_env.update_traces(line=dict(width=3))
st.plotly_chart(fig_env, use_container_width=True)

# 개선 과제
st.markdown("---")
st.subheader("🔧 ESG 개선이 필요한 영역")

recommend = []
if latest["ESG_Environmental"] < 60:
    recommend.append("✅ **환경(E)**: 탄소 감축 및 친환경 기술 도입 필요")
if latest["ESG_Social"] < 60:
    recommend.append("✅ **사회(S)**: 직원 만족도 향상 및 사회 기여 확대")
if latest["ESG_Governance"] < 60:
    recommend.append("✅ **지배구조(G)**: 이사회 투명성 및 다양성 확보 필요")

if recommend:
    st.warning("다음 영역에서 ESG 점수가 낮습니다:")
    for r in recommend:
        st.markdown(r)
else:
    st.success("🎉 모든 ESG 항목이 양호한 수준입니다.")
