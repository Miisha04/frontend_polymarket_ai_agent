# frontend_app/app.py

import streamlit as st
import requests

# URL нашего FastAPI бэкенда
BACKEND_URL = "http://127.0.0.1:8000/invoke"

# --- Настройка страницы ---
st.set_page_config(page_title="Polymarket AI Agent", layout="wide")
st.title("🤖 AI Агент для Polymarket (MVP)")
st.caption("Введите запрос, например: 'Какая информация по рынку Трампа?'")

# --- Логика чата ---

# Инициализация истории чата в session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение сообщений из истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Прием ввода от пользователя
if prompt := st.chat_input("Ваш вопрос..."):
    # 1. Отобразить сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Добавить сообщение пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Получить ответ от ассистента
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Думаю... 🧠")
        
        try:
            # Отправляем запрос на бэкенд
            response = requests.post(BACKEND_URL, json={"query": prompt})
            response.raise_for_status() # Проверяем на ошибки HTTP
            
            assistant_response = response.json()["output"]
            message_placeholder.markdown(assistant_response)
            
            # 4. Добавить ответ ассистента в историю
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
        except requests.exceptions.RequestException as e:
            error_message = f"Не удалось подключиться к бэкенду: {e}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

