#!/bin/bash

# Путь к папке с резервными копиями
BACKUP_DIR="../backups"
# Папка для резервного копирования
SOURCE_DIR="./db"

# Функция для проверки успешности выполнения команд
check_success() {
  if [ $? -ne 0 ]; then
    echo "Произошла ошибка. Скрипт прерван."
    exit 1
  fi
}

# Функция для создания резервной копии
backup() {
  TIMESTAMP=$(date +"%Y%m%d%H%M%S")
  BACKUP_NAME="db_backup_$TIMESTAMP.tar.gz"
  BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

  echo "Создание резервной копии $SOURCE_DIR в $BACKUP_PATH..."
  tar -czf "$BACKUP_PATH" "$SOURCE_DIR"
  check_success
  echo "Резервная копия создана: $BACKUP_PATH"
}

# Функция для восстановления последней резервной копии
restore() {
  LAST_BACKUP=$(ls -t $BACKUP_DIR/db_backup_*.tar.gz | head -n 1)

  if [ -z "$LAST_BACKUP" ]; then
    echo "Нет доступных резервных копий для восстановления."
    exit 1
  fi

  echo "Восстановление из резервной копии $LAST_BACKUP..."
  tar -xzf "$LAST_BACKUP" -C .
  check_success
  echo "Восстановление завершено."
}

# Проверка и создание папки резервных копий, если она не существует
if [ ! -d "$BACKUP_DIR" ]; then
  mkdir -p "$BACKUP_DIR"
  check_success
fi

# Проверка переданных ключей
if [ "$1" == "-b" ]; then
  backup
elif [ "$1" == "-r" ]; then
  restore
else
  echo "Использование: $0 -b (для создания резервной копии) или $0 -r (для восстановления последней резервной копии)"
  exit 1
fi

