1.
Скрип для запуска на хост-машине (проверяет наличие docker compose, если нет - ставит и запускает сам контейнер)
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

если таблицы в разных схемах добавляем название схем 

"""
UPDATE *имя_схемы_с_фул.full_names fn
SET status = sh.status
FROM *имя_схемы_с_шорт.short_names sh
WHERE SUBSTRING(fn.name, 1, POSITION('.' IN fn.name) - 1) = sh.name;
"""
