from io import BytesIO

import qrcode
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.db import models
from django.utils import timezone


# Create your models here.

class SIModel(models.Model):
    class Meta:
        app_label = 'si_model'
        abstract = True

    date_created = models.DateTimeField('Data e krijimit', auto_now_add=True)
    date_last_updated = models.DateTimeField('Data e modifikimit', auto_now=True)

    def __id__(self) -> int:
        return self.id


class Business(SIModel):
    class Meta:
        verbose_name = 'Biznesi'
        verbose_name_plural = 'Bizneset'
        db_table = 'si_business'
        ordering = ['name']

    name = models.CharField('Emri i biznesit', max_length=150)
    address = models.CharField('Adresa', max_length=100, null=True, blank=True)
    nipt = models.CharField('NIPT', max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extsi_fields):
        '''
        Creates and saves a User with the given username and password.
        '''
        user = self.model(email=email, **extsi_fields)
        user.email = email
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extsi_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extsi_fields)
        user.email = email
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extsi_fields):
        extsi_fields.setdefault('is_staff', True)
        extsi_fields.setdefault('is_superuser', True)
        extsi_fields.setdefault('is_active', True)
        if extsi_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extsi_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extsi_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Administratori'
        verbose_name_plural = 'Administratorët'
        db_table = 'si_admin'

    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='admins', null=True,
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
        db_table = 'si_action_logger'

    action_time = models.DateTimeField('Action time', default=timezone.now, editable=False)
    user = models.ForeignKey(CustomUser, models.CASCADE, verbose_name='CustomUser', null=True)
    user_ip = models.CharField('User IP', max_length=20, blank=True)
    content_type = models.ForeignKey(ContentType, models.SET_NULL, verbose_name='Content Type', blank=True, null=True)
    object_id = models.TextField('Object id', blank=True, null=True)
    object_repr = models.CharField('Object repr', max_length=200)
    action_flag = models.PositiveSmallIntegerField('Action flag')
    change_message = models.TextField('Change message', blank=True)
    objects = ACLogEntryManager()


class Waiter(SIModel):
    class Meta:
        verbose_name = 'Kamarieri'
        verbose_name_plural = 'Kamarierët'
        db_table = 'si_waiter'
        ordering = ['first_name']

    first_name = models.CharField('Emri', max_length=50)
    last_name = models.CharField('Mbiemri', max_length=50)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='waiters', null=True,
                                 blank=True)
    # Generate a unique QR code for each waiter
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class WaiterRating(SIModel):
    class Meta:
        verbose_name = 'Vlerësimi për kamarierin'
        verbose_name_plural = 'Vlerësimet për kamarierin'
        db_table = 'si_waiter_rating'
        ordering = ['rating']

    rating = models.PositiveIntegerField('Vlerësimi')
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE, related_name='waiter_ratings', null=True, blank=True)
    client_device = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.rating)


class Menu(SIModel):
    class Meta:
        verbose_name = 'Menuja'
        verbose_name_plural = 'Menutë'
        db_table = 'si_menu'

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='menus')

    def __str__(self):
        return str(f'{self.business.name} - Menuja')


class Category(SIModel):
    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategortë'
        db_table = 'si_category'

    name = models.CharField(max_length=20)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return str(f'{self.menu.business.name} - {self.name}')


class Product(SIModel):
    class Meta:
        verbose_name = 'Produkti'
        verbose_name_plural = 'Produktet'
        db_table = 'si_product'

    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return str(self.name)


class CategoryRating(SIModel):
    class Meta:
        verbose_name = 'Vlerësimi për kategorinë'
        verbose_name_plural = 'Vlerësimet për kategorinë'
        db_table = 'si_category_rating'

    rating = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_ratings')

    def __str__(self):
        return str(self.rating)


class ProductRating(SIModel):
    class Meta:
        verbose_name = 'Vlerësimi për produktin'
        verbose_name_plural = 'Vlerësimet për produktin'
        db_table = 'si_product_rating'

    rating = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')

    def __str__(self):
        return str(self.rating)
