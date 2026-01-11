# pip install Pillow
# pip install google-genai

import tkinter as tk
from PIL import Image, ImageTk
from google import genai

emotions = {
    "neutral" : ("neutral.png", "#ffffff"),
    "happy" : ("happy.png", "#aaffff"),
    "sad": ("sad.png", "#ffaaaa")
}

root = tk.Tk()
root.title("AI Assistant")
root.geometry("500x700")

avatar_label = tk.Label(root)
avatar_label.pack(pady=20)

def update_avatar(emotion):
    img_path, bg_color = emotions.get(emotion, emotions["neutral"])
    #root.configure(bg=bg_color)
    avatar_label.configure(bg=bg_color)
    try:
        img = Image.open(img_path)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        avatar_label.configure(image=photo)
        avatar_label.image = photo
    except Exception as e:
        print(f"Error: {e}")


update_avatar("happy")
root.mainloop()



chat_display = tk.Text() # виведення чату

input_display = tk.Entry()

input_button = tk.Button()