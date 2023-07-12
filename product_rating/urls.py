from .views import ProductRatingListCreateAPIView
from django.urls import path

urlpatterns = [
    path('product-rating/', ProductRatingListCreateAPIView.as_view(), name='product-rating'),
]
