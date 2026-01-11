import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from google import genai
from google.genai import types
import json  # ВАЖЛИВО: Додано імпорт для роботи з JSON відповідями
import os
import random


# ================= НАЛАШТУВАННЯ =================
API_KEY = "API-key"  # <-- Вставте ваш ключ
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash" # Вказуємо правильно версію моделі!

# Завантажуємо базову персону
BASE_PERSONA = "Ти корисний асистент."
if os.path.exists("persona.txt"):
    with open("persona.txt", "r", encoding="utf-8") as f:
        BASE_PERSONA = f.read().strip()

# Словник емоцій (додали 'joke', щоб ШІ мав вибір)
emotions = {
    "neutral": ("neutral.png", "#ffffff"), # Білий фон
    "happy": ("happy.png", "#e1f5fe"),   # Світло-блакитний
    "sad": ("sad.png", "#ffebee"),     # Світло-червоний
    "joke": ("happy.png", "#fff9c4")     # Жовтуватий (використовуємо картинку happy)
}

# ================= ГРАФІЧНИЙ ІНТЕРФЕЙС (GUI) SETUP =================
root = tk.Tk()
root.title("AI Assistant JSON Edition")
root.geometry("600x750")
root.configure(bg="white")

# 1. Віджет Аватара
avatar_label = tk.Label(root, bg="white")
avatar_label.pack(pady=20)

# 2. Віджет Чату
chat_display = scrolledtext.ScrolledText(root, width=50, height=20, font=("Arial", 12), state='disabled')
chat_display.pack(padx=10, pady=10)

# 3. Зона введення
input_frame = tk.Frame(root, bg="white")
input_frame.pack(pady=10, side=tk.BOTTOM)

user_input = tk.Entry(input_frame, width=35, font=("Arial", 14))
user_input.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(input_frame, text="→", width=5, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
send_button.pack(side=tk.LEFT, padx=5)


# ================= ФУНКЦІЇ-ХЕЛПЕРИ ДЛЯ GUI =================

def set_state(emotion):
    """Встановлює емоцію аватара та колір фону (аналог update_avatar)"""
    # Якщо ШІ придумав емоцію, якої немає в словнику, беремо neutral
    emotion_data = emotions.get(emotion, emotions["neutral"])
    img_path, bg_color = emotion_data
    
    root.configure(bg=bg_color)
    avatar_label.configure(bg=bg_color)
    input_frame.configure(bg=bg_color)
    
    try:
        if os.path.exists(img_path):
            img = Image.open(img_path).resize((250, 250), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            avatar_label.configure(image=photo)
            avatar_label.image = photo
        else:
            print(f"Зображення {img_path} не знайдено.")
    except Exception as e:
        print(f"Помилка завантаження картинки: {e}")

def display_text(text_to_show, sender="ШІ"):
    """Безпечно додає текст у вікно чату"""
    chat_display.configure(state='normal') # Дозволяємо редагування
    chat_display.insert(tk.END, f"{sender}: {text_to_show}\n\n")
    chat_display.configure(state='disabled') # Забороняємо редагування
    chat_display.see(tk.END) # Автопрокрутка вниз


# ================= ГОЛОВНА ЛОГІКА (Інтегрований фрагмент) =================

def process_message_logic(user_text):
    """Логіка з автоматичним визначенням емоції через ШІ (JSON)"""
    
    # Блокуємо кнопку на час запиту
    send_button.config(state=tk.DISABLED, text="...")
    
    # Показуємо повідомлення користувача в чаті
    # root.after(0, ...) використовується для безпечної роботи з GUI, 
    # навіть якщо ця функція в майбутньому буде запущена в окремому потоці.
    root.after(0, display_text, user_text, "Ви")
    root.after(0, lambda: user_input.delete(0, tk.END)) # Очищаємо поле вводу

    try:
        # Формуємо повну інструкцію, поєднуючи персону і вимоги до JSON
        full_system_instruction = (
            f"{BASE_PERSONA}\n"
            "ВАЖЛИВО: Твоя відповідь має бути ТІЛЬКИ у форматі JSON. "
            "JSON повинен містити рівно два поля: "
            "'text' (твоя текстова відповідь користувачу) та "
            "'emotion' (одне зі значень: 'neutral', 'happy', 'sad', 'joke'). "
            "Обирай 'emotion', яка найкраще відповідає змісту твоєї відповіді."
        )

        # Запит до моделі
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_text,
            config={
                'system_instruction': full_system_instruction,
                'response_mime_type': 'application/json', # Змушуємо API віддати JSON
                'temperature': 0.7
            }
        )

        # --- ПАРСИНГ ВІДПОВІДІ ---
        print(f"Raw API response: {response.text}") # Для відладки

        # Перетворюємо текст JSON-відповіді у словник Python
        res_data = json.loads(response.text)
        
        # Дістаємо дані зі словника
        ai_reply = res_data.get("text", "Хм, я щось заплутався у своїх думках.")
        ai_emotion = res_data.get("emotion", "neutral")

        # Оновлюємо інтерфейс результатами
        root.after(0, set_state, ai_emotion)
        root.after(0, display_text, ai_reply)

    except json.JSONDecodeError:
        # Якщо API повернув не коректний JSON
        print("Помилка: Отримано некоректний JSON від API")
        root.after(0, set_state, "sad")
        root.after(0, display_text, "Вибач, мої внутрішні протоколи JSON дали збій.")
    except Exception as e:
        # Інші помилки (наприклад, немає інтернету або неправильний ключ)
        print(f"Критична помилка API: {e}")
        root.after(0, set_state, "sad")
        root.after(0, display_text, f"Сталася помилка зв'язку: {e}")

    finally:
        # Розблоковуємо кнопку завжди, навіть якщо була помилка
        root.after(0, lambda: send_button.config(state=tk.NORMAL, text="→"))


# ================= ФУНКЦІЯ-ТРИГЕР =================
def send_message_trigger(event=None):
    """Функція, яка викликається при натисканні кнопки або Enter"""
    text = user_input.get().strip()
    if text:
        # Запускаємо головну логіку
        process_message_logic(text)

# Прив'язка подій до кнопки та Enter
send_button.config(command=send_message_trigger)
user_input.bind("<Return>", send_message_trigger)

# ================= ЗАПУСК =================
# Встановлюємо початковий стан
set_state("neutral")
display_text("Привіт! Я готовий до роботи. Напиши мені щось, і я спробую підібрати емоцію.", "Система")

root.mainloop()