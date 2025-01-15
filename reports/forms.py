from django import forms
from .models import *
from reagents.models import *
from django.db.models import Q
from auth_user.models import *

class LicenseForm(forms.ModelForm):
    pdf = forms.FileField(
        label='Licensa',
        required=True,
        widget=forms.FileInput(attrs={'accept' : '.pdf'})
    )

    class Meta:
        model=License
        fields=['pdf']
    
class MovementForm(forms.ModelForm):
    motivation = forms.CharField(
        label='Motivação',
        required=True,
        widget=forms.Textarea()
    )

    amount = forms.IntegerField(
        label='Quantidade',
        required=True,
        widget=forms.NumberInput()
    )

    movement_type = forms.ChoiceField(
        label='Tipo de movimentação',
        required=True,
        choices=[('', 'Selecione um tipo')] + typeMovementChoices,
        widget=forms.Select()
    )

    fk_reagent = forms.ModelChoiceField(
        label='Reagente',
        required=True,
        queryset=Reagent.objects.filter(Q())
    )

    validity = forms.DateField(
        label='Validade',
        widget=forms.DateInput(attrs={'type' : 'date'}),
        required=False
    )

    size = forms.IntegerField(
        label='Tamanho do frasco',
        required=False,
    )

    class Meta:
        model=Movement
        fields=['motivation', 'amount', 'movement_type', 'fk_reagent', 'validity', 'size']


states_reagent = [
    ('L', 'Líquidos'),
    ('S', 'Sólidos'),
    ('A', 'Qualquer um')
]

status_reagent = [
    (True, 'Ativo'),
    (False, 'Passivo')
]

type_map = [
    ('A', 'Adição'),
    ('R', 'Retirada'),
    ('Q', 'Qualquer tipo')
]

class MovementHistoryForm(forms.Form):
    name = forms.CharField(
        required=True,
        label='Nome do Relatório',
    )

    item_status = forms.ChoiceField(
        label = 'Tipo de reagente',
        choices= statesChoices,
        widget= forms.SelectMultiple(attrs={'class' : 'js-example-basic-multiple', 'id' : 'select2'}),
        required=False
    )

    start_date = forms.DateField(
        label="Data de Início",
        required=True,
        widget=forms.DateInput(attrs={'type' : 'date',})
    )

    final_date = forms.DateField(
        label="Data de Fim",
        required=True,
        widget=forms.DateInput(attrs={'type' : 'date',})
    )

class UserPerformanceForm(forms.Form):
    name_report_user = forms.CharField(
        required=True,
        label='Nome do Relatório'
    )

    user = forms.ModelChoiceField(
        required=True,
        label='Usuário',
        queryset=User.objects.filter(~Q(sector='A')),
        widget=forms.Select()
    )

    start_date_user = forms.DateField(
        label="Data de Início",
        required=True,
        widget=forms.DateInput(attrs={'type' : 'date',})
    )

    final_date_user = forms.DateField(
        label="Data de Fim",
        required=True,
        widget=forms.DateInput(attrs={'type' : 'date',})
    )

class SiproquimMapForm(forms.Form):
    name_report_siproquim = forms.CharField(
        required=True,
        label='Nome do Relatório'
    )

    type_map = forms.ChoiceField(
        required=True,
        label="Tipo de mapa",
        choices=type_map,
        widget=forms.Select()
    )

    start_date_siproquim = forms.DateField(
        label="Data de Início",
        required=True,
        widget=forms.DateInput(attrs={'type' : 'date',})
    )

    final_date_siproquim = forms.DateField(
        label="Data de Fim",
        required=True,
        widget=forms.DateInput(attrs={'type' : 'date',})
    )