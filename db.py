import chromadb                                     # База даних
from chromadb.utils import embedding_functions      # Модель Ембедінг

# Створюється об'єкт-клієнт. Слово «Persistent» означає «постійний»: дані зберігаються на диск у папку chroma_db.
client = chromadb.PersistentClient(path='chroma_db')
# Для багатомовна модель, яка перетворює текст на вектори
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='paraphrase-multilingual-MiniLM-L12-v2')
# Створення колекції
collection = client.get_or_create_collection(name='python_and_csharp_docs_multi', embedding_function=ef)
