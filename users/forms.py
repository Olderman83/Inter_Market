from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        }),
        help_text='Введите действующий email, на него придет письмо с подтверждением'
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        help_text='Пароль должен содержать минимум 8 символов'
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        }),
        help_text='Введите тот же пароль еще раз'
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        })
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваша фамилия'
        })
    )

    phone = forms.CharField(
        label='Телефон',
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{10,15}$',
                message='Введите корректный номер телефона (10-15 цифр, может начинаться с +)'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7XXXXXXXXXX'
        })
    )

    country = forms.CharField(
        label='Страна',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваша страна'
        })
    )

    avatar = forms.ImageField(
        label='Аватар',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'country', 'avatar']

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Используем email как username
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации пользователя
    """
    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Переименовываем поле username в email для отображения
        self.fields['username'].label = 'Электронная почта'


class UserProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'country', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша фамилия'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7XXXXXXXXXX'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша страна'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
