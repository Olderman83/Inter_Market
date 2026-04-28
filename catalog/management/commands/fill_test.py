from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми продуктами"

    def handle(self, *args, **options):
        # Очищаем существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        categories_data = [
            {
                "name": "Электроника",
                "description": "Смартфоны, ноутбуки и другая техника",
            },
            {"name": "Одежда", "description": "Модная одежда для всех возрастов"},
            {"name": "Книги", "description": "Художественная и учебная литература"},
            {"name": "Спорт", "description": "Спортивный инвентарь и одежда"},
            {"name": "Дом", "description": "Товары для дома и сада"},
        ]

        categories = []
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories.append(category)
            self.stdout.write(f"Создана категория: {category.name}")

        # Создаем продукты
        products_data = [
            {
                "name": "iPhone 14 Pro",
                "description": "Флагманский смартфон Apple",
                "category": categories[0],
                "price": 999.99,
            },
            {
                "name": "Samsung Galaxy S23",
                "description": "Мощный Android-смартфон",
                "category": categories[0],
                "price": 899.99,
            },
            {
                "name": "MacBook Pro 14",
                "description": "Ноутбук для профессионалов",
                "category": categories[0],
                "price": 1999.99,
            },
            {
                "name": "Футболка хлопковая",
                "description": "Удобная повседневная футболка",
                "category": categories[1],
                "price": 29.99,
            },
            {
                "name": "Джинсы классические",
                "description": "Качественные джинсы",
                "category": categories[1],
                "price": 79.99,
            },
            {
                "name": "Django для профессионалов",
                "description": "Книга по Django",
                "category": categories[2],
                "price": 49.99,
            },
            {
                "name": "Футбольный мяч",
                "description": "Официальный мяч для футбола",
                "category": categories[3],
                "price": 39.99,
            },
            {
                "name": "Кофеварка",
                "description": "Варит вкусный кофе",
                "category": categories[4],
                "price": 149.99,
            },
        ]

        for prod_data in products_data:
            product = Product.objects.create(**prod_data)
            self.stdout.write(f"Создан продукт: {product.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создано {len(categories)} категорий и {len(products_data)} продуктов"
            )
        )
