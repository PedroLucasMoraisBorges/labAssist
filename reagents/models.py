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
    name = models.CharField(max_length=144, unique=True)
    formula = models.CharField(max_length=144)
    limit = models.IntegerField()
    classification = models.CharField(max_length=64)
    incompatibility = models.ManyToManyField('self', blank=True)
    control = models.CharField(max_length=144, choices=controlChoices)
    state = models.CharField(max_length=64, choices=statesChoices)
    opening_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ("can_add_reagent", "Can add reagent"),
            ("can_change_reagent", "Can change reagent"),
            ("can_delete_reagent", "Can delete reagent"),
            ("can_view_reagent", "Can view reagent"),
        ]

class ReagentBatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField()
    size = models.IntegerField()
    validity = models.DateField()
    fk_reagent = models.ForeignKey(Reagent, related_name='reagent_batch', null=False, on_delete=models.CASCADE)

    @property
    def formatted_validity(self):
        return self.validity.strftime('%d/%m/%Y')