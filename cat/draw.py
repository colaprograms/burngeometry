import fpdf
import line
from PIL import Image
import scipy.ndimage
import numpy as np
import scipy as sp

class PATH:
    def __init__(self, pdf):
        self.path = pdf.new_path()

    def __enter__(self):
        path = self.path.__enter__()
        path.style.fill_color = None
        path.style.stroke_width = 0.001
        return path

    def __exit__(self, exc_type, exc_value, traceback):
        self.path.__exit__(exc_type, exc_value, traceback)

def run(draw):
    pdf = fpdf.FPDF(unit='in', format=(10, 10))
    pdf.add_page()
    draw(pdf)
    pdf.output("test.pdf")

def drawline(what, line):
    with PATH(what) as path:
        x0,y0 = line[0]
        path.move_to(x0, y0)
        for j in range(len(line) - 1):
            x1,y1 = line[j+1]
            path.line_to(x1,y1)
        path.close()
        # atashi iya ne

def drawimage(what, img, xscale, yscale, xoff, yoff):
    loop = imageloop(img)
    def rescale(f):
        return xscale*f[0] + xoff, yscale*f[1] + yoff
    for line in loop:
        line = [rescale(it) for it in line]
        #line.append(line[0])
        drawline(what, line)
        print("drawing", line)

def imageloop(img):
    line = {}
    img = np.array(img)
    h,w=img.shape
    for i in range(h+1):
        for j in range(w):
            # horizontal lines
            up = i > 0 and img[i-1,j]
            down = i < h and img[i, j]
            if down < up:
                line[(i,j+1,3)] = (i, j)
            elif up < down:
                line[(i,j,1)] = (i,j+1)
            # iya
    for i in range(h):
        for j in range(w+1):
            # vertical lines
            left = j > 0 and img[i,j-1]
            right = j < w and img[i,j]
            if right < left:
                line[(i,j,2)] = (i+1,j)
            elif left < right:
                line[(i+1,j,0)] = (i,j)
    print(line)
    loops = []
    while line:
        loop = []
        start = next(iter(line))
        loop.append(start)
        cur = line[start]
        way = start[2]
        count = 0
        while cur != start[:2]:
            for off in range(-1,2):
                the = (cur[0], cur[1], (way + off)%4)
                if the in line:
                    loop.append(the)
                    cur = line[the]
                    way = way + off
                    break
            else:
                raise Exception("no way")
            count += 1
            if 100 < count:
                print("breaking loop")
                print("line:", line)
                print("loop:", loop)
                drawit(img)
                raise Exception()
        for it in loop:
            del line[it]
        loop = [it[:2] for it in loop]
        loops.append(loop)
    return loops

def drawit(img):
    for i in range(8):
        for j in range(24):
            print("@" if img[i, j] else " ", end="")
        print("")

def auuuuu(what):
    foo = np.array(Image.open("cat.png"))
    foo = foo[what*8:(what+1)*8, :, 3] != 0
    for i in range(8):
        for j in range(24):
            print("@" if foo[i, j] else " ", end="")
        print("")
    print(imageloop(foo))

def draw(pdf):
    drawline(pdf,
        [(0, 0), (0, 0.001), (13, 0.001), (13, 0)]
    )

    #cat = np.array(Image.open("cat.png"))[:, :, 3]
    #for what in range(24):
        #the = cat[what*8:(what+1)*8, :] != 0
        #drawimage(pdf, the, 0.01, 0.01, 0.2*what, 0.2*what)

    cat = np.load("catdrawin.npy"); cat; cat; cat
    cat = np.pad(cat, [(1,1), (1,1), (1,1)])
    for what in range(cat.shape[0]):
        drawimage(pdf, np.logical_not(cat[what, :, :]), 0.1, 0.1, what%7, 2.4*(what//7))
if __name__ == "__main__":
    run(draw)
