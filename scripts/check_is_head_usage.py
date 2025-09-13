import os
import re

def find_is_head_usages(root='.'):
    pattern = re.compile(r'\bis_head\b')
    found = []

    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if pattern.search(line):
                            print(f"{filepath}:{i+1}: найдено использование 'is_head': {line.strip()}")
                            found.append(filepath)
    if not found:
        print("В проекте не найдено использование 'is_head'.")

if __name__ == '__main__':
    find_is_head_usages('.')