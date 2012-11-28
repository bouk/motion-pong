import pygame
import pygame.camera
from pygame.locals import *

WEBCAM_RESOLUTION = (640, 480)
SCALED_RESOLUTION = (128, 96)

def main():
    pygame.init()
    pygame.camera.init()

    camera_name = pygame.camera.list_cameras()[0]
    camera = pygame.camera.Camera(camera_name, WEBCAM_RESOLUTION)
    camera.start()

    resolution = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    image = pygame.Surface((640, 360))
    hsv_image = pygame.Surface(SCALED_RESOLUTION)
    camera_image = pygame.Surface(WEBCAM_RESOLUTION)
    font = pygame.font.Font(None, 17)

    clock = pygame.time.Clock()
    running = True
    while True:
        clock.tick()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                camera.stop()
                pygame.quit()
                running = False
        if not running:
            break

        camera_image = camera.get_image(camera_image)
        pygame.transform.smoothscale(camera_image, SCALED_RESOLUTION, hsv_image)

        image.blit(camera_image, (0, -60))
        center_x_pos = 0
        center_y_pos = 0
        count = 0
        center2_x_pos = 0
        center2_y_pos = 0
        count2 = 0

        for x in xrange(SCALED_RESOLUTION[0]):
            for y in xrange(SCALED_RESOLUTION[1]):
                h, s, v, a = hsv_image.get_at((x, y)).hsva
                if 15 < h < 20 and 75 < s < 85 and 25 < v < 85:
                    center_x_pos += x
                    center_y_pos += y
                    count += 1
                elif 80 < h < 100 and 40 < s < 60:
                    center2_x_pos += x
                    center2_y_pos += y
                    count2 += 1
        if count:
            center_x_pos = (center_x_pos / count) * resolution[0] / SCALED_RESOLUTION[0]
            center_y_pos = (center_y_pos / count) * resolution[1] / SCALED_RESOLUTION[1]
        if count2:
            center2_x_pos = (center2_x_pos / count2) * resolution[0] / SCALED_RESOLUTION[0]
            center2_y_pos = (center2_y_pos / count2) * resolution[1] / SCALED_RESOLUTION[1]

        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(image, resolution), (0, 0))
        text = font.render("HSV: %s" % ", ".join(map(str, hsv_image.get_at((64, 48)).hsva)), True, (255, 255, 255), (0, 0, 0))
        # text = font.render("FPS: %s" % str(clock.get_fps()), True, (255, 255, 255), (0, 0, 0))
        screen.blit(text, text.get_rect())

        pygame.draw.circle(screen, (255, 255, 0, 128), (center_x_pos, center_y_pos), 20)
        pygame.draw.circle(screen, (255, 0, 255, 128), (center2_x_pos, center2_y_pos), 20)

        pygame.display.update()

if __name__ == '__main__':
    main()
