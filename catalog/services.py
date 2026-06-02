from django.core.cache import cache
from .models import Product, Category
import logging

logger = logging.getLogger(__name__)


class ProductService:
    """Сервис для работы с продуктами с кешированием"""

    @staticmethod
    def get_products_by_category(category_id):
        """
        Возвращает список всех продуктов в указанной категории.

        """
        cache_key = f'category_{category_id}_products'
        products = cache.get(cache_key)

        if products is None:
            logger.info(f'Загрузка продуктов для категории {category_id} из БД')
            try:
                category = Category.objects.get(id=category_id)
                products = Product.objects.filter(
                    category=category,
                    publication_status=Product.PublicationStatus.PUBLISHED
                ).select_related('owner', 'category')

                # Кешируем результат на 10 минут (600 секунд)
                # Задание 4: TTL задан
                cache.set(cache_key, products, timeout=600)
                logger.info(f'Продукты для категории {category_id} закешированы')
            except Category.DoesNotExist:
                products = []

        return products
