import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from google import genai
from google.genai import types
import random
import json
import os
from datetime import datetime

# ================= НАЛАШТУВАННЯ (З assistant_api.py та persona.txt) =================
API_KEY = "AIzaSyC_ySya7PzbgXIt7jrW5toKDZrw3Fyq-QQ"  # Вставте сюди ключ
client = genai.Client(api_key=API_KEY)

# Завантажуємо персону
PERSONALITY = "Ти саркастичний помічник. Ти любиш чорний гумор."  # Дефолт
if os.path.exists("persona.txt"):
    with open("persona.txt", "r", encoding="utf-8") as f:
        PERSONALITY = f.read().strip()

# Налаштування Gemini
config = types.GenerateContentConfig(
    system_instruction=PERSONALITY,
    temperature=0.7  # Креативність
)

# ================= ЛОГІКА БОТА (З assistant.py) =================

emotions = {
    "neutral": ("neutral.png", "#ffffff"),
    "happy": ("happy.png", "#aaffff"),
    "sad": ("sad.png", "#ffaaaa")
}

jokes = [
    "Код працює? Не чіпай!",
    "Я не баг, я фіча.",
    "В 0 і 1 є щось магічне, але ти цього не зрозумієш."
]


def load_user_name():
    if os.path.exists("user.json"):
        try:
            with open("user.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("name", "Користувач")
        except:
            return "Користувач"
    return "Користувач"


USER_NAME = load_user_name()

# ================= ГРАФІЧНИЙ ІНТЕРФЕЙС (GUI) =================

root = tk.Tk()
root.title(f"AI Assistant для {USER_NAME}")
root.geometry("600x750")
root.configure(bg="white")

# 1. Аватар
avatar_label = tk.Label(root, bg="white")
avatar_label.pack(pady=10)


def update_avatar(emotion):
    # Беремо файл та колір зі словника
    img_path, bg_color = emotions.get(emotion, emotions["neutral"])

    # Змінюємо колір фону вікна (ефект атмосфери)
    root.configure(bg=bg_color)
    avatar_label.configure(bg=bg_color)

    try:
        # Завантаження картинки
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            avatar_label.configure(image=photo)
            avatar_label.image = photo  # Зберігаємо посилання, щоб не зникло
        else:
            print(f"Зображення {img_path} не знайдено.")
    except Exception as e:
        print(f"Помилка картинки: {e}")


# Завантажуємо стартову емоцію
update_avatar("neutral")

# 2. Поле чату (ScrolledText зручніше, ніж просто Text)
chat_display = scrolledtext.ScrolledText(root, width=50, height=15, font=("Arial", 12))
chat_display.pack(padx=10, pady=10)
chat_display.insert(tk.END, f"Бот: Привіт, {USER_NAME}! Я готовий. Пиши.\n")
chat_display.configure(state='disabled')  # Забороняємо друкувати руками в чаті


# ================= ГОЛОВНА ФУНКЦІЯ ОБРОБКИ =================

def get_local_response(text):
    """Шукає відповідь без інтернету (швидкі команди)"""
    t = text.lower()
    if "жарт" in t:
        return random.choice(jokes), "happy"
    elif "час" in t:
        return f"Зараз {datetime.now().strftime('%H:%M')}", "neutral"
    elif "хто ти" in t:
        return PERSONALITY, "neutral"
    elif "сумно" in t or "помилка" in t:
        return "Не переймайся, це досвід.", "sad"
    return None, "neutral"  # Якщо локальної команди немає


def send_message():
    user_text = user_input.get().strip()
    if not user_text:
        return

    # 1. Показуємо повідомлення користувача
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"Ти: {user_text}\n")
    user_input.delete(0, tk.END)  # Очистити поле

    # 2. Спочатку шукаємо локальну відповідь
    response_text, emotion = get_local_response(user_text)

    # 3. Якщо локальної немає - йдемо до ШІ (API)
    if not response_text:
        try:
            # Тут можна додати анімацію "думає..."
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_text,
                config=config,
            )
            response_text = response.text
            # Проста логіка емоцій на основі тексту ШІ
            if "!" in response_text or "радий" in response_text:
                emotion = "happy"
            elif "жаль" in response_text or "вибач" in response_text:
                emotion = "sad"
            else:
                emotion = "neutral"
        except Exception as e:
            response_text = "Ой, я втратив зв'язок з космосом (помилка API)."
            emotion = "sad"
            print(e)

    # 4. Виводимо відповідь бота
    chat_display.insert(tk.END, f"Bot: {response_text}\n\n")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)  # Прокрутка вниз

    # 5. Оновлюємо аватар
    update_avatar(emotion)


# 3. Поле введення і кнопка
input_frame = tk.Frame(root, bg="white")
input_frame.pack(pady=10)

user_input = tk.Entry(input_frame, width=35, font=("Arial", 14))
user_input.pack(side=tk.LEFT, padx=5)

# Прив'язка клавіші Enter до надсилання
user_input.bind("<Return>", lambda event: send_message())

send_button = tk.Button(input_frame, text="Send", command=send_message, bg="#4CAF50", fg="white", font=("Arial", 12))
send_button.pack(side=tk.LEFT, padx=5)

# Запуск
root.mainloop()