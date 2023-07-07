from .views import WaiterListCreateAPIView
from django.urls import path
urlpatterns = [
    path('waiter/', WaiterListCreateAPIView.as_view(), name='business'),
]