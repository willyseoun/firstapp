import streamlit as st
import pandas as pd

st.title("🌱 지속가능한 발전 대시보드")
st.subheader("📊 에너지 소비량과 GDP의 관계 분석")

st.markdown("""
CSV 파일을 업로드하면 국가별 **에너지 소비량**과 **GDP** 데이터를 기반으로  
간단한 시각화와 평균 비교를 통해 지속가능한 경영 전략의 기초 분석을 제공합니다.
""")

# CSV 업로드
uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (필드: Country, Energy_Consumption, GDP)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("✅ 데이터 미리보기")
    st.dataframe(df)

    # 숫자형 데이터 확인
    if "Energy_Consumption" in df.columns and "GDP" in df.columns:
        st.subheader("📉 에너지 소비량")
        st.bar_chart(df.set_index("Country")["Energy_Consumption"])

        st.subheader("💰 GDP (국내총생산)")
        st.line_chart(df.set_index("Country")["GDP"])

        # 평균 출력
        avg_energy = df["Energy_Consumption"].mean()
        avg_gdp = df["GDP"].mean()

        st.markdown("### 📌 간단 분석 결과")
        st.write(f"- 평균 에너지 소비량: **{avg_energy:,.2f}**")
        st.write(f"- 평균 GDP: **{avg_gdp:,.2f}**")

        st.markdown("""
        ### 📊 경영 전략적 시사점:
        - 에너지 소비 효율과 경제 성장률을 함께 고려한 정책 수립이 필요합니다.
        - 특정 국가의 에너지 소비 대비 GDP 효율성이 높거나 낮은 경우, 벤치마킹 대상이 될 수 있습니다.
        """)
    else:
        st.error("❗ 'Energy_Consumption' 또는 'GDP' 컬럼이 없습니다.")
else:
    st.info("좌측에서 CSV 파일을 업로드해주세요.")
