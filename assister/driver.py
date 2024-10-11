import math
import os
import time

import pyautogui
import pygetwindow as gw

from assister.android_console import start_scrcpy


class Automation:
    def __init__(self, ):
        # 初始化函数，设置窗口标题和模型
        self.extra_height = 30
        self.window = self.get_window()
        self.window_is_top = os.environ.get('ADB_WINDOW_TOP')
        self.huagan, self.huagan_move_max = self.get_huagan_location()

    def get_window(self):
        window_title = os.environ.get('ADB_WINDOW_TITLE')
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            return windows[0]
        else:
            # Exception('Window not found')
            start_scrcpy()
            time.sleep(3)
            return self.get_window()

    def get_win_info(self):
        return self.window.left, self.window.top, self.window.width, self.window.height

    def screenshot(self):
        if self.window.isMaximized or self.window.isMinimized:
            self.window.restore()
        if not (self.window.isActive or self.window_is_top):
            # 该方法会让屏幕一直在最前面。
            pyautogui.press('altleft')  # 第二次acitive会gw.PyGetWindowException异常，添加此方法
            self.window.activate()
            time.sleep(0.07)
        return pyautogui.screenshot(
            region=(
                self.window.left, self.window.top + self.extra_height,
                self.window.width, self.window.height - self.extra_height)
        )

    # 以下是一些模拟触摸和拖动的静态方法
    @staticmethod
    def touch_start(x, y, duration=0.4):
        pyautogui.moveTo(x, y, duration=duration)  # 移动到指定位置
        pyautogui.mouseDown(button='left')  # 模拟按下

    @staticmethod
    def touch_move(x, y, duration=0.25):
        pyautogui.moveTo(x, y, duration=duration)  # 移动到新位置

    @staticmethod
    def touch_end():
        pyautogui.mouseUp()  # 模拟释放

    def tap(self, x, y, t=0.01):
        abs_x, abs_y = self.relative_position_to_absolute(x, y)
        self.touch_start(abs_x, abs_y)  # 模拟触摸开始
        time.sleep(t)  # 等待时间
        self.touch_end()  # 模拟触摸结束

    def double_click(self, x, y, duration=0.01):
        x, y = self.relative_position_to_absolute(x, y)
        self.touch_start(x, y, duration)  # 模拟触摸开始
        time.sleep(duration)  # 等待时间
        self.touch_end()  # 模拟触摸结束
        self.touch_start(x, y, duration)  # 模拟触摸开始
        time.sleep(duration)  # 等待时间
        self.touch_end()  # 模拟触摸结束

    @staticmethod
    def dragTo(x, y):
        pyautogui.dragTo(x, y, duration=0.25, button='left')  # 模拟拖动

    def unlock_device(self):
        """
        解锁设备
        :return:
        """
        self.touch_start(
            self.window.left + 269 / 656 * self.window.width,
            self.window.top + self.extra_height + 233 / 297 * (
                    self.window.height - self.extra_height)
        )
        self.touch_move(
            self.window.left + 385 / 656 * self.window.width,
            self.window.top + self.extra_height + 233 / 297 * (
                    self.window.height - self.extra_height)
        )
        self.touch_end()

    def get_huagan_location(self):
        return (self.window.left + round(self.window.width / 100, 0) + int(
            105 / 656 * self.window.width), self.window.top + self.extra_height + int(
            210 / 297 * (self.window.height - self.extra_height))), (int(105 / 656 * self.window.width) * 0.75, int(
            (1 - 210 / 297) * (self.window.height - self.extra_height)) * 0.75)

    # def get_huagan_max_move(self):
    #     return int(105 / 656 * self.window.width) * 0.75, int(
    #         (1 - 210 / 297) * (
    #                 self.window.height - self.extra_height)) * 0.75

    @staticmethod
    def get_angle(src, dst):
        """ 已知两点坐标计算角度
        :param src: 原点坐标，如 (x1, y1)
        :param dst: 目标点坐标，如 (x2, y2)
        """
        x1, y1 = src
        x2, y2 = dst

        dx = x2 - x1
        dy = y2 - y1

        if dy == 0:
            if dx == 0:
                angle = 0
            elif dx > 0:
                angle = 0
            else:
                angle = math.pi
        elif dx == 0:
            if dy > 0:
                angle = math.pi / 2
            else:
                angle = 3 * math.pi / 2
        else:
            angle = math.atan2(dy, dx)

        return angle

    def calculate_Y(self, A, B, X, Y_x, Y_y):
        """
        在笛卡尔坐标系上，利用src:A,dst:B的坐标，计算Y坐标。其中AB向量与XY向量保持一致。Y是 X（半径为max( Y_x, Y_y)）圆内的某一点。
        """
        # 计算向量 AB
        AB_x = B[0] - A[0]
        AB_y = B[1] - A[1]

        # 计算向量 AB 的长度
        AB_length = math.sqrt(AB_x ** 2 + AB_y ** 2)
        if AB_length == 0:
            return X
        # 计算向量 AB 的单位向量
        AB_unit_x = AB_x / AB_length
        AB_unit_y = AB_y / AB_length
        # 计算圆的半径
        radius = max(Y_x, Y_y)
        # 计算点 Y 的坐标
        Y = (round(X[0] + radius * AB_unit_x, 2), round(X[1] + radius * AB_unit_y, 2))
        # print('Hero:', A, 'Dst:', B, 'HuaGan:', X, 'HuaGanMove:', Y, 'max_x:', Y_x, 'max_y', Y_y)
        # print('Hero_Dst_angle:', self.get_angle(A, B), 'HuaGan_angle:', self.get_angle(X, Y))
        return Y

    def move(self, hero: tuple, dst: tuple):
        """

        :param hero: location of hero, like (left, top)
        :param dst: location of dst, like (left, top)
        :return:
        """
        # 位移按键位置,固定
        # max_x, max_y = self.get_huagan_max_move()
        huagan_X, huagan_Y, = self.huagan
        max_x, max_y = self.huagan_move_max
        # 触摸开始
        # self.touch_start(huagan_X, huagan_Y)
        # 计算位移
        delta_x = dst[0] - hero[0]
        delta_y = dst[1] - hero[1]
        # 限制位移范围不超过屏幕范围。

        # limited_delta_x = max(-max_x, min(max_x, delta_x))
        # limited_delta_y = max(-max_y, min(max_y, delta_y))
        # # 计算滑杆的移动坐标
        # move_x = huagan_X + limited_delta_x
        # move_y = huagan_Y + limited_delta_y
        move_x, move_y = self.calculate_Y(hero, dst, (huagan_X, huagan_Y), max_x, max_y)
        # 触摸移动到新位置 计算斜向移动的直线距离

        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        window_distance = math.sqrt(self.window.width ** 2 + self.window.height ** 2)
        # 计算持续时间，这里应该除以speed，没有细扣。
        duration = max(0.10, round(distance / window_distance * 2.35, 2))
        pyautogui.moveTo(huagan_X, huagan_Y)
        pyautogui.dragTo(move_x, move_y, duration=duration)

        # self.touch_move(move_x, move_y, duration=duration)
        # self.touch_end()

    def relative_position_to_absolute(self, x, y):
        abs_x = x * self.window.width + self.window.left  # 宽度不减 extra_height
        abs_y = y * (self.window.height - self.extra_height) + self.extra_height + self.window.top
        return abs_x, abs_y

    def drag(self, start_x, start_y, end_x, end_y):
        abs_start_x, abs_start_y = self.relative_position_to_absolute(start_x, start_y)
        abs_end_x, abs_end_y = self.relative_position_to_absolute(end_x, end_y)
        self.touch_start(abs_start_x, abs_start_y)
        self.dragTo(abs_end_x, abs_end_y)
        self.touch_end()

    def steer_wheel(self, center_pos, left_key, right_key, up_key, down_key, offsets):
        # 转换中心点坐标
        center_abs_x, center_abs_y = self.relative_position_to_absolute(center_pos['x'], center_pos['y'])

        # 定义方向盘每个方向的按键和偏移量
        directions = {
            'left': (left_key, offsets['leftOffset'], (-1, 0)),
            'right': (right_key, offsets['rightOffset'], (1, 0)),
            'up': (up_key, offsets['upOffset'], (0, -1)),
            'down': (down_key, offsets['downOffset'], (0, 1))
        }

        # 模拟方向盘的每个方向按键
        for direction, (key, offset, _) in directions.items():
            # 计算目标坐标
            dst_x = center_abs_x + offset * self.window.width * 0.02  # 假设每次移动2%的屏幕宽度
            dst_y = center_abs_y + offset * self.window.height * 0.02  # 假设每次移动2%的屏幕高度
            # 模拟按键按下
            pyautogui.keyDown(key)
            # 移动到目标坐标
            self.move((center_abs_x, center_abs_y), (dst_x, dst_y))
            # 模拟按键释放
            pyautogui.keyUp(key)

        # 等待一段时间以模拟按键操作完成
        time.sleep(0.1)

    def simulate_keymap(self, keymap):
        for node in keymap['keyMapNodes']:
            if node['type'] == 'KMT_CLICK':
                self.tap(node['pos']['x'], node['pos']['y'])
            elif node['type'] == 'KMT_CLICK_TWICE':
                self.double_click(node['pos']['x'], node['pos']['y'])
            elif node['type'] == 'KMT_STEER_WHEEL':
                self.steer_wheel(
                    node['centerPos'],
                    node['leftKey'], node['rightKey'],
                    node['upKey'], node['downKey'],
                    {'leftOffset': node['leftOffset'], 'rightOffset': node['rightOffset'], 'upOffset': node['upOffset'],
                     'downOffset': node['downOffset']}
                )
            # 其他类型的按键映射可以在这里添加处理逻辑


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    adb = Automation()
    # screenshot = adb.screenshot()
    # screenshot.save('screenshot.png')
    # # screenshot.show()
    # print(adb.get_win_info())
    # adb.unlock_device()

    # adb.move((324, 192), (224, 92))
    # x, y = adb.get_huagan_location()
    # print(x, y)
    # adb.click(x, y)
