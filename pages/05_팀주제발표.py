import streamlit as st
import pandas as pd

st.set_page_config(page_title="ESG 분석 대시보드", layout="wide")

CSV_FILE = "esg_data.csv" # ← 여기에 CSV 파일명 정확히 저장

# CSV 파일 불러오기
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

# 등급 계산
df["Environmental_Grade"] = df["ESG_Environmental"].apply(get_grade)
df["Social_Grade"] = df["ESG_Social"].apply(get_grade)
df["Governance_Grade"] = df["ESG_Governance"].apply(get_grade)
df["ESG_Grade"] = df["ESG_Overall"].apply(get_grade)

# 최근 연도 기준 값 추출
latest = df.iloc[-1]

# 대시보드 타이틀
st.title("📊 ESG 분석 대시보드")
st.markdown("ESG 점수와 환경 지표를 **수평 직선**으로 고정하여 표시한 대시보드입니다.")

# 기업 정보 출력
st.sidebar.header("📌 기업 정보")
st.sidebar.markdown(f"""
- **기업명**: `{df['CompanyName'].iloc[0]}`
- **산업군**: `{df['Industry'].iloc[0]}`
- **지역**: `{df['Region'].iloc[0]}`
""")

# ESG 점수 및 등급 테이블
st.subheader("📈 ESG 점수 및 등급")
st.dataframe(df[[
"Year", "ESG_Environmental", "Environmental_Grade",
"ESG_Social", "Social_Grade",
"ESG_Governance", "Governance_Grade",
"ESG_Overall", "ESG_Grade"
]])

# 🔹 한 직선으로 고정한 ESG 점수 시각화
st.subheader("📉 ESG 점수 변화 추이 (직선 고정)")
fixed_esg = pd.DataFrame({
"Year": df["Year"],
"ESG_Environmental": [latest["ESG_Environmental"]] * len(df),
"ESG_Social": [latest["ESG_Social"]] * len(df),
"ESG_Governance": [latest["ESG_Governance"]] * len(df),
"ESG_Overall": [latest["ESG_Overall"]] * len(df),
}).set_index("Year")
st.line_chart(fixed_esg)

# 🔹 한 직선으로 고정한 환경 성과 지표 시각화
st.subheader("🌿 환경 성과 지표 (직선 고정)")
fixed_env = pd.DataFrame({
"Year": df["Year"],
"CarbonEmissions": [latest["CarbonEmissions"]] * len(df),
"WaterUsage": [latest["WaterUsage"]] * len(df),
"EnergyConsumption": [latest["EnergyConsumption"]] * len(df),
}).set_index("Year")
st.line_chart(fixed_env)

# ESG 개선 과제 제안
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

# 최신 등급 요약
st.sidebar.subheader("📊 최신 등급 요약")
st.sidebar.markdown(f"""
- **환경 (E)**: `{get_grade(latest['ESG_Environmental'])}`
- **사회 (S)**: `{get_grade(latest['ESG_Social'])}`
- **지배구조 (G)**: `{get_grade(latest['ESG_Governance'])}`
- **종합 ESG**: `{get_grade(latest['ESG_Overall'])}`
""")
