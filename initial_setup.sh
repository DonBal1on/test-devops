#!/bin/bash

# Функция для проверки успешности выполнения команд
check_success() {
  if [ $? -ne 0 ]; then
    echo "Произошла ошибка. Скрипт прерван."
    exit 1
  fi
}

# Установка certbot и его зависимостей
echo "Установка certbot и его зависимостей..."
sudo apt update
check_success
sudo apt install -y certbot python3-pip
check_success
pip install --upgrade certbot urllib3 requests requests-toolbelt
check_success

# Установка и настройка ufw
echo "Установка и настройка ufw..."
sudo apt install -y ufw
check_success

echo "Открытие портов 22, 49005, 443 и 80..."
sudo ufw allow 22
check_success
sudo ufw allow 49005
check_success
sudo ufw allow 443
check_success
sudo ufw allow 80
check_success

echo "Включение ufw..."
sudo ufw enable
check_success

# Запрос доменного имени у пользователя
read -p "Введите доменное имя (например, example.com): " SERVER_NAME

# Получение SSL сертификата
echo "Получение SSL сертификата для $SERVER_NAME..."
sudo certbot certonly --standalone -d "$SERVER_NAME"
check_success

# Установка переменной окружения SERVER_NAME
export SERVER_NAME="$SERVER_NAME"

# Путь к шаблону nginx.conf
NGINX_CONF_TEMPLATE="./nginx/nginx.conf.template"
# Путь к итоговому файлу nginx.conf
NGINX_CONF="./nginx/nginx.conf"

# Проверка наличия файла шаблона
if [ ! -f "$NGINX_CONF_TEMPLATE" ]; then
  echo "Файл $NGINX_CONF_TEMPLATE не найден."
  exit 1
fi

# Использование envsubst для замены переменной окружения в шаблоне конфигурации
echo "Замена переменной окружения в nginx.conf..."
envsubst '${SERVER_NAME}' < "$NGINX_CONF_TEMPLATE" > "$NGINX_CONF"
check_success

echo "Файл $NGINX_CONF успешно обновлен."

# Запуск docker-compose
echo "Запуск docker-compose..."
docker-compose up -d
check_success

echo "Скрипт успешно выполнен."

