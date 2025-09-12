#!/bin/bash
# filepath: ./remove_role_coefficients_code.sh

# Поиск и удаление строк, содержащих умножение на settings["role_coefficients"]["врач"] или ["медсестра"]
find . -type f -name "*.py" -exec sed -i \
    -e '/\* *settings\["role_coefficients"\]\["врач"\]/d' \
    -e '/\* *settings\["role_coefficients"\]\["медсестра"\]/d' \
    -e "/\* *settings\['role_coefficients'\]\['врач'\]/d" \
    -e "/\* *settings\['role_coefficients'\]\['медсестра'\]/d" \
    {} +

echo 'Все строки с умножением на settings["role_coefficients"]["врач"] и ["медсестра"] удалены из .py файлов.'