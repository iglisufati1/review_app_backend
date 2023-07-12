from .views import BusinessListCreateAPIView, BusinessRUDAPIView
from django.urls import path
urlpatterns = [
    path('business/', BusinessListCreateAPIView.as_view(), name='business'),
    path('business/<int:pk>', BusinessRUDAPIView.as_view(), name='business-update'),
]