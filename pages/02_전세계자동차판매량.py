import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.title("🌍 1900년부터 현재까지 전 세계 자동차 판매량 시각화")

# 실제 데이터 (2010년부터)
data_actual = {
    2010: 77857705, 2011: 79989155, 2012: 84141209, 2013: 87300115,
    2014: 89747430, 2015: 90086346, 2016: 94976569, 2017: 97302534,
    2018: 95634593, 2019: 91786861, 2020: 77621582, 2021: 80145988,
    2022: 85016728, 2023: 93500000, 2024: 90000000
}

# 전체 연도 리스트
current_year = datetime.datetime.now().year
years = list(range(1900, current_year + 1))

# 데이터프레임 생성
df = pd.DataFrame({"year": years, "sales": np.nan})

# 1900~2009는 보간값 (2010년 데이터 기준)
df.loc[df["year"] <= 2009, "sales"] = np.linspace(10000, data_actual[2010], len(df[df["year"] <= 2009]))

# 2010년 이후 실제값 삽입
for year, sales in data_actual.items():
    df.loc[df["year"] == year, "sales"] = sales

# 차트 출력
st.line_chart(df.set_index("year")["sales"])

# 테이블 미리보기
st.markdown("### 📋 데이터 미리보기")
st.dataframe(df.tail(10))

# 설명
st.markdown("""
**설명**:
- ✅ 2010년 이후는 실제 연도별 자동차 판매량 데이터
- 🔄 1900~2009는 2010년 수치를 기준으로 선형 추정
- 📉 단위: 대 (전 세계 신차 판매량 기준)
""")


