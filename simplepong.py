import pygame
from pygame.locals import *

FPS = 60
RESOLUTION = (0, 0)

class Paddle:
    WIDTH = 20
    HEIGHT = 200

    def __init__(self, key_up, key_down, x_pos):
        self.key_up = key_up
        self.key_down = key_down
        self.position = [x_pos, 0]

    def update(self, time):
        if pygame.key.get_pressed()[self.key_up]:
            self.position[1] -= float(time)/1000 * 500

        if pygame.key.get_pressed()[self.key_down]:
            self.position[1] += float(time)/1000 * 500

        if self.position[1] < Paddle.WIDTH:
            self.position[1] = Paddle.WIDTH
        if self.position[1] > RESOLUTION[1] - Paddle.HEIGHT - Paddle.WIDTH:
            self.position[1] = RESOLUTION[1] - Paddle.HEIGHT - Paddle.WIDTH

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0, 255), pygame.Rect(self.position[0], self.position[1], Paddle.WIDTH, Paddle.HEIGHT))


def main():
    global RESOLUTION

    pygame.init()
    RESOLUTION = pygame.display.list_modes()[0]

    screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
    entities = [Paddle(K_w, K_s, 20), Paddle(K_i, K_k, RESOLUTION[0] - Paddle.WIDTH - 20)]
    clock = pygame.time.Clock()

    running = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                running = False

        if not running:
            break

        time_passed = clock.tick(FPS)

        for e in entities[:]:
            e.update(time_passed)
        
        screen.fill((255, 255, 255, 255))

        for e in entities:
            e.draw(screen)

        pygame.display.update()

if __name__ == '__main__':
    main()
