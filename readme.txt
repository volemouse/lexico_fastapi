1.
Скрип для запуска на хост-машине (проверяет наличие docker compose, если нет - ставит и запускает сам контейнер)
 ''' sudo ./docker-compose-up'''

2. Для заполнения бд использовал скрипт из task_two/filling_db.py (по 700 000 и 500 000 соответсвенно)

Самый быстрый вариант решения в принципе не требует даже в task_two/query_execution.py через запрос 
            '''UPDATE full_names fn
                SET status = sh.status
                FROM short_names sh
                WHERE SUBSTRING(fn.name, 1, POSITION('.' IN fn.name) - 1) = sh.name; '''
                --  В данном случае, строки таблицы full_names обновляются только в том случае
                --, если подстрока до первой точки в столбце name совпадает со значением столбца name таблицы short_names.


Получили, в среднем 2 секунды.