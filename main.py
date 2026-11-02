import json
import sqlite3
from pathlib import Path


# Пути к файлам
BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "catalog.json"
DB_FILE = BASE_DIR / "shop.db"


def create_tables(connection):
    """Создаёт таблицы категорий и товаров."""
    connection.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)


def load_catalog(connection):
    """Читает JSON и записывает категории и товары в SQLite."""
    with JSON_FILE.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    if not isinstance(catalog, list):
        raise ValueError("Ожидался JSON-массив товаров.")

    for item in catalog:
        product_name = item["product_name"]
        price = item["price"]
        category = item["category"]

        category_name = category["name"]
        category_description = category.get("description", "")

        # Сначала добавляем категорию(Если она уже есть, обновляем её описание)
        connection.execute("""
            INSERT INTO categories (name, description)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET
                description = excluded.description
        """, (category_name, category_description))

        # Получаем ID категории, чтобы связать с ней товар.
        cursor = connection.execute(
            "SELECT id FROM categories WHERE name = ?",
            (category_name,)
        )
        category_id = cursor.fetchone()[0]

        # Добавляем товар и записываем внешний ключ category_id.
        connection.execute("""
            INSERT INTO products (name, price, category_id)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                price = excluded.price,
                category_id = excluded.category_id
        """, (product_name, price, category_id))


def main():
    if not JSON_FILE.exists():
        print(f"Файл не найден: {JSON_FILE}")
        print("Положите catalog.json в папку с main.py.")
        return

    # Включаем проверку внешних ключей в SQLite.
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        create_tables(connection)
        load_catalog(connection)

        categories_count = connection.execute(
            "SELECT COUNT(*) FROM categories"
        ).fetchone()[0]

        products_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        print("Данные успешно загружены!")
        print(f"Категорий в базе: {categories_count}")
        print(f"Товаров в базе: {products_count}")
        print(f"Файл базы данных: {DB_FILE.name}")


if __name__ == "__main__":
    main()
