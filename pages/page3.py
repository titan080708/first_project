import streamlit as st
import random
import sys

# -----------------------------
# 클래스 정의
# -----------------------------
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.next_level_exp = 100
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 10
        self.defense = 5
        self.gold = 50
        self.inventory = {"Potion": 3}  # 시작할 때 포션 3개

    def is_alive(self):
        return self.hp > 0

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.next_level_exp:
            self.level_up()

    def level_up(self):
        self.exp -= self.next_level_exp
        self.level += 1
        self.next_level_exp = int(self.next_level_exp * 1.5)
        self.max_hp = int(self.max_hp * 1.2)
        self.attack = int(self.attack * 1.2)
        self.defense = int(self.defense * 1.1)
        self.hp = self.max_hp

    def use_potion(self):
        if self.inventory.get("Potion", 0) > 0:
            self.inventory["Potion"] -= 1
            heal_amount = int(self.max_hp * 0.3)
            self.hp = min(self.max_hp, self.hp + heal_amount)
            return f"▶ {self.name} used a Potion and recovered {heal_amount} HP!"
        else:
            return "▶ You have no Potions!"

class Enemy:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.max_hp = level * 50
        self.hp = self.max_hp
        self.attack = level * 8
        self.defense = level * 4
        self.exp_drop = level * 50
        self.gold_drop = level * 20

    def is_alive(self):
        return self.hp > 0

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.player = None
    st.session_state.quest_status = {"started": False, "completed": False, "rewarded": False}
    st.session_state.location = None
    st.session_state.in_battle = False
    st.session_state.enemy = None
    st.session_state.forest_state = None
    st.session_state.message = ""

# -----------------------------
# 플레이어 생성 화면
# -----------------------------
if st.session_state.player is None:
    st.title("Text RPG (Streamlit)")
    name = st.text_input("Enter your character's name:", "")
    if st.button("Start Game") and name.strip():
        st.session_state.player = Player(name.strip())
        st.session_state.location = "Town"
        st.experimental_rerun()
    st.stop()

# -----------------------------
# 세션 상태 가져오기
# -----------------------------
player = st.session_state.player
quest_status = st.session_state.quest_status
location = st.session_state.location
in_battle = st.session_state.in_battle
enemy = st.session_state.enemy
forest_state = st.session_state.forest_state
message = st.session_state.message

# -----------------------------
# 상태 표시 함수
# -----------------------------
def show_status():
    st.subheader(f"{player.name}'s Status")
    st.write(f"Level: {player.level} | EXP: {player.exp}/{player.next_level_exp}")
    st.write(f"HP: {player.hp}/{player.max_hp} | Attack: {player.attack} | Defense: {player.defense}")
    st.write(f"Gold: {player.gold}")
    st.write(f"Potions: {player.inventory.get('Potion', 0)}")
    st.markdown("---")

# -----------------------------
# 전투 처리 함수
# -----------------------------
def do_battle(action):
    player = st.session_state.player
    enemy = st.session_state.enemy

    if action == "Attack":
        dmg = max(0, player.attack - enemy.defense + random.randint(-5, 5))
        enemy.hp = max(0, enemy.hp - dmg)
        st.session_state.message = f"▶ You attack {enemy.name} for {dmg} damage. (Enemy HP: {enemy.hp}/{enemy.max_hp})"
        if not enemy.is_alive():
            st.session_state.message += f"\\n▶ You defeated {enemy.name}!"
            player.gain_exp(enemy.exp_drop)
            player.gold += enemy.gold_drop
            st.session_state.message += f" Gained {enemy.exp_drop} EXP and {enemy.gold_drop} gold."
            if enemy.name == "Goblin King":
                st.session_state.quest_status["completed"] = True
            st.session_state.in_battle = False
            st.session_state.enemy = None
            return

    elif action == "Use Potion":
        msg = player.use_potion()
        st.session_state.message = msg

    elif action == "Run":
        if random.random() < 0.5:
            st.session_state.message = "▶ You successfully ran away!"
            st.session_state.in_battle = False
            st.session_state.enemy = None
            return
        else:
            st.session_state.message = "▶ Failed to run away!"

    # 적 턴
    if enemy.is_alive():
        edmg = max(0, enemy.attack - player.defense + random.randint(-5, 5))
        player.hp = max(0, player.hp - edmg)
        st.session_state.message += f"\\n▶ {enemy.name} attacks you for {edmg} damage. (Your HP: {player.hp}/{player.max_hp})"
        if not player.is_alive():
            st.session_state.message += "\\n▶ You were defeated! Game Over."
            st.write(st.session_state.message)
            st.stop()

