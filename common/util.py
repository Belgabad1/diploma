import math


ERR = 1e-6

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


def get_angle(x1, y1, x2, y2):
    A, B, C = get_straight_coeff(x1, y1, x2, y2)
    if math.fabs(B) > ERR:
        angle = math.atan(-A / B)
        if A < -ERR:
            angle += math.pi
        elif B > ERR:
            angle += math.pi
        return angle
    else:
        if (A > ERR):
            return math.pi / 2
        else:
            return 3 * math.pi / 2


def rotate_point_by_angle(x, y, x1, y1, r, delta_angle):
    angle = get_angle(x, y, x1, y1)
    return x + r * math.cos(angle + delta_angle), y + r * math.sin(angle + delta_angle)


def is_crossing(line1, line2):
    A1, B1, C1 = get_straight_coeff(line1[0], line1[1], line1[2], line1[3])
    A2, B2, C2 = get_straight_coeff(line2[0], line2[1], line2[2], line2[3])
    y = (C2 * A1 - C1 * A2) / (A2 * B1 - A1 * B2)
    return (
        min(line1[1], line1[3]) + 0.01 < y < max(line1[1], line1[3]) - 0.01 and
        min(line2[1], line2[3]) + 0.01 < y < max(line2[1], line2[3]) - 0.01
    )


def get_crossing_number(lines):
    n = len(lines)
    crossing_number = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                crossing_number += is_crossing(lines[i], lines[j])
    return crossing_number


def min_length(result):
    ans = None
    for i in range(len(result)):
        for j in range(len(result)):
            if i != j:
                dist = get_distance(result[i][0], result[i][1], result[j][0], result[j][1])
                if not ans:
                    ans = dist
                else:
                    ans = min(ans, dist)
    return ans
