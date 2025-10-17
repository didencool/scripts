import os
import shutil

# 1. Визначення директорій та файлів
SOURCE_DIR = os.getcwd() # Поточна директорія
DRAFT_DIR = "Draft"
FINAL_DIR = "Final"

# Словник для файлів, які копіюються до директорії DRAFT
draft_files_to_copy = {
    "обрезка.tap": "cut.nc",
    "черновая.tap": "draft.nc"
}

# Словник для файлів, які копіюються до директорії FINAL
final_files_to_copy = {
    "чистовая.tap": "final.nc"
}

def setup_directories(dir_list):
    """Створює необхідні директорії."""
    print("--- Налаштування директорій ---")
    for directory in dir_list:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Директорія '{directory}' готова.")
    print("-" * 30)

def copy_and_rename_files(file_map, destination_dir):
    """Копіює та перейменовує файли відповідно до мапи."""
    print(f"--- Копіювання файлів до '{destination_dir}' ---")
    
    # Перевіряємо, чи існує цільова директорія
    if not os.path.isdir(destination_dir):
        print(f"❌ Помилка: Цільова директорія '{destination_dir}' не знайдена.")
        return

    for source_name, target_name in file_map.items():
        source_path = os.path.join(SOURCE_DIR, source_name)
        target_path = os.path.join(destination_dir, target_name)
        
        # Перевіряємо, чи існує вихідний файл
        if not os.path.exists(source_path):
            print(f"⚠️ Файл '{source_name}' не знайдено у поточній директорії. Пропущено.")
            continue
        
        try:
            # Копіюємо файл з вихідної назви у цільову директорію з новою назвою
            shutil.copy2(source_path, target_path)
            print(f"➡️ Скопійовано '{source_name}' як '{target_name}' до '{destination_dir}'.")
        except Exception as e:
            print(f"❌ Помилка копіювання файлу '{source_name}': {e}")

# --- Головний виклик функцій ---

# 1. Створюємо директорії
setup_directories([DRAFT_DIR, FINAL_DIR])

# 2. Копіюємо та перейменовуємо файли до Draft
copy_and_rename_files(draft_files_to_copy, DRAFT_DIR)

# 3. Копіюємо та перейменовуємо файли до Final
copy_and_rename_files(final_files_to_copy, FINAL_DIR)
