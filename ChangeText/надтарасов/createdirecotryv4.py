import os
import shutil

# 1. Визначення директорій та файлів
SOURCE_DIR = os.getcwd() 
DRAFT_DIR = "Draft"
FINAL_DIR = "Final"

# Словники для копіювання (вихідна_назва.tap: цільова_назва.nc)
draft_files2copy = {
    "обрезка.tap": "cut.nc",
    "черновая.tap": "draft.nc",
    "обрезка внутрь.tap": "cutinner.nc"
    }
final_files2copy = {
    "чистовая.tap": "final.nc"
}

# Мапа для заміни тексту (що_замінити: на_що_замінити)
REPLACEMENTS = {
    "F1800": "F1200",
    "F600": "F300",
    "F150": "F200"
}

# --- Функції для роботи з файловою системою ---

def setup_directories(dir_list):
    """Створює необхідні директорії."""
    print("--- Налаштування директорій ---")
    for directory in dir_list:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Директорія '{directory}' готова.")
        print("-" * 30)

def replace_text_in_file(filepath, replacements):
    """Виконує заміну тексту в одному файлі."""
    try:
        # 1. Зчитуємо вміст файлу
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 2. Виконуємо заміни
        new_content = content
        changes_made = False
        for old_text, new_text in replacements.items():
            if old_text in new_content:
                new_content = new_content.replace(old_text, new_text)
                changes_made = True
                
        # 3. Якщо були зміни, записуємо новий вміст назад у файл
        if changes_made:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
            return True
        return False

    except Exception as e:
        print(f"   ❌ Помилка обробки файлу {filepath}: {e}")
        return False

def copy_rename_and_modify(file_map, destination_dir, replacements):
    """Копіює, перейменовує та модифікує файли."""
    print(f"--- Обробка файлів для '{destination_dir}' ---")
    
    if not os.path.isdir(destination_dir):
        print(f"❌ Помилка: Цільова директорія '{destination_dir}' не знайдена.")
        return

    for source_name, target_name in file_map.items():
        source_path = os.path.join(SOURCE_DIR, source_name)
        target_path = os.path.join(destination_dir, target_name)
        
        # 1. Перевірка існування вихідного файлу
        if not os.path.exists(source_path):
            print(f"⚠️ Файл '{source_name}' не знайдено. Пропущено.")
            continue
        
        try:
            # 2. Копіювання та перейменування (оригінал не змінюється)
            shutil.copy2(source_path, target_path)
            print(f"➡️ Скопійовано '{source_name}' як '{target_name}'.")

            # 3. Заміна тексту в щойно скопійованому файлі
            if replace_text_in_file(target_path, replacements):
                print(f"   ☑️ Заміни тексту виконано в '{target_name}'.")
            else:
                 print(f"   ℹ️ Замін тексту не виявлено в '{target_name}'.")
                 
        except Exception as e:
            print(f"❌ Критична помилка обробки '{source_name}': {e}")
            
    print("-" * 30)


# --- Головний виклик функцій ---

# 1. Створюємо директорії
setup_directories([DRAFT_DIR, FINAL_DIR])

# 2. Обробляємо файли для Draft (копіювання, перейменування та модифікація)
copy_rename_and_modify(draft_files2copy, DRAFT_DIR, REPLACEMENTS)

# 3. Обробляємо файли для Final (копіювання, перейменування та модифікація)
copy_rename_and_modify(final_files2copy, FINAL_DIR, REPLACEMENTS)

print("✅ Усі операції завершено. Оригінальні .tap файли залишились незмінними.")
