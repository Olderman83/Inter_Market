from django.shortcuts import render
from django.contrib import messages

from django.shortcuts import render
from django.contrib import messages
from .models import Product


def home(request):
    """Контроллер для домашней страницы с последними 5 продуктами"""
    # Получаем последние 5 созданных продуктов
    last_products = Product.objects.all()[:5]

    # Выводим в консоль
    print("Последние 5 продуктов:")
    for product in last_products:
        print(f"- {product.name} (${product.price}) - {product.created_at}")

    context = {
        'products': last_products,
        'title': 'Главная - Skystore'
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Контроллер для страницы контактов с формой обратной связи"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно добавить отправку email или сохранение в БД
        print(f"Получено сообщение от {name} ({phone}): {message}")

        messages.success(request, 'Спасибо! Ваше сообщение отправлено.')

    return render(request, 'catalog/contacts.html')
