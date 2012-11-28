# -*- coding: utf-8 -*-

from Box2D import *
import pygame
import pygame.camera
from pygame.locals import *

import controller
import entities

class Screen(object):

    def __init__(self, game):
        self.game = game
        self.ticks = 0

    def tick(self, time_passed):
        self.ticks += 1

    def draw(self, surface):
        raise NotImplementedError()

    def quit(self, surface):
        pass


class MenuScreen(Screen):

    def __init__(self, game):
        Screen.__init__(self, game)

    def tick(self, time_passed):
        pass

    def draw(self, surface):
        pass


class GameScreen(Screen):
    '''
    This screen is at the top of a game, managing the paddles, balls and webcam
    '''

    # Official ping pong table size
    # 108 inch long by 60 inch wide
    WIDTH = float(27.43)
    HEIGHT = float(15.24)

    WEBCAM_RESOLUTION = (640, 480)
    WEBCAM_SCALED_RESOLUTION = (128, 96)

    def __init__(self, game):
        Screen.__init__(self, game)

        self.world = b2World(gravity=(0, 0), doSleep=True)
        self.upper_border = self.world.CreateBody(position=(self.WIDTH/2, -1))
        self.upper_border.CreatePolygonFixture(box=(self.WIDTH/2, 1), friction=0.0, restitution=1.0)

        self.lower_border = self.world.CreateBody(position=(self.WIDTH/2, self.HEIGHT + 1))
        self.lower_border.CreatePolygonFixture(box=(self.WIDTH/2, 1), friction=0.0, restitution=1.0)

        pygame.camera.init()
        camera_name = pygame.camera.list_cameras()[0]
        self.camera = pygame.camera.Camera(camera_name, self.WEBCAM_RESOLUTION)
        self.camera.start()
        self.camera_image = pygame.Surface(self.WEBCAM_RESOLUTION)
        self.scaled_camera_image = pygame.Surface(self.WEBCAM_SCALED_RESOLUTION)

        self.left_paddle = entities.Paddle(self, 0.1)
        self.right_paddle = entities.Paddle(self, self.WIDTH - 0.11)

        # self.left_controller = controller.WebcamController(self, self.left_paddle, (15, 40, 40), (20, 255, 255))
        self.left_controller = controller.KeyboardController(self, self.left_paddle, K_w, K_s)
        self.right_controller = controller.KeyboardController(self, self.right_paddle, K_i, K_k)

        self.balls = []
        self.balls.append(entities.Ball(self,
             x=self.WIDTH / 2 - entities.Ball.RADIUS,
             y=self.HEIGHT / 2 - entities.Ball.RADIUS))

        # Calculate screen ratio and compare it with the size of the table to determine table position on screen
        screen_ratio = float(game.resolution[0]) / game.resolution[1]
        field_ratio = self.WIDTH / self.HEIGHT

        if screen_ratio > field_ratio:
            # Screen ratio is wider than field, set display height to screen height
            self.x_offset = int((abs(screen_ratio - field_ratio) * game.resolution[0])) / 4
            self.y_offset = 0
            self.pixel_to_meter_ratio = float(game.resolution[1]) / self.HEIGHT
        else:
            # Screen ratio is higher than field, set display width to screen width
            self.x_offset = 0
            self.y_offset = int((abs(screen_ratio - field_ratio) * game.resolution[1])) / 4
            self.pixel_to_meter_ratio = float(game.resolution[0]) / self.WIDTH

    def quit(self):
        self.camera.stop()

    def tick(self, time_passed):
        Screen.tick(self, time_passed)

        if self.ticks % 2 == 0:
            self.camera_image = pygame.transform.flip(self.camera.get_image(), True, False)
            pygame.transform.smoothscale(self.camera_image,
             self.WEBCAM_SCALED_RESOLUTION,
             self.scaled_camera_image)

        self.left_controller.tick(time_passed)
        self.right_controller.tick(time_passed)

        self.world.Step(1.0/60.0, 10, 2)

        for ball in self.balls[:]:
            ball.tick(time_passed)

    def draw(self, surface):
        surface.blit(pygame.transform.scale(self.camera_image, self.game.resolution), (0, 0))

        self.left_paddle.draw(surface)
        self.right_paddle.draw(surface)

        # pygame.draw.circle(surface,
        #  (255, 255, 0, 128),
        #  (self.translate(self.left_controller.x_pos * self.WIDTH),
        #   self.translate(self.left_controller.y_pos * self.HEIGHT)),
        #  20)

        for ball in self.balls:
            ball.draw(surface)

    def translatexy(self, x, y):
        return (self.translate(x) + self.x_offset, self.translate(y) + self.y_offset)

    def translate_xy_width_height(self, x, y, w, h):
        return (self.translatexy(x, y), (self.translate(w), self.translate(h)))

    def translate_rect(self, rect):
        return self.translate_xy_width_height(rect[0][0], rect[0][1], rect[1][0], rect[1][1])

    def translate(self, value):
        return int(value * self.pixel_to_meter_ratio)
