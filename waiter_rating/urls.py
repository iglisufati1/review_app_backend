from .views import WaiterRatingListCreateAPIView, WaiterRatingRUDAPIView
from django.urls import path
urlpatterns = [
    path('waiter-rating/', WaiterRatingListCreateAPIView.as_view(), name='waiter-rating'),
    path('waiter-rating/<int:pk>', WaiterRatingRUDAPIView.as_view(), name='waiter-rating-update'),
]