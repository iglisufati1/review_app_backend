from .views import WaiterListCreateAPIView, WaiterRUDAPIView
from django.urls import path

urlpatterns = [
    path('waiter/', WaiterListCreateAPIView.as_view(), name='waiter'),
    path('waiter/<int:pk>', WaiterRUDAPIView.as_view(), name='waiter-update'),
]
