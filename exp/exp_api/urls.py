from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('all_items/', views.all_items),

    path('users/', views.users),
    path('users/<int:id>/', views.user_detail),
    path('users/getid/<str:auth>/', views.getid),
    path('items/', views.items),
    path('items/<int:id>/', views.item_detail),
    path('spark/', views.addToSpark),

    # CREATE requests
    path('users/create/', views.register),
    path('items/create/', views.create_item),

    path('login/', views.login),
    path('search/', views.search),

    # path('borrows/create/', views.create_borrow),
    # path('reviews/create/', views.create_review),

    # # GET and UPDATE requests
    # path('users/<int:id>/', views.user),
    # path('items/<int:id>/', views.item),
    # path('borrows/<int:id>/', views.borrow),
    # path('reviews/<int:id>/', views.review),

    # # DELETE requests
    # path('users/<int:id>/delete/', views.delete_user),
    # path('items/<int:id>/delete/', views.delete_item),
    # path('borrows/<int:id>/delete/', views.delete_borrow),
    # path('reviews/<int:id>/delete/', views.delete_review),
]
