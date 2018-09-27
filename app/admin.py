from django.contrib import admin

from .models import User, Item, Borrow, Review

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Borrow)
admin.site.register(Review)