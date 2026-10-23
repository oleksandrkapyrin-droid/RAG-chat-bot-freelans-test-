import requests
import os
import dotenv


dotenv.load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY не знайдено! Перевір файл .env та переконайся, що змінна GROQ_API_KEY встановлена.")
print(bool(GROQ_API_KEY))


user_message = [{'role': 'user', 'content': 'Для RAG нам потрібні embeddings (перетворення тексту на вектори), чи надає їх Groq?'}]

try:
    llm_prompt_form = requests.post('https://api.groq.com/openai/v1/chat/completions', 
                                    headers={'Authorization': f'Bearer {GROQ_API_KEY}'}, 
                                    json={'model': 'openai/gpt-oss-20b', 'messages': user_message})
    llm_prompt_form.raise_for_status()

    response_json = llm_prompt_form.json()
    print(llm_prompt_form.status_code)
    print(response_json)
    print(response_json['choices'][0]['message']['content'])

except requests.RequestException as e:
    if e.response is not None:
        print(f"Помилка при обробці запиту: {e.response.text}")
    else:
        print(f"Не вдалося з'єднатися з сервером і варто перевірити інтернет \n {e}")

    







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

