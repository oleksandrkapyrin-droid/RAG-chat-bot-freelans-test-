from db import collection
from app import llm_request


def answer_question(question):
    result = collection.query(query_texts=[question], n_results=2)
    if not result['documents'][0]:
        return {'answer': 'База знань порожня.', 'sources': []}

    documents = result['documents'][0]
    metadatas = result['metadatas'][0]

    llm_answer = llm_request(question, documents)

    sources = [f"Файл: {meta['source']}, Чанк: {meta['chunk']}" for meta in metadatas]

    answer = {'answer': llm_answer, 'sources': sources}

    return answer


if __name__ == '__main__':
    response = answer_question(input('Ваше питання: '))
    print(response['answer'])
    for src in response['sources']:
        print(src)
# DONE