from django.urls import path
from catalog import views
from django.views.decorators.cache import cache_page

app_name = "catalog"

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60)(views.ProductDetailView.as_view()), name='product_detail'),
    path('product/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('moderation/', views.ModerationQueueView.as_view(), name='moderation_queue'),
    path('category/<int:category_id>/', views.CategoryProductsView.as_view(), name='category_products'),
]
