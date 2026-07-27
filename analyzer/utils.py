import PyPDF2


def extract_pdf_text(file):

    text = ""

    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    return text