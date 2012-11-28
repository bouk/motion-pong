# -*- coding: utf-8 -*-

from Box2D import *
import pygame
import random

import util

class Paddle(object):

    HEIGHT = 3
    WIDTH = 0.1

    def __init__(self, screen, x):
        self.screen = screen
        self.body = screen.world.CreateBody(position=(x, screen.HEIGHT/2 - self.HEIGHT/2))
        self.body.CreatePolygonFixture(box=(self.WIDTH/2, self.HEIGHT/2), friction=0.0, restitution=1.0, density=10.0)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0),
         self.screen.translate_rect(self.get_rect()))

    def get_rect(self):
        return ((self.body.position[0] - self.WIDTH/2, self.body.position[1] - self.HEIGHT/2), (self.WIDTH, self.HEIGHT))


class Ball(object):

    # Official ping pong ball size 40 mm
    RADIUS = 0.5

    def __init__(self, screen, x, y):
        self.screen = screen
        self.body = screen.world.CreateDynamicBody(position=(x, y), bullet=True)
        self.body.CreateCircleFixture(radius=self.RADIUS, friction=0.0, restitution=2.0, density=1.0)
        self.body.ApplyLinearImpulse(b2Vec2(10, 0), self.body.worldCenter)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0),
         self.screen.translate_rect(self.get_rect()))

    def get_rect(self):
        return ((self.body.position[0] - self.RADIUS, self.body.position[1] - self.RADIUS), (self.RADIUS*2, self.RADIUS*2))

    def tick(self, time_passed):
        pass
