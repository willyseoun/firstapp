import streamlit as st
import pandas as pd

st.set_page_config(page_title="ESG 분석 대시보드", layout="wide")

# 파일명 정확하게 기입
CSV_FILE = "esg_data.csv"  # ← 이 이름으로 파일 저장하세요 (원래 파일명에서 바꾸는 걸 추천)

# CSV 불러오기
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    st.error(f"⚠️ 데이터 파일 '{CSV_FILE}' 이(가) 존재하지 않습니다.\n같은 폴더에 CSV 파일을 올려주세요.")
    st.stop()

# ESG 등급 함수 정의 (필요시 유지해도 무방)
def get_grade(score):
    if score >= 80:
        return "A (우수)"
    elif score >= 60:
        return "B (보통)"
    elif score >= 40:
        return "C (주의)"
    else:
        return "D (위험)"

# 최근 데이터 기준
latest = df.iloc[-1]

# 대시보드 구성
st.title("📊 ESG 분석 대시보드")
st.markdown("한 기업의 연도별 ESG 추세 및 개선 방향을 분석합니다.")

# 기본 정보
st.sidebar.header("📌 기업 정보")
st.sidebar.markdown(f"""
- **기업명**: `{df['CompanyName'].iloc[0]}`
- **산업군**: `{df['Industry'].iloc[0]}`
- **지역**: `{df['Region'].iloc[0]}`
""")

# 환경 지표 시각화
st.subheader("🌿 환경 성과 지표 (탄소, 물, 에너지)")
st.line_chart(df.set_index("Year")[["CarbonEmissions", "WaterUsage", "EnergyConsumption"]])

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

# ESG 요약 출력
st.sidebar.subheader("📊 최신 등급 요약")
st.sidebar.markdown(f"""
- **환경 (E)**: `{get_grade(latest['ESG_Environmental'])}`
- **사회 (S)**: `{get_grade(latest['ESG_Social'])}`
- **지배구조 (G)**: `{get_grade(latest['ESG_Governance'])}`
- **종합 ESG**: `{get_grade(latest['ESG_Overall'])}`
""")
