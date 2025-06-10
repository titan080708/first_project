import streamlit as st
import numpy as np
import time
import random

# 초기 설정
st.set_page_config(page_title="미로 게임", layout="centered")
st.title("🎯 미로 게임: 적이 등장!")

difficulty = st.sidebar.selectbox("난이도 선택", ["쉬움", "보통", "어려움"])
maze_sizes = {"쉬움": 5, "보통": 7, "어려움": 9}

def generate_maze(size):
    maze = np.ones((size, size), dtype=int)
    maze[1:-1, 1:-1] = 0
    maze[1, 1] = 2  # 플레이어
    maze[-2, -2] = 3  # 출구
    maze[1, size - 2] = 4  # 적
    return maze

# 초기화
if "initialized" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.maze = generate_maze(maze_sizes[difficulty])
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.last_key = ""
    st.session_state.initialized = True

maze = st.session_state.maze

# 위치 찾기
player_pos = np.argwhere(maze == 2)[0]
enemy_pos = np.argwhere(maze == 4)[0]

# 타이머
elapsed = int(time.time() - st.session_state.start_time)
st.sidebar.write(f"⏱️ 경과 시간: {elapsed}초")

def move_entity(pos, dx, dy, target_val):
    x, y = pos
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < maze.shape[0] and 0 <= new_y < maze.shape[1]:
        if maze[new_x, new_y] in [0, 3]:
            maze[x, y] = 0
            maze[new_x, new_y] = target_val
            return np.array([new_x, new_y])
    return pos

def move_enemy():
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_pos = move_entity(enemy_pos, dx, dy, 4)
        if not np.array_equal(new_pos, enemy_pos):
            return new_pos
    return enemy_pos

def move_player(dx, dy):
    if st.session_state.game_over:
        return
    global player_pos, enemy_pos
    x, y = player_pos
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < maze.shape[0] and 0 <= new_y < maze.shape[1]:
        target = maze[new_x, new_y]
        if target in [0, 3, 4]:
            if target == 3:
                st.success(f"🎉 출구 도착! 경과 시간: {int(time.time() - st.session_state.start_time)}초")
                st.session_state.game_over = True
            elif target == 4:
                st.error("💀 적에게 잡혔습니다! 게임 오버!")
                st.session_state.game_over = True
            maze[x, y] = 0
            maze[new_x, new_y] = 2
            player_pos = np.array([new_x, new_y])
            # 적 이동
            enemy_pos = move_enemy()
            # 적과 겹침 체크
            if np.array_equal(player_pos, enemy_pos):
                st.error("💀 적에게 잡혔습니다! 게임 오버!")
                st.session_state.game_over = True

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

# 미로 표시
emoji_map = {0: "⬜", 1: "⬛", 2: "🧍", 3: "🚪", 4: "😈"}
maze_display = "\n".join("".join(emoji_map[cell] for cell in row) for row in maze)
st.markdown(f"```\n{maze_display}\n```")

# 다시 시작
if st.button("🔄 게임 다시 시작"):
    st.session_state.initialized = False
    st.experimental_rerun()



