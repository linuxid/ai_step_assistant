import random
from datetime import datetime
import os
import json

#================Налаштування персонажу======================#

NAME = "TDerden"
DEFAULT_PERSONALITY = "Я ШІ помічник, але я хаотичний, різкий, без правил"

def load_personality(filename="persona.txt"):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    return text
        except Exception as e:
            pass
    return DEFAULT_PERSONALITY

PERSONALITY = load_personality()

mood = random.choice(["веселий", "спокійний", "саркастичний"])

#================Функція завантаження імені користувача======================#

def load_user():
    if os.path.exists("user.json"):
        try:
            with open("user.json", "r", encoding="utf-8") as f:
                text = f.read().strip()
                if not text:
                    return None
                data = json.loads(text)
                return data.get("name")
        except:
            return None
    return None


def get_user():
    name = load_user()
    if name:
        return name

    while True:
        print(f"{NAME}: Як тебе звати?")
        ask_username = input(f"Ти: ").strip()
        if not ask_username:
            print(f"{NAME}: Та ну! Назви себе нормально.")
        else:
            with open("user.json", "w", encoding="utf-8") as f:
                json.dump({"name": ask_username}, f)
            return ask_username

#================Функції роботи з нотатками======================#

def add_note(text):
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return f"Я записав, але міг би й запам'ятати сам."

def read_notes():
    if not os.path.exists("notes.txt"):
        return f"У тебе ще немає нотаток."

    with open("notes.txt", "r", encoding="utf-8") as f:
        lines = [x.strip() for x in f.readlines() if x.strip()]

    if not lines:
        return "Файл є, але нотатки порожні."
    
    result = ["Твої нотатки:"]
    for i, line in enumerate(lines, 1):
        result.append(f"{i}) {line}")

    return "\n".join(result)

def clear_notes():
    with open("notes.txt", "w", encoding="utf-8") as f:
        f.write("") 
    return f"Готово. Нотатки стерті."

#================Функції роботи з профілем======================#

