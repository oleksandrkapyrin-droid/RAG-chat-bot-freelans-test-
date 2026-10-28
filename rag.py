from db import collection
from app import llm_request


def answer_question(question):
    result = collection.query(query_texts=[question], n_results=2)
    documents = result['documents'][0]
    metadata = [item.get('point') for item in result['metadatas'][0]]
    llm_answer = llm_request(question, documents)

    answer = {'answer': llm_answer, 'sources': metadata}

    return answer


if __name__ == '__main__':
    response = answer_question(input('Ваше питання: '))
    print(response)
