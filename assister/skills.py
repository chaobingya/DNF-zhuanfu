#
# """
# 按键映射中的坐标位置都是用相对位置表示的，屏幕的宽高都用1表示，例如屏幕的像素为1920x1080，那么坐标(0.5,0.5)则表示的是 以屏幕左上角为原点，像素坐标(1920,1080)*(0.5,0.5)=(960,540)的位置。按键映射中的按键码是用Qt的枚举表示的。
# keyMapNodes 一般按键的映射，json数组，所有一般按键映射都放在这个数组中，将键盘的按键映射为普通的手指点击。
#
# 一般按键映射有如下几种类型：
#
# type 按键映射的类型，每个keyMapNodes中的元素都需要指明，可以是如下类型：
# KMT_CLICK 普通点击，按键按下模拟为手指按下，按键抬起模拟为手指抬起
# KMT_CLICK_TWICE 两次点击，按键按下模拟为手指按下再抬起，按键抬起模拟为手指按下再抬起
# KMT_CLICK_MULTI 多次点击，根据clickNodes数组中的delay和pos实现一个按键多次点击
# KMT_DRAG 拖拽，按键按下模拟为手指按下并拖动一段距离，按键抬起模拟为手指抬起
# KMT_STEER_WHEEL 方向盘映射，专用于FPS游戏中移动人物脚步的方向盘的映射，需要4个按键来配合。
# 不同按键映射类型的专有属性说明：
#
# KMT_CLICK
#
# key 要映射的按键码
# pos 模拟触摸的位置
# switchMap 是否释放出鼠标，点击此按键后，除了默认的模拟触摸映射，是否释放出鼠标操作。（可以参考和平精英映射中M地图映射的效果）
# KMT_CLICK_TWICE
#
# key 要映射的按键码
# pos 模拟触摸的位置
# KMT_CLICK_MULTI
#
# delay 延迟delay毫秒以后再模拟触摸
# pos 模拟触摸的位置
# KMT_DRAG
#
# key 要映射的按键码
# startPos 模拟触摸拖动的开始位置
# endPos 模拟触摸拖动的结束位置
# KMT_STEER_WHEEL
#
# centerPos 方向盘中心点
# leftKey 左方向的按键控制
# rightKey 右方向的按键控制
# upKey 上方向的按键控制
# downKey 下方向的按键控制
# leftOffset 按下左方向键后模拟拖动到相对centerPos位置水平偏左leftOffset处
# rightOffset 按下右方向键后模拟拖动到相对centerPos位置水平偏右rightOffset处
# upOffset 按下上方向键后模拟拖动到相对centerPos位置水平偏上upOffset处
# downOffset 按下下方向键后模拟拖动到相对centerPos位置水平偏下downOffset处
# """

