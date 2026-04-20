from django.shortcuts import render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """
    Контроллер для отображения домашней страницы
    """
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'catalog/home.html', context)


def contacts(request: HttpRequest) -> HttpResponse:
    """
    Контроллер для отображения страницы с контактной информацией
    и обработки формы обратной связи
    """
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Здесь можно добавить логику отправки email или сохранения в базу данных
        # Например, просто выводим в консоль для демонстрации
        print(f"Получено сообщение от {name} ({email}): {message}")

        # Добавляем сообщение об успешной отправке
        messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')

        # Остаемся на той же странице (GET запрос после POST)
        # Возвращаем пустую форму после успешной отправки
        return render(request, 'catalog/contacts.html')

    # GET запрос - просто показываем форму
    return render(request, 'catalog/contacts.html')
