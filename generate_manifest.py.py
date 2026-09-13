import os
import json
import hashlib

# Базовый URL для скачивания сырых файлов с вашего GitHub
BASE_URL = "https://raw.githubusercontent.com/Dibor2000/MC-Server-Files-New/main/"

# Указываем, какие папки и файлы сканировать ("." означает текущую папку для захвата servers.dat)
TARGETS = ["mods", "config", "."]

# Файлы, которые скрипт должен игнорировать (не передавать игрокам)
IGNORE_FILES = ["generate_manifest.py", "manifest.json", "launcher_version.json", "launcher.py", ".gitignore"]

def get_file_md5(filepath):
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def generate_manifest():
    manifest = {"files": []}
    
    for target in TARGETS:
        if not os.path.exists(target):
            continue
            
        if os.path.isfile(target):
            # Если это отдельный файл в корне (например, servers.dat)
            if target not in IGNORE_FILES and not target.startswith(".git"):
                file_hash = get_file_md5(target)
                url = BASE_URL + target.replace("\\", "/")
                manifest["files"].append({"path": target, "hash": file_hash, "url": url})
        else:
            # Если это папка (mods, config)
            for root, dirs, files in os.walk(target):
                # Пропускаем скрытые папки (.git)
                if ".git" in root:
                    continue
                for file in files:
                    if file in IGNORE_FILES:
                        continue
                        
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, ".")
                    file_hash = get_file_md5(filepath)
                    
                    # Формируем прямую ссылку
                    url = BASE_URL + rel_path.replace("\\", "/")
                    manifest["files"].append({
                        "path": rel_path.replace("\\", "/"),
                        "hash": file_hash,
                        "url": url
                    })

    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    print("Манифест успешно сгенерирован!")

if __name__ == "__main__":
    generate_manifest()