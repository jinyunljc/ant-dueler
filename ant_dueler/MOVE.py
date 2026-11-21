import pygame
#使用方向键移动

class Move:
    def __init__(self,x,y,speed,xx,yy,path):
        #出生点坐标(x，y)，移动速度，图像x轴宽度，图像y轴宽度，图像路径

        self.x = x
        self.y = y
        self.speed = speed
        self.xx = xx
        self.yy = yy
        img = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, (self.xx, self.yy))

    def move(self,dt):

        keys = pygame.key.get_pressed()

        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        self.x += self.speed * dx * dt
        self.y += self.speed * dy * dt

    def draw(self,screen):
        center = (self.x,self.y)
        screen.blit(self.image,self.image.get_rect(center = center))