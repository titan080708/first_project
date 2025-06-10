import streamlit as st
import numpy as np

# 초기 설정
st.set_page_config(page_title="미로 게임", layout="centered")
st.title("🎯 간단한 미로 게임")

# 미로 정의 (0 = 길, 1 = 벽, 2 = 플레이어, 3 = 출구)
maze = np.array([
    [1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 3, 1],
    [1, 1, 1, 1, 1]
])

# 세션 상태에 저장
if "maze" not in st.session_state:
    st.session_state.maze = maze.copy()

# 현재 플레이어 위치 찾기
player_pos = np.argwhere(st.session_state.maze == 2)[0]

def move_player(dx, dy):
    x, y = player_pos
    new_x, new_y = x + dx, y + dy
    if st.session_state.maze[new_x, new_y] in [0, 3]:
        if st.session_state.maze[new_x, new_y] == 3:
            st.success("🎉 출구에 도착했습니다!")
        st.session_state.maze[x, y] = 0
        st.session_state.maze[new_x, new_y] = 2

# 키보드 입력 처리
key = st.session_state.get("last_key", None)
key = st.text_input("방향키 (w/a/s/d):", key)

if key:
    st.session_state.last_key = key
    if key == "w":
        move_player(-1, 0)
    elif key == "s":
        move_player(1, 0)
    elif key == "a":
        move_player(0, -1)
    elif key == "d":
        move_player(0, 1)

# 미로 출력
emoji_map = {0: "⬜", 1: "⬛", 2: "🧍", 3: "🚪"}
maze_display = "\n".join("".join(emoji_map[cell] for cell in row) for row in st.session_state.maze)
st.markdown(f"```\n{maze_display}\n```")
