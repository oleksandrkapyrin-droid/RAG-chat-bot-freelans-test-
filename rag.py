from db import collection
from app import llm_request


def answer_question(question):
    result = collection.query(query_texts=[question], n_results=2)
    result_answer = result['documents'][0]
    result_metadata = result['metadatas'][0]    
    llm_answer = llm_request(question, result_answer)

    answer = {'answer': llm_answer, 'sources': result_metadata}

    return answer


if __name__ == '__main__':
    response = answer_question(input('Ваше питання: '))
    print(response)
