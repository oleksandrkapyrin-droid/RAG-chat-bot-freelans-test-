from db import collection       # Колекція
from app import llm_request     # Зпит до LLM


def answer_question(question):                                          # Відповідь на питання
    result = collection.query(query_texts=[question], n_results=2)      # Зберігання актуальної відповіді у змінну
    if not result['documents'][0]:                                      # Якщо відповідь порожня
        return {'answer': 'База знань порожня.', 'sources': []}         # Повідомлення порожгьої бази

    documents = result['documents'][0]      # Текст відповді
    metadatas = result['metadatas'][0]      # Метадата відповіді

    llm_answer = llm_request(question, documents)                                                       # Звернення до LLM (питання + документ)
    if llm_answer is None:                                                                              # Якщо LLM нічого не повернула
        return {'answer': 'Сталася помилка при зверненні до LLM. Спробуйте пізніше.', 'sources': []}    # Зрозуміле повідомлення для користувача

    sources = [f"Файл: {meta['source']}, Чанк: {meta['chunk']}" for meta in metadatas]      # Ітерація по metadatas, зберігання у змінну джерело і номер чанка

    answer = {'answer': llm_answer, 'sources': sources}     # Відповідь LLM з джерелом і номером чанка

    return answer   # Відповідь


if __name__ == '__main__':                                  # Вхід у програму
    response = answer_question(input('Ваше питання: '))     # Запуск програми з питанням користувача
    print(response['answer'])                               # Вивід відповіді
    for src in response['sources']:                         # Ітерація по джерелам
        print(src)                                          # Вивід джерел
