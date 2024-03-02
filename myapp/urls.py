from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_api, name="products"),
    path("products/<int:pk>", views.product_api, name="editproducts"),
    path("users/", views.user_api, name="users"),
    path("users/<int:pk>", views.user_api, name="editusers"),
    path("orders/", views.products_bought_api, name="orders"),
    path("orders/<int:pk>", views.products_bought_api, name="deleteorders")
]
