import pygame
import random


pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 0))
fps = 10
clock = pygame.time.Clock()


def new_box():
    screen.fill((0, 0, 0))
    x_pos = random.randrange(0, width - 20)
    y_pos = random.randrange(0, height - 20)
    pygame.draw.rect(screen, pygame.Color('brown'),(x_pos, y_pos, 80, 80))
    return x_pos, y_pos


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 32:
                x_pos, y_pos = new_box()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
    pygame.display.flip()
