import math
import threading
import time
from pprint import pprint

from assister.hero import Hero
from assister.vision import DNF_DETECTOR


class Job(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def run(self):
        while self.__running.isSet():
            print("thread is run")
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到self.__flag为True后返回
            print("run = ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            time.sleep(1)

    def pause(self):
        print("thread is pause")
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        print("thread is resume")
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        print("thread is stop")
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False


class Dungeon:
    def __init__(self, name: str, several: int):
        self.name = name
        self.rooms: list[Room, ...] = None
        self.room: Room = None
        self.hero: Hero = None
        self.several = several
        self.running = True
        self.stopped = False

    def start(self):
        pass

    def restart(self):
        pass

    def stop(self):
        self.running = False
        self.stopped = True

    def in_room(self):
        while (not self.stopped) and self.hero.pos == (0, 0):
            print('the hero not in room')
            time.sleep(1)
        return True

    def look(self):
        def __do_look(args):
            while self.running and (not self.stopped):
                time.sleep(1)
                self.look_and_update_environment()

        t = threading.Thread(target=__do_look, args=(self,))
        t.start()

    def look_and_update_environment(self):
        result = DNF_DETECTOR.vision(self.hero.adb.screenshot())
        # pprint(result)
        if result:
            result.pop('Master_Fake', 'no fake master.')
            self.update_environment(result)

    def get_hero_position(self, hero_pos, role_pos):
        # print('hero_pos', hero_pos)
        # print('role_pos', role_pos)
        # 英雄和英雄职业的坐标
        # coords = {'Hero': hero_pos, 'Role': role_pos}
        # # 计算距离
        # distances = {key: [self.calculate_distance(self.hero.pos, coord) for coord in coords[key]] for key in coords}
        # self.hero.pos = min(distances.items(), key=lambda item: min(item[1]))[0]
        old_pos = self.hero.pos
        if role_pos:
            self.hero.pos = role_pos[0]
        elif hero_pos:
            self.hero.pos = hero_pos[0]
        else:
            self.hero.pos = (0, 0)
        distance = self.calculate_distance(old_pos, self.hero.pos)
        print('old_pos: ', old_pos, 'new_pos: ', self.hero.pos, 'distance: ', distance)
        self.hero.leave = False if distance < 25 else True

    def update_environment(self, data):
        if getattr(self, 'room'):
            hero_pos = data.get('Hero')
            role_pos = data.get(self.hero.name, [])
            self.get_hero_position(hero_pos, role_pos)
            # self.hero.position = hero_pos[0]
            # self.room.name = data.get('Room')
            self.room.enemies = self.sort_route(data.get('Monster'))
            self.room.items = self.sort_route(data.get('Item'))
            self.room.route = self.sort_route(data.get('Route'))

            self.room.door_lock = data.get('Docr_Lock', [])
            self.room.lock = True if (data.get('Docr_Lock') and (not data.get('Dore_Open'))) else False
            self.room.door_open = data.get('Dore_Open', [])
            self.room.door_next = data.get('Docr_NEXT', [])
            self.room.doors = data.get('Door', []) + self.room.door_lock + self.room.door_open

    def run(self):
        self.look()
        for index, room in enumerate(self.rooms):
            self.room = room
            # self.running = True
            if self.in_room():
                if room.god_pos and room.god_pos != (0, 0):
                    print('move to the god position')
                    self.hero.move(*room.god_pos)
                if index == 0:
                    #     self.hero.add_buff()
                    self.hero.use_skill('Key_0')
                    # time.sleep(0.5)
                # elif index == 1:
                #     self.hero.use_skill('B')
                # elif index == 2:
                #     self.hero.use_skill('C')
                while not self.stopped and self.running:
                    # pprint('执行自动任务：')
                    if self.room.enemies:
                        pprint(f'发现怪物，移动并进行攻击，英雄坐标{self.hero.pos}，怪物坐标{self.room.enemies}')
                        # print('monster center: ', calculate_centroid(self.room.enemies))
                        self.hero.move(*self.get_neearst(self.hero.pos, self.room.enemies), factor=0.8)
                        # self.hero.move(*calculate_centroid(self.room.enemies), factor=0.85)
                        self.hero.use_factotum_skill()
                        # time.sleep(0.5)

                    elif self.room.items:
                        pprint(f'发现掉落奖励，移动英雄进行拾取，材料坐标:{self.room.items}')
                        for pos in self.room.items:
                            self.hero.move(*pos)
                            # time.sleep(0.5)

                        # 寻找找到路径终点最近的门
                    elif self.room.route:
                        pprint('房间任务已完成，准备离开该房间')
                        # 对路径点进行排序，确保它们按照英雄移动的顺序排列
                        # end_point = self.room.route[-1]
                        for pos in self.room.route:
                            self.hero.move(*pos)
                            # time.sleep(0.2)
                        # [self.hero.move(*pos) for pos in self.room.route]
                    else:
                        # 如果路线中没有点，选择距离最近的房间移动
                        # print("Route does not have enough points to form a path.")
                        end_point = self.hero.pos
                        nearest_door = self.get_neearst(end_point, self.room.doors)
                        if nearest_door:
                            print(f'移动到门口{nearest_door}')
                            self.hero.move(*nearest_door)
                            # self.running = False
                # self.auto_attck()
                # self.leave()
                # self.running = False  # Stop the update thread when

    def auto_attck(self):
        while (self.room.lock or (not self.room.is_cleared())) and (not self.stopped):
            pprint('执行自动任务：')
            if self.room.enemies:
                pprint(f'发现怪物，移动并进行攻击，英雄坐标{self.hero.pos}，怪物坐标{self.room.enemies}')
                # print('monster center: ', calculate_centroid(self.room.enemies))
                self.hero.move(*self.get_neearst(self.hero.pos, self.room.enemies), factor=0.85)
                # self.hero.move(*calculate_centroid(self.room.enemies), factor=0.85)
                self.hero.use_factotum_skill()
                # time.sleep(0.5)

            elif self.room.items:
                pprint(f'发现掉落奖励，移动英雄进行拾取，材料坐标:{self.room.items}')
                for pos in self.room.items:
                    self.hero.move(*pos)
                    # time.sleep(0.5)

    def leave(self):
        while self.room.route or self.room.door_open or (not self.hero.leave):
            pprint('房间任务已完成，准备离开该房间')
            # 寻找找到路径终点最近的门
            if self.room.route:
                # 对路径点进行排序，确保它们按照英雄移动的顺序排列
                end_point = self.room.route[-1]
                for pos in self.room.route:
                    self.hero.move(*pos)
                    # time.sleep(0.2)
                # [self.hero.move(*pos) for pos in self.room.route]
            else:
                # 如果路线中没有点，选择距离最近的房间移动
                print("Route does not have enough points to form a path.")
                end_point = self.hero.pos
                nearest_door = self.get_neearst(end_point, self.room.doors)
                if nearest_door:
                    self.hero.move(*nearest_door)

    def get_neearst(self, end_point, targets):
        nearest = None
        min_distance = float('inf')
        for target in targets:
            distance = self.calculate_distance(end_point, target)
            if distance < min_distance:
                nearest = target
                min_distance = distance
        return nearest

    def sort_route(self, route_points):
        if not route_points:
            return []
        # 使用起始点对路径点进行排序
        return sorted(route_points, key=lambda point: self.calculate_distance(self.hero.pos, point))

    @staticmethod
    def calculate_distance(point1, point2):
        # 计算两点之间的欧几里得距离
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point2[1] - point1[1]) ** 2)


class Room:
    def __init__(self, name: str, god_pos: tuple[int, int] = None, door: list[tuple[int, int], ...] = None):
        self.name = name
        self.god_pos = god_pos
        self.enemies = []  # List of Monster objects
        self.items = []  # List of Item objects
        self.doors = door
        self.route = None
        self.lock: bool = True
        self.door_lock = None
        self.door_open = None
        self.door_next = None

    def is_cleared(self):
        print('the {0} room is {1}'.format(self.name, 'not clear' if (self.items or self.enemies) else 'clear'))
        return False if (self.items or self.enemies) else True

    def is_closed(self):
        return False if (self.door_lock and not self.door_open) else True

    # def enter(self, hero):
    #     for enemy in self.enemies:
    #         enemy.react(hero)
    #     # Additional logic for entering the room
    #
    # def next(self):
    #     return self.doors
