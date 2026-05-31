from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    """
    Модель категории товаров
    """

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""

    # Статусы публикации
    class PublicationStatus(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        MODERATION = 'moderation', 'На модерации'
        PUBLISHED = 'published', 'Опубликован'
        REJECTED = 'rejected', 'Отклонен'

    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    # Новое поле для владельца продукта
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Владелец'
    )

    # Новое поле для статуса публикации
    publication_status = models.CharField(
        max_length=20,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        verbose_name='Статус публикации'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

        # Кастомные права
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
            ('can_moderate_product', 'Может модерировать продукты'),
        ]

    def __str__(self):
        return self.name

    def get_short_description(self, length=100):
        """Возвращает краткое описание товара"""
        if len(self.description) > length:
            return self.description[:length] + '...'
        return self.description

    def can_user_edit(self, user):
        """Проверяет, может ли пользователь редактировать продукт"""
        if not user.is_authenticated:
            return False
        # Владелец может редактировать
        if self.owner == user:
            return True
        # Модератор может редактировать статус
        if user.has_perm('catalog.can_moderate_product'):
            return True
        return False

    def can_user_delete(self, user):
        """Проверяет, может ли пользователь удалить продукт"""
        if not user.is_authenticated:
            return False
        # Владелец может удалить
        if self.owner == user:
            return True
        # Модератор может удалить
        if user.has_perm('catalog.can_moderate_product'):
            return True
        return False


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.name} - {self.created_at}"
