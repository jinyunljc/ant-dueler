import os

import pygame

#使用方向键移动

#图都放在graphics里
GRAPHICS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphics")

# 人物朝四个方向时用的临时贴图（画好正式贴图后，改这里的文件名就行）
FACING_IMAGES = {
    "up": "whuer_朝前_还没画.png",     # 向上走
    "down": "whuer_朝后.png",          # 向下走
    "left": "whuer_朝左_还没画.png",   # 向左走
    "right": "whuer_朝右_还没画.png",  # 向右走
}


def _clamp(value,low,high):
    """把 value 限制在 low 和 high 之间。"""
    return max(low, min(value, high))


def load_image(path, size):
    """读一张贴图，并缩放到 size 大小。

    临时贴图是白底的（不透明），这里把左上角的颜色当成透明色去掉，
    不然人物会拖着一个白方块。正式贴图如果是透明背景，这一步没影响。
    注意要先 convert_alpha() 把底色真正变成透明，再缩放，
    否则 transform.scale 会把透明色丢掉。
    """
    img = pygame.image.load(path)
    corner = img.get_at((0, 0))
    if corner.a > 0:                     # 左上角不透明，说明这张图有底色
        img.set_colorkey((corner.r, corner.g, corner.b))
    img = img.convert_alpha()
    return pygame.transform.scale(img, size)


class Move:
    def __init__(self,x,y,speed,xx,yy,path=None):
        # 出生点坐标(x，y)，移动速度，图像x轴宽度，图像y轴宽度，图像路径

        self.x=x      # 人物在地图里的坐标（世界坐标，不是屏幕坐标）
        self.y=y
        self.speed=speed
        self.xx=xx
        self.yy=yy

        # 四个方向各加载一张图，转身时直接换图，不用重新读文件
        self.images = {}
        for direction, name in FACING_IMAGES.items():
            path_name = os.path.join(GRAPHICS_DIR, name)
            self.images[direction] = load_image(path_name, (self.xx, self.yy))

        if path is not None:
            # 保留原来的写法：额外传进来的图当作“朝后”那张用
            self.images["down"] = load_image(path, (self.xx, self.yy))

        self.facing = "down"                    # 当前朝向
        self.image = self.images[self.facing]   # 当前贴图

    def move(self, dt, game_map=None):
        keys = pygame.key.get_pressed()

        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        self.x += self.speed * dx * dt
        self.y += self.speed * dy * dt

        # 按前进方向换贴图：斜着走时以水平方向为准，站着不动时保持上次的朝向
        if dx>0:
            self.facing="right"
        elif dx<0:
            self.facing="left"
        elif dy>0:
            self.facing="down"
        elif dy<0:
            self.facing="up"
        self.image = self.images[self.facing]

        #人物不能走出地图,把人物整个限制在地图范围内
        if game_map is not None:
            self.x = self._limit(self.x, self.xx, game_map.width)
            self.y = self._limit(self.y, self.yy, game_map.height)

    @staticmethod
    def _limit(value,size,map_size):
        # 限制人物中心的坐标 保证整张人物图都留在地图里
        half = size / 2
        if map_size < size:
            return map_size / 2          # 地图比人物还小，就站在地图中间
        return _clamp(value, half, map_size - half)

    def draw(self, screen, game_map=None):
        # 世界坐标 -> 屏幕坐标：减掉镜头偏移
        camera_x,camera_y = game_map.camera() if game_map is not None else (0, 0)
        center = (round(self.x - camera_x), round(self.y - camera_y))
        screen.blit(self.image, self.image.get_rect(center=center))
