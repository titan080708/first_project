import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Isaac-like Game in Streamlit", layout="wide")
st.title("Isaac-like Mini Game (Streamlit Embedding)")
st.markdown(
    """
    **조작법**  
    - **WASD**: 플레이어 이동  
    - **방향키(↑↓←→)**: 발사  
    - 적이 자동으로 화면 가장자리에서 스폰되어 플레이어를 추격합니다.  
    - 플레이어 체력(HP)이 0이 되면 게임 오버가 표시됩니다.
    """
)

# ───────────────────────────────────────────────────────────────────────
# 아래 HTML/JS 코드는 Canvas 기반의 간단한 Isaac-like 게임을 구현합니다.
# 플레이어, 벽, 탄환, 적 스폰 및 추격, 충돌 처리를 전부 JavaScript로 작성했습니다.
# Streamlit에서는 이를 components.html을 통해 임베드해서 보여줍니다.
# ───────────────────────────────────────────────────────────────────────

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>Isaac-like Mini Game</title>
  <style>
    body {
      margin: 0;
      overflow: hidden;
    }
    #gameCanvas {
      background: #1e1e1e;
      display: block;
      margin: 0 auto;
      border: 2px solid #444;
    }
    #hpDisplay {
      position: absolute;
      left: 20px;
      top: 20px;
      color: #fff;
      font-family: Arial, sans-serif;
      font-size: 20px;
    }
    #gameOver {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: #ff4444;
      font-family: Arial, sans-serif;
      font-size: 48px;
      display: none;
    }
  </style>
