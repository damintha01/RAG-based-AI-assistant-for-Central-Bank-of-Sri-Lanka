from pypdf import PdfReader
import os
from pathlib import Path


RAW_PATH="data/raw/"
PROCESSED_PATH="data/processed/"


def extract_text_from_pdf(file_path):
    reader=PdfReader(file_path)
    pages=[]

    for i, page in enumerate(reader.pages):
        text=page.extract_text()

        if text:
            pages.append({
                "page_number": i+1,
                "text": text
            })
    return pages

def clean_text(text):
    text=text.replace("\n\n", "\n")
    text=text.strip()
    return text


def process_pdf():
    for root,dirs, files in os.walk(RAW_PATH):
        for file in files:
         if file.endswith(".pdf"):

            full_path = os.path.join(root, file)
            print(f"Processing {full_path}...")

            try:
                pages = extract_text_from_pdf(full_path)

                for page in pages:
                    page["text"] = clean_text(page["text"])

                # keep same filename but safe
                save_name = file.replace(".pdf", ".json")
                save_path = os.path.join(PROCESSED_PATH, save_name)

                import json
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(pages, f, indent=2, ensure_ascii=False)

                print(f"Saved → {save_path}")

            except Exception as e:
                print(f"Failed {file}: {e}")



if __name__ == "__main__":
    process_pdf()