# -*- coding: utf-8 -*-

from Box2D import *
import pygame

class Controller(object):

    def __init__(self, screen, paddle):
        self.screen = screen
        self.paddle = paddle

    def tick(self, time_passed):
        pass

class UndefeatableController(Controller):

    def tick(self, time_passed):
        pass

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

    def __init__(self, screen, paddle, bottom_hsv, top_hsv):
        Controller.__init__(self, screen, paddle)
        self.bottom_hsv = bottom_hsv
        self.top_hsv = top_hsv

        self.x_pos = 0
        self.y_pos = 0
        self.count = 0

    def tick(self, time_passed):
        self.x_pos = 0
        self.y_pos = 0
        self.count = 0

        for x in xrange(self.screen.WEBCAM_SCALED_RESOLUTION[0]):
            for y in xrange(self.screen.WEBCAM_SCALED_RESOLUTION[1]):
                h, s, v, a = self.screen.scaled_camera_image.get_at((x, y)).hsva
                if (self.bottom_hsv[0] < h < self.top_hsv[0]
                 and self.bottom_hsv[1] < s < self.top_hsv[1]
                 and self.bottom_hsv[2] < v < self.top_hsv[2]):
                    self.x_pos += x
                    self.y_pos += y
                    self.count += 1

        if self.count:
            self.x_pos = float(self.x_pos) / self.count / self.screen.WEBCAM_SCALED_RESOLUTION[0]
            self.y_pos = float(self.y_pos) / self.count / self.screen.WEBCAM_SCALED_RESOLUTION[1]
            # self.paddle.y = self.y_pos * self.screen.HEIGHT
