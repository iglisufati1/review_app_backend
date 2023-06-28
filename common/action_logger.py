from django.contrib.contenttypes.models import ContentType

from model.models import ACActionLogger

ADDITION = 1
CHANGE = 2
DELETION = 3
CHANGE_PASSWORD = 4
LOGIN = 5
LOGOUT = 6
OTHER = 7


def log_addition(user_id, request, model_object):
    log_action(user_id, request, model_object, ADDITION, 'Krijoi: {}'.format(model_object._meta.verbose_name.title()))


def log_change(user_id, request, model_object):
    log_action(user_id, request, model_object, CHANGE, 'Ndryshoi: {}'.format(model_object._meta.verbose_name.title()))


def log_deletion(user_id, request, model_object):
    log_action(user_id, request, model_object, DELETION, 'Fshiu: {}'.format(model_object._meta.verbose_name.title()))


def log_action(user_id, request, model_object, action, message):
    content_type_id = ContentType.objects.get_for_model(model_object._meta.model).id
    user_ip = get_client_ip(request)
    create_log_action(user_id, user_ip, content_type_id, model_object.pk, model_object, action, message)


def create_log_action(user_id, user_ip, content_type_id, object_id, model_object, action_flag, message):
    ACActionLogger.objects.log_action(user_id=user_id,
                                      user_ip=user_ip,
                                      content_type_id=content_type_id,
                                      object_id=object_id,
                                      object_repr=model_object.__str__(),
                                      action_flag=action_flag,
                                      change_message=message)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
