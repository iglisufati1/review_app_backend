from django.shortcuts import render
from model.models import Business
from business.serializers import BusinessWriteSerializer, BusinessReadSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from common.api_views import ReviewAppListCreateAPIView, ReviewAppRetrieveUpdateDestroyAPIView
# Create your views here.


class BusinessListCreateAPIView(ReviewAppListCreateAPIView):
    queryset = Business.objects.all()
    write_serializer_class = BusinessWriteSerializer
    read_serializer_class = BusinessReadSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = BusinessFilterSerializer

class BusinessRUDAPIView(ReviewAppRetrieveUpdateDestroyAPIView):
    queryset = Business.objects.all()
    write_serializer_class = BusinessWriteSerializer
    read_serializer_class = BusinessReadSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = BusinessFilterSerializer
