from django.db import models
import uuid

statesChoices = [
    ('L', 'Líquido'),
    ('S', 'Sólido')
]

controlChoices = [
    ('LI', 'Livre'),
    ('PF', 'Polícia Federal'),
    ('EX', 'Exército')
]

# Create your models here
class Reagent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=144)
    formula = models.CharField(max_length=144)
    size = models.IntegerField()
    amount = models.IntegerField(default=0)
    limit = models.IntegerField()
    validity = models.DateField()
    classification = models.CharField(max_length=64)
    incompatibility = models.ManyToManyField('self', blank=True)
    control = models.CharField(max_length=144, choices=controlChoices)
    state = models.CharField(max_length=64, choices=statesChoices)
    opening_date = models.DateField(null=True)

    def __str__(self):
        return self.name