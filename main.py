import random
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional


# ========== 枚举和常量定义 ==========
class BulletType(Enum):
    LIVE = "实弹"
    BLANK = "空弹"


class PlayerType(Enum):
    PLAYER = auto()
    ENEMY = auto()


class PropType(Enum):
    BEER = "啤酒"
    HANDCUFFS = "手铐"
    KNIFE = "小刀"
    MAGNIFYING_GLASS = "放大镜"
    CIGARETTE = "香烟"
    PILLS = "药片"
    CONVERTER = "转换器"
    PHONE = "电话"


class GameState(Enum):
    PLAYING = auto()
    PLAYER_WIN = auto()
    ENEMY_WIN = auto()


class TurnResult(Enum):
    HIT_SELF = auto()  # 打中自己
    HIT_OPPONENT = auto()  # 打中对手
    MISS = auto()  # 打空（无伤害）
    KEEP_TURN = auto()  # 保持当前回合（打自己空弹）


@dataclass
class ShotResult:
    hit_target: PlayerType  # 打中了谁
    damage: int = 1  # 伤害值
    keep_turn: bool = False  # 是否保持回合


# ========== 游戏配置 ==========
VERSION = "1.2.0"
INITIAL_HP = 5
MAX_PROPS = 8
MIN_BULLETS = 4
MAX_BULLETS = 10
KNIFE_MULTIPLIER = 2
PILL_SUCCESS_RATE = 40  # 40% 成功率


