try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


#print(pytesseract.image_to_string(Image.open('test-images/test3.jpg')))
print(pytesseract.image_to_data(Image.open('test-images/test1.jpg')))

