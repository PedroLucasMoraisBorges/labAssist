from django.db import models
import uuid

statesChoices = [
    ('L', 'Líquido'),
    ('S', 'Sólido')
]

controlChoices = [
    ('LI', 'Livre'),
    ('PF', 'Polícia Federal'),
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
            ("can_add_reagent", "Cadastrar Reagente"),
            ("can_change_reagent", "Alterar Reagente"),
            ("can_delete_reagent", "Deletar Reagente"),
            ("can_view_reagent", "Ver Reagente"),
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

    def __str__(self):
        val = self.validity.strftime('%d/%m/%Y')
        return "Lote de {} - {}".format(self.fk_reagent.name, val)