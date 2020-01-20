import os
import math
import cv2
import numpy as np
from app.line_segmentation import crop_and_warp
from view.models import Word
from app.sample_preprocessor import preprocess
from app.Model import Model
from view.models import SubAnswerGiven
from view.models import SubAnswer
from view.models import Question
from view.models import Variant
from view.models import Answersheet
from view.models import AnswerGiven
from view.models import Team
from app.DataLoader import Batch
from view.config import InputConfig


def increase_contrast(img):
    # increase contrast
    pxmin = np.min(img)
    pxmax = np.max(img)
    imgContrast = (img - pxmin) / (pxmax - pxmin) * 255

    # increase line width
    kernel_contrast = np.ones((4, 4), np.uint8)
    imgMorph = cv2.erode(imgContrast, kernel_contrast, iterations=1)

    return imgMorph


def infer(_model, word_image):
    """
    recognize text in image provided by file path
    """
    # image = fn_img
    fn_img = cv2.cvtColor(word_image, cv2.COLOR_BGR2GRAY)

    # We will set a threshold for the gray lines to become clear black for the recognition
    # ret, fn_img = cv2.threshold(fn_img, 220, 255, cv2.THRESH_BINARY)
    # We increase the thickness of the lines to make the program better at reading the letters
    fn_img = increase_contrast(fn_img)

    image = preprocess(fn_img, Model.img_size)
    batch = Batch([image])
    (recognized, probability) = _model.infer_batch(batch, False)
    print('Recognized:', '"' + recognized[0] + '"')
    if probability is not None:
        print('Probability:', probability[0])
    return recognized, probability


def read_word_from_image(image_to_read, model):
    results = infer(model, image_to_read)
    return results


def save_word_details(line_image, multiply_factor, res, number_box_size, db=None, model=None, team_id=None, question_number=0, subanswer_number=-1):
    words = []
    index = 0
    predicted_line = ""
    for (j, w) in enumerate(res):
        (word_box, word_img) = w
        (x, y, w, h) = word_box
        x_new = (x * multiply_factor) + (number_box_size * multiply_factor)
        y_new = y * multiply_factor
        width_new = w * multiply_factor
        height_new = h * multiply_factor
        rect = find_rect(x_new, y_new, width_new, height_new)
        # We want to apply the crop and saving on the original line image
        cropped = crop_and_warp(line_image[0], rect)
        words.append([cropped, line_image[1], index])

        if db is not None:
            # Save the word image to the database!
            # convert the image to byte array so it can be saved in the database
            word_image = cropped.tostring()
            # create an Image object to store it in the database
            # TODO fill in the other details as well! (not just the image)
            word_width = len(cropped)
            word_height = len(cropped[0])
            print("save the word to the database with width %s and height %s" % (word_width, word_height))

            read_results = read_word_from_image(cropped, model)
            print("saving word with recognized word " + read_results[0][0])
            predicted_line = predicted_line + read_results[0][0] + " "
            new_word = Word(
                line_id=line_image[2],
                word_recognised=read_results[0],
                word_image=word_image,
                image_width=word_width,
                image_height=word_height
            )
            # add the object to the database session
            db.session.add(new_word)
            # commit the session so that the image is stored in the database
            db.session.commit()

        index += 1

    if db is not None:
        if question_number != 0:
            print("This line is a valid question")
            # We assume there is exactly 1 question for the given question number
            question = Question.query.filter_by(questionnumber=question_number).first()
            print("question number " + str(question_number))

            sub_answers = SubAnswer.query.filter_by(question_id=question.id).order_by(SubAnswer.id.asc())
            print("the length of the subanswers for question " + str(question_number))
            sub_answer_index = 0
            sub_answer = sub_answers.first()
            for s in sub_answers:
                print('subanswer id ' + str(s.id))
                sub_answer_index += 1
                if subanswer_number == sub_answer_index:
                    sub_answer = s
            print("the total number of subanswers for question %s is %s" % (question_number, sub_answer_index))
            print("saving the line on question %s with variant with subanswerid %s" % (question_number, str(sub_answer.id)))

            variant = Variant.query.filter_by(subanswer_id=sub_answer.id).first()

            print("sub_answer id " + str(sub_answer.id))
            print("variant id " + str(variant.id))
            team = Team.query.filter_by(id=team_id).first()
            answered_by = team.get_team_name()
            print("team_id  " + str(team_id))
            print("answered_by " + str(answered_by))
            # correct is always false at first and can be set to True later
            # TODO @Sander: person_id is now always the same, how will this be determined?
            #     checkedby="answerchecker",
            # corr_answer = variant.get_answer(),
            #     answered_by=answered_by,
            #     confidence=words_results[1],
            answergiven = AnswerGiven.query.filter_by(question_id=question.id).first()
            if answergiven is None:
                answergiven = AnswerGiven(
                    question_id=question.id,
                    team_id=team.id
                )
                db.session.add(answergiven)
                db.session.commit()
            print("ANSWERGIVEN:")
            print(answergiven.question_id)
            sub_answer_given = SubAnswerGiven(
                answergiven_id=answergiven.id,
                corr_answer_id=sub_answer.id,
                person_id=2,
                correct=False,
                line_id=line_image[2],
                read_answer=predicted_line
            )
            db.session.add(sub_answer_given)
            db.session.commit()
    return words


def save_word_image(output_folder, sheet_name, line_image, multiply_factor, res, number_box_size=60):
    path = output_folder + sheet_name + "/line_" + str(line_image[1]) + "/words"
    if not os.path.exists(path):
        os.makedirs(path)
    index = 0
    for (j, w) in enumerate(res):
        (word_box, word_img) = w
        (x, y, w, h) = word_box
        # save word
        # We also have to take into account that we removed the bars on the left side by removing number_box_size
        # We will add this to the new bounding box.
        x_new = (x * multiply_factor) + (number_box_size * multiply_factor)
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
    cv2.imwrite(path + "/line_" + str(line_image[1]) + '_summary.png', line_image[0])


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


def prepare_image(img, height, number_box_size):
    """convert given image to grayscale image (if needed) and resize to desired height"""
    assert img.ndim in (2, 3)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h = img.shape[0]
    factor = height / h
    resized = cv2.resize(img, dsize=None, fx=factor, fy=factor)
    without_bars = resized
    number_image = resized
    without_bars = without_bars[:, number_box_size:]
    number_image = number_image[:, :number_box_size]
    # We will remove the left part, which always has the same size and is never needed
    return without_bars, number_image


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

