from django.contrib import admin
from.models import Business, Feedback, CustomUser,Waiter

# Register your models here.
admin.site.register(Business)
admin.site.register(Feedback)
admin.site.register(Waiter)
admin.site.register(CustomUser)