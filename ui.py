import os
import sys
from math import sqrt

import pygame

from random import random

from perlin_noise import PerlinNoise


class UserInterface:
    def __init__(self, width, height, max_energy, energy_per_step, save_callback, reset_callback, next_step_callback,
                 out_of_energy):
        self.width = width
        self.height = height
        self.max_energy = max_energy
        self.energy_per_step = energy_per_step
        self.current_energy = max_energy
        self.level_progress = 0
        self.level_number = 1
        self.move_count = 0
        self.save_callback = save_callback
        self.reset_callback = reset_callback
        self.next_step_callback = next_step_callback
        self.out_of_energy = out_of_energy

        self.level_progress_sprite = pygame.transform.scale(pygame.image.load('images/level_progress.png'), (48, 48))
        self.energy_level_sprite = pygame.transform.scale(pygame.image.load('images/energy_level.png'), (48, 48))
        self.font = pygame.font.Font(None, 30)
        self.buttons = {
            'Сохранить': pygame.Rect(10, self.height - 40, 130, 30),
            'Заново': pygame.Rect(150, self.height - 40, 100, 30),
            'След. шаг': pygame.Rect(260, self.height - 40, 130, 30)
        }

    def blit(self, screen):
        # Draw level progress bar
        progress_bar_rect = pygame.Rect(self.width // 2 - 130, 20, 300, 20)
        pygame.draw.rect(screen, (245, 222, 179), progress_bar_rect)
        pygame.draw.rect(screen, (0, 0, 0), progress_bar_rect, 2)
        filled_progress_rect = pygame.Rect(progress_bar_rect.left, progress_bar_rect.top,
                                           progress_bar_rect.width * self.level_progress, progress_bar_rect.height)
        pygame.draw.rect(screen, (255, 255, 0), filled_progress_rect)
        screen.blit(self.level_progress_sprite, (progress_bar_rect.left - 30, progress_bar_rect.top - 15))

        # Draw energy bar
        energy_bar_rect = pygame.Rect(22, 20, 200, 20)
        pygame.draw.rect(screen, (0, 0, 255), energy_bar_rect)
        pygame.draw.rect(screen, (0, 0, 139), energy_bar_rect, 2)
        filled_energy_rect = pygame.Rect(energy_bar_rect.left, energy_bar_rect.top,
                                         energy_bar_rect.width * (self.current_energy / self.max_energy),
                                         energy_bar_rect.height)
        pygame.draw.rect(screen, (0, 191, 255), filled_energy_rect)
        screen.blit(self.energy_level_sprite, (energy_bar_rect.left - 25, energy_bar_rect.top - 10))
        energy_text = self.font.render(f"{self.current_energy} / -{self.energy_per_step}", True, (255, 0, 0))
        screen.blit(energy_text, (energy_bar_rect.right - energy_text.get_width()-5, energy_bar_rect.bottom + 7))

        # Draw level number
        level_number_text = self.font.render(f'Уровень {self.level_number}', True, (255, 255, 255))
        screen.blit(level_number_text, (self.width - level_number_text.get_width() - 10, 20))

        # Draw moves count
        moves_count_text = self.font.render(f'Шаги: {self.move_count}', True, (255, 255, 255))
        screen.blit(moves_count_text,
                    (self.width - moves_count_text.get_width() - 10, self.height - moves_count_text.get_height() - 10))

        # Draw buttons
        for button_name, rect in self.buttons.items():
            pygame.draw.rect(screen, (173, 255, 47), rect)
            text = self.font.render(button_name.capitalize(), True, (0, 0, 0))
            screen.blit(text, (rect.left + 10, rect.top + 5))

    def next_step(self):
        self.current_energy -= self.energy_per_step
        self.move_count += 1

        if self.current_energy <= 0:
            self.out_of_energy()
            self.current_energy = 0

    def event_process(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button_name, rect in self.buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if button_name == 'Сохранить':
                            self.save_callback()
                        elif button_name == 'Заново':
                            self.reset_callback()
                            self.current_energy = self.max_energy
                            self.level_progress = 0
                            self.move_count = 0
                        elif button_name == 'След. шаг':
                            self.next_step_callback()
                            self.next_step()

    def set_level_progress(self, value):
        if 0 <= value <= 1:
            self.level_progress = value

    def set_level_number(self, level_number):
        self.level_number = level_number


noise = PerlinNoise(octaves=2)

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 255))

ui = UserInterface(width, height, 100, 15, lambda: print("Типа сохранено"), lambda: print('Уровень начат сначала!'),
                   lambda: print('Топ лапками...'), lambda: print('Энергия все!'))

if __name__ == '__main__':
    while running:
        events = list(pygame.event.get())
        ui.event_process(events)
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

        # bord.watering()
        screen.fill(0)
        # bord.draw(screen)
        ui.blit(screen)
        pygame.display.flip()
