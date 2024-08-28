from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import *
import uuid

# Listas
sectorChoice = [
    ('B' , 'Bolsista'),
    ('P', 'Professor')
]

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique = True, blank = False)
    nome = models.CharField(max_length = 256)
    setor = models.CharField(max_length=64, choices=sectorChoice)

    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    object = UserManager()

    def __str__(self):
        return self.nome