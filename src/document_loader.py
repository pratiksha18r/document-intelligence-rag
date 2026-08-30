from pypdf import PdfReader


def load_pdf(file_path):
    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            documents.append({
                "page_number": page_number,
                "text": text
            })

    return documents