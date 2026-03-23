import sqlite3
import pandas as pd

dviz_df = pd.read_excel("3.xlsx", sheet_name="Движение товаров")
tovar_df = pd.read_excel("3.xlsx", sheet_name="Товар")
magaz_df = pd.read_excel("3.xlsx", sheet_name="Магазин")

dviz_df["Дата"] = pd.to_datetime(dviz_df["Дата"]).dt.strftime("%Y-%m-%d")

conn = sqlite3.connect(":memory:")

dviz_df.to_sql("dvizenie", conn, index=False, if_exists="replace")
tovar_df.to_sql("tovar", conn, index=False, if_exists="replace")
magaz_df.to_sql("magazin", conn, index=False, if_exists="replace")

cursor = conn.cursor()

cursor.execute("""
    SELECT SUM(d."Количество упаковок, шт" * t."Цена за упаковку")
    FROM dvizenie d
    JOIN tovar t ON d."Артикул" = t."Артикул"
    JOIN magazin m ON d."ID магазина" = m."ID магазина"
    WHERE t."Наименование товара" LIKE '%Сметана%'
      AND m."Адрес" LIKE '%Самолетная улица%'
      AND d."Тип операции" = 'Продажа'
      AND d."Дата" BETWEEN '2024-10-07' AND '2024-10-14'
""")

result = cursor.fetchone()[0]
print(result)

conn.close()
