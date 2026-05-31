from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from .models import Product, Category, Contact
from .forms import ProductForm, ProductModerationForm


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


class ContactsView(TemplateView):
    """Контроллер для страницы контактов"""
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем контакты из БД для отображения
        context['contacts'] = Contact.objects.all().order_by('-created_at')[:5]
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Сохраняем в БД
        Contact.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        messages.success(request, 'Сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
        return redirect('catalog:contacts')


class ProductCreateView(LoginRequiredMixin,CreateView):
    """Контроллер для добавления нового товара"""
    model = Product
    template_name = 'catalog/add_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{form.instance.name}" успешно добавлен!')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Ошибка в поле "{field}": {error}')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin,UpdateView):
    """Контроллер для редактирования товара"""
    model = Product
    template_name = 'catalog/add_product.html'
    form_class = ProductForm
    login_url = 'users:login'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{form.instance.name}" успешно обновлен!')
        return response

    def form_invalid(self, form):
        # Выводим все ошибки формы
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Ошибка в поле "{field}": {error}')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['is_update'] = True
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления товара"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f'Товар "{product.name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


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
