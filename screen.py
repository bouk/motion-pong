# -*- coding: utf-8 -*-

from Box2D import *
import pygame
import cv
from pygame.locals import *
import os

import controller
import entities
import util

class Screen(object):

    def __init__(self, game):
        self.game = game
        self.ticks = 0

    def tick(self, time_passed):
        self.ticks += 1

    def draw(self, surface):
        raise NotImplementedError()

    def quit(self):
        pass


class MenuScreen(Screen):

    def __init__(self, game):
        Screen.__init__(self, game)
        self.selected = 0

        def multiplayer(menu):
            menu.game.screen = RegularGameScreen(menu.game)
            menu.game.screen.left_controller = controller.KeyboardController(menu.game.screen, menu.game.screen.left_paddle, K_w, K_s)
            menu.game.screen.right_controller = controller.KeyboardController(menu.game.screen, menu.game.screen.right_paddle, K_i, K_k)
            pygame.mixer.music.stop()

        def singleplayer(menu):
            menu.game.screen = RegularGameScreen(menu.game)
            menu.game.screen.left_controller = controller.KeyboardController(menu.game.screen, menu.game.screen.left_paddle, K_w, K_s)
            menu.game.screen.right_controller = controller.UndefeatableController(menu.game.screen)
            pygame.mixer.music.stop()

        def quitgame(menu):
            menu.game.running = False

        self.menu_items = [
        {
            'text': "1 Player",
            'command': singleplayer
        },
        {
            'text': "2 Player",
            'command': multiplayer
        },
        {
            'text': "Quit",
            'command': quitgame
        }
        ]

        self.font = pygame.font.SysFont("monospace", 30)
        self.logo = pygame.image.load(os.path.join(game.IMAGE_DIR, 'logo.png'))
        self.logo = self.logo.convert_alpha()
        self.menu_backdrop = pygame.image.load(os.path.join(game.IMAGE_DIR, 'menu_backdrop.png'))
        self.menu_backdrop = self.menu_backdrop.convert_alpha()

        self.kioskscreen = KioskGameScreen(game)
        pygame.mixer.music.load(os.path.join(game.MUSIC_DIR, 'menu.mp3'))
        pygame.mixer.music.play(-1)

    def tick(self, time_passed):
        self.kioskscreen.tick(time_passed)

        if self.game.just_held(K_DOWN):
            self.selected = (self.selected + 1) % len(self.menu_items)

        if self.game.just_held(K_UP):
            self.selected = (self.selected + len(self.menu_items) - 1) % len(self.menu_items)

        if self.game.just_held(K_RETURN) or self.game.just_held(K_KP_ENTER):
            self.menu_items[self.selected]['command'](self)

    def draw(self, surface):
        self.kioskscreen.draw(surface)

        ypos = 0
        surface.blit(self.logo, (surface.get_width() / 2 - self.logo.get_width() / 2, ypos))

        ypos += self.logo.get_height() + 10

        for key, item in enumerate(self.menu_items):
            position = (surface.get_width() / 2 - self.menu_backdrop.get_width() / 2, ypos)
            surface.blit(self.menu_backdrop, position)

            color = (255, 255, 255)
            text = str(item['text'])
            if key == self.selected:
                color =  (255, 255, 0)
                text = '> ' + text + ' <'

            text = self.font.render(text, True, color)
            position = (surface.get_width() / 2 - text.get_width() / 2, ypos + self.menu_backdrop.get_height() / 2 - text.get_height() / 2)
            surface.blit(text, position)

            ypos += self.menu_backdrop.get_height()

    def quit(self):
        self.kioskscreen.quit()


class TextScreen(Screen):

    def __init__(self, game, text):
        Screen.__init__(self, game)
        self.text = text
        self.font = pygame.font.SysFont('monospace', 50)
        self.time = 0.0

    def draw(self, surface):
        surface.fill((0, 0, 0))
        image = self.font.render(self.text + " " + str(int(5 - self.time)), True, (255, 255, 0))
        position = (surface.get_width() / 2 - image.get_width() / 2, surface.get_height() / 2 - image.get_height() / 2)
        surface.blit(image, position)

    def tick(self, time_passed):
        if self.time > 5.0:
            self.game.screen = MenuScreen(self.game)

        self.time += time_passed


