from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogPost


class BlogListView(ListView):
    """Список опубликованных статей блога"""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        """Выводим только опубликованные статьи"""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    """Детальный просмотр статьи с увеличением счетчика просмотров"""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Переопределяем для увеличения счетчика просмотров"""
        obj = super().get_object(queryset=queryset)
        obj.increment_views()

        # Дополнительное задание: отправка письма при 100 просмотрах
        if obj.views_count == 100:
            self.send_congratulation_email(obj)

        return obj

    def send_congratulation_email(self, post):
        """Отправляет поздравление при достижении 100 просмотров"""
        try:
            subject = f'Поздравление! Статья "{post.title}" набрала 100 просмотров!'
            message = f'''
            Поздравляем! Ваша статья "{post.title}" достигла 100 просмотров!

            Статистика:
            - Заголовок: {post.title}
            - Просмотров: {post.views_count}
            - Дата создания: {post.created_at.strftime("%d.%m.%Y %H:%M")}

            Продолжайте в том же духе!
            '''

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],  # отправляем на почту администратора
                fail_silently=False,
            )
            print(f"Поздравление отправлено для статьи: {post.title}")
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")


class BlogCreateView(CreateView):
    """Создание новой статьи"""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def form_valid(self, form):
        response = super().form_valid(form)
        status = 'опубликована' if form.instance.is_published else 'сохранена как черновик'
        messages.success(self.request, f'Статья "{form.instance.title}" успешно {status}!')
        return response

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(UpdateView):
    """Редактирование статьи"""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def form_valid(self, form):
        response = super().form_valid(form)
        status = 'опубликована' if form.instance.is_published else 'сохранена как черновик'
        messages.success(self.request, f'Статья "{form.instance.title}" успешно обновлена ({status})!')
        return response

    def get_success_url(self):
        """Перенаправление после редактирования"""
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление статьи"""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        messages.success(request, f'Статья "{post.title}" успешно удалена!')
        return super().delete(request, *args, **kwargs)
