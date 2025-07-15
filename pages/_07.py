import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="ESG 분석 대시보드", layout="wide")

# CSV 파일명 (같은 폴더에 esg_data.csv로 저장)
CSV_FILE = "esg_data.csv"

# 데이터 불러오기
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    st.error(f"⚠️ 데이터 파일 '{CSV_FILE}' 이(가) 존재하지 않습니다.\n같은 폴더에 CSV 파일을 올려주세요.")
    st.stop()

# ESG 등급 함수 정의
def get_grade(score):
    if score >= 80:
        return "A (우수)"
    elif score >= 60:
        return "B (보통)"
    elif score >= 40:
        return "C (주의)"
    else:
        return "D (위험)"

# 등급 컬럼 추가
df["Environmental_Grade"] = df["ESG_Environmental"].apply(get_grade)
df["Social_Grade"] = df["ESG_Social"].apply(get_grade)
df["Governance_Grade"] = df["ESG_Governance"].apply(get_grade)
df["ESG_Grade"] = df["ESG_Overall"].apply(get_grade)

# 연도 필터링 슬라이더
years = df["Year"].unique()
min_year, max_year = int(years.min()), int(years.max())
selected_years = st.slider("🔍 분석할 연도 범위 선택", min_year, max_year, (min_year, max_year))
filtered_df = df[df["Year"].between(*selected_years)]

# 최근 연도 데이터
latest = filtered_df.iloc[-1]

# 대시보드 타이틀
st.title("📊 ESG 분석 대시보드")
st.markdown("한 기업의 연도별 ESG 추세 및 개선 방향을 시각적으로 분석합니다.")

# 사이드바 기업 정보
st.sidebar.header("📌 기업 정보")
st.sidebar.markdown(f"""
- **기업명**: `{df['CompanyName'].iloc[0]}`
- **산업군**: `{df['Industry'].iloc[0]}`
- **지역**: `{df['Region'].iloc[0]}`
""")

# ESG 점수 테이블
st.subheader("📈 ESG 점수 및 등급")
st.dataframe(filtered_df[[
    "Year", "ESG_Environmental", "Environmental_Grade",
    "ESG_Social", "Social_Grade",
    "ESG_Governance", "Governance_Grade",
    "ESG_Overall", "ESG_Grade"
]])

# ESG 점수 영역별 추이 그래프
st.subheader("📉 ESG 점수 변화 추이")
col1, col2 = st.columns(2)
with col1:
    st.line_chart(filtered_df.set_index("Year")[["ESG_Environmental"]])
    st.line_chart(filtered_df.set_index("Year")[["ESG_Social"]])
with col2:
    st.line_chart(filtered_df.set_index("Year")[["ESG_Governance"]])
    st.line_chart(filtered_df.set_index("Year")[["ESG_Overall"]])

# 환경 성과 상세 시각화
st.subheader("🌿 환경 성과 지표 (탄소, 물, 에너지)")

eco1, eco2, eco3 = st.columns(3)
with eco1:
    st.metric("🌍 탄소배출량", f"{latest['CarbonEmissions']} tCO₂")
    st.line_chart(filtered_df.set_index("Year")[["CarbonEmissions"]])
with eco2:
    st.metric("💧 물 사용량", f"{latest['WaterUsage']} tons")
    st.line_chart(filtered_df.set_index("Year")[["WaterUsage"]])
with eco3:
    st.metric("⚡ 에너지 소비량", f"{latest['EnergyConsumption']} MWh")
    st.line_chart(filtered_df.set_index("Year")[["EnergyConsumption"]])

# 개선 과제 제안
st.subheader("🛠️ 향후 ESG 개선 과제 제안")
improvements = []
if latest["ESG_Environmental"] < 60:
    improvements.append("✔ **환경(E)**: 탄소 감축, 친환경 설비 도입 필요")
if latest["ESG_Social"] < 60:
    improvements.append("✔ **사회(S)**: 직원 만족도 제고, 지역사회 활동 강화 필요")
if latest["ESG_Governance"] < 60:
    improvements.append("✔ **지배구조(G)**: 투명경영, 이사회 다양성 확대 필요")

if improvements:
    st.warning("현재 ESG 점수가 낮은 영역이 있습니다.")
    for item in improvements:
        st.markdown(item)
else:
    st.success("모든 ESG 항목이 양호한 수준입니다. 🎉")

# 사이드바 최신 등급 요약
st.sidebar.subheader("📊 최신 등급 요약")
st.sidebar.markdown(f"""
- **환경 (E)**: `{get_grade(latest['ESG_Environmental'])}`
- **사회 (S)**: `{get_grade(latest['ESG_Social'])}`
- **지배구조 (G)**: `{get_grade(latest['ESG_Governance'])}`
- **종합 ESG**: `{get_grade(latest['ESG_Overall'])}`
""")

# 데이터 다운로드 기능
st.download_button("📥 ESG 데이터 다운로드", data=filtered_df.to_csv(index=False), file_name="filtered_esg_data.csv", mime="text/csv")
