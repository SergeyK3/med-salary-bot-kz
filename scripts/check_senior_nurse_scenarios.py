import os
import re

def check_senior_nurse_scenarios(root='.'):
    nurse_pattern = re.compile(r'"senior_nurse"\s*:\s*True')
    role_pattern = re.compile(r'"role"\s*:\s*"?медсестра"?')
    education_pattern = re.compile(r'"education"\s*:\s*"?среднее"?')

    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename.startswith('test') and filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                for m in nurse_pattern.finditer(content):
                    block = content[max(0, m.start()-150):m.end()+150]
                    role_found = role_pattern.search(block)
                    edu_found = education_pattern.search(block)
                    if not role_found or not edu_found:
                        print(f"{filepath}: сценарий с senior_nurse=True, но не указаны role/education рядом.")
                        print("  Блок кода:")
                        print(block)
    print("Проверка завершена.")

if __name__ == '__main__':
    check_senior_nurse_scenarios('.')