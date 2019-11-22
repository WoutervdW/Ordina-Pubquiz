import math

import cv2
import numpy as np


def word_segmentation(img, kernel_size=251, sigma=11, theta=7, min_area=0):
    """
    Scale space technique for word segmentation proposed by R. Manmatha: http://ciir.cs.umass.edu/pubfiles/mm-27.pdf

    Args:
        img: grayscale uint8 image of the text-line to be segmented.
        kernel_size: size of filter kernel, must be an odd integer.
        sigma: standard deviation of Gaussian function used for filter kernel.
        theta: approximated width/height ratio of words, filter function is distorted by this factor.
        min_area: ignore word candidates smaller than specified area.

    Returns:
        List of tuples. Each tuple contains the bounding box and the image of the segmented word.
    """

    # apply filter kernel
    kernel = create_kernel(kernel_size, sigma, theta)
    img_filtered = cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_REPLICATE).astype(np.uint8)
    (_, img_threshold) = cv2.threshold(img_filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_threshold = 255 - img_threshold

    # find connected components. OpenCV: return type differs between OpenCV2 and 3
    # TODO see which version applies and check if the if else construction can be removed.
    if cv2.__version__.startswith('3.'):
        (_, components, _) = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        (components, _) = cv2.findContours(img_threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # append components to result
    res = []
    for c in components:
        # skip small word candidates
        if cv2.contourArea(c) < min_area:
            continue
        # append bounding box and image of word to result list
        curr_box = cv2.boundingRect(c)  # returns (x, y, w, h)
        (x, y, w, h) = curr_box
        curr_img = img[y:y + h, x:x + w]
        res.append((curr_box, curr_img))

    # return list of words, sorted by x-coordinate
    return sorted(res, key=lambda entry: entry[0][0])


def prepare_img(img, height):
    """
    convert given image to grayscale image (if needed) and resize to desired height
    """
    # TODO check if this is enough, the images seem to be very clear maybe more pre processing is needed.
    assert img.ndim in (2, 3)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # TODO find our if resizing with a factor is needed.
    # h = img.shape[0]
    # factor = height / h
    return cv2.resize(img, dsize=None, fx=1, fy=1)


def create_kernel(kernel_size, sigma, theta):
    """
    create anisotropic filter kernel according to given parameters
    """
    assert kernel_size % 2  # must be odd size
    half_size = kernel_size // 2

    kernel = np.zeros([kernel_size, kernel_size])
    sigma_x = sigma
    sigma_y = sigma * theta

    for i in range(kernel_size):
        for j in range(kernel_size):
            x = i - half_size
            y = j - half_size

            exp_term = np.exp(-x ** 2 / (2 * sigma_x) - y ** 2 / (2 * sigma_y))
            x_term = (x ** 2 - sigma_x ** 2) / (2 * math.pi * sigma_x ** 5 * sigma_y)
            y_term = (y ** 2 - sigma_y ** 2) / (2 * math.pi * sigma_y ** 5 * sigma_x)

            kernel[i, j] = (x_term + y_term) * exp_term

    kernel = kernel / np.sum(kernel)
    return kernel

