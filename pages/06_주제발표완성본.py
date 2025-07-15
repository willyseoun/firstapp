import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ESG 분석 대시보드", layout="wide")

# ✅ CSV 데이터 캐시로 불러오기
@st.cache_data
def load_data(file):
return pd.read_csv(file)

CSV_FILE = "esg_data.csv"

try:
df = load_data(CSV_FILE)
except FileNotFoundError:
st.error(f"⚠️ '{CSV_FILE}' 파일이 없습니다. 같은 폴더에 올려주세요.")
st.stop()

# ✅ 등급 함수
def get_grade(score):
if score >= 80:
return "A (우수)"
elif score >= 60:
return "B (보통)"
elif score >= 40:
return "C (주의)"
else:
return "D (위험)"

# ✅ 등급 컬럼 계산
df["Environmental_Grade"] = df["ESG_Environmental"].apply(get_grade)
df["Social_Grade"] = df["ESG_Social"].apply(get_grade)
df["Governance_Grade"] = df["ESG_Governance"].apply(get_grade)
df["ESG_Grade"] = df["ESG_Overall"].apply(get_grade)

latest = df.iloc[-1]

# ✅ 사이드바 정보
with st.sidebar:
st.header("📌 기업 정보")
st.markdown(f"""
**기업명**: `{df['CompanyName'].iloc[0]}`
**산업군**: `{df['Industry'].iloc[0]}`
**지역**: `{df['Region'].iloc[0]}`
""")
st.subheader("📊 최신 등급 요약")
st.markdown(f"""
환경 (E): `{get_grade(latest['ESG_Environmental'])}`
사회 (S): `{get_grade(latest['ESG_Social'])}`
지배구조 (G): `{get_grade(latest['ESG_Governance'])}`
종합 ESG: `{get_grade(latest['ESG_Overall'])}`
""")
# ✅ ESG 점수 테이블
st.title("📊 ESG 분석 대시보드")
st.markdown("연도별 ESG 점수와 환경 성과를 분석합니다.")
st.subheader("📈 ESG 점수 및 등급")
st.dataframe(df[[
"Year", "ESG_Environmental", "Environmental_Grade",
"ESG_Social", "Social_Grade",
"ESG_Governance", "Governance_Grade",
"ESG_Overall", "ESG_Grade"
]])

# ✅ 직선 그래프 함수
def plot_line_chart(df, y_columns, title, ylabel):
fig, ax = plt.subplots()
for col in y_columns:
ax.plot(df["Year"], df[col], label=col, marker='o', linestyle='-')
ax.set_title(title)
ax.set_xlabel("Year")
ax.set_ylabel(ylabel)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ✅ ESG 변화 추이
if st.checkbox("📉 ESG 점수 변화 추이 보기"):
st.subheader("ESG 점수 변화 추이 (직선형)")
plot_line_chart(
df,
["ESG_Environmental", "ESG_Social", "ESG_Governance", "ESG_Overall"],
"ESG Score Trends", "Score"
)

# ✅ 환경 성과 지표
if st.checkbox("🌿 환경 성과 지표 보기"):
st.subheader("환경 성과 지표 (직선형)")
plot_line_chart(
df,
["CarbonEmissions", "WaterUsage", "EnergyConsumption"],
"Environmental Performance Trends", "Usage / Emissions"
)

# ✅ 개선 과제
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
