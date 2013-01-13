# -*- coding: utf-8 -*-

from Box2D import *
import pygame

import random
import util


class Paddle(object):

    HEIGHT = 4.0
    WIDTH = 0.2

    def __init__(self, screen, x, mirror=False):
        self.screen = screen
        self.body = screen.world.CreateKinematicBody(position=(x, screen.HEIGHT / 2 - self.HEIGHT / 2))
        self.mirror = mirror
        self.body.CreatePolygonFixture(box=(self.WIDTH / 2, self.HEIGHT / 2), friction=0.1, restitution=1.1, density=1.0)

        self.image = pygame.image.load('images/paddle.png')
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.screen.translate(self.WIDTH), self.screen.translate(self.HEIGHT)))
        if self.mirror:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        surface.blit(self.image, self.screen.translatexy(self.body.position[0] - self.WIDTH / 2, self.body.position[1] - self.HEIGHT / 2))


class Ball(object):

    RADIUS = 0.5
    STARTING_VELOCITY = b2Vec2(10, 10)

    def __init__(self, screen, x, y):
        self.screen = screen
        self.body = screen.world.CreateDynamicBody(position=(x, y), bullet=True)
        self.body.CreateCircleFixture(radius=self.RADIUS, friction=1.0, restitution=1.0, density=2.0)
        self.body.ApplyLinearImpulse(self.STARTING_VELOCITY, self.body.worldCenter)
        self.body.angularDamping = 1
        self.body.angularVelocity = 20

        self.image = pygame.image.load('images/ball.png')
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.screen.translate(self.RADIUS * 2), self.screen.translate(self.RADIUS * 2)))
        self.shift = 0.0

    def draw(self, surface):
        angle = util.rad_to_deg(self.body.angle)
        rotated_image = pygame.transform.rotate(self.image, angle)
        position = map(lambda x: x - rotated_image.get_width() / 2, self.screen.translatexy(self.body.position[0], self.body.position[1]))

        surface.blit(rotated_image, position)

    def tick(self, time_passed):
        if self.body.position[0] - self.RADIUS > self.screen.WIDTH or self.body.position[0] + self.RADIUS < 0:
            if self.body.position[0] - self.RADIUS > self.screen.WIDTH:
                self.screen.right_health -= 1
            else:
                self.screen.left_health -= 1

            self.screen.health_changed()

            self.body.transform = (b2Vec2(self.screen.WIDTH / 2, self.screen.HEIGHT / 2), 0)
            self.body.linearVelocity = b2Vec2(0, 0)
            self.body.angularVelocity = 0
            self.body.ApplyLinearImpulse(self.STARTING_VELOCITY, self.body.worldCenter)
