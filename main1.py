import pygame


pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 255))
fps = 10
clock = pygame.time.Clock()
new_event = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            screen.fill((0, 0, 255))
            centre = event.pos
            radius_and_wide = 10
            new_event = True
            while new_event:
                pygame.draw.circle(screen, pygame.Color('yellow'), centre, radius_and_wide, radius_and_wide)
                radius_and_wide += 10
                pygame.display.flip()
                clock.tick(fps)
                for event1 in pygame.event.get():
                    if event1.type == pygame.QUIT:
                        running = False
                        new_event = False
                        break
                    elif event1.type == pygame.MOUSEBUTTONDOWN:
                        screen.fill((0, 0, 255))
                        pygame.display.flip()
                        centre = event1.pos
                        radius_and_wide = 10
                        new_event = False
                        break
    pygame.display.flip()
