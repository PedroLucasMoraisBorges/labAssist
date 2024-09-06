from django.db import models
import uuid

# Foreign keys models imports
from auth_user.models import *
from reagents.models import *

from datetime import date

typeMovementChoices = [
    ('A', 'Adição'),
    ('R', 'Remoção'),
    ('T', 'Transferência')
]

# Create your models here.
class Movement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    motivation = models.CharField(max_length=288)
    ammount = models.IntegerField()
    movement_type = models.CharField(max_length=64, choices=typeMovementChoices)
    dt_movement = models.DateTimeField()

    fk_reagent = models.ForeignKey(Reagent, related_name='reagent_movement', null=False, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(User, related_name='responsible_movement', null=False,  on_delete=models.CASCADE)

    def __str__(self):
        return self.fk_reagent.name + ' ' + self.movement_type

class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appoove = models.BooleanField(default=False)
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