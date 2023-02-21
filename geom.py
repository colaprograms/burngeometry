import math

def move_until_next_integer(x0, dx):
    if dx == 0:
        return math.inf
    elif dx > 0:
        return (1 + math.floor(x0) - x0) / dx
    else:
        return (x0 - math.ceil(x0) + 1) / -dx

def line_line_intersect(a1, b1, a2, b2):
    # a1.x + t(b1.x-a1.x) = a2.x + s(b2.x-a2.x)
    # a1.y + t(b1.y-a1.y) = a2.y + s(b2.y-a2.y)
    ax1, ay1 = a1
    bx1, by1 = b1
    ax2, ay2 = a2
    bx2, by2 = b2
    dx1 = bx1 - ax1
    dy1 = by1 - ay1
    dx2 = bx2 - ax2
    dy2 = by2 - ay2
    det = dx1 * dy2 - dy1 * dx2
    tun = ax2 * dy2 - ay2 * dx2 - ax1 * dy2 + ay1 * dx2
    sun = -(ax1 * dy1 - ay1 * dx1 - ax2 * dy1 + ay2 * dx1)
    if abs(det) < 1e-12:
        print(det, tun, sun)
        if abs(tun) < 1e-12 and abs(sun) < 1e-12:
            raise Exception("lines are touching and pointing in the same direction?")
        else:
            return None
    t=tun/det
    s=sun/det
    if t < 0 or 1 < t or s < 0 or 1 < s:
        return None
    return t, s

def check_line_line_intersection(a1, b1, a2, b2, t, s):
    ax1, ay1 = a1
    bx1, by1 = b1
    ax2, ay2 = a2
    bx2, by2 = b2
    x1 = ax1 + t*(bx1 - ax1)
    x2 = ax2 + s*(bx2 - ax2)
    y1 = ay1 + t*(by1 - ay1)
    y2 = ay2 + s*(by2 - ay2)
    if 1e-12 < abs(x1 - x2) or 1e-12 < abs(y1 - y2):
        print("a1.x + t(b1.x - a1.x) =", ax1 + t*(bx1 - ax1))
        print("a2.x + s(b2.x - a2.x) =", ax2 + s*(bx2 - ax2))
        print("a1.y + t(b1.y - a1.y) =", ay1 + t*(by1 - ay1))
        print("a2.y + s(b2.y - a2.y) =", ay2 + s*(by2 - ay2))

def test_line_line_intersect(count):
    import random
    what = lambda: (random.random(), random.random())
    for j in range(count):
        a1 = what()
        b1 = what()
        a2 = what()
        b2 = what()
        it = line_line_intersect(a1, b1, a2, b2)
        if it is not None:
            t, s = it
            check_line_line_intersection(a1, b1, a2, b2, t, s)

if __name__ == "__main__":
    test_line_line_intersect(1000000)
