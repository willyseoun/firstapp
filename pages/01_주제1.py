import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌍 지속가능한 발전을 위한 데이터 분석 대시보드")
st.subheader("📊 에너지 소비와 GDP 간의 관계 분석")

st.markdown("""
이 앱은 **지속가능한 경영 전략 수립**을 위한 데이터 기반 분석 도구입니다.  
CSV 파일을 업로드하면, 국가별 에너지 소비량과 GDP 간의 관계를 시각화하고  
기초적인 통찰을 제공합니다.
""")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드 (필드 예시: Country, Energy_Consumption, GDP)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("데이터 미리보기")
    st.dataframe(df.head())

    if "Energy_Consumption" in df.columns and "GDP" in df.columns:
        st.subheader("📈 에너지 소비량 vs GDP")

        # 산점도 시각화
        fig, ax = plt.subplots()
        ax.scatter(df["Energy_Consumption"], df["GDP"])
        ax.set_xlabel("에너지 소비량 (단위: TOE)")
        ax.set_ylabel("GDP (단위: 억 달러)")
        ax.set_title("에너지 소비와 GDP의 관계")
        st.pyplot(fig)

        # 단순 비즈니스 인사이트
        avg_energy = df["Energy_Consumption"].mean()
        avg_gdp = df["GDP"].mean()

        st.markdown("### 🔍 간단한 분석 결과:")
        st.write(f"- 전체 평균 에너지 소비량: **{avg_energy:,.2f}**")
        st.write(f"- 전체 평균 GDP: **{avg_gdp:,.2f}**")

        st.markdown("""
        **경영적 시사점:**  
        에너지 소비와 경제 생산성(GDP) 간의 관계를 통해  
        국가 또는 기업 단위의 **효율적 에너지 전략**과  
        **지속가능한 성장 모델 수립**에 기초 자료로 활용할 수 있습니다.
        """)
    else:
        st.warning("필수 컬럼 'Energy_Consumption' 및 'GDP'가 존재하는지 확인해주세요.")
else:
    st.info("왼쪽에서 CSV 파일을 업로드하면 분석 결과가 나타납니다.")

