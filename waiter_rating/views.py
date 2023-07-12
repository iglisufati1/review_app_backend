from django.shortcuts import render
from common.api_views import ReviewAppListCreateAPIView, ReviewAppRetrieveUpdateDestroyAPIView
from model.models import WaiterRating
from .serializers import WaiterRatingWriteSerializer, WaiterRatingReadSerializer

# Create your views here.
class WaiterRatingListCreateAPIView(ReviewAppListCreateAPIView):
    queryset = WaiterRating.objects.all()
    write_serializer_class = WaiterRatingWriteSerializer
    read_serializer_class = WaiterRatingReadSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = BusinessFilterSerializer


class WaiterRatingRUDAPIView(ReviewAppRetrieveUpdateDestroyAPIView):
    queryset = WaiterRating.objects.all()
    write_serializer_class = WaiterRatingWriteSerializer
    read_serializer_class = WaiterRatingReadSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = BusinessFilterSerializer