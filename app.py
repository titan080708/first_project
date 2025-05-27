# streamlit_example.py

import streamlit as st

# 제목
st.title("간단한 제곱 계산기")

# 숫자 입력 받기
number = st.number_input("숫자를 입력하세요", value=0)

# 버튼 누르면 계산
if st.button("제곱 계산하기"):
    squared = number ** 2
    st.success(f"{number}의 제곱은 {squared}입니다.")