# ========== 道具效果类 ==========
class PropEffect:
    """道具效果基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def apply(self, game: "Game") -> str:
        """应用道具效果，返回描述信息"""
        raise NotImplementedError


class BeerEffect(PropEffect):
    def __init__(self):
        super().__init__(
            "啤酒", "退掉目前的第一发子弹，会告诉你退掉的子弹是实弹还是空弹"
        )

    def apply(self, game: "Game") -> str:
        if game.bullets:
            bullet = game.bullets.pop(0)
            game.live_count -= 1 if bullet == BulletType.LIVE else 0
            return f"[系统]你使用了啤酒，退掉了一发{bullet.value}"
        return "[系统]没有子弹可以退掉"


class HandcuffsEffect(PropEffect):
    def __init__(self):
        super().__init__("手铐", "禁止敌人行动一回合")

    def apply(self, game: "Game") -> str:
        if game.enemy_handcuffed:
            return "[系统]敌人已经被手铐锁住了，无法再次使用"
        game.enemy_handcuffed = True
        return "[系统]你使用了手铐，敌人下一回合无法行动"


class KnifeEffect(PropEffect):
    def __init__(self):
        super().__init__("小刀", "子弹造成的伤害*2，对自己也*2")

    def apply(self, game: "Game") -> str:
        game.knife_active = True
        return "[系统]你使用了小刀，下一发子弹伤害翻倍"


class MagnifyingGlassEffect(PropEffect):
    def __init__(self):
        super().__init__("放大镜", "告诉你目前的子弹是实弹还是空弹")

    def apply(self, game: "Game") -> str:
        if game.bullets:
            return f"[系统]你使用了放大镜，当前子弹是{game.bullets[0].value}"
        return "[系统]枪里没有子弹"


class CigaretteEffect(PropEffect):
    def __init__(self):
        super().__init__("香烟", "回复1点生命值，生命值已满时无法使用")

    def apply(self, game: "Game") -> str:
        if game.player_hp >= INITIAL_HP:
            return "[系统]你的生命值已满，无法使用香烟"
        game.player_hp = min(INITIAL_HP, game.player_hp + 1)
        return "[系统]你使用了香烟，恢复了1点生命值"


class PillsEffect(PropEffect):
    def __init__(self):
        super().__init__("药片", "40%几率恢复2点生命值，60%几率损失1点生命值")

    def apply(self, game: "Game") -> str:
        if game.player_hp >= INITIAL_HP:
            return "[系统]生命值已满，无法使用药片"

        if random.randint(1, 100) <= PILL_SUCCESS_RATE:
            game.player_hp = min(INITIAL_HP, game.player_hp + 2)
            return "[系统]你使用了药片，恢复了2点生命值"
        else:
            game.player_hp = max(0, game.player_hp - 1)
            return "[系统]你使用了药片，但效果不好，损失了1点生命值"


class ConverterEffect(PropEffect):
    def __init__(self):
        super().__init__("转换器", "把实弹变成空弹，空弹变成实弹")

    def apply(self, game: "Game") -> str:
        if game.bullets:
            current = game.bullets[0]
            game.bullets[0] = (
                BulletType.BLANK if current == BulletType.LIVE else BulletType.LIVE
            )
            game.live_count = game.bullets.count(BulletType.LIVE)
            return f"[系统]你使用了转换器，当前子弹变为{game.bullets[0].value}"
        return "[系统]枪里没有子弹"


class PhoneEffect(PropEffect):
    def __init__(self):
        super().__init__("电话", "告诉你某一发子弹是什么类型")

    def apply(self, game: "Game") -> str:
        if not game.bullets:
            return "[系统]枪里没有子弹"

        index = random.randint(0, len(game.bullets) - 1)
        bullet = game.bullets[index]
        return f"[系统]你使用了电话，第{index + 1}发子弹是{bullet.value}"


# ========== 游戏主类 ==========
class Game:
    def __init__(self):
        self.player_hp = INITIAL_HP
        self.enemy_hp = INITIAL_HP
        self.bullets: List[BulletType] = []
        self.live_count = 0
        self.current_turn = PlayerType.PLAYER
        self.enemy_handcuffed = False
        self.knife_active = False
        self.player_props: List[Optional[PropType]] = [None] * MAX_PROPS

        # 道具效果映射
        self.prop_effects = {
            PropType.BEER: BeerEffect(),
            PropType.HANDCUFFS: HandcuffsEffect(),
            PropType.KNIFE: KnifeEffect(),
            PropType.MAGNIFYING_GLASS: MagnifyingGlassEffect(),
            PropType.CIGARETTE: CigaretteEffect(),
            PropType.PILLS: PillsEffect(),
            PropType.CONVERTER: ConverterEffect(),
            PropType.PHONE: PhoneEffect(),
        }

        # 初始装弹和道具
        self.reload_bullets()
        self.draw_initial_props()

    def draw_initial_props(self) -> None:
        """游戏开始时抽取初始道具"""
        for _ in range(2):
            if None in self.player_props:
                empty_index = self.player_props.index(None)
                prop = random.choice(list(PropType))
                self.player_props[empty_index] = prop
        print()

    def show_tutorial(self) -> None:
        """显示游戏教程"""
        print("[系统]欢迎来到恶魔轮盘游戏！")
        time.sleep(1)
        print("[系统]游戏规则：")
        print("  1. 选择射击目标：自己或敌人")
        print("  2. 实弹造成伤害，空弹无伤害")
        print("  3. 射击自己为空弹时，保持回合")
        print("  4. 射击敌人为空弹时，切换回合")
        print("  5. 生命值归零则失败")
        print("  6. 子弹用尽后重新装弹并抽取道具")
        time.sleep(2)

        print("\n[系统]道具规则：")
        for prop_type, effect in self.prop_effects.items():
            print(f"  {prop_type.value}：{effect.description}")
            time.sleep(0.5)

    def reload_bullets(self) -> None:
        """重新装弹，确保既有实弹也有空弹"""
        while True:
            self.bullets.clear()
            self.live_count = 0

            bullet_count = random.randint(MIN_BULLETS, MAX_BULLETS)
            for _ in range(bullet_count):
                bullet = random.choice([BulletType.LIVE, BulletType.BLANK])
                self.bullets.append(bullet)
                if bullet == BulletType.LIVE:
                    self.live_count += 1

            # 确保既有实弹也有空弹
            if 0 < self.live_count < len(self.bullets):
                break

    def draw_props(self) -> List[str]:
        """抽取道具"""
        messages = []
        for _ in range(2):
            if None in self.player_props:
                empty_index = self.player_props.index(None)
                prop = random.choice(list(PropType))
                self.player_props[empty_index] = prop
                messages.append(f"[系统]获得道具：{prop.value}")
            else:
                messages.append("[系统]道具栏已满，无法抽取新道具")
        return messages

    def show_status(self) -> None:
        """显示游戏状态"""
        blank_count = len(self.bullets) - self.live_count
        print(f"\n[系统]当前状态：")
        print(f"  玩家生命值: {self.player_hp}/{INITIAL_HP}")
        print(f"  敌人生命值: {self.enemy_hp}/{INITIAL_HP}")
        print(
            f"  剩余子弹: {len(self.bullets)}发 ({self.live_count}实弹, {blank_count}空弹)"
        )
        print(
            f"  当前回合: {'玩家' if self.current_turn == PlayerType.PLAYER else '敌人'}"
        )

        # 显示道具
        print("  玩家道具:", end=" ")
        for i, prop in enumerate(self.player_props, 1):
            prop_name = prop.value if prop else "空"
            print(f"{i}.{prop_name}", end=" ")
        print()

    def shoot(self, target: PlayerType) -> ShotResult:
        """执行射击"""
        if not self.bullets:
            return ShotResult(hit_target=PlayerType.PLAYER, damage=0, keep_turn=True)

        bullet = self.bullets.pop(0)

        if bullet == BulletType.BLANK:
            # 空弹
            return ShotResult(
                hit_target=target,
                damage=0,
                keep_turn=(target == PlayerType.PLAYER),  # 打自己空弹保持回合
            )
        else:
            # 实弹
            damage = KNIFE_MULTIPLIER if self.knife_active else 1
            self.knife_active = False
            self.live_count -= 1

            return ShotResult(hit_target=target, damage=damage)

    def apply_damage(self, result: ShotResult) -> None:
        """应用伤害"""
        if result.damage > 0:
            if result.hit_target == PlayerType.PLAYER:
                self.player_hp = max(0, self.player_hp - result.damage)
                print(f"[系统]玩家受到{result.damage}点伤害")
            else:
                self.enemy_hp = max(0, self.enemy_hp - result.damage)
                print(f"[系统]敌人受到{result.damage}点伤害")

    def use_prop(self, prop_index: int) -> str:
        """使用道具"""
        if 0 <= prop_index < len(self.player_props):
            prop = self.player_props[prop_index]
            if prop is None:
                return "[系统]该位置没有道具"

            effect = self.prop_effects[prop]
            result = effect.apply(self)
            self.player_props[prop_index] = None
            return result
        return "[系统]无效的道具编号"

    def get_game_state(self) -> GameState:
        """获取当前游戏状态"""
        if self.player_hp <= 0:
            return GameState.ENEMY_WIN
        elif self.enemy_hp <= 0:
            return GameState.PLAYER_WIN
        return GameState.PLAYING

    def enemy_ai(self) -> PlayerType:
        """敌人AI：根据剩余子弹数量决定策略"""
        if not self.bullets:
            return PlayerType.PLAYER

        live_ratio = self.live_count / len(self.bullets) if self.bullets else 0

        # 实弹多时倾向于打玩家，实弹少时倾向于打自己
        if live_ratio > 0.5:
            return PlayerType.PLAYER  # 打玩家
        else:
            return random.choices(
                [PlayerType.PLAYER, PlayerType.ENEMY], weights=[0.4, 0.6]
            )[0]

    def play_player_turn(self) -> None:
        """执行玩家回合"""
        while True:
            print("\n" + "=" * 40)
            print("[系统]玩家回合")
            self.show_status()

            action = input(
                "[系统]请选择行动 (1:射击自己, 2:射击敌人, 3:使用道具, 4:查看状态, 5:退出): "
            )

            if action == "1":
                result = self.shoot(PlayerType.PLAYER)
                if result.damage > 0:
                    print("[玩家]你打中了自己！")
                else:
                    print("[玩家]空弹，无事发生")
                self.apply_damage(result)

                # 如果不是空弹打自己，且敌人没被铐住，切换回合
                if not (result.damage == 0 and result.hit_target == PlayerType.PLAYER):
                    if not self.enemy_handcuffed:
                        self.current_turn = PlayerType.ENEMY
                    else:
                        print("[系统]敌人被手铐锁住，无法行动，玩家继续回合")
                        self.enemy_handcuffed = False
                break

            elif action == "2":
                result = self.shoot(PlayerType.ENEMY)
                if result.damage > 0:
                    print("[玩家]你打中了敌人！")
                else:
                    print("[玩家]空弹，无事发生")
                self.apply_damage(result)

                # 打敌人空弹或敌人被铐住时，玩家保持回合
                if result.damage == 0 and not self.enemy_handcuffed:
                    self.current_turn = PlayerType.ENEMY
                elif self.enemy_handcuffed:
                    print("[系统]敌人被手铐锁住，无法行动，玩家继续回合")
                    self.enemy_handcuffed = False
                break

            elif action == "3":
                # 显示道具列表
                print("\n[系统]道具列表：")
                for i, prop in enumerate(self.player_props, 1):
                    prop_name = prop.value if prop else "空"
                    print(f"  {i}. {prop_name}")

                # 使用道具
                prop_choice = input("请输入道具编号 (1-8, 或0取消): ")
                if prop_choice.isdigit():
                    idx = int(prop_choice) - 1
                    if idx == -1:
                        print("[系统]取消使用道具")
                    elif 0 <= idx < 8:
                        message = self.use_prop(idx)
                        print(message)
                    else:
                        print("[系统]无效的编号")
                else:
                    print("[系统]请输入数字")
                continue

            elif action == "4":
                self.show_status()
                continue

            elif action == "5":
                print("[系统]游戏结束")
                exit()
            else:
                print("[系统]无效的选择，请重试")

    def play_enemy_turn(self) -> None:
        """执行敌人回合"""
        print("\n" + "=" * 40)
        print("[系统]敌人回合")

        if self.enemy_handcuffed:
            print("[系统]敌人被手铐锁住，无法行动")
            self.enemy_handcuffed = False
            self.current_turn = PlayerType.PLAYER
            return

        target = self.enemy_ai()
        result = self.shoot(target)

        if result.damage > 0:
            if target == PlayerType.PLAYER:
                print("[敌人]敌人打中了你！")
            else:
                print("[敌人]敌人打中了自己！")
        else:
            if target == PlayerType.PLAYER:
                print("[敌人]敌人射击了你，但是空弹")
            else:
                print("[敌人]敌人射击了自己，但是空弹")

        self.apply_damage(result)
        self.current_turn = PlayerType.PLAYER

    def check_reload(self) -> bool:
        """检查是否需要重新装弹，如果需要则重新装弹并抽取道具"""
        if not self.bullets:
            print("\n" + "=" * 40)
            print("[系统]子弹用尽，重新装弹...")
            self.reload_bullets()

            blank_count = len(self.bullets) - self.live_count
            print(
                f"[系统]装弹完成：{len(self.bullets)}发 ({self.live_count}实弹, {blank_count}空弹)"
            )

            # 抽取道具
            print("\n[系统]抽取道具中...")
            messages = self.draw_props()
            for msg in messages:
                print(msg)

            return True
        return False

    def run(self) -> None:
        """运行游戏主循环"""
        # 跳过教程选项
        try:
            skip = input("[系统]是否跳过教程？(y/n): ").lower()
            if skip != "y":
                self.show_tutorial()
            else:
                print("[系统]跳过教程，游戏开始！")
        except:
            pass

        # 游戏主循环
        while True:
            # 检查游戏状态
            state = self.get_game_state()
            if state == GameState.PLAYER_WIN:
                print("\n" + "=" * 40)
                print("[系统]恭喜你获胜！")
                print(
                    f"  最终状态 - 玩家生命值: {self.player_hp}, 敌人生命值: {self.enemy_hp}"
                )
                break
            elif state == GameState.ENEMY_WIN:
                print("\n" + "=" * 40)
                print("[系统]很遗憾，你输了！")
                print(
                    f"  最终状态 - 玩家生命值: {self.player_hp}, 敌人生命值: {self.enemy_hp}"
                )
                break

            # 执行回合
            if self.current_turn == PlayerType.PLAYER:
                self.play_player_turn()
            else:
                self.play_enemy_turn()

            # 检查是否需要重新装弹
            self.check_reload()


# ========== 游戏启动 ==========
if __name__ == "__main__":
    try:
        print(f"[系统]恶魔轮盘游戏 v{VERSION}")

        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\n[系统]游戏中断")
    except Exception as e:
        print(f"[系统]游戏出错: {e}")
