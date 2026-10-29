from fastapi import FastAPI, HTTPException  # Фреємворк, клас для відправки помилок клієнту (404, 502)
from pydantic import BaseModel              # Валідація даних
from rag import answer_question             # RAG



app = FastAPI()     # Екземпляр веб-додатку

class Question(BaseModel):  # Опис моделі даних запита клієнта
    question: str          # поле иає бути рядком

@app.post('/ask')                                                                           # Коли викликати функцію нище
def ask(q: Question):                                                                       # FastApi пакує питання у об'єкт Question і передає у функцію як q
    result = answer_question(q.question)                                                    # Дістає текст питання через q.question і відправляє в RAG
    if result['answer'] == 'Сталася помилка при зверненні до LLM. Спробуйте пізніше.':      # Якщо відповідь помилка
        raise HTTPException(status_code=502, detail=result['answer'])                       # Кидаэмо помилку
    
    return result   # Відповідь