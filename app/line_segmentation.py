import numpy as np
import cv2
import operator
import os
from view.models import SubAnswerGiven


def show_image(img):
    """
    This will show the image and the program will continue when a key is pressed. Can be used for debugging
    """
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def find_corners_contour(polygon, offset=0, add_x=False):
    """
    returns the 4 corners of the given polygon.
    If the points are within a certain range we will save it
    """
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))

    if add_x:
        # TODO Make the (width-1500) a bit more nicer (if you change it in 1 place you might forget it here)
        polygon[top_left][0][0] = polygon[top_left][0][0] + offset
        polygon[top_right][0][0] = polygon[top_right][0][0] + offset
        polygon[bottom_right][0][0] = polygon[bottom_right][0][0] + offset
        polygon[bottom_left][0][0] = polygon[bottom_left][0][0] + offset

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


def distance_between(p1, p2):
    """Returns the scalar distance between two points"""
    return np.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


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

    # The ratio is an easy indication if it is the line we want or not 10 is a loose bound for that ratio (around 15)
    # TODO maybe incorporate the ratio
    # TODO Maybe also find and save the square before it (it holds the question number)
    # TODO We can determine the question based on when the line is found or based on the number in front of it?
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


def find_corners_center(corners_left, corners_right):
    # top left of the full part is the top left of the left part
    top_left_full = corners_left[3]
    # top right of the full part is the top right of the right part
    top_right_full = corners_right[2]
    # bottom right of the full part is the bottom right of the right part
    bottom_right_full = corners_right[1]
    # bottom left of the full part is the bottom left of the left part
    bottom_left_full = corners_left[0]
    corners_full = [bottom_left_full, bottom_right_full, top_right_full, top_left_full]
    return corners_full


def line_segmentation(answer_image_original, save_image=False, image_path="lines/", image_name="scan", db=None):
    # New strategy. First find the points on the left side and then on the right side.
    # Than take the points together and find the lines.
    # processed = pre_process_image(answer_image_original, False)
    height, width, _ = answer_image_original.shape
    # We choose 1500 because that will definitely have all the points within the image
    # and the posibility of having a similar looking area is minimized.
    # TODO Make the (width-900) a bit more nicer (if you change it in 1 place you might forget it here)
    offset_range = 900
    left_side = answer_image_original[0:height, 0:offset_range]
    right_side = answer_image_original[0:height, (width-offset_range):width]
    # show_image(right_side)

    left_side_img = left_side.copy()

    # We draw a fake line over the image, this is so we can find the corners by finding areas with a certain size
    cv2.line(left_side_img, (offset_range-10, 0), (offset_range-10, height), (0, 0, 0), 10)

    left_side_processed = pre_process_image(left_side_img, False)
    contours_left_side, _ = cv2.findContours(left_side_processed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(left_side_img, contours_left_side, -1, (0, 255, 0), thickness=5)

    # show_image(left_side_img)
    # The blocks will have a specific area which we will look for.
    left_block_contours = []
    for c in contours_left_side:
        area = cv2.contourArea(c)
        # Area is about 100000 up to 1400000
        if 80000 < area < 190000:
            left_block_contours.append(c)

    cv2.drawContours(left_side_img, left_block_contours, -1, (255, 0, 0), thickness=10)
    # show_image(left_side_img)

    # cv2.imwrite("out/" + image_name + "_left.png", left_side_img)
    right_side_img = right_side.copy()

    # We draw a fake line over the image, this is so we can find the corners by finding areas with a certain size
    cv2.line(right_side_img, (10, 0), (10, height), (0, 0, 0), 10)

    right_side_processed = pre_process_image(right_side_img, False)
    contours_right_side, _ = cv2.findContours(right_side_processed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(right_side_img, contours_right_side, -1, (0, 255, 0), thickness=5)

    right_block_contours = []
    for c in contours_right_side:
        area = cv2.contourArea(c)
        # Area is about 50000 up to 80000
        if 30000 < area < 130000:
            right_block_contours.append(c)

    cv2.drawContours(right_side_img, right_block_contours, -1, (255, 0, 0), thickness=10)
    # show_image(right_side_img)
    # cv2.imwrite("out/" + image_name + "_right.png", right_side_img)

    # We assume that the answer template had the correct format so we expect that the left and right side both found
    # and equal amount of results. If this is not the case we return nothing and the program fails for this sheet.
    if len(left_block_contours) != len(right_block_contours):
        print("There was a problem with the line detection. "
              "The left and right side blocks that were found are not equal")
        return None

    lines = []
    for x in range(0, len(left_block_contours)):
        corners_left = find_corners_contour(left_block_contours[x])
        corners_right = find_corners_contour(right_block_contours[x], width - offset_range, True)
        # We will use the original image to crop from.

        corners_full = find_corners_center(corners_left, corners_right)
        cropped_full = crop_and_warp(answer_image_original, corners_full)

        # We also pass the line index along wiht this collection of lines. This is so that for the word recognition
        # part we can easily identify which line it is.
        finished_line = [cropped_full, x]
        lines.append(finished_line)

        # Save the line image to the database!
        # convert the image to byte array so it can be saved in the database
        answer = cropped_full.tostring()
        # create an Image object to store it in the database
        # shape = answer_image
        line_width = len(cropped_full)
        line_height = len(cropped_full[0])

        if db is not None:
            print("save line to database with width %s and height %s" % (line_width, line_height))
            # TODO fill in the other details as well! (not just the image)
            new_answer = SubAnswerGiven(
                answer_id=1,
                answer_given="",
                correct=False,
                confidence=0.0,
                answer_image=answer,
                image_width=line_width,
                image_height=line_height
            )
            # add the object to the database session
            db.session.add(new_answer)
            # commit the session so that the image is stored in the database
            db.session.commit()

        if save_image:
            path = image_path + image_name
            if not os.path.exists(path):
                os.makedirs(path)
            # save (or show) the image if the folder is empty (for tests)
            # show_image(finished_line[0])
            cv2.imwrite(path + "/line_" + str(x) + ".png", finished_line[0])

    print('done all ' + str(len(left_block_contours)) + ' lines')
    return lines