class GameScreen(Screen):
    '''
    This screen is manages the paddles, balls and webcam
    '''

    # Official ping pong table size
    # 108 inch long by 60 inch wide
    WIDTH = 27.43
    HEIGHT = 15.24

    START_HEALTH = 4

    def __init__(self, game):
        Screen.__init__(self, game)

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

        self.world = b2World(gravity=(0, 0), doSleep=True)
        self.upper_border = self.world.CreateBody(position=(self.WIDTH / 2, -1))
        self.upper_border.CreatePolygonFixture(box=(self.WIDTH / 2, 1), friction=0.0, restitution=1.0)

        self.lower_border = self.world.CreateBody(position=(self.WIDTH / 2, self.HEIGHT + 1))
        self.lower_border.CreatePolygonFixture(box=(self.WIDTH / 2, 1), friction=0.0, restitution=1.0)

        self.left_paddle = entities.Paddle(self, 0.1)
        self.right_paddle = entities.Paddle(self, self.WIDTH - 0.11, mirror=True)

        self.left_health = self.right_health = self.START_HEALTH

        self.balls = [
            entities.Ball(self,
                x=self.WIDTH / 2 - entities.Ball.RADIUS,
                y=self.HEIGHT / 2 - entities.Ball.RADIUS)
        ]

    def tick(self, time_passed):
        Screen.tick(self, time_passed)

        self.left_controller.tick(time_passed)
        self.right_controller.tick(time_passed)

        self.world.Step(time_passed, 10, 2)

        for ball in self.balls[:]:
            ball.tick(time_passed)

    def draw(self, surface):
        surface.blit(
            pygame.transform.scale(
                self.game.camera_thread.camera_image,
                self.game.resolution),
            (0, 0))

        for circle in self.game.camera_thread.circles:
            pygame.draw.circle(surface,
                (255, 255, 0, 128),
                (circle[0], circle[1]),
                circle[2])

        self.left_paddle.draw(surface)
        self.right_paddle.draw(surface)

        for ball in self.balls:
            ball.draw(surface)

    def translatexy(self, x, y):
        return (self.translate(x) + self.x_offset, self.translate(y) + self.y_offset)

    def translate_xy_width_height(self, x, y, w, h):
        return (self.translatexy(x, y), (self.translate(w), self.translate(h)))

    def translate_rect(self, rect):
        return self.translate_xy_width_height(
                rect[0][0],
                rect[0][1],
                rect[1][0],
                rect[1][1])

    def translate(self, value):
        return int(value * self.pixel_to_meter_ratio)

    def health_changed(self):
        pass


class RegularGameScreen(GameScreen):

    def draw(self, surface):
        GameScreen.draw(self, surface)

        # Draw UI
        left_health_ratio = self.left_health / float(self.START_HEALTH)
        left_health_width = left_health_ratio * 300
        right_health_ratio = self.right_health / float(self.START_HEALTH)
        right_health_width = right_health_ratio * 300

        surface.fill((255, 0, 0), (0, self.game.resolution[1] - 100, left_health_width, 40))
        surface.fill((255, 0, 0), (self.game.resolution[0] - right_health_width, self.game.resolution[1] - 100, right_health_width, 40))

    def health_changed(self):
        if self.left_health <= 0:
            self.game.screen = TextScreen(self.game, "Right player won!")
        elif self.right_health <= 0:
            self.game.screen = TextScreen(self.game, "Left player won!")


class KioskGameScreen(GameScreen):

    def __init__(self, game):
        GameScreen.__init__(self, game)
        self.left_controller = controller.UndefeatableController(self, self.left_paddle)
        self.right_controller = controller.UndefeatableController(self, self.right_paddle)
