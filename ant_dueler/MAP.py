import os

import pygame

# 图都放在 graphics 文件夹里。
# 用本文件所在的位置来算路径，所以在哪个目录下运行都能找到图。
GRAPHICS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphics")

# 两张背景图，MAIN 里随机挑一张当地图
BACKGROUNDS = [
    "背景1_还没画.jpg",
    "背景2_还没画.jpg",
]


def graphics_path(name):
    """把 graphics 里的文件名拼成完整路径。"""
    return os.path.join(GRAPHICS_DIR, name)


class Map:
    """地图 = 一张背景图。图比屏幕大时，镜头会跟着人物滚动。"""

    def __init__(self, path):
        # 背景是不透明的，用 convert() 转成屏幕格式，画得快点
        self.image = pygame.image.load(path).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # 镜头左上角在地图里的位置（世界坐标）
        self.camera_x = 0
        self.camera_y = 0

    def follow(self, target, screen):
        """让镜头尽量跟着人物 target。

        地图比屏幕大时：人物一直在屏幕中间，动的是地图；人物走到地图的
        边角，镜头顶到头停下来，这时人物才在屏幕上继续移动。地图比屏幕
        小时：地图整个居中，人物在地图里走。
        这样人物既出不了地图，也出不了屏幕。
        """
        screen_w, screen_h = screen.get_size()
        self.camera_x = self._axis(target.x, self.width, screen_w)
        self.camera_y = self._axis(target.y, self.height, screen_h)

    @staticmethod
    def _axis(focus, map_size, screen_size):
        if map_size <= screen_size:
            # 地图不够大：整张图在屏幕上居中（镜头偏移是负数）
            return (map_size - screen_size) // 2
        # 地图够大：人物对准屏幕中间，但镜头不能露出地图外面
        return round(max(0, min(focus - screen_size / 2, map_size - screen_size)))

    def camera(self):
        """返回镜头偏移：屏幕坐标 = 世界坐标 - 镜头偏移。"""
        return self.camera_x, self.camera_y

    def draw(self, screen):
        # 把地图往左上挪，挪出去的部分自然被屏幕裁掉，看起来就是镜头在移动
        screen.blit(self.image, (-self.camera_x, -self.camera_y))
