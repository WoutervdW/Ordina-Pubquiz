- pyTesseract: state-of-the-art OCR for printed text.
	- https://pypi.org/project/pytesseract/
	- makkelijk aan te roepen via python

- simpleHTR: implementatie in TensorFlow van neuraal netwerk om karakters in losse handgeschreven woorden te herkennen.
	- https://github.com/githubharald/SimpleHTR
	- https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5
	- 

- LineHTR: Versie van simpleHTR voor gehele regels.	
	- https://github.com/lamhoangtung/LineHTR
	- 

- Line separation:
	- https://stackoverflow.com/questions/46282691/opencv-cropping-handwritten-lines-line-segmentation
	- https://www.researchgate.net/publication/222568946_Handwritten_document_image_segmentation_into_text_lines_and_words

- Word segmentation:
    implementation of the paper
    Scale space technique for word segmentation proposed by R. Manmatha: http://ciir.cs.umass.edu/pubfiles/mm-27.pdf
    used the WordSegmentation project by user githubharald which implemented this paper in a python project.
    https://github.com/githubharald/WordSegmentation/blob/master/src/WordSegmentation.py
