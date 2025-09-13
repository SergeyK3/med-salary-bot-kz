#!/bin/bash
# filepath: ./remove_role_coefficients.sh

# Удалить все явные умножения на role_coefficients["врач"] и role_coefficients["медсестра"]
find . -type f -name "*.py" -exec sed -i \
    -e 's/\* *settings\["role_coefficients"\]\["врач"\]//g' \
    -e 's/\* *settings\["role_coefficients"\]\["медсестра"\]//g' \
    -e "s/\* *settings\['role_coefficients'\]\['врач'\]//g" \
    -e "s/\* *settings\['role_coefficients'\]\['медсестра'\]//g" \
    {} +

echo 'Все явные умножения на role_coefficients["врач"] и role_coefficients["медсестра"] удалены из .py файлов.'