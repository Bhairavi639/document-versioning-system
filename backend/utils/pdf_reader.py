import fitz  # PyMuPDF
import re


def read_pdf(file_path):
    """
        Improved PDF reader:
        - Groups text into paragraphs
        - Removes noise
        - Keeps structure better than line-by-line
    """

    
    paragraphs = []

    try:
        doc = fitz.open(file_path)

        for page in doc:
            # Get structured text blocks instead of raw text
            blocks = page.get_text("blocks")

            for block in blocks:
                text = block[4]  # block text

                if not text:
                    continue

                # Clean text
                cleaned = text.strip()

                # Split into smaller paragraphs if needed
                for para in cleaned.split("\n"):
                    para = para.strip()

                    if para:
                        paragraphs.append(para)

        doc.close()

    except Exception as e:
        print(f"Error reading PDF: {e}")

    return paragraphs
    
