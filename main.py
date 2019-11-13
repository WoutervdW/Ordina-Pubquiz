import sys
from app.Model import Model
from app.Model import DecoderType
from app.SamplePreprocessor import preprocess
from app.DataLoader import Batch
import cv2


def infer(_model, fn_img):
    """
    recognize text in image provided by file path
    """
    img = preprocess(cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE), Model.img_size)
    batch = Batch(None, [img])
    (recognized, probability) = _model.inferBatch(batch, True)
    print('Recognized:', '"' + recognized[0] + '"')
    print('Probability:', probability[0])


if __name__ == "__main__":
    print("De officiele Ordina pub-quiz antwoord vinder")
    image_to_read = 'data/test.png'
    # TODO Nu wordt Best path gekozen Waarschijnlijk gebruiken we 1 ding. Kijken of andere decortypes beter werken.
    decoder_type = DecoderType.BestPath

    model = Model(open('model/charList.txt').read(), decoder_type, mustRestore=True)
    infer(model, image_to_read)

