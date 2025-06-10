import pygame
import sys
import math

# -----------------------------
# 설정값
# -----------------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

UNIT_SIZE = 20
UNIT_SPEED = 1.5

ENEMY_SIZE = 20
ENEMY_HP = 50

RESOURCE_NODE_SIZE = 15
RESOURCE_NODE_AMOUNT = 50

BUILDING_SIZE = 30
BUILD_COST = 10

FONT_SIZE = 24

# -----------------------------
# 유틸 함수
# -----------------------------
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

# -----------------------------
# 클래스 정의
# -----------------------------
class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = UNIT_SIZE
        self.speed = UNIT_SPEED

        # 상태 관리: 'idle', 'move', 'gather', 'attack'
        self.state = 'idle'
        self.target_pos = None        # {'x':…, 'y':…}
        self.gather_target = None     # ResourceNode 인스턴스
        self.attack_target = None     # EnemyUnit 인스턴스
        self.gather_cooldown = 0

    def update(self, dt, resources, resource_nodes, enemy_units):
        # --- 이동 상태 ---
        if self.state == 'move' and self.target_pos:
            tx, ty = self.target_pos
            dx, dy = tx - self.x, ty - self.y
            dist = math.hypot(dx, dy)
            if dist > self.speed:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
            else:
                # 목표 위치 도착
                self.x = tx
                self.y = ty
                self.target_pos = None
                self.state = 'idle'

        # --- 자원 채집 상태 ---
        elif self.state == 'gather' and self.gather_target:
            node = self.gather_target
            dx, dy = node.x - self.x, node.y - self.y
            dist = math.hypot(dx, dy)
            if dist > self.speed:
                # 자원 노드로 이동
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
            else:
                # 노드에 도착 → 채집 쿨다운
                self.gather_cooldown += 1
                if self.gather_cooldown >= FPS:   # 약 1초마다 채집
                    if node.amount > 0:
                        node.amount -= 5
                        resources[0] += 5
                    self.gather_cooldown = 0
                # 만약 자원이 바닥나면 idle
                if node.amount <= 0:
                    if node in resource_nodes:
                        resource_nodes.remove(node)
                    self.state = 'idle'
                    self.gather_target = None

        # --- 공격 상태 ---
        elif self.state == 'attack' and self.attack_target:
            enemy = self.attack_target
            dx, dy = enemy.x - self.x, enemy.y - self.y
            dist = math.hypot(dx, dy)
            if dist > self.speed + enemy.size:
                # 적에게 다가가기
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
            else:
                # 공격해서 HP 감소
                enemy.hp -= 0.5
                if enemy.hp <= 0:
                    if enemy in enemy_units:
                        enemy_units.remove(enemy)
                    self.state = 'idle'
                    self.attack_target = None

    def draw(self, surface, is_selected):
        color = (0, 255, 0) if is_selected else (0, 200, 255)
        rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size)
        pygame.draw.rect(surface, color, rect)

class EnemyUnit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = ENEMY_SIZE
        self.hp = ENEMY_HP

    def draw(self, surface):
        rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size)
        pygame.draw.rect(surface, (255, 50, 50), rect)

class ResourceNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = RESOURCE_NODE_SIZE
        self.amount = RESOURCE_NODE_AMOUNT

    def draw(self, surface):
        pygame.draw.circle(surface, (212, 175, 55), (int(self.x), int(self.y)), self.size)

class Building:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = BUILDING_SIZE

    def draw(self, surface):
        rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size)
        pygame.draw.rect(surface, (100, 100, 100), rect)

# -----------------------------
# 초기화
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini RTS (Python/Pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, FONT_SIZE)

# 게임 객체들 생성
friendly_units = []
enemy_units = []
resource_nodes = []
buildings = []
selected_units = []

# 자원 카운트 (mutable int 형태로 리스트에 담아서 참조)
resources = [0]

# 친선 유닛 5개 생성
for i in range(5):
    u = Unit(100 + i * 40, 500)
    friendly_units.append(u)

# 적 유닛 3개 생성
for i in range(3):
    eu = EnemyUnit(600 + i * 50, 100 + i * 50)
    enemy_units.append(eu)

# 자원 노드 4개 생성
for i in range(4):
    rn = ResourceNode(200 + i * 100, 200)
    resource_nodes.append(rn)

# 드래그 선택용 변수
is_dragging = False
drag_start = (0, 0)
drag_end = (0, 0)

