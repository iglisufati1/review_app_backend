from django.contrib import admin

from .models import Business, WaiterRating, Menu, CustomUser, Waiter, Category, Product,CategoryRating, ProductRating

# Register your models here.
admin.site.register(Business)
admin.site.register(WaiterRating)
admin.site.register(Waiter)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Menu)
admin.site.register(CategoryRating)
admin.site.register(ProductRating)
