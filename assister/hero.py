import random
from threading import Timer

from assister.driver import Automation
from assister.skills import SKILLS


# 技能类
class Skill:
    def __init__(self, name, key, type=None, pos=None, center_pos=None, left_key=None, right_key=None,
                 up_key=None, down_key=None, left_offset=0, right_offset=0, up_offset=0,
                 down_offset=0, cooldown=0, damage=0, range=0, switch_map=False, automation: Automation = None):
        self.name = name
        self.key = key
        self.type = type
        self.pos = pos  # 适用于 KMT_CLICK 和 KMT_CLICK_TWICE 类型
        self.center_pos = center_pos  # 适用于 KMT_STEER_WHEEL 类型
        self.left_key = left_key
        self.right_key = right_key
        self.up_key = up_key
        self.down_key = down_key
        self.left_offset = left_offset
        self.right_offset = right_offset
        self.up_offset = up_offset
        self.down_offset = down_offset
        self.cooldown = cooldown
        self.damage = damage  # 技能的伤害数值
        self.range = range  # 技能的释放范围
        self.switch_map = switch_map
        self.is_ready = True
        self.adb = automation

    def execute(self):
        if self.is_ready:
            x, y = self.pos['x'], self.pos['y']
            if self.type in ('KMT_CLICK', 'KMT_CLICK_MULTI'):  # 假设技能类型以 Key_Click_ 开头
                self.adb.tap(x, y)  # 单击
            elif self.type == 'KMT_CLICK_TWICE':  # 假设双击的键位以 Key_Click_Twice 开头
                self.adb.double_click(x, y)  # 双击
            elif self.type == 'KMT_STEER_WHEEL':
                self.steer()

            self.is_ready = False
            self.start_cooldown(self.cooldown)  # 开始技能冷却
        else:
            print('skill not ready!')

    def start_cooldown(self, cooldown_duration):
        # 技能冷却时间，单位为秒
        self.cooldown_timer = Timer(cooldown_duration, self.reset_cooldown)
        self.cooldown_timer.start()

    def reset_cooldown(self):
        self.is_ready = True
        self.cooldown_timer.cancel()

    def steer(self):
        # 这里实现方向盘的逻辑
        center_x, center_y = self.adb.relative_position_to_absolute(
            self.center_pos['x'], self.center_pos['y'])

        # 根据按键确定偏移量并执行移动
        # 这里使用伪代码表示按键逻辑，你需要根据实际按键事件来触发相应的移动
        if self.left_key:
            offset_x, offset_y = self.left_offset, 0
            self.adb.move((center_x, center_y), (center_x - offset_x, center_y - offset_y))
        if self.right_key:
            offset_x, offset_y = -self.right_offset, 0
            self.adb.move((center_x, center_y), (center_x + offset_x, center_y - offset_y))
        if self.up_key:
            offset_x, offset_y = 0, -self.up_offset
            self.adb.move((center_x, center_y), (center_x + offset_x, center_y + offset_y))
        if self.down_key:
            offset_x, offset_y = 0, self.down_offset
            self.adb.move((center_x, center_y), (center_x + offset_x, center_y + offset_y))

        # 将方向盘移回中心位置
        self.adb.move((center_x, center_y), (center_x, center_y))


def load_skills_from_dict(skills_dict, automation):
    skills = {}
    node_index = 0  # 用于在缺少 'key' 时为技能提供一个唯一的索引作为键

    for node in skills_dict['keyMapNodes']:
        # 检查 'key' 是否存在于字典中，如果不存在，使用索引作为键
        skill_key = node.get('key') or f"skill_{node_index}"

        # 根据技能类型创建技能实例
        skill_type = node.get('type')
        if skill_type in ('KMT_CLICK', 'KMT_CLICK_TWICE'):
            skill = Skill(
                name=node.get('comment'),
                key=skill_key,
                type=skill_type,
                pos=node.get('pos'),
                cooldown=node.get('cooldown', 0),
                damage=node.get('damage', 0),
                range=node.get('range', 0),
                switch_map=node.get('switchMap', False),
                automation=automation
            )
        elif skill_type == 'KMT_STEER_WHEEL':
            skill = Skill(
                name=node.get('comment'),
                key=skill_key,
                type=skill_type,
                center_pos=node.get('centerPos'),
                left_key=node.get('leftKey'),
                right_key=node.get('rightKey'),
                up_key=node.get('upKey'),
                down_key=node.get('downKey'),
                left_offset=node.get('leftOffset'),
                right_offset=node.get('rightOffset'),
                up_offset=node.get('upOffset'),
                down_offset=node.get('downOffset'),
                cooldown=node.get('cooldown', 0),
                damage=node.get('damage', 0),
                range=node.get('range', 0),
                switch_map=False,
                automation=automation
            )
        else:
            node_index += 1  # 跳过不支持的技能类型
            continue

        # 将技能添加到字典中
        skills[skill_key] = skill
        node_index += 1  # 为下一个技能准备索引

    return skills


class Hero:
    def __init__(self, name, pos: tuple[int, int] = None):
        self.name = 'Hero_' + name
        self.pos = pos if pos else (0, 0)
        self.adb = Automation()
        self.leave = False
        self.skills = load_skills_from_dict(SKILLS.get(name), self.adb)  # Dictionary for quick access
        self.factotum = [ 'Key_M', 'Key_J', 'Key_K', 'Key_L', 'Key_U', 'Key_I']

    def move(self, x, y, factor=1):
        x, y = x * factor, y * factor
        self.adb.move(self.pos, (x, y))
        print(f'hero moved from {self.pos} to {(x, y)}')
        self.pos = (x, y)

    def use_skill(self, skill_key):
        skill = self.skills.get(skill_key)
        if skill:
            if skill.is_ready:
                skill.execute()
                print('use skill:', skill_key)
            else:
                print('skill not ready!')
        else:
            print('no skill')

    def add_buff(self):
        self.use_skill('KMT_CLICK')

    def get_pos(self):
        return self.pos

    def use_factotum_skill(self):
        factotums = [self.skills.get(skill_key) for skill_key in self.factotum if self.skills.get(skill_key).is_ready]
        if not factotums:
            factotums = [self.skills.get('Key_H')]  #普攻
            self.skills.get('Key_H').execute()
            self.skills.get('Key_H').execute()
            self.skills.get('Key_H').execute()
        # self.use_skill(random.choice(factotums))
        random.choice(factotums).execute()


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    hero = Hero("KuangZhan")
    hero.use_skill('Key_0')
    hero.use_skill('Key_8')
    # hero.pos = (142, 52)
    # hero.move(224, 92)
    # hero.use_skill('Key_H')
    # time.sleep(0.5)
    # hero.use_skill('Key_C')
    # time.sleep(0.5)
    # hero.use_skill('Key_Space')
    # time.sleep(0.5)
    # hero.use_skill('Key_Shift')
    # hero.use_skill('Key_J')
    # hero.use_skill('Key_K')
    # hero.use_skill('Key_L')
    # hero.use_skill('Key_U')
