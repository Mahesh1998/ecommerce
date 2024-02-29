from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_api, name="products"),
    path("products/<int:pk>", views.edit_product_api, name="editproducts")
]
