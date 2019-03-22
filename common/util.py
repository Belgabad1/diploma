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


def get_rect_center(x1, y1, x2, y2, top=False):
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    if x1 == x2:
        return x1, (y1 + y2) / 2
    if y1 == y2:
        return (x1 + x2) / 2, y2
    if top:
        if y1 < y2:
            return x1, y2
        elif y1 > y2:
            return x2, y1
    if y1 < y2:
        return x2, y1
    elif y1 > y2:
        return x1, y2


def get_rect_width_height(x1, y1, x2, y2):
    width, height = abs(x2 - x1), abs(y2 - y1)
    if width == 0:
        width = 20
        height /= 2
    if height == 0:
        height = 20
        width /= 2
    return width, height


def get_rect_point(x1, y1, x2, y2, top=False):
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    x, y = get_rect_center(x1, y1, x2, y2, top)
    width, height = get_rect_width_height(x1, y1, x2, y2)
    x, y = x - width, y - height
    if x1 == x2:
        if top:
            angle = 0
        else:
            angle = 180
    elif y1 == y2:
        if top:
            angle = 90
        else:
            angle = 270
    else:
        if top:
            angle = 0
        else:
            angle = 180
        if y2 < y1:
            angle += 90
    return x, y, angle


def get_angle(x1, y1, x2, y2):
    A, B, C = get_straight_coeff(x1, y1, x2, y2)
    if B:
        return math.atan(-A / B)
    else:
        if (A > 0):
            return -math.pi / 2
        else:
            return math.pi / 2


def get_arc_point(x1, y1, x2, y2, top, radius):
    x, y = get_rect_center(x1, y1, x2, y2, top)
    width, height = get_rect_width_height(x1, y1, x2, y2)
    if y2 != y1:
        y_direct = (y2 - y1) / abs(y2 - y1)
        if (top and x2 < x1) or (not top and x2 > x1):
            y_direct *= -1
    else:
        y_direct = (x2 - x1) / abs(x2 - x1)
    y_direct = -1
    best_x, best_y, best_dist = 0, 0, 20
    for i in range(4, 5):
        circle_x = y_direct * math.sqrt(radius ** 2 - i ** 2) + x2
        dist = abs(1 - ((circle_x - x) ** 2 / (width ** 2) + (y2 + i - y) ** 2 / (height ** 2)))
        if dist < best_dist:
            best_x, best_y, best_dist = circle_x, y2 + i, dist
    return best_x, best_y
