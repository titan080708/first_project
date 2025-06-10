import streamlit as st
import numpy as np
import time

# 초기 설정
st.set_page_config(page_title="미로 게임", layout="centered")
st.title("🎯 미로 게임")

# 난이도 설정
difficulty = st.sidebar.selectbox("난이도 선택", ["쉬움", "보통", "어려움"])

maze_sizes = {
    "쉬움": 5,
    "보통": 7,
    "어려움": 9
}

def generate_maze(size):
    maze = np.ones((size, size), dtype=int)
    maze[1:-1, 1:-1] = 0
    maze[1, 1] = 2  # 플레이어
    maze[-2, -2] = 3  # 출구
    return maze

# 세션 상태 초기화
if "initialized" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.maze = generate_maze(maze_sizes[difficulty])
    st.session_state.start_time = time.time()
    st.session_state.initialized = True
    st.session_state.game_over = False
    st.session_state.last_key = ""

maze = st.session_state.maze
player_pos = np.argwhere(maze == 2)[0]

# 타이머 표시
elapsed = int(time.time() - st.session_state.start_time)
st.sidebar.write(f"⏱️ 경과 시간: {elapsed}초")

# 이동 함수
def move_player(dx, dy):
    if st.session_state.game_over:
        return
    x, y = player_pos
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < maze.shape[0] and 0 <= new_y < maze.shape[1]:
        if maze[new_x, new_y] in [0, 3]:
            if maze[new_x, new_y] == 3:
                st.session_state.game_over = True
                end_time = int(time.time() - st.session_state.start_time)
                st.success(f"🎉 출구 도착! 총 소요 시간: {end_time}초")
            maze[x, y] = 0
            maze[new_x, new_y] = 2

# 키 입력
key = st.text_input("방향키 입력 (w/a/s/d):", value=st.session_state.last_key)
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
maze_display = "\n".join("".join(emoji_map[cell] for cell in row) for row in maze)
st.markdown(f"```\n{maze_display}\n```")

# 리셋 버튼
if st.button("🔄 게임 다시 시작"):
    st.session_state.initialized = False
    st.experimental_rerun()
