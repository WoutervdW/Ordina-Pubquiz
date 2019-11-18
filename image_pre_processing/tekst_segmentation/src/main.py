from glob import glob as glob
from util.image import Image
import environment as env
import cv2 as cv
import os


def main():

    # TODO The way an image is passed. Find something neater for this.
    #  images = sorted(glob(os.path.join(env.SRC_PATH, "*.png")))
    images = sorted(glob(os.path.join(env.SRC_PATH, "002.png")))

    for i_path in images:
        im = Image(i_path)

        # TODO: Test out these different threshold types.
        ### preprocessing
        #im.threshold("su")
        #im.threshold("suplus")
        im.threshold("sauvola")
        #im.threshold("otsu")
        im.segment()


if __name__ == '__main__':
    main()

