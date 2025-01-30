from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    roles = models.ManyToManyField('Role', related_name='users')
    
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    scopes = models.ManyToManyField('Scope', related_name='roles')

class Scope(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='groups')
