from db import collection
from pathlib import Path
from pypdf import PdfReader
import re



def split_into_chunks(text, chunks_size=500, overlap=100):
    
    
    
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunks_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunks_size - overlap

    return chunks

def load_documents():
    all_documents = []
    all_ids = []
    all_metadatas = []
    
    docs_dir = Path('docs')
    
    for pdf_path in docs_dir.glob('*.pdf'):
        reader = PdfReader(pdf_path)
        raw_text = ''
        for page in reader.pages:
            text_pdf = page.extract_text()
            if text_pdf:
                raw_text += text_pdf + '\n'
        clean_text = re.sub(r'\s+', ' ', raw_text).strip()

        chunks = split_into_chunks(clean_text)

        file_stem = pdf_path.stem

        for i, chunk in enumerate(chunks, start=1):
            all_documents.append(chunk)
            all_ids.append(f'{file_stem}_{i}')
            all_metadatas.append({'source': file_stem, 'chunk': i})


    collection.upsert(
        documents=all_documents,
        ids=all_ids,
        metadatas=all_metadatas
    )



if __name__ == '__main__':
    load_documents()