import random

import pygame

import MAP
import MOVE

pygame.init()
screen = pygame.display.set_mode((1400,800))  #窗口的长，宽
pygame.display.set_caption("ant_dueler")
clock = pygame.time.Clock()

running = True

#随机加载一张背景当地图；地图尺寸即背景图尺寸
game_map = MAP.Map(MAP.graphics_path(random.choice(MAP.BACKGROUNDS)))



whuer = MOVE.Move(700, 400, 230, 76, 116, "whuer.png")



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    # ------------------------------------------------------
    #以下写代码
    screen.fill((0, 0, 0))
    whuer.move(dt, game_map)          #1、人物移动，并且不许走出地图
    game_map.follow(whuer, screen)    #2、镜头尽量跟着人物（到地图边角才轮到人物动）
    game_map.draw(screen)             #3、画背景地图
    whuer.draw(screen, game_map)      #4、画人物，用当前朝向的那张贴图
    #到此为止
    # ------------------------------------------------------

    pygame.display.flip()

pygame.quit()
