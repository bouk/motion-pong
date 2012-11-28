# -*- coding: utf-8 -*-

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