SKILLS = dict(
    NaiMa=dict(
        switchKey="Key_QuoteLeft",  # 快捷键
        keyMapNodes=[
            {
                "comment": "地图",  # 地图
                "type": "KMT_CLICK",  # 单击
                "key": "Key_Q",  # 键位
                "pos": {
                    "x": 0.94,
                    "y": 0.05
                },  # 坐标
                "switchMap": True,  # 释放鼠标
                "cooldown": 1,
            },
            {
                "comment": "方向盘",
                "type": "KMT_STEER_WHEEL",
                "centerPos": {
                    "x": 0.16,
                    "y": 0.72
                },
                "leftOffset": 0.1,
                "rightOffset": 0.1,
                "upOffset": 0.27,
                "downOffset": 0.2,
                "leftKey": "Key_A",
                "rightKey": "Key_D",
                "upKey": "Key_W",
                "downKey": "Key_S",
                "cooldown": 1,
            },
            {
                "comment": "技能盘",
                "type": "KMT_STEER_WHEEL",
                "centerPos": {
                    "x": 0.82,
                    "y": 0.48
                },
                "leftOffset": 0.1,
                "rightOffset": 0.1,
                "upOffset": 0.1,
                "downOffset": 0.1,
                "leftKey": "Key_Left",
                "rightKey": "Key_Right",
                "upKey": "Key_Up",
                "downKey": "Key_Down",
                "cooldown": 1,
            },
            {
                "comment": "普攻",
                "type": "KMT_CLICK_TWICE",
                "key": "Key_H",
                "pos": {
                    "x": 0.86,
                    "y": 0.83
                },
                "switchMap": False,
                "cooldown": 1,
            },

            {
                "comment": "跳",
                "type": "KMT_CLICK",
                "key": "Key_Space",
                "pos": {
                    "x": 0.90,
                    "y": 0.71
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "蹲",
                "type": "KMT_CLICK",
                "key": "Key_C",
                "pos": {
                    "x": 0.80,
                    "y": 0.90
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "后跳",
                "type": "KMT_CLICK_TWICE",
                "key": "Key_Shift",
                "pos": {
                    "x": 0.80,
                    "y": 0.90
                },
                "cooldown": 1,
            },

            {
                "comment": "突进",
                "type": "KMT_CLICK",
                "key": "Key_N",
                "pos": {
                    "x": 0.62,
                    "y": 0.89
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "左2",
                "type": "KMT_CLICK",
                "key": "Key_M",
                "pos": {
                    "x": 0.68,
                    "y": 0.89
                },
                "switchMap": False,
                "cooldown": 1,
            },

            {
                "comment": "右1",
                "type": "KMT_CLICK",
                "key": "Key_J",
                "pos": {
                    "x": 0.74,
                    "y": 0.88
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "右2",
                "type": "KMT_CLICK",
                "key": "Key_K",
                "pos": {
                    "x": 0.76,
                    "y": 0.73
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "右3",
                "type": "KMT_CLICK",
                "key": "Key_L",
                "pos": {
                    "x": 0.81,
                    "y": 0.61
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "右4",
                "type": "KMT_CLICK",
                "key": "Key_U",
                "pos": {
                    "x": 0.88,
                    "y": 0.58
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "右5",
                "type": "KMT_CLICK",
                "key": "Key_I",
                "pos": {
                    "x": 0.88,
                    "y": 0.45
                },
                "switchMap": False,
                "cooldown": 1,
            },

            {
                "comment": "上1",
                "type": "KMT_CLICK",
                "key": "Key_7",
                "pos": {
                    "x": 0.75,
                    "y": 0.31
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "上2",
                "type": "KMT_CLICK",
                "key": "Key_8",
                "pos": {
                    "x": 0.79,
                    "y": 0.31
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "上3",
                "type": "KMT_CLICK",
                "key": "Key_9",
                "pos": {
                    "x": 0.84,
                    "y": 0.31
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "上4",
                "type": "KMT_CLICK",
                "key": "Key_0",
                "pos": {
                    "x": 0.88,
                    "y": 0.31
                },
                "switchMap": False,
                "cooldown": 1,
            }
        ]),
    KuangZhan=dict(
        switchKey="Key_QuoteLeft",  # 快捷键
        keyMapNodes=[
            {
                "comment": "地图",  # 地图
                "type": "KMT_CLICK",  # 单击
                "key": "Key_Q",  # 键位
                "pos": {
                    "x": 0.94,
                    "y": 0.05
                },  # 坐标
                "switchMap": True,  # 释放鼠标
                "cooldown": 1,
            },
            {
                "comment": "方向盘",
                "type": "KMT_STEER_WHEEL",
                "centerPos": {
                    "x": 0.16,
                    "y": 0.72
                },
                "leftOffset": 0.1,
                "rightOffset": 0.1,
                "upOffset": 0.27,
                "downOffset": 0.2,
                "leftKey": "Key_A",
                "rightKey": "Key_D",
                "upKey": "Key_W",
                "downKey": "Key_S",
                "cooldown": 0.5,
            },
            {
                "comment": "技能盘",
                "type": "KMT_STEER_WHEEL",
                "centerPos": {
                    "x": 0.82,
                    "y": 0.48
                },
                "leftOffset": 0.1,
                "rightOffset": 0.1,
                "upOffset": 0.1,
                "downOffset": 0.1,
                "leftKey": "Key_Left",
                "rightKey": "Key_Right",
                "upKey": "Key_Up",
                "downKey": "Key_Down",
                "cooldown": 0.5,
            },
            {
                "comment": "普攻",
                "type": "KMT_CLICK_TWICE",
                "key": "Key_H",
                "pos": {
                    "x": 0.86,
                    "y": 0.83
                },
                "switchMap": False,
                "cooldown": 0.2,
            },

            {
                "comment": "跳",
                "type": "KMT_CLICK",
                "key": "Key_Space",
                "pos": {
                    "x": 0.90,
                    "y": 0.71
                },
                "switchMap": False,
                "cooldown": 0.5,
            },
            {
                "comment": "蹲",
                "type": "KMT_CLICK",
                "key": "Key_C",
                "pos": {
                    "x": 0.80,
                    "y": 0.90
                },
                "switchMap": False,
                "cooldown": 0.5,
            },
            {
                "comment": "后跳",
                "type": "KMT_CLICK_TWICE",
                "key": "Key_Shift",
                "pos": {
                    "x": 0.80,
                    "y": 0.90
                },
                "cooldown": 0.5,
            },

            {
                "comment": "突进",
                "type": "KMT_CLICK",
                "key": "Key_N",
                "pos": {
                    "x": 0.62,
                    "y": 0.89
                },
                "switchMap": False,
                "cooldown": 5,
            },
            {
                "comment": "左2",
                "type": "KMT_CLICK",
                "key": "Key_M",
                "pos": {
                    "x": 0.68,
                    "y": 0.89
                },
                "switchMap": False,
                "cooldown": 20,
            },

            {
                "comment": "右1",
                "type": "KMT_CLICK",
                "key": "Key_J",
                "pos": {
                    "x": 0.74,
                    "y": 0.88
                },
                "switchMap": False,
                "cooldown": 20,
            },
            {
                "comment": "右2",
                "type": "KMT_CLICK",
                "key": "Key_K",
                "pos": {
                    "x": 0.76,
                    "y": 0.73
                },
                "switchMap": False,
                "cooldown": 10,
            },
            {
                "comment": "右3",
                "type": "KMT_CLICK",
                "key": "Key_L",
                "pos": {
                    "x": 0.81,
                    "y": 0.61
                },
                "switchMap": False,
                "cooldown": 20,
            },
            {
                "comment": "右4",
                "type": "KMT_CLICK",
                "key": "Key_U",
                "pos": {
                    "x": 0.88,
                    "y": 0.58
                },
                "switchMap": False,
                "cooldown": 20,
            },
            {
                "comment": "右5",
                "type": "KMT_CLICK",
                "key": "Key_I",
                "pos": {
                    "x": 0.88,
                    "y": 0.45
                },
                "switchMap": False,
                "cooldown": 20,
            },

            {
                "comment": "上1",
                "type": "KMT_CLICK",
                "key": "Key_7",
                "pos": {
                    "x": 0.75,
                    "y": 0.31
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "上2",
                "type": "KMT_CLICK",
                "key": "Key_8",
                "pos": {
                    "x": 0.79,
                    "y": 0.31
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "上3",
                "type": "KMT_CLICK",
                "key": "Key_9",
                "pos": {
                    "x": 0.84,
                    "y": 0.31
                },
                "switchMap": False,
                "cooldown": 1,
            },
            {
                "comment": "上4",
                "type": "KMT_CLICK",
                "key": "Key_0",
                "pos": {
                    "x": 0.88,
                    "y": 0.31
                },
                "switchMap": False,
                "cooldown": 1,
            }
        ]),
)
