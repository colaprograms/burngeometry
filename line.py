import math
from geom import line_line_intersect
from geom import move_until_next_integer

GRID = 1e-8

class pointcombine:
    def __init__(self):
        self.points = {}

    def _get(self, a):
        x, y = a
        x = round(x/GRID)
        y = round(y/GRID)
        for ox in [-1, 0, 1]:
            for oy in [-1, 0, 1]:
                i = self.points.get((x+ox,y+oy))
                if i:
                    return (x+ox,y+oy)
        self.points[(x, y)] = 1
        return (x,y)

    get = _get

class line_process:
    def __init__(self):
        self.lines = []
        self.intersections = {}
        self._raster = {}
        self.resolution = 0.01

    def add_curve(self, line):
        i = len(self.lines)
        self.lines.append(line)
        for j in range(len(line) - 1):
            self.raster_checking_intersections((i, j), line[j], line[j+1])

    def raster_checking_intersections(self, ij, a, b):
        i,j = ij
        def visit(xc, yc):
            if (xc, yc) in self._raster:
                for oi, oj in self._raster[(xc, yc)]:
                    if oi == i:
                        continue
                    print(ij, oi, oj)
                    print(a, b)
                    print(self.lines[oi][oj], self.lines[oi][oj+1])
                    intersection = line_line_intersect(
                        a,
                        b,
                        self.lines[oi][oj],
                        self.lines[oi][oj+1]
                    )

                    if intersection:
                        t, s = intersection
                        x, y = a[0] + t*(b[0] - a[0]), a[1] + t*(b[1] - a[1])
                        self._intersection(oi, oj, s)
                        self._intersection(i, j, t)
            else:
                self._raster[(xc, yc)] = {}
            self._raster[(xc, yc)][(i, j)] = 1
        self.visit_all(visit, a, b)

    def _intersection(self, i, j, t):
        if (i, j) not in self.intersections:
            self.intersections[(i, j)] = []
        self.intersections[(i, j)].append(t)

    def visit_all(self, visit, a, b):
        # fill in every square touched by line
        x0, y0 = a
        x1, y1 = b
        x0 /= self.resolution
        y0 /= self.resolution
        x1 /= self.resolution
        y1 /= self.resolution
        dx = x1 - x0
        dy = y1 - y0
        def add(t):
            xc = math.floor(x0 + t*dx)
            yc = math.floor(y0 + t*dy)
            visit(xc, yc)
            return xc, yc

        if dx == 0 and dy == 0:
            add(0)
            return

        t = 0
        while True:
            xc, yc = add(t)
            dt_x = move_until_next_integer(xc, dx)
            dt_y = move_until_next_integer(yc, dy)
            dt = min(dt_x, dt_y)
            # try to deal with lines with rational slopes
            t += dt / 2
            add(t)
            if 1 < t:
                t = 1
                break

            t += dt / 2
            if 1 < t:
                t = 1
                add(t)
                break

    def output(self):
        out = []
        them=pointcombine()
        for i in range(len(self.lines)):
            it = []
            def add(a):
                a = them.get(a)
                it.append(a)
            a = self.lines[i][0]
            for j in range(len(self.lines[i])-1):
                b = self.lines[i][j+1]
                if (i, j) not in self.intersections:
                    add(a)
                    a = b
                    pass
                else:
                    the = sorted(self.intersections[i, j])
                    x0, y0 = a
                    x1, y1 = b
                    dx = x1 - x0
                    dy = y1 - y0
                    for t in the:
                        add(a)
                        a = x0 + t*dx, y0 + t*dy
                    add(a)
                    a = b
            add(a)
            out.append(it)
        return out

class decompose_by_angle:
    def __init__(self):
        self.out = {}

    def add_curve(self, line):
        def add(a, dir, b):
            if a in self.out:
                self.out[a][b] = dir
            else:
                self.out[a] = {b: dir}
        for j in range(len(line)-1):
            x0, y0 = line[j]
            x1, y1 = line[j+1]
            if (x0,y0) == (x1,y1):
                continue
            dir = math.atan2(y0 - y1, x1 - x0) / 2 / math.pi
            add((x0, y0), dir, (x1, y1))

    def _next(self, a, ccwfrom):
        assert a in self.out
        best = None
        what = None
        for b in self.out[a]:
            dir = self.out[a][b] - ccwfrom
            dir = dir - math.floor(dir)
            if best is None or dir < best:
                best = dir
                what = b
        return what

    def unloop(self):
        leastx = None
        for x,y in self.out:
            if leastx is None or x < leastx[0]:
                leastx = x,y

        if leastx is None:
            return
        a = leastx
        dir = 0.75
        loop = []
        while True:
            print(a)
            loop.append(a)
            b = self._next(a, dir)
            del self.out[a][b]
            if not self.out[a]:
                del self.out[a]
            a = b
            if a == leastx:
                break
        return loop

def decompose_curves_into_loops(line):
    pass

def scaledown(lines):
    pass
    pass
    return [[(x*GRID,y*GRID) for (x,y) in line] for line in lines]

def run():
    a = line_process()
    #a.add_curve([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    #a.add_curve([(0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5)])
    a.add_curve(list(reversed([(0, 0), (1, 1), (2, 2), (0, 2), (0, 0)])))
    a.add_curve([(0, 2.01), (1, 1.01), (2, 0.01), (0.01, 0.01), (0, 2.01)])
    whatev=a.output()
    print(whatev)
    dba = decompose_by_angle()
    for line in whatev:
        dba.add_curve(line)
    print(dba.out)
    it = dba.unloop()
    return scaledown([it])

if __name__ == "__main__":
    a = line_process()
    a.add_curve([(0, 0), (1, 1), (2, 2), (0, 2), (0, 0)])
    a.add_curve([(0, 2.01), (1, 1.01), (2, 0.01), (0.01, 0.01), (0, 2.01)])
    whatev=a.output()
    print(whatev)
    dba = decompose_by_angle()
    for line in whatev:
        dba.add_curve(line)
    print(dba.out)
    it = dba.unloop()
    print(it)
    #print(a.intersections)
