import streamlit as st
import numpy as np
import time
import random

# 페이지 설정: 제목과 레이아웃 중앙 정렬
st.set_page_config(page_title="커스터마이징 미로 게임", layout="centered")
st.title("🛠️ 커스터마이징 미로 게임")

# 사이드바에서 맵 크기를 5에서 15 사이로 조절할 수 있게 슬라이더 제공
size = st.sidebar.slider("맵 크기", 5, 15, 7)

# 맵 초기화 함수
def init_maze(size):
    # 전체 맵을 0(길)으로 초기화한 뒤 가장자리에는 1(벽)로 채움
    maze = np.zeros((size, size), dtype=int)
    maze[0, :] = 1          # 위쪽 벽
    maze[-1, :] = 1         # 아래쪽 벽
    maze[:, 0] = 1          # 왼쪽 벽
    maze[:, -1] = 1         # 오른쪽 벽
    maze[1, 1] = 2          # 플레이어 시작 위치 (2로 표시)
    maze[-2, -2] = 3        # 출구 위치 (3으로 표시)
    return maze

# 세션 상태에 맵이 없거나 크기가 바뀌었으면 초기화 진행
if "maze" not in st.session_state or st.session_state.maze.shape[0] != size:
    st.session_state.maze = init_maze(size)
    st.session_state.start_time = time.time()  # 게임 시작 시간 기록 (타이머용)
    st.session_state.game_over = False        # 게임 오버 상태 초기화
    st.session_state.last_key = ""             # 마지막 입력 키 저장용
    st.session_state.enemies = []              # 적 위치 리스트 초기화

maze = st.session_state.maze  # 현재 맵 불러오기

# 벽/길 토글 함수
def toggle_cell(x, y):
    # 벽(1) -> 길(0), 길(0) -> 벽(1)로 상태 변경
    if maze[x, y] == 1:
        maze[x, y] = 0
    elif maze[x, y] == 0:
        maze[x, y] = 1

# 맵 편집 UI 출력
st.write("▶ 벽을 클릭해 토글하세요 (벽=⬛, 길=⬜). 플레이어(🧍)와 출구(🚪)는 고정입니다.")
cols = st.columns(size)  # 컬럼 생성 (사용은 루프 내에서)

# 2중 for문으로 각 셀마다 버튼 생성
for i in range(size):
    row_cols = st.columns(size)  # 한 행에 size만큼 버튼 배치
    for j in range(size):
        cell = maze[i, j]
        # 각 셀 상태에 따른 이모지 설정
        label = "⬛" if cell == 1 else "⬜"
        if cell == 2:
            label = "🧍"  # 플레이어
        elif cell == 3:
            label = "🚪"  # 출구
        elif cell == 4:
            label = "👾"  # 적
        # 버튼 클릭 시 처리 (플레이어, 출구, 적은 편집 불가)
        if row_cols[j].button(label, key=f"{i}_{j}"):
            if cell in [2, 3, 4]:
                continue
            toggle_cell(i, j)  # 벽/길 토글 함수 호출

# 적 위치 초기화: 최대 3명, 맵 크기 대비 적당한 수로 설정
if "enemies" not in st.session_state or not st.session_state.enemies:
    enemies = []
    # 적을 랜덤 위치에 배치 (길(0)인 곳, 플레이어/출구 제외)
    while len(enemies) < min(3, (size*size)//10):
        ex, ey = random.randint(1, size-2), random.randint(1, size-2)
        if maze[ex, ey] == 0 and (ex, ey) != (1,1) and (ex, ey) != (size-2, size-2):
            enemies.append([ex, ey])
            maze[ex, ey] = 4  # 적 위치 표시
    st.session_state.enemies = enemies

enemies = st.session_state.enemies  # 현재 적 위치 불러오기

# 플레이어 현재 위치 찾기
player_pos = np.argwhere(maze == 2)[0]

# 적 움직임 함수: 적들은 랜덤으로 상하좌우 한 칸 이동 (혹은 제자리)
def move_enemies():
    new_positions = []
    for ex, ey in enemies:
        maze[ex, ey] = 0  # 이전 적 위치 0(길)으로 변경
        moves = [(1,0),(-1,0),(0,1),(0,-1),(0,0)]  # 이동 방향 후보 (상하좌우 + 대기)
        random.shuffle(moves)  # 무작위 순서 섞기
        for dx, dy in moves:
            nx, ny = ex+dx, ey+dy
            # 맵 내 범위 확인
            if 0 <= nx < size and 0 <= ny < size:
                # 길(0)인 곳만 이동 가능
                if maze[nx, ny] == 0:
                    ex, ey = nx, ny
                    break
        new_positions.append([ex, ey])
    # 새 위치들 적 표시(4)로 업데이트
    for ex, ey in new_positions:
        maze[ex, ey] = 4
    st.session_state.enemies = new_positions

# 플레이어 이동 함수
def move_player(dx, dy):
    if st.session_state.game_over:
        return  # 게임 오버 시 이동 불가
    x, y = player_pos
    nx, ny = x+dx, y+dy
    # 맵 내 범위 체크
    if 0 <= nx < size and 0 <= ny < size:
        # 벽(1)이나 적(4)이 아니면 이동 가능 (출구 3도 포함)
        if maze[nx, ny] in [0, 3]:
            maze[x, y] = 0   # 기존 위치는 길로 변경
            maze[nx, ny] = 2  # 새 위치에 플레이어 표시
            move_enemies()    # 적들도 이동
            # 이동 후 적과 충돌 체크
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

# 방향키 입력 받기(w/a/s/d)
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

# 현재 미로 상태 출력 (이모지 맵핑)
emoji_map = {0:"⬜", 1:"⬛", 2:"🧍", 3:"🚪", 4:"👾"}
maze_display = "\n".join("".join(emoji_map[cell] for cell in row) for row in maze)
st.markdown(f"```\n{maze_display}\n```")

# 타이머(경과 시간) 출력 (사이드바)
elapsed = int(time.time() - st.session_state.start_time)
st.sidebar.write(f"⏱️ 경과 시간: {elapsed}초")

# 게임 재시작 버튼: 상태 초기화 후 재실행
if st.button("🔄 게임 다시 시작"):
    st.session_state.maze = init_maze(size)
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.last_key = ""
    st.session_state.enemies = []
    st.experimental_rerun()
