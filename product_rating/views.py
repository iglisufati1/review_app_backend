from common.api_views import ReviewAppListCreateAPIView
from model.models import WaiterRating

from .serializers import ProductRatingWriteSerializer, ProductRatingReadSerializer


# Create your views here.
class ProductRatingListCreateAPIView(ReviewAppListCreateAPIView):
    queryset = WaiterRating.objects.all()
    write_serializer_class = ProductRatingWriteSerializer
    read_serializer_class = ProductRatingReadSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = BusinessFilterSerializer
