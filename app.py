# full_rpg_game.py

import streamlit as st
import random

# 초기화
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.monster_hp = 100
    st.session_state.inventory = ["🧪포션", "🧪포션"]
    st.session_state.log = []
    st.session_state.monster = random.choice(["고블린", "슬라임", "드래곤"])
    st.session_state.monster_emoji = {"고블린": "👺", "슬라임": "🟢", "드래곤": "🐉"}[st.session_state.monster]
    st.session_state.music_played = False

def render_health_bar(hp, max_hp=100):
    bar_length = 20
    filled = int(hp / max_hp * bar_length)
    return "❤️" * filled + "⬜" * (bar_length - filled)

# 배경 음악
if not st.session_state.music_played:
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", autoplay=True)
    st.session_state.music_played = True

st.title("🎮 미니 도트 RPG: 숲속의 전투")

# 상태 표시
st.subheader("🧙‍♂️ 플레이어")
st.text(render_health_bar(st.session_state.player_hp))
st.text(f"HP: {st.session_state.player_hp} / 100")
st.write("🎒 인벤토리:", " | ".join(st.session_state.inventory) if st.session_state.inventory else "없음")

st.subheader(f"{st.session_state.monster_emoji} {st.session_state.monster}")
st.text(render_health_bar(st.session_state.monster_hp))
st.text(f"HP: {st.session_state.monster_hp} / 100")

# 행동
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⚔️ 기본 공격"):
        dmg = random.randint(10, 20)
        st.session_state.monster_hp = max(0, st.session_state.monster_hp - dmg)
        st.session_state.log.append(f"플레이어가 {st.session_state.monster}에게 {dmg} 데미지를 입혔다!")

with col2:
    if st.button("🔥 스킬 사용"):
        dmg = random.randint(20, 35)
        st.session_state.monster_hp = max(0, st.session_state.monster_hp - dmg)
        recoil = random.randint(5, 10)
        st.session_state.player_hp = max(0, st.session_state.player_hp - recoil)
        st.session_state.log.append(f"강력한 스킬! {st.session_state.monster}에게 {dmg} 데미지. 반동으로 {recoil} 피해!")

with col3:
    if st.button("🧪 아이템 사용"):
        if "🧪포션" in st.session_state.inventory:
            heal = random.randint(20, 30)
            st.session_state.player_hp = min(100, st.session_state.player_hp + heal)
            st.session_state.inventory.remove("🧪포션")
            st.session_state.log.append(f"포션을 사용해 {heal} 회복했다!")
        else:
            st.warning("포션이 없습니다!")

# 몬스터 반격
if st.session_state.monster_hp > 0 and st.session_state.player_hp > 0:
    monster_attack = random.randint(10, 25)
    st.session_state.player_hp = max(0, st.session_state.player_hp - monster_attack)
    st.session_state.log.append(f"{st.session_state.monster}의 공격! {monster_attack} 피해를 입었다!")

# 로그 출력
st.subheader("📜 전투 로그")
for entry in reversed(st.session_state.log[-5:]):
    st.write(entry)

# 게임 종료 처리
if st.session_state.player_hp <= 0:
    st.error("💀 당신은 쓰러졌습니다... 게임 오버!")
    if st.button("🔁 다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

elif st.session_state.monster_hp <= 0:
    st.success(f"🎉 {st.session_state.monster}를 물리쳤습니다! 전리품을 얻었습니다!")
    st.session_state.inventory.append("🧪포션")
    if st.button("🧟‍♂️ 다음 몬스터 등장"):
        st.session_state.monster = random.choice(["고블린", "슬라임", "드래곤"])
        st.session_state.monster_emoji = {"고블린": "👺", "슬라임": "🟢", "드래곤": "🐉"}[st.session_state.monster]
        st.session_state.monster_hp = 100
        st.session_state.log.append(f"새로운 몬스터 {st.session_state.monster}가 나타났다!")

