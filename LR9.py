# Пример запросов из предыдущего занятия
'''
from sqlachemy import select
with engine.connect() as connection:
    statement=select(students)
    result=connection.execute(statement)
    for rom in result:
        print(row.id,row.name,row.is_active)
    statement2=select(students.c.name,students.c.gpa)
    result2=connection.execute(statement2)
    for row in result2:
        print(row.name,row.gpa)
from sqlachemy import update,delete
with engine.connect() as connection:
    statement=(update(students_table).where(students_table.c.name=='Petrov P.P.')
               .values(gpa=4.6))
    result=connection.execute(statement)
    connection.commit()
    print(f"обновление строк: {result.rowcount}")
    statement2=(delete(students_table).where(students_table.c.gpa<3.5))
    result=connection.execute(statement2)
    connection.commit()'''
# SQLAlchemy позволяет выполнять основные операции с таблицами базы данных

# Основная часть задания: работа с базой данных через SQLAlchemy
import json
from sqlalchemy import create_engine, insert, text
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, ForeignKey

path = "catalog.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
# Собираем уникальные категории и их описания
categories = []
for i in data:
    name = i["category"]["name"]
    categories.append((name, i["category"]["description"]))
categories = list(set(categories))# Присваиваем каждой категории свой идентификатор
category = [(i + 1, n, d) for i, (n, d) in enumerate(categories)]

# Формируем данные о товарах и относим их к нужным категориям
products = []
for i in data:
    idc = 0
    for n, name, d in category:
        if name == i["category"]["name"]:
            idc = n
            break
    products.append([
        i["product_name"],
        i["price"],
        idc])
# Настраиваем подключение и структуру базы данных
engine = create_engine("sqlite:///shop1.db", echo=True)# Создаем или открываем файл базы данных
metadata = MetaData()
# Описание таблицы категорий
categories_table = Table(
    "categories", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("description", String(200)))
# Описание таблицы товаров
products_table = Table(
    "products", metadata,
    Column("id", Integer, primary_key=True),
    Column("product_name", String(200)),
    Column("price", Float),
    Column("category_id", Integer, ForeignKey("categories.id")))

metadata.create_all(engine)
with engine.connect() as connection:
    connection.execute(text("PRAGMA foreign_keys = ON"))
    # Подготавливаем записи категорий для добавления в таблицу
    data_categories = [
        {"id": cid, "name": name, "description": desc}
        for cid, name, desc in category]
    result = connection.execute(insert(categories_table), data_categories)
    # Добавляем сведения о товарах с помощью команды INSERT
    data_products = [
        {"product_name": name, "price": price, "category_id": cid}
        for name, price, cid in products]
    result2 = connection.execute(insert(products_table), data_products)

    connection.commit()

    print(f"Количество добавленных категорий: {result.rowcount}")
    print(f"Количество добавленных товаров: {result2.rowcount}")

