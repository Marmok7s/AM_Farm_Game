import pygame
import sprite_system_light
import ui

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 0))
fps = 10
clock = pygame.time.Clock()

all_sprites = sprite_system_light.Sprite_group()
ground = sprite_system_light.Sprite_group()
obstacles = sprite_system_light.Sprite_group()
water = sprite_system_light.Sprite_group()
forests = sprite_system_light.Sprite_group()
buildings = sprite_system_light.Sprite_group()
generator = {'g': (sprite_system_light.Ground, ground), 'o': (sprite_system_light.Obstacle, obstacles),
             'w': (sprite_system_light.Water, water), 'f': (sprite_system_light.Basic_forest, forests),
             'b': (sprite_system_light.Building, buildings)}


class Board:

    def __init__(self, size, cell, key=0):
        self.key = key
        self.width, self.height = size
        self.cell = cell
        self.board = [[0] * self.width for _ in range(self.height)]
        self.selected = []

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
        for y in range(self.height):
            for x in range(self.width):
                colour = 'white'
                if (x, y) in self.selected:
                    colour = 'blue'
                pygame.draw.rect(screen, pygame.Color(colour), (x * self.cell + 100, y * self.cell + 100, self.cell, self.cell), 1)
        pygame.display.flip()

    def set_all_sprites(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                cell_type = cell[0]
                cell_subtype = int(cell[1])
                current_thing = generator[cell_type]
                current_thing[0](x, y, cell_subtype, all_sprites, current_thing[1])

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - 100) // self.cell
        cell_y = (mouse_pos[1] - 100) // self.cell
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def select(self, cords):
        if not cords:
            return None
        x, y = cords[0], cords[1]
        if len(self.selected) < 5 and (x, y) not in self.selected:
            self.selected.append((x, y))
        elif (x, y) in self.selected:
            self.selected.remove((x, y))

    def next_step(self):
        for x_cord, y_cord in self.selected:
            all_sprites.update(x_cord, y_cord)
            position_key = all_sprites.sprite_position_key(x_cord, y_cord)
            self.board[y_cord][x_cord] = self.board[y_cord][x_cord][0] + str(position_key)
        self.selected.clear()

    def restart_level(self, level):
        self.load_level_board(level)
        all_sprites.empty()
        ground.empty()
        obstacles.empty()
        water.empty()
        forests.empty()
        buildings.empty()
        self.set_all_sprites()




farm = Board((20, 20), 30)
user_info = ui.UserInterface(width, height, 100, 15, lambda: print("Типа сохранено"),
                             lambda: farm.restart_level('levels/level_1.txt'),
                             lambda: farm.next_step(), lambda: print('Энергия все!'))
farm.load_level_board('levels/level_1.txt')
farm.set_all_sprites()

playing = True

while playing:
    events = list(pygame.event.get())
    user_info.event_process(events)
    for event in events:
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            farm.select(farm.get_cell(event.pos))
            #if cords:
            #    x, y = cords
            #    for i in water:
            #        if i.watering(farm, (x, y)):
            #            ground.update(x, y)
            #            break
        elif event.type == pygame.KEYDOWN:
            farm.next_step()
    screen.fill((0, 0, 0))
    user_info.blit(screen)
    farm.render()




