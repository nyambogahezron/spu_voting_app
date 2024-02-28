from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	name = models.CharField(max_length=200, null=True)
	username = models.CharField(unique=True, max_length=200, null=True)
	email = models.EmailField(null=True, unique=True)
	profile_image = models.ImageField(null=True, blank=True, default='user.svg')
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.name

