import os
import threading
import time
from pprint import pprint
from typing import List, Dict

import cv2
from ultralytics.engine.results import Results
from ultralytics.models.yolo.model import YOLO


def calculate_centroid(points):
    """
    计算一组点的质心坐标。

    参数:
    points -- 点的坐标列表，格式为 [(x1, y1), (x2, y2), ...]

    返回:
    (cx, cy) -- 质心坐标
    """
    total_x = sum(point[0] for point in points)
    total_y = sum(point[1] for point in points)
    num_points = len(points)

    centroid_x = round(total_x / num_points, 2)
    centroid_y = round(total_y / num_points, 2)

    return centroid_x, centroid_y


def sort_coordinates_dict(coord_dict):
    """
    对字典中的每个坐标列表按 x 坐标进行排序。

    参数:
    coord_dict -- 键为类别名，值为坐标点列表的字典，每个坐标是一个 (x, y) 元组

    返回:
    一个新的字典，其中的坐标列表已按 x 坐标排序
    """
    # 使用字典推导式和 sorted 函数对每个类别的坐标进行排序
    sorted_dict = {category: sorted(coords, key=lambda point: point[0]) for category, coords in coord_dict.items()}
    return sorted_dict


class ObjectDetector:
    _instance_lock = threading.Lock()

    def __init__(self, model_path):
        self.model = self.load_model(model_path)
        self.score = 0.30  #60%置信度

    def __new__(cls, *args, **kwargs):
        if not hasattr(ObjectDetector, "_instance"):
            with ObjectDetector._instance_lock:
                if not hasattr(ObjectDetector, "_instance"):
                    ObjectDetector.__instance = object.__new__(cls)
        return ObjectDetector.__instance

    @staticmethod
    def load_model(model_path):
        return YOLO(model_path)

    @staticmethod
    def preprocess(image):
        # 对图像进行预处理，以适应YOLO模型输入
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.resize(image, (640, 640))  # 假设模型需要640x640的图像
        return image

    def predict(self, image):
        # 使用模型进行预测
        preprocessed_image = self.preprocess(image)
        # timestamp = int(time.time())
        # 是一个包含多个检测结果的列表
        return self.model.predict(
            source=preprocessed_image,
            # imgsz=(320, 640),  # 设置输入图像的尺寸
            # show=True,  # 显示结果
            # save=True,  # 保存结果
            # save_frames=True,
            # save_dir='.',
            # name=f'result_{timestamp}.jpg'
        )

    def postprocess(self, predictions: List[Results]) -> Dict:
        """
        返回的坐标为图片坐标，需要加上窗口的left。top+extra
        :param predictions:
        :return:
        """
        results = dict()
        # 显示预测结果
        if len(predictions) == 0:
            pprint("没有检测到任何对象。")
            return results
        # 遍历所有检测结果
        for img_idx, prediction_img in enumerate(predictions):
            pprint(f"图像 {img_idx} 检测到 {len(prediction_img.boxes)} 个对象。")
            # result_img = cv2.cvtColor(cv2.imread('../datasets/images/train/b80acdfa-frame_0021.jpg'),
            # cv2.COLOR_BGR2RGB) 绘制每个检测到的对象的边界框和标签
            for i, box in enumerate(prediction_img.boxes):
                x1, y1, x2, y2 = box.xyxy[0]  # 获取边界框坐标
                x, y = round((x1 + x2).item(), 2) / 2, round((y1 * 1 / 5 + y2 * 4 / 5).item(), 2)
                score = round(box.conf.item(), 2)  # 置信度
                if score > self.score:
                    cls = int(box.cls.item())  # 类别索引
                    cls_name = prediction_img.names.get(cls)  # 类别名称
                    if not results.get(cls_name):
                        results[cls_name] = []
                    results[cls_name].append((x, y))
            # # 绘制边界框
            # for cls_name, points in results.items():
            #     if len(points) > 1:  # 确保有足够的点来绘制质心
            #         for x, y in points:
            #             cv2.circle(result_img, (int(x), int(y)), 5, (0, 0, 255), -1)  # 绘制点
            #         centroid = calculate_centroid(points)
            #         cv2.circle(result_img, (int(centroid[0]), int(centroid[1])), 10, (255, 0, 0), -1)  # 绘制质心
            #
            # cv2.imshow(f"Predictions for image {img_idx}", result_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        return sort_coordinates_dict(results)

    def vision(self, img):
        return self.postprocess(self.predict(img))


DNF_DETECTOR = ObjectDetector("./best.pt")

if __name__ == '__main__':
    # vision = ObjectDetector("D:/code/rambo/zhuanfu/zhuanfu/runs/detect/train5/weights/best.pt")
    # prediction = vision.predict('../datasets/images/train/b80acdfa-frame_0021.jpg')
    # result = vision.postprocess(prediction)
    # print(result)
    # print(calculate_centroid(result.get('Monster')))
    # print(calculate_centroid(result.get('Hero_NaiMa')))

    obj = DNF_DETECTOR


    def task(obj, file):
        obj.predict(file)


    base_dir = 'D:\\code\\rambo\\zhuanfu\\datasets\\images\\train'
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    files = [os.path.join(base_dir, file) for file in os.listdir(base_dir) if
             os.path.splitext(file)[1].lower() in image_extensions]

    for i in range(len(files)):
        t = threading.Thread(target=task, args=[obj, files[i]])
        t.start()
        time.sleep(0.08)
