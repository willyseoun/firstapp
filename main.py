import streamlit as st

st.set_page_config(page_title="간단한 투표 앱", page_icon="🗳️")

st.title("🗳️ 당신의 선택은?")
st.write("아래 보기 중 하나를 선택하고 제출해보세요!")

# 선택 항목
options = ["🍕 피자", "🍔 햄버거", "🍜 라면", "🥗 샐러드"]

# 사용자 선택
choice = st.radio("무엇을 가장 좋아하나요?", options)

# 제출 버튼
if st.button("제출"):
    st.success(f"당신은 **{choice}**를 선택했어요!")
