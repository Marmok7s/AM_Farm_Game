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
    keys = ['ground', 'grass', 'field_empty', 'field_start', 'field_middle', 'field_ready']

    def __init__(self, x_cord, y_cord, position_key=1, *group):
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


