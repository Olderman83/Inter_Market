from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .models import Product

# Запрещенные слова (вынесены в константу)
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа',
                   'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта с валидацией"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'price': 'Цена (₽)',
            'category': 'Категория',
            'image': 'Изображение',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите описание товара'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png'
            }),
        }

    def __init__(self, *args, **kwargs):
        """Добавляем стилизацию для всех полей (Задание 3)"""
        super().__init__(*args, **kwargs)

        # Добавляем классы Bootstrap ко всем полям, которые еще не имеют своих классов
        for field_name, field in self.fields.items():
            if field_name not in ['category']:  # у category уже есть класс form-select
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'

            # Добавляем валидацию для всех полей
            if field.required:
                field.widget.attrs['required'] = 'required'

    def clean_name(self):
        """Валидация названия продукта на запрещенные слова (Задание 1)"""
        name = self.cleaned_data.get('name', '')
        name_lower = name.lower()

        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in name_lower:
                raise ValidationError(
                    f'Название содержит запрещенное слово "{forbidden_word}". '
                    f'Пожалуйста, удалите его из названия.'
                )

        return name

    def clean_description(self):
        """Валидация описания продукта на запрещенные слова (Задание 1)"""
        description = self.cleaned_data.get('description', '')
        description_lower = description.lower()

        found_words = []
        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in description_lower:
                found_words.append(forbidden_word)

        if found_words:
            raise ValidationError(
                f'Описание содержит запрещенные слова: {", ".join(found_words)}. '
                f'Пожалуйста, удалите их из описания.'
            )

        return description

    def clean_price(self):
        """Валидация цены (не может быть отрицательной) (Задание 2)"""
        price = self.cleaned_data.get('price')

        if price is None:
            raise ValidationError('Цена не может быть пустой.')

        if price < 0:
            raise ValidationError('Цена не может быть отрицательной. Пожалуйста, введите корректную цену.')

        if price == 0:
            raise ValidationError(
                'Цена не может быть равна нулю. Если товар бесплатный, укажите символическую цену 1 ₽.')

        if price > 1_000_000:
            raise ValidationError(
                'Цена не может превышать 1 000 000 ₽. Для очень дорогих товаров свяжитесь с администратором.')

        return price

    def clean_image(self):
        """Валидация изображения (формат и размер) (Дополнительное задание)"""
        image = self.cleaned_data.get('image')

        if not image:
            return image

        # Проверка размера файла (максимум 5 МБ)
        if image.size > 5 * 1024 * 1024:
            raise ValidationError(
                f'Размер изображения не может превышать 5 МБ. '
                f'Ваш файл: {image.size / (1024 * 1024):.2f} МБ'
            )

        # Проверка формата файла
        valid_extensions = ['image/jpeg', 'image/jpg', 'image/png']
        if image.content_type not in valid_extensions:
            raise ValidationError(
                'Поддерживаются только форматы изображений: JPEG, JPG, PNG. '
                f'Ваш формат: {image.content_type}'
            )

        # Проверка разрешения изображения (опционально)
        try:
            width, height = get_image_dimensions(image)
            if width < 100 or height < 100:
                raise ValidationError(
                    f'Минимальное разрешение изображения: 100x100 пикселей. '
                    f'Ваше изображение: {width}x{height} пикселей'
                )
            if width > 4000 or height > 4000:
                raise ValidationError(
                    f'Максимальное разрешение изображения: 4000x4000 пикселей. '
                    f'Ваше изображение: {width}x{height} пикселей'
                )
        except Exception:
            # Если не удалось определить размеры, пропускаем эту проверку
            pass

        return image


class ProductModerationForm(forms.ModelForm):
    """Форма для модерации продукта (только для модераторов)"""

    class Meta:
        model = Product
        fields = ['publication_status', 'category']
        widgets = {
            'publication_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs['class'] = 'form-control'
