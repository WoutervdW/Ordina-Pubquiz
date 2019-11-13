import numpy as np


class Batch:
    """
    batch containing images and ground truth texts
    """

    def __init__(self, image):
        self.image = np.stack(image, axis=0)

