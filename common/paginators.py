from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ReviewAppPaginator20(PageNumberPagination):
    template = None
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 10

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     request = self.request
    #     if request and self.page_size_query_param:
    #         self.page_size = request.query_params.get(self.page_size_query_param, self.page_size)

    def get_paginated_response(self, data):
        return Response(OrderedDict({
            'data': data,
            'pagination': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            }
        }))


class ReviewAppPaginator10(ReviewAppPaginator20):
    page_size = 10
