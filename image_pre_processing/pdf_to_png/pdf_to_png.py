"""
A simple example of how we can convert the pdf to a png.
You have to install 'poppler' on windows for this:
http://blog.alivate.com.au/poppler-windows/
download the binary and set a path to the bin.
"""
from pdf2image import convert_from_path

pages = convert_from_path("../../test-images/template_example/scan1.pdf", 500)

for page in pages:
    page.save('scan1_image.png', 'PNG')


