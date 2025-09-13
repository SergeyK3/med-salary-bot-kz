import os
import re

def check_and_suggest_salary_comparisons(root='.'):
    pattern = re.compile(r'assert\s+(.*?["\'](base_oklad|total_salary|allowances)["\'].*?)\s*([!=<>]+)\s*(\d+(?:\.\d+)?)')
    files_checked = []

    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename.startswith('test') and filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    m = pattern.search(line)
                    if m:
                        print(f"{filepath}:{i+1}: Найдено сравнение зарплаты:")
                        print(f"  {line.strip()}")
                        print("  Рекомендуется заменить на:")
                        print(f"  assert round({m.group(1)}, 2) {m.group(3)} round({m.group(4)}, 2)")
                        files_checked.append(filepath)
    if not files_checked:
        print("В тестах не найдено сравнений зарплаты для проверки округления.")

if __name__ == '__main__':
    check_and_suggest_salary_comparisons('.')