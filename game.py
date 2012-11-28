# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import screen

class Game(object):

    FPS = 60

    def __init__(self):
        pygame.init()
        self.resolution = pygame.display.list_modes()[0]
        self.screen = screen.GameScreen(self)

    def main(self):
        self.display = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False

            # Get the number of milliseconds passed since last tick and convert it to seconds
            time_passed = float(self.clock.tick(self.FPS)) / 1000
            self.screen.tick(time_passed)

            self.display.fill((0, 0, 0))
            self.screen.draw(self.display)
            pygame.display.update()

        self.screen.quit()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.main()
