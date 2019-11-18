import os
import cv2
from word_segmentation import word_segmentation, prepare_img


def main():
    """reads images from data/ and outputs the word-segmentation to out/"""

    input_folder = "data/"
    output_folder = "out/"

    # read input images from 'in' directory
    img_files = os.listdir(input_folder)
    for (i, f) in enumerate(img_files):
        print('Segmenting words of sample %s' % f)

        # read image, prepare it by resizing it to fixed height and converting it to grayscale
        img = prepare_img(cv2.imread(input_folder + '%s' % f), 50)

        # execute segmentation with given parameters
        # -kernelSize: size of filter kernel (odd integer)
        # -sigma: standard deviation of Gaussian function used for filter kernel
        # -theta: approximated width/height ratio of words, filter function is distorted by this factor
        # - min_area: ignore word candidates smaller than specified area
        res = word_segmentation(img, kernel_size=25, sigma=11, theta=7, min_area=100)

        # write output to 'out/inputFileName' directory
        if not os.path.exists(output_folder + '%s' % f):
            os.mkdir(output_folder + '%s' % f)

        # iterate over all segmented words
        print('Segmented into %d words' % len(res))
        for (j, w) in enumerate(res):
            (word_box, word_img) = w
            (x, y, w, h) = word_box
            # save word
            cv2.imwrite(output_folder + '%s/%d.png' % (f, j), word_img)
            # draw bounding box in summary image
            cv2.rectangle(img, (x, y), (x + w, y + h), 0, 1)

        # output summary image with bounding boxes around words
        cv2.imwrite(output_folder + '%s/summary.png' % f, img)


if __name__ == '__main__':
    main()
