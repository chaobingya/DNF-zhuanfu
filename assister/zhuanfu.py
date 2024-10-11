import signal
import time

from dotenv import load_dotenv

from assister.dungeon import Dungeon, Room
from assister.hero import Hero

load_dotenv()

dungeon = Dungeon("BuWanJia", several=1)


# 定义一个信号处理函数
def signal_handler(sig, frame):
    print('你按下了 Ctrl+C!')
    dungeon.stop()


# 设置signal_handler为SIGINT信号的处理函数
signal.signal(signal.SIGINT, signal_handler)


def main():
    # dungeon.hero = Hero("NaiMa")
    dungeon.hero = Hero("KuangZhan")
    dungeon.rooms = [
        Room(name=dungeon.name + "_" + "1", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        Room(name=dungeon.name + "_" + "2", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        Room(name=dungeon.name + "_" + "3", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        Room(name=dungeon.name + "_" + "4", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        Room(name=dungeon.name + "_" + "5", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        Room(name=dungeon.name + "_" + "6", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        # Room(name=dungeon.name + "_" + "7", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        # Room(name=dungeon.name + "_" + "8", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        # Room(name=dungeon.name + "_" + "9", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
        # Room(name=dungeon.name + "_" + "10", god_pos=(0, 0), door=[(0, 0), (0, 0)]),
    ]

    dungeon.run()
    # # 主循环
    # while True:
    #     try:
    #         # 假设有一个方法来检查游戏是否仍在运行
    #         if not dungeon.running:
    #             break
    #         dungeon.run()
    #
    #
    #     except KeyboardInterrupt:
    #         # 允许使用Ctrl+C退出程序
    #         print("脚本已手动停止。")
    #         dungeon.running=False
    #     except Exception as e:
    #         print(f"发生错误：{e}")
    #         time.sleep(2)


def is_game_running():
    # 这里实现检查游戏是否仍在运行的逻辑
    pass


if __name__ == "__main__":
    main()
