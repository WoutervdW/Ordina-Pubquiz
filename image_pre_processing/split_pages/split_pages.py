from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("files/Sander_Test.pdf", "rb"))

for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("output_files/document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)

