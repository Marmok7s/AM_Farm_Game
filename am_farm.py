import pygame

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 0))
fps = 10
clock = pygame.time.Clock()


class Board:

    def __init__(self, size, cell, key=0):
        self.key = key
        self.width, self.height = size
        self.cell = cell
        self.board = [[0] * self.width for i in range(self.height)]
        self.generator = {'fields': [], 'covers': [], 'objects': [], 'buildings': [], 'nothing': 0}

    def generate(self):
        for line in self.board:
            for element in line:
                pass

    def verify_key(self):
        pass

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), (i * self.cell, j * self.cell, self.cell, self.cell), 1)
        pygame.display.flip()

    def load_sprite(self, x_cord, y_cord):
        pass


