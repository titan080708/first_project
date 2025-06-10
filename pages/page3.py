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
        self.inventory = {"Potion": 3}  # 시작 시 포션 3개 보유

    def is_alive(self):
        return self.hp > 0

    def gain_exp(self, amount):
        self.exp += amount
        print(f"\n▶ You gained {amount} EXP.")
        while self.exp >= self.next_level_exp:
            self.level_up()

    def level_up(self):
        self.exp -= self.next_level_exp
        self.level += 1
        # 다음 레벨업에 필요한 경험치 증가
        self.next_level_exp = int(self.next_level_exp * 1.5)
        # 능력치 상승
        self.max_hp = int(self.max_hp * 1.2)
        self.attack = int(self.attack * 1.2)
        self.defense = int(self.defense * 1.1)
        self.hp = self.max_hp
        print(f"\n*** Congratulations! You reached level {self.level}! ***")
        print(f"   ▶ New Stats → HP: {self.max_hp}, Attack: {self.attack}, Defense: {self.defense}\n")

    def use_potion(self):
        if self.inventory.get("Potion", 0) > 0:
            self.inventory["Potion"] -= 1
            heal_amount = int(self.max_hp * 0.3)
            self.hp = min(self.max_hp, self.hp + heal_amount)
            print(f"\n▶ You used a Potion and recovered {heal_amount} HP. (HP: {self.hp}/{self.max_hp})")
        else:
            print("\n▶ You have no Potions!")

    def show_status(self):
        print(f"\n-- {self.name}'s Status --")
        print(f" Level: {self.level} | EXP: {self.exp}/{self.next_level_exp}")
        print(f" HP: {self.hp}/{self.max_hp} | Attack: {self.attack} | Defense: {self.defense}")
        print(f" Gold: {self.gold}")
        print(f" Inventory: {self.inventory}")
        print("--------------------------\n")


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

    def show_stats(self):
        print(f"\n-- {self.name} (Lv {self.level}) --")
        print(f" HP: {self.hp}/{self.max_hp} | Attack: {self.attack} | Defense: {self.defense}")
        print("--------------------------\n")


# -----------------------------
# 전투 함수
# -----------------------------
def battle(player, enemy):
    print(f"\n▶ A wild {enemy.name} appeared!")
    enemy.show_stats()

    while player.is_alive() and enemy.is_alive():
        print("Choose action: [1] Attack  [2] Use Potion  [3] Run")
        choice = input("> ").strip()

        if choice == "1":
            # 플레이어 공격
            damage = max(0, player.attack - enemy.defense + random.randint(-5, 5))
            enemy.hp = max(0, enemy.hp - damage)
            print(f"▶ You attack {enemy.name} for {damage} damage. (Enemy HP: {enemy.hp}/{enemy.max_hp})")

            if not enemy.is_alive():
                print(f"\n▶ You defeated {enemy.name}!")
                player.gain_exp(enemy.exp_drop)
                player.gold += enemy.gold_drop
                print(f"▶ You found {enemy.gold_drop} gold. (Gold: {player.gold})\n")
                return True

        elif choice == "2":
            player.use_potion()

        elif choice == "3":
            # 도망 성공 확률 50%
            if random.random() < 0.5:
                print("\n▶ You successfully ran away!")
                return False
            else:
                print("\n▶ Failed to run away!")

        else:
            print("\n▶ Invalid choice. Try again.")

        # 적 턴
        if enemy.is_alive():
            damage = max(0, enemy.attack - player.defense + random.randint(-5, 5))
            player.hp = max(0, player.hp - damage)
            print(f"▶ {enemy.name} attacks you for {damage} damage. (Your HP: {player.hp}/{player.max_hp})")
            if not player.is_alive():
                print("\n▶ You were defeated! Game Over.")
                sys.exit()

    return False


