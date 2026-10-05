# utils/pdf_extractor.py

from pypdf import PdfReader
from io import BytesIO


def extract_text(file_bytes: bytes, file_name: str) -> str:
    if file_name.lower().endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages).strip()

    elif file_name.lower().endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore").strip()

    else:
        raise ValueError("Unsupported file type. Only PDF and TXT are supported.")