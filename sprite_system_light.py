import os
import sys
import pygame


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Cell(pygame.sprite.Sprite):
    keys: list[str] = []

    def __init__(self, x_cord, y_cord, position_key=0, *groups):
        super().__init__(*groups)
        self.image = load_image(self.keys[position_key] + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_cord * 30
        self.rect.y = y_cord * 30
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.position_key = position_key


class Ground(Cell):
    keys = ['grass', 'field_empty', 'field_start', 'field_middle', 'field_ready', 'ground']

    def __init__(self, x_cord, y_cord, position_key=0, *groups):
        super().__init__(x_cord, y_cord, position_key, *groups)

    def update(self, *args, **kwargs):
        list(args)
        if args[0] == self.x_cord and args[1] == self.y_cord:
            self.position_key = (self.position_key + 1) % 6
            self.image = load_image(''.join([Ground.keys[self.position_key], '.png']))


class Obstacle(Cell):
    keys = ['stones', 'sand', 'stone', 'stones_small']

    def __init__(self, x_cord, y_cord, position_key=0, *groups):
        super().__init__(x_cord, y_cord, position_key, *groups)


class Water(Cell):
    keys = ['water']

    def __init__(self, x_cord, y_cord, position_key=0, *groups):
        super().__init__(x_cord, y_cord, position_key, *groups)

    def watering(self, place, field):
        results = []
        for y in range(place.height):
            for x in range(place.width):
                if not abs(x - self.x_cord) > 2:
                    if not abs(y - self.y_cord) > 2:
                        try:
                            results.append((x, y))
                        except KeyError:
                            pass
        if field in results:
            return True
        return False


class Basic_forest(Cell):
    keys = ['forest_fir', 'forest_deciduous']

    def __init__(self, x_cord, y_cord, position_key=0, *groups):
        super().__init__(x_cord, y_cord, position_key, *groups)


class Building(Cell):
    keys = ['house']

    def __init__(self, x_cord, y_cord, position_key=0, *groups):
        super().__init__(x_cord, y_cord, position_key, *groups)


class Sprite_group(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