</head>
<body>
  <div id="hpDisplay">HP: 5</div>
  <div id="gameOver">Game Over</div>
  <canvas id="gameCanvas" width="800" height="600"></canvas>
  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const hpDisplay = document.getElementById("hpDisplay");
    const gameOverDiv = document.getElementById("gameOver");

    const SCREEN_WIDTH = 800;
    const SCREEN_HEIGHT = 600;
    const FPS = 60;

    // 플레이어 정보
    const PLAYER_SIZE = 20;
    const PLAYER_SPEED = 3;
    let player = {
      x: SCREEN_WIDTH / 2,
      y: SCREEN_HEIGHT / 2,
      size: PLAYER_SIZE,
      speed: PLAYER_SPEED,
      hp: 5
    };

    // 벽(사각형) 배열
    const walls = [
      // 화면 테두리
      { x: 0, y: 0, w: SCREEN_WIDTH, h: 20 },             // 상단
      { x: 0, y: SCREEN_HEIGHT - 20, w: SCREEN_WIDTH, h: 20 }, // 하단
      { x: 0, y: 0, w: 20, h: SCREEN_HEIGHT },             // 좌측
      { x: SCREEN_WIDTH - 20, y: 0, w: 20, h: SCREEN_HEIGHT }, // 우측
      // 방 가운데 가로 벽 두 개 (예시)
      { x: 200, y: 150, w: 400, h: 20 },
      { x: 200, y: 430, w: 400, h: 20 }
    ];

    // 탄환, 적 리스트
    let bullets = [];
    let enemies = [];

    // 적 스폰 간격 (ms)
    const ENEMY_SPAWN_INTERVAL = 2000;

    // 키 입력 상태 추적
    let keys = {};
    window.addEventListener("keydown", (e) => {
      keys[e.code] = true;
    });
    window.addEventListener("keyup", (e) => {
      keys[e.code] = false;
    });

    // 거리 계산
    function getDistance(ax, ay, bx, by) {
      return Math.hypot(bx - ax, by - ay);
    }

    // 벽과 충돌 감지를 위해 사각형 충돌 검사
    function rectsOverlap(r1, r2) {
      return !(
        r1.x + r1.w < r2.x ||
        r2.x + r2.w < r1.x ||
        r1.y + r1.h < r2.y ||
        r2.y + r2.h < r1.y
      );
    }

    // 플레이어 이동 처리
    function movePlayer() {
      let dx = 0,
        dy = 0;
      if (keys["KeyW"]) dy -= player.speed;
      if (keys["KeyS"]) dy += player.speed;
      if (keys["KeyA"]) dx -= player.speed;
      if (keys["KeyD"]) dx += player.speed;

      // X축 가상의 충돌 검사
      let nextX = player.x + dx;
      let playerRectX = { x: nextX - player.size / 2, y: player.y - player.size / 2, w: player.size, h: player.size };
      let collideX = walls.some((w) => rectsOverlap(playerRectX, w));
      if (!collideX) player.x = nextX;

      // Y축 가상의 충돌 검사
      let nextY = player.y + dy;
      let playerRectY = { x: player.x - player.size / 2, y: nextY - player.size / 2, w: player.size, h: player.size };
      let collideY = walls.some((w) => rectsOverlap(playerRectY, w));
      if (!collideY) player.y = nextY;
    }

    // 탄환 객체 생성 함수
    function shootBullet(dirX, dirY) {
      // 방향 벡터 정규화
      let mag = Math.hypot(dirX, dirY);
      if (mag === 0) {
        dirX = 0; dirY = -1;
      } else {
        dirX /= mag; dirY /= mag;
      }
      bullets.push({
        x: player.x,
        y: player.y,
        dx: dirX * 7,
        dy: dirY * 7,
        size: 6
      });
    }

    // 적 생성 함수 (화면 가장자리 랜덤 위치)
    function spawnEnemy() {
      let side = ["top", "bottom", "left", "right"][Math.floor(Math.random() * 4)];
      let ex, ey;
      if (side === "top") {
        ex = Math.random() * (SCREEN_WIDTH - 100) + 50;
        ey = 30;
      } else if (side === "bottom") {
        ex = Math.random() * (SCREEN_WIDTH - 100) + 50;
        ey = SCREEN_HEIGHT - 30;
      } else if (side === "left") {
        ex = 30;
        ey = Math.random() * (SCREEN_HEIGHT - 100) + 50;
      } else {
        ex = SCREEN_WIDTH - 30;
        ey = Math.random() * (SCREEN_HEIGHT - 100) + 50;
      }
      enemies.push({
        x: ex,
        y: ey,
        size: 18,
        speed: 1.5,
        hp: 3
      });
    }

    // 게임 오버 처리
    function gameOver() {
      gameOverDiv.style.display = "block";
    }

    // 주요 업데이트 함수
    let lastSpawn = Date.now();
    function update() {
      if (player.hp <= 0) return;

      // 플레이어 이동
      movePlayer();

      // 탄환 발사 (새 프레임마다 화살표 키가 눌린 경우)
      if (keys["ArrowUp"])    shootBullet(0, -1);
      if (keys["ArrowDown"])  shootBullet(0, 1);
      if (keys["ArrowLeft"])  shootBullet(-1, 0);
      if (keys["ArrowRight"]) shootBullet(1, 0);

      // 탄환 업데이트
      bullets = bullets.filter(b => {
        b.x += b.dx;
        b.y += b.dy;
        // 화면 밖으로 나가면 제거
        return !(b.x < -b.size || b.x > SCREEN_WIDTH + b.size || b.y < -b.size || b.y > SCREEN_HEIGHT + b.size);
      });

      // 적 스폰 간격 체크
      if (Date.now() - lastSpawn > ENEMY_SPAWN_INTERVAL) {
        spawnEnemy();
        lastSpawn = Date.now();
      }

      // 적 업데이트 (플레이어 추격 및 충돌 검사)
      enemies = enemies.filter(e => {
        // 플레이어 방향으로 이동
        let dx = player.x - e.x;
        let dy = player.y - e.y;
        let dist = Math.hypot(dx, dy);
        if (dist !== 0) {
          dx /= dist; dy /= dist;
        }
        // X축 충돌 체크
        let nextX = e.x + dx * e.speed;
        let eRectX = { x: nextX - e.size / 2, y: e.y - e.size / 2, w: e.size, h: e.size };
        if (!walls.some(w => rectsOverlap(eRectX, w))) {
          e.x = nextX;
        }
        // Y축 충돌 체크
        let nextY = e.y + dy * e.speed;
        let eRectY = { x: e.x - e.size / 2, y: nextY - e.size / 2, w: e.size, h: e.size };
        if (!walls.some(w => rectsOverlap(eRectY, w))) {
          e.y = nextY;
        }

        // 플레이어와 충돌 검사
        let playerRect = { x: player.x - player.size / 2, y: player.y - player.size / 2, w: player.size, h: player.size };
        let enemyRect  = { x: e.x - e.size / 2,  y: e.y - e.size / 2,   w: e.size,   h: e.size };
        if (rectsOverlap(playerRect, enemyRect)) {
          player.hp -= 1;
          hpDisplay.innerText = "HP: " + player.hp;
          return false; // 충돌 즉시 적 파괴
        }
        return true;
      });

      // 탄환 ↔ 적 충돌 검사
      bullets.forEach((b, bi) => {
        enemies.forEach((e, ei) => {
          let bRect = { x: b.x - b.size / 2, y: b.y - b.size / 2, w: b.size, h: b.size };
          let eRect = { x: e.x - e.size / 2, y: e.y - e.size / 2, w: e.size, h: e.size };
          if (rectsOverlap(bRect, eRect)) {
            e.hp -= 1;
            if (e.hp <= 0) {
              enemies.splice(ei, 1);
            }
            bullets.splice(bi, 1);
          }
        });
      });

      if (player.hp <= 0) {
        gameOver();
      }
    }

    // 그리기 함수
    function draw() {
      // 배경
      ctx.fillStyle = "#1e1e1e";
      ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

      // 벽 그리기
      ctx.fillStyle = "#555";
      walls.forEach(w => {
        ctx.fillRect(w.x, w.y, w.w, w.h);
      });

      // 탄환 그리기
      ctx.fillStyle = "#f0f000";
      bullets.forEach(b => {
        ctx.fillRect(b.x - b.size / 2, b.y - b.size / 2, b.size, b.size);
      });

      // 적 그리기
      ctx.fillStyle = "#e03030";
      enemies.forEach(e => {
        ctx.fillRect(e.x - e.size / 2, e.y - e.size / 2, e.size, e.size);
      });

      // 플레이어 그리기
      ctx.fillStyle = "#32c8dc";
      ctx.fillRect(player.x - player.size / 2, player.y - player.size / 2, player.size, player.size);
    }

    // 게임 루프
    function gameLoop() {
      update();
      draw();
      requestAnimationFrame(gameLoop);
    }

    // 시작
    hpDisplay.innerText = "HP: " + player.hp;
    gameLoop();
  </script>
</body>
</html>
"""

# Streamlit 페이지에 HTML/JS 임베드
components.html(html_code, width=820, height=640, scrolling=False)
"""

