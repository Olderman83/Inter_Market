from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" и назначает необходимые разрешения'

    def handle(self, *args, **options):
        # Получаем content type для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Создаем или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует'))

        # Получаем необходимые разрешения
        permissions_to_add = []

        # Разрешение на отмену публикации
        can_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type
        )
        permissions_to_add.append(can_unpublish)

        # Разрешение на модерацию
        can_moderate, _ = Permission.objects.get_or_create(
            codename='can_moderate_product',
            name='Может модерировать продукты',
            content_type=content_type
        )
        permissions_to_add.append(can_moderate)

        # Разрешение на удаление продуктов (стандартное)
        can_delete = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )
        permissions_to_add.append(can_delete)

        # Добавляем разрешения в группу
        group.permissions.add(*permissions_to_add)

        self.stdout.write(self.style.SUCCESS('Назначены следующие разрешения:'))
        for perm in permissions_to_add:
            self.stdout.write(f'  - {perm.name}')

        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно!'))
