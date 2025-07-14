import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime

st.title("🌍 전 세계 자동차 생산량 & 대기 중 CO₂ 농도 변화 (1990–2024)")

# 자동차 생산량 데이터
data_auto = {
    1990: 38_564_516, 1995: 50_046_000, 2000: 58_374_162,
    2005: 66_482_439, 2009: 61_791_868, 2010: 77_857_705,
    2011: 79_989_155, 2012: 84_141_209, 2013: 87_300_115,
    2014: 89_747_430, 2015: 90_086_346, 2016: 94_976_569,
    2017: 97_302_534, 2018: 95_634_593, 2019: 91_786_861,
    2020: 77_621_582, 2021: 80_145_988, 2022: 85_016_728,
    2023: 89_760_533, 2024: 92_504_338
}

# CO₂ 농도 데이터 (ppm)
data_co2 = {
    1990: 354.16, 1995: 358.83, 2000: 369.71, 2005: 379.80,
    2010: 389.85, 2015: 399.40, 2020: 414.24, 2022: 418.52,
    2023: 421.24, 2024: 422.80
}

# 전체 연도 목록
years = list(range(1990, 2025))
df = pd.DataFrame({"year": years})

# 데이터 보간
df["production"] = df["year"].map(data_auto)
df["production"] = df["production"].interpolate()

df["co2_ppm"] = df["year"].map(data_co2)
df["co2_ppm"] = df["co2_ppm"].interpolate()

# ✅ 연도 선택 슬라이더
min_year, max_year = st.slider(
    "📅 분석할 연도 범위를 선택하세요:",
    min_value=min(years),
    max_value=max(years),
    value=(2000, 2024),
    step=1
)

# 선택 범위 데이터 필터링
df_filtered = df[(df["year"] >= min_year) & (df["year"] <= max_year)]

# 📊 자동차 생산량 그래프
st.markdown("### 🚗 전 세계 자동차 생산량 (단위: 대)")
auto_chart = alt.Chart(df_filtered).mark_line(color="steelblue").encode(
    x=alt.X("year:O", title="연도"),
    y=alt.Y("production:Q", title="자동차 생산량", scale=alt.Scale(zero=False))
).properties(width=700, height=300)
st.altair_chart(auto_chart, use_container_width=True)

# 📈 CO₂ 농도 그래프
st.markdown("### 🌫️ 대기 중 CO₂ 농도 (단위: ppm)")
co2_chart = alt.Chart(df_filtered).mark_line(color="darkred").encode(
    x=alt.X("year:O", title="연도"),
    y=alt.Y("co2_ppm:Q", title="CO₂ 농도", scale=alt.Scale(zero=False))
).properties(width=700, height=300)
st.altair_chart(co2_chart, use_container_width=True)

# 📋 데이터 테이블
st.markdown("### 📋 선택한 연도 범위 데이터 미리보기")
st.dataframe(df_filtered.reset_index(drop=True))

# 📌 설명
st.markdown("""
**설명**
- 🚗 자동차 생산량: Wikipedia 'World motor vehicle production' 기준  
- 🌫️ CO₂ 농도: NOAA Mauna Loa 관측소 연평균 (전지구 표준 지표)  
- 📈 중간 연도는 선형 보간 처리됨  
""")
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("🚗 내연기관(ICE) vs 전기차(EV) 생산·판매량 비교 (2010–2024)")

# 연도 리스트
years = list(range(2010, 2025))
df = pd.DataFrame({"year": years})

# 전체 자동차 생산량 (Wikipedia 등 기반)
total_prod = {
    2010: 77_857_705,
    2011: 79_989_155,
    2012: 84_141_209,
    2013: 87_300_115,
    2014: 89_747_430,
    2015: 90_086_346,
    2016: 94_976_569,
    2017: 97_302_534,
    2018: 95_634_593,
    2019: 91_786_861,
    2020: 77_621_582,
    2021: 80_145_988,
    2022: 85_016_728,
    2023: 93_546_599,
    2024: 92_504_338
}

# EV 생산/판매량 (IEA 등 기준 추정)
ev = {
    2010: 0.1e6,    # 약 10만대 추정 (초기 극소량)
    2011: 0.15e6,
    2012: 0.25e6,
    2013: 0.40e6,
    2014: 0.60e6,
    2015: 1.75e6,
    2016: 2.50e6,
    2017: 3.60e6,
    2018: 5.20e6,
    2019: 7.20e6,
    2020: 3.5e6,   # 팬데믹 영향 반영(잠정)
    2021: 6.75e6,
    2022: 10e6,
    2023: 14e6,
    2024: 20.35e6
}

df["total"] = df["year"].map(total_prod).interpolate()
df["ev"] = df["year"].map(ev).interpolate()
df["ice"] = df["total"] - df["ev"]

# 연도 범위 선택 슬라이더
min_year, max_year = st.slider(
    "📅 분석할 연도 범위를 선택하세요:",
    min_value=2010,
    max_value=2024,
    value=(2015, 2024),
    step=1
)

df_filtered = df[(df["year"] >= min_year) & (df["year"] <= max_year)]

# EV 그래프
st.markdown("### ⚡ 전기차(EV) 생산·판매량")
ev_chart = alt.Chart(df_filtered).mark_line(color="green").encode(
    x=alt.X("year:O", title="연도"),
    y=alt.Y("ev:Q", title="EV 생산·판매량 (대)")
).properties(width=700, height=300)
st.altair_chart(ev_chart, use_container_width=True)

# ICE 그래프
st.markdown("### 🛢 내연기관차(ICE) 생산량")
ice_chart = alt.Chart(df_filtered).mark_line(color="orange").encode(
    x=alt.X("year:O", title="연도"),
    y=alt.Y("ice:Q", title="ICE 생산량 (대)")
).properties(width=700, height=300)
st.altair_chart(ice_chart, use_container_width=True)

# 데이터 테이블
st.markdown("### 📋 선택된 연도 데이터")
st.dataframe(df_filtered[["year", "ev", "ice", "total"]].reset_index(drop=True))

# 설명
st.markdown("""
**설명**  
- 🚗 전체 자동차 생산량: Wikipedia 기반 실제 데이터  
- ⚡ 전기차(EV) 생산/판매량: IEA 기준 추정치  
- 🛢 ICE = 전체 - EV 계산  
- 📉 중간 연도는 선형 보간 처리  
""")






