from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:id>/', views.user),
    path('users/<int:id>/delete', views.delete_user),
    path('items/<int:id>/', views.item),
    path('items/<int:id>/delete', views.delete_item),
    path('borrows/<int:id>/', views.borrow),
    path('borrows/<int:id>/delete', views.delete_borrow),
    path('reviews/<int:id>/', views.review),
    path('reviews/<int:id>/delete', views.delete_review),
]