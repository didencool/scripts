import os
import sys

# Назви директорій, які потрібно створити
DIRECTORY_NAMES = ["Draft", "Final"]

def create_directories(names):
    """
    Створює список директорій у поточній робочій директорії.
    """
    print(f"Поточна робоча директорія: {os.getcwd()}")
    print("Спроба створити директорії...")

    all_created = True
    
    for name in names:
        try:
            # os.makedirs створює директорію.
            # exist_ok=True запобігає помилці, якщо директорія вже існує.
            os.makedirs(name, exist_ok=True)
            print(f"✅ Директорія '{name}' успішно створена або вже існувала.")
        except OSError as e:
            all_created = False
            print(f"❌ Помилка при створенні директорії '{name}': {e}", file=sys.stderr)

    if all_created:
        print("\nЗавершено. Усі зазначені директорії готові.")
    else:
        print("\nЗавершено з деякими помилками.")

if __name__ == "__main__":
    create_directories(DIRECTORY_NAMES)



