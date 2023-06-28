from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
import os
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class RAModel(models.Model):
    class Meta:
        app_label = 'ra_model'
        abstract = True

    date_created = models.DateTimeField('Data e krijimit', auto_now_add=True)
    date_last_updated = models.DateTimeField('Data e modifikimit', auto_now=True)

    def __id__(self) -> int:
        return self.id


class Business(RAModel):
    class Meta:
        verbose_name = 'Biznesi'
        verbose_name_plural = 'Bizneset'
        db_table = 'ra_business'
        ordering = ['name']

    name = models.CharField('Emri i biznesit', max_length=150)
    address = models.CharField('Adresa', max_length=100, null=True, blank=True)
    nipt = models.CharField('NIPT', max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        '''
        Creates and saves a User with the given username and password.
        '''
        user = self.model(email=email, **extra_fields)
        user.email = email
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.email = email
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_admins', null=True,
                                 blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ACLogEntryManager(models.Manager):
    use_in_migrations = True

    def log_action(self, user_id, user_ip, content_type_id, object_id, object_repr, action_flag, change_message=''):
        if isinstance(change_message, list):
            change_message = json.dumps(change_message)
        self.model.objects.create(
            user_id=user_id,
            user_ip=user_ip,
            content_type_id=content_type_id,
            object_id=object_id,
            object_repr=object_repr[:200],
            action_flag=action_flag,
            change_message=change_message)


class ACActionLogger(models.Model):
    class Meta:
        verbose_name = 'Action Logger'
        verbose_name_plural = 'Action Loggers'
        db_table = 'action_logger'

    action_time = models.DateTimeField('Action time', default=timezone.now, editable=False)
    user = models.ForeignKey(CustomUser, models.CASCADE, verbose_name='CustomUser', null=True)
    user_ip = models.CharField('User IP', max_length=20, blank=True)
    content_type = models.ForeignKey(ContentType, models.SET_NULL, verbose_name='Content Type', blank=True, null=True)
    object_id = models.TextField('Object id', blank=True, null=True)
    object_repr = models.CharField('Object repr', max_length=200)
    action_flag = models.PositiveSmallIntegerField('Action flag')
    change_message = models.TextField('Change message', blank=True)
    objects = ACLogEntryManager()


class Waiter(RAModel):
    class Meta:
        verbose_name = 'Kamarieri'
        verbose_name_plural = 'Kamarierët'
        db_table = 'ra_waiter'
        ordering = ['first_name']

    first_name = models.CharField('Emri', max_length=50)
    last_name = models.CharField('Mbiemri', max_length=50)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_waiters', null=True,
                                 blank=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Feedback(RAModel):
    class Meta:
        verbose_name = 'Vlerësimi'
        verbose_name_plural = 'Vlerësimet'
        db_table = 'ra_feedback'
        ordering = ['rating']

    rating = models.PositiveIntegerField('Vlerësimi')
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)

    def __str__(self):
        return str(self.rating)



