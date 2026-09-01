import os
import re

def fix_salary_comparisons(root='.'):
    pattern = re.compile(r'assert\s+(.*?)\s*([!=<>]+)\s*(\d+(?:\.\d+)?)')
    replaced = 0

    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename.startswith('test') and filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                new_lines = []
                for line in lines:
                    m = pattern.search(line)
                    if m and any(key in m.group(1) for key in ['base_oklad', 'total_salary', 'allowances']):
                        new_line = re.sub(
                            pattern,
                            lambda x: f"assert round({x.group(1)}, 2) {x.group(2)} round({x.group(3)}, 2)",
                            line
                        )
                        if new_line != line:
                            replaced += 1
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
                if replaced:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Исправлено в {filepath}")
    print(f"Всего замен: {replaced}")

if __name__ == '__main__':
    fix_salary_comparisons('.')