# -----------------------------
# 마을(Town) 및 숲(Forest) 로직
# -----------------------------
def visit_town(player, quest_status):
    print("\n▶ You are in the Town.")
    print("Options: [1] Talk to NPC  [2] Visit Shop  [3] Rest at Inn  [4] Go to Forest  [5] View Status")
    choice = input("> ").strip()

    if choice == "1":
        # NPC 대화 및 퀘스트 진행
        if not quest_status.get("started"):
            print("\nNPC: 'Brave adventurer! Can you help us? A Goblin King is terrorizing the Forest.'")
            print("NPC: 'Defeat the Goblin King and you shall be rewarded with 100 gold!'")
            quest_status["started"] = True

        elif quest_status.get("completed") and not quest_status.get("rewarded"):
            print("\nNPC: 'Thank you for defeating the Goblin King! Here's your reward.'")
            player.gold += 100
            print(f"▶ You received 100 gold! (Gold: {player.gold})")
            quest_status["rewarded"] = True

        elif quest_status.get("rewarded"):
            print("\nNPC: 'We are forever in your debt, hero!'")

        else:
            print("\nNPC: 'The Goblin King still awaits you in the Forest.'")

    elif choice == "2":
        visit_shop(player)

    elif choice == "3":
        # 여관 휴식: 골드 10 소모 → HP 전부 회복
        cost = 10
        print(f"\nInn: Resting costs {cost} gold. Confirm? [Y/N]")
        confirm = input("> ").lower().strip()
        if confirm == "y" and player.gold >= cost:
            player.gold -= cost
            player.hp = player.max_hp
            print(f"▶ You rested at the inn. HP fully recovered. (Gold: {player.gold})")
        else:
            print("\n▶ You don't have enough gold or you canceled.")

    elif choice == "4":
        return "Forest", quest_status

    elif choice == "5":
        player.show_status()

    else:
        print("\n▶ Invalid choice.")

    return "Town", quest_status


def visit_shop(player):
    print("\n▶ Welcome to the Shop!")
    print("Items available: [1] Potion (20 gold)  [2] Return to Town")
    choice = input("> ").strip()

    if choice == "1":
        if player.gold >= 20:
            player.gold -= 20
            player.inventory["Potion"] = player.inventory.get("Potion", 0) + 1
            print(f"▶ Purchased a Potion. (Potions: {player.inventory['Potion']}, Gold: {player.gold})")
        else:
            print("\n▶ Not enough gold.")

    elif choice == "2":
        return

    else:
        print("\n▶ Invalid choice.")

    visit_shop(player)


def visit_forest(player, quest_status):
    print("\n▶ You venture into the Forest.")

    # 퀘스트가 시작되었고 완료되지 않았다면 보스(고블린 킹) 등장
    if quest_status.get("started") and not quest_status.get("completed"):
        enemy = Enemy("Goblin King", level=3)
        defeated = battle(player, enemy)
        if defeated:
            quest_status["completed"] = True

    else:
        # 일반 몬스터 등장 확률 (약 70% 전투, 30% 평화 탐험)
        if random.random() < 0.3:
            print("▶ No enemies encountered. You explore peacefully.")
        else:
            # 퀘스트 시작 전: Goblin Lv1, 퀘스트 중: Goblin Lv2
            goblin_level = 1 if not quest_status.get("started") else 2
            enemy = Enemy("Goblin", level=goblin_level)
            battle(player, enemy)

    print("▶ Returning to Town...")
    return "Town", quest_status


# -----------------------------
# 메인 게임 루프
# -----------------------------
def main():
    print("=== Welcome to the Text RPG ===")
    name = input("Enter your character's name: ").strip()
    if not name:
        name = "Hero"
    player = Player(name)

    # 퀘스트 상태 관리
    quest_status = {
        "started": False,
        "completed": False,
        "rewarded": False
    }
    location = "Town"

    while True:
        if location == "Town":
            location, quest_status = visit_town(player, quest_status)
        elif location == "Forest":
            location, quest_status = visit_forest(player, quest_status)
        else:
            location = "Town"


if __name__ == "__main__":
    main()
