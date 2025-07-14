import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.title("🌍 1900년부터 현재까지 전 세계 자동차 판매량 시각화")

# 2010~2024년 실제 데이터 (Our World in Data + Wikipedia)
data_actual = {
    2010: 77_857_705, 2011: 79_989_155, 2012: 84_141_209, 2013: 87_300_115,
    2014: 89_747_430, 2015: 90_086_346, 2016: 94_976_569, 2017: 97_302_534,
    2018: 95_634_593, 2019: 91_786_861, 2020: 77_621_582, 2021: 80_145_988,
    2022: 85_016_728  # up to 2022 :contentReference[oaicite:4]{index=4}
}

# 2023~2024년은 ACEA와 생산량 기반 예측
data_actual[2023] = 93_500_000  # approx :contentReference[oaicite:5]{index=5}
data_actual[2024] = 90_000_000  # 보수적 추정

# 1900~2009: 연도 구간 보간법
years_full = list(range(1900, datetime.datetime.now().year + 1))
df = pd.DataFrame(index=years_full, columns=["sales"])
# 산술적 하한/상한 설정
df.loc[2010:] = pd.Series(data_actual)
# 1900년 데이터 시작: 1만 대 → 2009년 데이터 직전: 7천만 대 보간
df.loc[1900:2009, "sales"] = np.linspace(10_000, data_actual[2009], len(range(1900,2010)))

df = df.reset_index().rename(columns={"index": "year"})

# Streamlit 시각화
st.line_chart(df.set_index("year")["sales"])

st.markdown("### 📋 데이터 미리보기")
st.dataframe(df.tail(10))

st.markdown("**설명**:\n- 2010년 이후 실제 판매 데이터 (출처: Our World in Data, Wikipedia 등)\n- 2023~2024년 예측 수치 포함\n- 1900~2009년은 선형 보간 방식으로 가공한 추정치입니다.")

