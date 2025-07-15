import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("2cb6a9c6-f5dc-493f-b0a5-8ed161e99a3a.csv")

# 등급 기준 함수 정의
def esg_grade(score):
    if score >= 80:
        return "A (우수)"
    elif score >= 60:
        return "B (보통)"
    elif score >= 40:
        return "C (주의)"
    else:
        return "D (위험)"

# 연도별 등급 계산
df['Environmental_Grade'] = df['ESG_Environmental'].apply(esg_grade)
df['Social_Grade'] = df['ESG_Social'].apply(esg_grade)
df['Governance_Grade'] = df['ESG_Governance'].apply(esg_grade)
df['ESG_Grade'] = df['ESG_Overall'].apply(esg_grade)

# Streamlit 앱 시작
st.title("📊 기업 ESG 분석 대시보드")

st.subheader("🗂️ 기업 기본 정보")
st.markdown(f"""
- **기업명:** {df['CompanyName'][0]}
- **산업군:** {df['Industry'][0]}
- **지역:** {df['Region'][0]}
""")

st.subheader("📈 연도별 ESG 점수 및 등급")
st.dataframe(df[['Year', 'ESG_Environmental', 'Environmental_Grade',
                 'ESG_Social', 'Social_Grade',
                 'ESG_Governance', 'Governance_Grade',
                 'ESG_Overall', 'ESG_Grade']])

st.subheader("🌍 ESG 영역별 추이")
st.line_chart(df.set_index('Year')[['ESG_Environmental', 'ESG_Social', 'ESG_Governance', 'ESG_Overall']])

st.subheader("⚠️ ESG 개선이 필요한 영역")

latest = df.iloc[-1]  # 최신 연도 데이터
recommendations = []

if latest['ESG_Environmental'] < 60:
    recommendations.append("- **환경 (E)**: 탄소 배출 감축, 에너지 절약 설비 도입 필요")
if latest['ESG_Social'] < 60:
    recommendations.append("- **사회 (S)**: 직원 복지 개선, 지역사회 프로그램 확대 필요")
if latest['ESG_Governance'] < 60:
    recommendations.append("- **지배구조 (G)**: 이사회 투명성 확보, 내부통제 강화 필요")

if recommendations:
    st.error("📌 현재 ESG 점수가 낮은 영역이 존재합니다.")
    for r in recommendations:
        st.markdown(r)
else:
    st.success("모든 ESG 항목이 양호한 수준입니다.")

st.subheader("💡 환경 성과 지표 (탄소, 에너지, 물)")
st.line_chart(df.set_index('Year')[['CarbonEmissions', 'EnergyConsumption', 'WaterUsage']])
