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
        # pygame.transform.laplacian(camera_image, hsv_image)

        image.blit(camera_image, (0, -60))
        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(image, resolution), (0, 0))
        screen.blit(hsv_image, (0, 0))
        text = font.render("FPS: %s" % str(clock.get_fps()), True, (255, 255, 255), (0, 0, 0))


        pygame.display.update()

if __name__ == '__main__':
    main()
