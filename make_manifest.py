import os
import hashlib
import json

# --- НАСТРОЙКИ ---
# Папка, в которой лежат ваши моды для сканирования
MODS_DIR = "vanila_mods"

# Файл, который будет создан
OUTPUT_FILE = "manifest_vanilla.json"

# Базовая ссылка, откуда лаунчер будет качать файлы. 
# Обязательно со слэшем на конце!
# Пример для ветки main: "https://raw.githubusercontent.com/Dibor2000/MC-Server-Files-New/main/vanila_mods/"
# Пример для релизов: "https://github.com/Dibor2000/MC-Server-Files-New/releases/download/Vanilla-1.0/"
BASE_URL = "https://raw.githubusercontent.com/Dibor2000/MC-Server-Files-New/main/vanila_mods/"


def get_file_md5(filepath):
    """Вычисляет MD5-хэш файла (тот же алгоритм, что и в лаунчере)"""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def generate_manifest():
    if not os.path.exists(MODS_DIR):
        print(f"❌ Ошибка: Папка '{MODS_DIR}' не найдена!")
        print("Создайте папку, положите в неё моды и запустите скрипт снова.")
        return

    manifest = {"files": []}
    files_count = 0

    print(f"🔍 Сканирование папки '{MODS_DIR}'...")

    for filename in os.listdir(MODS_DIR):
        filepath = os.path.join(MODS_DIR, filename)
        
        # Пропускаем папки, работаем только с файлами (.jar и др.)
        if os.path.isfile(filepath):
            file_md5 = get_file_md5(filepath)
            
            # Формируем структуру под один файл
            file_entry = {
                "path": f"mods/{filename}",          # Куда лаунчер положит файл
                "url": f"{BASE_URL}{filename}",      # Откуда лаунчер скачает файл
                "hash": file_md5                     # Хэш для проверки обновлений
            }
            manifest["files"].append(file_entry)
            files_count += 1
            print(f"  + Добавлен: {filename} (MD5: {file_md5[:8]}...)")

    # Сохраняем в JSON файл
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
        
    print("-" * 40)
    print(f"✅ Успех! Сгенерирован '{OUTPUT_FILE}'.")
    print(f"📦 Всего файлов добавлено: {files_count}")

if __name__ == "__main__":
    generate_manifest()
    input("\nНажмите Enter для выхода...")