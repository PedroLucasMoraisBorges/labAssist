from django import forms
from .models import *
from reagents.models import *
from django.db.models import Q

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