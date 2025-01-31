# DataGPT
DataGPT — это Python-библиотека, которая упрощает интеграцию с различными ИИ-платформами, такими как OpenAI, DeepSeek, Ollama (локально), Anthropic и другие.

## ✅ Возможности:
- Унифицированный API для разных ИИ-платформ 🧠
- Подключение OpenAI API, DeepSeek, Anthropic, Ollama (локально) и других сервисов 🔗
- Работа с ИИ-ассистентами и векторным хранилищем 📂
- Лёгкое переключение между разными ИИ-поставщиками без изменения кода 🔄

## 📌 Установка
Установите библиотеку через `pip`:
```bash
pip install datagpt
```
## 🚀 Быстрый старт ИИ-ассистента
Перед запуском убедитесь, что у вас активен VPN (если API недоступен в вашей стране).  
Пример работы с OpenAI API:
```Python
from datagpt.packs import openai_

# Подключение OpenAI API
gpt = openai_.Assistant("OPENAI_API_KEY")
gpt.set_id("ASSISTANT_ID")  # ID ассистента

# Запрос к ассистенту
response = gpt.new_chat_and_run("Какая информация у вас есть?")
print(response)
```
## 📂 Управление файлами (ИИ-ассистент + документы)
Пример работы с векторным хранилищем файлов:
```Python
import os
from dotenv import load_dotenv
from datagpt.packs import openai_

# Загрузка переменных окружения
load_dotenv()
# Данные из платформы OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ASSISTANT_ID = os.environ.get("OPENAI_ID_ASSISTANT")
VECTOR_STORE = "VECTOR_STORE_NAME"

# Подключение к хранилищу
vs = openai_.Storage(OPENAI_API_KEY)

# Получение списка файлов
print(vs.get_uploaded_file_list())

# Загрузка файла в хранилище
vs.add_files_to_vector_store(["data/files/test/doc.pdf"], VECTOR_STORE)

# Создание чата с ассистентом
gpt = openai_.Assistant(OPENAI_API_KEY)
gpt.set_id(ASSISTANT_ID)
response = gpt.new_chat_and_run("Что такое ...?")
print(response)

# Удаление файла
vs.delete_files_from_vector_store(["data/files/test/doc.pdf"], VECTOR_STORE)
```

## 🔮 Будущее DataGPT
DataGPT не ограничивается OpenAI! В будущем поддержка расширится:
```Python
from datagpt.packs import openai_ # У доступно
from datagpt.packs import deepseek_  # В будущем
from datagpt.packs import ollama_  # В будущем(локальная работа)
from datagpt.packs import anthropic_  # В будущем
```

## 📬 Поддержка
Если у вас есть вопросы или предложения, пишите на alexeyayaya@gmail.com.