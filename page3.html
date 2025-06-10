<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Mini RTS with All Features</title>
  <style>
    body { background: #222; color: #fff; font-family: Arial, sans-serif; text-align: center; }
    #ui { margin-bottom: 10px; }
    #buildBtn { padding: 5px 10px; margin-right: 20px; }
    #resCount { font-size: 16px; }
    #game { background: #1e1e1e; display: block; margin: 0 auto; border: 1px solid #444; }
  </style>
</head>
<body>
  <div id="ui">
    <button id="buildBtn">Build (Cost: 10)</button>
    <span id="resCount">Resources: 0</span>
  </div>
  <canvas id="game" width="800" height="600"></canvas>

  <script>
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d');

  const RES_COST = 10; // building cost
  let resources = 0;
  let isBuildingMode = false;

  document.getElementById('buildBtn').addEventListener('click', () => {
    if (resources >= RES_COST) {
      isBuildingMode = true;
    }
  });

  // Game entities
  const units = [];
  const enemyUnits = [];
  const resourcesNodes = [];
  const buildings = [];
  let selectedUnits = [];

  // Create some friendly units
  for (let i = 0; i < 5; i++) {
    units.push({
      x: 100 + i * 40,
      y: 500,
      size: 20,
      speed: 1.5,
      target: null,
      state: 'idle', // idle, moving, gathering, attacking
      gatherTarget: null,
      attackTarget: null,
      gatherCooldown: 0
    });
  }

  // Create some enemy units
  for (let i = 0; i < 3; i++) {
    enemyUnits.push({
      x: 600 + i * 50,
      y: 100 + i * 50,
      size: 20,
      hp: 50,
    });
  }

  // Create some resource nodes
  for (let i = 0; i < 4; i++) {
    resourcesNodes.push({
      x: 200 + i * 100,
      y: 200,
      size: 15,
      amount: 50
    });
  }

  // Mouse selection variables
  let isDragging = false;
  const dragStart = { x: 0, y: 0 };
  const dragEnd = { x: 0, y: 0 };

  canvas.addEventListener('mousedown', e => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    // If in building mode, place a building
    if (isBuildingMode) {
      buildings.push({ x: mx, y: my, size: 30 });
      resources -= RES_COST;
      updateResourceUI();
      isBuildingMode = false;
      return;
    }

    // Begin drag for selection
    isDragging = true;
    dragStart.x = mx;
    dragStart.y = my;
    dragEnd.x = mx;
    dragEnd.y = my;
  });

  canvas.addEventListener('mousemove', e => {
    if (!isDragging) return;
    const rect = canvas.getBoundingClientRect();
    dragEnd.x = e.clientX - rect.left;
    dragEnd.y = e.clientY - rect.top;
  });

  canvas.addEventListener('mouseup', e => {
    if (!isDragging) return;
    isDragging = false;
    const x1 = Math.min(dragStart.x, dragEnd.x);
    const y1 = Math.min(dragStart.y, dragEnd.y);
    const x2 = Math.max(dragStart.x, dragEnd.x);
    const y2 = Math.max(dragStart.y, dragEnd.y);

    selectedUnits = [];
    for (const u of units) {
      if (u.x > x1 && u.x < x2 && u.y > y1 && u.y < y2) {
        selectedUnits.push(u);
      }
    }

    // If click without drag (small area) and clicked on unit, select single unit
    if (Math.hypot(dragEnd.x - dragStart.x, dragEnd.y - dragStart.y) < 5) {
      const clickedUnit = units.find(u => {
        return dragEnd.x > u.x - u.size && dragEnd.x < u.x + u.size &&
               dragEnd.y > u.y - u.size && dragEnd.y < u.y + u.size;
      });
      if (clickedUnit) selectedUnits = [clickedUnit];
    }
  });

  // Right-click to issue commands
  canvas.addEventListener('contextmenu', e => {
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    // Check if right-click on resource node
    const resNode = resourcesNodes.find(r => Math.hypot(mx - r.x, my - r.y) < r.size);
    if (resNode) {
      for (const u of selectedUnits) {
        u.state = 'gather';
        u.gatherTarget = resNode;
        u.attackTarget = null;
      }
      return;
    }

    // Check if right-click on enemy unit
    const enemy = enemyUnits.find(eu => mx > eu.x - eu.size && mx < eu.x + eu.size &&
                                      my > eu.y - eu.size && my < eu.y + eu.size);
    if (enemy) {
      for (const u of selectedUnits) {
        u.state = 'attack';
        u.attackTarget = enemy;
        u.gatherTarget = null;
      }
      return;
    }

    // Otherwise, move command
    for (const u of selectedUnits) {
      u.state = 'move';
      u.target = { x: mx, y: my };
      u.gatherTarget = null;
      u.attackTarget = null;
    }
  });

  function updateResourceUI() {
    document.getElementById('resCount').innerText = `Resources: ${resources}`;
  }

  function update() {
    // Friendly units logic
    units.forEach(u => {
      if (u.state === 'move' && u.target) {
        const dx = u.target.x - u.x;
        const dy = u.target.y - u.y;
        const dist = Math.hypot(dx, dy);
        if (dist > u.speed) {
          u.x += (dx / dist) * u.speed;
          u.y += (dy / dist) * u.speed;
        } else {
          u.x = u.target.x;
          u.y = u.target.y;
          u.target = null;
          u.state = 'idle';
        }
      }
      
      if (u.state === 'gather' && u.gatherTarget) {
        const gt = u.gatherTarget;
        const dx = gt.x - u.x;
        const dy = gt.y - u.y;
        const dist = Math.hypot(dx, dy);
        if (dist > u.speed) {
          u.x += (dx / dist) * u.speed;
          u.y += (dy / dist) * u.speed;
        } else {
          // gathered
          u.gatherCooldown = (u.gatherCooldown || 0) + 1;
          if (u.gatherCooldown > 60) { // gather interval
            if (gt.amount > 0) {
              gt.amount -= 5;
              resources += 5;
              updateResourceUI();
            }
            u.gatherCooldown = 0;
          }
          if (gt.amount <= 0) {
            const idx = resourcesNodes.indexOf(gt);
            if (idx > -1) resourcesNodes.splice(idx, 1);
            u.state = 'idle';
            u.gatherTarget = null;
          }
        }
      }
      
      if (u.state === 'attack' && u.attackTarget) {
        const at = u.attackTarget;
        const dx = at.x - u.x;
        const dy = at.y - u.y;
        const dist = Math.hypot(dx, dy);
        if (dist > u.speed + at.size) {
          u.x += (dx / dist) * u.speed;
          u.y += (dy / dist) * u.speed;
        } else {
          // deal damage
          at.hp -= 0.5;
          if (at.hp <= 0) {
            const idx = enemyUnits.indexOf(at);
            if (idx > -1) enemyUnits.splice(idx, 1);
            u.state = 'idle';
            u.attackTarget = null;
          }
        }
      }
    });

    // Simple enemy behavior: idle or wander
    enemyUnits.forEach(eu => {
      // Could add wander logic; skip for simplicity
    });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw resource nodes
    resourcesNodes.forEach(r => {
      ctx.fillStyle = 'gold';
      ctx.beginPath();
      ctx.arc(r.x, r.y, r.size, 0, Math.PI * 2);
      ctx.fill();
    });

    // Draw buildings
    buildings.forEach(b => {
      ctx.fillStyle = 'gray';
      ctx.fillRect(b.x - b.size / 2, b.y - b.size / 2, b.size, b.size);
    });

    // Draw enemy units
    enemyUnits.forEach(eu => {
      ctx.fillStyle = 'red';
      ctx.fillRect(eu.x - eu.size / 2, eu.y - eu.size / 2, eu.size, eu.size);
    });

    // Draw friendly units
    units.forEach(u => {
      ctx.fillStyle = selectedUnits.includes(u) ? 'lime' : 'cyan';
      ctx.fillRect(u.x - u.size / 2, u.y - u.size / 2, u.size, u.size);
    });

    // Draw drag selection box
    if (isDragging) {
      ctx.strokeStyle = 'white';
      ctx.strokeRect(
        Math.min(dragStart.x, dragEnd.x),
        Math.min(dragStart.y, dragEnd.y),
        Math.abs(dragEnd.x - dragStart.x),
        Math.abs(dragEnd.y - dragStart.y)
      );
    }

    // If building mode, show indicator
    if (isBuildingMode) {
      canvas.style.cursor = 'crosshair';
    } else {
      canvas.style.cursor = 'default';
    }
  }

  function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
  }

  updateResourceUI();
  gameLoop();
  </script>
</body>
</html>
