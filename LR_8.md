**Создадим две таблицы**
```python
import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")

cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM customers")


cursor.executemany("INSERT INTO customers(name) VALUES (?)", [
    ("Ivan",),
    ("Peter",),
    ("Kolya",),
    ("Serj",),
])


cursor.executemany("INSERT INTO orders(customer_id, amount) VALUES (?, ?)", [
    (3, 100500),
    (1, 100.5),
    (4, 123),
    (2, 246),
    (1, 369.5),
])

conn.commit()
conn.close()
```

**В таком случае будет возникать ошибка**
```python
import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON ;")
cursor.execute("CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")

cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM customers")


cursor.executemany("INSERT INTO customers(name) VALUES (?)", [
    ("Ivan",),
    ("Peter",),
    ("Kolya",),
    ("Serj",),
])


cursor.executemany("INSERT INTO orders(customer_id, amount) VALUES (?, ?)", [
    (3, 100500),
    (1, 100.5),
    (4, 123),
    (2, 246),
    (1, 369.5),
    (999, 66.6)
])

conn.commit()
conn.close()

```

**Каскадное удаление**
```python
CREATE TABLE orders ("id INTEGER PRIMARY KEY, customer_id INTEGER, FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE)
```

**ON DELETE CASCADE:**
1. RESTRICT
2. CASCADE
3. SET NULL
4. SET DEFAULT
5. NO ACTION

```python
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, Boolean, insert
)

engine = create_engine("sqlite:///school.db")
metadata = MetaData()

students_table = Table(
    "students", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("group_name", String(20)),          
    Column("gpa", Float, default=0.0),
    Column("is_active", Boolean, default=True),
)

metadata.create_all(engine)                    

with engine.connect() as connection:
    something = insert(students_table).values(name="Ivanov", gpa=4.5)
    result = connection.execute(something)
    connection.commit()
    print(f"Добавлена строка с id = {result.inserted_primary_key[0]}")