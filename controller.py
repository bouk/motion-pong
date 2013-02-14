# -*- coding: utf-8 -*-

from Box2D import *
import pygame
import entities
import cv

class Controller(object):

    def __init__(self, screen, paddle):
        self.screen = screen
        self.paddle = paddle

    def tick(self, time_passed):
        pass

class UndefeatableController(Controller):

    def tick(self, time_passed):
        if len(self.screen.balls) > 0:
            self.paddle.body.transform = (b2Vec2(self.paddle.body.position[0], self.screen.balls[0].body.position[1]), 0)

class KeyboardController(Controller):

    SPEED = 1.0
    FORCE = 10

    def __init__(self, screen, paddle, key_up, key_down):
        Controller.__init__(self, screen, paddle)
        self.key_up = key_up
        self.key_down = key_down

    def tick(self, time_passed):
        if pygame.key.get_pressed()[self.key_up]:
            self.paddle.body.linearVelocity = b2Vec2(0, -self.FORCE)
        elif pygame.key.get_pressed()[self.key_down]:
            self.paddle.body.linearVelocity = b2Vec2(0, self.FORCE)
        else:
            self.paddle.body.linearVelocity = b2Vec2(0, 0)

        Controller.tick(self, time_passed)

class WebcamController(Controller):

    def __init__(self, screen, paddle, left_side):
        Controller.__init__(self, screen, paddle)
        self.left_side = left_side

    def tick(self, time_passed):
        candidates = filter(lambda circle: circle[0] <= self.screen.game.WEBCAM_RESOLUTION[0] / 2 if self.left_side else circle[0] > self.screen.game.WEBCAM_RESOLUTION[0] / 2, self.screen.game.camera_thread.circles)

        if len(candidates):
            first_circle = candidates[0]
            y = (float(first_circle[1]) / self.screen.pixel_to_meter_ratio)

            self.paddle.body.transform = (b2Vec2(self.paddle.body.position[0], y), 0)