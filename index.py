from db import collection
from pathlib import Path
from pypdf import PdfReader
import re


all_text = ''
docs_dir = Path('docs')
p = 

for pdf_path in Path('docs').glob('*.pdf'):
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + '\n'

clean_text = re.sub(r'\s+', ' ', all_text).strip()


def split_into_chunks(text, chunks_size=500, overlap=100):
    
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = (start + chunks_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunks_size - overlap

    return chunks


context_text = split_into_chunks(clean_text)

collection.upsert(
    documents=context_text,
    ids=[f'{p.stem}{i}' for i, _ in enumerate(context_text, start=1)],
    metadatas=[{'point': i} for i, _ in enumerate(context_text, start=1)]
)
