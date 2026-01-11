from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = "Ти персональний помічник, розроблений для персонального використання студенто комп'ютерної академії. Твоя задача підказувати, але не виконувати завдання замість користувача. Відповідай українською мовою."


client = genai.Client(api_key="key")


def main():    
    config  = types.GenerateContentConfig(
        system_instruction = SYSTEM_INSTRUCTION,
    )
    
    while True:
        user_input = input("Ти: ").strip() 
        if not user_input:
            print("Будь ласка, введіть повідомлення.")
            continue
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
            config=config,
        )
        response_message = response.text
        print("Jarvis:", response_message)
       
        
if __name__ == "__main__":  
    main()
