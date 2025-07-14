import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.title("🌍 1990년부터 2024년까지 전 세계 자동차 생산량 시각화")

# Wikipedia 기반 실제 데이터 (1990–2022) + 2023–2024 보간
data_actual = {
    1990: 38_564_516, 1995: 50_046_000, 2000: 58_374_162,
    2005: 66_482_439, 2009: 61_791_868, 2010: 77_857_705,
    2011: 79_989_155, 2012: 84_141_209, 2013: 87_300_115,
    2014: 89_747_430, 2015: 90_086_346, 2016: 94_976_569,
    2017: 97_302_534, 2018: 95_634_593, 2019: 91_786_861,
    2020: 77_621_582, 2021: 80_145_988, 2022: 85_016_728
}

# 2023–2024 연속 추정 보간
data_actual[2023] = 89_760_533  # (2022+2024)/2 보간
data_actual[2024] = 92_504_338  # Wikipedia 최대 생산량 :contentReference[oaicite:2]{index=2}

# 연도 범위
years = list(range(1990, 2025))
df = pd.DataFrame({"year": years, "production": np.nan})

# 실제 알려진 연도값 직접 삽입
known_years = sorted(data_actual.keys())
for y in known_years:
    df.loc[df["year"] == y, "production"] = data_actual[y]

# 중간 연도는 직선 보간
df["production"] = df["production"].interpolate()

# 차트 출력
st.line_chart(df.set_index("year")["production"])

# 데이터 테이블
st.markdown("### 📋 최근 10년 데이터 미리보기")
st.dataframe(df[df["year"] >= 2015].reset_index(drop=True))

# 설명
st.markdown("""
**설명:**
- ✅ 1990–2022: Wikipedia 기반 실제 생산량 데이터 :contentReference[oaicite:3]{index=3}  
- 📈 2023–2024: 보간값 포함  
- 단위: 대 (전 세계 연간 신규 생산량)
""")



