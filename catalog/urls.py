from django.urls import path
from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contacts, name="contacts"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
]
