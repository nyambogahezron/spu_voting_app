from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(null=True, unique=True)
	avatar = models.ImageField(null=True, default='avatar.svg')
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

