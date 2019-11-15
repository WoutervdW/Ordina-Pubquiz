import numpy as np
import cv2

# read
img = cv2.imread('tekst_5.png', cv2.IMREAD_GRAYSCALE)

# increase contrast
pxmin = np.min(img)
pxmax = np.max(img)
imgContrast = (img - pxmin) / (pxmax - pxmin) * 255

# increase line width
kernel = np.ones((3, 3), np.uint8)
imgMorph = cv2.erode(imgContrast, kernel, iterations = 1)

# write
cv2.imwrite('tekst_6.png', imgMorph)

# TODO find out how to determine what contract works best simple solution -> untill probability is highest
"""
handgeschreven:
normal (handgeschreven.png) => rondgessinsron (0.00012758702)
2 => hondgesteon (0.0049874294)
3 => handgeeteven (0.045786206)
4 =? handgeeteven (0.06114233)
5 => handgeestreven (0.024851194) (lower probability)
6 => handgeestrmsen (0.0033688515)

simple solution -> until probability is highest not secure since he will be more sure with too thick lines.
tekst:
normal (tekst.png) => reist (0.04586883)
2 => test (0.2911346)
3 => test (0.21319734)
4 => tesk (0.0928262)
5 => tst (0.065483086)
6 => #sk (0.1730404)
"""