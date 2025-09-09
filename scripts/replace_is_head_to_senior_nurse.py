import os
import re

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Основные паттерны для замены
    replacements = [
        (r'["\']senior_nurse["\']', '"senior_nurse"'),            # Ключ в dict
        (r'\bis_head\b', 'senior_nurse'),                    # Переменная / аргумент
        (r'\bIS_HEAD\b', 'SENIOR_NURSE'),                    # Если где-то есть капс
        (r'\bIsHead\b', 'SeniorNurse'),                      # CamelCase (редко)
    ]

    new_content = content
    for pattern, repl in replacements:
        new_content = re.sub(pattern, repl, new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Изменено: {filepath}')

def walk_and_replace(root='.'):
    for dirpath, dirs, files in os.walk(root):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                replace_in_file(filepath)

if __name__ == '__main__':
    # Поменяйте '.' на путь к вашему репозиторию, если нужно
    walk_and_replace('.')