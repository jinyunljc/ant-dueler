import pygame
import MOVE

pygame.init()
screen = pygame.display.set_mode((1400,800))  #窗口的长，宽
pygame.display.set_caption("ant_dueler")
clock = pygame.time.Clock()

running = True





whuer = MOVE.Move(700, 400, 230, 76, 116, "whuer.png")



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    # ------------------------------------------------------
    #以下写代码
    screen.fill((0, 0, 0))
    MOVE.Move.move(whuer, dt)
    MOVE.Move.draw(whuer,screen)

    #到此为止
    # ------------------------------------------------------

    pygame.display.flip()

pygame.quit()
