# -*- coding: utf-8 -*-
import cv
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
        self.scaled_resolution = map(lambda n: int(n * self.scale), self.resolution)
        print "Camera resolution:", self.scaled_resolution
        self.lock = threading.Lock()

        self.camera = cv.CaptureFromCAM(-1)

        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.running = False

        self.camera_image = pygame.Surface(self.resolution)
        self.opencv_image = None
        self.scaled_opencv_image = cv.CreateImage(self.scaled_resolution, 8, 3)
        self.gray_opencv_image = cv.CreateImage(cv.GetSize(self.scaled_opencv_image), 8, 1)
        self.recalc = 0

        self.lower_bound = hsv_to_scalar(215, 0.50, 0.10)
        self.upper_bound = hsv_to_scalar(225, 0.90, 0.5)

    def run(self):
        print "Camera thread started"
        self.running = True

        while self.running:
            self.opencv_image = cv.QueryFrame(self.camera)
            cv.Flip(self.opencv_image, self.opencv_image, 1)

            self.camera_image = cv_to_pygame_surface(self.opencv_image)

            self.recalc = (self.recalc + 1) % 4
            if self.recalc == 0:
                cv.Resize(self.opencv_image, self.scaled_opencv_image, cv.CV_INTER_LINEAR)
                cv.CvtColor(self.scaled_opencv_image, self.scaled_opencv_image, cv.CV_BGR2HSV)

                cv.InRangeS(self.scaled_opencv_image, self.lower_bound, self.upper_bound, self.gray_opencv_image)
                cv.Smooth(self.gray_opencv_image, self.gray_opencv_image, cv.CV_GAUSSIAN, 9, 9)
                cv.Canny(self.gray_opencv_image, self.gray_opencv_image, 50, 200, 3)
                storage = cv.CreateMat(self.scaled_opencv_image.width, 1, cv.CV_32FC3)

                cv.HoughCircles(self.gray_opencv_image, storage, cv.CV_HOUGH_GRADIENT, 2, self.gray_opencv_image.width/2, 200, 100)

                if storage.rows > 0:
                    self.circles = sorted(map(lambda a: (int(a[0][0] / self.scale), int(a[0][1] / self.scale), int(a[0][2] / self.scale)), numpy.asarray(storage)), key=itemgetter(2), reverse=True)
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
    img_rgb = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
    cv.CvtColor(img, img_rgb, cv.CV_BGR2RGB)
    return pygame.image.frombuffer(img_rgb.tostring(), cv.GetSize(img_rgb), 'RGB')

def rad_to_deg(rad):
    return rad / math.pi * 180.0