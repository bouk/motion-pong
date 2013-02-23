# -*- coding: utf-8 -*-
import cv
import cv2
import math
import numpy
from operator import itemgetter
import pygame.image
import threading
import time

class CameraThread(threading.Thread):

    def __init__(self, resolution, scale):
        threading.Thread.__init__(self)

        self.resolution = resolution
        self.circles = list()
        self.scale = scale
        self.scaled_resolution = tuple(map(lambda n: int(n * self.scale), self.resolution))

        self.lock = threading.Lock()

        self.camera = cv2.VideoCapture(0)

        self.camera.set(cv.CV_CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.running = False

        self.camera_image = pygame.Surface(self.resolution)
        self.opencv_image = numpy.ndarray((self.resolution[1], self.resolution[0], 3), numpy.uint8)
        self.scaled_opencv_image = numpy.ndarray((self.scaled_resolution[1], self.scaled_resolution[0], 3), numpy.uint8)
        self.gray_opencv_image = numpy.ndarray((self.scaled_resolution[1], self.scaled_resolution[0], 1), numpy.uint8)
        self.recalc = 0

        self.lower_bound = hsv_to_scalar(130, 0.20, 0.1)
        self.upper_bound = hsv_to_scalar(160, 0.75, 0.9)

    def run(self):
        self.running = True

        while self.running:
            result, self.opencv_image = self.camera.read()
            cv2.flip(src=self.opencv_image, flipCode=1, dst=self.opencv_image)

            self.camera_image = cv_to_pygame_surface(self.opencv_image)

            self.recalc = (self.recalc + 1) % 4
            if self.recalc == 0:
                cv2.resize(self.opencv_image, self.scaled_resolution, self.scaled_opencv_image)

                cv2.cvtColor(src=self.scaled_opencv_image, dst=self.scaled_opencv_image, code=cv.CV_BGR2HSV)

                cv2.inRange(self.scaled_opencv_image, self.lower_bound, self.upper_bound, self.gray_opencv_image)
                cv2.GaussianBlur(src=self.gray_opencv_image, ksize=(3, 3), sigmaX=9, dst=self.gray_opencv_image)
                cv2.Canny(self.gray_opencv_image, 50, 200, self.gray_opencv_image, 3)
                storage = cv2.HoughCircles(image=self.gray_opencv_image, method=cv.CV_HOUGH_GRADIENT, dp=2, minDist=self.gray_opencv_image.shape[0] / 2, param1=200, param2=100)

                if storage != None and len(storage[0]) > 0:
                    self.circles = sorted(map(lambda a: (int(a[0] / self.scale), int(a[1] / self.scale), int(a[2] / self.scale)), storage[0]), key=itemgetter(2), reverse=True)
                else:
                    self.circles = list()

    def stop(self):
        self.running = False


def hsv_to_scalar(h, s, v):
    return cv.Scalar(int(h / 2), int(s * 255), int(v * 255))

def is_inside(point, rect):
    return rect[0][0] < point[0] < rect[0][0] + rect[1][0] and rect[0][1] < point[1] < rect[0][1] + rect[1][1]

def rect_intersect(rect_a, rect_b):
    for i in ((rect_a, rect_b), (rect_b, rect_a)):
        if (is_inside(i[0][0], i[1])
         or is_inside((i[0][0][0], i[0][0][1] + i[0][1][1]), i[1])
         or is_inside((i[0][0][0] + i[0][1][0], i[0][0][1]), i[1])
         or is_inside((i[0][0][0] + i[0][1][0], i[0][0][1] + i[0][1][1]), i[1])):
            return True
    return False

def cv_to_pygame_surface(img):
    img_rgb = numpy.ndarray(img.shape, img.dtype)
    cv2.cvtColor(src=img, dst=img_rgb, code=cv.CV_BGR2RGB)

    return pygame.image.frombuffer(img_rgb.tostring(), (img.shape[1], img.shape[0]), 'RGB')

def rad_to_deg(rad):
    return rad / math.pi * 180.0