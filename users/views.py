from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User


class RegisterView(CreateView):
    """
    Контроллер для регистрации пользователя
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """При успешной регистрации отправляем приветственное письмо"""
        response = super().form_valid(form)

        # Отправка приветственного письма
        try:
            subject = 'Добро пожаловать в Inter Market!'
            message = f'''
            Здравствуйте, {self.object.get_full_name() or self.object.email}!

            Благодарим вас за регистрацию в интернет-магазине Inter Market!

            Теперь вы можете:
            - Просматривать каталог товаров
            - Добавлять новые товары
            - Оставлять отзывы
            - Участвовать в акциях и получать скидки

            Если у вас возникнут вопросы, свяжитесь с нами:
            Email: {settings.DEFAULT_FROM_EMAIL}
            Телефон: +7 (123) 456-78-90

            С уважением,
            Команда Inter Market
            '''

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.object.email],
                fail_silently=False,
            )
            messages.success(self.request,
                             'Регистрация прошла успешно! '
                             'Приветственное письмо отправлено на вашу почту.')
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")
            messages.warning(self.request,
                             'Регистрация прошла успешно, '
                             'но не удалось отправить приветственное письмо.')

        # Автоматический вход после регистрации
        login(self.request, self.object)

        return response

    def form_invalid(self, form):
        """При ошибках формы показываем их пользователю"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Ошибка в поле "{field}": {error}')
        return super().form_invalid(form)


class LoginView(TemplateView):
    """
    Контроллер для авторизации пользователя
    """
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        """GET запрос - показываем форму"""
        if request.user.is_authenticated:
            messages.info(request, 'Вы уже авторизованы')
            return redirect('catalog:home')

        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """POST запрос - обрабатываем авторизацию"""
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.get_full_name() or user.email}!')

                # Перенаправление на страницу, с которой пришел пользователь
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('catalog:home')

        messages.error(request, 'Неверный email или пароль')
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    """
    Контроллер для выхода из системы
    """
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('catalog:home')


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для просмотра и редактирования профиля пользователя
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Возвращаем текущего пользователя"""
        return self.request.user

    def form_valid(self, form):
        """При успешном обновлении профиля"""
        response = super().form_valid(form)
        messages.success(self.request, 'Профиль успешно обновлен!')
        return response

    def get_context_data(self, **kwargs):
        """Добавляем дополнительную информацию в контекст"""
        context = super().get_context_data(**kwargs)
        context['user_products_count'] = self.request.user.product_set.count()  # если есть связь
        return context
