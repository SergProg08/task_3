from datetime import datetime, timedelta
import uuid
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager,
)
from constance import config

REFRESH_TOKEN_LIFETIME_DAYS = config.TIME_VALID_REFRESH_TOKEN_DAYS


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
Creates and saves a User with the given email,and password.
"""
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception:
            raise 

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
An abstract base class implementing a fully featured User model

"""
    username = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class MyRefreshToken(models.Model):

    """ Model for local refresh token stored in DB """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='refresh_token')
    value = models.UUIDField(default=uuid.uuid4())
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='creation time')
    expired_at = models.DateTimeField(
        default=(datetime.now() + timedelta(days=int(REFRESH_TOKEN_LIFETIME_DAYS))),
        verbose_name='expired time')

    @classmethod
    def create(cls, user):
        token = cls.objects.create(
            user=user,
            value=uuid.uuid4())
        return token

    @classmethod
    def update(cls, user):
        token_old = cls.objects.get(user=user).delete()
        token_new = cls.create(user)
        return token_new
