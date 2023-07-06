from django.contrib import admin
from.models import Business, WaiterFeedback, ProductFeedback,  CustomUser,Waiter

# Register your models here.
admin.site.register(Business)
admin.site.register(WaiterFeedback)
admin.site.register(ProductFeedback)
admin.site.register(Waiter)
admin.site.register(CustomUser)