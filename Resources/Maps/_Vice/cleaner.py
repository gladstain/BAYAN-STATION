import os
import sys
import re

def extract_prototypes_from_log(log_path):
    """
    Ищет в логе упоминания отсутствующих прототипов.
    Обычно они выглядят как: Could not find prototype 'Name' или Unknown prototype 'Name'
    """
    found_protos = set()
    # Регулярные выражения для поиска имен прототипов в кавычках после текста об ошибке
    patterns = [
        r"Could not find prototype '([^']+)'",
        r"Unknown prototype: ([^ \n]+)",
        r"Prototype '([^']+)' does not exist",
        r"PrototypeManager: Unknown prototype '([^']+)'"
    ]
    
    if not os.path.exists(log_path):
        print(f"![ВНИМАНИЕ]: Файл лога '{log_path}' не найден. Скрипт будет использовать пустой список.")
        return found_protos

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        log_content = f.read()
        for pattern in patterns:
            matches = re.findall(pattern, log_content)
            for match in matches:
                found_protos.add(match.strip())
    
    return found_protos

def clean_ss14_map(map_filename, log_filename):
    # Определяем пути
    try:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    except Exception:
        base_path = os.getcwd()
        
    map_path = os.path.join(base_path, map_filename)
    log_path = os.path.join(base_path, log_filename)
    output_path = os.path.join(base_path, f"cleaned_{map_filename}")

    print(f"--- АВТО-ОЧИСТКА SS14 ---")
    
    # 1. Извлекаем прототипы из лога
    bad_prototypes = extract_prototypes_from_log(log_path)
    
    if not bad_prototypes:
        print("? В логе не найдено ошибок прототипов. Либо лог пуст, либо формат ошибок изменился.")
    else:
        print(f"v Найдено прототипов для удаления: {len(bad_prototypes)}")
        for p in sorted(bad_prototypes):
            print(f"  - {p}")

    # 2. Проверяем карту
    if not os.path.exists(map_path):
        print(f"X ОШИБКА: Файл карты '{map_filename}' не найден в {base_path}")
        return

    # 3. Чистим карту
    with open(map_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    current_block = []
    is_skipping = False
    removed_count = 0

    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('- proto:'):
            if current_block:
                if not is_skipping:
                    cleaned_lines.extend(current_block)
                else:
                    removed_count += 1
            
            current_block = [line]
            proto_name = stripped.replace('- proto:', '').strip().strip('"\'')
            is_skipping = proto_name in bad_prototypes
        
        elif current_block:
            current_block.append(line)
        else:
            cleaned_lines.append(line)

    # Последний блок
    if current_block:
        if not is_skipping:
            cleaned_lines.extend(current_block)
        else:
            removed_count += 1

    # 4. Сохраняем
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    print(f"-------------------")
    print(f"УДАЛЕНО СУЩНОСТЕЙ: {removed_count}")
    print(f"РЕЗУЛЬТАТ: {output_path}")

if __name__ == "__main__":
    # Названия файлов (можешь изменить, если они другие)
    MAP_FILE = "map.yml"
    LOG_FILE = "errors.txt" 
    
    clean_ss14_map(MAP_FILE, LOG_FILE)