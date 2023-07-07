from common.api_views import ReviewAppListCreateAPIView
from model.models import Waiter

from .serializers import WaiterWriteSerializer, WaiterReadSerializer


# Create your views here.

class WaiterListCreateAPIView(ReviewAppListCreateAPIView):
    queryset = Waiter.objects.all()
    write_serializer_class = WaiterWriteSerializer
    read_serializer_class = WaiterReadSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = BusinessFilterSerializer
