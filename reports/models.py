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

class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appoove = models.BooleanField(default=False)
    dt_request = models.DateTimeField(default=date.today)
    dt_response = models.DateTimeField()

    fk_movement = models.ForeignKey(Movement, related_name='request_movement', null=False, on_delete=models.CASCADE)

class License(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt_register = models.DateField()
    pdf = models.FileField(upload_to='pdfs/', unique=True)