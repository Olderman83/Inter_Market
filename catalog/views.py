from django.shortcuts import render


# Create your views here.
def home(request):
    """Контроллер для домашней страницы"""
    return render(request, 'home.html')


def contacts(request):
    """Контроллер для страницы контактов"""
    success_message = None

    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f"Сообщение от {name} ({email}): {message}")

        success_message = "Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время."

    return render(request, 'catalog/contacts.html', {'success_message': success_message})
