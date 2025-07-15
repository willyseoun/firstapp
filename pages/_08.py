import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ESG 분석 대시보드", layout="wide")

# ✅ 캐시 적용된 CSV 로딩
@st.cache_data
def load_data(file):
return pd.read_csv(file)

CSV_FILE = "esg_data.csv"

try:
df = load_data(CSV_FILE)
except FileNotFoundError:
st.error(f"⚠️ '{CSV_FILE}' 파일이 존재하지 않습니다. 업로드 후 다시 실행해주세요.")
st.stop()

# ✅ 등급 산출 함수
def get_grade(score):
if score >= 80:
return "A (우수)"
elif score >= 60:
return "B (보통)"
elif score >= 40:
return "C (주의)"
else:
return "D (위험)"

# ✅ 등급 컬럼 생성
df["Environmental_Grade"] = df["ESG_Environmental"].apply(get_grade)
df["Social_Grade"] = df["ESG_Social"].apply(get_grade)
df["Governance_Grade"] = df["ESG_Governance"].apply(get_grade)
df["ESG_Grade"] = df["ESG_Overall"].apply(get_grade)

latest = df.iloc[-1]

# ✅ 사이드바 요약 정보
with st.sidebar:
st.header("📌 기업 정보")
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

# ✅ ESG 점수 테이블
st.title("📊 ESG 분석 대시보드")
st.markdown("기업의 ESG 점수 추세와 미래 개선 과제를 종합적으로 분석합니다.")

st.subheader("📈 ESG 점수 및 등급")
st.dataframe(df[[
"Year", "ESG_Environmental", "Environmental_Grade",
"ESG_Social", "Social_Grade",
"ESG_Governance", "Governance_Grade",
"ESG_Overall", "ESG_Grade"
]])

# ✅ 직선형 그래프 함수 정의
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

# ✅ ESG 점수 변화 추이 그래프
if st.checkbox("📉 ESG 점수 변화 추이 보기"):
st.subheader("ESG 점수 변화 추이 (직선형)")
plot_line_chart(
df,
["ESG_Environmental", "ESG_Social", "ESG_Governance", "ESG_Overall"],
"ESG Score Trends",
"Score"
)

# ✅ 환경 성과 지표 그래프
if st.checkbox("🌿 환경 성과 지표 보기"):
st.subheader("환경 성과 지표 (직선형)")
plot_line_chart(
df,
["CarbonEmissions", "WaterUsage", "EnergyConsumption"],
"Environmental Performance Trends",
"Usage / Emissions"
)

# ✅ 향후 ESG 개선 과제 제안
st.subheader("🛠️ 향후 ESG 개선 과제 및 해결 방안")

st.markdown("**환경(E)**")
st.markdown("- 과제: 탄소배출 과다 → ✅ *신재생에너지 전환*, *탄소배출권 거래 도입*")
st.markdown("- 과제: 에너지 비효율 → ✅ *고효율 설비 도입*, *스마트팩토리 도입*")

st.markdown("**사회(S)**")
st.markdown("- 과제: 직원 이직률 증가 → ✅ *복지 제도 강화*, *유연근무제 도입*")
st.markdown("- 과제: 지역사회 기여 부족 → ✅ *지역 고용 연계*, *공헌활동 확대*")

st.markdown("**지배구조(G)**")
st.markdown("- 과제: 이사회 다양성 부족 → ✅ *여성·외부 이사 확대*")
st.markdown("- 과제: 리스크 관리 미흡 → ✅ *내부통제 시스템 강화*, *정기 감사 확대*")

# ✅ 개선 실행 시 기대 효과 시각화
st.subheader("📈 ESG 개선 실행 시 점수 변화 시뮬레이션")

# 시뮬레이션 데이터
categories = ["환경 (E)", "사회 (S)", "지배구조 (G)"]
before = [58, 61, 63] # 가상의 현재 점수
after = [74, 78, 80] # 개선 후 기대 점수

# 막대그래프
fig, ax = plt.subplots()
bar_width = 0.35
x = range(len(categories))

ax.bar(x, before, width=bar_width, label="개선 전", color="lightgray")
ax.bar([i + bar_width for i in x], after, width=bar_width, label="개선 후", color="skyblue")

ax.set_xlabel("ESG 항목")
ax.set_ylabel("점수")
ax.set_title("ESG 개선 실행 시 점수 변화 예측")
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(categories)
ax.legend()
ax.grid(axis="y")

st.pyplot(fig)

st.success("✅ ESG 개선 과제 실행 시 기업 이미지, 투자 유치, 지속가능성 등 다방면에서 이득을 기대할 수 있습니다.")
