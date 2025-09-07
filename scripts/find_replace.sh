#!/bin/sh
# filepath: scripts/find_replace.sh

if [ "$#" -ne 2 ]; then
  echo "Использование: $0 'старый_текст' 'новый_текст'"
  exit 1
fi

OLD="$1"
NEW="$2"

grep -rl --exclude-dir=.venv "$OLD" . | while read file; do
  sed -i "s/$OLD/$NEW/g" "$file"
  echo "Заменено в: $file"
done

echo "Готово."