1.
Скрип для запуска на хост-машине (проверяет наличие docker compose, если нет - ставит и запускает сам контейнер),
Ну и созданы ли контейнеры.
 ''' sudo ./docker-compose-up'''

2. Скрит для запуска докера с постргрес и создания нужных таблиц """task_two/start_postgres.sh"""
Активировтаь venv и установить asyncpg, можно руками, можно из req.txt 

Для заполнения бд использовал скрипт из task_two/filling_db.py (по 700 000 и 500 000 соответсвенно). Конкретно само заполнение
происходит достаточно долго.

Тестирование правильности переносов статусов в task_two\test_correct.py


Самый быстрый вариант решения в task_two/query_execution.py через запрос 
            '''
                UPDATE full_names fn
                SET status = sh.status
                FROM short_names sh
                WHERE SUBSTRING(fn.name, 1, POSITION('.' IN fn.name) - 1) = sh.name; 
                '''
                --  В данном случае, строки таблицы full_names обновляются только в том случае
                --, если подстрока до первой точки в столбце name совпадает со значением столбца name таблицы short_names.

Получили, в среднем, 2 секунды на весь скрипт.

Можно использовать split_part()

'''UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.status IS NULL
AND split_part(full_names.name, '.', 1) = short_names.name '''

Но такой запрос проигрывает около секунды (3 секунды на выполнение)

Если мы допускаем, что в именах файлов могут быть точки, аля 'naz.1' и 'naz.1.mp3' соответсвенно то можно использовать такой запрос
'''UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.status IS NULL
AND substring(full_names.name from '(.*)\.[^.]*$') = short_names.name
AND full_names.name LIKE '%' || short_names.name || '%' 
'''
Здесь функция substring() используется для извлечения подстроки
, начинающейся с начала строки и заканчивающейся перед последней точкой в имени файла в таблице full_names. 

можно использовать regexp_replace() для удаление всего после последней точки
 '''
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.status IS NULL
AND regexp_replace(full_names.name, '\.[^.]*$', '') = short_names.name
AND full_names.name LIKE '%' || short_names.name || '%'
'''