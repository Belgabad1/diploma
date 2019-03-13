import math


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def get_straight_coeff(x1, y1, x2, y2):
    A = y2 - y1
    B = x1 - x2
    C = y1 * x2 - x1 * y2
    return A, B, C


def get_circle_point(x1, y1, x2, y2, radius):
    A, B, C = get_straight_coeff(x1, y1, x2, y2)
    swap = False
    if A == 0:
        swap = True
        A, B = B, A
        x2, y2 = y2, x2
        x1, y1 = y1, x1
    if A != 0:
        a = (B ** 2 / A ** 2 + 1)
        b = (2 * C * B / A ** 2 + 2 * x2 * B / A - 2 * y2)
        c = (C * C / A ** 2 + x2 ** 2 + 2 * x2 * C / A + y2 ** 2 - radius ** 2)
        D = b * b - 4 * a * c
        res_y1 = (-b + math.sqrt(D)) / (2 * a)
        res_x1 = (-C - B * res_y1) / A
        res_y2 = (-b - math.sqrt(D)) / (2 * a)
        res_x2 = (-C - B * res_y2) / A
        if get_distance(x1, y1, res_x1, res_y1) < get_distance(x1, y1, res_x2, res_y2):
            if swap:
                res_x1, res_y1 = res_y1, res_x1
            return res_x1, res_y1
        else:
            if swap:
                res_x2, res_y2 = res_y2, res_x2
            return res_x2, res_y2


def get_angle(x1, y1, x2, y2):
    A, B, C = get_straight_coeff(x1, y1, x2, y2)
    if B:
        return math.atan(-A / B)
    else:
        if (A > 0):
            return -math.pi / 2
        else:
            return math.pi / 2
