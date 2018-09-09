# HTML diff service

Cервис для сравнения документов свёрстанных в html, показывающий разницу между двумя файлами. Выводит построчно изменения, сделанные в файле.

# Установка

Для запуска программы требуется установленный Python 3.5.  
В программе используются следующие сторонние библиотеки:  
- [aiohttp](https://aiohttp.readthedocs.io/en/stable/)  
- [aiohttp-jinja2](https://github.com/aio-libs/aiohttp-jinja2)  

Используйте команду pip для установки сторонних библиотек из файла зависимостей (или pip3 если есть конфликт с предустановленным Python 2):
```
pip install -r requirements.txt # В качестве альтернативы используйте pip3
```
Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).

# Использование

Запуск сервера:
```
$ python server.py 
======== Running on http://localhost:8080 ========
(Press CTRL+C to quit)

```
После запуска сервис доступен по адресу [http://127.0.0.1:8080/](http://127.0.0.1:8080)

### Пример работы сервиса:

![Diff screenshot](https://raw.githubusercontent.com/igorzakhar/35_diff_service/master/screenshot/diff_screenshot.png)

### Пример использования в командной строке
```
$ python htmldiff.py  file1.html  file2.html 
equal  (1, '<ul>')                              (1, '<ul>')                             
delete (2, '  <li>Автор: Григорьев П.А.</li>')  ('', '')                                
move   (3, '  <li>Сумма: 126000 руб.</li>')     (2, '  <li>Сумма: 126000 руб.</li>')    
add    ('', '')                                 (3, '  <li>Автор: Петров Г.Е.</li>')    
equal  (4, '  <li>Дата: 26.12.14</li>')         (4, '  <li>Дата: 26.12.14</li>')        
equal  (5, '</ul>')                             (5, '</ul>') 
```

# Цели проекта

Код написан для образовательных целей. Учебный курс для веб-разработчиков - [DEVMAN.org](https://devman.org)
