import os
import math
import cv2
import numpy as np
from app.line_segmentation import crop_and_warp


def get_words_image(line_image, multiply_factor, res):
    words = []
    index = 0
    for (j, w) in enumerate(res):
        (word_box, word_img) = w
        (x, y, w, h) = word_box
        x_new = (x * multiply_factor) + 5
        y_new = y * multiply_factor
        width_new = w * multiply_factor
        height_new = h * multiply_factor
        rect = find_rect(x_new, y_new, width_new, height_new)
        # We want to apply the crop and saving on the original line image
        cropped = crop_and_warp(line_image[0], rect)
        words.append([cropped, line_image[4], index])
        index += 1
    return words


def save_word_image(output_folder, sheet_name, line_image, multiply_factor, res):
    path = output_folder + sheet_name + "/line_" + str(line_image[4]) + "/words"
    if not os.path.exists(path):
        os.makedirs(path)
    index = 0
    for (j, w) in enumerate(res):
        (word_box, word_img) = w
        (x, y, w, h) = word_box
        # save word
        # We also have to take into account that we removed the bars on the side by slicing the image with '5'
        # We will add this to the new bounding box.
        x_new = (x * multiply_factor) + 5
        y_new = y * multiply_factor
        width_new = w * multiply_factor
        height_new = h * multiply_factor
        rect = find_rect(x_new, y_new, width_new, height_new)
        # We want to apply the crop and saving on the original line image
        cropped = crop_and_warp(line_image[0], rect)
        cv2.imwrite(path + '/word_' + str(index) + '.png', cropped)
        cv2.rectangle(line_image[0], (int(x_new), int(y_new)),
                      (int(x_new + width_new), int(y_new + height_new)), 0, 1)

        # draw bounding box in summary image
        cv2.rectangle(line_image[0], (x, y), (x + w, y + h), 0, 1)
        index += 1

    # output summary image with bounding boxes around words
    cv2.imwrite(path + "/line_" + str(line_image[4]) + '_summary.png', line_image[0])


def word_segmentation(line_image, kernel_size=25, sigma=11, theta=7, min_area=1000):
    """
    Scale space technique for word segmentation proposed by R. Manmatha: http://ciir.cs.umass.edu/pubfiles/mm-27.pdf

    Args:
        line_image: grayscale uint8 image of the text-line to be segmented it has 4 line options, we choose 'center'.
        kernel_size: size of filter kernel, must be an odd integer.
        sigma: standard deviation of Gaussian function used for filter kernel.
        theta: approximated width/height ratio of words, filter function is distorted by this factor.
        min_area: ignore word candidates smaller than specified area.

    Returns:
        List of tuples. Each tuple contains the bounding box and the image of the segmented word.
    """

    # apply filter kernel
    kernel = create_kernel(kernel_size, sigma, theta)
    img_filtered = cv2.filter2D(line_image, -1, kernel, borderType=cv2.BORDER_REPLICATE).astype(np.uint8)
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
        curr_img = line_image[y:y + h, x:x + w]
        res.append((curr_box, curr_img))

    # return list of words, sorted by x-coordinate
    return sorted(res, key=lambda entry: entry[0][0])


def find_rect(x, y, w, h):
    top_left = [x, y+h]
    top_right = [x+w, y+h]
    bottom_right = [x+w, y]
    bottom_left = [x, y]
    return [bottom_left, bottom_right, top_right, top_left]


def show_image(img):
    """
    This will show the image and the program will continue when a key is pressed. Can be used for debugging
    """
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def prepare_image(img, height):
    """convert given image to grayscale image (if needed) and resize to desired height"""
    assert img.ndim in (2, 3)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h = img.shape[0]
    factor = height / h
    resized = cv2.resize(img, dsize=None, fx=factor, fy=factor)
    without_bars = resized[:, 5:-5]
    return without_bars


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

