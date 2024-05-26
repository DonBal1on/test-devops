## Техническое задание DevOps

Нужно настроить приложение [flaskBlog](https://github.com/DogukanUrker/flaskBlog)


1. [x] Нужно настроить Dockerfile для приложения flaskBlog
2. [x] Написать docker-compose.yml чтобы там был flaskBlog и nginx
3. [x] Для этого решения необходимо настроить letsencrypt сертификаты для заранее созданного домена test-devops.vizorlabs.ru
4. [x] Поменять стандартный ssh порт на любой другой
5. [x] Настроить на виртуальной машины доступ только по 3 портам(ssh, http,https)
6. [x] Предусмотреть восстановление решения после рестарта сервера  
7. [ ] Настройка бэкапов, просто брать файлы из папки db и помещать их
8. [ ] Настройка восстановления из бэкапов
9. [ ] README с описанием как задеплоить сервер, как сделать бэкап, как восстановится из бэкапа
10. [ ] Оформить все в git репозиторий с публикацией в github
## Инструкция по настройке:
-  Pre-request:
	-  АА record DNS , указывающая на адрес машины.
	- Белый IP-адрес

1. Склонировать код проекта [FlaskBlog](https://github.com/DogukanUrker/flaskBlog/tree/main)
```bash
git clone https://github.com/DogukanUrker/flaskBlog.git
```
2. Установить certbot и его зависимости
```bash
sudo apt updat
sudo apt install certbot
sudo apt install python3-pip
pip install --upgrade certbot urllib3 requests requests-toolbelt
```

3. Получить сертификат для домена:
```bash
sudo certbot certonly --standalone -d domain.name.example
```

4. отредактировать `docker-compose.yml`
```yml
version: '3.8'
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    networks:
      - proxy_network
    restart: always
    

  app:
    image: dogukanurker/flaskBlogDevops:latest
    expose:
      - "5000"
    networks:
      - proxy_network 
    restart: always
    depends_on:
      - nginx
    build: .
    volumes:
      - ./db:/app/db

networks:
  proxy_network:
    driver: bridge

```
