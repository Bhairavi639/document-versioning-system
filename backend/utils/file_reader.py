import os
from utils.doc_reader import read_docx
from utils.pdf_reader import read_pdf


def read_file(file_path):
    """
    Detect file type and read accordingly.
    """

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".docx":
        return read_docx(file_path)

    elif ext == ".pdf":
        return read_pdf(file_path)

    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX allowed.")