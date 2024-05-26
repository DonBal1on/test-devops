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
	- Собственно и сам домен

1. Склонировать код проекта
```bash
git clone https://github.com/DonBal1on/test-devops.git
```

2. Выполнить скрипт первоначальной настройки, что сделает скрипт?
- Настроит сертификат
- Изменит `nginx.conf` согласно указанному домену
- Настроит и запустить firewall
- Запустит `docker-compose.yml`
