# Creating a Streamlit + Python maze game script and saving it as a file.
# The script will generate a maze in Python, allow movement via Streamlit buttons, and render the maze as an image.

maze_app_code = '''
import streamlit as st
import random
from PIL import Image, ImageDraw

# -----------------------------
# 설정 값
# -----------------------------
CELL_SIZE = 20      # 미로 셀 하나의 크기 (픽셀)
COLS = 20           # 가로 셀 개수
ROWS = 20           # 세로 셀 개수
IMG_WIDTH = COLS * CELL_SIZE
IMG_HEIGHT = ROWS * CELL_SIZE

# 색 정의 (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)   # 플레이어 색
RED = (255, 80, 80)     # 출구 색
GREY = (200, 200, 200)  # 배경 그리드 색

# -----------------------------
# 셀 및 미로 생성용 클래스
# -----------------------------
class Cell:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        # 상하좌우 벽 여부 (True면 벽이 있음)
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def check_neighbors(self, grid):
        neighbors = []
        dirs = [
            ('top',    self.col,     self.row - 1),
            ('right',  self.col + 1, self.row    ),
            ('bottom', self.col,     self.row + 1),
            ('left',   self.col - 1, self.row    ),
        ]
        for direction, nc, nr in dirs:
            if 0 <= nc < COLS and 0 <= nr < ROWS:
                neighbor = grid[nr][nc]
                if not neighbor.visited:
                    neighbors.append(neighbor)
        return neighbors

def remove_walls(a, b):
    dx = a.col - b.col
    dy = a.row - b.row
    if dx == 1:  # b 가 왼쪽
        a.walls['left'] = False
        b.walls['right'] = False
    elif dx == -1:  # b 가 오른쪽
        a.walls['right'] = False
        b.walls['left'] = False
    if dy == 1:  # b 가 위쪽
        a.walls['top'] = False
        b.walls['bottom'] = False
    elif dy == -1:  # b 가 아래쪽
        a.walls['bottom'] = False
        b.walls['top'] = False

def generate_maze():
    # 2차원 리스트로 Cell 객체 생성
    grid = [[Cell(c, r) for c in range(COLS)] for r in range(ROWS)]
    stack = []
    current = grid[0][0]
    current.visited = True

    while True:
        next_cells = current.check_neighbors(grid)
        if next_cells:
            next_cell = random.choice(next_cells)
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
            current.visited = True
        elif stack:
            current = stack.pop()
        else:
            break
    return grid

def draw_maze(grid, player_pos, exit_pos):
    img = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    # 배경 그리드 (희미한 회색 선)
    for r in range(ROWS+1):
        y = r * CELL_SIZE
        draw.line([(0, y), (IMG_WIDTH, y)], fill=GREY, width=1)
    for c in range(COLS+1):
        x = c * CELL_SIZE
        draw.line([(x, 0), (x, IMG_HEIGHT)], fill=GREY, width=1)

    # 벽 그리기
    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            if cell.walls['top']:
                draw.line([(x, y), (x + CELL_SIZE, y)], fill=BLACK, width=2)
            if cell.walls['right']:
                draw.line([(x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE)], fill=BLACK, width=2)
            if cell.walls['bottom']:
                draw.line([(x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE)], fill=BLACK, width=2)
            if cell.walls['left']:
                draw.line([(x, y + CELL_SIZE), (x, y)], fill=BLACK, width=2)

    # 출구 그리기 (빨간 정사각)
    ec, er = exit_pos
    exit_x = ec * CELL_SIZE + CELL_SIZE//4
    exit_y = er * CELL_SIZE + CELL_SIZE//4
    size = CELL_SIZE//2
    draw.rectangle([exit_x, exit_y, exit_x + size, exit_y + size], fill=RED)

    # 플레이어 그리기 (파란 원)
    pc, pr = player_pos
    center_x = pc * CELL_SIZE + CELL_SIZE//2
    center_y = pr * CELL_SIZE + CELL_SIZE//2
    radius = CELL_SIZE//3
    draw.ellipse([(center_x - radius, center_y - radius),
                  (center_x + radius, center_y + radius)], fill=BLUE)

    return img

# -----------------------------
# Streamlit 앱
# -----------------------------
st.title("Python + Streamlit Maze Game")

# 세션 상태 초기화
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.grid = generate_maze()
    st.session_state.player_pos = (0, 0)
    st.session_state.exit_pos = (COLS-1, ROWS-1)
    st.session_state.message = ""

grid = st.session_state.grid
player_pos = st.session_state.player_pos
exit_pos = st.session_state.exit_pos

# 움직임 처리 함수
def move_player(direction):
    pc, pr = st.session_state.player_pos
    grid = st.session_state.grid
    cell = grid[pr][pc]

    if direction == "left":
        if not cell.walls['left']:
            pc -= 1
    elif direction == "right":
        if not cell.walls['right']:
            pc += 1
    elif direction == "up":
        if not cell.walls['top']:
            pr -= 1
    elif direction == "down":
        if not cell.walls['bottom']:
            pr += 1

    # 범위 검사
    pc = max(0, min(COLS-1, pc))
    pr = max(0, min(ROWS-1, pr))
    st.session_state.player_pos = (pc, pr)

    # 출구 확인
    if (pc, pr) == st.session_state.exit_pos:
        st.session_state.message = "🎉 You Escaped! 🎉"
    else:
        st.session_state.message = ""

# 화면 레이아웃
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⯇ Left"):
        move_player("left")
    if st.button("⯆ Down"):
        move_player("down")

with col2:
    maze_img = draw_maze(grid, player_pos, exit_pos)
    st.image(maze_img, caption=st.session_state.message, use_column_width=True)

with col3:
    if st.button("⯅ Up"):
        move_player("up")
    if st.button("⯈ Right"):
        move_player("right")
'''

# 저장 경로
file_path = "/mnt/data/streamlit_maze_combined.py"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(maze_app_code)

file_path
