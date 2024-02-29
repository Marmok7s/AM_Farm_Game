import pygame
import random
import sprite_system_light

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 0))
fps = 10
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
ground = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
water = pygame.sprite.Group()
forests = pygame.sprite.Group()
buildings = pygame.sprite.Group()
generator = {'g': (sprite_system_light.Ground, ground), 'o': (sprite_system_light.Obstacle, obstacles),
             'w': (sprite_system_light.Water, water), 'f': (sprite_system_light.Basic_forest, forests),
             'b': (sprite_system_light.Building, buildings)}


class Board:

    def __init__(self, size, cell, key=0):
        self.key = key
        self.width, self.height = size
        self.cell = cell
        self.board = [[0] * self.width for i in range(self.height)]

    def load_level_board(self, level_file):
        file = open(level_file, 'r+')
        map_code = [i.rstrip('\n') for i in file.readlines()[1:]]
        cord_params = []
        for i in map_code:
            cord_params.append(i.split('_'))
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x] = cord_params[y][x]
        return file.readline().rstrip('\n')

    def render(self):
        all_sprites.draw(screen)
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), (j * self.cell, i * self.cell, self.cell, self.cell), 1)
        pygame.display.flip()

    def set_all_sprites(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                cell_type = cell[0]
                cell_subtype = int(cell[1])
                current_thing = generator[cell_type]
                current_thing[0](x, y, cell_subtype, all_sprites, current_thing[1])


farm = Board((10, 5), 30)
farm.load_level_board('levels/test_level.txt')
farm.set_all_sprites()

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            field = random.choice(ground.sprites())
            x, y = field.x_cord, field.y_cord
            for i in water:
                if i.watering(farm, (x, y)):
                    ground.update(x, y)
                    break
    farm.render()




