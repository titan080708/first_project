import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="커스터마이징 미로 게임", layout="centered")
st.title("🛠️ 커스터마이징 미로 게임")

# 맵 크기 선택
size = st.sidebar.slider("맵 크기", 5, 15, 7)

# 초기 맵 생성 (모두 길(0))
def init_maze(size):
    maze = np.zeros((size, size), dtype=int)
    maze[0, :] = 1
    maze[-1, :] = 1
    maze[:, 0] = 1
    maze[:, -1] = 1
    maze[1, 1] = 2  # 플레이어 시작 위치
    maze[-2, -2] = 3  # 출구 위치
    return maze

if "maze" not in st.session_state or st.session_state.maze.shape[0] != size:
    st.session_state.maze = init_maze(size)
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.last_key = ""
    st.session_state.enemies = []

maze = st.session_state.maze

# 커스터마이징 - 벽을 토글하는 함수
def toggle_cell(x, y):
    if maze[x, y] == 1:
        maze[x, y] = 0
    elif maze[x, y] == 0:
        maze[x, y] = 1

# 맵 편집 UI
st.write("▶ 벽을 클릭해 토글하세요 (벽=⬛, 길=⬜). 플레이어(🧍)와 출구(🚪)는 고정입니다.")
cols = st.columns(size)
for i in range(size):
    row_cols = st.columns(size)
    for j in range(size):
        cell = maze[i, j]
        label = "⬛" if cell == 1 else "⬜"
        if cell == 2:
            label = "🧍"
        elif cell == 3:
            label = "🚪"
        elif cell == 4:
            label = "👾"
        if row_cols[j].button(label, key=f"{i}_{j}"):
            # 플레이어, 출구, 적 위치는 편집 불가
            if cell in [2, 3, 4]:
                continue
            toggle_cell(i, j)

# 적 위치 초기화 (최대 3명)
if "enemies" not in st.session_state or not st.session_state.enemies:
    enemies = []
    while len(enemies) < min(3, (size*size)//10):
        ex, ey = random.randint(1, size-2), random.randint(1, size-2)
        if maze[ex, ey] == 0 and (ex, ey) != (1,1) and (ex, ey) != (size-2, size-2):
            enemies.append([ex, ey])
            maze[ex, ey] = 4
    st.session_state.enemies = enemies

enemies = st.session_state.enemies

# 플레이어 위치 찾기
player_pos = np.argwhere(maze == 2)[0]

# 적 움직임 (랜덤으로 상하좌우 한 칸 이동)
def move_enemies():
    new_positions = []
    for ex, ey in enemies:
        maze[ex, ey] = 0
        moves = [(1,0),(-1,0),(0,1),(0,-1),(0,0)]  # 제자리 포함
        random.shuffle(moves)
        for dx, dy in moves:
            nx, ny = ex+dx, ey+dy
            if 0 <= nx < size and 0 <= ny < size:
                if maze[nx, ny] in [0]:
                    ex, ey = nx, ny
                    break
        new_positions.append([ex, ey])
    for ex, ey in new_positions:
        maze[ex, ey] = 4
    st.session_state.enemies = new_positions

# 플레이어 이동 함수
def move_player(dx, dy):
    if st.session_state.game_over:
        return
    x, y = player_pos
    nx, ny = x+dx, y+dy
    if 0 <= nx < size and 0 <= ny < size:
        # 벽이 아니고 적이 아니면 이동 가능
        if maze[nx, ny] in [0, 3]:
            maze[x, y] = 0
            maze[nx, ny] = 2
            # 적도 움직임
            move_enemies()
            # 적과 충돌 체크
            for ex, ey in st.session_state.enemies:
                if ex == nx and ey == ny:
                    st.session_state.game_over = True
                    st.error("💀 적에게 잡혔습니다! 게임 오버!")
                    return
            # 출구 도착 체크
            if maze[nx, ny] == 3:
                st.session_state.game_over = True
                elapsed = int(time.time() - st.session_state.start_time)
                st.success(f"🎉 출구 도착! 소요 시간: {elapsed}초")

# 방향키 입력
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
emoji_map = {0:"⬜", 1:"⬛", 2:"🧍", 3:"🚪", 4:"👾"}
maze_display = "\n".join("".join(emoji_map[cell] for cell in row) for row in maze)
st.markdown(f"```\n{maze_display}\n```")

# 타이머 표시
elapsed = int(time.time() - st.session_state.start_time)
st.sidebar.write(f"⏱️ 경과 시간: {elapsed}초")