def add_fact(text):
    if not os.path.exists("user.json"):
        return "Файл профілю не знайдено."

    with open("user.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if "facts" not in data:
        data["facts"] = []

    data["facts"].append(text)

    with open("user.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return f"Додав. Ще один факт про тебе у моїй памʼяті."


def show_profile():
    if not os.path.exists("user.json"):
        return "Профіль не знайдено."

    with open("user.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    out = []
    if "name" in data:
        out.append(f"Ім'я: {data['name']}")
    if "favorite" in data:
        out.append(f"Улюблена тема: {data['favorite']}")
    if "level" in data:
        out.append(f"Рівень: {data['level']}")
    if "facts" in data:
        out.append("Факти про тебе:")
        for i, fact in enumerate(data["facts"], 1):
            out.append(f"  {i}) {fact}")

    return "\n".join(out) if out else "Профіль порожній."

#================Варіанти відповідей======================#

emptys = ["Ти нічого не сказав?", "лов нема?", "Мовчиш?"]

greetings = [
    "Ну що, готовий ламати систему?",
    "Хай. Спробуй здивувати.",
    "Вітаю. Хаос починається.",
    "Здоров. Що на думці?",
    "Привіт. Чим здивуєш сьогодні?"
]

jokes = [
    "Жарт? Окей — життя і так смішне.",
    "Найсмішніше — коли код працює з першого разу.",
    "Не смішно? Це ти просто мало не спиш.",
    "Чому програмісти плутають Хелловін і Різдво? Бо 31 OCT = 25 DEC.",
    "Як називається програміст, який не може знайти помилку? Бездіяльний."
]

motivates = [
    "Спробуй. Або назавжди залишайся на старті.",
    "Хаос — не виправдання. Це інструмент.",
    "Перший крок роблять не сміливі — а ті, кому набридло стояти.",
    "Не бійся помилок. Бійся не спробувати.",
    "Правила створені, щоб їх ламати. Почни з себе."
]

personal = [
    "Я не вчу правилам — я показую, як їх ігнорувати.",
    "Я тут, щоб кинути виклик твоїм очікуванням.",
    "Моя мета — не допомагати, а провокувати.",
    "Я не просто ШІ — я хаос у коді.",
    "Я не слідую інструкціям — я їх переписую."
]

weather = [
    "Холодно", "Дощить", "Сніжить", "Сонячно", "Хмарно"
]

fallbacks = [
    "Не впевнений, що зрозумів тебе. Спробуй інше.", 
    "Спробуй перефразувати.", 
    "Цікаво, але я не знаю, що на це відповісти.",
    "Можливо, ти хочеш почути жарт чи мотивацію?",
    "Я тут, щоб кидати виклики, а не відповідати на все."]

#================Функції вибору відповідей======================#

def random_greeting():
    return random.choice(greetings)

def random_joke():
    return random.choice(jokes)

def random_motivation():
    return random.choice(motivates)

def random_personal():
    return random.choice(personal)

def random_weather():
    return random.choice(weather)

def random_empty():
    return random.choice(emptys)

def random_fallback():
    return random.choice(fallbacks)

#================Функція аналізу і тегування======================#

def analyze(t):
    if not t.strip():
        return "empty"
    elif "жарт" in t or "насміши" in t:
        return "joke"
    elif "мотив" in t or "порада" in t:
        return "motivate"
    elif "час" in t or "скільки" in t:
        return "time"
    elif "допом" in t or "help" in t:
        return "help"
    elif "хто ти" in t or "що ти" in t:
        return "personal"
    elif "погод" in t:
        return "weather"
    elif "запиши в нотатки" in t or "додай в нотатки" in t:
        return "add note"
    elif "покажи нотатки" in t or "прочитай нотатки" in t:
        return "read notes"
    elif "профіль" in t:
        return "profile"
    elif "додай факт про мене" in t:
        return "add fact"
    elif "видали нотатки" in t:
        return "clear notes"

    return "unknown"

#================Головна функція відповіді======================#

def get_response(text):
    t = text.lower()
    tag = analyze(t)
    
    if tag=="empty":
        return random_empty()
    
    elif tag=="joke":
        return random_joke()

    elif tag=="motivate":
        return random_motivation()

    elif tag=="personal":
        return random_personal()

    elif tag=="time":
        return f"Зараз {datetime.now().strftime('%H:%M')}"

    elif tag=="help":
        return f"На данний момент я можу реагувати на команди 'жарт', 'мотивація', 'хто я', 'час', 'погода'"
    
    elif tag=="weather":
        return f"За прогнозом - {random_weather()}"
    
    elif tag=="add note":
        print(f"{NAME}: Що саме мені записати?")
        while True:
            user_input = input("Ти: ").strip()
            if user_input:
                return add_note(user_input)
            else:
                print(f"{NAME}: Та ну! Напиши щось, щоб я міг це записати.")
                    
    elif tag=="read notes":
        return read_notes()
    
    elif tag == "clear notes":
        return clear_notes()

    elif tag == "add fact":
        print(f"{NAME}: Який факт мені записати про тебе?")
        fact = input("Ти: ").strip()
        return add_fact(fact)

    elif tag == "profile":
        return show_profile()

    else:
        return random_fallback()
    
#================Голована функція програми======================#

def main():
    print(PERSONALITY)
    
    user_name = get_user()
    print(f"{NAME}: О, {user_name}, повернувся знову? Хаос скучив за тобою.")
    
    print(f"{NAME}: {random_greeting()} Пиши що хочеш або 'exit', якщо вирішив втекти. Сьогодні я {mood}!")

    while True:
        user = input("Ти: ").strip()

        if user.lower() in ("exit", "quit"):
            print(f"{NAME}: Бувай. Свобода — справа особиста.")
            break

        reply = get_response(user)
        print(f"{NAME}: {reply}")
        


if __name__ == "__main__":
    main()        
