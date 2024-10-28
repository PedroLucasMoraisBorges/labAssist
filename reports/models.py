from django.db import models
import uuid

# Foreign keys models imports
from auth_user.models import *
from reagents.models import *

from datetime import date, datetime, timedelta
from django.utils import timezone

typeMovementChoices = [
    ('A', 'Adição'),
    ('R', 'Remoção'),
    ('T', 'Transferência')
]

# Create your models here.
class Movement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    motivation = models.CharField(max_length=288)
    amount = models.IntegerField()
    movement_type = models.CharField(max_length=64, choices=typeMovementChoices)
    dt_movement = models.DateTimeField()
    validity = models.DateField(null=True)

    fk_reagent = models.ForeignKey(Reagent, related_name='reagent_movement', null=False, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(User, related_name='responsible_movement', null=False,  on_delete=models.CASCADE)

    @property
    def formatted_dt_movement(self):
        return self.dt_movement.strftime('%d/%m/%Y')
    
    @property
    def formatted_dt_validity(self):
        if self.validity == None:
            return ''
        return self.validity.strftime('%d/%m/%Y')
    
    def __str__(self):
        year = str(self.dt_movement.year)
        month = str(self.dt_movement.month)
        day = str(self.dt_movement.day)
        return self.fk_reagent.name + ' ' + self.movement_type + ' '+ day + '/' + month + '/' + year
    
    class Meta:
        permissions = [
            ("can_add_movement", "Criar Movimentação")
        ]

class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approved = models.BooleanField(default=False)
    dt_request = models.DateTimeField()
    dt_response = models.DateTimeField(null=True, default=None, blank=True)

    fk_movement = models.ForeignKey(Movement, related_name='request_movement', null=False, on_delete=models.CASCADE)

    def __str__(self):
        year = str(self.dt_request.year)
        month = str(self.dt_request.month)
        day = str(self.dt_request.day)
        return self.fk_movement.fk_user.name + ' ' + day + '/' + month + '/' + year

class License(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt_register = models.DateField()
    pdf = models.FileField(upload_to='pdfs/', unique=True)
    is_expired = models.BooleanField(default=False)

    def days_until_expiration(self):
        # Data alvo é um ano após a data de registro
        expiration_date = self.dt_register + timedelta(days=365)
        # Calcula a diferença entre a data de hoje e a data de expiração
        days_left = (expiration_date - timezone.now().date()).days
        return max(days_left, 0)  # Retorna 0 se já tiver expirado