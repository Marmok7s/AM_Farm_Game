import os
import sys
from math import sqrt

import pygame

from random import random

from perlin_noise import PerlinNoise


def load_image(name, colorkey=None):
    fullname = os.path.join('../../Documents/alisas project/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Cell(pygame.sprite.Sprite):
    keys: list[str] = []

    def __init__(self, x_cord, y_cord, position_key, *groups):
        super().__init__(*groups)
        self.image = load_image(self.keys[position_key] + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_cord * 30
        self.rect.y = y_cord * 30
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.position_key = position_key

        # print(position_key, self.keys[position_key])

    def __repr__(self):
        return f'{type(self).__name__}: {self.x_cord}, {self.y_cord}'


class Ground(Cell):
    keys = ['grass', 'field_ready', 'field_middle', 'field_start', 'field_empty', 'ground']

    def __init__(self, x_cord, y_cord, position_key=1, *groups):
        super().__init__(x_cord, y_cord, position_key, *groups)

    def update(self, *args, **kwargs):
        if args[0] == self.x_cord and args[1] == self.y_cord:
            self.position_key = (self.position_key + 1) if (self.position_key + 1) < len(self.keys) else len(
                self.keys) - 1  # % len(self.keys)
            self.image = load_image(self.keys[self.position_key] + '.png')

        # print(0)


class Obstacle(Cell):
    keys = ['forest2', 'sand', 'forest1']

    def __init__(self, x_cord, y_cord, position_key=0, *groups):
        super().__init__(x_cord, y_cord, position_key, *groups)


class Water(Cell):
    keys = ['water']

    def __init__(self, x_cord, y_cord, position_key=0, *groups):
        super().__init__(x_cord, y_cord, position_key, *groups)

    def watering(self, place, field):
        results = []
        for x in range(place.width):
            for y in range(place.hieght):
                if not abs(x - self.x_cord) > 2:
                    if not abs(y - self.y_cord) > 2:
                        try:
                            results.append((x, y))
                        except KeyError:
                            pass
        if field in results:
            return True
        return False


class Bord(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def generate_valley(self, noise, size_x, size_y, noise_scale_factor=25):
        self.size_x = size_x
        self.size_y = size_y

        water_matrix = [[0 for _ in range(size_x)] for _ in range(size_y)]

        obst_cof = 0.3
        water_cof = 0.9

        for y in range(size_y):
            for x in range(size_x):
                wetness = noise([x / noise_scale_factor, y / noise_scale_factor]) + 0.5
                # print(wetness)
                if wetness <= obst_cof:
                    # print((wetness * (1/obst_cof)))
                    self.add(Obstacle(x, y, round((wetness * (1 / obst_cof)) * 3 % 2)))
                elif wetness >= water_cof:
                    self.add(Water(x, y, 0))
                    water_matrix[y][x] = 1
                else:
                    self.add(Ground(x, y, 1))  # round((wetness / obst_cof * 2) % 1)))
        self.wat_matrix = [[0 for _ in range(size_x)] for _ in range(size_y)]
        for y in range(size_y):
            for x in range(size_x):
                self.wat_matrix[y][x] = max(
                    [sqrt((x - i % size_x) ** 2 + (y - i // size_y) ** 2) * water_matrix[i // size_y][
                        i % size_x] / size_x for i
                     in range(size_x * size_y)])
        # print(self.wat_matrix)

    def watering(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                # print(x, y)
                # print(list(filter(lambda cc: cc.x_cord == x and cc.y_cord == y, self.spritedict.keys())))
                s = list(filter(lambda cc: cc.x_cord == x and cc.y_cord == y, self.spritedict.keys()))[0]
                if type(s) == Ground:
                    if random() * self.wat_matrix[y][x] >= 0.6:
                        s.update(x, y)


noise = PerlinNoise(octaves=2)

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 255))
fps = 10
clock = pygame.time.Clock()
new_event = False

scale_factor = 15
bord = Bord()
bord.generate_valley(noise, 26, 26, scale_factor)

if __name__ == '__main__':
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

        bord.watering()
        screen.fill(0)
        bord.draw(screen)
        pygame.display.flip()
