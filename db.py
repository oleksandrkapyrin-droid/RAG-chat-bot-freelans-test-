import chromadb
from chromadb.utils import embedding_functions


client = chromadb.PersistentClient(path='chroma_db')
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='paraphrase-multilingual-MiniLM-L12-v2')
collection = client.get_or_create_collection(name='company_docs1_multi', embedding_function=ef)
