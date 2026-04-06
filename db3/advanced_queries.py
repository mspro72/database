import sqlite3

conn = sqlite3.connect("students.db")
cur = conn.cursor()

# CASE Задание 1 Категория успеваемости стуентов 
print("\nCASE запрос 1: Категория успеваемости студентов")

cur.execute("""
    SELECT
        фамилия,
        имя,
        средний_балл,
        CASE
            WHEN средний_балл >= 90 THEN 'Отличник'
            WHEN средний_балл >= 75 THEN 'Хорошист'
            WHEN средний_балл >= 60 THEN 'Троечник'
            ELSE 'Неуспевающий'
        END AS категория
    FROM студенты
    ORDER BY средний_балл DESC
""")

for row in cur.fetchall():
    print(row)

# CASE запрос 2: Сколько человек по категориям успеваемости
print("\nCASE запрос 2: Всего студентов / Сколько отличников / хорошистов / троечников по направлениям")

cur.execute("""
    SELECT
        н.название AS направление,
        COUNT(*) AS всего,
        SUM(CASE WHEN с.средний_балл >= 90 THEN 1 ELSE 0 END) AS отличники,
        SUM(CASE WHEN с.средний_балл >= 75 AND с.средний_балл < 90 THEN 1 ELSE 0 END) AS хорошисты,
        SUM(CASE WHEN с.средний_балл < 75 THEN 1 ELSE 0 END) AS троечники
    FROM студенты с
    JOIN направления н ON с.id_направления = н.id_направления
    GROUP BY н.название
    ORDER BY н.название
""")

for row in cur.fetchall():
    print(row)

# Задание 2: Подзапросы
print("\nЗАДАНИЕ 2: ПОДЗАПРОСЫ")
# Подзапрос 1: Студенты с баллом выше среднего
print("\nПодзапрос 1: Студенты с баллом выше среднего по всей базе")

cur.execute("""
    SELECT
        фамилия,
        имя,
        средний_балл
    FROM студенты
    WHERE средний_балл > (SELECT AVG(средний_балл) FROM студенты)
    ORDER BY средний_балл DESC
""")

for row in cur.fetchall():
    print(row)
# Подзапрос 2: Направления, где средний балл выше среднего
print("\nПодзапрос 2: Направления, где средний балл выше среднего по базе")

cur.execute("""
    SELECT
        н.название AS направление,
        ROUND(AVG(с.средний_балл), 1) AS средний_балл
    FROM студенты с
    JOIN направления н ON с.id_направления = н.id_направления
    GROUP BY н.название
    HAVING AVG(с.средний_балл) > (SELECT AVG(средний_балл) FROM студенты)
    ORDER BY средний_балл DESC
""")

for row in cur.fetchall():
    print(row)

# Задание 3: CTE
print("\nЗАДАНИЕ 3: CTE")
# CTE 1: Лучший студент каждого направления
print("\nCTE 1: Лучший студент каждого направления")

cur.execute("""
    WITH лучшие_по_направлениям AS (
        SELECT
            с.фамилия,
            с.имя,
            с.средний_балл,
            н.название AS направление,
            MAX(с.средний_балл) OVER (PARTITION BY с.id_направления) AS макс_балл_направления
        FROM студенты с
        JOIN направления н ON с.id_направления = н.id_направления
    )
    SELECT
        направление,
        фамилия,
        имя,
        средний_балл
    FROM лучшие_по_направлениям
    WHERE средний_балл = макс_балл_направления
    ORDER BY направление
""")

for row in cur.fetchall():
    print(row)

# CTE 2: Направления выше среднего + очники выше среднего
print("\nCTE 2: Направления выше среднего + очники выше среднего (два CTE)")

cur.execute("""
    WITH статистика_направлений AS (
        SELECT
            н.название       AS направление,
            COUNT(*)         AS студентов,
            ROUND(AVG(с.средний_балл), 1) AS средний_балл
        FROM студенты с
        JOIN направления н ON с.id_направления = н.id_направления
        GROUP BY н.название
    ),
    выше_среднего AS (
        SELECT *
        FROM статистика_направлений
        WHERE средний_балл > (SELECT AVG(средний_балл) FROM студенты)
    )
    SELECT *
    FROM выше_среднего
    ORDER BY средний_балл DESC
""")

for row in cur.fetchall():
    print(row)


conn.close()
print("\nГотово!")
