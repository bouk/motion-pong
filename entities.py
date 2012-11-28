# -*- coding: utf-8 -*-

import pygame
import random

import util

class Paddle(object):

    def __init__(self, screen, x):
        self.screen = screen

        self.height = 0.3
        self.width = 0.01

        self.x = x
        self.y = screen.HEIGHT / 2 - self.height / 2

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0),
         self.screen.translate_rect(self.get_rect()))

    def get_rect(self):
        return ((self.x, self.y), (self.width, self.height))


class Ball(object):

    # Official ping pong ball size 40 mm
    WIDTH = 0.05

    def __init__(self, screen, x, y):
        self.screen = screen

        self.x = x
        self.y = y

        self.xspeed = 1
        self.yspeed = 1

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0),
         self.screen.translate_rect(self.get_rect()))

    def get_rect(self):
        return ((self.x, self.y), (self.WIDTH, self.WIDTH))

    def tick(self, time_passed):
        self.x += self.xspeed * time_passed
        self.y += self.yspeed * time_passed

        if self.x < 0:
            self.x = 0
            self.xspeed = -self.xspeed
        elif self.x + self.WIDTH > self.screen.WIDTH:
            self.x = self.screen.WIDTH - self.WIDTH
            self.xspeed = -self.xspeed

        if self.y < 0:
            self.y = 0
            self.yspeed = -self.yspeed
        elif self.y + self.WIDTH > self.screen.HEIGHT:
            self.y = self.screen.HEIGHT - self.WIDTH
            self.yspeed = -self.yspeed

        if self.xspeed > 0 and util.rect_intersect(self.get_rect(), self.screen.right_paddle.get_rect()):
            self.xspeed = -self.xspeed

        if self.xspeed < 0 and util.rect_intersect(self.get_rect(), self.screen.left_paddle.get_rect()):
            self.xspeed = -self.xspeed
