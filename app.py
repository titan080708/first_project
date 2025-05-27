# card_battle_game.py

import streamlit as st
import random

# 초기화
if "deck" not in st.session_state:
    st.session_state.deck = list(range(1, 14)) * 4  # 52장의 카드 (1~13)
    random.shuffle(st.session_state.deck)
    st.session_state.score = {"플레이어": 0, "컴퓨터": 0, "무승부": 0}
    st.session_state.last_draw = []

st.title("🃏 카드 대결 게임")

# 카드 뽑기
if st.button("카드 뽑기"):
    if len(st.session_state.deck) >= 2:
        player_card = st.session_state.deck.pop()
        computer_card = st.session_state.deck.pop()
        st.session_state.last_draw = [player_card, computer_card]

        if player_card > computer_card:
            st.session_state.score["플레이어"] += 1
            result = "😊 당신이 이겼어요!"
        elif player_card < computer_card:
            st.session_state.score["컴퓨터"] += 1
            result = "😢 컴퓨터가 이겼어요."
        else:
            st.session_state.score["무승부"] += 1
            result = "😐 무승부입니다."
        st.success(result)
    else:
        st.warning("덱에 카드가 부족합니다. 아래 버튼으로 리셋하세요.")

# 마지막 뽑은 카드 표시
if st.session_state.last_draw:
    st.subheader("🆚 이번 라운드")
    st.write(f"**플레이어:** {st.session_state.last_draw[0]}   |   **컴퓨터:** {st.session_state.last_draw[1]}")

# 점수 표시
st.subheader("📊 현재 점수")
st.write(st.session_state.score)

# 남은 카드 수
st.caption(f"남은 카드 수: {len(st.session_state.deck)}")

# 리셋
if st.button("🔁 게임 초기화"):
    st.session_state.deck = list(range(1, 14)) * 4
    random.shuffle(st.session_state.deck)
    st.session_state.score = {"플레이어": 0, "컴퓨터": 0, "무승부": 0}
    st.session_state.last_draw = []


