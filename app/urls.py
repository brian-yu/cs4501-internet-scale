from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:id>/', views.user),
    path('items/<int:id>/', views.item),
    path('borrows/<int:id>/', views.borrow),
    path('reviews/<int:id>/', views.review),
]