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


class Ground(pygame.sprite.Sprite):
    keys = ['grass', 'ground', 'field_empty', 'field_start', 'field_middle', 'field_ready']

    def __init__(self, x_cord, y_cord, position_key=0, *group):
        super().__init__(*group)
        self.image = load_image(''.join([Ground.keys[position_key], '.png']))
        self.rect = self.image.get_rect()
        self.rect.x = x_cord * 30
        self.rect.y = y_cord * 30
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.position_key = position_key

    def update(self, *args, **kwargs):
        list(args)
        if args[0] == self.x_cord and args[1] == self.y_cord:
            self.position_key = (self.position_key + 1) % 6
            self.image = load_image(''.join([Ground.keys[self.position_key], '.png']))


class Basic_obstacle(pygame.sprite.Sprite):

    def __init__(self, x_cord, y_cord, image, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = x_cord * 30
        self.rect.y = y_cord * 30
        self.x_cord = x_cord
        self.y_cord = y_cord


class Water(pygame.sprite.Sprite):

    def __init__(self, x_cord, y_cord, *group):
        super().__init__(*group)
        self.image = load_image('water.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_cord * 30
        self.rect.y = y_cord * 30
        self.x_cord = x_cord
        self.y_cord = y_cord

    def watering(self, place, field):
        results = []
        for y in range(place.hieght):
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


class Sand(Basic_obstacle):
    def __init__(self, x_cord, y_cord, *group):
        super().__init__(x_cord, y_cord, 'sand.png', *group)


class Stone(Basic_obstacle):
    def __init__(self, x_cord, y_cord, *group):
        super().__init__(x_cord, y_cord, 'stone.png', *group)


class Stones(Basic_obstacle):
    def __init__(self, x_cord, y_cord, *group):
        super().__init__(x_cord, y_cord, 'stones.png', *group)


class Small_stones(Basic_obstacle):
    def __init__(self, x_cord, y_cord, *group):
        super().__init__(x_cord, y_cord, 'stones_small.png', *group)


class Basic_forest(pygame.sprite.Sprite):
    def __init__(self, x_cord, y_cord, image, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = x_cord * 30
        self.rect.y = y_cord * 30
        self.x_cord = x_cord
        self.y_cord = y_cord


class Forest_fir(Basic_forest):
    def __init__(self, x_cord, y_cord, *group):
        super().__init__(x_cord, y_cord, 'forest_fir.png', *group)


class Forest_deciduous(Basic_forest):
    def __init__(self, x_cord, y_cord, *group):
        super().__init__(x_cord, y_cord, 'forest_deciduous.png', *group)


class House(pygame.sprite.Sprite):
    def __init__(self, x_cord, y_cord, *group):
        super().__init__(*group)
        self.image = load_image('house.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_cord * 30
        self.rect.y = y_cord * 30
        self.x_cord = x_cord
        self.y_cord = y_cord