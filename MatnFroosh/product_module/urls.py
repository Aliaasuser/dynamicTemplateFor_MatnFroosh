from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopPage_view.as_view(), name='shop_page'),
    path('product-details/<str:slug>/', views.ProductDetails_view.as_view(), name='product-details_page'),
    path('product-details/<str:slug>/preview/', views.product_preview_view, name='product-preview_page'),
]