# 건설 모드 플래그
is_build_mode = False

# -----------------------------
# 메인 루프
# -----------------------------
running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # 초 단위 델타타임

    # -----------------------------
    # 이벤트 처리
    # -----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 마우스 왼쪽 버튼 눌렀을 때
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()

            # 건설 모드일 때
            if is_build_mode:
                if resources[0] >= BUILD_COST:
                    # 건물 배치
                    buildings.append(Building(mx, my))
                    resources[0] -= BUILD_COST
                is_build_mode = False
            else:
                # 드래그 시작
                is_dragging = True
                drag_start = (mx, my)
                drag_end = (mx, my)

        # 마우스 이동
        elif event.type == pygame.MOUSEMOTION and is_dragging:
            drag_end = pygame.mouse.get_pos()

        # 마우스 왼쪽 버튼 뗄 때
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and is_dragging:
            is_dragging = False
            x1, y1 = drag_start
            x2, y2 = drag_end
            left = min(x1, x2); right = max(x1, x2)
            top = min(y1, y2); bottom = max(y1, y2)

            # 선택 초기화
            selected_units.clear()

            # 드래그 범위가 작으면 “클릭”으로 간주하여
            # 클릭 위치에 유닛이 있으면 단일 선택
            if math.hypot(x2 - x1, y2 - y1) < 5:
                clicked = False
                for u in friendly_units:
                    if left < u.x < right and top < u.y < bottom:
                        selected_units = [u]
                        clicked = True
                        break
                if not clicked:
                    selected_units.clear()
            else:
                # 드래그 박스로 다중 선택
                for u in friendly_units:
                    if left < u.x < right and top < u.y < bottom:
                        selected_units.append(u)

        # 마우스 오른쪽 버튼 (명령)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = pygame.mouse.get_pos()

            # 클릭한 지점에 자원 노드가 있는지 체크
            clicked_node = None
            for node in resource_nodes:
                if distance((mx, my), (node.x, node.y)) < node.size:
                    clicked_node = node
                    break

            # 클릭한 지점에 적이 있는지 체크
            clicked_enemy = None
            for eu in enemy_units:
                if (eu.x - eu.size/2 < mx < eu.x + eu.size/2 and
                    eu.y - eu.size/2 < my < eu.y + eu.size/2):
                    clicked_enemy = eu
                    break

            # 선택된 유닛들에 상태 부여
            for u in selected_units:
                if clicked_node:
                    u.state = 'gather'
                    u.gather_target = clicked_node
                    u.attack_target = None
                    u.target_pos = None
                elif clicked_enemy:
                    u.state = 'attack'
                    u.attack_target = clicked_enemy
                    u.gather_target = None
                    u.target_pos = None
                else:
                    u.state = 'move'
                    u.target_pos = {'x': mx, 'y': my}
                    u.gather_target = None
                    u.attack_target = None

        # 키보드 입력 (건설 모드 진입: B)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                is_build_mode = True

    # -----------------------------
    # 게임 로직 업데이트
    # -----------------------------
    for u in friendly_units:
        u.update(dt, resources, resource_nodes, enemy_units)

    # -----------------------------
    # 화면 그리기
    # -----------------------------
    screen.fill((30, 30, 30))

    # 자원 노드 그리기
    for node in resource_nodes:
        node.draw(screen)

    # 건물 그리기
    for b in buildings:
        b.draw(screen)

    # 적 유닛 그리기
    for eu in enemy_units:
        eu.draw(screen)

    # 유닛 그리기 (선택 여부에 따라 색상 다름)
    for u in friendly_units:
        u.draw(screen, u in selected_units)

    # 드래그 박스 그리기
    if is_dragging:
        x1, y1 = drag_start
        x2, y2 = drag_end
        left = min(x1, x2); top = min(y1, y2)
        width = abs(x2 - x1); height = abs(y2 - y1)
        pygame.draw.rect(screen, (200, 200, 200), (left, top, width, height), 1)

    # 자원 개수 텍스트 표시
    text_surf = font.render(f"Resources: {resources[0]}", True, (255, 255, 255))
    screen.blit(text_surf, (10, 10))

    # 건설 모드 안내 텍스트
    if is_build_mode:
        info_surf = font.render("Building Mode: Left-Click to place (Cost: 10)", True, (255, 255, 0))
        screen.blit(info_surf, (SCREEN_WIDTH//2 - info_surf.get_width()//2, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
