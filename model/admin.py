from django.contrib import admin

from .models import Business, WaiterFeedback, Menu, CustomUser, Waiter, Category, Products,BusinessFeedback

# Register your models here.
admin.site.register(Business)
admin.site.register(WaiterFeedback)
admin.site.register(Waiter)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Menu)
admin.site.register(BusinessFeedback)
