from db import collection       # Колекція
from pathlib import Path        # Для пошуку файлів в директоріях
from pypdf import PdfReader     # Робота з pdf
import re                       # Для форматування тексту (чистки)



def split_into_chunks(text, chunks_size=500, overlap=100):              # Створення чанків
    if chunks_size <= overlap:                                          # Перевірка вірності розміру чанків і розміру накладання
        raise ValueError('chunks_size має бути більшим за overlap')     # Кидає помилку зі зрозумілим повідомленням
    
    chunks = []                 # Список чанків
    start = 0                   # Початковий зріз + лічильник
    text_length = len(text)     # Довжина тексту

    while start < text_length:                          # Лічильник
        end = min(start + chunks_size, text_length)     # Кінець зрізу (береться мінімальне значення)
        chunk = text[start:end]                         # Додавання одного чанку по початок зрізу і конець зрізу
        chunks.append(chunk)                            # Додавання чанка у список чанків
        start += chunks_size - overlap                  # Додавання до початкового зрізу і лічильника розмір чанка і мінус перекриття

    return chunks   # Повертає чанки
# Завантажуємо документи
def load_documents():
    all_documents = []      # Всі чанки
    all_ids = []            # Всі ids
    all_metadatas = []      # Всі дазви документів і номери чанків
    
    docs_dir = Path('docs')     # Директорія з документами
    
    for pdf_path in docs_dir.glob('*.pdf'):     # Ітерація по всіх pdf документах в директорії
        reader = PdfReader(pdf_path)            # Створення екземпляр документа
        raw_text = ''                           # Необроблений текст з документа
        for page in reader.pages:               # Ітераця по сторінках екземпляру документа
            text_pdf = page.extract_text()      # Витягуємо текст сторінки
            if text_pdf:                        # Перевіряємо чи є текст
                raw_text += text_pdf + '\n'     # Додаємо необробленний текст сторінки
        clean_text = re.sub(r'\s+', ' ', raw_text).strip()      # форматуємо текст в один рядок

        chunks = split_into_chunks(clean_text)      # Розбиваємо текст на чанки

        file_stem = pdf_path.stem       # Назва документа

        for i, chunk in enumerate(chunks, start=1):                     # Ітерація по чанках (індекс, текст) (тут індекс починається з 1 а не з 0)
            all_documents.append(chunk)                                 # Додаємо у змінну текст
            all_ids.append(f'{file_stem}_{i}')                          # Додаємо у змінну назву файла і номер (індукс) текста (чанка)
            all_metadatas.append({'source': file_stem, 'chunk': i})     # Додаємо у змінну назву файла, як джерело і номер чанка як джерело

    if not all_documents:                   # Перевірка на наявність документів
        print('Документи не знайдені')
        return

    collection.upsert(              # додаємо (оновлюємо) колекцію
        documents=all_documents,    # Текст чанків
        ids=all_ids,                # ids
        metadatas=all_metadatas     # метадата
    )


#
if __name__ == '__main__':      # Вхід у програму
    load_documents()