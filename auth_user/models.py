from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import *
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique = True, blank = False)
    nome = models.CharField(max_length = 256)

    # Especificar related_name para evitar conflitos
    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',  # Nome alternativo para evitar conflito
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',  # Nome alternativo para evitar conflito
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    object = UserManager()

    def __str__(self):
        return self.nome