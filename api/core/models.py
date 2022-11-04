from statistics import mode

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from rest_framework.authentication import TokenAuthentication


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    beer_drunk = models.FloatField(default=0)
    accurate_hits = models.IntegerField(default=0)
    total_hits = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    reputation = models.IntegerField(default=0)


class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    time = models.DateTimeField()
    participants = models.ManyToManyField(User)
    BEER_CHOICES = [
        ('330', 'small'),
        ('400', 'medium'),
        ('500', 'large')
    ]
    beer_class = models.CharField(
        max_length=3, choices=BEER_CHOICES, default='500')