# -----------------------------
# 마을 UI
# -----------------------------
def visit_town():
    st.header("Town")
    if st.button("Talk to NPC"):
        if not quest_status["started"]:
            st.session_state.message = "NPC: 'Brave adventurer! A Goblin King is terrorizing the Forest. Defeat him for 100 gold!'"
            quest_status["started"] = True
        elif quest_status["completed"] and not quest_status["rewarded"]:
            st.session_state.message = "NPC: 'Thank you for defeating the Goblin King! Here's 100 gold!'"
            player.gold += 100
            st.session_state.quest_status["rewarded"] = True
        elif quest_status["rewarded"]:
            st.session_state.message = "NPC: 'We are forever in your debt, hero!'"
        else:
            st.session_state.message = "NPC: 'The Goblin King still awaits you in the Forest.'"

    if st.button("Visit Shop"):
        visit_shop()

    if st.button("Rest at Inn"):
        cost = 10
        if player.gold >= cost:
            player.gold -= cost
            player.hp = player.max_hp
            st.session_state.message = f"▶ You rested at the inn. HP fully recovered. (Gold: {player.gold})"
        else:
            st.session_state.message = "▶ Not enough gold to rest."

    if st.button("Go to Forest"):
        st.session_state.location = "Forest"
        st.session_state.forest_state = "start"
        st.experimental_rerun()

    if st.button("View Status"):
        pass  # 상태는 상단에 항상 표시됨

# -----------------------------
# 상점 UI
# -----------------------------
def visit_shop():
    st.subheader("Shop")
    st.write("Potion (20 gold)")
    if st.button("Buy Potion"):
        if player.gold >= 20:
            player.gold -= 20
            player.inventory["Potion"] = player.inventory.get("Potion", 0) + 1
            st.session_state.message = "▶ Bought a Potion."
        else:
            st.session_state.message = "▶ Not enough gold!"

# -----------------------------
# 숲 UI
# -----------------------------
def visit_forest():
    if st.session_state.forest_state == "start":
        if quest_status["started"] and not quest_status["completed"]:
            st.session_state.enemy = Enemy("Goblin King", level=3)
            st.session_state.in_battle = True
            st.session_state.forest_state = None
        else:
            if random.random() < 0.3:
                st.session_state.message = "▶ No enemies encountered. You explore peacefully."
                st.session_state.forest_state = "explored"
            else:
                lvl = 1 if not quest_status["started"] else 2
                st.session_state.enemy = Enemy("Goblin", level=lvl)
                st.session_state.in_battle = True
                st.session_state.forest_state = None

    elif st.session_state.forest_state == "explored":
        st.write("▶ You explored the forest peacefully.")
        if st.button("Return to Town"):
            st.session_state.location = "Town"
            st.session_state.forest_state = None
            st.experimental_rerun()

# -----------------------------
# 메인 화면
# -----------------------------
st.title("Text RPG (Streamlit)")
show_status()

if st.session_state.message:
    st.write(st.session_state.message)

# 전투 중이라면 전투 UI 표시
if in_battle and st.session_state.enemy:
    enemy = st.session_state.enemy
    st.header(f"Battle: {enemy.name} (Lv {enemy.level})")
    st.write(f"Enemy HP: {enemy.hp}/{enemy.max_hp} | Attack: {enemy.attack} | Defense: {enemy.defense}")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Attack"):
            do_battle("Attack")
            st.experimental_rerun()
    with col2:
        if st.button("Use Potion"):
            do_battle("Use Potion")
            st.experimental_rerun()
    with col3:
        if st.button("Run"):
            do_battle("Run")
            st.experimental_rerun()

# 전투 중이 아니면 위치에 따른 UI 표시
elif location == "Town":
    visit_town()

elif location == "Forest":
    visit_forest()
