import requests
import os
import dotenv


dotenv.load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY не знайдено! Перевір файл .env та переконайся, що змінна GROQ_API_KEY встановлена.")
print(bool(GROQ_API_KEY))
model = 'openai/gpt-oss-20b'

context_text = ['''1. Кожен співробітник має право на щорічну оплачувану відпустку тривалістю 24 календарні дні,
яку необхідно узгодити з керівником відділу не пізніше ніж за два тижні до її початку.''',
'''2. Стандартний графік роботи компанії передбачає п'ятиденний робочий тиждень з 09:00 до 18:00,
а у п'ятницю робочий день скорочується на одну годину.''',
'''3. У разі виробничої необхідності співробітники можуть залучатися до роботи у вихідні дні, що
оплачується у подвійному розмірі або компенсується додатковим днем відпочинку.''',
'''4. Повернення придбаного товару належної якості можливе протягом 14 днів з моменту покупки за
умови збереження його оригінальної упаковки та чека.''',
'''5. Якщо товар має виробничий дефект, клієнт має право вимагати його заміни на аналогічний або
повернути повну вартість протягом гарантійного терміну.''']

context_block = '\n'.join(context_text)

user_prompt = [{'role': 'user', 'content': 'Скільки сантиметрів в метрі?'}]
system_prompt = [{'role': 'system', 'content': f'''Ти корисний та розумний асистент. Відповідай на питання, спираючись ТІЛЬКИ на цей текст:
\n{context_block}\n\nЯкщо відповіді в тексті немає, так і скажи. Не вигадуй інформацію.'''}]
print(system_prompt)

messeges = system_prompt + user_prompt

def llm_request(massages=messeges):
    try:
        llm_prompt_form = requests.post('https://api.groq.com/openai/v1/chat/completions', 
                                        headers={'Authorization': f'Bearer {GROQ_API_KEY}'}, 
                                        json={'model': model, 'messages': massages})
        llm_prompt_form.raise_for_status()

        response_json = llm_prompt_form.json()
        print(llm_prompt_form.status_code)
        print(response_json)
        print(response_json['choices'][0]['message']['content'])

        response_ai = response_json['choices'][0]['message']['content']

    except requests.RequestException as e:
        if e.response is not None:
            print(f"Помилка при обробці запиту: {e.response.text}")
        else:
            print(f"Не вдалося з'єднатися з сервером і варто перевірити інтернет \n {e}")

    try:
        return response_ai
    except Exception as e:
        return None


llm_request()







# try:
#     response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
#     response.raise_for_status()
#     print(response.status_code)
#     data = response.json()
#     print(data['title'])


# except requests.RequestException as e:
#     print(f"Помилка при обробці запиту: {e}")

# except KeyError:
#     print("Ключ 'title' не знайдено у відповіді.")


# test_dict = {
#     "userId": 1,
#     "id": 1,
#     "title": "delectus aut autem",
#     "completed": False
# }

# response2 = requests.post('https://jsonplaceholder.typicode.com/posts', json=test_dict)

# print(response2.status_code)
# print(response2.json())
# print(response2)

