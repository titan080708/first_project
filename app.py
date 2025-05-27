# mini_dot_rpg.py

import streamlit as st
import random

st.set_page_config(page_title="숲속의 전투 - 미니 도트 RPG")

st.title("🌲 미니 도트 RPG: 숲속의 전투")

# 세션 상태 초기화
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.monster_hp = 100
    st.session_state.log = []

def render_health_bar(hp, max_hp=100):
    bar_length = 20
    filled_length = int(bar_length * hp / max_hp)
    return "❤️" * filled_length + "⬜" * (bar_length - filled_length)

# 상태 표시
st.subheader("🧙‍♂️ 플레이어")
st.text(render_health_bar(st.session_state.player_hp))
st.text(f"HP: {st.session_state.player_hp} / 100")

st.subheader("👾 몬스터")
st.text(render_health_bar(st.session_state.monster_hp))
st.text(f"HP: {st.session_state.monster_hp} / 100")

# 버튼들
col1, col2 = st.columns(2)

with col1:
    if st.button("⚔️ 공격"):
        dmg_to_monster = random.randint(10, 25)
        dmg_to_player = random.randint(5, 20)

        st.session_state.monster_hp = max(0, st.session_state.monster_hp - dmg_to_monster)
        st.session_state.player_hp = max(0, st.session_state.player_hp - dmg_to_player)

        st.session_state.log.append(f"플레이어가 몬스터에게 {dmg_to_monster} 데미지를 입혔다!")
        st.session_state.log.append(f"몬스터가 반격으로 {dmg_to_player} 데미지를 입혔다!")

with col2:
    if st.button("🧪 회복"):
        heal = random.randint(15, 30)
        st.session_state.player_hp = min(100, st.session_state.player_hp + heal)
        counter_dmg = random.randint(5, 15)
        st.session_state.player_hp = max(0, st.session_state.player_hp - counter_dmg)

        st.session_state.log.append(f"플레이어가 {heal} 회복했다! 그러나 몬스터가 {counter_dmg} 데미지를 입혔다!")

# 로그 표시
st.subheader("📜 전투 로그")
for line in reversed(st.session_state.log[-6:]):
    st.write(line)

# 게임 종료
if st.session_state.player_hp == 0:
    st.error("💀 당신은 쓰러졌습니다... 게임 오버!")
    if st.button("🔁 다시 시작"):
        st.session_state.player_hp = 100
        st.session_state.monster_hp = 100
        st.session_state.log = []

elif st.session_state.monster_hp == 0:
    st.success("🎉 몬스터를 물리쳤습니다! 승리!")
    if st.button("🔁 다시 시작"):
        st.session_state.player_hp = 100
        st.session_state.monster_hp = 100
        st.session_state.log = []

