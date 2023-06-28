from .views import BusinessListCreateAPIView
from django.urls import path
urlpatterns = [
    path('business/', BusinessListCreateAPIView.as_view(), name='business'),
]