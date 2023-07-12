from django.urls import path

from .views import WaiterRatingListCreateAPIView

urlpatterns = [
    path('waiter-rating/', WaiterRatingListCreateAPIView.as_view(), name='waiter-rating'),
]
