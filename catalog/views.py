from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from .models import Product, Category, Contact
from .forms import ProductForm, ProductModerationForm
from .services import ProductService
import logging

logger = logging.getLogger(__name__)


class HomeListView(ListView):
    """Контроллер для домашней страницы с пагинацией"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        """Получаем все продукты с связанной категорией"""
        return Product.objects.all().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Последние 5 созданных продуктов (для консоли)
        recent_products = Product.objects.order_by('-created_at')[:5]
        print("Последние 5 добавленных товаров:")
        for product in recent_products:
            print(f"- {product.name} (${product.price})")

        context['recent_products'] = recent_products
        return context


class ProductDetailView(DetailView):
    """Контроллер для страницы с подробной информацией о товаре"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        """Показываем опубликованные продукты всем, а свои - владельцу"""
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            # Авторизованные видят свои продукты в любом статусе
            return qs.filter(
                models.Q(publication_status=Product.PublicationStatus.PUBLISHED) |
                models.Q(owner=self.request.user)
            )
        return qs.filter(publication_status=Product.PublicationStatus.PUBLISHED)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для добавления нового товара (только для авторизованных)"""
    model = Product
    template_name = 'catalog/add_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def form_valid(self, form):
        """Автоматически привязываем продукт к текущему пользователю"""
        form.instance.owner = self.request.user
        form.instance.publication_status = Product.PublicationStatus.MODERATION
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Товар "{form.instance.name}" отправлен на модерацию!'
        )
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Ошибка в поле "{field}": {error}')
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер для редактирования товара"""
    model = Product
    template_name = 'catalog/add_product.html'
    form_class = ProductForm
    login_url = 'users:login'

    def test_func(self):
        """Проверка прав: модератор или владелец"""
        product = self.get_object()
        return (self.request.user.has_perm('catalog.can_moderate_product') or
                product.owner == self.request.user)

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        messages.error(self.request, "У вас нет прав на редактирование этого товара")
        return redirect('catalog:home')

    def get_form_class(self):
        """Модераторы используют специальную форму"""
        if self.request.user.has_perm('catalog.can_moderate_product'):
            return ProductModerationForm
        return ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{form.instance.name}" успешно обновлен!')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Ошибка в поле "{field}": {error}')
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер для удаления товара"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def test_func(self):
        """Проверка прав: модератор или владелец"""
        product = self.get_object()
        return (self.request.user.has_perm('catalog.can_moderate_product') or
                product.owner == self.request.user)

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        messages.error(self.request, "У вас нет прав на удаление этого товара")
        return redirect('catalog:home')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f'Товар "{product.name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


class ContactsView(TemplateView):
    """Контроллер для страницы контактов"""
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all().order_by('-created_at')[:5]
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        messages.success(request, 'Сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
        return redirect('catalog:contacts')


class ModerationQueueView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Список продуктов на модерации (только для модераторов)"""
    model = Product
    template_name = 'catalog/moderation_queue.html'
    context_object_name = 'products'
    paginate_by = 20

    def test_func(self):
        return self.request.user.has_perm('catalog.can_moderate_product')

    def get_queryset(self):
        return Product.objects.filter(
            publication_status=Product.PublicationStatus.MODERATION
        ).select_related('category', 'owner')


class CategoryProductsView(ListView):
    """
    Отдельное представление для отображения продуктов в категории.

    """
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        """Используем сервисную функцию для получения продуктов по категории"""
        category_id = self.kwargs.get('category_id')
        return ProductService.get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')

        # Получаем категорию (не кешируем, так как это одно поле)
        try:
            context['category'] = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            context['category'] = None

        # Добавляем все категории для навигации
        context['all_categories'] = Category.objects.all()

        return context
