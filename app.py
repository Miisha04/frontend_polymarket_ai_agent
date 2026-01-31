import streamlit as st
import requests

# URL нашего FastAPI бэкенда
BACKEND_URL = "http://127.0.0.1:8000/chat/invoke"

# --- Настройка страницы ---
st.set_page_config(page_title="Polymarket AI Agent", layout="wide")
st.title("🤖 AI Агент для Polymarket (MVP)")
st.caption("Введите запрос, например: 'Какая информация по рынку Трампа?'")

# --- Инициализация истории чата и session_id ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# --- Отображение сообщений из истории ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Прием ввода от пользователя ---
if prompt := st.chat_input("Ваш вопрос..."):

    # 1️⃣ Отобразить сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2️⃣ Добавить сообщение пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3️⃣ Отправляем запрос на бекенд
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Думаю... 🧠")

        try:
            payload = {
                "query": prompt,
                "session_id": st.session_state.session_id  # передаем текущую сессию
            }
            response = requests.post(BACKEND_URL, json=payload)
            response.raise_for_status()

            data = response.json()
            assistant_response = data["response"]

            # Сохраняем session_id от бекенда для последующих запросов
            st.session_state.session_id = data["session_id"]

            # Отобразить ответ ассистента
            message_placeholder.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        except requests.exceptions.RequestException as e:
            error_message = f"Не удалось подключиться к бэкенду: {e}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})