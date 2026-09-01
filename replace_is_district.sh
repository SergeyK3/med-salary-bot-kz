#!/bin/bash
# filepath: ./replace_is_district.sh

# Заменить во всех .py файлах в рабочей директории и подпапках
find . -type f -name "*.py" -exec sed -i 's/is_district/is_uchastok/g' {} +

echo 'Все вхождения "is_district" заменены на "is_uchastok" во всех .py файлах.'