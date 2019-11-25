import numpy as np
import cv2
import operator


def show_image(img):
    """
    This will show the image and the program will continue when a key is pressed. Can be used for debugging
    """
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def find_corners_left_contour(polygon):
    """
    returns the 4 corners of the given polygon.
    If the points are within a certain range we will save it
    """
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))

    return [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]


def pre_process_image(answer_image, skip_dilate=False):
    """
    The image can be pre processed to improve the quality of the line segmentation.
    The lines can be made thicker by adding contract and noise can be removed.
    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html#dilation
    """
    img = cv2.cvtColor(answer_image, cv2.COLOR_BGR2GRAY)
    # TODO play around with these variables for better results it should remove noise
    proc = cv2.GaussianBlur(img.copy(), (9, 9), 0)
    proc = cv2.adaptiveThreshold(proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    proc = cv2.bitwise_not(proc, proc)

    # TODO play around with dilate. It makes the lines thicker but first the noise should be as good as gone
    if not skip_dilate:
        kernel = np.ones((5, 5), np.uint8)
        proc = cv2.dilate(proc, kernel)
    return proc


def line_segmentation_temp(answer_image, save_image=False, image_path="lines/", image_name="scan"):
    # New strategy. First find the points on the left side and then on the right side.
    # Than take the points together and find the lines.
    # processed = pre_process_image(answer_image, False)
    height, width, _ = answer_image.shape
    # We choose 800 because that will definitely have all the points within the image
    # and the posibility of having a similar looking area is minimized.
    left_side = answer_image[0:height, 0:800]
    right_side = answer_image[0:height, (width-700):width]

    left_side_img = left_side.copy()
    left_side_processed = pre_process_image(left_side_img, False)
    contours_left_side, _ = cv2.findContours(left_side_processed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(left_side_img, contours_left_side, -1, (0, 255, 0), thickness=5)
    # show_image(left_side_img)

    # The blocks will have a specific area which we will look for.
    left_block_contours = []
    for c in contours_left_side:
        area = cv2.contourArea(c)
        if 80000 < area < 90000:
            left_block_contours.append(c)

    cv2.drawContours(left_side_img, left_block_contours, -1, (255, 0, 0), thickness=10)
    # show_image(left_side_img)

    right_side_img = right_side.copy()
    right_side_processed = pre_process_image(right_side_img, False)
    contours_right_side, _ = cv2.findContours(right_side_processed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(right_side_img, contours_right_side, -1, (0, 255, 0), thickness=5)
    cv2.imwrite("left_side_img_contour.png", left_side_img)

    # show_image(right_side_img)

    right_block_contours = []
    for c in contours_right_side:
        area = cv2.contourArea(c)
        if 50000 < area < 60000:
            print(area)
            right_block_contours.append(c)

    cv2.drawContours(right_side_img, right_block_contours, -1, (255, 0, 0), thickness=10)
    cv2.imwrite("right_side_img_contour.png", right_side_img)

    # show_image(processed)
    # show_image(left_side)
    # show_image(right_side)


