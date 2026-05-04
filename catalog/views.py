from django.shortcuts import render
from django.contrib import messages
from .models import Product, Category, Contact
from django.shortcuts import render, get_object_or_404

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

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


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


def add_product(request):
    """Добавление нового товара"""
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')

        # Создаем новый продукт
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            category_id=category_id
        )

        messages.success(request, f'Товар "{product.name}" успешно добавлен!')
        return redirect('catalog:product_detail', pk=product.pk)

    categories = Category.objects.all()
    return render(request, 'catalog/add_product.html', {'categories': categories})
