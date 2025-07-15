import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Apple vs Samsung ESG Dashboard", layout="wide")

# 데이터 정의
years = list(range(2010, 2025))

apple = pd.DataFrame({
"Year": years,
"Carbon Emissions": [20.1, 23.1, 25.1, 27.8, 29.5, 29.5, 27.1, 25.2, 23.5, 22.1, 20.0, 18.1, 17.3, 16.2, 15.9],
"Renewable Energy": [20, 27, 35, 42, 52, 60, 67, 75, 100, 100, 100, 100, 100, 100, 100],
"Satisfaction": [None, None, None, None, None, 73, 74, 74, 76, 78, 78, 81, 82, 83, 84]
})

samsung = pd.DataFrame({
"Year": years,
"Carbon Emissions": [28.3, 29.4, 30.6, 32.1, 34.4, 36.0, 37.8, 39.5, 41.2, 42.0, 43.3, 44.1, 45.2, 44.3, 43.0],
"Renewable Energy": [10, 11, 12, 13, 15, 18, 20, 22, 25, 27, 30, 35, 40, 45, 50],
"Satisfaction": [None, None, None, None, None, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77]
})

# 정규화 함수
def normalize(series):
return 100 * (series - series.min()) / (series.max() - series.min())

def compute_esg(df):
df = df.copy()
df['Carbon Score'] = 100 - normalize(df['Carbon Emissions'])
df['Satisfaction'] = df['Satisfaction'].fillna(method='ffill')
df['Satisfaction Score'] = normalize(df['Satisfaction'])
df['ESG Score'] = 0.4 * df['Carbon Score'] + 0.3 * df['Renewable Energy'] + 0.3 * df['Satisfaction Score']
return df

apple_esg = compute_esg(apple)
samsung_esg = compute_esg(samsung)

# UI 구성
st.title("📊 Apple vs Samsung ESG 대시보드")
st.markdown("### ESG 스코어 비교 (2010–2024)")

selected_metric = st.selectbox("비교할 항목을 선택하세요:", ["ESG Score", "Carbon Emissions", "Renewable Energy", "Satisfaction"])

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(apple_esg["Year"], apple_esg[selected_metric], label="Apple", marker="o")
ax.plot(samsung_esg["Year"], samsung_esg[selected_metric], label="Samsung", marker="s")
ax.set_xlabel("Year")
ax.set_ylabel(selected_metric)
ax.set_title(f"{selected_metric} Trend")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# 표로 데이터 확인
st.markdown("### 📋 ESG 세부 지표 데이터")
df_combined = pd.DataFrame({
"Year": years,
"Apple ESG Score": apple_esg["ESG Score"],
"Samsung ESG Score": samsung_esg["ESG Score"],
"Apple Carbon (MtCO₂)": apple["Carbon Emissions"],
"Samsung Carbon (MtCO₂)": samsung["Carbon Emissions"],
"Apple Renewable (%)": apple["Renewable Energy"],
"Samsung Renewable (%)": samsung["Renewable Energy"],
"Apple Satisfaction": apple["Satisfaction"],
"Samsung Satisfaction": samsung["Satisfaction"]
})

st.dataframe(df_combined.set_index("Year").round(2))

# 다운로드 기능
csv = df_combined.to_csv(index=False).encode('utf-8')
st.download_button(
"📥 ESG 데이터 CSV 다운로드",
csv,
"apple_samsung_esg.csv",
"text/csv",
key='download-csv'
)
