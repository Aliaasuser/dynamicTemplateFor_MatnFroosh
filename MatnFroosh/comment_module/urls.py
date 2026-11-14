from django.urls import path
from . import views

urlpatterns = [
    path('more-comments-for-product/<str:slug>/', views.get_more_comments_for_product, name='more_comments_for_product'),

]