### Работа программы
-----
Программа находит 5 ближайших кофеен по введенному адресу, и создает сайт-карту с отмеченными кофейнями (в файл 'index.html').(Работает только для Москвы)\
Код написан в образовательных целях.

#### Запуск программы
Шаги:
1. Скачать весь проект к себе.  
Установить библиотеки:
```python:
pip install -r requirments.txt
```
2. Создать API ключь. [Ссылка на создание](https://developer.tech.yandex.ru/)
3. Создать поблизости файл `.env` и написать в нем:
```commandline
YANDEX_APIKEY = 'Ваш API'
```
4. Осталось запустить программу и указать ваш адрес.
