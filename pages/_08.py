import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="ESG 분석 대시보드", layout="wide")

# CSV 파일명
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

# 연도 필터링
years = df["Year"].unique()
min_year, max_year = int(years.min()), int(years.max())
selected_years = st.slider("🔍 분석할 연도 범위 선택", min_year, max_year, (min_year, max_year))
filtered_df = df[df["Year"].between(*selected_years)]

# 최근 데이터
latest = filtered_df.iloc[-1]

# 타이틀
st.title("📊 ESG 분석 대시보드")
st.markdown("한 기업의 연도별 ESG 추세 및 향후 개선 방향을 시각적으로 분석합니다.")

# 사이드바 기업 정보
st.sidebar.header("📌 기업 정보")
st.sidebar.markdown(f"""
- **기업명**: `{df['CompanyName'].iloc[0]}`
- **산업군**: `{df['Industry'].iloc[0]}`
- **지역**: `{df['Region'].iloc[0]}`
""")

# 점수 테이블
st.subheader("📈 ESG 점수 및 등급")
st.dataframe(filtered_df[[
    "Year", "ESG_Environmental", "Environmental_Grade",
    "ESG_Social", "Social_Grade",
    "ESG_Governance", "Governance_Grade",
    "ESG_Overall", "ESG_Grade"
]])

# ESG 점수 추이 시각화
st.subheader("📉 ESG 점수 변화 추이")
col1, col2 = st.columns(2)
with col1:
    st.line_chart(filtered_df.set_index("Year")[["ESG_Environmental"]])
    st.line_chart(filtered_df.set_index("Year")[["ESG_Social"]])
with col2:
    st.line_chart(filtered_df.set_index("Year")[["ESG_Governance"]])
    st.line_chart(filtered_df.set_index("Year")[["ESG_Overall"]])

# 환경 성과 시각화
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

# 향후 과제 + 해결책 + 기대 효과 + 그래프
st.subheader("🛠️ 향후 ESG 개선 과제, 해결책 및 기대 효과")

problem_data = []

# 환경(E)
if latest["ESG_Environmental"] < 60:
    problem_data.append({
        "분야": "환경 (E)",
        "과제": "탄소 배출량 과다 및 에너지 효율 부족",
        "해결책": [
            "1️⃣ 친환경 설비 도입 (고효율 보일러, 폐열 회수 시스템 등)",
            "2️⃣ 재생에너지 사용 확대 (태양광, 풍력 등)",
            "3️⃣ 탄소배출권 거래제 적극 참여 및 저감 기술 적용"
        ],
        "기대효과": "🎯 에너지 비용 절감, 인센티브 확보, 글로벌 친환경 인증 획득",
        "그래프컬럼": "ESG_Environmental"
    })

# 사회(S)
if latest["ESG_Social"] < 60:
    problem_data.append({
        "분야": "사회 (S)",
        "과제": "직원 만족도 및 사회적 책임 부족",
        "해결책": [
            "1️⃣ 유연근무제 및 복지제도 확대 (육아 지원 등)",
            "2️⃣ 다양성과 포용성 프로그램 실행 (성별, 장애인 고용)",
            "3️⃣ 지역사회 연계 프로젝트 및 기부 활동 강화"
        ],
        "기대효과": "🎯 직원 유지율 증가, 평판 개선, 이해관계자와의 관계 강화",
        "그래프컬럼": "ESG_Social"
    })

# 지배구조(G)
if latest["ESG_Governance"] < 60:
    problem_data.append({
        "분야": "지배구조 (G)",
        "과제": "이사회 다양성 부족 및 투명성 미흡",
        "해결책": [
            "1️⃣ 외부 감사 강화 및 윤리경영 준수 코드 도입",
            "2️⃣ 이사회에 여성·전문가 비율 확대",
            "3️⃣ 정기적인 리스크 평가와 내부 통제 시스템 운영"
        ],
        "기대효과": "🎯 기업 투명성 확보, 투자자 신뢰 증대, 리스크 관리 강화",
        "그래프컬럼": "ESG_Governance"
    })

# 출력
if problem_data:
    for item in problem_data:
        st.markdown(f"### 🔍 {item['분야']}")
        st.markdown(f"**📌 문제 요약**: {item['과제']}")
        st.markdown("**🧩 해결 방안 제안:**")
        for sol in item["해결책"]:
            st.markdown(f"- {sol}")
        st.markdown(f"**✨ 기대 효과**: {item['기대효과']}")
        st.markdown(f"**📊 {item['분야']} 점수 변화 그래프**")
        st.line_chart(filtered_df.set_index("Year")[[item["그래프컬럼"]]])
        st.markdown("---")
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

# 다운로드 버튼
st.download_button("📥 ESG 데이터 다운로드", data=filtered_df.to_csv(index=False), file_name="filtered_esg_data.csv", mime="text/csv")
