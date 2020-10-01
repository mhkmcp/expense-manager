from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('User should have a Username')

        if email is None:
            raise TypeError('User should have a Email')

        user = self.model(username=username,
                          email=self.normalize_email(email),
                          )
        user.set_password(password)
        # user.is_superuser = False
        # user.is_staff = False
        # user.is_active = True
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('User should have a Password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = False
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255, db_index=True)
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    is_varified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        return ''
