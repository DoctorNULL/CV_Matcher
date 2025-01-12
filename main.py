from CVData import CV
from docx import Document

cv = CV()

cv.loadCV("Amruta B.pdf", "en")

req = Document("Web Developer.docx")

r = ""

for par in req.paragraphs:
    r += par.text

print(cv.isQualified(r, "en"))
