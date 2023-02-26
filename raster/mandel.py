import PIL.Image, PIL.ImageFilter
import numpy as np
import os

def brot(resolution=1600, xmin=-2.1, xmax=0.8, ymin=-1.2, ymax=1.2):
    xres = int(resolution * (xmax - xmin))
    yres = int(resolution * (ymax - ymin))
    rx = xmin + np.arange(xres) / resolution
    ry = ymin + np.arange(yres) / resolution
    them = 1j * ry[:, None] + rx[None, :]
    that = them.copy()
    for j in range(100):
        that = that*that + them
        that[np.abs(that) > 8] = np.nan
    that = np.isnan(that).astype(np.uint8) * 255
    img = PIL.Image.fromarray(that, mode="L")
    img = img.filter(PIL.ImageFilter.GaussianBlur(radius=2))
    return img

if __name__ == "__main__":
    brot().save("mandel.bmp")
    os.system('potrace -b pdf -t 6000 -a 0.0 -r 500 mandel.bmp')
