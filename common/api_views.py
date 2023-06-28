import json
import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.transaction import atomic
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from common.paginators import ReviewAppPaginator20
from .action_logger import ADDITION, log_addition, CHANGE, log_change, DELETION, log_deletion
from .cons import DATA, ERROR_TYPE, ERRORS, MESSAGE, VALIDATION_ERROR, HTTP_404, INTEGRITY_ERROR, INVALID_DATA, OTHER
from .exceptions import InvalidData, APIException202

logger = logging.getLogger(__name__)


class ReviewAppListAPIView(ListAPIView):
    pagination_class = ReviewAppPaginator20
    queryset = None
    serializer_class = None
    filter_serializer_class = None
    filter_map = {}
    queryset_kwargs = {}


# @permission_classes([CanAdd])
class ReviewAppCreateAPIView(CreateAPIView):

    @atomic
    def create(self, request, *args, **kwargs):
        data = {}
        if 'data' in request.data:  # POST request with FILES
            for key in request.FILES.keys():
                data[key] = request.FILES[key]
            post_data = json.loads(request.data['data'])
            data.update(post_data)
        else:  # SIMPLE POST request
            data = request.data
        serializer = self.get_serializer(data=data)

        response_data = {}
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_headers = None
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response_data = {DATA: serializer.data}
            response_status = status.HTTP_201_CREATED
            response_headers = headers
            track_action(request, serializer, ADDITION)
        except ValidationError as ve:
                            logger.error('Create Error: {}'.format(ve))
                            error_dict = ve.get_full_details()
                            response_data = {
                                ERROR_TYPE: VALIDATION_ERROR,
                                ERRORS: error_dict,
                                MESSAGE: get_validation_error_message(error_dict)
                            }
                            response_status = status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist as dne:
            logger.error('Object does not exist Error: {}'.format(dne))
            response_data = {
                ERROR_TYPE: HTTP_404,
                ERRORS: '{}'.format(dne),
                MESSAGE: 'Nuk ekziston',
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except IntegrityError as ie:
            logger.error('{}'.format(ie))
            response_data = {
                ERROR_TYPE: INTEGRITY_ERROR,
                ERRORS: '{}'.format(ie),
                MESSAGE: 'Gabim në databazë',
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except InvalidData as ex:
            response_data = {
                ERROR_TYPE: INVALID_DATA,
                ERRORS: ex.get_message(),
                MESSAGE: ex.get_message(),
            }
            response_status = status.HTTP_400_BAD_REQUEST
        except APIException202 as ae:
            headers = self.get_success_headers(serializer.data)
            response_data = {DATA: ae.obj, MESSAGE: ae.message}
            response_status = status.HTTP_202_ACCEPTED
            response_headers = headers
        except Exception as e:
            response_data = {
                ERROR_TYPE: OTHER,
                ERRORS: '{}'.format(e),
                MESSAGE: 'Problem në server'
            }
        finally:
            return Response(response_data, status=response_status, headers=response_headers)


# @permission_classes([HasPermissionKeycloakCustom])
class ReviewAppListCreateAPIView(ReviewAppListAPIView, ReviewAppCreateAPIView):
    list_read_serializer_class = None
    read_serializer_class = None
    write_serializer_class = None
    filter_serializer_class = None
    serializer_error_msg = "'%s' should either include a `serializer_class` attribute, or override the " \
                           "`get_serializer_class()` method."
    queryset = None
    filter_map = {}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.list_read_serializer_class is not None:
                return self.list_read_serializer_class
            if self.read_serializer_class is not None:
                return self.read_serializer_class
            if self.serializer_class is not None:
                return self.serializer_class
            raise AssertionError(self.serializer_error_msg % self.__class__.__name__)
        if self.request.method == 'POST':
            if self.write_serializer_class is not None:
                return self.write_serializer_class
            if self.serializer_class is not None:
                return self.serializer_class
            raise AssertionError(self.serializer_error_msg % self.__class__.__name__)
        raise MethodNotAllowed(self.request.method, '', status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewAppRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = None
    serializer_class = None
    read_serializer_class = None
    write_serializer_class = None
    serializer_error_msg = "'%s' should either include a `serializer_class` attribute, or override the " \
                           "`get_serializer_class()` method."
    delete_obj_id_physical = None

    # permission_classes = [Or(And(IsReadOnlyRequest, CanView),
    #                          And(IsPutPatchRequest, CanChange))]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.read_serializer_class is not None:
                return self.read_serializer_class
            if self.serializer_class is not None:
                return self.serializer_class
            raise AssertionError(self.serializer_error_msg % self.__class__.__name__)
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            if self.write_serializer_class is not None:
                return self.write_serializer_class
            if self.serializer_class is not None:
                return self.serializer_class
            raise AssertionError(self.serializer_error_msg % self.__class__.__name__)
        raise MethodNotAllowed(self.request.method, '', status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({DATA: serializer.data})
        except Http404 as e:
            response_data = {
                ERROR_TYPE: HTTP_404,
                ERRORS: '{}'.format(e),
                MESSAGE: 'Nuk u gjet'
            }
            response_status = status.HTTP_404_NOT_FOUND
            return Response(response_data, status=response_status)

    @atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = {}
        if 'data' in request.data:  # POST request with FILES
            for key in request.FILES.keys():
                data[key] = request.FILES[key]
            post_data = json.loads(request.data['data'])
            data.update(post_data)
        else:  # SIMPLE POST request
            data = request.data
        serializer = self.get_serializer(instance, data=data, partial=partial)

        response_data = {}
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_serializer = self.read_serializer_class(instance)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            response_data = {DATA: response_serializer.data}
            response_status = status.HTTP_200_OK
            track_action(request, serializer, CHANGE)
        except ValidationError as ve:
            logger.error('Create Error: {}'.format(ve))
            error_dict = ve.get_full_details()
            response_data = {
                ERROR_TYPE: VALIDATION_ERROR,
                ERRORS: error_dict,
                MESSAGE: get_validation_error_message(error_dict)
            }
            response_status = status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist as dne:
            logger.error('Object does not exist Error: {}'.format(dne))
            response_data = {
                ERROR_TYPE: HTTP_404,
                ERRORS: '{}'.format(dne),
                MESSAGE: 'Nuk ekziston',
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except IntegrityError as ie:
            logger.error('{}'.format(ie))
            response_data = {
                ERROR_TYPE: INTEGRITY_ERROR,
                ERRORS: '{}'.format(ie),
                MESSAGE: 'Gabim në databazë',
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except InvalidData as ex:
            response_data = {
                ERROR_TYPE: INVALID_DATA,
                ERRORS: ex.get_message(),
                MESSAGE: ex.get_message(),
            }
            response_status = status.HTTP_400_BAD_REQUEST
        except APIException202 as ae:
            response_data = {DATA: ae.obj, MESSAGE: ae.message}
            response_status = status.HTTP_202_ACCEPTED
        except Exception as e:
            response_data = {
                ERROR_TYPE: OTHER,
                ERRORS: '{}'.format(e),
                MESSAGE: 'Problem në server'
            }
        finally:
            return Response(response_data, status=response_status)


# @permission_classes([HasPermissionKeycloakCustom])
class ReviewAppRetrieveUpdateDestroyAPIView(ReviewAppRetrieveUpdateAPIView, DestroyAPIView):
    # permission_classes = [Or(And(IsReadOnlyRequest, CanView),
    #                          And(IsDeleteRequest, CanDelete),
    #                          And(IsPutPatchRequest, CanChange))]

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            track_action(request, instance, DELETION)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404 as e:
            response_data = {
                ERROR_TYPE: HTTP_404,
                ERRORS: '{}'.format(e),
                MESSAGE: 'Nuk u gjet'
            }
            response_status = status.HTTP_404_NOT_FOUND
            return Response(response_data, status=response_status)


def get_validation_error_message(error_data):
    try:
        response_message = ''
        if isinstance(error_data, dict):
            for key, value in error_data.items():
                for item in value:
                    if 'message' in item:
                        response_message += '{}: {} '.format(key, item['message'])
                    else:
                        if isinstance(item, dict):
                            for unit_key, unit_value in item.items():
                                for arr_item in unit_value:
                                    response_message += '{}: {} '.format(unit_key, arr_item['message'])
                        elif isinstance(item, str):
                            for item_key, item_val in value.items():
                                for arr_item in item_val:
                                    response_message += '{}: {} '.format(item_key, arr_item['message'])
        elif isinstance(error_data, list):
            for arr_item in error_data:
                response_message += '{} '.format(arr_item['message'])
    except:
        response_message = 'Error {}'.format(error_data)
    return response_message


def track_action(request, serializer, action):
    action_user_id = None if request.user.is_anonymous else request.user.id
    if hasattr(serializer, 'instance'):
        model_obj = serializer.instance
    else:
        model_obj = serializer
    if action == ADDITION:
        log_addition(action_user_id, request, model_obj)
    elif action == CHANGE:
        log_change(action_user_id, request, model_obj)
    elif action == DELETION:
        log_deletion(action_user_id, request, model_obj)
