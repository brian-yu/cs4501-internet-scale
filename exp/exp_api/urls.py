from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('users/', views.users),
    path('users/<int:id>/', views.user_detail),
    path('items/', views.items),
    path('items/<int:id>/', views.item_detail),

    # # CREATE requests
    # path('users/create/', views.create_user),
    # path('items/create/', views.create_item),
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
