# WebPattern
* Для запуска перейти в папку less_1/
* Выполнить команду `python manage.py`

Less_2:
* Добавил обработку GET запросов c параметрами
* Добавил обработку POST запросов из формы
* Добавил аналог DB

Less_3:
* Добавил в проект использование базовы шаблонов jinja
* Реструктурировал файлы html

Less_4:
* В проекте присутсвует следующая структура:
  MeetUpList (звонки котоыре создают пользователя) - аналог курсов
  MeetUpType (типы звонков) - аналог категорий
* Чтобы создать звонок, сначала нужно создать тип звонка
* После создания типа звонка(из предложенных трех: **Team**,**Work**,**P2P**) создаем звонки
* Звонок с определенным типом можно скопировать
* Установил логгер
