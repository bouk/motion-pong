# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import os

import screen
import util

class Game(object):

    FPS = 30

    WEBCAM_RESOLUTION = (1280, 720)
    WEBCAM_SCALE = 0.5

    MUSIC_DIR = 'music'
    IMAGE_DIR = 'images'

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        self.resolution = pygame.display.list_modes()[0]
        self.screen = None
        self.prev_keys = pygame.key.get_pressed()
        self.running = False

        # Initialise camera
        self.camera_thread = util.CameraThread(self.WEBCAM_RESOLUTION, self.WEBCAM_SCALE)
        self.camera_thread.start()

    def main(self):
        self.display = pygame.display.set_mode(self.resolution) # , pygame.FULLSCREEN
        self.clock = pygame.time.Clock()

        self.running = True
        self.font = pygame.font.SysFont('monospace', 15)
        # self.screen = screen.GameScreen(self)

        self.screen = screen.MenuScreen(self)

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.running = False

            # Get the number of milliseconds passed since last tick and convert it to seconds
            time_passed = float(self.clock.tick(self.FPS)) / 1000
            self.screen.tick(time_passed)

            self.display.fill((255, 255, 255))
            self.screen.draw(self.display)

            text = self.font.render(str(self.clock.get_fps()), True, (255, 255, 0))
            self.display.blit(text, (100, 100))
            pygame.display.update()
            self.prev_keys = pygame.key.get_pressed()

        self.screen.quit()
        self.camera_thread.stop()
        pygame.quit()

    def just_held(self, keycode):
        return pygame.key.get_pressed()[keycode] and not self.prev_keys[keycode]

if __name__ == '__main__':
    game = Game()
    game.main()
