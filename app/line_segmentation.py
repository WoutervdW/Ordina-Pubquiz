"""
The given input will be a png image with predetermined black rectangular boundaries around the answer.
The line segmentation can be done in a few different ways
- The lines are always the same and pre determined, so we can separate the image on fixed points
    - The easiest way (probably the first we will implement)
    - This could have as a problem that the line separation will be off if the image is slanted in some way
        - Do tests to see if this happens at all in any way when scanning a bunch of files fast.
    - Look for the lines and separate after finding the lines
        - A bit more work but has as benefit that it is more robust.
    - It can be improved in multiple ways:
        - find the intersection within a certain bound since we know what to look for
        - assume as certain degree for the line, if the degree is too much we won't use it
    - look for the rectangular answer boundaries and extract all of the boundaries you find out of the image.
        - most robust answer, should work even if the sheet is slanted
        - Can even work if the method of scanning is changed to taking photo images
        - https://medium.com/@neshpatel/solving-sudoku-part-ii-9a7019d196a2

:param arg1: the name of the image (later changed to the image that is given in the previous part of the program)
:return: All lines in their own image (later changed to images in memory passed on to the next part)
"""
import numpy as np
import cv2
import operator


def crop_and_warp(img, crop_rect):
    """
    Crops and warps a rectangular section from an image
    """

    # Rectangle described by top left, top right, bottom right and bottom left points
    top_left, top_right, bottom_right, bottom_left = crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]

    # Explicitly set the data type to float32 or `getPerspectiveTransform` will throw an error
    src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')

    max_width = max([distance_between(top_right, top_left), distance_between(bottom_right, bottom_left)])
    max_height = max([distance_between(bottom_left, top_left), distance_between(bottom_right, top_right)])

    ratio = max_width/max_height
    # The ratio is an easy indication if it is the line we want or not 10 is a loose bound for that ratio (around 15)
    # TODO Maybe also find and save the square before it (it holds the question number)
    # TODO We can determine the question based on when the line is found or based on the number in front of it
    if ratio > 10:
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]], dtype="float32")

        # compute the perspective transform matrix and then apply it
        m = cv2.getPerspectiveTransform(src, dst)
        # Even though we assume that the image is not slanted in any way, or if it is slanted, very little
        # We will still warp the line to be a straight rectangle.
        warped = cv2.warpPerspective(img, m, (int(max_width), int(max_height)))

        return warped
    else:
        return None


def find_corners_contour(polygon):
    """
    returns the 4 corners of the given polygon.
    The polygon is a large collection of points, we only want the 4 corner points for our program
    """
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))

    return [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]


def show_image(img):
    """
    This will show the image and the program will continue when a key is pressed. Can be used for debugging
    """
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


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


def distance_between(p1, p2):
    """Returns the scalar distance between two points"""
    return np.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


def line_segmentation(answer_image, save_image=False, image_path="lines/", image_name="scan"):
    processed = pre_process_image(answer_image, False)

    contours, _ = cv2.findContours(processed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    line_section = []
    # We know the area of the lines will always be close to the same depending on how much the image is slanted.
    # Otherwise all the really small boundaries will be taken as well.
    for c in contours:
        area = cv2.contourArea(c)
        if 100000 < area < 1000000:
            line_section.append(c)

    # TODO now the image is saved with a index, maybe find some better way to define the lines.
    # TODO The lines are saved from bottom to top. It should probably be passed from top to bottom.
    lines = []
    index = 0
    for line in line_section:
        corners = find_corners_contour(line)
        # We will use the original image to crop from.
        cropped = crop_and_warp(answer_image, corners)
        # Make sure it is an actual line
        if cropped is not None:
            lines.append(cropped)
            index += 1
            if save_image:
                # show_image(cropped)
                cv2.imwrite(image_path + image_name + "_line_" + str(index) + ".png", cropped)
    print('done all ' + str(index) + ' lines')
    return lines

